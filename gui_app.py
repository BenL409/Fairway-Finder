import tkinter as tk
from tkinter import ttk

import requests
from tabulate import tabulate
from adjustments import get_temp_adjustment, get_wind_adjustment, get_wind_type
from courses import COURSES
from weather_test import API_KEY, LAT, LON

def run_forecast():
    selected_course = course_dropdown.get()
    if selected_course == "Pick a course":
        return
    course_data = COURSES[selected_course]
    lat, lon = course_data['lat'], course_data['lon']    
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        temp_c = data['main']['temp']
        wind_speed_mph = (data['wind']['speed'] * 2.237)
        wind_deg = data['wind']['deg']
        table_rows = []
        for i, heading in enumerate(course_data['headings'], 1):
            type_of_wind = get_wind_type(wind_deg, heading)
            total_adjustment = get_temp_adjustment(temp_c) + get_wind_adjustment(wind_speed_mph, wind_deg, heading)
            adj_str = f"+{total_adjustment} yards" if total_adjustment > 0 else f"{total_adjustment} yards" if total_adjustment < 0 else "No adjustment"
            table_rows.append((f"Hole {i}", type_of_wind.capitalize(), f"{adj_str}"))
        
        final_table = tabulate(table_rows, headers=["Hole", "Wind Type", "Adjustment"], tablefmt="simple")

        result_area.config(state="normal")
        result_area.delete(1.0, tk.END)
        result_area.insert(tk.END, f"Course: {selected_course}\nTemperature: {temp_c}°C Wind: {wind_deg}° @ {wind_speed_mph:.1f}mph \n\n")
        result_area.insert(tk.END, final_table)
        result_area.config(state="disabled")

    except requests.RequestException as e:
        result_area.config(state="normal")
        result_area.insert(tk.END, f"Error fetching weather data: {e}")    
        result_area.config(state="disabled")

root = tk.Tk()
root.title("Fairway Forecast")
root.geometry("400x650")

title = tk.Label(root, text="Fairway Forecast", font=("Helvetica", 16))
title.pack(pady=10)

tk.Label(root, text="Select a course:").pack(pady=5)
course_names = list(COURSES.keys())
course_dropdown = ttk.Combobox(root, values=course_names, state="readonly")
course_dropdown.pack(pady=5)
course_dropdown.set("Pick a course")

run_btn = tk.Button(root, text="Get Forecast", command=run_forecast, bg="#2ecc71", fg="white", font=("Helvetica", 12))
run_btn.pack(pady=20)


result_area = tk.Text(root, font=("Courier", 10), height=25, width=45, bg="#f0f0f0", padx=10, pady=10)
result_area.pack(pady=10)
result_area.config(state="disabled")

root.mainloop()
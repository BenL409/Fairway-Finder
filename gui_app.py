import tkinter as tk
from tkinter import ttk

import requests
from tabulate import tabulate
from adjustments import get_temp_adjustment, get_wind_adjustment, get_wind_type
from courses import COURSES
from weather_test import API_KEY

THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "long": "#e74c3c",
        "short": "#27ae60",
        "no_adj": "#3498db",
        "neutral": "#7f8c8d"
    },
    "dark": {
        "bg": "#2e2f30",
        "fg": "#ecf0f1",
        "long": "#e74c3c",
        "short": "#27ae60",
        "no_adj": "#3498db",
        "neutral": "#bdc3c7"
    }
}

current_theme = "light"

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

        result_area.config(state="normal")
        result_area.delete(1.0, tk.END)
        general_info = (
            f"COURSE: {selected_course}\n"
            f"TEMPERATURE: {temp_c}°C\n"
            f"WIND: {wind_speed_mph:.1f} mph at {wind_deg}°\n"
            f"{'=' * 35}\n\n"
        )
        result_area.insert(tk.END, general_info, "neutral")
        header = f"{'Hole':<8} {'Wind Type':<15} {'Adjustment':<10}\n"
        separator = "-" * 35 + "\n"
        result_area.insert(tk.END, header, "neutral")
        result_area.insert(tk.END, separator, "neutral")
        


        for i, heading in enumerate(course_data['headings'], 1):
            type_of_wind = get_wind_type(wind_deg, heading)
            total_adjustment = get_temp_adjustment(temp_c) + get_wind_adjustment(wind_speed_mph, wind_deg, heading)
            adj_str = f"+{total_adjustment}y" if total_adjustment > 0 else f"{total_adjustment}y" if total_adjustment < 0 else "---"
            row_str = f"Hole {i:<3}: {type_of_wind.capitalize():<15} {adj_str:<10}\n"
            if total_adjustment > 0:
                tag = "long"
            elif total_adjustment < 0:
                tag = "short"
            else:
                tag = "no_adj"     
                
            result_area.insert(tk.END, row_str, tag)
            
        result_area.config(state="disabled")
        
    except requests.RequestException as e:
        result_area.config(state="normal")
        result_area.insert(tk.END, f"Error fetching weather data: {e}")    
        result_area.config(state="disabled")
        
def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    theme = THEMES[current_theme]
    style.configure("TCombobox", fieldbackground=theme['bg'], foreground=theme['fg'])
    root.option_add("*TCombobox*Listbox.background", theme['bg'])
    root.option_add("*TCombobox*Listbox.foreground", theme['fg'])
    root.config(bg=theme['bg'])
    title.config(bg=theme['bg'], fg=theme['fg'])
    course_dropdown.config(background=theme['bg'], foreground=theme['fg'])
    run_btn.config(bg=theme['bg'], fg=theme['fg'])
    result_area.config(bg=theme['bg'], fg=theme['fg'])
    result_area.tag_config("long", foreground=theme['long'])
    result_area.tag_config("short", foreground=theme['short'])
    result_area.tag_config("no_adj", foreground=theme['no_adj'])
    theme_btn.config(text="Switch to Light Theme" if current_theme == "dark" else "Switch to Dark Theme")
    style.map('TCombobox', fieldbackground=[('readonly', theme['bg'])], foreground=[('readonly', theme['fg'])])
    course_dropdown.config(background=theme['bg'], foreground=theme['fg'])
    select_course_label.config(bg=theme['bg'], fg=theme['fg'])

root = tk.Tk()
root.title("Fairway Forecast")
root.geometry("400x700")

title = tk.Label(root, text="Fairway Forecast", font=("Helvetica", 16))
title.pack(pady=10)

style = ttk.Style()
style.map("TCombobox", fieldbackground=[("readonly", "#f0f0f0")], foreground=[("readonly", "#000000")])

select_course_label = tk.Label(root, text="Select a Course:", font=("Helvetica", 12))
select_course_label.pack(pady=5)
course_names = list(COURSES.keys())
course_dropdown = ttk.Combobox(root, values=course_names, state="readonly")
course_dropdown.pack(pady=5)
course_dropdown.set("Pick a course")

run_btn = tk.Button(root, text="Get Forecast", command=run_forecast, bg="#2ecc71", fg="white", font=("Helvetica", 12))
run_btn.pack(pady=20)

theme_btn = tk.Button(root, text="Switch to Dark Theme", command=toggle_theme, bg="#34495e", fg="white", font=("Helvetica", 10))
theme_btn.pack(pady=5)

result_area = tk.Text(root, font=("Courier", 10), height=25, width=45, bg="#f0f0f0", padx=10, pady=10)
result_area.tag_config("long", foreground="#e74c3c")
result_area.tag_config("short", foreground="#27ae60")
result_area.tag_config("no_adj", foreground="#3498db")
result_area.pack(pady=10)
result_area.config(state="disabled")

root.mainloop()
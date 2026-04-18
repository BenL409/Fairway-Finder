import requests

API_KEY = "c0f82587a3cd78b1b175925eb074e08c"

# Blankney Coordinates
LAT = 53.13
LON = -0.41

#Current weather API URL
url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url)
    data = response.json()
    wind_speed = (data['wind']['speed'] * 2.237)  # Convert m/s to mph

    if response.status_code == 200:
        print("Weather data retrieved successfully!")
        print("Current Weather Data:")
        print(f"Temperature: {data['main']['temp']}°C")
        print(f"Wind Speed: {wind_speed:.2f} mph")
    else:
        print(f"Error: {data['message']}")
except Exception as e:
    print(f"An error occurred: {e}")
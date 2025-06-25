import argparse
import requests
import sys
import json

API_KEY = '073812de6451d5a68ef2692fb0753226'  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print("Error fetching weather data:", response.json().get('message', 'Unknown error'))
        sys.exit(1)
    return response.json()

def list_options(weather_data):
    return list(weather_data['main'].keys()) + ['wind', 'weather']

def display_selected_info(weather_data, option):
    main = weather_data.get('main', {})
    wind = weather_data.get('wind', {})
    weather_desc = weather_data.get('weather', [{}])[0].get('description', None)

    if option in main:
        print(f"{option.capitalize()}: {main[option]}")
    elif option == 'wind':
        print(f"Wind speed: {wind.get('speed', 'N/A')} m/s")
    elif option == 'weather':
        print(f"Weather: {weather_desc}")
    else:
        print("Invalid option. Use --list to see available data points.")

def main():
    parser = argparse.ArgumentParser(description="Get weather forecast for a city.")
    parser.add_argument("city", help="City name to fetch weather for")
    parser.add_argument("--option", "-o", help="Specific weather data to display (e.g., temperature, humidity)")
    parser.add_argument("--list", action="store_true", help="List available weather data options")

    args = parser.parse_args()
    weather_data = get_weather(args.city)

    if args.list:
        print("Available data options:", ', '.join(list_options(weather_data)))
    elif args.option:
        display_selected_info(weather_data, args.option.lower())
    else:
        print("Full Weather Info:")
        print(json.dumps(weather_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
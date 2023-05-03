import requests
import tkinter as tk
from tkinter import ttk
import datetime


def get_weather_data(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()["list"]
        current_weather_data = weather_data[0]
        current_weather = {
            "location": location,
            "description": current_weather_data["weather"][0]["description"],
            "temperature": round(current_weather_data["main"]["temp"]),
            "humidity": current_weather_data["main"]["humidity"],
            "wind_speed": current_weather_data["wind"]["speed"],
        }
        forecast_weather_data = []
        for data in weather_data[1:]:
            forecast_weather = {
                "date": data["dt_txt"],
                "description": data["weather"][0]["description"],
                "temperature": round(data["main"]["temp"]),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            }
            forecast_weather_data.append(forecast_weather)

        return current_weather, forecast_weather_data
    else:
        return None


def display_weather_data(weather_data, output_label):
    if weather_data is not None:
        current_weather_data, forecast_weather_data = weather_data
        output_label.config(
            text=f'Current weather conditions in {current_weather_data["location"]}:\n'
            f'Description: {current_weather_data["description"]}\n'
            f'Temperature: {current_weather_data["temperature"]}°C\n'
            f'Humidity: {current_weather_data["humidity"]}%\n'
            f'Wind Speed: {current_weather_data["wind_speed"]} m/s\n\n'
            f"5-day weather forecast:\n"
        )
        table = ttk.Treeview(
            output_label, columns=("Date", "Description", "Temperature", "Humidity")
        )
        table.heading("Date", text="Date")
        table.heading("Description", text="Description")
        table.heading("Temperature", text="Average Temperature (°C)")
        table.heading("Humidity", text="Average Humidity (%)")
        table.column("#0", width=0, stretch=tk.NO)
        table.column("Date", width=150, anchor=tk.CENTER)
        table.column("Description", width=200, anchor=tk.CENTER)
        table.column("Temperature", width=200, anchor=tk.CENTER)
        table.column("Humidity", width=200, anchor=tk.CENTER)
        forecast_by_day = {}
        for forecast in forecast_weather_data:
            date_time = datetime.datetime.strptime(
                forecast["date"], "%Y-%m-%d %H:%M:%S"
            )
            date = date_time.strftime("%m/%d/%Y")
            if date not in forecast_by_day:
                forecast_by_day[date] = {
                    "description": forecast["description"],
                    "temperatures": [forecast["temperature"]],
                    "humidity": [forecast["humidity"]],
                }
            else:
                forecast_by_day[date]["temperatures"].append(forecast["temperature"])
                forecast_by_day[date]["humidity"].append(forecast["humidity"])
        for date, data in forecast_by_day.items():
            avg_temperature = round(
                sum(data["temperatures"]) / len(data["temperatures"]), 1
            )
            avg_humidity = round(sum(data["humidity"]) / len(data["humidity"]), 1)
            table.insert(
                "",
                tk.END,
                text="",
                values=(
                    date,
                    data["description"],
                    f"{avg_temperature}°C",
                    f"{avg_humidity}%",
                ),
            )
        table.pack(padx=10, pady=10)
    else:
        output_label.config(text="No weather data to display")


def get_weather():
    api_key = "YOUR_API_KEY_HERE"
    location = location_entry.get()
    weather_data = get_weather_data(api_key, location)
    display_weather_data(weather_data, output_label)


window = tk.Tk()
window.title("Weather App")
location_label = tk.Label(window, text="Location:")
location_entry = tk.Entry(window)
get_weather_button = tk.Button(window, text="Get Weather", command=get_weather)
output_label = tk.Label(window)
location_label.grid(row=0, column=0, padx=10, pady=10)
location_entry.grid(row=0, column=1, padx=10, pady=10)
get_weather_button.grid(row=0, column=2, padx=10, pady=10)
output_label.grid(row=1, column=0, columnspan=3)
window.mainloop()

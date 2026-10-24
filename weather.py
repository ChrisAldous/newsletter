import openmeteo_requests
import requests

weather_url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 40.297037,
    "longitude": -111.746702,
    "hourly": "temperature_2m",
    "timezone":"UTC-7",
    "temperature_unit":"fahrenheit",
    "forecast_days":1,
}
response = requests.get(weather_url, params=params)

# print(response.status_code)
# print(response.text)

if response.status_code == 200:
    data = response.json()
    # print(data)
    # print(f"This is the Data:\n{data["hourly"]["temperature_2m"]}")

    temp_by_hour = list(zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]))
    print(temp_by_hour)
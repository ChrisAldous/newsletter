import requests

def weather_report():
    weather_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 40.297037,
        "longitude": -111.746702,
        "hourly": "temperature_2m,weather_code",
        "timezone": "America/Denver",
        "temperature_unit": "fahrenheit",
        "forecast_days": 1,
    }

    try:
        response = requests.get(weather_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return list(zip(
            data["hourly"]["time"],
            data["hourly"]["temperature_2m"],
            data["hourly"]["weather_code"]
        ))

    except (requests.RequestException, KeyError, ValueError) as error:
        print(f"Weather error: {error}")
        return []

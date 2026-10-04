import requests

class pollutant_openmateo:
    @staticmethod
    def api_default_openmateo():
        return "https://air-quality-api.open-meteo.com/v1/air-quality"
    
    @staticmethod
    def fetch_data_openmateo():
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": -7.2756,
            "longitude": 112.7915,
            "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}


class weather_openmateo:
    @staticmethod
    def get_wmo_weather_desc(code):
        if code == 0:
            return "Cerah"
        elif code in [1, 2, 3]:
            return "Cerah Berawan"
        elif code in [45, 48]:
            return "Berkabut"
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return "Hujan"
        elif code in [95, 96, 99]:
            return "Hujan Badai"
        return "Cerah Berawan"

    @staticmethod
    def fetch_weather_timur():
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": -7.2756,
            "longitude": 112.7915,
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "hourly": "temperature_2m,wind_speed_10m,weather_code",
            "timezone": "Asia/Jakarta"
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            current = data.get("current", {})
            temp = current.get("temperature_2m")
            wind = current.get("wind_speed_10m")
            code = current.get("weather_code", 0)
            
            return {
                "status": "success",
                "location": "Surabaya Timur",
                "time_at": current.get("time"),
                "raw_data": {
                    "temperature_2m": temp,
                    "wind_speed_10m": wind,
                    "weather_code": code
                },
                "formatted": {
                    "temp": f"{round(temp)}°C" if temp is not None else "-",
                    "wind": f"{round(wind)} km/h" if wind is not None else "-",
                    "condition": weather_openmateo.get_wmo_weather_desc(code)
                },
                "hourly": data.get("hourly", {})
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
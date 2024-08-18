import requests
from SystemConfig.SystemConfig import SystemConfig
from datetime import datetime

class OpenWeatherService:
    def __init__(self):
        self.api_key = SystemConfig.API_KEY

    def get_weather(self, lat, lon):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'zh_tw'
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None

    def parse_weather(self, data, location_name):
        main = data.get('main', {})
        wind = data.get('wind', {})
        weather = data.get('weather', [{}])[0]
        temperature = main.get('temp')
        windspeed = wind.get('speed')
        weather_description = weather.get('description')
        timestamp = data.get('dt')
        
        # 將 Unix 時間戳轉換為 ISO 8601 格式
        last_updated = datetime.utcfromtimestamp(timestamp).isoformat()

        return {
            "location": location_name,
            "temperature": f"{temperature}°C",
            "windSpeed": f"{windspeed} m/s",
            "weatherDescription": weather_description,
            "lastUpdated": last_updated,
            "source": "OpenWeather"
        }
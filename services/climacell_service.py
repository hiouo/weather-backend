import requests
from datetime import datetime
from SystemConfig.SystemConfig import SystemConfig

class ClimacellService:
    def __init__(self):
        self.api_key = SystemConfig.CLIMACELL_KEY

    def get_weather(self, lat, lon):
        base_url = "https://api.tomorrow.io/v4/timelines"
        params = {
            'location': f"{lat},{lon}",
            'fields': ['temperature', 'windSpeed', 'weatherCode'],
            'timesteps': 'current',
            'units': 'metric',
            'apikey': self.api_key
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None

    def parse_weather(self, data, location_name):
        current = data.get('data', {}).get('timelines', [])[0].get('intervals', [])[0].get('values', {})
        temperature = current.get('temperature')
        windspeed = current.get('windSpeed')
        weather_code = current.get('weatherCode')
        timestamp = data.get('data', {}).get('timelines', [])[0].get('intervals', [])[0].get('startTime')

        # 將 ISO 8601 格式的時間轉換為更易讀的格式
        last_updated = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').isoformat()

        # 天氣描述映射表
        weather_descriptions = {
            "clear": "晴天",
            "partly_cloudy": "局部多雲",
            "cloudy": "多雲",
            "overcast": "陰天",
            "fog": "霧",
            "drizzle": "毛毛雨",
            "light_rain": "小雨",
            "rain": "雨",
            "heavy_rain": "大雨",
            "freezing_rain": "凍雨",
            "light_snow": "小雪",
            "snow": "雪",
            "heavy_snow": "大雪",
            "ice_pellets": "冰雹",
            "thunderstorm": "雷陣雨"
        }

        # 將天氣描述轉換為繁體中文
        weather_description_zh = weather_descriptions.get(weather_code, weather_code)

        return {
            "location": location_name,
            "temperature": f"{temperature}°C",
            "windSpeed": f"{windspeed:.2f} m/s",
            "weatherDescription": weather_description_zh,
            "lastUpdated": last_updated,
            "source": "Climacell"
        }
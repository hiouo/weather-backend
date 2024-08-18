import requests
from datetime import datetime
from SystemConfig.SystemConfig import SystemConfig

class WeatherAPIService:
    def __init__(self):
        self.api_key = SystemConfig.WEATHERAPI_KEY

    def get_weather(self, lat, lon):
        base_url = "https://api.weatherapi.com/v1/current.json"
        params = {
            'key': self.api_key,
            'q': f"{lat},{lon}",
            'lang': 'en'
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None

    def parse_weather(self, data, location_name):
        current = data.get('current', {})
        temperature = current.get('temp_c')
        windspeed = current.get('wind_kph') / 3.6  # 轉換為 m/s
        weather_description = current.get('condition', {}).get('text')
        last_updated = current.get('last_updated')

        # 天氣描述映射表
        weather_descriptions = {
            "Partly cloudy": "局部多雲",
            "Clear": "晴天",
            "Sunny": "陽光明媚",
            "Cloudy": "多雲",
            "Overcast": "陰天",
            "Mist": "薄霧",
            "Patchy rain possible": "可能有零星小雨",
            "Patchy snow possible": "可能有零星小雪",
            "Patchy sleet possible": "可能有零星雨夾雪",
            "Patchy freezing drizzle possible": "可能有零星凍毛毛雨",
            "Thundery outbreaks possible": "可能有雷陣雨",
            "Blowing snow": "吹雪",
            "Blizzard": "暴風雪",
            "Fog": "霧",
            "Freezing fog": "凍霧",
            "Patchy light drizzle": "零星小毛毛雨",
            "Light drizzle": "小毛毛雨",
            "Freezing drizzle": "凍毛毛雨",
            "Heavy freezing drizzle": "強凍毛毛雨",
            "Patchy light rain": "零星小雨",
            "Light rain": "小雨",
            "Moderate rain at times": "間歇性中雨",
            "Moderate rain": "中雨",
            "Heavy rain at times": "間歇性大雨",
            "Heavy rain": "大雨",
            "Light freezing rain": "小凍雨",
            "Moderate or heavy freezing rain": "中到大凍雨",
            "Light sleet": "小雨夾雪",
            "Moderate or heavy sleet": "中到大雨夾雪",
            "Patchy light snow": "零星小雪",
            "Light snow": "小雪",
            "Patchy moderate snow": "零星中雪",
            "Moderate snow": "中雪",
            "Patchy heavy snow": "零星大雪",
            "Heavy snow": "大雪",
            "Ice pellets": "冰雹",
            "Light rain shower": "小陣雨",
            "Moderate or heavy rain shower": "中到大陣雨",
            "Torrential rain shower": "暴雨",
            "Light sleet showers": "小雨夾雪陣雨",
            "Moderate or heavy sleet showers": "中到大雨夾雪陣雨",
            "Light snow showers": "小陣雪",
            "Moderate or heavy snow showers": "中到大陣雪",
            "Light showers of ice pellets": "小冰雹陣雨",
            "Moderate or heavy showers of ice pellets": "中到大冰雹陣雨",
            "Patchy light rain with thunder": "零星小雷雨",
            "Moderate or heavy rain with thunder": "中到大雷雨",
            "Patchy light snow with thunder": "零星小雷雪",
            "Moderate or heavy snow with thunder": "中到大雷雪"
        }

        # 將天氣描述轉換為繁體中文
        weather_description_zh = weather_descriptions.get(weather_description, weather_description)

        return {
            "location": location_name,
            "temperature": f"{temperature}°C",
            "windSpeed": f"{windspeed:.2f} m/s",
            "weatherDescription": weather_description_zh,
            "lastUpdated": last_updated,
            "source": "WeatherAPI"
        }
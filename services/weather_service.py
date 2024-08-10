import requests
from services.city_service import CityService
from SystemConfig.SystemConfig import SystemConfig

class WeatherService:
    def __init__(self):
        self.city_service = CityService()
        self.api_key = SystemConfig.API_KEY

    def get_weather(self, lat, lon):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,  # 從 SystemConfig 中讀取 API 密鑰
            'units': 'metric',  # 使用公制單位
            'lang': 'zh_tw'  # 使用繁體中文
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # 如果狀態碼不是 200，則引發 HTTPError
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None
    
    def update_weather_data(self, user_coords):
        city_dict = self.city_service.get_cities()
        distance_list = []

        # 計算每個地區與用戶位置的距離
        for city, districts in city_dict.items():
            for district, info in districts.items():
                city_coords = (info['lat'], info['lon'])
                distance = abs(user_coords[0] - city_coords[0]) + abs(user_coords[1] - city_coords[1])
                distance_list.append({
                    'city': city,
                    'district': district,
                    'name': info['name'],
                    'coordinates': city_coords,
                    'distance': distance
                })

        # 按距離排序並返回最近的10個地區
        sorted_distance_list = sorted(distance_list, key=lambda x: x['distance'])[:9]

        # 獲取這些地區的天氣數據
        weather_data_list = []
        for data in sorted_distance_list:
            weather_data = self.get_weather(data['coordinates'][0], data['coordinates'][1])
            if weather_data:
                weather_data_list.append({
                    'city': data['city'],
                    'district': data['district'],
                    'name': data['name'],
                    'weather': weather_data
                })

        return weather_data_list
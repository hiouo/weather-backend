from services.open_meteo_service import OpenMeteoService
from services.openweather_service import OpenWeatherService
from services.weatherapi_service import WeatherAPIService
from services.climacell_service import ClimacellService
from services.city_service import CityService

class WeatherService:
    def __init__(self):
        self.city_service = CityService()
        self.weather_services = {
            "OpenMeteo": OpenMeteoService(),
            "OpenWeather": OpenWeatherService(),
            "WeatherAPI": WeatherAPIService(),
            "Climacell": ClimacellService()
            # 可以在這裡添加更多的天氣 API 服務
        }

    def get_weather_data(self, lat, lon):
        city_dict = self.city_service.get_cities()
        distance_list = []

        for city, districts in city_dict.items():
            for district, info in districts.items():
                city_coords = (info['lat'], info['lon'])
                distance = abs(lat - city_coords[0]) + abs(lon - city_coords[1])
                distance_list.append({
                    'city': city,
                    'district': district,
                    'name': info['name'],
                    'coordinates': city_coords,
                    'distance': distance
                })

        sorted_distance_list = sorted(distance_list, key=lambda x: x['distance'])[:1]

        weather_data = []

        for data in sorted_distance_list:
            location_name = f"{data['city']} {data['district']}"
            for service_name, service in self.weather_services.items():
                api_data = service.get_weather(data['coordinates'][0], data['coordinates'][1])
                if api_data:
                    parsed_data = service.parse_weather(api_data, location_name)
                    weather_data.append(parsed_data)

        return weather_data
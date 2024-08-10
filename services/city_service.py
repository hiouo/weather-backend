import json
import os

class CityService:
    def __init__(self):
        self.city_name_mapping = self.load_city_name_mapping()

    def load_city_name_mapping(self):
        file_path = os.path.join('data', 'cities.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                cities_data = json.load(f)
                city_name_mapping = {}
                for city, districts in cities_data.items():
                    for district, info in districts.items():
                        city_name_mapping[district] = info['name']
                return city_name_mapping
        except FileNotFoundError:
            print("JSON file not found.")
            return {}
        except json.JSONDecodeError:
            print("Error decoding JSON file.")
            return {}

    def get_cities(self):
        file_path = os.path.join('data', 'cities.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("JSON file not found.")
            return {}
        except json.JSONDecodeError:
            print("Error decoding JSON file.")
            return {}

    def get_english_city_name(self, chinese_city_name):
        return self.city_name_mapping.get(chinese_city_name, chinese_city_name)
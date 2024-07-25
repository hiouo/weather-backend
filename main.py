from flask import Flask, jsonify, redirect, send_from_directory, request
import requests
from datetime import datetime, timedelta
from threading import Thread
import time
import math
import os

from SystemConfig.SystemConfig import System

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')

api_key = System.get_api_key()

class TaiwanCities:
    def __init__(self):
        self.cities = {
            "台北": {"name": "Taipei", "lat": 25.0330, "lon": 121.5654},
            "新北": {"name": "New Taipei", "lat": 25.0128, "lon": 121.4658},
            "桃園": {"name": "Taoyuan", "lat": 24.9931, "lon": 121.3000},
            "台中": {"name": "Taichung", "lat": 24.1477, "lon": 120.6736},
            "台南": {"name": "Tainan", "lat": 22.9999, "lon": 120.2270},
            "高雄": {"name": "Kaohsiung", "lat": 22.6273, "lon": 120.3014},
            "基隆": {"name": "Keelung", "lat": 25.1276, "lon": 121.7392},
            "新竹": {"name": "Hsinchu", "lat": 24.8138, "lon": 120.9675},
            "新竹縣": {"name": "Hsinchu County", "lat": 24.7033, "lon": 121.1252},
            "苗栗": {"name": "Miaoli", "lat": 24.4893, "lon": 120.9417},
            "彰化": {"name": "Changhua", "lat": 24.0685, "lon": 120.5575},
            "南投": {"name": "Nantou", "lat": 23.9608, "lon": 120.9719},
            "雲林": {"name": "Yunlin", "lat": 23.7074, "lon": 120.4313},
            "嘉義": {"name": "Chiayi", "lat": 23.4801, "lon": 120.4491},
            "屏東": {"name": "Pingtung", "lat": 22.6813, "lon": 120.4818},
            "宜蘭": {"name": "Yilan", "lat": 24.7021, "lon": 121.7378},
            "花蓮": {"name": "Hualien", "lat": 23.9769, "lon": 121.6044},
            "台東": {"name": "Taitung", "lat": 22.7583, "lon": 121.1444},
            "澎湖": {"name": "Penghu", "lat": 23.5711, "lon": 119.5795}
        }

    def get_cities(self):
        return self.cities

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'zh_tw'  # 使用繁體中文
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_forecast(city):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'zh_tw'  # 使用繁體中文
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def unix_to_readable(unix_time):
    # 將Unix時間戳轉換為UTC+8時間
    utc_time = datetime.utcfromtimestamp(unix_time)
    utc_plus_8_time = utc_time + timedelta(hours=8)
    return utc_plus_8_time.strftime('%Y-%m-%d %H:%M:%S')

def update_weather_data():
    global weather_data_list
    cities = TaiwanCities()
    city_dict = cities.get_cities()
    weather_data_list = []

    for zh_city, city_info in city_dict.items():
        weather_data = get_weather(city_info['name'])
        if weather_data:
            weather_info = {
                "zh_city": zh_city,
                "en_city": weather_data['name'],
                "temp": weather_data['main']['temp'],
                "description": weather_data['weather'][0]['description'],
                "data_time": unix_to_readable(weather_data['dt']),
                "lat": city_info['lat'],
                "lon": city_info['lon']
            }
            weather_data_list.append(weather_info)
        else:
            weather_info = {
                "zh_city": zh_city,
                "en_city": city_info['name'],
                "temp": "N/A",
                "description": "N/A",
                "data_time": "N/A",
                "lat": city_info['lat'],
                "lon": city_info['lon']
            }
            weather_data_list.append(weather_info)

def background_task():
    while True:
        update_weather_data()
        time.sleep(600)  # 每10分鐘更新一次

@app.route('/')
def index():
    return redirect('/weather')

@app.route('/weather')
def weather_page():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/future')
def future_page():
    return send_from_directory(app.static_folder, 'future.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/weather', methods=['GET'])
def get_weather_api():
    global weather_data_list
    return jsonify(weather_data_list)

@app.route('/api/future', methods=['POST'])
def future_weather():
    cities = TaiwanCities()
    city_dict = cities.get_cities()
    selected_city = request.json.get('city', '台北')
    forecast_data_list = []

    if selected_city:
        en_city = city_dict[selected_city]['name']
        forecast_data = get_forecast(en_city)
        if forecast_data:
            for entry in forecast_data['list']:
                forecast_info = {
                    "zh_city": selected_city,
                    "en_city": forecast_data['city']['name'],
                    "temp": entry['main']['temp'],
                    "description": entry['weather'][0]['description'],
                    "data_time": unix_to_readable(entry['dt'])
                }
                forecast_data_list.append(forecast_info)

    return jsonify(forecast_data_list)

@app.route('/api/sort_cities', methods=['POST'])
def sort_cities():
    user_lat = float(request.json['lat'])
    user_lon = float(request.json['lon'])
    cities = TaiwanCities().get_cities()

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # 地球半徑，單位為公里
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lat2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    sorted_cities = sorted(cities.items(), key=lambda city: haversine(user_lat, user_lon, city[1]['lat'], city[1]['lon']))
    print("Sorted cities based on distance:", sorted_cities)  # 調試信息

    # 創建一個字典來映射城市名稱到天氣數據
    weather_data_dict = {city['zh_city']: city for city in weather_data_list}
    sorted_weather_data = [weather_data_dict[city[0]] for city in sorted_cities if city[0] in weather_data_dict]
    
    print("Sorted weather data:", sorted_weather_data)  # 調試信息
    return jsonify(sorted_weather_data)

if __name__ == '__main__':
    weather_data_list = []
    update_weather_data()  # 初始化時更新一次數據
    thread = Thread(target=background_task)
    thread.daemon = True
    thread.start()
    app.run(host='0.0.0.0', port=80)
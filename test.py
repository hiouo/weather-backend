import requests

def get_weather(lat, lon):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': True,
        'timezone': 'Asia/Taipei'  # 設置時區為台北
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # 如果狀態碼不是 200，則引發 HTTPError
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
        return None

# 台北市大同區的經緯度
latitude = 25.0631  # 大同區的緯度
longitude = 121.5133  # 大同區的經度

weather_data = get_weather(latitude, longitude)

if weather_data:
    current_weather = weather_data.get('current_weather', {})
    temperature = current_weather.get('temperature')
    windspeed = current_weather.get('windspeed')
    weather_code = current_weather.get('weathercode')
    time = current_weather.get('time')

    # 天氣代碼對應的中文描述
    weather_descriptions = {
        0: "晴天",
        1: "主要晴天",
        2: "部分多雲",
        3: "多雲",
        45: "霧",
        48: "霧凇",
        51: "輕微毛毛雨",
        53: "中度毛毛雨",
        55: "強烈毛毛雨",
        56: "輕微凍雨",
        57: "強烈凍雨",
        61: "輕微雨",
        63: "中度雨",
        65: "強烈雨",
        66: "輕微凍雨",
        67: "強烈凍雨",
        71: "輕微雪",
        73: "中度雪",
        75: "強烈雪",
        77: "雪粒",
        80: "輕微陣雨",
        81: "中度陣雨",
        82: "強烈陣雨",
        85: "輕微陣雪",
        86: "強烈陣雪",
        95: "雷陣雨",
        96: "輕微冰雹雷陣雨",
        99: "強烈冰雹雷陣雨"
    }

    weather_description = weather_descriptions.get(weather_code, "未知天氣")

    # 打印結果
    print(f"地區: 台北市大同區")
    print(f"溫度: {temperature}°C")
    print(f"風速: {windspeed} m/s")
    print(f"天氣描述: {weather_description}")
    print(f"資料更新時間: {time}")
else:
    print("No weather data found")
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.weather_service import WeatherService
from services.user_location import UserLocation

app = Flask(__name__)
CORS(app)  # 啟用 CORS
weather_service = WeatherService()

@app.route('/api/weather', methods=['POST'])
def get_weather():
    user_location = UserLocation()

    if not user_location.is_valid():
        return jsonify({"error": "Invalid user location"}), 400

    weather_data = weather_service.get_weather_data(user_location.latitude, user_location.longitude)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "No weather data found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
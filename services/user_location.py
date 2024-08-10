from flask import request

class UserLocation:
    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.extract_location()

    def extract_location(self):
        if request.json:
            self.latitude = request.json.get('latitude')
            self.longitude = request.json.get('longitude')

    def is_valid(self):
        return self.latitude is not None and self.longitude is not None
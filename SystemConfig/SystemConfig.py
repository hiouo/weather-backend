class System:
    @staticmethod
    def get_api_key():
        with open("api_token.txt", "r") as file:
            return file.read().strip()
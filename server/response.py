from flask import jsonify

class Response:
    def __init__(self, message:str, data:dict) -> None:
        self.message = message
        self.data = data
    
    def send_success_response(self, status_code:int=200):
        return {
            "data": self.data,
            "message": self.message,
        }, status_code
    
    def send_failiure_response(self, status_code:int=400):
        return {
            "data": self.data,
            "message": self.message,
        }, status_code

    def __str__(self):
        return f"Response(message={self.message}, data={self.data})"

    def __repr__(self):
        return str(self)
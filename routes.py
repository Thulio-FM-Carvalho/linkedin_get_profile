from flask import request
from service import Service
from app import app

service = Service()


@app.route('/profileUrl', methods=['POST'])
def profile_url():
    data = request.get_json()
    data_str = data['data']
    profile_data = service.get_profile(data_str)
    return profile_data, 200


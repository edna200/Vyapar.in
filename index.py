import json
import datetime
import requests
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Function to add custom headers
def add_headers(response):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Server'] = 'Pro_Max_Futuristics'
    response.headers['Custom-Header'] = 'Pro_Max'
    return response

# Function to get data
def get_data():
    date = datetime.datetime.now()
    currentdt = date.strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "license_code": "jamiicodeless",
        "expiry_date": "2999-12-31 23:59:59",
        "plan": "Pos",
        "planId": 166,
        "status": 2,
        "created_at": "2022-01-01 00:00:00",
        "current_date": currentdt,
        "groupTitle": None,
        "planType": 3,
        "perDayCost": 0,
        "perDayCostUsd": 0,
        "pairExpiryDate": "2999-12-31 23:59:59"
    }
    return jsonify(data)

# Route for old API
@app.route('/api/license/<device_id>', methods=['GET', 'POST'])
def api_old(device_id):
    response = make_response(get_data())
    return add_headers(response)

# Route for new API
@app.route('/api/ns/license/<device_id>', methods=['GET', 'POST'])
def api_new(device_id):
    response = make_response(get_data())
    return add_headers(response)

# Route to forward requests to vyaparapp.in
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    url = f'https://vyaparapp.in/{path}'
    if request.method == 'GET':
        r = requests.get(url)
        response = make_response(r.text)
    elif request.method == 'POST':
        r = requests.post(url, data=request.form)
        response = make_response(r.text)
    return add_headers(response)

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    response = make_response(jsonify(error="Not Found"), 404)
    return add_headers(response)

@app.errorhandler(500)
def internal_server_error(e):
    response = make_response(jsonify(error="Internal Server Error"), 500)
    return add_headers(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
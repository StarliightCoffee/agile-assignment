from flask import Flask
import requests

app = Flask(__name__)

@app.route('/api/account-mgmt/healthcheck')
def healthcheck():
    return 'OK', 200

@app.route('/api/account-mgmt/get-user-name/<int:user_id>', methods=['GET'])
def get_user_name(user_id):
    response = requests.get(f"http://db-api:5431/api/db-api/get-user/{user_id}")
    if response.status_code != 200:
        return response.text, response.status_code
    return {'name': response.json()['name']}, 200

@app.route('/api/account-mgmt/get-user-type/<int:user_id>')
def get_user_type(user_id):
    response = requests.get(f"http://db-api:5431/api/db-api/get-user/{user_id}")
    if response.status_code != 200:
        return response.text, response.status_code
    return {'type': response.json()['type']}, 200

@app.route('/api/account-mgmt/get-user-email/<int:user_id>')
def get_user_email(user_id):
    response = requests.get(f"http://db-api:5431/api/db-api/get-user/{user_id}")
    if response.status_code != 200:
        return response.text, response.status_code
    return {'email': response.json()['email']}, 200

@app.route('/api/account-mgmt/get-user-phone-number/<int:user_id>')
def get_user_phone_number(user_id):
    response = requests.get(f"http://db-api:5431/api/db-api/get-user/{user_id}")
    if response.status_code != 200:
        return response.text, response.status_code
    return {'phone_number': response.json()['phone_number']}, 200

@app.route('/api/account-mgmt/get-user-membership-type/<int:user_id>')
def get_user_membership_type(user_id):
    response = requests.get(f"http://db-api:5431/api/db-api/get-user/{user_id}")
    if response.status_code != 200:
        return response.text, response.status_code
    return {'membership_type': response.json()['membership_type']}, 200

@app.route('/api/account-mgmt/delete-user/<int:user_id>')
def delete_user(user_id):
    response = requests.get(f"http://db-api:5431/api/db-api/")
    if response.status_code != 200:
        return response.text, response.status_code
    return 'User deleted', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5320)

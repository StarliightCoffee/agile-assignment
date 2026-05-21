from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/api/get-membership-status/<int:member_id>', methods=['GET'])
def get_membership_status(member_id):
    response = requests.get(f"http://db-api:5431/api/db-api/get-user/{member_id}")
    if response.status_code == 200:
        return 'Active', 200
    return 'Inactive', 200

@app.route('/api/change-user-membership', methods=['POST'])
def change_user_membership():
    data = request.get_json()
    user_id = data.get("user_id")
    new_membership_status = data.get("new_membership_status")

    response = requests.post(
        f"http://db-api:5431/api/db-api/update-user-membership/{user_id}",
        data={'membership_type': new_membership_status}
    )
    if response.status_code != 200:
        return response.text, response.status_code
    return 'Membership updated', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5211)

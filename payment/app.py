from flask import Flask, request, jsonify
import requests
import os
import psycopg2

app = Flask(__name__)

DB_API_INTERNAL = os.getenv('DB_API_INTERNAL', 'http://db-api:5431')
MEMBERSHIP_MODULE = os.getenv('MEMBERSHIP_MODULE', 'http://membership-module:5211')

MEMBERSHIP_PRICES = {
    'Standard': '20.00',
    'Pro': '40.00',
    'Pro+': '100.00'
}

PARKING_PRICES = {
    1: '3.00',
    2: '4.00',
    3: '5.50'
}


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        port=int(os.getenv('DB_PORT', 5432)),
        database=os.getenv('DB_NAME', 'gym_pro'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'CoolPass321')
    )


def luhn_check(card_number: str) -> bool:
    digits = [int(ch) for ch in card_number if ch.isdigit()]
    if len(digits) < 13:
        return False

    checksum = 0
    parity = len(digits) % 2

    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d

    return checksum % 10 == 0


def _fetch_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT "User ID", "User name", "Membership type" FROM "User" WHERE "User ID" = %s',
            (user_id,)
        )
        row = cur.fetchone()

        if not row:
            return None, (jsonify({'error': 'User not found'}), 404)

        return {
            'user_id': row[0],
            'name': row[1],
            'membership_type': row[2]
        }, None
    except Exception as e:
        return None, (jsonify({'error': 'Failed to fetch user', 'details': str(e)}), 500)
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass


def _fetch_stored_cards(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT "CreditCardID", "Card number", "Expiry", "CVC" FROM "Credit Card Information" WHERE "User ID" = %s',
            (user_id,)
        )
        rows = cur.fetchall()

        cards = [{
            'credit_card_id': row[0],
            'card_number': row[1],
            'expiry': row[2],
            'cvc': row[3]
        } for row in rows]

        return cards, None
    except Exception as e:
        return None, (jsonify({'error': 'Failed to fetch stored cards', 'details': str(e)}), 500)
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass


def _store_card(user_id, card_number, expiry, cvc):
    try:
        response = requests.post(
            f'{DB_API_INTERNAL}/api/db-api/insert-credit-card',
            data={
                'user_id': user_id,
                'card_number': card_number,
                'expiry': expiry,
                'cvc': cvc
            },
            timeout=5
        )
    except requests.RequestException as e:
        return False, (jsonify({'error': 'Failed to call insert-credit-card', 'details': str(e)}), 502)

    if response.status_code not in (200, 201):
        return False, (
            jsonify({
                'error': 'insert-credit-card failed',
                'status_code': response.status_code,
                'body': response.text
            }),
            502
        )

    return True, None


def _update_membership(user_id, new_membership):
    try:
        response = requests.post(
            f'{MEMBERSHIP_MODULE}/api/change-user-membership',
            json={'user_id': user_id, 'new_membership_status': new_membership},
            timeout=5
        )
        if response.status_code != 200:
            return False, (jsonify({'error': 'Membership update failed', 'details': response.text}), 502)
        return True, None
    except requests.RequestException as e:
        return False, (jsonify({'error': 'Failed to contact membership-module', 'details': str(e)}), 502)


def _validate_card_input(card_number, expiry, cvc):
    if not all([card_number, expiry, cvc]):
        return False, (jsonify({'error': 'card_number, expiry and cvc are required'}), 400)

    if not luhn_check(card_number):
        return False, (jsonify({'error': 'Invalid credit card number'}), 400)

    return True, None


@app.route('/api/db-api/pay', methods=['POST'])
def pay():
    data = request.get_json() or {}

    user_id = data.get('user_id')
    action = data.get('action')  # membership or parking
    target_membership = data.get('target_membership')
    parking_hours = data.get('parking_hours')
    card_number = data.get('card_number')
    expiry = data.get('expiry')
    cvc = data.get('cvc')
    store_card = bool(data.get('store_card', False))

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    if action not in ('membership', 'parking'):
        return jsonify({'error': "action must be 'membership' or 'parking'"}), 400

    user, err = _fetch_user(user_id)
    if err:
        return err

    membership_type = user['membership_type']

    # Membership payment
    if action == 'membership':
        if not target_membership:
            return jsonify({'error': 'target_membership is required'}), 400

        if target_membership not in MEMBERSHIP_PRICES:
            return jsonify({'error': 'Invalid target_membership'}), 400

        price = MEMBERSHIP_PRICES[target_membership]

        if membership_type == 'No Membership':
            ok, err = _validate_card_input(card_number, expiry, cvc)
            if not ok:
                return err

            ok, err = _store_card(user_id, card_number, expiry, cvc)
            if not ok:
                return err

            ok, err = _update_membership(user_id, target_membership)
            if not ok:
                return err

            return jsonify({
                'message': 'Membership purchased successfully',
                'user_id': user_id,
                'old_membership': membership_type,
                'new_membership': target_membership,
                'price': f'£{price}',
                'card_stored': True
            }), 200

        if membership_type in ['Standard', 'Pro', 'Pro+']:
            cards, err = _fetch_stored_cards(user_id)
            if err:
                return err

            if cards:
                ok, err = _update_membership(user_id, target_membership)
                if not ok:
                    return err

                return jsonify({
                    'message': 'Membership purchased using stored card',
                    'user_id': user_id,
                    'old_membership': membership_type,
                    'new_membership': target_membership,
                    'price': f'£{price}',
                    'used_stored_card': True
                }), 200

            ok, err = _validate_card_input(card_number, expiry, cvc)
            if not ok:
                return err

            if store_card:
                ok, err = _store_card(user_id, card_number, expiry, cvc)
                if not ok:
                    return err

            ok, err = _update_membership(user_id, target_membership)
            if not ok:
                return err

            return jsonify({
                'message': 'Membership purchased using provided card',
                'user_id': user_id,
                'old_membership': membership_type,
                'new_membership': target_membership,
                'price': f'£{price}',
                'card_stored': store_card
            }), 200

    # Parking payment
    if action == 'parking':
        if parking_hours is None:
            return jsonify({'error': 'parking_hours is required'}), 400

        try:
            parking_hours = int(parking_hours)
        except (TypeError, ValueError):
            return jsonify({'error': 'parking_hours must be 1, 2 or 3'}), 400

        if parking_hours not in (1, 2, 3):
            return jsonify({'error': 'parking_hours must be 1, 2 or 3'}), 400

        price = PARKING_PRICES[parking_hours]

        if membership_type in ['Pro', 'Pro+']:
            return jsonify({
                'message': 'No payment required for parking from Pro and Pro+ members',
                'user_id': user_id,
                'membership_type': membership_type,
                'price': '£0.00'
            }), 200

        if membership_type == 'Standard':
            cards, err = _fetch_stored_cards(user_id)
            if err:
                return err

            if cards:
                return jsonify({
                    'message': 'Parking payment processed using stored card',
                    'user_id': user_id,
                    'membership_type': membership_type,
                    'parking_hours': parking_hours,
                    'price': f'£{price}',
                    'used_stored_card': True
                }), 200

            ok, err = _validate_card_input(card_number, expiry, cvc)
            if not ok:
                return err

            ok, err = _store_card(user_id, card_number, expiry, cvc)
            if not ok:
                return err

            return jsonify({
                'message': 'Parking payment processed and card stored',
                'user_id': user_id,
                'membership_type': membership_type,
                'parking_hours': parking_hours,
                'price': f'£{price}',
                'card_stored': True
            }), 200

        if membership_type == 'No Membership':
            ok, err = _validate_card_input(card_number, expiry, cvc)
            if not ok:
                return err

            ok, err = _store_card(user_id, card_number, expiry, cvc)
            if not ok:
                return err

            return jsonify({
                'message': 'Parking payment processed',
                'user_id': user_id,
                'membership_type': membership_type,
                'parking_hours': parking_hours,
                'price': f'£{price}',
                'card_stored': True
            }), 200

    return jsonify({'error': 'Unhandled payment flow'}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5427)
from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

@app.route('/healthcheck')
def healthcheck():
    return 'OK', 200

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        port=int(os.getenv('DB_PORT', 5432)),
        database=os.getenv('DB_NAME', 'gym_pro'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'CoolPass321')
    )


@app.route('/api/db-healthcheck', methods=['GET'])
def db_healthcheck():
    # Open postgres connection and check if it's alive
    try:
        conn = get_db_connection()
        conn.close()
        return 'DB is up', 200
    except psycopg2.Error as e:
        return 'DB is down: ' + str(e), 500
    
@app.route('/api/db-api/get-user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500
    cur = conn.cursor()
    cur.execute('SELECT * FROM "User" WHERE "User ID" = %s', (user_id,))
    
    # Jsonify the result and return it
    user = cur.fetchone()
    if user:
        return {
            'id': user[0],
            'name': user[1],
            'type': user[2],
            'email': user[3],
            'phone_number': user[4],
            'membership_type': user[5]
        }, 200
    else:
        return 'User not found', 404

@app.route('/api/get-license-plate/<int:user_id>', methods=['GET'])
def get_licenseplate(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT Parking."User ID" FROM Parking WHERE id = %s', (user_id))
    
    # Jsonify the result and return it
    user = cur.fetchone()
    if user:
        cur.execute('SELECT * FROM Users WHERE id = %s', (user,))
        user = cur.fetchone()
        return {
            'id': user[0],
            'name': user[1],
            'type': user[2],
            'email': user[3],
            'phone_number': user[4],
            'membership_type': user[5]
        }, 200
    else:
        return 'User not found', 404
    
    cur.close()
    conn.close()

@app.route('/api/db-api/create-user', methods=['POST'])
def create_user():
    name = request.form.get('name')
    user_type = request.form.get('user_type')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    membership_type = request.form.get('membership_type')

    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500
    cur = conn.cursor()

    cur.execute('INSERT INTO "User" ("User name", "User type", "Email", "Phone number", "Membership type") VALUES (%s, %s, %s, %s, %s)', (name, user_type, email, phone_number, membership_type))
    conn.commit()

    cur.close()
    conn.close()

    return 'User inserted', 200

@app.route('/api/db-api/get-schedule', methods=['GET'])
def get_schedule():
    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500

    cur = conn.cursor()
    
    cur.execute('SELECT * FROM "Schedule"')
    schedule = cur.fetchall()

    cur.close()
    conn.close()

    return schedule, 200

@app.route('/api/db-api/insert-schedule-item', methods=['POST'])
def insert_schedule_item():
    user_id = request.form.get('user_id')
    trainer_id = request.form.get('trainer_id')
    date = request.form.get('date')

    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500

    cur = conn.cursor()

    cur.execute('INSERT INTO "Schedule" ("User ID (member)", "User ID (trainer)", "Date/time") VALUES (%s, %s, %s)', (user_id, trainer_id, date))
    conn.commit()

    cur.close()
    conn.close()

    return 'Queried successfully', 200

@app.route('/api/db-api/insert-parking-item', methods=['POST'])
def insert_parking_item():
    user_id = request.form.get('user_id')
    license_plate = request.form.get('license_plate')
    payment = request.form.get('payment')
    start_timestamp = request.form.get('start_timestamp')
    end_timestamp = request.form.get('end_timestamp')

    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500
    cur = conn.cursor()

    cur.execute(
        'INSERT INTO "Parking" ("User ID", "License plate", "Payment", "Start timestamp", "End timestamp") VALUES (%s, %s, %s, %s, %s)',
        (user_id, license_plate, payment, start_timestamp, end_timestamp)
    )
    conn.commit()

    cur.close()
    conn.close()

    return 'Parking item inserted', 200


@app.route('/api/db-api/get-parking/<int:user_id>', methods=['GET'])
def get_parking_by_user_id(user_id):
    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500
    cur = conn.cursor()

    cur.execute('SELECT * FROM "Parking" WHERE "User ID" = %s', (user_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{
        'parking_id': row[0],
        'user_id': row[1],
        'license_plate': row[2],
        'payment': row[3],
        'start_timestamp': row[4],
        'end_timestamp': row[5]
    } for row in rows], 200


@app.route('/api/db-api/insert-credit-card', methods=['POST'])
def insert_credit_card():
    user_id = request.form.get('user_id')
    card_number = request.form.get('card_number')
    expiry = request.form.get('expiry')
    cvc = request.form.get('cvc')

    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500
    cur = conn.cursor()

    cur.execute(
        'INSERT INTO "Credit Card Information" ("User ID", "Card number", "Expiry", "CVC") VALUES (%s, %s, %s, %s)',
        (user_id, card_number, expiry, cvc)
    )
    conn.commit()

    cur.close()
    conn.close()

    return 'Credit card inserted', 200


@app.route('/api/db-api/get-credit-card/<int:user_id>', methods=['GET'])
def get_credit_card_by_user_id(user_id):
    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500
    cur = conn.cursor()

    cur.execute('SELECT * FROM "Credit Card Information" WHERE "User ID" = %s', (user_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{
        'credit_card_id': row[0],
        'user_id': row[1],
        'card_number': row[2],
        'expiry': row[3],
        'cvc': row[4]
    } for row in rows], 200

@app.route('/api/db-api/update-user-membership/<int:user_id>', methods=['POST'])
def update_user_membership(user_id):
    membership_type = request.form.get('membership_type')

    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500
    cur = conn.cursor()
    cur.execute('UPDATE "User" SET "Membership type" = %s WHERE "User ID" = %s', (membership_type, user_id))
    conn.commit()

    rows_updated = cur.rowcount
    cur.close()
    conn.close()

    if rows_updated == 0:
        return 'User not found', 404
    return 'Membership updated', 200


@app.route('/api/db-api/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500
    cur = conn.cursor()
    cur.execute('DELETE FROM "User" WHERE "User ID" = %s', (user_id,))
    conn.commit()

    rows_deleted = cur.rowcount

    cur.close()
    conn.close()

    if rows_deleted == 0:
        return 'User not found', 404
    return 'User deleted', 200


@app.route('/api/db-api/create-debug-user', methods=['GET'])
def create_debug_user():
    conn = get_db_connection()
    if not conn:
        return 'DB failure', 500
    cur = conn.cursor()

    cur.execute('SELECT "User ID" FROM "User" WHERE "User name" = %s', ('debug_user',))
    existing = cur.fetchone()
    if existing:
        cur.close()
        conn.close()
        return {'id': existing[0]}, 200

    cur.execute(
        'INSERT INTO "User" ("User name", "User type", "Email", "Phone number", "Membership type") VALUES (%s, %s, %s, %s, %s) RETURNING "User ID"',
        ('debug_user', 'member', 'debug@gympro.com', '0000000000', 'Standard')
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {'id': user_id}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5431)

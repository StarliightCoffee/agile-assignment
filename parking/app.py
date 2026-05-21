from flask import Flask, request, jsonify
import requests
import re
from datetime import datetime, timedelta

app = Flask(__name__)

# Basic UK styled license plates pattern ("AA11 A1A" / "AA11A1A")
LICENSE_PLATE_RE = re.compile(r'^[A-Z]{2}\d{2}\s?[A-Z]\d[A-Z]$')

DB_API_BASE = "http://db-api:5431/api"

PAYMENT_BY_HOURS = {
    1: "3.00",
    2: "4.00",
    3: "5.50"
}

def now_iso():
    return datetime.now().isoformat()

def iso_after_hours(hours):
    return (datetime.now() + timedelta(hours=hours)).isoformat()

def validate_plate(plate: str) -> bool:
    if not plate:
        return False
    plate = plate.strip().upper()
    return bool(LICENSE_PLATE_RE.match(plate))

@app.route("/check-membership", methods=["POST"])
def check_membership():
    payload = request.get_json() or {}

    user_id = payload.get("user_id")
    license_plate = payload.get("license_plate")  # can be none
    duration = payload.get("duration")  # expected 1,2,3
    store_plate = payload.get("store_plate")  # boolean, optional

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    # Validates duration if provided (but we'll also require it later)
    if duration is not None:
        try:
            duration = int(duration)
        except Exception:
            return jsonify({"error": "duration must be an integer (1, 2 or 3)"}), 400
        if duration not in (1, 2, 3):
            return jsonify({"error": "duration must be 1, 2 or 3 hours"}), 400

    # Get membership type
    try:
        r = requests.get(f"{DB_API_BASE}/get-membership_type/{user_id}", timeout=5)
    except requests.RequestException as e:
        return jsonify({"error": "failed to contact db-api", "details": str(e)}), 502

    if r.status_code != 200:
        return jsonify({"error": "db-api returned non-200 for membership lookup", "status_code": r.status_code}), 502

    membership_type = r.json().get("membership_type")
    if not membership_type:
        return jsonify({"error": "membership_type not found in db-api response"}), 502

    # If No Membership: license_plate is required from user input
    if membership_type == "No Membership":
        if not license_plate:
            return jsonify({
                "membership_type": membership_type,
                "needs_license_plate": True,
                "error": "license_plate is required for No Membership users"
            }), 400

        plate_norm = license_plate.strip().upper()
        if not validate_plate(plate_norm):
            return jsonify({"error": "license_plate format invalid. Expected e.g. 'AA11 A1A'"}), 400

        if duration is None:
            return jsonify({"error": "duration (1,2,3) is required"}), 400

        start_ts = now_iso()
        end_ts = iso_after_hours(duration)
        payment = PAYMENT_BY_HOURS[duration]

        insert_payload = {
            "user_id": user_id,
            "license_plate": plate_norm,
            "payment": payment,
            "start_timestamp": start_ts,
            "end_timestamp": end_ts
        }

        try:
            ins = requests.post(f"{DB_API_BASE}/insert_parking_item", json=insert_payload, timeout=5)
        except requests.RequestException as e:
            return jsonify({"error": "failed to insert parking item", "details": str(e)}), 502

        if ins.status_code not in (200, 201):
            return jsonify({"error": "db-api failed to insert parking item", "status_code": ins.status_code, "body": ins.text}), 502

        return jsonify({
            "membership_type": membership_type,
            "license_plate": plate_norm,
            "stored": False,
            "start_timestamp": start_ts,
            "end_timestamp": end_ts,
            "payment": payment,
            "message": "Parking created for No Membership user"
        }), 200

    # For Standard/Pro/Pro+ users
    if membership_type in ["Standard", "Pro", "Pro+"]:
        # Check if license plate is stored for this user
        try:
            rp = requests.get(f"{DB_API_BASE}/get-license_plate/{user_id}", timeout=5)
        except requests.RequestException as e:
            return jsonify({"error": "failed to contact db-api for license plate", "details": str(e)}), 502

        stored_plate = None
        if rp.status_code == 200:
            stored_plate = rp.json().get("license_plate")

        # If stored plate found and client didn't provide one, use stored plate
        if stored_plate and not license_plate:
            plate_norm = stored_plate.strip().upper()
            if not validate_plate(plate_norm):
                return jsonify({"error": "stored license plate format invalid"}), 500

            if duration is None:
                return jsonify({"error": "duration (1,2,3) is required"}), 400

            start_ts = now_iso()
            end_ts = iso_after_hours(duration)
            payment = PAYMENT_BY_HOURS[duration]

            insert_payload = {
                "user_id": user_id,
                "license_plate": plate_norm,
                "payment": payment,
                "start_timestamp": start_ts,
                "end_timestamp": end_ts
            }

            try:
                ins = requests.post(f"{DB_API_BASE}/insert_parking_item", json=insert_payload, timeout=5)
            except requests.RequestException as e:
                return jsonify({"error": "failed to insert parking item", "details": str(e)}), 502

            if ins.status_code not in (200, 201):
                return jsonify({"error": "db-api failed to insert parking item", "status_code": ins.status_code, "body": ins.text}), 502

            return jsonify({
                "membership_type": membership_type,
                "license_plate": plate_norm,
                "stored": True,
                "start_timestamp": start_ts,
                "end_timestamp": end_ts,
                "payment": payment,
                "message": f"Parking created for {membership_type} user using stored plate"
            }), 200

        # No stored plate or client provided a different plate
        if not license_plate:
            return jsonify({
                "membership_type": membership_type,
                "needs_license_plate": True,
                "error": f"license_plate is required for {membership_type} users when none is stored"
            }), 400

        plate_norm = license_plate.strip().upper()
        if not validate_plate(plate_norm):
            return jsonify({"error": "license_plate format invalid. Expected e.g. 'AA11 A1A'"}), 400

        # If user wants to store the plate, call db-api to store it before inserting parking
        if store_plate:
            store_payload = {"user_id": user_id, "license_plate": plate_norm}
            try:
                sp = requests.post(f"{DB_API_BASE}/store-license-plate", json=store_payload, timeout=5)
            except requests.RequestException as e:
                return jsonify({"error": "failed to store license plate", "details": str(e)}), 502

            if sp.status_code not in (200, 201):
                return jsonify({"error": "db-api failed to store license plate", "status_code": sp.status_code, "body": sp.text}), 502

        # Now create parking item
        if duration is None:
            return jsonify({"error": "duration (1,2,3) is required"}), 400

        start_ts = now_iso()
        end_ts = iso_after_hours(duration)
        payment = PAYMENT_BY_HOURS[duration]

        insert_payload = {
            "user_id": user_id,
            "license_plate": plate_norm,
            "payment": payment,
            "start_timestamp": start_ts,
            "end_timestamp": end_ts
        }

        try:
            ins = requests.post(f"{DB_API_BASE}/insert_parking_item", json=insert_payload, timeout=5)
        except requests.RequestException as e:
            return jsonify({"error": "failed to insert parking item", "details": str(e)}), 502

        if ins.status_code not in (200, 201):
            return jsonify({"error": "db-api failed to insert parking item", "status_code": ins.status_code, "body": ins.text}), 502

        return jsonify({
            "membership_type": membership_type,
            "license_plate": plate_norm,
            "stored": bool(store_plate),
            "start_timestamp": start_ts,
            "end_timestamp": end_ts,
            "payment": payment,
            "message": f"Parking created for {membership_type} user"
        }), 200

    return jsonify({"error": "Unknown membership type"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5428)
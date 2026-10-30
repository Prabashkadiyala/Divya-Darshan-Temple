from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import pymysql

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# MySQL Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "divyadarshan_db"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# -------------------------------------------------------------
# FRONTEND ROUTE
# -------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

# -------------------------------------------------------------
# API ROUTE: USER REGISTRATION (WITH BCRYPT ENCRYPTION)
# -------------------------------------------------------------
@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        full_name = data.get('fullName')
        email = data.get('email')
        phone = data.get('phone')
        raw_password = data.get('password')

        if not all([full_name, email, phone, raw_password]):
            return jsonify({"success": False, "error": "All fields are required"}), 400

        # Hash password using Bcrypt
        hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({"success": False, "error": "Email already registered"}), 400

            # Insert new user into MySQL
            sql = "INSERT INTO users (full_name, email, phone, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (full_name, email, phone, hashed_password))
            conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Registration successful!"}), 201

    except Exception as e:
        print("Registration Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

# -------------------------------------------------------------
# API ROUTE: USER LOGIN
# -------------------------------------------------------------
@app.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            return jsonify({
                "success": True,
                "user": {
                    "id": user['id'],
                    "fullName": user['full_name'],
                    "email": user['email']
                }
            }), 200
        else:
            return jsonify({"success": False, "error": "Invalid email or password"}), 401

    except Exception as e:
        print("Login Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

# -------------------------------------------------------------
# API ROUTE: SAVE BOOKING TO MYSQL
# -------------------------------------------------------------
@app.route('/api/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.json
        print("Received booking data:", data)  # This will print the data in your terminal
        
        ref_no = data.get('refNo')
        temple_name = data.get('templeName')
        devotee_name = data.get('devoteeName')
        aadhaar = data.get('aadhaar')
        darshan_type = data.get('darshanType')
        slot = data.get('slot')
        breakdown = data.get('breakdown')
        total_amount = data.get('totalAmount', 0)

        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """INSERT INTO bookings 
                     (ref_no, temple_name, devotee_name, aadhaar, darshan_type, slot, breakdown, total_amount) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                ref_no, temple_name, devotee_name, aadhaar, 
                darshan_type, slot, breakdown, total_amount
            ))
            conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Booking stored in database!"}), 201

    except Exception as e:
        print("❌ CRITICAL DATABASE ERROR:", str(e))  # This will print the exact SQL error
        return jsonify({"success": False, "error": str(e)}), 500
# -------------------------------------------------------------
# API ROUTE: GET ALL BOOKINGS FROM MYSQL (FOR ADMIN / DASHBOARD)
# -------------------------------------------------------------
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
            bookings = cursor.fetchall()
        conn.close()

        return jsonify({"success": True, "bookings": bookings}), 200

    except Exception as e:
        print("Fetch Bookings Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    print("Starting DivyaDarshan Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
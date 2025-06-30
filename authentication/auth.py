from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Simulated users
users = {}

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # Check if any field is missing
    if not username or not email or not password or not confirm_password:
        return jsonify({"error": "All fields are required"}), 400

    # Check password match
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # Check if email or username already exists
    if email in users or any(u["username"] == username for u in users.values()):
        return jsonify({"error": "User with this email or username already exists"}), 400

    # Register user
    users[email] = {
        "username": username,
        "password": password  # NOTE: In real apps, hash the password!
    }

    return jsonify({"message": "Registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    if users.get(username) == password:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("new_password")

    if email in users:
        users[email] = new_password
        return jsonify({"message": "Password reset successful"}), 200

    return jsonify({"error": "User not found"}), 404


@app.route("/logout", methods=["POST"])
def logout():
    # Dummy logout: you can just return a success message
    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": list(users.keys())}), 200

if __name__ == "__main__":
    app.run(debug=True)

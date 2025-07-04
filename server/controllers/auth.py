from flask import Blueprint, request, jsonify, session
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, User

@app.route('/hello')
def hello():
    return jsonify({"message": "Hello, World!"}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(data['password'])
    user = User(
        email=email,
        name=data.get('name'),
        password=hashed_password,
        address=data.get('address'),
        pin_code=data.get('pin_code'),
        role='user'
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    session['user_id'] = user.user_id
    session['role'] = user.role
    return jsonify({"message": "Login successful", "role": user.role, "user_id": user.user_id, "name": user.name.capitalize()}), 200

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/current_user', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Not logged in"}), 401
    user = User.query.get(user_id)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200

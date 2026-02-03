# users_api.py
from flask import Flask, jsonify, request
from functools import wraps
import uuid
 
app = Flask(__name__)
 
# In-memory data store
users_db = {
    "1": {"id": "1", "name": "John Doe", "email": "john@lab.local", "role": "admin"},
    "2": {"id": "2", "name": "Jane Smith", "email": "jane@lab.local", "role": "user"},
    "3": {"id": "3", "name": "Bob Wilson", "email": "bob@lab.local", "role": "user"}
}
 
# Logging middleware
@app.before_request
def log_request():
    auth_user = request.headers.get('X-Authenticated-User', 'anonymous')
    app.logger.info(f"Request from: {auth_user} - {request.method} {request.path}")
 
# API Routes
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """List all users"""
    return jsonify({
        "status": "success",
        "data": list(users_db.values()),
        "total": len(users_db)
    })
 
@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = users_db.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    return jsonify({"status": "success", "data": user})
 
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
 
    new_id = str(uuid.uuid4())[:8]
    users_db[new_id] = {
        "id": new_id,
        "name": data['name'],
        "email": data['email'],
        "role": data.get('role', 'user')
    }
    return jsonify({"status": "success", "data": users_db[new_id]}), 201
 
@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    if user_id not in users_db:
        return jsonify({"status": "error", "message": "User not found"}), 404
 
    data = request.get_json()
    users_db[user_id].update({
        "name": data.get('name', users_db[user_id]['name']),
        "email": data.get('email', users_db[user_id]['email']),
        "role": data.get('role', users_db[user_id]['role'])
    })
    return jsonify({"status": "success", "data": users_db[user_id]})
 
@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    if user_id not in users_db:
        return jsonify({"status": "error", "message": "User not found"}), 404
 
    del users_db[user_id]
    return jsonify({"status": "success", "message": "User deleted"}), 200
 
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "users-api"})
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)

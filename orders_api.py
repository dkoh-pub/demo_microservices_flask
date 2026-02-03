# orders_api.py
from flask import Flask, jsonify, request
from datetime import datetime
import uuid
 
app = Flask(__name__)
 
# In-memory data store
orders_db = {
    "ORD001": {
        "id": "ORD001",
        "user_id": "1",
        "product_id": "P001",
        "quantity": 2,
        "status": "completed",
        "created_at": "2026-01-15T10:30:00Z"
    },
    "ORD002": {
        "id": "ORD002",
        "user_id": "2",
        "product_id": "P002",
        "quantity": 5,
        "status": "pending",
        "created_at": "2026-02-01T14:20:00Z"
    }
}
 
@app.route('/api/v1/orders', methods=['GET'])
def get_orders():
    """List all orders"""
    user_id = request.args.get('user_id')
    status = request.args.get('status')
 
    result = list(orders_db.values())
    if user_id:
        result = [o for o in result if o['user_id'] == user_id]
    if status:
        result = [o for o in result if o['status'] == status]
 
    return jsonify({"status": "success", "data": result})
 
@app.route('/api/v1/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get order by ID"""
    order = orders_db.get(order_id)
    if not order:
        return jsonify({"status": "error", "message": "Order not found"}), 404
    return jsonify({"status": "success", "data": order})
 
@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    """Create new order"""
    data = request.get_json()
    new_id = f"ORD{str(uuid.uuid4())[:3].upper()}"
    orders_db[new_id] = {
        "id": new_id,
        "user_id": data['user_id'],
        "product_id": data['product_id'],
        "quantity": data.get('quantity', 1),
        "status": "pending",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify({"status": "success", "data": orders_db[new_id]}), 201
 
@app.route('/api/v1/orders/<order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    """Update order status"""
    if order_id not in orders_db:
        return jsonify({"status": "error", "message": "Order not found"}), 404
 
    data = request.get_json()
    valid_statuses = ['pending', 'processing', 'shipped', 'completed', 'cancelled']
    if data.get('status') not in valid_statuses:
        return jsonify({"status": "error", "message": "Invalid status"}), 400
 
    orders_db[order_id]['status'] = data['status']
    return jsonify({"status": "success", "data": orders_db[order_id]})
 
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "orders-api"})
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)

# products_api.py
from flask import Flask, jsonify, request
import uuid
 
app = Flask(__name__)
 
# In-memory data store
products_db = {
    "P001": {"id": "P001", "name": "BIG-IP i5800", "category": "ADC", "price": 45000},
    "P002": {"id": "P002", "name": "NGINX Plus", "category": "Software", "price": 2500},
    "P003": {"id": "P003", "name": "F5 Distributed Cloud", "category": "SaaS", "price": 5000}
}
 
@app.route('/api/v1/products', methods=['GET'])
def get_products():
    """List all products"""
    category = request.args.get('category')
    if category:
        filtered = [p for p in products_db.values() if p['category'] == category]
        return jsonify({"status": "success", "data": filtered})
    return jsonify({"status": "success", "data": list(products_db.values())})
 
@app.route('/api/v1/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    product = products_db.get(product_id)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404
    return jsonify({"status": "success", "data": product})
 
@app.route('/api/v1/products', methods=['POST'])
def create_product():
    """Create new product"""
    data = request.get_json()
    new_id = f"P{str(uuid.uuid4())[:3].upper()}"
    products_db[new_id] = {
        "id": new_id,
        "name": data['name'],
        "category": data.get('category', 'General'),
        "price": data.get('price', 0)
    }
    return jsonify({"status": "success", "data": products_db[new_id]}), 201
 
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "products-api"})
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)

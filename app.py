from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Set up the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the Order model (database table)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Order {self.customer_name} ordered {self.product_name}>'

# Route to create a new order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    new_order = Order(
        customer_name=data['customer_name'],
        product_name=data['product_name'],
        quantity=data['quantity'],
        price=data['price']
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order created successfully!"}), 201

# Route to get all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': order.id,
        'customer_name': order.customer_name,
        'product_name': order.product_name,
        'quantity': order.quantity,
        'price': order.price
    } for order in orders])

# Ensure we run the db creation inside the application context
if __name__ == '__main__':
    with app.app_context():  # Create an application context explicitly
        db.create_all()  # Create the database tables

    app.run(debug=True)

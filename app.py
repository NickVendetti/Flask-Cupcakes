"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from models import db, Cupcake, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

# Initialize the database connection
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Render the static HTML page for the cupcake app."""
    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    """Get data about all cupcakes."""
    cupcakes = Cupcake.query.all()
    cupcakes_list = [
        {
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image
        } for cupcake in cupcakes
    ]
    return jsonify(cupcakes=cupcakes_list)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake_data = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
    return jsonify(cupcake=cupcake_data)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake."""
    data = request.json

    # Ensure all required fields are present
    if not all(k in data for k in ['flavor', 'size', 'rating']):
        return jsonify({"error": "Missing required data"}), 400

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data.get('image', 'https://tinyurl.com/demo-cupcake')
    )
    
    db.session.add(new_cupcake)
    db.session.commit()

    response_json = {
        "cupcake": {
            "id": new_cupcake.id,
            "flavor": new_cupcake.flavor,
            "size": new_cupcake.size,
            "rating": new_cupcake.rating,
            "image": new_cupcake.image
        }
    }
    return jsonify(response_json), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update an existing cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    updated_cupcake = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

    return jsonify(cupcake=updated_cupcake)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

if __name__ == '__main__':
    app.run(debug=True)
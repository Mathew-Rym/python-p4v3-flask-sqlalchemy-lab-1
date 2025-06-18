# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 202)

# Add views here
@app.route('/earthquakes/<int:id>')
def view_earthquake(id):
    earthquake = Earthquake.query.get(id)
    
    if earthquake:
        response = jsonify({
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        })
        return make_response(response, 200)
    
    else: 
        response = jsonify({
            'message':f"Earthquake {id} not found."
        })
        return make_response(response, 404)
    

@app.route('/earthquakes/magnitude/<float:magnitude>')
def view_magnitudes(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    response = jsonify({
        'count': len(earthquakes),
        'quakes': [quake.to_dict() for quake in earthquakes]
    })
    return make_response(response, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

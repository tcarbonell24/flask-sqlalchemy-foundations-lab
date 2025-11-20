# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
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
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def earthquake(id):
    earthquake = Earthquake.query.filter_by(id=id).first()

    if earthquake:
        body = {
            'id': earthquake.id,
            'year': earthquake.year,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location
        }
        status = 200
    else:
        # Ensure the message matches the test exactly
        body = {'message': f'Earthquake {id} not found.'}
        status = 404

    return make_response(body, status)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Build list of earthquake dictionaries
    quakes_list = [
        {
            'id': eq.id,
            'location': eq.location,
            'magnitude': eq.magnitude,
            'year': eq.year
        }
        for eq in earthquakes
    ]

    body = {
        'count': len(quakes_list),
        'quakes': quakes_list
    }

    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

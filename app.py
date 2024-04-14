from flask import Flask, request, jsonify, abort
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

app = Flask(__name__)

if os.environ.get('ENV') == 'production':
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@hostname/database_name'
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Kudos(db.Model):
    path = db.Column(db.String(80), primary_key=True)
    kudos = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'path': self.path,
            'kudos': self.kudos,
            'title': self.title,
            'description': self.description
        }


class AppToken(db.Model):
    token = db.Column(db.String(255), primary_key=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)


def app_authorized(token):

    if (not token):
        return False

    existing_token = AppToken.query.filter_by(token=token).first()

    if (not existing_token):
        return False

    return True


@app.route("/")
def index():
    return 'The kudos-service is running!'


@app.route("/kudos", methods=["GET"])
def overview():
    all_kudos = Kudos.query.all()

    kudos_list = []
    for kudos in all_kudos:
        kudos_data = {
            'path': kudos.path,
            'kudos': kudos.kudos,
            'title': kudos.title,
            'description': kudos.description
        }
        kudos_list.append(kudos_data)

    return jsonify(kudos_list)


@app.route("/kudos/<path:path>", methods=["POST", "GET", "PATCH", "DELETE"])
def kudos(path):
    if request.method == 'GET':
        # Retreive kudos by path
        # no protection needed
        existing_kudos = Kudos.query.filter_by(path=path).first()

        if (existing_kudos):
            return jsonify(existing_kudos.to_dict())
        else:
            abort(404)

    elif request.method == 'POST':
        # Create a new kudos with that path, require title and description
        # Ideally protected

        data = request.get_json()

        if not app_authorized(data.get('token')):
            return jsonify({'error': 'Unauthorized request, invalid app token'}), 401

        if 'title' not in data or 'description' not in data:
            return jsonify({'error': 'Title and description for the kudos entry is required'}), 400

        existing_kudos = Kudos.query.filter_by(path=path).first()

        if existing_kudos:
            # Update existing record
            existing_kudos.title = data['title']
            existing_kudos.description = data['description']
            db.session.commit()
            return jsonify(existing_kudos.to_dict())
        else:
            # Create new record
            new_kudos = Kudos(
                path=path,
                title=data['title'],
                description=data['description']
            )
            db.session.add(new_kudos)
            db.session.commit()
            return jsonify(new_kudos.to_dict())

    elif request.method == 'PATCH':
        # Update the count on a kudos
        existing_kudos = Kudos.query.filter_by(path=path).first()

        if (existing_kudos):
            existing_kudos.kudos = existing_kudos.kudos + 1
            db.session.commit()
            return jsonify(existing_kudos.to_dict())
        else:
            abort(404)

    elif request.method == 'DELETE':
        data = request.get_json()

        if not app_authorized(data.get('token')):
            return jsonify({'error': 'Unauthorized request, invalid app token'}), 401

        kudos = Kudos.query.filter_by(path=path).first()
        if kudos:
            db.session.delete(kudos)
            db.session.commit()
            return 'Kudos deleted successfully', 200
        else:
            abort(404)

    else:
        return 'Unsupported request method for /kudos'

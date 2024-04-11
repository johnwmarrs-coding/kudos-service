from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
    

@app.route("/")
def index():
    return 'The kudos-service is running!'

@app.route("/kudos", methods=["GET"])
def overview():
    return "Overview of kudos objects"

@app.route("/kudos/<path>", methods=["POST", "GET", "PATCH", "DELETE"])
def kudos(path):
    kudos_path = request.args.get('path')
    if request.method == 'GET':
        # Retreive kudos by path
        # no protection needed
        pass
    elif request.method == 'POST':
        # Create a new kudos with that path, require title and description
        # Ideally protected
        pass
    elif request.method == 'PATCH':
        # Update the count on a kudos
        # Ideally protected
        pass
    elif request.method == 'DELETE':
        # remove the kudos by path
        # ideally protected
        pass
    else:
        return 'Unsupported request method for /kudos'

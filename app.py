from flask import flask

app = Flask(__name__)

@app.route("/")
def index():
    return 'The kudos-service is running!'

@app.route("/kudos/overview", methods=["GET"])
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

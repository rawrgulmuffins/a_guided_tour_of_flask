from . import app
from . import db

@app.route('/ping', methods=["POST"])
def ping():
    return 'Hello World!'

@app.route('/version', methods=["GET"])
def return_version():
    return app.config["VERSION"]

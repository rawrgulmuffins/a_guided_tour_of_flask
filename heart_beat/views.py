from flask import request
import pprint

from . import app
from . import db

@app.route('/ping', methods=["POST"])
def ping():
    pprint.pprint(request.form)
    return "=D\n"

@app.route('/version', methods=["GET"])
def return_version():
    return app.config["VERSION"]

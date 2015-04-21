"""
All URL routes live in this file. Anything function with a @app.route is a
valid url end-point which is auto-magically created by flask. All return values
must be valid bytes or (unicode) strings.

NOTE: This flask application was built to run on Python3.4
"""

from flask import request

from . import app
from . import db
from . import models

def insert_ping_data(posted_json):
    """
    This function is used to insert data into the database once all passing
    all of the request level error checking.

    If we have all known keys and they're populated with data we may
    still run into an Error in DiagnosticPingData if the string data
    can't be converted to the expected data types.
    """
    new_ping_row = models.DiagnosticPingData(**posted_json)
    db.session.add(new_ping_row)
    db.session.commit()


@app.route('/ping', methods=["POST"])
def ping():
    """
    Given a http post request with the Content-Type=application/json, parse the
    json that's been given to us. If any of the expected fields are None then
    the database insert will fail and a error code will be returned.

    NOTE: if the Content-Type is set incorrectly then request.get_json() will
          return None and no actions will be taken.

    Expected JSON keys:

        client_start_time: Type=db.DateTime
        logset_gather_time: Type=db.DateTime
        one_fs_version: Type=db.String
        esrs_enabled: Type=db.Boolean
        tool_version: Type=db.String
        sr_number: Type=db.Integer

    More database table and column information can be found at
    heart_beat/modles.py

    status code 200 is returned if valid data is passed and was able to be
        inserted into the db.
    Status code 400 is returned in four separate cases. No JSON data, Null JSON
        data, JSON data is missing keys, JSON data contains Nulls.
    Status code 405 is anything put POST is used as the method.
    Status code 406 is used if any content-type is used other than
        application/json.
    """
    json_keys = [
        "client_start_time",
        "logset_gather_time",
        "onefs_version",
        "esrs_enabled",
        "tool_version",
        "sr_number",]
    posted_json = request.get_json()

    # Didn't get json data for some reason.
    if posted_json is None:
        # Bad content-type header.
        if request.content_type != 'application/json':
            return "bad Content-Type", 406
        else:
            # Either no json was given or json == {"null"}
            return "No JSON or Null JSON", 400

    # We could just let the sqlalchemy model test to see if all the keys are
    # present and have data but we'll get better error codes if we check at the
    # view level.
    if all(key in posted_json for key in json_keys):
        if None not in posted_json.values():
            insert_ping_data(posted_json)
            return "", 200
        else:
            # No db columns can be null. See models.py for more details.
            return "JSON data contains Nulls", 400
    else:
        # Malformed JSON data, missing keys.
        return "Missing Keys from json data", 400


@app.route('/version', methods=["GET"])
def return_version():
    """
    Returns the version string which is set either in development_config.py 
    (if you've run using runserver and set debug=True) or production_config.py
    """
    return app.config["VERSION"]

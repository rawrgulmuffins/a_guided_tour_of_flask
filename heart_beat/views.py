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
    """
    json_keys = [
        "client_start_time",
        "logset_gather_time",
        "onefs_version",
        "esrs_enabled",
        "tool_version",
        "sr_number",]
    posted_json = request.get_json()
    # We could just let the sqlalchemy model test to see if all the keys are
    # present and have data but we'll get better error codes if we check at the
    # view level.
    if (all(key in posted_json for key in json_keys) and
            None not in posted_json.values()):
        # If we have all known keys and they're populated with data we may
        # still run into an Error in DiagnosticPingData if the string data
        # can't be converted to the expected data types.
        new_ping_row = models.DiagnosticPingData(**posted_json)
        db.session.add(new_ping_row)
        db.session.commit()
        return "=D\n"
    else:
        # We've been given a set of json data that doesn't have the keys we're
        # looking for or has the keys but doesn't contain data.
        return "=(\n"

@app.route('/version', methods=["GET"])
def return_version():
    """
    Returns the version string which is set either in development_config.py 
    (if you've run using runserver and set debug=True) or production_config.py
    """
    return app.config["VERSION"]

"""
Holds all configs and app level constructs. If you'd like to add something that
affects the app object for the entire application it should happen in this
file.
"""
#pylint: disable=invalid-name

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from register_assets import register_all

app = Flask(__name__, static_url_path='/static')

# the environment variable LIMBO_SETTINGS is set in runserver, run_unit_tests
# or limbo.wsgi.

def load_configs():
    """Take all configs found in development_config."""
    app.config.from_pyfile("development_config", silent=False)

load_configs()

# global SQLAlchemy configuration
db = SQLAlchemy(app)

#Create and register all static asset bundles.
#register_all(app)

#NOTE: DON'T LISTEN TO YOUR IDE! heart_beat.views is used and required.
import heart_beat.views  # views contains all URL routes, Importing sets routes.
def setup_db():
    """Database creation in a file rather then a statement for easier tests."""
    db.create_all()

def teardown_db():
    """Database deletion in a file rather then a statement for easier tests."""
    db.drop_all()

setup_db()

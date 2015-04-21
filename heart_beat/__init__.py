"""
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from register_assets import register_all

app = Flask(__name__, static_url_path='/static')

# the environment variable LIMBO_SETTINGS is set in runserver, run_unit_tests
# or limbo.wsgi.

app.config.from_pyfile("development_config.py", silent=False)

# global SQLAlchemy configuration
db = SQLAlchemy(app)

#Create and register all static asset bundles.
#register_all(app)

#NOTE: DON'T LISTEN TO YOUR IDE! limbo.views is used and required.
import heart_beat.views  # views contains all URL routes, Importing sets routes.
def setup_db():
    db.create_all()

def teardown_db():
    db.drop_all()

setup_db()

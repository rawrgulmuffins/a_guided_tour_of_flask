"""
This file starts a limbo application and servers limbo on this machines current
address on port 80

NOTE: This test server is not meant for production.
"""
from heart_beat import app

if __name__ == "__main__":
    #run install.py to install dependencies and create the database
    app.run(host="0.0.0.0", port=5000, debug=True)

"""
DO NOT USE THIS FILE TO RUN A PRODUCTION SERVER. THIS IS IN ALL CAP'S FOR A
REASON AND YOU SHOULD LISTEN.

If you use runserver.py to run in a production environment you will be running
this flask application using python.SimpleHTTPServer (which is about as
fast as a turtle dragging an sports car) and more importantly you will be
deploying code which comes with network facing arbitrary code execution built
in by design. The flask dev server is wonderful for proof of convent and dev
work but is absolutely not ok for production use.
"""
from heart_beat import app

if __name__ == "__main__":
    #run install.py to install dependencies and create the database
    app.run(host="0.0.0.0", port=5000, debug=True)

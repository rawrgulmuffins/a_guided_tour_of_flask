from flask import Flask, render_template
# This is some path magic that's required because this is an IPython notebook.
app = Flask("the_flask_module")

# You can pass arguments to templates which can be tested.
@app.route('/')
def if_template():
    return "I'm modified!"


app.run(host="0.0.0.0", port=5001, debug=True)
# You now have a running web server. go to http://localhost:5000/ in a web browser or curl http://localhost:5000

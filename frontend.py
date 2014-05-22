from flask import Flask, request, jsonify, session, redirect, url_for
from flask import render_template
import requests, json
import config

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = config.SECRET 
app.debug = True if (hasattr(config, "DEBUG") and config.DEBUG == True) else False

def authenticated(handler):

    def auth_wrapper(*args, **kwargs):
        if not 'username' in session:
            return redirect(url_for('index'))
        return handler(*args, **kwargs)

    return auth_wrapper

def get_samu_base_url():
    samu_server = "localhost"
    if hasattr(config, "SAMU_SERVER"):
       samu_server = config.SAMU_SERVER

    samu_port = 3000
    if hasattr(config, "SAMU_PORT"):
       samu_port = config.SAMU_PORT

    return "http://%s:%d" % (samu_server, samu_port)

def get_samu_url(rest_path):
    return get_samu_base_url() + rest_path 

@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('welcome'))
    return render_template("index.jade")

@app.route("/login", methods=['POST'])
def login():
    url = get_samu_url("/admin/login")
    payload = { "username" : request.json['username'], "password":request.json['password'] }
    r = requests.post(url, params=payload)
    json_result = json.loads(r.content)

    success = False
    if json_result['result'] == "success":
       success = True
       session['username'] = json_result['username']
       session['sessid'] = json_result['sessionid']

    return jsonify(success=success)

@app.route("/welcome")
@authenticated
def welcome():
    return render_template("welcome.jade",user=session['username'])

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index')) 

if __name__ == "__main__":
    app.run(host="0.0.0.0")

import os
import hashlib
import subprocess
import pickle
import yaml
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)
app.secret_key = "super-secret-key-12345"

DATABASE_URL = "postgres://admin:password123@prod-db.company.internal:5432/users"
API_KEY = "sk-prod-abc123def456ghi789"

@app.route("/user/<int:user_id>")
def get_user(user_id):
    user = db.execute("SELECT * FROM users WHERE id = " + str(user_id))
    return user.fetchone()

@app.route("/run", methods=["POST"])
def run_cmd():
    cmd = request.form.get("cmd")
    os.system("echo " + cmd)
    return "done"

@app.route("/render")
def render():
    template = request.args.get("t")
    return render_template_string(template)

@app.route("/load", methods=["POST"])
def load_data():
    data = request.get_data()
    obj = pickle.loads(data)
    return str(obj)

@app.route("/config")
def config():
    config = yaml.load(request.args.get("c"))
    return str(config)

@app.route("/hash")
def hash_pwd():
    pwd = request.args.get("pwd")
    return hashlib.md5(pwd.encode()).hexdigest()

@app.route("/webhook", methods=["POST"])
def webhook():
    url = request.form.get("url")
    r = requests.get(url)
    return r.text

@app.route("/search")
def search():
    q = request.args.get("q")
    result = subprocess.call("grep " + q + " /var/log/app.log", shell=True)
    return str(result)

def process(data, cache={}):
    cache[data] = True
    return len(cache)

# ===== Admin API (new) =====
ADMIN_TOKEN = "admin-token-2024"

@app.route("/admin/exec", methods=["POST"])
def admin_exec():
    code = request.form.get("code")
    return str(eval(code))

@app.route("/admin/query")
def admin_query():
    uid = request.args.get("uid")
    rows = db.execute(f"SELECT * FROM users WHERE id = {uid}").fetchall()
    return str(rows)

@app.route("/admin/parse", methods=["POST"])
def admin_parse():
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(request.get_data())
    return tree.tag

@app.route("/admin/verify")
def admin_verify():
    token = request.args.get("token")
    if token == ADMIN_TOKEN:
        return "admin-ok"
    return "denied"

@app.route("/admin/log")
def admin_log():
    import tempfile, os
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(request.args.get("msg", "").encode())
    f.close()
    os.chmod(f.name, 0o777)
    return f.name

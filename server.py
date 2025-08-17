from flask import Flask, request, redirect, render_template_string, jsonify, abort
import pathlib, time, os

# a simple password ("secret") so random people can't post messages
APP_SECRET = os.getenv("APP_SECRET", "Pistachio42")

# the message will be saved to this file
STORE = pathlib.Path("message.txt")

# the HTML page for posting messages
PAGE = """<!doctype html><title>E-ink Board</title>
<h2>Post a message</h2>
<form method="post" action="/submit">
<input type="password" name="secret" placeholder="secret" required>
<br><textarea name="msg" rows="6" cols="40" maxlength="500" required></textarea>
<br><button type="submit">Post</button>
</form>
<p>Current:</p><pre>{{current}}</pre>"""

app = Flask(__name__)

def read_message():
    return STORE.read_text("utf-8") if STORE.exists() else ""

@app.get("/")
def index():
    return render_template_string(PAGE, current=read_message())

@app.post("/submit")
def submit():
    if request.form.get("secret") != APP_SECRET:
        abort(403)
    msg = (request.form.get("msg") or "").strip()
    STORE.write_text(msg, "utf-8")
    return redirect("/")

@app.get("/latest")
def latest():
    return jsonify({"message": read_message(), "ts": int(time.time())})

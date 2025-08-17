from flask import Flask, request, redirect, render_template_string, jsonify, abort
import os, pathlib, time

APP_SECRET = os.getenv("APP_SECRET", "mick2020")     # set this on Render
STORE = pathlib.Path("message.txt")                  # where we persist the message

PAGE = """
<!doctype html><title>E-ink Board</title>
<h2>Post a message</h2>
<form method="post" action="/submit">
  <input type="password" name="secret" placeholder="secret" required>
  <br><textarea name="msg" rows="6" cols="40" maxlength="500" required></textarea>
  <br><button type="submit">Post</button>
</form>
<p>Current:</p><pre>{{current}}</pre>
"""

app = Flask(__name__)

def read_current():
    return STORE.read_text(encoding="utf-8") if STORE.exists() else ""

@app.get("/")
def index():
    return render_template_string(PAGE, current=read_current())

@app.post("/submit")
def submit():
    if request.form.get("secret") != APP_SECRET:
        abort(403)
    text = (request.form.get("msg") or "").strip()
    STORE.write_text(text, encoding="utf-8")
    return redirect("/")

@app.get("/latest")
def latest():
    # endpoint the Pi polls
    return jsonify({"message": read_current(), "ts": int(time.time())})



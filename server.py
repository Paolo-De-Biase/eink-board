from flask import Flask, request, redirect, render_template_string, jsonify, abort
import os, pathlib, time

APP_SECRET = os.getenv("APP_SECRET", "mick2020")     # set this on Render
STORE = pathlib.Path("message.txt")                  # where we persist the message

PAGE = """
<!doctype html>
<html>
<head>
  <title>E-ink Board</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f8f9fa;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      min-height: 100vh;
      margin: 0;
      padding: 2rem;
    }
    .container {
      background: white;
      padding: 2rem;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      width: 100%;
      max-width: 500px;
    }
    h2 {
      margin-top: 0;
      color: #333;
    }
    input[type="password"], textarea {
      width: 100%;
      padding: 0.75rem;
      margin-top: 0.5rem;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 1rem;
    }
    button {
      margin-top: 1rem;
      background: #007bff;
      color: white;
      border: none;
      padding: 0.75rem 1.5rem;
      border-radius: 6px;
      cursor: pointer;
      font-size: 1rem;
    }
    button:hover {
      background: #0056b3;
    }
    .current {
      margin-top: 2rem;
      padding: 1rem;
      background: #f1f3f5;
      border-radius: 6px;
      font-family: monospace;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Post a message</h2>
    <form method="post" action="/submit">
      <input type="password" name="secret" placeholder="Secret" required>
      <textarea name="msg" rows="5" maxlength="500" required></textarea>
      <button type="submit">Post</button>
    </form>
    <div class="current">
      <strong>Current:</strong>
      <div>{{current}}</div>
    </div>
  </div>
</body>
</html>
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



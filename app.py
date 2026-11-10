"""Intentionally vulnerable, localhost-only SQL injection teaching demo."""
from threading import Lock
import sqlite3
from flask import Flask, render_template_string, request

app = Flask(__name__)
# In-memory database. Lock serializes accesses across Flask request threads.
db = sqlite3.connect(":memory:", check_same_thread=False)
db_lock = Lock()
with db_lock, db:
    db.execute("CREATE TABLE users (username TEXT, password TEXT)")
    db.executemany(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        [("admin", "SecurePass123"), ("student", "student123")],
    )

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SQL Injection Web Security Demo</title>
<style>
body { font: 16px Arial, sans-serif; max-width: 850px; margin: 36px auto; padding: 0 16px; line-height: 1.5; }
nav a { margin-right: 20px; }
input { display: block; width: 300px; max-width: 90%; padding: 10px; margin: 10px 0; }
button { padding: 10px 20px; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; background: #f1f3f5; padding: 15px; }
.success { color: green; } .failed { color: darkred; }
.warning { padding: 10px; background: #fff0cc; border-left: 4px solid orange; }
</style>
</head>
<body>
<h1>Web Security Demo: SQL Injection</h1>
<p class="warning">For classroom use on 127.0.0.1 only. Never deploy publicly.</p>
<nav><a href="/vulnerable">Vulnerable Login</a><a href="/secure">Secure Login</a></nav>
<h2>{{ mode }} Login</h2>
<form method="post">
<label>Username <input name="username" autocomplete="off" required></label>
<label>Password <input name="password" type="text" autocomplete="off" required></label>
<button type="submit">Login</button>
</form>
{% if result %}<h3 class="{{ status }}">{{ result }}</h3>{% endif %}
{% if query %}<h3>SQL Query</h3><pre>{{ query }}</pre>{% endif %}
<h3>Fictional demo accounts</h3>
<p><code>admin / SecurePass123</code><br><code>student / student123</code></p>
<small>Passwords are intentionally plaintext and visible solely for this teaching demo.</small>
</body>
</html>"""

def show(mode, result="", query="", status=""):
    return render_template_string(PAGE, mode=mode, result=result, query=query, status=status)

@app.route("/")
def index():
    return '<h1>SQL Injection Lab</h1><a href="/vulnerable">Vulnerable Login</a> | <a href="/secure">Secure Login</a>'

@app.route("/vulnerable", methods=["GET", "POST"])
def vulnerable():
    if request.method == "GET":
        return show("Vulnerable")
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    # VULNERABILITY: input is concatenated into executable SQL.
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print("\n[VULNERABLE SQL]", query, flush=True)
    try:
        with db_lock:
            user = db.execute(query).fetchone()
    except sqlite3.Error as exc:
        return show("Vulnerable", f"SQL error: {exc}", query, "failed")
    return show("Vulnerable",
                f"Login successful: {user[0]}" if user else "Login failed",
                query, "success" if user else "failed")

@app.route("/secure", methods=["GET", "POST"])
def secure():
    if request.method == "GET":
        return show("Secure")
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    # DEFENSE: placeholders keep input as data, never SQL syntax.
    query = "SELECT * FROM users WHERE username=? AND password=?"
    print("\n[SECURE SQL]", query, "\nParameters:", repr((username, password)), flush=True)
    with db_lock:
        user = db.execute(query, (username, password)).fetchone()
    return show("Secure",
                f"Login successful: {user[0]}" if user else "Login failed",
                query, "success" if user else "failed")

if __name__ == "__main__":
    print("Vulnerable: http://127.0.0.1:5000/vulnerable")
    print("Secure:     http://127.0.0.1:5000/secure")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)

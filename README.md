# SQL Injection Web Security Demo

A five-minute, Linux-based classroom demonstration of **SQL injection authentication bypass** and its prevention with **parameterized queries**.

**Local-only demonstration.** The Flask application binds to `127.0.0.1:5000` and intentionally contains insecure code. Do not deploy it to a public or shared network.

## Quick start

```bash
git clone https://github.com/jjbaek35/sql-injection-web-demo.git
cd sql-injection-web-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

- Vulnerable login: http://127.0.0.1:5000/vulnerable
- Secure login: http://127.0.0.1:5000/secure

## Documentation

- [Installation instructions](installation.txt)
- [Five-minute lab guide](read.md)
- [Python source](app.py)

No separate SQL database server is required; Python's built-in SQLite module is used.

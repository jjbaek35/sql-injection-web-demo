# SQL Injection: Five-Minute Web Security Lab

## Objective

Demonstrate **authentication bypass through SQL injection**, inspect the
resulting SQL statement, and compare it with the **parameterized query** defense.

**Environment:** Local Linux, Python 3, Flask, SQLite, and a web browser.

**Safety:** Run only on your own machine at `127.0.0.1:5000`. This
application is intentionally vulnerable. The database is in memory and
resets when the server restarts.

## Preparation

Follow [installation.txt](installation.txt), start the application with
`python app.py`, and open these two tabs:

- Vulnerable: http://127.0.0.1:5000/vulnerable
- Secure: http://127.0.0.1:5000/secure

Keep the Flask terminal visible to see the generated SQL statements.

## Instructor walkthrough (5 minutes)

| Time | Action | Expected result | Discussion |
| --- | --- | --- | --- |
| 0:00-1:00 | Vulnerable page: enter `admin` and `wrongpassword`. | Login failed | Normal credential validation |
| 1:00-2:00 | Vulnerable page: enter the SQL injection payload below. | Login successful: admin | Authentication bypass |
| 2:00-3:00 | Examine the SQL statement shown on the page/terminal. | `OR 1=1` and `--` appear | User input becomes SQL syntax |
| 3:00-4:00 | Repeat the same payload on the secure page. | Login failed | Bound input remains data |
| 4:00-5:00 | Compare the two functions in `app.py`. | SQL concatenation vs placeholders | Preventing SQL injection |

## Attack input

**Username** (include a space after the two hyphens):

```text
' OR 1=1 -- 
```

**Password:**

```text
anything
```

**Expected vulnerable result:** `Login successful: admin`

The vulnerable application constructs:

```sql
SELECT * FROM users
WHERE username='' OR 1=1 -- ' AND password='anything'
```

### Why it works

1. The first single quote closes the username literal.
2. `OR 1=1` makes the WHERE condition true.
3. `-- ` comments out the rest of the statement, including the password condition.
4. SQLite returns the first matching record (fictional `admin`).

## Defense: parameterized SQL

The secure version uses placeholders:

```python
query = "SELECT * FROM users WHERE username=? AND password=?"
user = db.execute(query, (username, password)).fetchone()
```

SQLite treats the submitted payload as **data**, not executable SQL.
The identical attack therefore returns `Login failed`.

## Verification table

| Username | Password | Vulnerable | Secure |
| --- | --- | --- | --- |
| `admin` | `SecurePass123` | Login successful: admin | Login successful: admin |
| `admin` | `wrongpassword` | Login failed | Login failed |
| `' OR 1=1 -- ` | `anything` | Login successful: admin | Login failed |

## Discussion questions

1. Why does `OR 1=1` bypass the vulnerable login?
2. How does the SQL comment operator `--` affect the password check?
3. Why are parameterized queries safer than string concatenation?
4. Would password hashing alone fix this SQL injection issue?

## Learning outcomes

Students will be able to identify unsafe query construction,
explain SQL injection authentication bypass, and implement a
parameterized-query defense.

## Instructor and safety notes

- Use only fictional demo accounts and localhost; never deploy this app online.
- Passwords are visibly stored as plaintext *only* for this controlled demo;
  production applications must use password hashing and session security.
- The demo shares an in-memory SQLite connection with a lock; production
  systems should use per-request database connections or connection pooling.
- Avoid destructive or multi-statement payloads; they are unnecessary here.

## Summary

**SQL injection occurs when untrusted input is interpreted as part of
an SQL command. Parameterized queries separate SQL commands from data
and prevent this form of authentication bypass.**

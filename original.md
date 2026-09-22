# App original con las Vulnerabilidades sin corregir

```
"""
App de demostración - INTENCIONALMENTE VULNERABLE
Uso exclusivo para laboratorio de detección con herramientas SAST.
NO desplegar en producción ni exponer a internet.
"""

import hashlib
import os
import sqlite3

from flask import Flask, request

app = Flask(__name__)

# --- Vulnerabilidad 3: Secreto / API key codificada en el código ---
API_KEY = "sk_live_51Hc3jFakeKeyDoNotUse1234567890"


def get_db():
    conn = sqlite3.connect("app.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    return conn


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # --- Vulnerabilidad 1: Inyección SQL (consulta concatenada) ---
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    conn = get_db()
    cursor = conn.execute(query)
    user = cursor.fetchone()

    return {"ok": user is not None}


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    # --- Vulnerabilidad 4: Hash débil (MD5) para contraseñas ---
    hashed = hashlib.md5(password.encode()).hexdigest()

    conn = get_db()
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed)
    )
    conn.commit()
    return {"ok": True}


@app.route("/ping", methods=["GET"])
def ping():
    host = request.args.get("host", "127.0.0.1")

    # --- Vulnerabilidad 2: Inyección de comandos (os.system con entrada de usuario) ---
    result = os.system("ping -c 1 " + host)
    return {"exit_code": result}


@app.route("/files", methods=["GET"])
def read_file():
    filename = request.args.get("name", "readme.txt")

    # --- Vulnerabilidad 6: Path traversal en endpoint de lectura de archivos ---
    with open("uploads/" + filename, "r") as f:
        content = f.read()
    return {"content": content}


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
```
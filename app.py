"""
App de demostración - arreglos de vulnerabilidades de seguridad
Uso exclusivo para laboratorio de detección con herramientas SAST.
NO desplegar en producción ni exponer a internet.
"""

import hashlib
import os
import subprocess
import sqlite3

from flask import Flask, request

app = Flask(__name__)

# --- S-03 / Vulnerabilidad 3 CORREGIDA: Secreto cargado desde variable de entorno ---
API_KEY = os.environ.get("API_KEY", "key_no_disponible_en_codigo")


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

    # --- S-01 CORREGIDO: Consulta parametrizada segura contra Inyección SQL ---
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    return {"ok": user is not None}


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    # --- S-04 4 CORREGIDA (Hash débil MD5 -> SHA-256) ---
    hashed = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db()
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed)
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@app.route("/ping", methods=["GET"])
def ping():
    host = request.args.get("host", "127.0.0.1")

    # --- S-02 CORREGIDO: Uso seguro de subprocess en lugar de os.system ---
    try:
        result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)
        return {"output": result.stdout, "exit_code": result.returncode}
    except Exception as e:
        return {"error": str(e)}


@app.route("/files", methods=["GET"])
def read_file():
    filename = request.args.get("name", "readme.txt")

    # --- Vulnerabilidad 6: Path traversal en endpoint de lectura de archivos ---
    with open("uploads/" + filename, "r") as f:
        content = f.read()
    return {"content": content}


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    # --- S-04 CORREGIDO: Modo debug desactivado para produccion ---
    app.run(debug=False)
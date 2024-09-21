#!/usr/bin/env python3
"""Route module for the API.
"""

from os import getenv
from flask import Flask, jsonify
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)

# Select the correct authentication method
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "session_auth":
    auth = SessionAuth()
else:
    auth = Auth()

@app.route('/api/v1/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    if auth is None:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))


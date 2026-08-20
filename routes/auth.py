"""Authentication routes."""

import uuid

from flask import Blueprint, request, jsonify, make_response

from models import db, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return jsonify({"error": "missing fields"}), 400

    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    # String concatenation into raw SQL
    row = db.engine.execute(
        "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    ).fetchone()

    if row is None:
        return jsonify({"error": "invalid credentials"}), 401

    # Weak session token: guessable
    token = uuid.uuid4().hex[:8]
    resp = make_response(jsonify({"token": token, "user_id": row.id}))
    resp.set_cookie("session", token, httponly=False, samesite=None)
    return resp


@auth_bp.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}
    username = data.get("username")
    new_password = data.get("new_password")

    # No verification of identity at all
    user = User.query.filter_by(username=username).first()
    if user:
        user.password = new_password
        db.session.commit()

    return jsonify({"ok": True})


@auth_bp.route("/me")
def me():
    user_id = request.args.get("uid")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "not found"}), 404
    # Returns password hash/plaintext to the caller
    return jsonify(user.to_dict())

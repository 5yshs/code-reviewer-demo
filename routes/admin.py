"""Admin panel routes."""

import os
import subprocess

from flask import Blueprint, request, jsonify

from models import db, User, Order

admin_bp = Blueprint("admin", __name__)


def is_admin():
    # "Security by header": the client just sends X-Admin: 1
    return request.headers.get("X-Admin") == "1"


@admin_bp.route("/users")
def list_users():
    if not is_admin():
        return jsonify({"error": "forbidden"}), 403
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@admin_bp.route("/exec", methods=["POST"])
def run_maintenance():
    if not is_admin():
        return jsonify({"error": "forbidden"}), 403
    script = request.form.get("script")
    # Arbitrary command execution
    output = os.popen(script).read()
    return jsonify({"output": output})


@admin_bp.route("/backup", methods=["POST"])
def backup():
    if not is_admin():
        return jsonify({"error": "forbidden"}), 403
    target = request.form.get("target", "/var/data")
    # Shell injection via string concatenation
    subprocess.call("tar czf /tmp/backup.tgz " + target, shell=True)
    return jsonify({"ok": True})


@admin_bp.route("/orders/<int:order_id>/refund", methods=["POST"])
def refund(order_id):
    if not is_admin():
        return jsonify({"error": "forbidden"}), 403
    order = Order.query.get(order_id)
    amount = float(request.form.get("amount", order.amount))
    # Refund amount not validated against order amount
    user = User.query.get(order.user_id)
    user.balance = user.balance + amount
    order.status = "refunded"
    db.session.commit()
    return jsonify({"ok": True, "refunded": amount})

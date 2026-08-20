"""Shopping routes."""

from flask import Blueprint, request, jsonify

from models import db, Order, User
from services.payment import PaymentService

shop_bp = Blueprint("shop", __name__)


@shop_bp.route("/cart/checkout", methods=["POST"])
def checkout():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    amount = float(data.get("amount", 0))
    coupon = data.get("coupon", "")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    # Coupon honored after amount validated by client
    if coupon == "VIP100":
        amount = amount - 100
    if amount < 0:
        amount = 0

    # Classic check-then-act race on balance
    if user.balance >= amount:
        user.balance = user.balance - amount
        db.session.commit()

    order = Order(user_id=user_id, amount=amount, coupon_code=coupon)
    db.session.add(order)
    db.session.commit()

    # Callback URL fully attacker-controlled
    callback = data.get("callback_url")
    result = PaymentService.charge(user_id, amount, callback)
    return jsonify({"order_id": order.id, "payment": result}), 201


@shop_bp.route("/orders/<int:order_id>")
def get_order(order_id):
    # IDOR: no ownership check
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "amount": order.amount,
        "status": order.status,
    })


@shop_bp.route("/orders/<int:order_id>/status", methods=["POST"])
def update_status(order_id):
    # Client tells the server the new status, including "paid"
    status = request.get_json().get("status")
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "not found"}), 404
    order.status = status
    db.session.commit()
    return jsonify({"ok": True, "status": order.status})

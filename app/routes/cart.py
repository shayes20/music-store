from flask import Blueprint, render_template, request, redirect, url_for
import json

from .session import get_user
from app.database import get_db_connection

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart", methods=["GET"])
@cart_bp.route("/cart.html", methods=["GET"])
def cart() -> str:
    user = get_user()

    cart_data = request.cookies.get("cart", "[]")
    cart_items = json.loads(cart_data)

    total_items = sum([item["quantity"] for item in cart_items])
    total_price = sum([item["price"] * item["quantity"] for item in cart_items])

    return render_template(
        "cart.html",
        user=user,
        cart_items=cart_items,
        total_items=total_items,
        total_price=total_price,
    )


@cart_bp.route("/purchase", methods=["GET"])
@cart_bp.route("/purchase.html", methods=["GET"])
def purchase() -> str:
    user = get_user()

    if user is None:
        return redirect(url_for("login.login"))

    cart_data = request.cookies.get("cart", "[]")
    cart_items = json.loads(cart_data)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO
                        receipts(username, date, total)
                    VALUES
                        (%s, NOW(), %s)
                    RETURNING id
                    """, (user.username, sum([item['price'] * item['quantity'] for item in cart_items]))
                )

                receipt_id = cur.fetchone()[0]

                for item in cart_items:
                    cur.execute(
                        f"""
                        INSERT INTO
                            purchases(receipt_id, item_id, quantity)
                        VALUES
                            ( %s, %s , %s)
                        """, (receipt_id, item['id'], item['quantity'])
                    )
                cur.close()
        response = redirect(url_for("cart.cart"))
        response.set_cookie("cart", json.dumps([]))

        return response
    except:
        return '', 500

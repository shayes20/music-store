from flask import Blueprint, render_template, redirect, url_for
from .session import get_user
from app.database import get_db_connection

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["GET"])
@orders_bp.route("/orders.html", methods=["GET"])
def orders() -> str:
    user = get_user()

    if user is None:
        return render_template("login.html")

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    receipts.id, receipts.username, receipts.date, receipts.total, SUM(purchases.quantity) as item_count
                FROM
                    receipts
                JOIN
                    purchases
                ON
                    receipts.id = purchases.receipt_id
                WHERE
                    receipts.username = %s
                GROUP BY
                    receipts.id
                ORDER BY
                    receipts.date DESC;
                """, (user.username,)
            )

            orders_raw = cur.fetchall()
            orders = []

            for order_raw in orders_raw:
                order = {
                    "id": order_raw[0],
                    "username": order_raw[1],
                    "date": order_raw[2].strftime("%A, %d %B %Y"),
                    "total": order_raw[3],
                    "items": order_raw[4],
                }

                orders.append(order)
            cur.close()

    return render_template("orders.html", user=user, orders=orders)


@orders_bp.route("/order/<int:order_id>", methods=["GET"])
def order(order_id: int) -> str:
    if order_id is None or not isinstance(order_id, int):
        return redirect(url_for("orders.orders"))

    user = get_user()

    if user is None:
        return redirect(url_for("orders.orders"))

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    purchases.quantity, items.name, items.description, items.image, items.price
                FROM
                    purchases
                JOIN
                    items
                ON
                    purchases.item_id = items.id
                WHERE
                    purchases.receipt_id = %s
                """, (order_id,)
            )

            receipt_items_raw = cur.fetchall()
            receipt_items = []

            for item_raw in receipt_items_raw:
                item = {
                    "quantity": item_raw[0],
                    "name": item_raw[1],
                    "description": item_raw[2],
                    "image": item_raw[3],
                    "price": item_raw[4],
                }

                receipt_items.append(item)

            cur.execute(
                """
                SELECT
                    total, date
                FROM
                    receipts
                WHERE
                    id = %s
                """, (order_id,)
            )

            total_price, date = cur.fetchone()
            date = date.strftime("%A, %d %B %Y")
            cur.close()

    total_items = sum([item["quantity"] for item in receipt_items])

    return render_template(
        "order.html",
        user=user,
        order_id=order_id,
        total_price=total_price,
        total_items=total_items,
        date=date,
        receipt_items=receipt_items,
    )

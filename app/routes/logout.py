from flask import Blueprint, redirect, url_for

logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout", methods=["GET"])
@logout_bp.route("/logout.html", methods=["GET"])
def logout() -> str:
    response = redirect(url_for("index.index"))
    response.set_cookie("session_id", "", expires=0)

    return response

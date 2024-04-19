from flask import Flask


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )


    # Database Setup
    from .database import create_tables

    create_tables()

    # Add Routes
    from .routes import (
        cart_bp,
        index_bp,
        login_bp,
        logout_bp,
        orders_bp,
        register_bp,
    )

    app.register_blueprint(cart_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(register_bp)

    return app

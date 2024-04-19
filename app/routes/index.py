from flask import Blueprint, render_template_string, render_template, request
from .session import get_user
from app.database import get_db_connection

index_bp = Blueprint("index", __name__)


@index_bp.route("/", methods=["GET"])
@index_bp.route("/index", methods=["GET"])
@index_bp.route("/index.html", methods=["GET"])
def index() -> str:
    user = get_user()

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, description, image, price FROM items
                """
            )
            items = cursor.fetchall()
            cursor.close()
    q = request.args.get("q", "")

    return render_template_string(
        """
        {% extends 'base.html' %} {% block content %}
        <form class="mb-4 flex justify-center" action="{{ url_for('index.index') }}">
        <input
            type="text"
            name="q"
            placeholder="Search items..."
            class="px-4 py-2 border rounded-lg w-full sm:w-1/2 lg:w-1/3 mr-4 text-gray-600"
        />
        <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-2 rounded"
        >
            Search
        </button>
        </form>
        {% if q %}
        <p class="text-center mb-4">Search results for <strong>{{ q }}</strong></p>"
        {% endif %}
        <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
        >
        {% for id, name, description, image, price in items %}
        {% if not q or q and q in name or q in description %}
        <div class="bg-white rounded-lg shadow-lg overflow-hidden flex flex-col">
            <img
            src="{{ url_for('static', filename='images'+image) }}"
            alt="{{ name }}"
            class="w-full object-cover"
            />
            <div class="w-full h-0.5 bg-black"></div>
            <div class="p-2 flex flex-grow flex-col">
            <h3 class="font-bold text-lg text-gray-600">{{ name }}</h3>
            <p class="text-sm text-gray-600 mt-1 flex-grow">{{ description }}</p>
            <button
                class="mt-3 w-full bg-blue-500 text-white text-xs font-bold uppercase rounded hover:bg-blue-600 py-2"
                onClick="addToCart({{ id }}, '{{ name }}', '{{ description }}', '{{ image}}', {{ price }})"
            >
                Buy for {{ price }}
            </button>
            </div>
        </div>
        {% endif %}
        {% endfor %}
        </div>
        {% endblock %}
        """,
        items=items,
        user=user,
        q=q,
    )

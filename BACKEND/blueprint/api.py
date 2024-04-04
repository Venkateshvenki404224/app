from flask import Blueprint, render_template
from src.Database import Database

bp = Blueprint("api", __name__, url_prefix="/v1/api/")
db = Database.get_connection()

@bp.route("/", methods=["GET, POST"])
def home():
    return render_template("index.html")

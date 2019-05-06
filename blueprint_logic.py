from flask import Blueprint

logic = Blueprint("logic", __name__)

@logic.route("/login"):
def login(uid, password):
    
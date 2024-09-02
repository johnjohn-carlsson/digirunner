from flask import Blueprint, render_template, request

indexBluePrint = Blueprint('index', __name__)

@indexBluePrint.route('/')
def index():
    return render_template("index.html")
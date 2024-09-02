from flask import Blueprint, render_template, request

mapsBluePrint = Blueprint('maps', __name__)

@mapsBluePrint.route('/maps')
def maps():
 

    return render_template(
        "maps.html"
    )

@mapsBluePrint.route("/maps/wow")
def wow():

    return render_template(
        "wowmaps.html"
    )
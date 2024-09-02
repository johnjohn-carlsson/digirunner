from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from database import *

mapsBluePrint = Blueprint('maps', __name__)

@mapsBluePrint.route('/maps', methods=['GET', 'POST'])
@login_required
def maps():
    return render_template("maps.html")

@mapsBluePrint.route("/maps/wow", methods=['GET', 'POST'])
@login_required
def wow():
    if request.method == 'POST':
        selected_map = request.form.get('selected_route')
        
        update_selected_route(current_user.Username, selected_map)
        
        return redirect(url_for('profile.profile', user=current_user.Username))
    
    return render_template("wowmaps.html")
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import *
from interactive_map import *
import os

profileBluePrint = Blueprint('profile', __name__)

@profileBluePrint.route('/user/<user>', methods=['GET', 'POST'])
@login_required
def profile(user):

    # Ensure the logged-in user can only access their own profile
    if user != current_user.Username:
        flash("You cannot access someone else's profile.", 'error')
        return redirect(url_for('profile.profile', user=current_user.Username))

    leaderboard = fetch_leaderboard()
    profile = fetch_user(user)

    map_image_path = os.path.join('static', 'images', 'usermaps', f"{user}_updated_map.jpg")
    user_has_map = os.path.exists(map_image_path)

    if request.method == 'POST':
        amount_ran = request.form.get('running-results')
        
        if amount_ran:
            db_user = fetch_user(user)
            total_amount_ran_on_map = db_user.ActiveRouteMeters / 1000 + float(amount_ran)
            update_amount_ran(user, amount_ran)

            # Dynamically call the appropriate function based on the selected map
            selected_map_function = f"{profile.ActiveRoute.replace(' ', '_').lower()}_route"
            route_function = globals().get(selected_map_function)

            print(route_function)

            if route_function and callable(route_function):
                route_function(current_user, float(total_amount_ran_on_map))

        return redirect(
            url_for('profile.profile', user=user, leaderboard=leaderboard, user_has_map=user_has_map))
    
    if profile:
        return render_template(
            "profile.html",
            user=profile,
            leaderboard=leaderboard,
            user_has_map = user_has_map
        )
    
    return render_template('index.html')

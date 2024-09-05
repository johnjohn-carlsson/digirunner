from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import *
from interactive_map import *
import os

profileBluePrint = Blueprint('profile', __name__)

@profileBluePrint.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):

    # Ensure the logged-in user can only access their own profile
    if username != current_user.Username:
        flash("You cannot access someone else's profile.", 'error')
        return redirect(url_for('profile.profile', username=current_user.Username))

    leaderboard = fetch_leaderboard()
    profile:User = fetch_user(username)

    map_image_path = os.path.join('static', 'images', 'usermaps', f"{username}_updated_map.jpg")
    user_has_map = os.path.exists(map_image_path)

    if request.method == 'POST':
        amount_ran = float(request.form.get('running-results'))
        
        if amount_ran:
            update_amount_ran(username, amount_ran)
            run_selected_route(profile, profile.ActiveRouteMeters, profile.ActiveRouteWorld, profile.ActiveRoute)

            print("\n\n")
            print(username)
            print(profile)
            print(amount_ran)
            print(profile.ActiveRouteWorld)
            print(profile.ActiveRoute)
            print("\n\n")

        return redirect(
            url_for('profile.profile', username = profile.Username, leaderboard=leaderboard, user_has_map=user_has_map))
    
    if profile:
        return render_template(
            "profile.html",
            user = profile,
            leaderboard=leaderboard,
            user_has_map = user_has_map
        )

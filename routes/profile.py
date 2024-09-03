from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import *
from interactive_map import *

profileBluePrint = Blueprint('profile', __name__)

@profileBluePrint.route('/user/<user>', methods=['GET', 'POST'])
@login_required
def profile(user):

    # Ensure the logged-in user can only access their own profile
    if user != current_user.Username:
        flash("You cannot access someone else's profile.", 'error')
        return redirect(url_for('profile.profile', user=current_user.Username))

    leaderboard = fetch_leaderboard()

    if request.method == 'POST':
        amount_ran = request.form.get('running-results')
        
        if amount_ran:
            db_user = fetch_user(user)

            total_amount_ran_on_map = db_user.ActiveRouteMeters/1000 + float(amount_ran)

            print(total_amount_ran_on_map)

            update_amount_ran(user, amount_ran)
            eastern_kingdoms_route(current_user, float(total_amount_ran_on_map))

        return redirect(
            url_for('profile.profile', user=user, leaderboard=leaderboard))

    profile = fetch_user(user)
    if profile:
        return render_template(
            "profile.html",
            user=profile,
            leaderboard=leaderboard
        )
    
    return render_template('index.html')

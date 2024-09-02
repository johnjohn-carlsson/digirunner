from flask import Blueprint, render_template, request, redirect, url_for
from database import *

profileBluePrint = Blueprint('profile', __name__)

@profileBluePrint.route('/user/<user>', methods=['GET', 'POST'])
def profile(user):

    if request.method == 'POST':
        amount_ran = request.form.get('running-results')
        
        if amount_ran:
            update_amount_ran(user, amount_ran)

        return redirect(url_for('profile.profile', user=user))

    profile = fetch_user(user)
    if profile:

        return render_template(
            "profile.html",
            user = profile,
            )
    
    return render_template('index.index')
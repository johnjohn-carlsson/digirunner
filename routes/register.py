from flask import Blueprint, render_template, request, redirect, flash, url_for
from database import save_to_db

registerBluePrint = Blueprint('register', __name__)

@registerBluePrint.route('/register', methods=['GET', 'POST'])
def register():

    token_images = []
    for n in range(1,17):
        character_image = f'/static/images/char_{n}-removebg-preview.png'
        token_images.append(character_image)

    if request.method == 'POST':
        # Get form data
        token = f"char_{(int(request.form['token']) + 1)}-removebg-preview.png"
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validation checks (you can expand this as needed)
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register.register'))

        user_dictionary = {
            "Token": token,
            "Username": username,
            "Email": email,
            "Password": password
        }

        save_to_db(user_dictionary)

        return redirect(url_for('index.index'))

    return render_template(
        'register.html',
        characters = token_images
        )
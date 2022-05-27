from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import UserAdmin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

authAdmin = Blueprint('authAdmin', __name__)


# new_user = UserAdmin(email='dtcong@gmail.com',
#                      password=generate_password_hash('12345678', method='sha256'))
# db.session.add(new_user)
# db.session.commit()
# login_user(UserAdmin,remember=True)

@authAdmin.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        userAdmin = UserAdmin.query.filter_by(email=email).first()
        if userAdmin:
            if check_password_hash(userAdmin.password, password):
                flash('Logged in successfully!', category='success')
                login_user(userAdmin, remember=True)
                return redirect(url_for('viewsAdmin.home'))
            else:
                flash('Incorrect password. Try Again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("admin/login.html", userAdmin=current_user)


@authAdmin.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authAdmin.login'))

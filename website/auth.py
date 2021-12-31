from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Companies
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        company = Companies.query.filter_by(email=email).first()
        if company:
            if check_password_hash(company.password, password):
                flash('Logged in successfully!', category='success')
                login_user(company, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        company_name = request.form.get('CompanyName')
        mobile_number = request.form.get('MobileNumber')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        company = Companies.query.filter_by(email=email).first()
        if company:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(company_name) < 2:
            flash('Company name must be greater than 1 character.', category='error')
        elif len(mobile_number) < 10:
            flash('Mobile Number must be 10 digits.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_company = Companies(email=email, company_name=company_name,mobile_number=mobile_number, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_company)
            db.session.commit()
            login_user(new_company, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

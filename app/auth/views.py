from flask import flash, url_for, render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import redirect

from app import db
from app.auth import auth
from app.auth.forms import RegistrationForm, LoginForm
from app.models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            login_user(employee)

            return redirect(url_for('home.dashboard'))

        else:
            flash('Invalid email or password')
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('auth.login'))
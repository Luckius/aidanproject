from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort,g
from flask_login import login_user, current_user, logout_user, login_required
from web import app, bcrypt ,db
from web.forms import RegistrationForm, LoginForm
from web.models import User




@app.route("/account" ,methods=['GET', 'POST'])
def account():
    user_data = User.query.all()
    for i in user_data:
        mydate = i.date
        mydate1 = datetime.strptime(mydate,'%Y-%m-%d')
        nowt = datetime.now()
        t = nowt - mydate1
        d = int(t.days)/365
        print(d)
    return render_template('index.html', user_data=user_data)








@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        date = form.dt.data.strftime('%Y-%m-%d')
        converted_date = datetime.strptime(date,'%Y-%m-%d')
        today_time = datetime.now()
        time_diff = today_time - converted_date
        years = int(time_diff.days)/365
        if not years < 18:
            user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                forename=form.forename.data,surname=form.surname.data,date=date)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            flash("Please your under 18 years old, can't register here!","warning")
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            db.session.commit()
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, SampleForm, AddUsersForm
from flaskapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/sampling", methods=['GET', 'POST'])
def sampling():
    # handle for people trying to wrongly access the page
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # create a new form
    form = SampleForm()

    # wait for the submit button to be pressed

    # get results
    results = []

    # if statement doesn't work... rest does
    if form.validate_on_submit():
        some_error = False
        for field in form.survey_questions:
            answer_choice = request.form.getlist(f"{field}")
            try:
                results.append(answer_choice[0])
            except IndexError:
                flash('Invalid Submission', 'danger')
                some_error = True
                break

        # sample results: ['M', '1', '3', 'True']

        if not some_error:
            if current_user.verified:
                sample = Post(gender=results[0], age=results[1], rating=results[2], purchase=bool(results[3]),
                              location=current_user.location, user_id=current_user.id)
                db.session.add(sample)
                db.session.commit()
                flash(f'Sample Submitted!', 'success')
            else:
                flash(f'You have not been verified yet. Please contact CEO Lina Zdruli.', 'warning')

        # format a post for the DB

    return render_template('sampling.html', title='Sampling', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('sampling'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    location=form.location.data)

        # verification set to false by default
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to log in.', 'success')
        # create a way for lina to decide who gets to post samples
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('sampling'))
    form = LoginForm()

    # wait for the submit button to be pressed
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('sampling'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    # delete old image
    old_image = current_user.image_file
    old_image_path = os.path.join(app.root_path, 'static/profile_pics', old_image)
    os.remove(old_image_path)

    # save new image
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)

    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.location.data = current_user.location
    image_file = url_for('static', filename=f"profile_pics/{current_user.image_file}")
    return render_template('account.html', title='Account', image_file=image_file, form=form)


# admin page for lina
@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if 'lina@dafero.com' not in current_user.email:
        return redirect(url_for('account'))

    user_list = User.query.filter_by(verified=False).order_by(User.id.desc()).limit(10)

    # add the users to the output list
    # make user list into a checklist of users to add or delete
    tuple_list = [(user.id, user.email) for user in user_list]

    form = AddUsersForm()

    # add/drop users
    if form.validate_on_submit():
        selections = request.form.getlist('checklist')

        decision = form.verify_or_remove.data
        if 'verify' == decision:
            if len(selections) > 0:
                form.add_users(selections)
                flash(f'{len(selections)} Users verified', 'success')
            else:
                flash('Please select users to verify', 'warning')

        if 'remove' == decision:
            # remove users
            if form.remove_verified.data:
                if len(selections) > 0:
                    form.remove_users(selections)
                    flash(f'{len(selections)} non-verified users removed from database', 'danger')
                else:
                    flash('Please select users to remove', 'warning')
            else:
                flash(f'Please check the confirmation box to remove {len(selections)} users', 'warning')

        return redirect(url_for('admin'))

    return render_template('admin.html', title='Admin', form=form, tuple_list=tuple_list)

# make a way to remove current users


'''
sources:
- https://www.youtube.com/watch?v=ZwCIexvMOGM
- https://stackoverflow.com/questions/12345015/sqlalchemy-get-last-x-rows-in-order/12345374 --> admin page
'''

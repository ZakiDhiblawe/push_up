import re
from flask import Blueprint, redirect, render_template, url_for, request, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required
from .models import User, Workout
from . import db
import os
import secrets
from PIL import Image 
from flask import current_app


main = Blueprint('main', __name__)

@main.route("/profile")
@login_required
def profile():
    return render_template('home/profile.html', user=current_user)

@main.route("/new")
@login_required
def new_workout():
    return render_template('home/new_work.html', name=current_user.name)

@main.route("/new", methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form.get("pushups")
    comment = request.form.get("comment")

    workout = Workout(pushups=pushups, comment=comment, author=current_user)
    db.session.add(workout)
    db.session.commit()

    flash('Your workout has been added')
    return redirect(url_for('main.workouts'))

@main.route('/all')
@login_required
def workouts():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    workouts = user.workouts
    return render_template('home/all.html', workouts=workouts, user=user)

@main.route('/workout/<int:workout_id>/update', methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    
    if request.method == 'POST':
        workout.pushups = request.form.get('pushups')
        workout.comment = request.form.get('comment')
        db.session.commit()

        flash("The workout has been updated")
        return redirect(url_for('main.workouts'))
    return render_template('home/update_workout.html', workout=workout)

@main.route('/workout/<int:workout_id>/delete', methods=['GET'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.workouts'))

@main.route('/workout/<int:workout_id>/delete_dash', methods=['GET'])
@login_required
def del_dash(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.index'))
    

from datetime import datetime

@main.route('/')
@login_required
def index():
    from collections import defaultdict
    from datetime import timedelta

    today = datetime.utcnow().date()

    # Calculate total pushups for today
    workouts_today = Workout.query.filter(
        Workout.user_id == current_user.id,
        Workout.date_posted >= today,
        Workout.date_posted < today + timedelta(days=1)
    ).all()
    total_pushups_today = sum(workout.pushups for workout in workouts_today)

    # Aggregated data for charts
    daily_totals = defaultdict(int)
    monthly_totals = defaultdict(int)

    for workout in Workout.query.filter(
        Workout.user_id == current_user.id,
        Workout.date_posted >= today.replace(day=1),
        Workout.date_posted < (today + timedelta(days=31)).replace(day=1)
    ).all():
        daily_totals[workout.date_posted.date()] += workout.pushups
        monthly_totals[workout.date_posted.strftime('%B')] += workout.pushups
    

    workouts = current_user.workouts
    return render_template(
        'home/index.html',
        user=current_user,
        total_pushups_today=total_pushups_today,
        daily_totals=daily_totals,
        monthly_totals=monthly_totals,
        workouts=workouts
    )


@main.route('/profile/update_info', methods=['POST'])
@login_required
def update_info():
    if 'profile_picture' in request.files:
        picture_file = request.files['profile_picture']
        if picture_file and picture_file.filename != '':
            picture_filename = save_picture(picture_file)
            current_user.profile_picture = picture_filename

    if 'name' in request.form:
        current_user.name = request.form.get('name')

    db.session.commit()
    flash('Your profile information has been updated')
    return redirect(url_for('main.profile'))

@main.route('/profile/update_password', methods=['POST'])
@login_required
def update_password():
    if 'current_password' in request.form and 'new_password' in request.form and 'confirm_password' in request.form:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(current_user.password, current_password):
            flash('The current password is incorrect', 'danger')
            return redirect(url_for('main.profile'))

        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('main.profile'))
        
        strong_password = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not strong_password.match(new_password):
            flash('New password must be at least 8 characters long, include one uppercase letter, one lowercase letter, one number, and one special character (e.g., @, $)', 'danger')
            return redirect(url_for('main.profile'))


        current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        flash('Password has been updated', 'success')

    db.session.commit()
    return redirect(url_for('main.profile'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)

    output_size = (1400, 1250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename




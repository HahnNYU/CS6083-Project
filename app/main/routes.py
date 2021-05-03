from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import TimeBlockOptions, Patient
from app.main.forms import TimePreferenceForm


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home Page')


@bp.route('/time_preference', methods=['GET','POST'])
@login_required
def time_preference():
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        form = TimePreferenceForm()
        form.time_options.choices = [(str(option.time_block_id), str(option)) for option in TimeBlockOptions.query.all()]
        if form.validate_on_submit():
            patient = Patient.query.filter_by(login_id=current_user.id).first()
            for time_id in form.time_options.data: 
                time_block = TimeBlockOptions.query.filter_by(time_block_id=int(time_id)).first()
                patient.add_time(time_block)
            db.session.commit()
        patient = Patient.query.filter_by(login_id=current_user.id).first()
        time_preferences = [str(t) for t in patient.time_preferences]
        return render_template('time_preference.html', title='Patient Time Preference', form=form, time_preferences=time_preferences)


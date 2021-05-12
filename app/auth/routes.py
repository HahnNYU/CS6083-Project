from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import (LoginForm, PatientRegistrationForm, 
                        ProviderRegistrationForm)
from app.models import UserLogin, Address, Patient, Provider, AppointmentMatch
from app.auth.utils import register_geolocate 

from sqlalchemy import or_
from datetime import datetime 



@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserLogin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        if user.user_type == 'Patient':
            return redirect(url_for('main.manage_appointment'))
        elif user.user_type == 'Provider':
            return redirect(url_for('main.index'))
        elif user.user_type =='Admin':
            return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign in', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/patient_register', methods=['GET','POST'])
def patient_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        # Create LoginUser
        user = UserLogin(username=form.username.data, user_type='Patient')
        user.set_password(form.password.data)
        # Create Address
        street = form.street.data 
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data 
        latitude, longitude = register_geolocate(street, city, state, zipcode)
        address = Address(street=street, 
                          city=city,
                          zipcode=zipcode, 
                          state=state,
                          latitude=latitude,
                          longitude=longitude)
        # Create Patient
        patient = Patient(patient_name=form.name.data, 
                          ssn=form.ssn.data,
                          date_of_birth=form.date_of_birth.data, 
                          phone=form.phone.data,
                          email=form.email.data, 
                          max_distance=form.max_distance.data)
        # Push new LoginUser, Address, and Patient to db
        db.session.add(user)
        db.session.add(address)
        db.session.add(patient)
        db.session.commit()
        # Add login_id and address_id to patient are push to db
        patient.login_id = user.id
        patient.address_id = address.address_id
        db.session.commit()
        flash('You are now a registered patient!')
        return redirect(url_for('auth.login'))
    return render_template('auth/patient_register.html', title='Patient Register', form=form)


@bp.route('/provider_register', methods=['GET','POST'])
def provider_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ProviderRegistrationForm()
    if form.validate_on_submit():
        # Create LoginUser
        user = UserLogin(username=form.username.data, user_type='Provider')
        user.set_password(form.password.data)
        # Create Address
        street = form.street.data 
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data 
        latitude, longitude = register_geolocate(street, city, state, zipcode)
        address = Address(street=street, 
                          city=city,
                          zipcode=zipcode, 
                          state=state,
                          latitude=latitude,
                          longitude=longitude)
        # Create Provider
        provider = Provider(provider_name=form.name.data,
                            phone=form.phone.data,
                            provider_type=form.provider_type.data)
        # Push new LoginUser, Address, and Provider to db
        db.session.add(user)
        db.session.add(address)
        db.session.add(provider)
        db.session.commit()
        # Add login_id and address_id to provider are push to db
        provider.login_id = user.id
        provider.address_id = address.address_id
        db.session.commit()
        flash('You are now a registered provider!')
        return redirect(url_for('auth.login'))
    return render_template('auth/provider_register.html', title='Provider Register', form=form)

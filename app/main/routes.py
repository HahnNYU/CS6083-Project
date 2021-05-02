from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import bp


@bp.route('/', methods=['GET'])
def index():
    return 'Home Page'


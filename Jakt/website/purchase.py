from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Purchased
from flask_login import login_required, current_user

bp = Blueprint('purchased', __name__, url_prefix='/purchased')

@bp.route('/')
@login_required
def purchased():
    purchased = Purchased.query.all()
    return render_template('history.html', purchased=purchased, current_id=int(current_user.get_id()))

from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app.models import Project

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
@login_required
def index():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects)

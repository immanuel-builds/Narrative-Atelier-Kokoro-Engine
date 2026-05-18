from flask import redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import Project

bp = Blueprint('projects', __name__)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        project = Project(title=title, description=description, author=current_user)
        db.session.add(project)
        db.session.commit()
    return redirect(url_for('dashboard.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    project = Project.query.get_or_404(id)
    if project.user_id != current_user.id:
        return redirect(url_for('dashboard.index'))
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('dashboard.index'))

@bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    project = Project.query.get_or_404(id)
    if project.user_id != current_user.id:
        return redirect(url_for('dashboard.index'))
    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        project.title = title
        project.description = description
        db.session.commit()
    return redirect(url_for('dashboard.index'))

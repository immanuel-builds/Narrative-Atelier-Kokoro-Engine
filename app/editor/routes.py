from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from app import db
from app.models import Project, Chapter

bp = Blueprint('editor', __name__)

@bp.route('/<int:project_id>')
@login_required
def view(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return redirect(url_for('dashboard.index'))

    chapters = project.chapters.order_by(Chapter.chapter_order).all()
    chapter_id = request.args.get('chapter_id', type=int)

    current_chapter = None
    if chapter_id:
        current_chapter = Chapter.query.get(chapter_id)
        if not current_chapter or current_chapter.project_id != project.id:
            current_chapter = chapters[0] if chapters else None
    else:
        current_chapter = chapters[0] if chapters else None

    return render_template('editor.html', project=project, chapters=chapters, current_chapter=current_chapter)

@bp.route('/<int:project_id>/chapter/create', methods=['POST'])
@login_required
def create_chapter(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return redirect(url_for('dashboard.index'))

    title = request.form.get('title')
    if title:
        last_chapter = project.chapters.order_by(Chapter.chapter_order.desc()).first()
        order = (last_chapter.chapter_order + 1) if last_chapter else 1
        chapter = Chapter(title=title, content="", chapter_order=order, project=project)
        db.session.add(chapter)
        db.session.commit()
        return redirect(url_for('editor.view', project_id=project.id, chapter_id=chapter.id))

    return redirect(url_for('editor.view', project_id=project.id))

@bp.route('/chapter/<int:chapter_id>/save', methods=['POST'])
@login_required
def save_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    if chapter.project.user_id != current_user.id:
        return {"status": "error", "message": "Unauthorized"}, 403

    content = request.form.get('content')
    chapter.content = content
    db.session.commit()
    return {"status": "success"}

@bp.route('/chapter/<int:chapter_id>/delete', methods=['POST'])
@login_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    project_id = chapter.project_id
    if chapter.project.user_id != current_user.id:
        return redirect(url_for('dashboard.index'))

    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for('editor.view', project_id=project_id))

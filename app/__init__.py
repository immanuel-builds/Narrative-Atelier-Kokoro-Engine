from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.dashboard.routes import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.projects.routes import bp as projects_bp
    app.register_blueprint(projects_bp, url_prefix='/projects')

    from app.editor.routes import bp as editor_bp
    app.register_blueprint(editor_bp, url_prefix='/editor')

    @app.route('/')
    def index():
        from flask import render_template
        from flask_login import current_user
        if current_user.is_authenticated:
            from flask import redirect, url_for
            return redirect(url_for('dashboard.index'))
        return render_template('landing.html')

    return app

from app import models

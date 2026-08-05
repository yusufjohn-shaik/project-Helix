# ==========================================
# Project-Helix — DBMS Course Project
# Main Flask Application Entry Point
# ==========================================

import os
import logging
from flask import Flask, render_template
from config import Config

def create_app(config_class=Config):
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Make sure uploads directory exists for saving files
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Setup simple logging to application.log file
    log_dir = os.path.join(app.root_path, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(log_dir, 'application.log'))
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # Import feature routes (Blueprints)
    from routes.auth import auth_bp
    from routes.startup import startup_bp
    from routes.team import team_bp
    from routes.hiring import hiring_bp
    from routes.tasks import tasks_bp
    from routes.funding import funding_bp
    from routes.documents import documents_bp
    from routes.meetings import meetings_bp
    from routes.expenses import expenses_bp
    from routes.reports import reports_bp
    from routes.notifications import notifications_bp

    # Register all routes with Flask app
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(startup_bp, url_prefix='/startups')
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(hiring_bp, url_prefix='/hiring')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(funding_bp, url_prefix='/funding')
    app.register_blueprint(documents_bp, url_prefix='/documents')
    app.register_blueprint(meetings_bp, url_prefix='/meetings')
    app.register_blueprint(expenses_bp, url_prefix='/expenses')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')

    # Home page route
    @app.route('/')
    def index():
        return render_template('dashboard.html')

    # Custom 404 error page handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error="404 - Page Not Found"), 404

    # Custom 500 server error page handler
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error="500 - Internal Server Error"), 500

    return app

# Run local development server
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)


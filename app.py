# ====================================================================
# Project-Helix — Startup Operating System (DBMS Course Project)
# Application Factory & Main Entry Point (9-Table Core Architecture)
# Designed as specified in Project_Helix_DBMS_25B11CS893.pptx
# ====================================================================

import os
import logging
from flask import Flask, render_template, session, redirect, url_for, request
from config import Config

def create_app(config_class=Config):
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure uploads directory exists
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'static/uploads'), exist_ok=True)

    # Setup application logging
    log_dir = os.path.join(app.root_path, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(log_dir, 'application.log'))
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # Import feature routes (Blueprints for 9 core tables)
    from routes.auth import auth_bp
    from routes.startup import startup_bp
    from routes.team import team_bp
    from routes.hiring import hiring_bp
    from routes.tasks import tasks_bp
    from routes.funding import funding_bp
    from routes.reports import reports_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(startup_bp, url_prefix='/startups')
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(hiring_bp, url_prefix='/hiring')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(funding_bp, url_prefix='/funding')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    # Before-request hook to protect application pages
    @app.before_request
    def require_login():
        allowed_endpoints = {'auth.login', 'auth.register', 'static'}
        if 'user_id' not in session and request.endpoint and request.endpoint not in allowed_endpoints:
            return redirect(url_for('auth.login'))

    # Main dashboard route
    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        from services.report_service import ReportService
        from services.startup_service import StartupService
        from services.job_service import JobService
        from services.task_service import TaskService
        from services.funding_service import FundingService

        kpis = ReportService.get_ecosystem_kpis()
        recent_startups = StartupService.get_all_startups()[:5]
        recent_jobs = JobService.get_all_jobs()[:5]
        recent_tasks = TaskService.get_all_tasks()[:5]
        recent_rounds = FundingService.get_funding_rounds()[:5]

        return render_template(
            'dashboard.html',
            kpis=kpis,
            startups=recent_startups,
            jobs=recent_jobs,
            tasks=recent_tasks,
            rounds=recent_rounds
        )

    # Custom 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error="404 - Page Not Found"), 404

    # Custom 500 error handler
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error="500 - Internal Server Error"), 500

    return app

# Development server entry point
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

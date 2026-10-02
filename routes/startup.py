# Startup Routes for 9-Table Database Architecture
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.startup_service import StartupService
from services.job_service import JobService
from services.task_service import TaskService
from services.funding_service import FundingService
from services.authentication_service import AuthenticationService

startup_bp = Blueprint('startup', __name__)

@startup_bp.route('/')
def list_startups():
    """Lists all registered startups."""
    startups = StartupService.get_all_startups()
    return render_template('startup/list.html', startups=startups)

@startup_bp.route('/create', methods=['GET', 'POST'])
def create_startup():
    """Registers a new startup."""
    if 'user_id' not in session:
        flash('Please log in to register a startup.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        industry = request.form.get('industry', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'active')
        founded_date = request.form.get('founded_date')
        created_by = session['user_id']
        
        StartupService.create_startup(name, description, industry, created_by, status, founded_date)
        flash(f'Startup "{name}" registered successfully!', 'success')
        return redirect(url_for('startup.list_startups'))
        
    return render_template('startup/create.html')

@startup_bp.route('/<int:startup_id>')
def detail(startup_id):
    """Renders comprehensive startup portfolio view across 9 tables."""
    startup = StartupService.get_startup_by_id(startup_id)
    if not startup:
        flash('Startup not found.', 'danger')
        return redirect(url_for('startup.list_startups'))

    team = StartupService.get_team_members(startup_id)
    jobs = JobService.get_jobs_by_startup(startup_id)
    projects = TaskService.get_projects(startup_id)
    rounds = FundingService.get_funding_rounds(startup_id)
    all_users = AuthenticationService.get_all_users()

    return render_template(
        'startup/detail.html',
        startup=startup,
        team=team,
        jobs=jobs,
        projects=projects,
        rounds=rounds,
        all_users=all_users
    )

@startup_bp.route('/<int:startup_id>/edit', methods=['GET', 'POST'])
def edit(startup_id):
    """Edits startup information."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    startup = StartupService.get_startup_by_id(startup_id)
    if not startup:
        flash('Startup not found.', 'danger')
        return redirect(url_for('startup.list_startups'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        industry = request.form.get('industry', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'active')
        
        StartupService.update_startup(startup_id, name, description, industry, status)
        flash('Startup updated successfully!', 'success')
        return redirect(url_for('startup.detail', startup_id=startup_id))
        
    return render_template('startup/edit.html', startup=startup)

@startup_bp.route('/<int:startup_id>/delete', methods=['POST'])
def delete_startup(startup_id):
    """Deletes startup and cascades to dependent records."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    StartupService.delete_startup(startup_id)
    flash('Startup deleted successfully.', 'info')
    return redirect(url_for('startup.list_startups'))

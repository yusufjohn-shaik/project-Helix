# Project & Task Management Routes for 9-Table Database Architecture
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.task_service import TaskService
from services.startup_service import StartupService
from services.authentication_service import AuthenticationService

tasks_bp = Blueprint('tasks', __name__)

# ----------------------------------------------------
# Projects Routes
# ----------------------------------------------------
@tasks_bp.route('/')
@tasks_bp.route('/projects')
def projects_list():
    """Lists all ongoing and completed projects."""
    projects = TaskService.get_projects()
    return render_template('tasks/projects_list.html', projects=projects)

@tasks_bp.route('/projects/create', methods=['GET', 'POST'])
def project_create():
    """Creates a new project for a startup."""
    if 'user_id' not in session:
        flash('Please login to create a project.', 'warning')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        startup_id = request.form.get('startup_id')
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        status = request.form.get('status', 'ongoing')
        
        if not startup_id or not name:
            flash('Please choose a startup and provide a project title.', 'danger')
            return redirect(url_for('tasks.project_create'))

        TaskService.create_project(startup_id, name, description, start_date, end_date, status)
        flash(f'Project "{name}" created successfully!', 'success')
        return redirect(url_for('tasks.projects_list'))
        
    startups = StartupService.get_all_startups()
    return render_template('tasks/project_create.html', startups=startups)

@tasks_bp.route('/projects/<int:project_id>')
def project_detail(project_id):
    """Views project details and its full task backlog."""
    project = TaskService.get_project_by_id(project_id)
    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('tasks.projects_list'))

    tasks_list = TaskService.get_tasks_for_project(project_id)
    startup_team = StartupService.get_team_members(project['startup_id']) if project.get('startup_id') else []
    all_users = AuthenticationService.get_all_users()
    
    return render_template(
        'tasks/project_detail.html',
        project=project,
        tasks=tasks_list,
        team_members=startup_team or all_users
    )

@tasks_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
def project_delete(project_id):
    """Deletes project and cascades to tasks."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    TaskService.delete_project(project_id)
    flash('Project deleted.', 'info')
    return redirect(url_for('tasks.projects_list'))

# ----------------------------------------------------
# Tasks Routes
# ----------------------------------------------------
@tasks_bp.route('/list')
def tasks_list():
    """Renders all tasks across all projects."""
    tasks = TaskService.get_all_tasks()
    projects = TaskService.get_projects()
    return render_template('tasks/tasks_list.html', tasks=tasks, projects=projects)

@tasks_bp.route('/create', methods=['GET', 'POST'])
def task_create():
    """Creates a new task in a project."""
    if 'user_id' not in session:
        flash('Please login to create a task.', 'warning')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        project_id = request.form.get('project_id')
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        assigned_to = request.form.get('assigned_to')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority', 'medium')
        status = request.form.get('status', 'pending')
        
        if not project_id or not title:
            flash('Please select a project and provide a task title.', 'danger')
            return redirect(url_for('tasks.task_create'))

        TaskService.create_task(project_id, title, description, assigned_to, due_date, priority, status)
        flash(f'Task "{title}" created!', 'success')
        return redirect(url_for('tasks.project_detail', project_id=project_id))
        
    projects = TaskService.get_projects()
    users = AuthenticationService.get_all_users()
    return render_template('tasks/task_create.html', projects=projects, users=users)

@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
def task_edit(task_id):
    """Edits task details and status."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    task = TaskService.get_task_by_id(task_id)
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('tasks.tasks_list'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        assigned_to = request.form.get('assigned_to')
        status = request.form.get('status', 'pending')
        priority = request.form.get('priority', 'medium')
        
        TaskService.update_task(task_id, title, description, assigned_to, status, priority)
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.project_detail', project_id=task['project_id']))
        
    users = AuthenticationService.get_all_users()
    return render_template('tasks/task_edit.html', task=task, users=users)

@tasks_bp.route('/<int:task_id>/status', methods=['POST'])
def task_update_status(task_id):
    """Quick status change for task."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    new_status = request.form.get('status', 'done')
    project_id = request.form.get('project_id')
    TaskService.update_task_status(task_id, new_status)
    flash(f'Task status updated to {new_status}!', 'success')
    if project_id:
        return redirect(url_for('tasks.project_detail', project_id=project_id))
    return redirect(url_for('tasks.tasks_list'))

# Team Management Routes for 9-Table Database Architecture
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.startup_service import StartupService
from services.authentication_service import AuthenticationService

team_bp = Blueprint('team', __name__)

@team_bp.route('/')
def list_all_team():
    """Lists all team member assignments across all startups."""
    all_members = StartupService.get_all_team_members()
    startups = StartupService.get_all_startups()
    return render_template('team/list.html', team=all_members, startups=startups, is_all=True)

@team_bp.route('/<int:startup_id>')
def list_team(startup_id):
    """Lists team members for a specific startup."""
    team = StartupService.get_team_members(startup_id)
    startup = StartupService.get_startup_by_id(startup_id)
    all_users = AuthenticationService.get_all_users()
    return render_template('team/list.html', team=team, startup=startup, all_users=all_users, is_all=False)

@team_bp.route('/<int:startup_id>/add', methods=['GET', 'POST'])
def add_member(startup_id):
    """Adds a registered user as a team member in a startup."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    startup = StartupService.get_startup_by_id(startup_id)
    if not startup:
        flash('Startup not found.', 'danger')
        return redirect(url_for('startup.list_startups'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        role_in_team = request.form.get('role_in_team', 'Member').strip()
        
        if not user_id:
            flash('Please select a user to add to the team.', 'danger')
            return redirect(url_for('team.add_member', startup_id=startup_id))

        success, msg = StartupService.add_team_member(startup_id, user_id, role_in_team)
        if success:
            flash(msg, 'success')
            return redirect(url_for('startup.detail', startup_id=startup_id))
        else:
            flash(msg, 'warning')
            return redirect(url_for('team.add_member', startup_id=startup_id))
            
    users = AuthenticationService.get_all_users()
    return render_template('team/add_member.html', startup=startup, users=users)

@team_bp.route('/remove/<int:team_id>/<int:startup_id>', methods=['POST'])
def remove_member(team_id, startup_id):
    """Removes a team member assignment."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    StartupService.remove_team_member(team_id)
    flash('Team member removed.', 'info')
    return redirect(url_for('startup.detail', startup_id=startup_id))

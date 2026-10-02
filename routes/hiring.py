# Job / Hiring Routes for 9-Table Database Architecture
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.job_service import JobService
from services.startup_service import StartupService

hiring_bp = Blueprint('hiring', __name__)

@hiring_bp.route('/')
@hiring_bp.route('/jobs')
def jobs_list():
    """Lists all job postings with startup and status info."""
    status_filter = request.args.get('status')
    jobs = JobService.get_all_jobs(status=status_filter)
    startups = StartupService.get_all_startups()
    return render_template('hiring/jobs_list.html', jobs=jobs, startups=startups, current_status=status_filter)

@hiring_bp.route('/jobs/create', methods=['GET', 'POST'])
def job_create():
    """Posts a new job opening for a startup."""
    if 'user_id' not in session:
        flash('Please login to post a job vacancy.', 'warning')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        startup_id = request.form.get('startup_id')
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'open')
        
        if not startup_id or not title:
            flash('Please specify both the startup and job title.', 'danger')
            return redirect(url_for('hiring.job_create'))

        JobService.create_job(startup_id, title, description, status)
        flash(f'Job posting "{title}" created successfully!', 'success')
        return redirect(url_for('hiring.jobs_list'))
        
    startups = StartupService.get_all_startups()
    return render_template('hiring/job_create.html', startups=startups)

@hiring_bp.route('/jobs/<int:job_id>')
def job_detail(job_id):
    """Views job posting details."""
    job = JobService.get_job_by_id(job_id)
    if not job:
        flash('Job posting not found.', 'danger')
        return redirect(url_for('hiring.jobs_list'))
    return render_template('hiring/job_detail.html', job=job)

@hiring_bp.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
def job_edit(job_id):
    """Updates job posting."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    job = JobService.get_job_by_id(job_id)
    if not job:
        flash('Job posting not found.', 'danger')
        return redirect(url_for('hiring.jobs_list'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'open')
        JobService.update_job(job_id, title, description, status)
        flash('Job updated successfully.', 'success')
        return redirect(url_for('hiring.job_detail', job_id=job_id))
        
    return render_template('hiring/job_create.html', job=job, is_edit=True)

@hiring_bp.route('/jobs/<int:job_id>/close', methods=['POST'])
def job_close(job_id):
    """Closes an open job posting."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    JobService.close_job(job_id)
    flash('Job posting marked as closed.', 'info')
    return redirect(url_for('hiring.jobs_list'))

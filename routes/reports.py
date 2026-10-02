# Analytics & Reports Routes for 9-Table Database Architecture
from flask import Blueprint, render_template, jsonify
from services.report_service import ReportService

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
def dashboard():
    """Renders comprehensive reports dashboard querying views."""
    startups = ReportService.get_startup_summaries()
    funding = ReportService.get_funding_report()
    tasks = ReportService.get_task_report()
    jobs = ReportService.get_jobs_report()
    kpis = ReportService.get_ecosystem_kpis()
    return render_template('reports/dashboard.html', startups=startups, funding=funding, tasks=tasks, jobs=jobs, kpis=kpis)

@reports_bp.route('/startups')
@reports_bp.route('/revenue')
def revenue():
    """Renders startup ecosystem summary view report."""
    summaries = ReportService.get_startup_summaries()
    return render_template('reports/revenue.html', summaries=summaries)

@reports_bp.route('/funding')
def funding():
    """Renders funding details and investment report."""
    funding_data = ReportService.get_funding_report()
    return render_template('reports/funding.html', funding_data=funding_data)

@reports_bp.route('/tasks')
def tasks():
    """Renders tasks and projects breakdown report."""
    task_data = ReportService.get_task_report()
    return render_template('reports/tasks.html', task_data=task_data)

@reports_bp.route('/jobs')
@reports_bp.route('/hiring')
def hiring():
    """Renders jobs overview report."""
    jobs_data = ReportService.get_jobs_report()
    return render_template('reports/hiring.html', jobs_data=jobs_data)

@reports_bp.route('/api/metrics')
def api_metrics():
    """JSON API returning view aggregates."""
    summaries = ReportService.get_startup_summaries()
    funding = ReportService.get_funding_report()
    tasks = ReportService.get_task_report()
    jobs = ReportService.get_jobs_report()
    kpis = ReportService.get_ecosystem_kpis()
    return jsonify({
        "kpis": kpis,
        "startups": summaries,
        "funding": funding,
        "tasks": tasks,
        "jobs": jobs
    })

# Analytics & Reporting Service for 9-Table Database Architecture
from database.queries import run_query

class ReportService:
    @staticmethod
    def get_startup_summaries():
        """Retrieve startup executive summaries from vw_startup_summary view."""
        sql = "SELECT * FROM vw_startup_summary ORDER BY startup_id ASC"
        try:
            return run_query(sql)
        except Exception:
            # Fallback direct query
            fallback_sql = """
                SELECT s.startup_id, s.name as startup_name, s.industry, s.status as startup_status, s.founded_date,
                       u.name as founder_name, u.email as founder_email,
                       (SELECT COUNT(*) FROM TEAM_MEMBERS tm WHERE tm.startup_id = s.startup_id) as team_size,
                       (SELECT COUNT(*) FROM PROJECTS p WHERE p.startup_id = s.startup_id) as total_projects,
                       (SELECT COUNT(*) FROM TASKS t JOIN PROJECTS p ON t.project_id = p.project_id WHERE p.startup_id = s.startup_id AND t.status NOT IN ('done', 'completed')) as pending_tasks,
                       NVL((SELECT SUM(i.amount) FROM INVESTMENTS i JOIN FUNDING_ROUNDS fr ON i.round_id = fr.round_id WHERE fr.startup_id = s.startup_id), 0) as total_funding_raised
                FROM STARTUPS s JOIN USERS u ON s.created_by = u.user_id
                ORDER BY s.startup_id ASC
            """
            return run_query(fallback_sql)

    @staticmethod
    def get_funding_report():
        """Retrieve funding rounds and investment analytics from vw_funding_details view."""
        sql = "SELECT * FROM vw_funding_details ORDER BY round_id ASC"
        try:
            return run_query(sql)
        except Exception:
            fallback_sql = """
                SELECT fr.round_id, s.startup_id, s.name as startup_name, fr.round_type, fr.target_amount,
                       fr.status as round_status, fr.round_date,
                       NVL(SUM(i.amount), 0) as total_invested,
                       COUNT(i.investment_id) as investor_count,
                       CASE WHEN fr.target_amount > 0 THEN ROUND((NVL(SUM(i.amount), 0) / fr.target_amount) * 100, 2) ELSE 0 END as funding_percentage
                FROM FUNDING_ROUNDS fr
                JOIN STARTUPS s ON fr.startup_id = s.startup_id
                LEFT JOIN INVESTMENTS i ON fr.round_id = i.round_id
                GROUP BY fr.round_id, s.startup_id, s.name, fr.round_type, fr.target_amount, fr.status, fr.round_date
                ORDER BY fr.round_id ASC
            """
            return run_query(fallback_sql)

    @staticmethod
    def get_jobs_report():
        """Retrieve jobs and recruitment breakdown from vw_jobs_overview view."""
        sql = "SELECT * FROM vw_jobs_overview ORDER BY job_id ASC"
        try:
            return run_query(sql)
        except Exception:
            fallback_sql = """
                SELECT j.job_id, j.startup_id, s.name as startup_name, s.industry as startup_industry,
                       j.title as job_title, j.description as job_description, j.status as job_status, j.posted_date
                FROM JOBS j JOIN STARTUPS s ON j.startup_id = s.startup_id
                ORDER BY j.job_id ASC
            """
            return run_query(fallback_sql)

    @staticmethod
    def get_task_report():
        """Retrieve task breakdown across projects from vw_task_overview view."""
        sql = "SELECT * FROM vw_task_overview ORDER BY task_id ASC"
        try:
            return run_query(sql)
        except Exception:
            fallback_sql = """
                SELECT t.task_id, t.project_id, p.name as project_name, s.startup_id, s.name as startup_name,
                       t.title as task_title, t.description as task_description, t.priority, t.status as task_status,
                       t.due_date, u.user_id as assignee_id, u.name as assignee_name, u.username as assignee_username
                FROM TASKS t
                JOIN PROJECTS p ON t.project_id = p.project_id
                JOIN STARTUPS s ON p.startup_id = s.startup_id
                LEFT JOIN USERS u ON t.assigned_to = u.user_id
                ORDER BY t.task_id ASC
            """
            return run_query(fallback_sql)

    @staticmethod
    def get_ecosystem_kpis():
        """Fetch total counts across all 9 entities for dashboard metrics."""
        sql = """
            SELECT 
                (SELECT COUNT(*) FROM STARTUPS) as total_startups,
                (SELECT COUNT(*) FROM USERS) as total_users,
                (SELECT COUNT(*) FROM TEAM_MEMBERS) as total_team_members,
                (SELECT COUNT(*) FROM JOBS WHERE status = 'open') as open_jobs,
                (SELECT COUNT(*) FROM PROJECTS WHERE status = 'ongoing') as active_projects,
                (SELECT COUNT(*) FROM TASKS WHERE status NOT IN ('done', 'completed')) as pending_tasks,
                (SELECT COUNT(*) FROM FUNDING_ROUNDS) as total_rounds,
                (SELECT COUNT(*) FROM INVESTORS) as total_investors,
                COALESCE((SELECT SUM(amount) FROM INVESTMENTS), 0) as total_capital_invested
        """
        try:
            return run_query(sql, fetchone=True)
        except Exception:
            return {
                "total_startups": 0,
                "total_users": 0,
                "total_team_members": 0,
                "open_jobs": 0,
                "active_projects": 0,
                "pending_tasks": 0,
                "total_rounds": 0,
                "total_investors": 0,
                "total_capital_invested": 0
            }

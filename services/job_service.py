# Job Service for 9-Table Database Architecture
from database.queries import run_query

class JobService:
    @staticmethod
    def get_all_jobs(status=None):
        """Fetch all job openings joined with startup info."""
        if status:
            sql = """SELECT j.job_id, j.startup_id, j.title, j.description, j.status, j.posted_date,
                            s.name as startup_name, s.industry as startup_industry
                     FROM JOBS j
                     JOIN STARTUPS s ON j.startup_id = s.startup_id
                     WHERE j.status = :status
                     ORDER BY j.job_id DESC"""
            return run_query(sql, {"status": status})
        else:
            sql = """SELECT j.job_id, j.startup_id, j.title, j.description, j.status, j.posted_date,
                            s.name as startup_name, s.industry as startup_industry
                     FROM JOBS j
                     JOIN STARTUPS s ON j.startup_id = s.startup_id
                     ORDER BY j.job_id DESC"""
            return run_query(sql)

    @staticmethod
    def get_jobs_by_startup(startup_id):
        """Fetch job postings for a specific startup."""
        sql = """SELECT j.job_id, j.startup_id, j.title, j.description, j.status, j.posted_date,
                        s.name as startup_name
                 FROM JOBS j
                 JOIN STARTUPS s ON j.startup_id = s.startup_id
                 WHERE j.startup_id = :sid
                 ORDER BY j.job_id DESC"""
        return run_query(sql, {"sid": int(startup_id)})

    @staticmethod
    def get_job_by_id(job_id):
        """Fetch a single job record by ID."""
        sql = """SELECT j.job_id, j.startup_id, j.title, j.description, j.status, j.posted_date,
                        s.name as startup_name, s.industry, s.description as startup_desc
                 FROM JOBS j
                 JOIN STARTUPS s ON j.startup_id = s.startup_id
                 WHERE j.job_id = :id"""
        return run_query(sql, {"id": int(job_id)}, fetchone=True)

    @staticmethod
    def create_job(startup_id, title, description, status="open"):
        """Insert a new job posting into JOBS table."""
        sql = """INSERT INTO JOBS (startup_id, title, description, status, posted_date)
                 VALUES (:startup_id, :title, :description, :status, SYSDATE)"""
        params = {
            "startup_id": int(startup_id),
            "title": title.strip(),
            "description": description.strip() if description else "",
            "status": status
        }
        run_query(sql, params, fetchall=False)
        return True

    @staticmethod
    def update_job(job_id, title, description, status):
        """Update job posting details."""
        sql = """UPDATE JOBS 
                 SET title = :title, description = :description, status = :status
                 WHERE job_id = :id"""
        params = {
            "id": int(job_id),
            "title": title.strip(),
            "description": description.strip() if description else "",
            "status": status
        }
        run_query(sql, params, fetchall=False)
        return True

    @staticmethod
    def close_job(job_id):
        """Close an active job posting."""
        sql = "UPDATE JOBS SET status = 'closed' WHERE job_id = :id"
        run_query(sql, {"id": int(job_id)}, fetchall=False)
        return True

    @staticmethod
    def delete_job(job_id):
        """Delete job posting."""
        sql = "DELETE FROM JOBS WHERE job_id = :id"
        run_query(sql, {"id": int(job_id)}, fetchall=False)
        return True

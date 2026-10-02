# Startup & Team Management Service for 9-Table Database Architecture
from database.queries import run_query

class StartupService:
    @staticmethod
    def get_all_startups():
        """Select all startups with founder and team metrics."""
        sql = """SELECT s.startup_id, s.name, s.description, s.industry, s.founded_date, s.status, s.created_by,
                        u.name as founder_name, u.username as founder_username,
                        (SELECT COUNT(*) FROM TEAM_MEMBERS tm WHERE tm.startup_id = s.startup_id) as team_size
                 FROM STARTUPS s
                 JOIN USERS u ON s.created_by = u.user_id
                 ORDER BY s.startup_id DESC"""
        return run_query(sql)

    @staticmethod
    def get_startup_by_id(startup_id):
        """Fetch a single startup record with founder info."""
        sql = """SELECT s.startup_id, s.name, s.description, s.industry, s.founded_date, s.status, s.created_by,
                        u.name as founder_name, u.username as founder_username, u.email as founder_email
                 FROM STARTUPS s
                 JOIN USERS u ON s.created_by = u.user_id
                 WHERE s.startup_id = :id"""
        return run_query(sql, {"id": startup_id}, fetchone=True)

    @staticmethod
    def create_startup(name, description, industry, created_by, status="active", founded_date=None):
        """Insert a new startup into STARTUPS table and automatically add founder to TEAM_MEMBERS."""
        if founded_date:
            sql = """INSERT INTO STARTUPS (name, description, industry, founded_date, status, created_by)
                     VALUES (:name, :description, :industry, TO_DATE(:founded_date, 'YYYY-MM-DD'), :status, :created_by)"""
            params = {
                "name": name.strip(),
                "description": description.strip() if description else "",
                "industry": industry.strip() if industry else "Technology",
                "founded_date": founded_date,
                "status": status,
                "created_by": int(created_by)
            }
        else:
            sql = """INSERT INTO STARTUPS (name, description, industry, founded_date, status, created_by)
                     VALUES (:name, :description, :industry, SYSDATE, :status, :created_by)"""
            params = {
                "name": name.strip(),
                "description": description.strip() if description else "",
                "industry": industry.strip() if industry else "Technology",
                "status": status,
                "created_by": int(created_by)
            }
        run_query(sql, params, fetchall=False)

        # Retrieve new startup_id to add founder as initial team member
        fetch_id_sql = "SELECT MAX(startup_id) as new_id FROM STARTUPS WHERE created_by = :created_by"
        res = run_query(fetch_id_sql, {"created_by": int(created_by)}, fetchone=True)
        if res and res.get('new_id'):
            new_id = res['new_id']
            StartupService.add_team_member(new_id, int(created_by), "Founder")
            return new_id
        return True

    @staticmethod
    def update_startup(startup_id, name, description, industry, status="active"):
        """Update existing startup details; invokes procedure if closing."""
        if status == 'closed':
            try:
                run_query("CALL archive_startup(:id)", {"id": int(startup_id)}, fetchall=False)
            except Exception:
                pass
        sql = """UPDATE STARTUPS 
                 SET name = :name, description = :description, industry = :industry, status = :status
                 WHERE startup_id = :id"""
        params = {
            "id": int(startup_id),
            "name": name.strip(),
            "description": description.strip() if description else "",
            "industry": industry.strip() if industry else "Technology",
            "status": status
        }
        run_query(sql, params, fetchall=False)
        return True

    @staticmethod
    def get_team_members(startup_id):
        """Fetch all team members for a startup."""
        sql = """SELECT tm.team_id, tm.startup_id, tm.user_id, tm.role_in_team, tm.joined_date,
                        u.name as user_name, u.username, u.email, u.role as user_global_role
                 FROM TEAM_MEMBERS tm
                 JOIN USERS u ON tm.user_id = u.user_id
                 WHERE tm.startup_id = :id
                 ORDER BY tm.team_id ASC"""
        return run_query(sql, {"id": int(startup_id)})

    @staticmethod
    def get_all_team_members():
        """Fetch all team member records across all startups."""
        sql = """SELECT tm.team_id, tm.startup_id, tm.user_id, tm.role_in_team, tm.joined_date,
                        s.name as startup_name, u.name as user_name, u.username, u.email
                 FROM TEAM_MEMBERS tm
                 JOIN STARTUPS s ON tm.startup_id = s.startup_id
                 JOIN USERS u ON tm.user_id = u.user_id
                 ORDER BY tm.team_id DESC"""
        return run_query(sql)

    @staticmethod
    def add_team_member(startup_id, user_id, role_in_team):
        """Add a user as a team member in a startup."""
        check_sql = "SELECT team_id FROM TEAM_MEMBERS WHERE startup_id = :sid AND user_id = :uid"
        existing = run_query(check_sql, {"sid": int(startup_id), "uid": int(user_id)}, fetchone=True)
        if existing:
            return False, "User is already an enrolled team member of this startup."

        sql = """INSERT INTO TEAM_MEMBERS (startup_id, user_id, role_in_team, joined_date)
                 VALUES (:startup_id, :user_id, :role_in_team, SYSDATE)"""
        params = {
            "startup_id": int(startup_id),
            "user_id": int(user_id),
            "role_in_team": role_in_team.strip() if role_in_team else "Member"
        }
        run_query(sql, params, fetchall=False)
        return True, "Team member added successfully."

    @staticmethod
    def remove_team_member(team_id):
        """Remove a team member assignment."""
        sql = "DELETE FROM TEAM_MEMBERS WHERE team_id = :id"
        run_query(sql, {"id": int(team_id)}, fetchall=False)
        return True

    @staticmethod
    def delete_startup(startup_id):
        """Delete startup record (cascading deletes associated team, jobs, projects, rounds)."""
        sql = "DELETE FROM STARTUPS WHERE startup_id = :id"
        run_query(sql, {"id": int(startup_id)}, fetchall=False)
        return True

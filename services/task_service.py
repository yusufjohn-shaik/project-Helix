# Project & Task Management Service for 9-Table Database Architecture
from database.queries import run_query

class TaskService:
    # ----------------------------------------------------
    # Projects CRUD
    # ----------------------------------------------------
    @staticmethod
    def get_projects(startup_id=None):
        """Fetch projects optionally filtered by startup."""
        if startup_id:
            sql = """SELECT p.project_id, p.startup_id, p.name, p.description, p.start_date, p.end_date, p.status,
                            s.name as startup_name,
                            (SELECT COUNT(*) FROM TASKS t WHERE t.project_id = p.project_id) as total_tasks,
                            (SELECT COUNT(*) FROM TASKS t WHERE t.project_id = p.project_id AND t.status IN ('done', 'completed')) as completed_tasks
                     FROM PROJECTS p
                     JOIN STARTUPS s ON p.startup_id = s.startup_id
                     WHERE p.startup_id = :sid
                     ORDER BY p.project_id DESC"""
            return run_query(sql, {"sid": int(startup_id)})
        else:
            sql = """SELECT p.project_id, p.startup_id, p.name, p.description, p.start_date, p.end_date, p.status,
                            s.name as startup_name,
                            (SELECT COUNT(*) FROM TASKS t WHERE t.project_id = p.project_id) as total_tasks,
                            (SELECT COUNT(*) FROM TASKS t WHERE t.project_id = p.project_id AND t.status IN ('done', 'completed')) as completed_tasks
                     FROM PROJECTS p
                     JOIN STARTUPS s ON p.startup_id = s.startup_id
                     ORDER BY p.project_id DESC"""
            return run_query(sql)

    @staticmethod
    def get_project_by_id(project_id):
        """Fetch a single project with startup info."""
        sql = """SELECT p.project_id, p.startup_id, p.name, p.description, p.start_date, p.end_date, p.status,
                        s.name as startup_name
                 FROM PROJECTS p
                 JOIN STARTUPS s ON p.startup_id = s.startup_id
                 WHERE p.project_id = :id"""
        return run_query(sql, {"id": int(project_id)}, fetchone=True)

    @staticmethod
    def create_project(startup_id, name, description, start_date=None, end_date=None, status="ongoing"):
        """Create a new project."""
        if start_date and end_date:
            sql = """INSERT INTO PROJECTS (startup_id, name, description, start_date, end_date, status)
                     VALUES (:startup_id, :name, :description, TO_DATE(:start_date, 'YYYY-MM-DD'), TO_DATE(:end_date, 'YYYY-MM-DD'), :status)"""
            params = {
                "startup_id": int(startup_id),
                "name": name.strip(),
                "description": description.strip() if description else "",
                "start_date": start_date,
                "end_date": end_date,
                "status": status
            }
        else:
            sql = """INSERT INTO PROJECTS (startup_id, name, description, start_date, status)
                     VALUES (:startup_id, :name, :description, SYSDATE, :status)"""
            params = {
                "startup_id": int(startup_id),
                "name": name.strip(),
                "description": description.strip() if description else "",
                "status": status
            }
        run_query(sql, params, fetchall=False)
        return True

    @staticmethod
    def update_project(project_id, name, description, status):
        """Update project details."""
        sql = """UPDATE PROJECTS
                 SET name = :name, description = :description, status = :status
                 WHERE project_id = :id"""
        params = {
            "id": int(project_id),
            "name": name.strip(),
            "description": description.strip() if description else "",
            "status": status
        }
        run_query(sql, params, fetchall=False)
        return True

    @staticmethod
    def delete_project(project_id):
        """Delete project."""
        sql = "DELETE FROM PROJECTS WHERE project_id = :id"
        run_query(sql, {"id": int(project_id)}, fetchall=False)
        return True

    # ----------------------------------------------------
    # Tasks CRUD
    # ----------------------------------------------------
    @staticmethod
    def get_tasks_for_project(project_id):
        """Fetch all tasks for a project."""
        sql = """SELECT t.task_id, t.project_id, t.title, t.description, t.assigned_to, t.status, t.due_date, t.priority,
                        u.name as assignee_name, u.username as assignee_username
                 FROM TASKS t
                 LEFT JOIN USERS u ON t.assigned_to = u.user_id
                 WHERE t.project_id = :pid
                 ORDER BY t.task_id DESC"""
        return run_query(sql, {"pid": int(project_id)})

    @staticmethod
    def get_all_tasks():
        """Fetch all tasks across projects."""
        sql = """SELECT t.task_id, t.project_id, t.title, t.description, t.assigned_to, t.status, t.due_date, t.priority,
                        p.name as project_name, s.name as startup_name,
                        u.name as assignee_name, u.username as assignee_username
                 FROM TASKS t
                 JOIN PROJECTS p ON t.project_id = p.project_id
                 JOIN STARTUPS s ON p.startup_id = s.startup_id
                 LEFT JOIN USERS u ON t.assigned_to = u.user_id
                 ORDER BY t.task_id DESC"""
        return run_query(sql)

    @staticmethod
    def get_task_by_id(task_id):
        """Fetch single task by ID."""
        sql = """SELECT t.task_id, t.project_id, t.title, t.description, t.assigned_to, t.status, t.due_date, t.priority,
                        p.name as project_name, p.startup_id
                 FROM TASKS t
                 JOIN PROJECTS p ON t.project_id = p.project_id
                 WHERE t.task_id = :id"""
        return run_query(sql, {"id": int(task_id)}, fetchone=True)

    @staticmethod
    def create_task(project_id, title, description="", assigned_to=None, due_date=None, priority="medium", status="pending"):
        """Create a new task."""
        p_val = priority.lower() if priority else 'medium'
        s_val = status.lower() if status else 'pending'
        uid = int(assigned_to) if assigned_to else None

        if due_date:
            sql = """INSERT INTO TASKS (project_id, title, description, assigned_to, status, due_date, priority)
                     VALUES (:project_id, :title, :description, :assigned_to, :status, TO_DATE(:due_date, 'YYYY-MM-DD'), :priority)"""
            params = {
                "project_id": int(project_id),
                "title": title.strip(),
                "description": description.strip() if description else "",
                "assigned_to": uid,
                "status": s_val,
                "due_date": due_date,
                "priority": p_val
            }
        else:
            sql = """INSERT INTO TASKS (project_id, title, description, assigned_to, status, priority)
                     VALUES (:project_id, :title, :description, :assigned_to, :status, :priority)"""
            params = {
                "project_id": int(project_id),
                "title": title.strip(),
                "description": description.strip() if description else "",
                "assigned_to": uid,
                "status": s_val,
                "priority": p_val
            }
        run_query(sql, params, fetchall=False)
        return True

    @staticmethod
    def update_task_status(task_id, status):
        """Update task status using stored procedure if completing."""
        s_val = status.lower() if status else 'pending'
        if s_val in ['done', 'completed']:
            try:
                run_query("CALL complete_task(:task_id)", {"task_id": int(task_id)}, fetchall=False)
                return True
            except Exception:
                pass
        sql = "UPDATE TASKS SET status = :status WHERE task_id = :task_id"
        run_query(sql, {"status": s_val, "task_id": int(task_id)}, fetchall=False)
        return True

    @staticmethod
    def update_task(task_id, title, description, assigned_to, status, priority):
        """Full update on a task."""
        uid = int(assigned_to) if assigned_to else None
        sql = """UPDATE TASKS
                 SET title = :title, description = :description, assigned_to = :assigned_to,
                     status = :status, priority = :priority
                 WHERE task_id = :id"""
        params = {
            "id": int(task_id),
            "title": title.strip(),
            "description": description.strip() if description else "",
            "assigned_to": uid,
            "status": status.lower(),
            "priority": priority.lower()
        }
        run_query(sql, params, fetchall=False)
        return True

    @staticmethod
    def delete_task(task_id):
        """Delete task."""
        sql = "DELETE FROM TASKS WHERE task_id = :id"
        run_query(sql, {"id": int(task_id)}, fetchall=False)
        return True

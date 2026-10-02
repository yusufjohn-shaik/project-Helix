# Project and Task Models for 9-Table Database Architecture

class Project:
    def __init__(self, project_id=None, startup_id=None, name="", description="", start_date=None, end_date=None, status="ongoing"):
        self.project_id = project_id
        self.startup_id = startup_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "startup_id": self.startup_id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status
        }


class Task:
    def __init__(self, task_id=None, project_id=None, title="", description="", assigned_to=None, status="pending", due_date=None, priority="medium"):
        self.task_id = task_id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.status = status
        self.due_date = due_date
        self.priority = priority

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "due_date": self.due_date,
            "priority": self.priority
        }

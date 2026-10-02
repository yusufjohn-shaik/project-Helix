# Job Model for 9-Table Database Architecture

class Job:
    def __init__(self, job_id=None, startup_id=None, title="", description="", status="open", posted_date=None):
        self.job_id = job_id
        self.startup_id = startup_id
        self.title = title
        self.description = description
        self.status = status
        self.posted_date = posted_date

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "startup_id": self.startup_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "posted_date": self.posted_date
        }

# Hiring / Job Service Wrapper for 9-Table Database Architecture
from .job_service import JobService

class HiringService(JobService):
    """Alias pointing to JobService for backward compatibility."""
    pass

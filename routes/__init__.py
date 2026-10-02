# Routes Package for 9-Table Database Architecture

from .auth import auth_bp
from .startup import startup_bp
from .team import team_bp
from .hiring import hiring_bp
from .tasks import tasks_bp
from .funding import funding_bp
from .reports import reports_bp

__all__ = [
    'auth_bp',
    'startup_bp',
    'team_bp',
    'hiring_bp',
    'tasks_bp',
    'funding_bp',
    'reports_bp'
]

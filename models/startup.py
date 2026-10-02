# Startup and TeamMember Models for 9-Table Database Architecture

class Startup:
    def __init__(self, startup_id=None, name="", description="", industry="", founded_date=None, status="active", created_by=None):
        self.startup_id = startup_id
        self.name = name
        self.description = description
        self.industry = industry
        self.founded_date = founded_date
        self.status = status
        self.created_by = created_by

    def to_dict(self):
        return {
            "startup_id": self.startup_id,
            "name": self.name,
            "description": self.description,
            "industry": self.industry,
            "founded_date": self.founded_date,
            "status": self.status,
            "created_by": self.created_by
        }


class TeamMember:
    def __init__(self, team_id=None, startup_id=None, user_id=None, role_in_team="Member", joined_date=None):
        self.team_id = team_id
        self.startup_id = startup_id
        self.user_id = user_id
        self.role_in_team = role_in_team
        self.joined_date = joined_date

    def to_dict(self):
        return {
            "team_id": self.team_id,
            "startup_id": self.startup_id,
            "user_id": self.user_id,
            "role_in_team": self.role_in_team,
            "joined_date": self.joined_date
        }

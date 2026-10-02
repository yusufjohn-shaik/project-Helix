# User Model for 9-Table Database Architecture

class User:
    def __init__(self, user_id=None, name="", username="", email="", password_hash="", role="member", created_at=None):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at
        }

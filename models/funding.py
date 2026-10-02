# Investor, FundingRound, and Investment Models for 9-Table Database Architecture

class Investor:
    def __init__(self, investor_id=None, name="", email="", phone="", firm_name=""):
        self.investor_id = investor_id
        self.name = name
        self.email = email
        self.phone = phone
        self.firm_name = firm_name

    def to_dict(self):
        return {
            "investor_id": self.investor_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "firm_name": self.firm_name
        }


class FundingRound:
    def __init__(self, round_id=None, startup_id=None, round_type="", target_amount=0.0, status="open", round_date=None):
        self.round_id = round_id
        self.startup_id = startup_id
        self.round_type = round_type
        self.target_amount = float(target_amount or 0.0)
        self.status = status
        self.round_date = round_date

    def to_dict(self):
        return {
            "round_id": self.round_id,
            "startup_id": self.startup_id,
            "round_type": self.round_type,
            "target_amount": self.target_amount,
            "status": self.status,
            "round_date": self.round_date
        }


class Investment:
    def __init__(self, investment_id=None, investor_id=None, round_id=None, amount=0.0, investment_date=None):
        self.investment_id = investment_id
        self.investor_id = investor_id
        self.round_id = round_id
        self.amount = float(amount or 0.0)
        self.investment_date = investment_date

    def to_dict(self):
        return {
            "investment_id": self.investment_id,
            "investor_id": self.investor_id,
            "round_id": self.round_id,
            "amount": self.amount,
            "investment_date": self.investment_date
        }

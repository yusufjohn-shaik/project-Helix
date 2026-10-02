# Funding & Investor Relations Service for 9-Table Database Architecture
from database.queries import run_query, run_transaction

class FundingService:
    # ----------------------------------------------------
    # Investors CRUD
    # ----------------------------------------------------
    @staticmethod
    def get_investors():
        """Fetch all investors with their total investment capital."""
        sql = """SELECT inv.investor_id, inv.name, inv.email, inv.phone, inv.firm_name,
                        NVL(SUM(i.amount), 0) as total_invested,
                        COUNT(i.investment_id) as investment_count
                 FROM INVESTORS inv
                 LEFT JOIN INVESTMENTS i ON inv.investor_id = i.investor_id
                 GROUP BY inv.investor_id, inv.name, inv.email, inv.phone, inv.firm_name
                 ORDER BY inv.investor_id DESC"""
        return run_query(sql)

    @staticmethod
    def get_investor_by_id(investor_id):
        """Fetch a single investor with their portfolio investments."""
        sql = """SELECT investor_id, name, email, phone, firm_name 
                 FROM INVESTORS 
                 WHERE investor_id = :id"""
        return run_query(sql, {"id": int(investor_id)}, fetchone=True)

    @staticmethod
    def create_investor(name, email, phone, firm_name):
        """Create new investor record."""
        sql = """INSERT INTO INVESTORS (name, email, phone, firm_name)
                 VALUES (:name, :email, :phone, :firm_name)"""
        params = {
            "name": name.strip(),
            "email": email.strip(),
            "phone": phone.strip() if phone else "",
            "firm_name": firm_name.strip() if firm_name else "Independent"
        }
        run_query(sql, params, fetchall=False)
        return True

    # ----------------------------------------------------
    # Funding Rounds CRUD
    # ----------------------------------------------------
    @staticmethod
    def get_funding_rounds(startup_id=None):
        """Fetch funding rounds with raised progress."""
        if startup_id:
            sql = """SELECT fr.round_id, fr.startup_id, fr.round_type, fr.target_amount, fr.status, fr.round_date,
                            s.name as startup_name,
                            NVL(SUM(i.amount), 0) as total_raised,
                            COUNT(i.investment_id) as investor_count
                     FROM FUNDING_ROUNDS fr
                     JOIN STARTUPS s ON fr.startup_id = s.startup_id
                     LEFT JOIN INVESTMENTS i ON fr.round_id = i.round_id
                     WHERE fr.startup_id = :sid
                     GROUP BY fr.round_id, fr.startup_id, fr.round_type, fr.target_amount, fr.status, fr.round_date, s.name
                     ORDER BY fr.round_id DESC"""
            return run_query(sql, {"sid": int(startup_id)})
        else:
            sql = """SELECT fr.round_id, fr.startup_id, fr.round_type, fr.target_amount, fr.status, fr.round_date,
                            s.name as startup_name,
                            NVL(SUM(i.amount), 0) as total_raised,
                            COUNT(i.investment_id) as investor_count
                     FROM FUNDING_ROUNDS fr
                     JOIN STARTUPS s ON fr.startup_id = s.startup_id
                     LEFT JOIN INVESTMENTS i ON fr.round_id = i.round_id
                     GROUP BY fr.round_id, fr.startup_id, fr.round_type, fr.target_amount, fr.status, fr.round_date, s.name
                     ORDER BY fr.round_id DESC"""
            return run_query(sql)

    @staticmethod
    def get_funding_round_by_id(round_id):
        """Fetch single round with startup and raised summary."""
        sql = """SELECT fr.round_id, fr.startup_id, fr.round_type, fr.target_amount, fr.status, fr.round_date,
                        s.name as startup_name,
                        NVL((SELECT SUM(amount) FROM INVESTMENTS WHERE round_id = fr.round_id), 0) as total_raised
                 FROM FUNDING_ROUNDS fr
                 JOIN STARTUPS s ON fr.startup_id = s.startup_id
                 WHERE fr.round_id = :id"""
        return run_query(sql, {"id": int(round_id)}, fetchone=True)

    @staticmethod
    def create_funding_round(startup_id, round_type, target_amount, status="open"):
        """Create a funding round for a startup."""
        sql = """INSERT INTO FUNDING_ROUNDS (startup_id, round_type, target_amount, status, round_date)
                 VALUES (:startup_id, :round_type, :target_amount, :status, SYSDATE)"""
        params = {
            "startup_id": int(startup_id),
            "round_type": round_type.strip(),
            "target_amount": float(target_amount),
            "status": status
        }
        run_query(sql, params, fetchall=False)
        return True

    @staticmethod
    def close_round(round_id):
        """Close an active round using stored procedure."""
        try:
            run_query("CALL close_funding_round(:id)", {"id": int(round_id)}, fetchall=False)
        except Exception:
            run_query("UPDATE FUNDING_ROUNDS SET status = 'closed' WHERE round_id = :id", {"id": int(round_id)}, fetchall=False)
        return True

    # ----------------------------------------------------
    # Investments (Associative Table: INVESTORS <-> ROUNDS)
    # ----------------------------------------------------
    @staticmethod
    def add_investment_transaction(round_id, investor_id, amount):
        """Atomic transaction to record an investment."""
        sql_insert = """INSERT INTO INVESTMENTS (investor_id, round_id, amount, investment_date)
                        VALUES (:investor_id, :round_id, :amount, SYSDATE)"""
        params = {
            "investor_id": int(investor_id),
            "round_id": int(round_id),
            "amount": float(amount)
        }
        return run_transaction([(sql_insert, params)])

    @staticmethod
    def get_round_investments(round_id):
        """Fetch all investment tickets for a round."""
        sql = """SELECT i.investment_id, i.investor_id, i.round_id, i.amount, i.investment_date,
                        inv.name as investor_name, inv.firm_name, inv.email as investor_email
                 FROM INVESTMENTS i
                 JOIN INVESTORS inv ON i.investor_id = inv.investor_id
                 WHERE i.round_id = :rid
                 ORDER BY i.investment_id DESC"""
        return run_query(sql, {"rid": int(round_id)})

    @staticmethod
    def get_investor_investments(investor_id):
        """Fetch all investments made by an investor."""
        sql = """SELECT i.investment_id, i.investor_id, i.round_id, i.amount, i.investment_date,
                        fr.round_type, s.name as startup_name
                 FROM INVESTMENTS i
                 JOIN FUNDING_ROUNDS fr ON i.round_id = fr.round_id
                 JOIN STARTUPS s ON fr.startup_id = s.startup_id
                 WHERE i.investor_id = :iid
                 ORDER BY i.investment_id DESC"""
        return run_query(sql, {"iid": int(investor_id)})

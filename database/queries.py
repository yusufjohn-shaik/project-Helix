# ====================================================================
# Project-Helix — Database Query Helpers for PostgreSQL
# Executes parameterized SQL statements and returns dictionary results
# ====================================================================

import re
import logging
from .connection import get_db_connection
from .helpers import row_to_dict, rows_to_dicts

logger = logging.getLogger(__name__)

def format_sql(sql):
    """
    Adapts SQL syntax if needed:
    - Converts :param named placeholders to %(param)s (PostgreSQL format)
    - Replaces Oracle SYSDATE with CURRENT_TIMESTAMP
    - Replaces Oracle NVL() with standard ANSI COALESCE()
    """
    if not sql:
        return sql
    # Match :word not preceded by another colon (avoids ::cast)
    formatted = re.sub(r'(?<!:):([a-zA-Z0-9_]+)', r'%(\1)s', sql)
    formatted = re.sub(r'\bSYSDATE\b', 'CURRENT_TIMESTAMP', formatted, flags=re.IGNORECASE)
    formatted = re.sub(r'\bNVL\b', 'COALESCE', formatted, flags=re.IGNORECASE)
    formatted = re.sub(r'\s+FROM\s+dual\b', '', formatted, flags=re.IGNORECASE)
    return formatted

def run_query(sql, params=None, fetchone=False, fetchall=True):
    """
    Executes a SQL query against PostgreSQL.
    - params: dict of bind parameters (prevents SQL Injection)
    - fetchone: returns a single row as a dict
    - fetchall: returns all rows as a list of dicts
    """
    if params is None:
        params = {}

    conn = None
    cursor = None
    clean_sql = format_sql(sql)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(clean_sql, params)

        if fetchone:
            single_row = cursor.fetchone()
            return row_to_dict(cursor, single_row)
        elif fetchall:
            if cursor.description is not None:
                all_rows = cursor.fetchall()
                return rows_to_dicts(cursor, all_rows)
            else:
                conn.commit()
                return []

        # For write queries where fetchall is False
        conn.commit()
        return []

    except Exception as err:
        logger.error(f"Database query error: {err} | SQL: {clean_sql}")
        if conn:
            conn.rollback()
        raise err

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

def run_transaction(queries_list):
    """
    Runs a list of (sql, params) tuples atomically in a single transaction.
    Rolls back entirely if any statement fails.
    """
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for item in queries_list:
            sql_stmt = format_sql(item[0])
            sql_params = item[1] if item[1] is not None else {}
            cursor.execute(sql_stmt, sql_params)

        conn.commit()
        return True

    except Exception as err:
        if conn is not None:
            conn.rollback()
        logger.error(f"Transaction error: {err}")
        raise err

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

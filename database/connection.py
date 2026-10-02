# ====================================================================
# Project-Helix — PostgreSQL Database Connection
# Designed for College Student Project & Easy Viva Explanation
# ====================================================================

import logging
import psycopg2
from config import Config

logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Opens and returns a direct connection to PostgreSQL database.
    Uses credentials defined in .env (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).
    """
    try:
        connection = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        return connection
    except Exception as err:
        logger.error(f"Failed to connect to PostgreSQL: {err}")
        raise err

def close_db_pool():
    """Cleanup hook for application teardown if needed."""
    pass

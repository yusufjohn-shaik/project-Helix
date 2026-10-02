# ====================================================================
# Project-Helix — Database Setup Script for PostgreSQL
# Automatically executes schema, sample data, triggers, procedures, views & indexes
# ====================================================================

import os
import sys

# Ensure root directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_db_connection

def run_sql_file(connection, file_path):
    """Executes a full SQL script against PostgreSQL."""
    file_name = os.path.basename(file_path)
    print(f"Executing {file_name}...")
    cursor = connection.cursor()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        cursor.execute(content)
        connection.commit()
        print(f"  [OK] Successfully executed {file_name}\n")
    except Exception as e:
        connection.rollback()
        print(f"  [Error] Failed to execute {file_name}: {e}\n")
        raise e
    finally:
        cursor.close()

def initialize_database():
    """Runs all 6 SQL files in the correct sequence."""
    try:
        conn = get_db_connection()
        sql_dir = os.path.join(os.path.dirname(__file__), '..', 'sql')
        
        sql_files = [
            'schema.sql',
            'sample_data.sql',
            'triggers.sql',
            'procedures.sql',
            'views.sql',
            'indexes.sql'
        ]
        
        for sql_file in sql_files:
            file_path = os.path.join(sql_dir, sql_file)
            if os.path.exists(file_path):
                run_sql_file(conn, file_path)
            else:
                print(f"Warning: {sql_file} not found.")

        conn.close()
        print("====================================================================")
        print("[SUCCESS] All 9 PostgreSQL tables and sample data initialized!")
        print("====================================================================")
    except Exception as e:
        print(f"Failed to initialize database: {e}")

if __name__ == '__main__':
    initialize_database()

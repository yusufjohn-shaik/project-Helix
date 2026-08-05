# Project-Helix 🚀 (DBMS Course Project)

Project-Helix is a web application created as a student Database Management Systems (DBMS) project. It manages startup ecosystems, hiring, funding rounds, tasks, documents, meetings, and expenses using an Oracle Database.

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript (Jinja2 Templates)
- **Backend:** Python Flask
- **Database:** Oracle Database (Oracle 10g XE / 19c) connected via `oracledb`

## Project Structure

- `database/`: Connecting to Oracle DB and running SQL queries
- `models/`: Simple Python classes for holding database table data
- `services/`: Helper functions to run SQL queries for each feature
- `routes/`: Flask page routes for handling forms and pages
- `templates/`: HTML templates for UI
- `static/`: CSS styles and JS scripts
- `sql/`: DDL schemas, PL/SQL stored procedures, triggers, views, and sample data
- `docs/`: Project report, ER Diagram, and SRS documentation

## How to Run

1. **Environment Setup:**
   Create `.env` file with your Oracle DB credentials:
   ```env
   DB_USER=helix_admin
   DB_PASSWORD=your_password
   DB_DSN=localhost:1521/XE
   SECRET_KEY=supersecretkey
   ```

2. **Database Setup:**
   Run the scripts in `sql/` folder in Oracle SQL Developer or SQL*Plus:
   - `schema.sql` (Creates tables)
   - `views.sql` (Creates database views)
   - `procedures.sql` (Creates PL/SQL procedures)
   - `triggers.sql` (Creates PL/SQL triggers)
   - `indexes.sql` (Creates indexes)
   - `sample_data.sql` (Inserts sample data)

3. **Install Requirements & Run:**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```


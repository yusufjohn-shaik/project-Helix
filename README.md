# Project-Helix 🚀 (Startup Operating System)

**Academic DBMS Course Project**  
*Aditya University — B.Tech Computer Science Engineering*  
*Project ID:* `25B11CS893` | *Architecture:* 9 Tables (3NF)

Project-Helix is a full-stack, database-driven web application for managing the startup lifecycle end to end. Built with a normalized 9-table relational database on PostgreSQL, it manages founder registrations, startup entities, team allocations, job openings, projects, sprint tasks, venture capital funding rounds, accredited investors, and investment commitments.

---

## 1. Database Architecture (9 Tables in 3NF)

As specified in `Project_Helix_DBMS_25B11CS893.pptx`:

```
+----------------+          1:N          +-----------------+
|     USERS      |---------------------->|    STARTUPS     |
+----------------+                       +-----------------+
| user_id (PK)   |                          | startup_id (PK) |
| name           |                          | name            |
| username (UK)  |                          | industry        |
| email (UK)     |                          | description     |
| password_hash  |                          | founded_date    |
| role           |                          | status          |
| created_at     |                          | created_by (FK) |
+----------------+                          +-----------------+
  |      |                                    |     |     |
  | 1:N  | 1:N                           1:N  |     | 1:N | 1:N
  v      v                               v    v     v     v
+--------------+ +-----------+ +-----------+ +----------+ +----------------+
| TEAM_MEMBERS | |   TASKS   | |   JOBS    | | PROJECTS | | FUNDING_ROUNDS |
+--------------+ +-----------+ +-----------+ +----------+ +----------------+
|team_id (PK)  | |task_id(PK)| |job_id(PK) | |proj_id(PK)| |round_id (PK)  |
|startup_id(FK)| |proj_id(FK)| |startup(FK)| |startup(FK)| |startup_id (FK)|
|user_id (FK)  | |assigned_to| |title      | |name      | |round_type      |
|role_in_team  | |priority   | |status     | |status    | |target_amount   |
|joined_date   | |status     | |posted_date| |start_date| |status          |
+--------------+ +-----------+ +-----------+ +----------+ +----------------+
                                                                |
                                                           1:N  v
                                                         +---------------+
                                                         |  INVESTMENTS  |
                                                         +---------------+
                                                         |investment_idPK|
                                                         |round_id (FK)  |
                                                         |investor_id(FK)|
                                                         |amount         |
                                                         |investment_date|
                                                         +---------------+
                                                                ^
                                                           1:N  |
                                                         +---------------+
                                                         |   INVESTORS   |
                                                         +---------------+
                                                         |investor_id(PK)|
                                                         |name           |
                                                         |email (UK)     |
                                                         |phone          |
                                                         |firm_name      |
                                                         +---------------+
```

### Table Classifications (Slide 8 & 21)
- **7 Strong Entities:** `USERS`, `STARTUPS`, `JOBS`, `PROJECTS`, `TASKS`, `FUNDING_ROUNDS`, `INVESTORS`
- **2 Associative Entities:**
  - `TEAM_MEMBERS`: Resolves Many-to-Many relationship `USERS ↔ STARTUPS`
  - `INVESTMENTS`: Resolves Many-to-Many relationship `INVESTORS ↔ FUNDING_ROUNDS`
- **Total Entities:** 9 | **Total Attributes:** 52

---

## 2. Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript, Jinja2 Templates
- **Backend:** Python 3, Flask (Application Factory & Blueprints)
- **Database:** Oracle Database (10g XE / 11g / 19c / 21c) connected via `python-oracledb`
- **Security:** Werkzeug password hashing, parameterized SQL queries

---

## 3. Project Directory Structure

```
Project-Helix/
├── app.py                      # Flask Application Factory & Blueprints Registration
├── config.py                   # Environment & Database Configurations
├── database/                   # Connection Pool & Query Execution Helpers
│   ├── connection.py           # Oracle Connection Pool with Thick/Thin Mode
│   ├── queries.py              # Parameterized run_query() & run_transaction()
│   ├── helpers.py              # Cursor dictionary mapping helpers
│   └── init_db.py              # Automated SQL DDL runner
├── models/                     # Python Data Models
│   ├── user.py                 # User Model
│   ├── startup.py              # Startup & TeamMember Models
│   ├── job.py                  # Job Model
│   ├── tasks.py                # Project & Task Models
│   └── funding.py              # Investor, FundingRound, Investment Models
├── services/                   # Business Logic & SQL Execution Layer
│   ├── authentication_service.py
│   ├── startup_service.py
│   ├── job_service.py
│   ├── task_service.py
│   ├── funding_service.py
│   └── report_service.py
├── routes/                     # Flask Blueprint Controllers
│   ├── auth.py                 # /auth
│   ├── startup.py              # /startups
│   ├── team.py                 # /team
│   ├── hiring.py               # /hiring
│   ├── tasks.py                # /tasks
│   ├── funding.py              # /funding
│   └── reports.py              # /reports
├── templates/                  # Jinja2 HTML Templates
├── static/                     # CSS stylesheets & client JavaScript
├── sql/                        # PostgreSQL SQL DDL Scripts
│   ├── schema.sql              # 9-Table 3NF DDL & SERIAL Primary Keys
│   ├── triggers.sql            # PL/pgSQL Business Integrity Triggers
│   ├── views.sql               # Database Views (vw_startup_summary, etc.)
│   ├── procedures.sql          # PL/pgSQL Stored Procedures
│   ├── indexes.sql             # Performance B-Tree Indexes
│   └── sample_data.sql         # 10 Sample Rows Per Table (from PPT)
└── docs/                       # Academic Specifications & Diagrams
    ├── ER_Diagram.md           # ER Diagram & Participation Constraints
    ├── SRS.md                  # Software Requirements Specification
    └── VIVA_EXPLANATION_GUIDE.md # Comprehensive DBMS Viva & Defense Guide
```

---

## 4. Setup & Running Instructions

### 1. Database Configuration
Create or configure `.env` in the root directory:
```env
DB_USER=helix_user
DB_PASSWORD=helix123
DB_NAME=helix
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=helix-secret-key-123
```

### 2. Database Initialization
Run the automated DDL runner against PostgreSQL:
```bash
python database/init_db.py
```
This executes sequentially:
1. `sql/schema.sql` (Creates 9 tables in 3NF)
2. `sql/sample_data.sql` (Inserts 10 seed rows per table & sets sequences)
3. `sql/triggers.sql` (PL/pgSQL triggers)
4. `sql/procedures.sql` (Stored procedures)
5. `sql/views.sql` (4 analytical views)
6. `sql/indexes.sql` (14 B-Tree indexes)

### 3. Run Web Application
```bash
pip install -r requirements.txt
python app.py
```
Access the application dashboard at: `http://localhost:5000`

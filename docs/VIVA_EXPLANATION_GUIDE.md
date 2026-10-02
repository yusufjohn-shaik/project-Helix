# Project-Helix — DBMS Viva & Code Explanation Guide
**Student Name:** Shaik Yusuf John  
**Roll No:** 25B11CS893  
**Degree & Branch:** B.Tech — Computer Science & Engineering  
**Institution:** Aditya University  
**Project Title:** Project-Helix — Startup Ecosystem Management System  
**Database:** PostgreSQL (Host: `localhost:5432`, Database: `helix`, User: `helix_user`)  
**Backend:** Python 3 (Flask) via `psycopg2`  
**Architecture:** 9 Tables (3NF), 4 Views, 3 Stored Procedures, 3 Triggers, 14 Indexes  

---

## 1. 30-Second Elevator Pitch (What to Say When the Examiner Says "Explain Your Project")

> *"Good morning Sir/Madam. My project is **Project-Helix**, a comprehensive Startup Ecosystem Management Database. It manages the complete lifecycle of a startup venture—from founder registration, team formation, project milestone tracking, job recruitment, to fundraising rounds and investor equity allocation.*
> 
> *The database is strictly designed in **Third Normal Form (3NF)** and implemented on **PostgreSQL**. It consists of **9 tables** (7 Strong Entities and 2 Associative Entities to resolve Many-to-Many relationships), with **52 total attributes** and **10 explicit relationship constraints** enforcing entity and referential integrity.*
> 
> *The backend application is built using **Python Flask**, which connects directly to PostgreSQL using parameterized SQL queries, database views, and PL/pgSQL stored procedures."*

---

## 2. Database Architecture Breakdown

### A. The 9 Core Tables (Slide 32 Alignment)

| # | Table Name | Type | Primary Key | Description |
|---|---|---|---|---|
| 1 | **`USERS`** | Strong Entity | `user_id` (SERIAL) | Stores founders, team members, investors, and system administrators. |
| 2 | **`STARTUPS`** | Strong Entity | `startup_id` (SERIAL) | Stores registered ventures created by founders (`created_by -> USERS`). |
| 3 | **`TEAM_MEMBERS`** | Associative Entity | `team_id` (SERIAL) | Resolves **M:N** between `USERS` and `STARTUPS`. Links employees to ventures. |
| 4 | **`JOBS`** | Strong Entity | `job_id` (SERIAL) | Stores open recruitment postings published by startups. |
| 5 | **`PROJECTS`** | Strong Entity | `project_id` (SERIAL) | Stores product development milestones for each startup. |
| 6 | **`TASKS`** | Strong Entity | `task_id` (SERIAL) | Stores actionable tasks in a project; optionally assigned to a user. |
| 7 | **`FUNDING_ROUNDS`** | Strong Entity | `round_id` (SERIAL) | Stores capital rounds (Seed, Series A, etc.) raised by startups. |
| 8 | **`INVESTORS`** | Strong Entity | `investor_id` (SERIAL) | Stores profiles of venture funds and individual angel investors. |
| 9 | **`INVESTMENTS`** | Associative Entity | `investment_id` (SERIAL) | Resolves **M:N** between `INVESTORS` and `FUNDING_ROUNDS`. Stores capital tickets. |

---

### B. Why Associative Entities? (Viva Favorite!)

- **Question:** *"Why do you have `TEAM_MEMBERS` and `INVESTMENTS` instead of putting columns directly in USERS or STARTUPS?"*
- **Answer:**
  1. **Users and Startups have a Many-to-Many (M:N) relationship:** One user can be a member/advisor in multiple startups, and one startup has many team members. In relational database theory (1NF/3NF), you cannot store repeating values in a single column. Hence, `TEAM_MEMBERS` breaks this M:N relationship into two 1:N relationships (`STARTUPS -> TEAM_MEMBERS` and `USERS -> TEAM_MEMBERS`).
  2. **Investors and Funding Rounds have a Many-to-Many (M:N) relationship:** An investor can write checks into multiple rounds, and one funding round can receive capital from multiple investors. `INVESTMENTS` stores the individual transaction ticket (`amount`, `investment_date`) resolving the M:N relationship.

---

## 3. Relationships & Participation Constraints (Slides 10–19)

In DBMS, participation determines whether an entity **must** participate in a relationship:
- **Total Participation (Double Line in ER):** Every entity occurrence MUST participate (Enforced with `NOT NULL` Foreign Key).
- **Partial Participation (Single Line in ER):** An entity occurrence CAN exist without participating (Nullable Foreign Key).

### The 10 Relationships in Project-Helix:

1. **User Creates Startup (1:N):**
   - User side: **Partial** (A user does not have to create a startup; they could be a regular member or investor).
   - Startup side: **Total** (`STARTUPS.created_by` is `NOT NULL`). A startup cannot exist without a creator/founder.
2. **Startup Employs Team Member (1:N):**
   - Startup side: **Partial** (A newly registered startup might have no employees yet).
   - TeamMember side: **Total** (`TEAM_MEMBERS.startup_id` is `NOT NULL`).
3. **User Joins Team (1:N):**
   - User side: **Partial** (A user may not have joined any team yet).
   - TeamMember side: **Total** (`TEAM_MEMBERS.user_id` is `NOT NULL`).
4. **Startup Posts Job (1:N):**
   - Startup side: **Partial** (A startup doesn't have to hire).
   - Job side: **Total** (`JOBS.startup_id` is `NOT NULL`). A job posting must belong to a startup.
5. **Startup Manages Project (1:N):**
   - Startup side: **Partial** (A startup may not have created projects yet).
   - Project side: **Total** (`PROJECTS.startup_id` is `NOT NULL`).
6. **Project Contains Tasks (1:N):**
   - Project side: **Partial** (A newly initialized project may have 0 tasks initially).
   - Task side: **Total** (`TASKS.project_id` is `NOT NULL`). A task cannot exist without a parent project.
7. **Task Assigned To User (N:1) — [SPECIAL CASE]:**
   - Task side: **Partial** (`TASKS.assigned_to` is **NULLABLE**). A task can be created unassigned in the backlog.
   - User side: **Partial**. A user does not have to be assigned a task.
   - *Constraint:* `ON DELETE SET NULL`. If the assigned user account is deleted, the task remains intact with `assigned_to = NULL`.
8. **Startup Initiates Funding Round (1:N):**
   - Startup side: **Partial** (Bootstrapped startups don't raise funds).
   - FundingRound side: **Total** (`FUNDING_ROUNDS.startup_id` is `NOT NULL`).
9. **Investor Deploys Investment (1:N):**
   - Investor side: **Partial** (An investor may browse without making an investment).
   - Investment side: **Total** (`INVESTMENTS.investor_id` is `NOT NULL`).
10. **Funding Round Receives Investment (1:N):**
    - FundingRound side: **Partial** (A newly opened round may have received 0 checks so far).
    - Investment side: **Total** (`INVESTMENTS.round_id` is `NOT NULL`).

---

## 4. PostgreSQL Implementation Details

### A. How Auto-Increment Works (`SERIAL` + Sequences)
In PostgreSQL, primary keys use the `SERIAL` pseudo-type:
```sql
CREATE TABLE USERS (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ...
);
```
- Under the hood, PostgreSQL automatically creates a sequence named `users_user_id_seq`.
- In our seed script (`sample_data.sql`), we insert the 10 initial sample records with IDs 1 to 10.
- We then execute:
  ```sql
  SELECT setval('users_user_id_seq', 10);
  ```
  This tells PostgreSQL that the current maximum ID is 10. Any new record inserted via the application will automatically receive ID 11, 12, etc.

---

### B. The 4 Database Views (`sql/views.sql`)
Views are stored virtual tables defined by a SQL query. They simplify reporting and eliminate repetitive, expensive multi-table JOINs in application queries:

1. **`vw_startup_summary`:**
   - Joins `STARTUPS` and `USERS`.
   - Computes aggregated metrics: `team_size`, `total_projects`, `pending_tasks`, and `total_funding_raised`.
   - Powers the Executive Summary report.
2. **`vw_funding_details`:**
   - Joins `FUNDING_ROUNDS`, `STARTUPS`, and `INVESTMENTS`.
   - Computes `total_invested`, `investor_count`, and `funding_percentage` using `SUM()`, `COUNT()`, and `GROUP BY`.
3. **`vw_task_overview`:**
   - Joins `TASKS`, `PROJECTS`, `STARTUPS`, and `USERS`.
   - Displays project and startup names alongside task priority and assignee name.
4. **`vw_jobs_overview`:**
   - Joins `JOBS` and `STARTUPS` for centralized recruitment listings.

---

### C. Stored Procedures & Triggers (`sql/procedures.sql` & `sql/triggers.sql`)

#### 3 Stored Procedures:
1. **`close_funding_round(p_round_id)`:** Marks a funding round as closed in PL/pgSQL.
2. **`archive_startup(p_startup_id)`:** Cascades business status: closes open jobs and puts ongoing projects on hold when a startup shuts down.
3. **`complete_task(p_task_id)`:** Sets task status to `'done'`.

#### 3 Database Triggers:
1. **`trg_startup_founder_ai` (AFTER INSERT on STARTUPS):** Automatically enrolls the startup creator into `TEAM_MEMBERS` with role `'Founder'`.
2. **`trg_investment_status_ai` (AFTER INSERT on INVESTMENTS):** Calculates total funding raised and automatically flips round status to `'funded'` when target amount is reached.
3. **`trg_project_dates_bi` (BEFORE INSERT/UPDATE on PROJECTS):** Validates that `end_date >= start_date`.

---

## 5. How Python Flask Connects to PostgreSQL

The codebase is organized cleanly into 4 distinct layers:
```
[ Browser / User ]
       │  HTTP GET / POST
       ▼
[ Routes (routes/*.py) ]
       │  Calls business logic
       ▼
[ Services (services/*.py) ]
       │  Executes SQL queries
       ▼
[ Database Layer (database/queries.py & connection.py) ]
       │  Uses psycopg2 driver
       ▼
[ PostgreSQL Database (localhost:5432/helix) ]
```

### Parameterized Queries (Preventing SQL Injection)
We **never** concatenate raw user input into SQL strings (no `f"SELECT * FROM USERS WHERE id = {user_id}"`).
Instead, we use bind variables:
```python
sql = "SELECT * FROM USERS WHERE username = %(uname)s"
params = {"uname": username}
cursor.execute(sql, params)
```
PostgreSQL compiles the query execution plan first and treats `%(uname)s` strictly as literal data, making SQL injection impossible.

---

## 6. Top 15 Viva Questions & Direct Answers

#### Q1: What is the normalization level of your database?
> **Answer:** All 9 tables are in **Third Normal Form (3NF)**:
> - **1NF:** All attributes are atomic (no arrays or comma-separated values), and each table has a primary key.
> - **2NF:** It is in 1NF and contains no partial dependencies (all non-key attributes are fully dependent on the entire primary key).
> - **3NF:** It is in 2NF and contains no transitive dependencies (non-key attributes depend only on the primary key, not on other non-key attributes).

#### Q2: What is the difference between `ON DELETE CASCADE` and `ON DELETE SET NULL` in your project?
> **Answer:**
> - `ON DELETE CASCADE`: Used when the child cannot exist without the parent. For example, if a `PROJECT` is deleted, all its `TASKS` are automatically deleted.
> - `ON DELETE SET NULL`: Used when the child can exist independently. In `TASKS`, the foreign key `assigned_to` references `USERS`. If a team member leaves and their user account is deleted, the task is **not** deleted; its `assigned_to` attribute is simply set to `NULL` so someone else can pick it up.

#### Q3: Why did you choose PostgreSQL?
> **Answer:** PostgreSQL is an advanced, open-source object-relational database management system (ORDBMS). It is native on Linux, highly standard, fully ACID compliant, and provides rich support for PL/pgSQL stored procedures, triggers, views, and complex aggregations.

#### Q4: How did you implement auto-incrementing primary keys in PostgreSQL?
> **Answer:** We used the `SERIAL` primary key pseudo-type. When creating a table with `SERIAL`, PostgreSQL automatically creates an integer sequence and sets the column default to `nextval('seq_name')`. We also used `SELECT setval('seq_name', 10);` after inserting the 10 seed rows so that new inserts start at ID 11.

#### Q5: What is the difference between a Database View and a Base Table?
> **Answer:** A base table physically stores data on the disk. A View is a virtual table defined by a SQL query; it does not store data itself. When we query `vw_funding_details`, PostgreSQL runs the underlying JOIN and aggregation query on the fly, keeping the application code simple and clean.

#### Q6: What is a Foreign Key constraint?
> **Answer:** A foreign key is a column or combination of columns in one table that references the primary key of another table, ensuring referential integrity (e.g., you cannot insert a job posting with an invalid or non-existent `startup_id`).

#### Q7: What are the two Associative Entities in your schema and what do they resolve?
> **Answer:**
> 1. `TEAM_MEMBERS` resolves the M:N relationship between `USERS` and `STARTUPS`.
> 2. `INVESTMENTS` resolves the M:N relationship between `INVESTORS` and `FUNDING_ROUNDS`.

#### Q8: What indexes did you create and why?
> **Answer:** We created 14 B-Tree indexes on all foreign key columns (like `idx_tasks_project_id`, `idx_startups_created_by`) and frequent search/filter columns (like `email`, `status`, `industry`). In PostgreSQL, indexing foreign keys dramatically speeds up JOIN operations and prevents full table scans.

#### Q9: How are passwords stored in the database?
> **Answer:** Passwords are never stored in plain text. They are hashed using a cryptographic hash function (`werkzeug.security.generate_password_hash`). Only the irreversible salt and hash are stored in `USERS.password_hash`.

#### Q10: What is a Stored Procedure? Where did you use it?
> **Answer:** A stored procedure is a precompiled collection of PL/pgSQL statements stored directly inside the PostgreSQL database engine. We implemented:
> - `close_funding_round(p_round_id)`: closes fundraising.
> - `archive_startup(p_startup_id)`: handles business shutdown by cascading status updates to open jobs and projects.
> - `complete_task(p_task_id)`: marks a task complete.

#### Q11: What is a Trigger in PostgreSQL? Give an example from your project.
> **Answer:** A trigger is a database callback function that executes automatically in response to certain events (`INSERT`, `UPDATE`, `DELETE`) on a specific table. For example, our trigger `trg_investment_status_ai` executes `AFTER INSERT ON INVESTMENTS`: it sums all investments for the round, and if the total meets or exceeds the target, it automatically updates the funding round status from `'open'` to `'funded'`.

#### Q12: Can a Task exist without an Assignee?
> **Answer:** Yes, because the participation of Task in the assignment relationship is **Partial** (`assigned_to` is nullable). This models real-world backlogs where tasks are created before being assigned.

#### Q13: Can a Task exist without a Project?
> **Answer:** No, because `TASKS.project_id` has a `NOT NULL` constraint with `ON DELETE CASCADE`. A task must belong to a project milestone.

#### Q14: How did you connect Python to PostgreSQL?
> **Answer:** We used the official `psycopg2` driver in Python. Our `database/connection.py` module establishes connections using the database credentials, and `database/queries.py` wraps execution in reusable `run_query()` functions with parameter binding.

#### Q15: How do you demonstrate the system live to the examiner?
> **Answer:**
> 1. Show the 9 tables in terminal using `psql -U helix_user -d helix`: run `\dt`.
> 2. Query a view: `SELECT * FROM vw_startup_summary LIMIT 3;`.
> 3. Launch the web application: `python app.py` and open `http://localhost:5000/`.
> 4. Log in as founder `aarav` and show the 9 KPI counters on the dashboard.
> 5. Create a new Task from the web UI to demonstrate the auto-increment sequence assigning ID 11.
> 6. Show the Reports page to demonstrate the database Views calculating live totals.

---

## 7. Quick Setup Commands on Linux Laptop

### Step 1: Inspect Database in psql Terminal
```bash
psql -U helix_user -d helix -h localhost
-- Enter password: helix123
\dt
-- Shows all 9 tables: USERS, STARTUPS, TEAM_MEMBERS, JOBS, PROJECTS, TASKS, FUNDING_ROUNDS, INVESTORS, INVESTMENTS
\dv
-- Shows all 4 views: vw_startup_summary, vw_funding_details, vw_task_overview, vw_jobs_overview
\q
```

### Step 2: Initialize Database via Python
```bash
./venv/bin/python database/init_db.py
```
*(Runs `schema.sql`, `sample_data.sql`, `triggers.sql`, `procedures.sql`, `views.sql`, and `indexes.sql`).*

### Step 3: Run the Web Server
```bash
./venv/bin/python app.py
```
Access at: **`http://127.0.0.1:5000/`**
- **Test Login:** Username: `aarav` | Password: `password123`

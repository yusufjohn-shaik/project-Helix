# User Manual & Operating Guide
## Project-Helix — Startup Operating System (PostgreSQL)
**Student Name:** Shaik Yusuf John  
**Roll No:** 25B11CS893  
**Institution:** Aditya University  

---

### Quick Start Guide

#### 1. Setup & Database Initialization
1. Ensure **PostgreSQL** is running (`localhost:5432`, Database: `helix`, User: `helix_user`).
2. Run database setup:
   ```bash
   python database/init_db.py
   ```
   This automatically executes:
   - `sql/schema.sql` (Creates 9 tables in 3NF with SERIAL auto-increment primary keys)
   - `sql/sample_data.sql` (Inserts 10 seed records per table & resets sequences to 10)
   - `sql/triggers.sql` (PL/pgSQL business integrity triggers)
   - `sql/procedures.sql` (Stored procedures for lifecycle updates)
   - `sql/views.sql` (4 analytical aggregation views)
   - `sql/indexes.sql` (B-Tree indexes for fast queries)
3. Start the Flask application:
   ```bash
   python app.py
   ```
   Open your browser at `http://127.0.0.1:5000/`.

---

#### 2. Registration & Authentication
- **Register:** Navigate to `/auth/register` to create a new user profile (`USERS` table).
- **Login:** Log in at `/auth/login` using your username or email. Preloaded sample founders include:
  - Username: `aarav` | Password: `password123`
  - Username: `diya` | Password: `password123`
- **Profile:** Manage your account details and change password at `/auth/profile`.

---

#### 3. Managing Startups & Teams
- **Register Startup:** Go to **Startups -> + Register Startup** to create a new venture (`STARTUPS` table).
- **Startup Directory:** View all ventures, filter by industry, and inspect profiles.
- **Team Allocation:** From the startup detail page or **Team Members** menu, assign users to startups with designated roles (`Founder`, `Developer`, `Designer`, `Advisor`) in `TEAM_MEMBERS`.

---

#### 4. Project Milestones & Task Backlog
- **Projects:** Create milestones under **Tasks -> View Projects -> + Create Project** (`PROJECTS` table).
- **Task Backlog:** Create tasks and assign them to specific team members or leave unassigned (`TASKS` table).
- **Task Status:** Update task states (`Pending`, `In Progress`, `Completed`) directly from the board or edit modal.

---

#### 5. Recruitment & Job Postings
- **Post Jobs:** Add open positions under **Jobs -> + Post New Job** (`JOBS` table).
- **Manage Openings:** Update status between `Open`, `Filled`, and `Closed`.

---

#### 6. Funding Rounds & Capital Investment
- **Open Funding Round:** Go to **Funding -> + Create Funding Round** (`FUNDING_ROUNDS` table) with target capital goals.
- **Investor Directory:** Manage venture capital firms and angel investors (`INVESTORS` table).
- **Record Investment:** Enter investment tickets directly into `INVESTMENTS` on the round details page.
- **Close Round:** Mark completed rounds as `Closed` with one click.

---

#### 7. Analytics & Database Reports
- **Executive Summary:** Aggregated startup metrics powered by `vw_startup_summary`.
- **Funding Report:** Progress against fundraising goals powered by `vw_funding_details`.
- **Task Report:** Cross-project productivity tracking powered by `vw_task_overview`.
- **Hiring Report:** Industry-wide talent acquisition stats powered by `vw_jobs_overview`.

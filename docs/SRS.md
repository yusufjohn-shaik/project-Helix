# Software Requirements Specification (SRS)
## Project Helix — Startup Operating System (9-Table Relational DBMS)
**Institution:** Aditya University — B.Tech Computer Science Engineering  
**Project ID:** 25B11CS893

### 1. Introduction
Project Helix is a centralized, database-driven Startup Management System built to manage the startup lifecycle from team formation to project execution and investor capitalization.

### 2. Architecture & Technology Stack
- **Frontend Layer:** HTML5, CSS3, JavaScript (Jinja2 Templates)
- **Database Management System:** PostgreSQL (v14+ / v18) via `psycopg2`
- **Schema Normalization:** 9 Relational Tables in 3NF (7 Strong Entities, 2 Associative Entities)

### 3. Functional Requirements (9 Core Entities)
1. **User Management (`USERS`):** Secure authentication, password hashing, session control, and identity roles (`founder`, `member`, `admin`, `investor`).
2. **Startup Management (`STARTUPS`):** Registration of startup entities, industry classification, founding dates, and status lifecycle.
3. **Team Allocation (`TEAM_MEMBERS`):** Resolves Many-to-Many relationships between Users and Startups with assigned organizational roles.
4. **Job Board (`JOBS`):** Startup vacancy postings with position descriptions and recruitment status.
5. **Projects (`PROJECTS`):** Company milestone initiatives with target execution dates.
6. **Task Execution (`TASKS`):** Assignable task backlog linked to projects with priority queues, due dates, and execution states.
7. **Funding Rounds (`FUNDING_ROUNDS`):** Capital raise cycles (`Seed`, `Series A`, `Series B`) with target amounts and funding progress.
8. **Investor Directory (`INVESTORS`):** Accredited angel and venture firm profiles.
9. **Investment Ledger (`INVESTMENTS`):** Transactional commitment ledger linking investors to funding rounds.
10. **Analytics & Views:** Real-time database views (`vw_startup_summary`, `vw_funding_details`, `vw_task_overview`, `vw_jobs_overview`).

### 4. Non-Functional Requirements & DBMS Integrity
- **Relational Integrity:** Foreign key constraints with `ON DELETE CASCADE` and `ON DELETE SET NULL`.
- **Domain Constraints:** `CHECK` constraints on status fields, amounts, and non-empty titles.
- **Participation Constraints:** Explicit total vs. partial participation enforcement at DDL level.
- **Performance:** B-tree indexes on foreign keys, email lookups, and status filters.

# Project-Helix — 2-Minute Video Presentation Script (Oracle 10g XE)
**Project Title:** Project-Helix — Startup Ecosystem Management System  
**Target RDBMS:** Oracle Database 10g Express Edition (XE)  
**Backend:** Python Flask  
**Total Target Time:** Exactly 2 Minutes (approx. 270 words)  

---

### [0:00 – 0:25] 1. Project Overview & Tech Stack (25 Seconds)
*🎥 [Screen: Project-Helix Dashboard or Title Slide]*

> *"Welcome to the demonstration of **Project-Helix**, an end-to-end Startup Ecosystem Management System designed to govern the entire startup lifecycle—from founder onboarding and team allocation to project milestone tracking and venture fundraising.*  
> 
> *The system is powered by **Oracle Database 10g Express Edition (XE)** as the core relational database engine, connected to a responsive **Python Flask** web application."*

---

### [0:25 – 1:00] 2. Database Architecture (3NF Schema) (35 Seconds)
*🎥 [Screen: ER Diagram / Slide 32]*

> *"The underlying database is strictly normalized in **Third Normal Form (3NF)**, comprising **9 tables** and **52 attributes**.*  
> 
> *It models **7 Strong Entities**—Users, Startups, Jobs, Projects, Tasks, Funding Rounds, and Investors.*  
> 
> *To resolve Many-to-Many relationships without data redundancy, the schema incorporates **2 Associative Entities**: `TEAM_MEMBERS`, which maps users to startups with specific team roles, and `INVESTMENTS`, which links investors to funding rounds with transactional check sizes.*  
> 
> *All 10 relationships enforce referential integrity with cascading constraints and partial-participation rules."*

---

### [1:00 – 1:35] 3. Live Web Application Walkthrough (35 Seconds)
*🎥 [Screen: Switch to Browser at http://localhost:5000]*

> *[Showing Dashboard]*  
> *"On the live Dashboard, real-time KPI counters reflect current data across all 9 database entities.*  
> 
> *[Clicking Startups & Team]*  
> *Under **Startups**, founders can register new ventures, while the **Team** module handles member allocations.*  
> 
> *[Clicking Tasks]*  
> *In **Tasks**, we track project deliverables and task priority queues, supporting unassigned backlog items via nullable foreign keys.*  
> 
> *[Clicking Funding & Reports]*  
> *Under **Funding**, startups open investment rounds where investors deploy capital tickets. The **Reports** section is directly powered by 4 analytical database views for real-time aggregated metrics."*

---

### [1:35 – 1:50] 4. Oracle 10g XE Database Features (15 Seconds)
*🎥 [Screen: Show SQL Scripts folder or SQL*Plus]*

> *"At the database layer, we leverage core Oracle 10g XE features:*  
> *- **Oracle Sequences** paired with `BEFORE INSERT` triggers to automate primary key generation.*  
> *- **PL/SQL Stored Procedures** for round closures and operational status cascades.*  
> *- And **14 B-Tree Indexes** on foreign keys to optimize query execution plans."*

---

### [1:50 – 2:00] 5. Conclusion (10 Seconds)
*🎥 [Screen: Final Dashboard / Summary View]*

> *"Project-Helix demonstrates how enterprise relational database design and ACID compliance can power a robust, scalable startup operating system.*  
> *Thank you!"*

-- ====================================================================
-- Project-Helix — Sample Data (10 Records Per Table)
-- Designed for Oracle 10g Express Edition (XE) & SQL*Plus
-- Exact records as presented in Project_Helix_DBMS_25B11CS893.pptx
-- ====================================================================

-- 1. USERS (10 records)
INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (1, 'Aarav Sharma', 'aarav', 'aarav@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'founder', TO_DATE('2025-01-10', 'YYYY-MM-DD'));

INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (2, 'Diya Verma', 'diya', 'diya@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'founder', TO_DATE('2025-01-12', 'YYYY-MM-DD'));

INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (3, 'Kabir Singh', 'kabir', 'kabir@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'founder', TO_DATE('2025-01-15', 'YYYY-MM-DD'));

INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (4, 'Meera Iyer', 'meera', 'meera@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'founder', TO_DATE('2025-01-18', 'YYYY-MM-DD'));

INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (5, 'Rohan Nair', 'rohan', 'rohan@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'founder', TO_DATE('2025-01-20', 'YYYY-MM-DD'));

INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (6, 'Sara Khan', 'sara', 'sara@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'member', TO_DATE('2025-02-01', 'YYYY-MM-DD'));

INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (7, 'Vikram Rao', 'vikram', 'vikram@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'member', TO_DATE('2025-02-05', 'YYYY-MM-DD'));

INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (8, 'Anika Gupta', 'anika', 'anika@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'member', TO_DATE('2025-02-10', 'YYYY-MM-DD'));

INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (9, 'Ishaan Das', 'ishaan', 'ishaan@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'member', TO_DATE('2025-02-15', 'YYYY-MM-DD'));

INSERT INTO USERS (user_id, name, username, email, password_hash, role, created_at)
VALUES (10, 'Priya Menon', 'priya', 'priya@mail.com', 'scrypt:32768:8:1$salt$e10adc3949ba59abbe56e057f20f883e', 'admin', TO_DATE('2025-02-20', 'YYYY-MM-DD'));

-- 2. STARTUPS (10 records)
INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (1, 'NovaCart', 'E-commerce automation platform', 'E-commerce', TO_DATE('2024-03-01', 'YYYY-MM-DD'), 'active', 1);

INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (2, 'QuickLedger', 'Accounting SaaS for small business', 'FinTech', TO_DATE('2024-04-15', 'YYYY-MM-DD'), 'active', 2);

INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (3, 'AgroSense', 'IoT sensors for precision farming', 'AgriTech', TO_DATE('2024-05-10', 'YYYY-MM-DD'), 'active', 3);

INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (4, 'EduSpark', 'Adaptive learning platform for schools', 'EdTech', TO_DATE('2024-06-01', 'YYYY-MM-DD'), 'planning', 4);

INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (5, 'GreenGrid', 'Renewable energy monitoring dashboard', 'CleanTech', TO_DATE('2024-06-20', 'YYYY-MM-DD'), 'active', 5);

INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (6, 'MediTrack', 'Hospital inventory management system', 'HealthTech', TO_DATE('2024-07-05', 'YYYY-MM-DD'), 'active', 1);

INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (7, 'FitPulse', 'Wearable fitness analytics app', 'HealthTech', TO_DATE('2024-08-01', 'YYYY-MM-DD'), 'active', 2);

INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (8, 'UrbanMove', 'Smart city ride-sharing platform', 'Mobility', TO_DATE('2024-08-15', 'YYYY-MM-DD'), 'planning', 3);

INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (9, 'PayEase', 'Cross-border micro-payments gateway', 'FinTech', TO_DATE('2024-09-01', 'YYYY-MM-DD'), 'active', 4);

INSERT INTO STARTUPS (startup_id, name, description, industry, founded_date, status, created_by)
VALUES (10, 'SkillForge', 'Vocational skills marketplace', 'EdTech', TO_DATE('2024-09-20', 'YYYY-MM-DD'), 'closed', 5);

-- 3. TEAM_MEMBERS (10 records)
INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (1, 1, 1, 'Founder', TO_DATE('2024-03-01', 'YYYY-MM-DD'));

INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (2, 1, 6, 'Developer', TO_DATE('2024-03-05', 'YYYY-MM-DD'));

INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (3, 2, 2, 'Founder', TO_DATE('2024-04-15', 'YYYY-MM-DD'));

INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (4, 2, 7, 'Designer', TO_DATE('2024-04-20', 'YYYY-MM-DD'));

INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (5, 3, 3, 'Founder', TO_DATE('2024-05-10', 'YYYY-MM-DD'));

INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (6, 3, 8, 'Developer', TO_DATE('2024-05-15', 'YYYY-MM-DD'));

INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (7, 4, 4, 'Founder', TO_DATE('2024-06-01', 'YYYY-MM-DD'));

INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (8, 5, 5, 'Founder', TO_DATE('2024-06-20', 'YYYY-MM-DD'));

INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (9, 5, 9, 'Developer', TO_DATE('2024-06-25', 'YYYY-MM-DD'));

INSERT INTO TEAM_MEMBERS (team_id, startup_id, user_id, role_in_team, joined_date)
VALUES (10, 6, 1, 'Advisor', TO_DATE('2024-07-05', 'YYYY-MM-DD'));

-- 4. JOBS (10 records)
INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (1, 1, 'Backend Developer', 'Build REST APIs in Flask', 'open', TO_DATE('2025-03-01', 'YYYY-MM-DD'));

INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (2, 1, 'UI/UX Designer', 'Design product screens', 'open', TO_DATE('2025-03-02', 'YYYY-MM-DD'));

INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (3, 2, 'Data Analyst', 'Analyze transaction trends', 'closed', TO_DATE('2025-02-15', 'YYYY-MM-DD'));

INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (4, 3, 'IoT Engineer', 'Sensor firmware development', 'open', TO_DATE('2025-03-10', 'YYYY-MM-DD'));

INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (5, 4, 'Content Writer', 'Create course material', 'filled', TO_DATE('2025-01-20', 'YYYY-MM-DD'));

INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (6, 5, 'DevOps Engineer', 'Manage cloud deployment', 'open', TO_DATE('2025-03-15', 'YYYY-MM-DD'));

INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (7, 6, 'QA Tester', 'Test hospital inventory module', 'open', TO_DATE('2025-03-18', 'YYYY-MM-DD'));

INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (8, 7, 'Mobile Developer', 'Build Android fitness app', 'open', TO_DATE('2025-03-20', 'YYYY-MM-DD'));

INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (9, 8, 'Product Manager', 'Own the ride-sharing roadmap', 'open', TO_DATE('2025-03-22', 'YYYY-MM-DD'));

INSERT INTO JOBS (job_id, startup_id, title, description, status, posted_date)
VALUES (10, 9, 'Security Engineer', 'Harden payment gateway', 'open', TO_DATE('2025-03-25', 'YYYY-MM-DD'));

-- 5. PROJECTS (10 records)
INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (1, 1, 'Checkout Revamp', 'Redesign checkout flow', TO_DATE('2025-01-01', 'YYYY-MM-DD'), TO_DATE('2025-04-01', 'YYYY-MM-DD'), 'ongoing');

INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (2, 2, 'Ledger Sync', 'Sync ledgers across branches', TO_DATE('2025-01-10', 'YYYY-MM-DD'), TO_DATE('2025-03-10', 'YYYY-MM-DD'), 'completed');

INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (3, 3, 'Field Sensor Rollout', 'Deploy sensors to 50 farms', TO_DATE('2025-02-01', 'YYYY-MM-DD'), NULL, 'ongoing');

INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (4, 4, 'Curriculum Builder', 'Build adaptive lesson engine', TO_DATE('2025-02-15', 'YYYY-MM-DD'), NULL, 'on_hold');

INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (5, 5, 'Grid Dashboard V2', 'Rebuild monitoring dashboard', TO_DATE('2025-03-01', 'YYYY-MM-DD'), NULL, 'ongoing');

INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (6, 6, 'Inventory Audit', 'Full hospital stock audit', TO_DATE('2025-01-05', 'YYYY-MM-DD'), TO_DATE('2025-02-05', 'YYYY-MM-DD'), 'completed');

INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (7, 7, 'Wearable Sync', 'Sync data from fitness bands', TO_DATE('2025-03-05', 'YYYY-MM-DD'), NULL, 'ongoing');

INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (8, 8, 'Route Optimizer', 'ML-based route optimization', TO_DATE('2025-03-10', 'YYYY-MM-DD'), NULL, 'ongoing');

INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (9, 9, 'Gateway Hardening', 'Improve payment security', TO_DATE('2025-03-12', 'YYYY-MM-DD'), NULL, 'ongoing');

INSERT INTO PROJECTS (project_id, startup_id, name, description, start_date, end_date, status)
VALUES (10, 10, 'Marketplace Launch', 'Launch skills marketplace v1', TO_DATE('2024-10-01', 'YYYY-MM-DD'), TO_DATE('2024-12-01', 'YYYY-MM-DD'), 'completed');

-- 6. TASKS (10 records)
INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (1, 1, 'Design checkout wireframes', 'Low-fi wireframes for review', 7, 'done', TO_DATE('2025-01-15', 'YYYY-MM-DD'), 'high');

INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (2, 1, 'Integrate payment gateway', 'Connect PayEase API', 6, 'in_progress', TO_DATE('2025-03-01', 'YYYY-MM-DD'), 'high');

INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (3, 2, 'Reconcile branch ledgers', 'Match ledger entries across branches', 2, 'done', TO_DATE('2025-02-20', 'YYYY-MM-DD'), 'medium');

INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (4, 3, 'Calibrate soil sensors', 'Field calibration for accuracy', 8, 'in_progress', TO_DATE('2025-03-05', 'YYYY-MM-DD'), 'medium');

INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (5, 4, 'Draft grade-5 curriculum', 'Write lesson plans', 4, 'pending', TO_DATE('2025-04-01', 'YYYY-MM-DD'), 'low');

INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (6, 5, 'Rebuild chart module', 'Use new charting library', 9, 'in_progress', TO_DATE('2025-03-20', 'YYYY-MM-DD'), 'medium');

INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (7, 6, 'Count ICU stock', 'Physical stock verification', 1, 'done', TO_DATE('2025-01-20', 'YYYY-MM-DD'), 'high');

INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (8, 7, 'Build BLE sync module', 'Sync wearable device data', 7, 'pending', TO_DATE('2025-04-05', 'YYYY-MM-DD'), 'medium');

INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (9, 8, 'Train ETA model', 'Predict ride ETAs', 8, 'pending', TO_DATE('2025-04-10', 'YYYY-MM-DD'), 'high');

INSERT INTO TASKS (task_id, project_id, title, description, assigned_to, status, due_date, priority)
VALUES (10, 9, 'Pen-test payment API', 'Third-party security review', 9, 'pending', TO_DATE('2025-04-15', 'YYYY-MM-DD'), 'high');

-- 7. FUNDING_ROUNDS (10 records)
INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (1, 1, 'Seed', 500000, 'funded', TO_DATE('2024-05-01', 'YYYY-MM-DD'));

INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (2, 2, 'Seed', 300000, 'funded', TO_DATE('2024-06-01', 'YYYY-MM-DD'));

INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (3, 3, 'Series A', 2000000, 'open', TO_DATE('2025-01-01', 'YYYY-MM-DD'));

INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (4, 4, 'Seed', 250000, 'open', TO_DATE('2025-02-01', 'YYYY-MM-DD'));

INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (5, 5, 'Series A', 1500000, 'funded', TO_DATE('2024-11-01', 'YYYY-MM-DD'));

INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (6, 6, 'Seed', 400000, 'closed', TO_DATE('2024-08-01', 'YYYY-MM-DD'));

INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (7, 7, 'Bridge', 150000, 'open', TO_DATE('2025-03-01', 'YYYY-MM-DD'));

INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (8, 8, 'Seed', 350000, 'open', TO_DATE('2025-03-15', 'YYYY-MM-DD'));

INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (9, 9, 'Series B', 5000000, 'open', TO_DATE('2025-03-20', 'YYYY-MM-DD'));

INSERT INTO FUNDING_ROUNDS (round_id, startup_id, round_type, target_amount, status, round_date)
VALUES (10, 10, 'Seed', 200000, 'funded', TO_DATE('2024-09-01', 'YYYY-MM-DD'));

-- 8. INVESTORS (10 records)
INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (1, 'Rajesh Singhania', 'rajesh@sequoia.mock', '+91-9876543210', 'Peak XV Ventures');

INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (2, 'Anita Agarwal', 'anita@accel.mock', '+91-9876543211', 'Accel Partners');

INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (3, 'Sanjay Mehrotra', 'sanjay@matrix.mock', '+91-9876543212', 'Matrix Partners');

INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (4, 'Deepika Murthy', 'deepika@nexus.mock', '+91-9876543213', 'Nexus Venture Partners');

INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (5, 'Vikram Oberoi', 'vikram@elevation.mock', '+91-9876543214', 'Elevation Capital');

INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (6, 'Pooja Chhabra', 'pooja@blume.mock', '+91-9876543215', 'Blume Ventures');

INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (7, 'Naveen Jindal', 'naveen@lightspeed.mock', '+91-9876543216', 'Lightspeed India');

INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (8, 'Kavita Nair', 'kavita@kalaari.mock', '+91-9876543217', 'Kalaari Capital');

INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (9, 'Arun Jaitley', 'arun@indiainvest.mock', '+91-9876543218', 'India Angel Network');

INSERT INTO INVESTORS (investor_id, name, email, phone, firm_name)
VALUES (10, 'Sunita Goenka', 'sunita@goenkafund.mock', '+91-9876543219', 'Goenka Family Office');

-- 9. INVESTMENTS (10 records)
INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (1, 1, 1, 200000, TO_DATE('2024-05-05', 'YYYY-MM-DD'));

INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (2, 2, 1, 300000, TO_DATE('2024-05-10', 'YYYY-MM-DD'));

INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (3, 3, 2, 300000, TO_DATE('2024-06-05', 'YYYY-MM-DD'));

INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (4, 4, 3, 1200000, TO_DATE('2025-01-10', 'YYYY-MM-DD'));

INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (5, 5, 3, 800000, TO_DATE('2025-01-15', 'YYYY-MM-DD'));

INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (6, 6, 5, 900000, TO_DATE('2024-11-05', 'YYYY-MM-DD'));

INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (7, 7, 5, 600000, TO_DATE('2024-11-10', 'YYYY-MM-DD'));

INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (8, 8, 6, 400000, TO_DATE('2024-08-05', 'YYYY-MM-DD'));

INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (9, 9, 9, 3000000, TO_DATE('2025-03-25', 'YYYY-MM-DD'));

INSERT INTO INVESTMENTS (investment_id, investor_id, round_id, amount, investment_date)
VALUES (10, 10, 10, 200000, TO_DATE('2024-09-05', 'YYYY-MM-DD'));

-- Reset SERIAL sequences to 10 so the next auto-generated ID is 11
SELECT setval('users_user_id_seq', 10);
SELECT setval('startups_startup_id_seq', 10);
SELECT setval('team_members_team_id_seq', 10);
SELECT setval('jobs_job_id_seq', 10);
SELECT setval('projects_project_id_seq', 10);
SELECT setval('tasks_task_id_seq', 10);
SELECT setval('funding_rounds_round_id_seq', 10);
SELECT setval('investors_investor_id_seq', 10);
SELECT setval('investments_investment_id_seq', 10);

-- Commit all inserted records to PostgreSQL database
COMMIT;

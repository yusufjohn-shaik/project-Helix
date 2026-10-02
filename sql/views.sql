-- ====================================================================
-- Project-Helix — Database Views for PostgreSQL
-- Analytical Views for Reporting & Aggregations
-- ====================================================================

-- 1. Startup Ecosystem Summary View
-- Aggregates team size, total funding raised, projects count, and open tasks
CREATE OR REPLACE VIEW vw_startup_summary AS
SELECT 
    s.startup_id,
    s.name AS startup_name,
    s.industry,
    s.status AS startup_status,
    s.founded_date,
    u.name AS founder_name,
    u.email AS founder_email,
    (SELECT COUNT(*) FROM TEAM_MEMBERS tm WHERE tm.startup_id = s.startup_id) AS team_size,
    (SELECT COUNT(*) FROM PROJECTS p WHERE p.startup_id = s.startup_id) AS total_projects,
    (SELECT COUNT(*) 
     FROM TASKS t 
     JOIN PROJECTS p ON t.project_id = p.project_id 
     WHERE p.startup_id = s.startup_id AND t.status NOT IN ('done', 'completed')) AS pending_tasks,
    COALESCE((SELECT SUM(i.amount) 
         FROM INVESTMENTS i 
         JOIN FUNDING_ROUNDS fr ON i.round_id = fr.round_id 
         WHERE fr.startup_id = s.startup_id), 0) AS total_funding_raised
FROM STARTUPS s
JOIN USERS u ON s.created_by = u.user_id;

-- 2. Funding Rounds & Investment Details View
CREATE OR REPLACE VIEW vw_funding_details AS
SELECT 
    fr.round_id,
    s.startup_id,
    s.name AS startup_name,
    fr.round_type,
    fr.target_amount,
    fr.status AS round_status,
    fr.round_date,
    COALESCE(SUM(i.amount), 0) AS total_invested,
    COUNT(i.investment_id) AS investor_count,
    CASE 
        WHEN fr.target_amount > 0 THEN ROUND((COALESCE(SUM(i.amount), 0) / fr.target_amount) * 100, 2)
        ELSE 0 
    END AS funding_percentage
FROM FUNDING_ROUNDS fr
JOIN STARTUPS s ON fr.startup_id = s.startup_id
LEFT JOIN INVESTMENTS i ON fr.round_id = i.round_id
GROUP BY fr.round_id, s.startup_id, s.name, fr.round_type, fr.target_amount, fr.status, fr.round_date;

-- 3. Comprehensive Task & Project Overview View
CREATE OR REPLACE VIEW vw_task_overview AS
SELECT 
    t.task_id,
    t.project_id,
    p.name AS project_name,
    s.startup_id,
    s.name AS startup_name,
    t.title AS task_title,
    t.description AS task_description,
    t.priority,
    t.status AS task_status,
    t.due_date,
    u.user_id AS assignee_id,
    u.name AS assignee_name,
    u.username AS assignee_username
FROM TASKS t
JOIN PROJECTS p ON t.project_id = p.project_id
JOIN STARTUPS s ON p.startup_id = s.startup_id
LEFT JOIN USERS u ON t.assigned_to = u.user_id;

-- 4. Jobs & Recruitment Overview View
CREATE OR REPLACE VIEW vw_jobs_overview AS
SELECT 
    j.job_id,
    j.startup_id,
    s.name AS startup_name,
    s.industry AS startup_industry,
    j.title AS job_title,
    j.description AS job_description,
    j.status AS job_status,
    j.posted_date
FROM JOBS j
JOIN STARTUPS s ON j.startup_id = s.startup_id;

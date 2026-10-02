-- ====================================================================
-- Project-Helix — Performance Indexes for PostgreSQL
-- B-Tree Indexes on Foreign Keys & Frequent Search Columns
-- ====================================================================

-- 1. Indexes on USERS
CREATE INDEX IF NOT EXISTS idx_users_email ON USERS(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON USERS(role);

-- 2. Indexes on STARTUPS
CREATE INDEX IF NOT EXISTS idx_startups_created_by ON STARTUPS(created_by);
CREATE INDEX IF NOT EXISTS idx_startups_status ON STARTUPS(status);
CREATE INDEX IF NOT EXISTS idx_startups_industry ON STARTUPS(industry);

-- 3. Indexes on TEAM_MEMBERS
CREATE INDEX IF NOT EXISTS idx_team_startup_id ON TEAM_MEMBERS(startup_id);
CREATE INDEX IF NOT EXISTS idx_team_user_id ON TEAM_MEMBERS(user_id);

-- 4. Indexes on JOBS
CREATE INDEX IF NOT EXISTS idx_jobs_startup_id ON JOBS(startup_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON JOBS(status);

-- 5. Indexes on PROJECTS
CREATE INDEX IF NOT EXISTS idx_projects_startup_id ON PROJECTS(startup_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON PROJECTS(status);

-- 6. Indexes on TASKS
CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON TASKS(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON TASKS(assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON TASKS(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON TASKS(priority);

-- 7. Indexes on FUNDING_ROUNDS
CREATE INDEX IF NOT EXISTS idx_rounds_startup_id ON FUNDING_ROUNDS(startup_id);
CREATE INDEX IF NOT EXISTS idx_rounds_status ON FUNDING_ROUNDS(status);

-- 8. Indexes on INVESTORS
CREATE INDEX IF NOT EXISTS idx_investors_email ON INVESTORS(email);

-- 9. Indexes on INVESTMENTS
CREATE INDEX IF NOT EXISTS idx_investments_round_id ON INVESTMENTS(round_id);
CREATE INDEX IF NOT EXISTS idx_investments_investor_id ON INVESTMENTS(investor_id);

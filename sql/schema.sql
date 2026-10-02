-- ====================================================================
-- Project-Helix — 9-Table Database Schema (3NF)
-- Designed for PostgreSQL & College Viva Defense
-- Student: Shaik Yusuf John (25B11CS893)
-- ====================================================================

-- Step 1: Drop tables in reverse dependency order if they already exist
DROP TABLE IF EXISTS INVESTMENTS CASCADE;
DROP TABLE IF EXISTS INVESTORS CASCADE;
DROP TABLE IF EXISTS FUNDING_ROUNDS CASCADE;
DROP TABLE IF EXISTS TASKS CASCADE;
DROP TABLE IF EXISTS PROJECTS CASCADE;
DROP TABLE IF EXISTS JOBS CASCADE;
DROP TABLE IF EXISTS TEAM_MEMBERS CASCADE;
DROP TABLE IF EXISTS STARTUPS CASCADE;
DROP TABLE IF EXISTS USERS CASCADE;

-- ====================================================================
-- Step 2: Create Tables with Constraints (Foreign Key Order)
-- ====================================================================

-- 1. USERS (Strong Entity)
-- Stores account details for founders, team members, investors, and admins
CREATE TABLE USERS (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'member' CHECK (role IN ('founder', 'member', 'admin', 'investor')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. STARTUPS (Strong Entity)
-- Stores registered startup ventures created by a user (founder)
CREATE TABLE STARTUPS (
    startup_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(1000),
    industry VARCHAR(50),
    founded_date DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'planning', 'closed', 'archived')),
    created_by INTEGER NOT NULL,
    CONSTRAINT fk_startups_user FOREIGN KEY (created_by) REFERENCES USERS(user_id) ON DELETE CASCADE
);

-- 3. TEAM_MEMBERS (Associative Entity)
-- Resolves Many-to-Many relationship between USERS and STARTUPS
CREATE TABLE TEAM_MEMBERS (
    team_id SERIAL PRIMARY KEY,
    startup_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role_in_team VARCHAR(50),
    joined_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_team_startup FOREIGN KEY (startup_id) REFERENCES STARTUPS(startup_id) ON DELETE CASCADE,
    CONSTRAINT fk_team_user FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
);

-- 4. JOBS (Strong Entity)
-- Stores open job postings for a startup
CREATE TABLE JOBS (
    job_id SERIAL PRIMARY KEY,
    startup_id INTEGER NOT NULL,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(1000),
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'closed', 'filled')),
    posted_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_jobs_startup FOREIGN KEY (startup_id) REFERENCES STARTUPS(startup_id) ON DELETE CASCADE
);

-- 5. PROJECTS (Strong Entity)
-- Stores development projects and milestones initiated by a startup
CREATE TABLE PROJECTS (
    project_id SERIAL PRIMARY KEY,
    startup_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(1000),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'ongoing' CHECK (status IN ('ongoing', 'completed', 'on_hold')),
    CONSTRAINT fk_projects_startup FOREIGN KEY (startup_id) REFERENCES STARTUPS(startup_id) ON DELETE CASCADE
);

-- 6. TASKS (Strong Entity)
-- Stores actionable tasks within a project; optionally assigned to a user
CREATE TABLE TASKS (
    task_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(1000),
    assigned_to INTEGER,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'done', 'todo', 'completed')),
    due_date DATE,
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    CONSTRAINT fk_tasks_project FOREIGN KEY (project_id) REFERENCES PROJECTS(project_id) ON DELETE CASCADE,
    CONSTRAINT fk_tasks_user FOREIGN KEY (assigned_to) REFERENCES USERS(user_id) ON DELETE SET NULL
);

-- 7. FUNDING_ROUNDS (Strong Entity)
-- Stores fundraising rounds (Seed, Series A, etc.) raised by startups
CREATE TABLE FUNDING_ROUNDS (
    round_id SERIAL PRIMARY KEY,
    startup_id INTEGER NOT NULL,
    round_type VARCHAR(30) NOT NULL,
    target_amount NUMERIC(12,2) NOT NULL CHECK (target_amount >= 0),
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'funded', 'closed')),
    round_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_rounds_startup FOREIGN KEY (startup_id) REFERENCES STARTUPS(startup_id) ON DELETE CASCADE
);

-- 8. INVESTORS (Strong Entity)
-- Stores profiles of venture funds and individual investors
CREATE TABLE INVESTORS (
    investor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    firm_name VARCHAR(100)
);

-- 9. INVESTMENTS (Associative Entity)
-- Resolves Many-to-Many relationship between INVESTORS and FUNDING_ROUNDS
CREATE TABLE INVESTMENTS (
    investment_id SERIAL PRIMARY KEY,
    investor_id INTEGER NOT NULL,
    round_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
    investment_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_investments_investor FOREIGN KEY (investor_id) REFERENCES INVESTORS(investor_id) ON DELETE CASCADE,
    CONSTRAINT fk_investments_round FOREIGN KEY (round_id) REFERENCES FUNDING_ROUNDS(round_id) ON DELETE CASCADE
);
    k
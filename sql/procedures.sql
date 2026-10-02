-- ====================================================================
-- Project-Helix — Stored Procedures for PostgreSQL
-- Stored Procedures for Lifecycle Updates
-- ====================================================================

-- 1. Procedure to close a funding round
CREATE OR REPLACE PROCEDURE close_funding_round(
    p_round_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE FUNDING_ROUNDS
    SET status = 'closed'
    WHERE round_id = p_round_id;
END;
$$;

-- 2. Procedure to archive/close a startup (cascading operational updates)
CREATE OR REPLACE PROCEDURE archive_startup(
    p_startup_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Mark startup as closed
    UPDATE STARTUPS
    SET status = 'closed'
    WHERE startup_id = p_startup_id;

    -- Close open jobs
    UPDATE JOBS
    SET status = 'closed'
    WHERE startup_id = p_startup_id;

    -- Put ongoing projects on hold
    UPDATE PROJECTS
    SET status = 'on_hold'
    WHERE startup_id = p_startup_id;
END;
$$;

-- 3. Procedure to mark a task as completed
CREATE OR REPLACE PROCEDURE complete_task(
    p_task_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE TASKS
    SET status = 'done'
    WHERE task_id = p_task_id;
END;
$$;

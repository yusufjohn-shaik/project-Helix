-- ====================================================================
-- Project-Helix — Database Triggers for PostgreSQL
-- Business Logic & Integrity Constraints
-- ====================================================================

-- 1. Trigger: Automatically add Founder to TEAM_MEMBERS when a STARTUP is registered
CREATE OR REPLACE FUNCTION trg_add_founder_to_team()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM TEAM_MEMBERS 
        WHERE startup_id = NEW.startup_id AND user_id = NEW.created_by
    ) THEN
        INSERT INTO TEAM_MEMBERS (startup_id, user_id, role_in_team, joined_date)
        VALUES (NEW.startup_id, NEW.created_by, 'Founder', CURRENT_DATE);
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_startup_founder_ai ON STARTUPS;
CREATE TRIGGER trg_startup_founder_ai
AFTER INSERT ON STARTUPS
FOR EACH ROW
EXECUTE FUNCTION trg_add_founder_to_team();

-- 2. Trigger: Automatically update Funding Round status to 'funded' when target is reached
CREATE OR REPLACE FUNCTION trg_update_funding_status()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC(12,2);
    v_target NUMERIC(12,2);
BEGIN
    SELECT COALESCE(SUM(amount), 0) INTO v_total
    FROM INVESTMENTS
    WHERE round_id = NEW.round_id;

    SELECT target_amount INTO v_target
    FROM FUNDING_ROUNDS
    WHERE round_id = NEW.round_id;

    IF v_total >= v_target AND v_target > 0 THEN
        UPDATE FUNDING_ROUNDS
        SET status = 'funded'
        WHERE round_id = NEW.round_id;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_investment_status_ai ON INVESTMENTS;
CREATE TRIGGER trg_investment_status_ai
AFTER INSERT ON INVESTMENTS
FOR EACH ROW
EXECUTE FUNCTION trg_update_funding_status();

-- 3. Trigger: Validate project start_date and end_date
CREATE OR REPLACE FUNCTION trg_validate_project_dates()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.end_date IS NOT NULL AND NEW.start_date IS NOT NULL THEN
        IF NEW.end_date < NEW.start_date THEN
            RAISE EXCEPTION 'Project end_date (%) cannot be earlier than start_date (%)', NEW.end_date, NEW.start_date;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_project_dates_bi ON PROJECTS;
CREATE TRIGGER trg_project_dates_bi
BEFORE INSERT OR UPDATE ON PROJECTS
FOR EACH ROW
EXECUTE FUNCTION trg_validate_project_dates();

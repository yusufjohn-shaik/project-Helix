import os
import sys
import subprocess
import argparse

# 20-Phase progressive rollout mapping for 9-Table Database Architecture
# Matching Project_Helix_DBMS_25B11CS893.pptx
PHASES = {
    1: {
        "title": "Day 1: Project Initialization & Configuration",
        "files": [".gitignore", ".env.example", "requirements.txt", "README.md", "app.py"],
        "message": "feat: initialize Project-Helix repository and core configuration"
    },
    2: {
        "title": "Day 2: PostgreSQL Database Connection",
        "files": ["config.py", "database/connection.py", "database/__init__.py"],
        "message": "feat: setup PostgreSQL database connection and environment config"
    },
    3: {
        "title": "Day 3: Reusable Database Query Helpers",
        "files": ["database/queries.py", "database/helpers.py", "database/init_db.py"],
        "message": "feat: implement reusable database query execution helpers"
    },
    4: {
        "title": "Day 4: SQL Database Schema (9 Tables in 3NF)",
        "files": ["sql/schema.sql"],
        "message": "docs(sql): add 9-table 3NF relational database schema"
    },
    5: {
        "title": "Day 5: SQL Sequences & Auto-increment Triggers",
        "files": ["sql/triggers.sql"],
        "message": "feat(sql): implement sequence auto-increment triggers for 9 tables"
    },
    6: {
        "title": "Day 6: SQL Views, Procedures & Performance Indexes",
        "files": ["sql/procedures.sql", "sql/views.sql", "sql/indexes.sql"],
        "message": "feat(sql): add database views, stored procedures, and performance indexes"
    },
    7: {
        "title": "Day 7: SQL Database Seed Data",
        "files": ["sql/sample_data.sql"],
        "message": "seed(sql): populate 10 sample records per table from presentation slides"
    },
    8: {
        "title": "Day 8: User Model & Authentication Service",
        "files": ["models/user.py", "services/authentication_service.py"],
        "message": "feat(auth): implement User data model and AuthenticationService"
    },
    9: {
        "title": "Day 9: Authentication Routes & Templates",
        "files": ["routes/auth.py", "templates/auth/login.html", "templates/auth/register.html", "templates/auth/profile.html", "templates/auth/change_password.html"],
        "message": "feat(auth): add login, registration, and user profile views"
    },
    10: {
        "title": "Day 10: Core UI Layout, Navigation & Styling",
        "files": ["templates/base.html", "templates/dashboard.html", "static/css/base.css", "static/js/main.js"],
        "message": "feat(ui): implement main application layout, design system, and navigation"
    },
    11: {
        "title": "Day 11: Startup Management Service & Routes",
        "files": ["models/startup.py", "services/startup_service.py", "routes/startup.py"],
        "message": "feat(startup): implement Startup and TeamMember models and routes"
    },
    12: {
        "title": "Day 12: Startup UI Templates & Team Management",
        "files": ["templates/startup/list.html", "templates/startup/create.html", "templates/startup/detail.html", "templates/startup/edit.html", "routes/team.py", "templates/team/list.html", "templates/team/add_member.html"],
        "message": "feat(startup): add startup directory, team member allocation views"
    },
    13: {
        "title": "Day 13: Project & Task Services",
        "files": ["models/tasks.py", "services/task_service.py", "routes/tasks.py"],
        "message": "feat(task): implement Project and Task models and services"
    },
    14: {
        "title": "Day 14: Project & Task Management Templates",
        "files": ["templates/tasks/projects_list.html", "templates/tasks/project_create.html", "templates/tasks/project_detail.html", "templates/tasks/tasks_list.html", "templates/tasks/task_create.html", "templates/tasks/task_edit.html"],
        "message": "feat(task): add task creation, status tracking, and project detail UI"
    },
    15: {
        "title": "Day 15: Job Board Models, Services & Routes",
        "files": ["models/job.py", "models/hiring.py", "services/job_service.py", "services/hiring_service.py", "routes/hiring.py"],
        "message": "feat(jobs): implement Job model, JobService, and hiring routes"
    },
    16: {
        "title": "Day 16: Job Board UI Templates",
        "files": ["templates/hiring/jobs_list.html", "templates/hiring/job_create.html", "templates/hiring/job_detail.html"],
        "message": "feat(jobs): add job vacancy listings, creation, and detail views"
    },
    17: {
        "title": "Day 17: Funding & Investor Models & Services",
        "files": ["models/funding.py", "services/funding_service.py", "routes/funding.py"],
        "message": "feat(funding): implement Investor, FundingRound, and Investment services"
    },
    18: {
        "title": "Day 18: Funding UI & Investment Round Views",
        "files": ["templates/funding/investors_list.html", "templates/funding/investor_create.html", "templates/funding/rounds_list.html", "templates/funding/round_create.html", "templates/funding/round_detail.html"],
        "message": "feat(funding): add funding rounds and investor management templates"
    },
    19: {
        "title": "Day 19: Reports & Analytics Views Integration",
        "files": ["services/report_service.py", "routes/reports.py", "templates/reports/dashboard.html", "templates/reports/funding.html", "templates/reports/hiring.html", "templates/reports/revenue.html", "templates/reports/tasks.html"],
        "message": "feat(reports): implement database view reporting dashboards and charts"
    },
    20: {
        "title": "Day 20: System Documentation & ER Diagrams",
        "files": ["docs/ER_Diagram.md", "docs/SRS.md", "docs/README.md"],
        "message": "docs: add 9-table ER diagrams, participation constraints, and project documentation"
    }
}

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
    return result.returncode == 0

def execute_phase(day):
    if day not in PHASES:
        print(f"Invalid day: {day}. Must be between 1 and 20.")
        return

    phase = PHASES[day]
    print(f"\n==========================================")
    print(f"[ROLLOUT] Executing {phase['title']}")
    print(f"==========================================")

    # Git add files for this phase
    for file_path in phase['files']:
        if os.path.exists(file_path):
            run_cmd(["git", "add", file_path])
        else:
            print(f"Warning: File {file_path} does not exist, skipping.")

    # Git commit
    commit_success = run_cmd(["git", "commit", "-m", phase['message']])
    
    if commit_success:
        print(f"\n[SUCCESS] Day {day} committed successfully!")
        print(f"To push to GitHub, run:")
        print(f"  git push -u origin master (or main)\n")
    else:
        print(f"\n[NOTICE] Nothing new to commit or already committed for Day {day}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="20-Day Staged Git Commit Rollout for Project-Helix (9-Table Architecture)")
    parser.add_argument("--day", type=int, help="Day phase to commit (1 to 20)")
    args = parser.parse_args()

    if args.day:
        execute_phase(args.day)
    else:
        print("Usage: python rollout.py --day <1-20>")
        print("\nAvailable Phases:")
        for d, p in PHASES.items():
            print(f"  Day {d:2d}: {p['title']}")

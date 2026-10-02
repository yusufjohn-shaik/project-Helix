# Project-Helix — End-to-End Request-Response Architecture Flowchart

This document details the exact end-to-end lifecycle of a web request in **Project-Helix**—from the moment a user clicks an action in the browser, down to the database execution, and back up to the rendered user interface.

![Request-Response Architecture Diagram](request_flow_diagram.jpg)

---

## 1. High-Level System Flowchart

```mermaid
flowchart TD
    subgraph Client ["1. Client (Web Browser)"]
        UI["User submits Form (e.g. Create Task)"]
        HTTP_REQ["Sends HTTP POST Request with Form Data"]
        RENDER["Browser Renders Updated HTML Webpage"]
    end

    subgraph Presentation ["2. Presentation Layer (Flask Routes)"]
        ROUTE["Blueprint Route: @tasks_bp.route('/create')"]
        AUTH_CHECK{"Session Authenticated?"}
        PARSE["Extract & Validate Form Inputs"]
    end

    subgraph Business ["3. Business Logic Layer (Services)"]
        SERVICE["TaskService.create_task(...)"]
        SQL_BUILD["Construct SQL Statement & Bind Parameters"]
    end

    subgraph DataAccess ["4. Data Access Layer (database/)"]
        QUERIES["database/queries.py: run_query()"]
        PARAM_BIND["Bind Parameters (:param / %(param)s)"]
        CONN_MGR["database/connection.py: get_db_connection()"]
    end

    subgraph DatabaseEngine ["5. Relational Database Engine"]
        SQL_EXEC["Execute SQL on Table"]
        CONSTRAINTS{"Check Constraints & FKs"}
        TRIG_SEQ["Trigger / Sequence Auto-Assigns Primary Key"]
        COMMIT["Commit Transaction to Disk (ACID Durability)"]
    end

    %% Forward Request Flow
    UI --> HTTP_REQ
    HTTP_REQ --> ROUTE
    ROUTE --> AUTH_CHECK
    AUTH_CHECK -- Yes --> PARSE
    AUTH_CHECK -- No --> LOGIN_REDIRECT["Redirect to Login Page"]
    PARSE --> SERVICE
    SERVICE --> SQL_BUILD
    SQL_BUILD --> QUERIES
    QUERIES --> CONN_MGR
    CONN_MGR --> PARAM_BIND
    PARAM_BIND --> SQL_EXEC
    SQL_EXEC --> CONSTRAINTS
    CONSTRAINTS -- Valid --> TRIG_SEQ
    TRIG_SEQ --> COMMIT

    %% Return Response Flow
    COMMIT --> DB_OK["Return Success / Row ID"]
    DB_OK --> SERVICE_RET["Service returns True"]
    SERVICE_RET --> FLASH["Flash Success Message"]
    FLASH --> REDIRECT["HTTP 302 Redirect to Project Detail"]
    REDIRECT --> HTTP_RESP["HTTP Response (HTML + CSS)"]
    HTTP_RESP --> RENDER
```

---

## 2. Sequence Diagram (Step-by-Step Timeline)

```mermaid
sequenceDiagram
    autonumber
    actor User as User (Browser)
    participant Route as Flask Route (routes/tasks.py)
    participant Service as Service Layer (services/task_service.py)
    participant DBQuery as Query Layer (database/queries.py)
    participant DB as Relational Database

    User->>Route: 1. Click "Create Task" (HTTP POST /tasks/create)
    Note over Route: Checks session['user_id']<br/>Extracts title, priority, project_id
    Route->>Service: 2. TaskService.create_task(project_id, title, priority...)
    Note over Service: Prepares parameterized SQL query
    Service->>DBQuery: 3. run_query(sql, params)
    Note over DBQuery: Binds parameters to prevent SQL Injection
    DBQuery->>DB: 4. Execute INSERT INTO TASKS (...)
    Note over DB: Validates FKs (project_id, assigned_to)<br/>Assigns primary key (Auto-increment)<br/>Commits transaction
    DB-->>DBQuery: 5. Query execution OK (commit successful)
    DBQuery-->>Service: 6. Returns execution status
    Service-->>Route: 7. Returns True (success)
    Note over Route: Adds flash message: "Task created!"<br/>Generates HTTP 302 Redirect to /tasks/projects/{id}
    Route-->>User: 8. Browser receives 302 -> GET /projects/{id}
    Route-->>User: 9. Returns rendered project_detail.html with new task visible!
```

---

## 3. Real-World Walkthrough (Example: "Creating a Task")

| Step | Component | What Happens Under the Hood |
|---|---|---|
| **1. User Action** | **Browser (Client)** | User fills the form on `task_create.html` (e.g. Title: *"Build Connection Pool"*, Project ID: `1`, Priority: `'High'`) and clicks the **Create Task** button. |
| **2. HTTP Transmission** | **Network** | The browser sends an `HTTP POST` request to `http://localhost:5000/tasks/create` with the form payload in the request body. |
| **3. Controller Handling** | **Flask Route (`routes/tasks.py`)** | The `@tasks_bp.route('/create', methods=['POST'])` function intercepts the request: <br>• Checks `session['user_id']` (redirects to login if unauthenticated). <br>• Extracts `request.form.get('title')`, `project_id`, `priority`. |
| **4. Service Execution** | **Service Layer (`services/task_service.py`)** | Calls `TaskService.create_task(...)`. The service prepares an `INSERT INTO TASKS` statement with clean bind parameters: `{"project_id": 1, "title": "Build Connection Pool", "priority": "high"}`. |
| **5. Parameter Binding** | **Database Layer (`database/queries.py`)** | The `run_query()` function opens a connection using `get_db_connection()` and sends the SQL and bind dictionary separately. **SQL Injection is prevented** because user input is never concatenated into raw SQL strings. |
| **6. Database Engine** | **Database (RDBMS)** | The database server executes the command: <br>• **Integrity Check:** Confirms `project_id = 1` exists in table `PROJECTS`. <br>• **Domain Check:** Verifies `priority IN ('low', 'medium', 'high')`. <br>• **Primary Key Generation:** Assigns the next unique ID from the sequence (e.g. `task_id = 11`). <br>• **Commit:** Writes data changes permanently to disk according to ACID properties. |
| **7. Return Flow** | **Python & Flask** | The database returns confirmation $\rightarrow$ `run_query()` returns $\rightarrow$ `TaskService` returns `True` $\rightarrow$ Flask adds a notification: `flash('Task created!', 'success')`. |
| **8. UI Update** | **Browser (Client)** | Flask sends an `HTTP 302 Redirect` to `project_detail`. The browser automatically requests the updated page, and Jinja2 renders the table showing the new task with its assigned ID and status badge. |

---

## 4. How to Explain This in Viva (10-Second Summary)

> *"Sir, Project-Helix follows an industry-standard **Layered MVC Architecture**:*  
> *When a user interacts with the HTML frontend, the browser dispatches an HTTP request to our **Flask Route Controllers**. The Controller verifies user authentication and delegates the request to the **Service Layer** for business validation.*  
> *The Service layer invokes our **Database Query Layer**, which binds inputs safely to prevent SQL injection and executes the query against our relational database.*  
> *The database engine enforces foreign key constraints and triggers, permanently commits the transaction, and returns the result back through the pipeline so Jinja2 can render the updated web page for the user."*

# 📝 Notes API — Project Context

## 🚀 Project Overview
The **Notes API** is a RESTful service built with **FastAPI** designed to manage personal notes. It implements a private-by-default architecture where users can create, categorize, and track the lifecycle of their notes.

### Key Features:
- **User Isolation**: Every user owns and manages their own data; no cross-user access.
- **Note Lifecycle**: Notes transition through `todo`, `done`, and `archived` states.
- **Tagging**: Flexible organization using user-specific tags.
- **Search & Filtering**: Retrieve notes by status, tags, or keyword search.
- **Soft Delete**: Notes are hidden from users upon deletion but retained internally.

### 🛠 Tech Stack
- **Framework**: FastAPI (Python 3.13+)
- **Dependency Management**: `uv`
- **Database**: PostgreSQL (using `psycopg2` for synchronous repository access)
- **Dependency Injection**: `python-dependency-injector`
- **Validation & Settings**: `pydantic` and `pydantic-settings`
- **Logging**: `loguru`

---

## 🏗 Architecture & Design
The project follows a layered architecture to ensure separation of concerns:

1.  **Routers (`app/routers/`)**: Handle HTTP requests and define API endpoints.
2.  **Services (`app/services/`)**: Contain business logic and orchestrate domain behaviors.
3.  **Repositories (`app/repositories/`)**: Abstract data access and handle SQL queries.
4.  **Core (`app/core/`)**: Configuration, Dependency Injection container, and base models.
5.  **DB (`app/db/`)**: Database connection pooling management.

---

## ⚙️ Building and Running

### Prerequisites
- Python 3.13 or higher.
- [uv](https://github.com/astral-sh/uv) installed.
- A running PostgreSQL instance.

### Setup
1.  **Install dependencies**:
    ```bash
    uv sync
    ```
2.  **Environment Configuration**:
    Create a `.env` file in the root directory:
    ```env
    POSTGRES_URL=postgresql://user:password@localhost:5432/notes_db
    ```
3.  **Initialize Database**:
    Apply the schema found in `app/scripts/schema.sql` to your PostgreSQL database.

### Running the Application
Start the development server with hot-reload enabled:
```bash
uv run python -m app.main
```
The API will be available at `http://localhost:8000`.

### Testing
- **TODO**: Automated tests are currently not implemented in the codebase.

---

## ✍️ Development Conventions

### Coding Style
- **Type Hinting**: Mandatory for all function signatures and complex variables.
- **Dependency Injection**: Use the `Container` in `app/core/container.py` for managing dependencies. Avoid manual instantiation of services/repositories in routers.
- **SQL**: Use raw SQL within repository classes for data access. Ensure all user-provided values are properly parameterized to prevent SQL injection.

### Project Structure
- `app/core/models.py`: Pydantic models for request/response bodies.
- `app/scripts/schema.sql`: Source of truth for the database schema.
- `docs/notes_app_core_domain_specification.md`: Detailed business logic and domain rules.

### Note Statuses
Always use the following literal strings for note statuses:
- `todo` (Default)
- `done`
- `archived`

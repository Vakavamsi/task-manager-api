# Task Manager API

A backend Task Manager API built with **FastAPI**, **PostgreSQL**, **Raw SQL**, **Docker**, and **Groq AI**.

The API provides complete task management functionality along with AI-powered task description generation and summarization.

## Features

- Create, read, update, and delete tasks
- PostgreSQL database
- Raw SQL queries using `psycopg2`
- Pydantic request validation
- Pagination using `limit` and `offset`
- Filter tasks by status
- AI-generated task descriptions using Groq
- AI-powered task summarization
- Retry logic for AI API failures
- Health check endpoint
- Proper HTTP error handling
- Docker and Docker Compose support
- Environment-based configuration

## Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL 18
- psycopg2
- Pydantic
- Groq API
- Docker
- Docker Compose
- Uvicorn

## Project Structure

```text
task-manager-api/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── groq_service.py
│   ├── main.py
│   └── schemas.py
│
├── database/
│   └── init.sql
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Database Model

The application uses a `tasks` table with the following fields:

| Field | Type | Description |
|---|---|---|
| `id` | SERIAL | Primary key |
| `title` | TEXT | Task title |
| `description` | TEXT | Task description |
| `status` | TEXT | `pending`, `in_progress`, or `completed` |
| `created_at` | TIMESTAMP | Task creation time |
| `updated_at` | TIMESTAMP | Last modification time |

## API Endpoints

### Create Task

```http
POST /tasks
```

Example request:

```json
{
  "title": "Build login API",
  "description": "Create a secure login API.",
  "status": "pending"
}
```

### Get Tasks

```http
GET /tasks
```

Supports pagination:

```http
GET /tasks?limit=10&offset=0
```

Supports status filtering:

```http
GET /tasks?status=completed
```

Supported statuses:

- `pending`
- `in_progress`
- `completed`

### Get Task

```http
GET /tasks/{task_id}
```

### Update Task

```http
PUT /tasks/{task_id}
```

Example:

```json
{
  "status": "completed"
}
```

### Delete Task

```http
DELETE /tasks/{task_id}
```

### Generate Task Description

```http
POST /tasks/{task_id}/generate-description
```

This endpoint sends the task title to Groq AI and generates a description.

### Summarize Task

```http
POST /tasks/{task_id}/summarize
```

This endpoint generates a short summary from the task description.

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

## Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=task_manager
DB_USER=postgres
DB_PASSWORD=your_postgres_password
GROQ_API_KEY=your_groq_api_key
```

Do not commit `.env` to GitHub.

## Running with Docker

Make sure Docker Desktop is running.

### Build the application

```bash
docker compose build
```

### Start the services

```bash
docker compose up -d
```

### Check running containers

```bash
docker compose ps
```

The API will be available at:

```text
http://localhost:8000
```

## Swagger API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

You can test all API endpoints directly from Swagger UI.

## Stop the Application

```bash
docker compose down
```

To remove the database volume as well:

```bash
docker compose down -v
```

## Error Handling

The API handles common errors including:

- `200` — Successful request
- `201` — Successful task creation
- `400` — Invalid request
- `404` — Task not found
- `422` — Validation error
- `500` — Server or AI service error

## AI Integration

Groq is used for:

- Generating task descriptions from task titles
- Generating short summaries from task descriptions
- Retrying failed AI requests up to three attempts

## Security

- Database credentials are stored in environment variables.
- Groq API credentials are stored in environment variables.
- `.env` is excluded through `.gitignore`.
- `.env` is excluded from the Docker build using `.dockerignore`.
- API keys and passwords are not hardcoded in the source code.

## Author

**Vaka Vamsi**

GitHub: https://github.com/Vakavamsi
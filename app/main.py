from fastapi import FastAPI, HTTPException

from .database import get_db_connection
from .schemas import TaskCreate, TaskUpdate, TaskStatus
from .groq_service import generate_task_description, generate_task_summary

app = FastAPI(title="Task Manager API")


@app.get("/")
def root():
    return {"message": "Task Manager API is running"}


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO tasks (title, description, status)
            VALUES (%s, %s, %s)
            RETURNING id, title, description, status, created_at, updated_at;
        """

        cursor.execute(
            query,
            (task.title, task.description, task.status)
        )

        created_task = cursor.fetchone()

        connection.commit()

        return {
            "id": created_task[0],
            "title": created_task[1],
            "description": created_task[2],
            "status": created_task[3],
            "created_at": created_task[4],
            "updated_at": created_task[5]
        }

    except Exception:
        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to create task"
        )

    finally:
        cursor.close()
        connection.close()


@app.get("/tasks")
def get_tasks(
    limit: int = 10,
    offset: int = 0,
    status: TaskStatus | None = None
):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        if status:
            query = """
                SELECT id, title, description, status, created_at, updated_at
                FROM tasks
                WHERE status = %s
                ORDER BY id
                LIMIT %s OFFSET %s;
            """

            cursor.execute(
                query,
                (status, limit, offset)
            )

        else:
            query = """
                SELECT id, title, description, status, created_at, updated_at
                FROM tasks
                ORDER BY id
                LIMIT %s OFFSET %s;
            """

            cursor.execute(
                query,
                (limit, offset)
            )

        tasks = cursor.fetchall()

        result = []

        for task in tasks:
            result.append({
                "id": task[0],
                "title": task[1],
                "description": task[2],
                "status": task[3],
                "created_at": task[4],
                "updated_at": task[5]
            })

        return result

    finally:
        cursor.close()
        connection.close()
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        query = """
            DELETE FROM tasks
            WHERE id = %s
            RETURNING id;
        """

        cursor.execute(query, (task_id,))

        deleted_task = cursor.fetchone()

        if deleted_task is None:
            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        connection.commit()

        return {
            "message": "Task deleted successfully",
            "id": deleted_task[0]
        }

    except HTTPException:
        raise

    except Exception:
        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete task"
        )

    finally:
        cursor.close()
        connection.close()
@app.post("/tasks/{task_id}/generate-description")
def generate_description(task_id: int):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        # Get the task
        cursor.execute(
            "SELECT id, title FROM tasks WHERE id = %s;",
            (task_id,)
        )

        task = cursor.fetchone()

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        # Generate description using Groq
        description = generate_task_description(task[1])

        # Save generated description
        cursor.execute(
            """
            UPDATE tasks
            SET description = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, title, description, status, created_at, updated_at;
            """,
            (description, task_id)
        )

        updated_task = cursor.fetchone()

        connection.commit()

        return {
            "id": updated_task[0],
            "title": updated_task[1],
            "description": updated_task[2],
            "status": updated_task[3],
            "created_at": updated_task[4],
            "updated_at": updated_task[5]
        }

    except HTTPException:
        raise

    except Exception as error:
        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate description: {str(error)}"
        )

    finally:
        cursor.close()
        connection.close()
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
@app.post("/tasks/{task_id}/summarize")
def summarize_task(task_id: int):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, title, description
            FROM tasks
            WHERE id = %s;
            """,
            (task_id,)
        )

        task = cursor.fetchone()

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        if not task[2]:
            raise HTTPException(
                status_code=400,
                detail="Task description is empty"
            )

        summary = generate_task_summary(task[2])

        return {
            "id": task[0],
            "title": task[1],
            "summary": summary
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {str(error)}"
        )

    finally:
        cursor.close()
        connection.close()
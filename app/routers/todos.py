from fastapi import APIRouter, HTTPException
from app.models import TodoCreate, TodoResponse
from app.services.todo_service import TodoService
from app.repositories.todo_repository import TodoRepository


# Initialize repository and service
repository = TodoRepository()
service = TodoService(repository)

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate) -> TodoResponse:
    """Create a new todo."""
    try:
        created_todo = service.create_todo(
            title=todo.title,
            description=todo.description
        )
        return TodoResponse(
            id=created_todo.id,
            title=created_todo.title,
            description=created_todo.description,
            completed=created_todo.completed,
            created_at=created_todo.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int) -> TodoResponse:
    """Get a todo by ID."""
    todo = service.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=todo.created_at
    )


@router.get("", response_model=list[TodoResponse])
def get_all_todos() -> list[TodoResponse]:
    """Get all todos."""
    todos = service.get_all_todos()
    return [
        TodoResponse(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at
        )
        for todo in todos
    ]


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate) -> TodoResponse:
    """Update a todo."""
    updated_todo = service.update_todo(
        todo_id=todo_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse(
        id=updated_todo.id,
        title=updated_todo.title,
        description=updated_todo.description,
        completed=updated_todo.completed,
        created_at=updated_todo.created_at
    )


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    """Delete a todo."""
    success = service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")

from typing import Optional
from app.repositories.todo_repository import TodoRepository, Todo, Priority


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def create_todo(self, title: str, description: Optional[str] = None, priority: Optional[Priority] = None) -> Todo:
        """Create a new todo."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if priority is None:
            priority = Priority.MEDIUM
        return self.repository.create(title=title.strip(), description=description, priority=priority)

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Get a todo by ID."""
        return self.repository.get_by_id(todo_id)

    def get_all_todos(self) -> list[Todo]:
        """Get all todos."""
        return self.repository.get_all()

    def update_todo(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None, priority: Optional[Priority] = None) -> Optional[Todo]:
        """Update a todo."""
        return self.repository.update(todo_id, title, description, completed, priority)

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo."""
        return self.repository.delete(todo_id)

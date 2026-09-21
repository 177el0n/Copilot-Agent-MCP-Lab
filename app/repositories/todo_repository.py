from datetime import datetime
from typing import Optional


class Todo:
    def __init__(
        self,
        id: int,
        title: str,
        description: Optional[str] = None,
        completed: bool = False,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now()


class TodoRepository:
    def __init__(self):
        self._todos: dict[int, Todo] = {}
        self._next_id = 1

    def create(self, title: str, description: Optional[str] = None, completed: bool = False) -> Todo:
        """Create a new todo and save it."""
        todo = Todo(
            id=self._next_id,
            title=title,
            description=description,
            completed=completed
        )
        self._todos[self._next_id] = todo
        self._next_id += 1
        return todo

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get a todo by ID."""
        return self._todos.get(todo_id)

    def get_all(self) -> list[Todo]:
        """Get all todos."""
        return list(self._todos.values())

    def update(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Todo]:
        """Update a todo."""
        todo = self._todos.get(todo_id)
        if todo is None:
            return None
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if completed is not None:
            todo.completed = completed
        return todo

    def delete(self, todo_id: int) -> bool:
        """Delete a todo."""
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

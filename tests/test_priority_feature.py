"""Tests for the priority feature."""

import pytest
from app.repositories.todo_repository import TodoRepository, Todo, Priority
from app.services.todo_service import TodoService
from app.models import TodoCreate, TodoResponse


class TestPriorityRepository:
    """Test priority feature in TodoRepository."""

    def test_create_todo_with_default_priority(self):
        """Test that unspecified priority defaults to 'medium'."""
        repo = TodoRepository()
        todo = repo.create(title="Test Todo", description="Test")
        assert todo.priority == Priority.MEDIUM

    def test_create_todo_with_high_priority(self):
        """Test creating a todo with high priority."""
        repo = TodoRepository()
        todo = repo.create(title="Urgent", priority=Priority.HIGH)
        assert todo.priority == Priority.HIGH

    def test_create_todo_with_low_priority(self):
        """Test creating a todo with low priority."""
        repo = TodoRepository()
        todo = repo.create(title="Low priority", priority=Priority.LOW)
        assert todo.priority == Priority.LOW

    def test_update_todo_priority(self):
        """Test updating a todo's priority."""
        repo = TodoRepository()
        todo = repo.create(title="Test", priority=Priority.MEDIUM)
        updated = repo.update(todo.id, priority=Priority.HIGH)
        assert updated.priority == Priority.HIGH

    def test_priority_persists_after_update(self):
        """Test that priority is preserved with other updates."""
        repo = TodoRepository()
        todo = repo.create(title="Test", description="Original", priority=Priority.HIGH)
        updated = repo.update(todo.id, description="Updated")
        assert updated.priority == Priority.HIGH
        assert updated.description == "Updated"


class TestPriorityService:
    """Test priority feature in TodoService."""

    def test_create_todo_with_default_priority(self):
        """Test that service defaults priority to medium."""
        repo = TodoRepository()
        service = TodoService(repo)
        todo = service.create_todo(title="Test")
        assert todo.priority == Priority.MEDIUM

    def test_create_todo_with_explicit_priority(self):
        """Test service accepts explicit priority."""
        repo = TodoRepository()
        service = TodoService(repo)
        todo = service.create_todo(title="Urgent", priority=Priority.HIGH)
        assert todo.priority == Priority.HIGH

    def test_update_todo_priority(self):
        """Test service updates priority correctly."""
        repo = TodoRepository()
        service = TodoService(repo)
        todo = service.create_todo(title="Test", priority=Priority.MEDIUM)
        updated = service.update_todo(todo.id, priority=Priority.LOW)
        assert updated.priority == Priority.LOW


class TestPriorityModel:
    """Test priority in Pydantic models."""

    def test_todo_create_default_priority(self):
        """Test TodoCreate has default priority."""
        todo_data = TodoCreate(title="Test")
        assert todo_data.priority == Priority.MEDIUM

    def test_todo_create_explicit_priority(self):
        """Test TodoCreate accepts priority."""
        todo_data = TodoCreate(title="Test", priority=Priority.HIGH)
        assert todo_data.priority == Priority.HIGH

    def test_todo_response_includes_priority(self):
        """Test TodoResponse model includes priority field."""
        repo = TodoRepository()
        created = repo.create(title="Test", priority=Priority.LOW)
        response = TodoResponse(
            id=created.id,
            title=created.title,
            description=created.description,
            completed=created.completed,
            priority=created.priority,
            created_at=created.created_at
        )
        assert response.priority == Priority.LOW


class TestPriorityEnum:
    """Test Priority enum values."""

    def test_priority_enum_values(self):
        """Test that Priority enum has correct values."""
        assert Priority.HIGH.value == "high"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.LOW.value == "low"

    def test_priority_enum_comparison(self):
        """Test Priority enum comparisons."""
        assert Priority.HIGH == Priority.HIGH
        assert Priority.HIGH != Priority.MEDIUM
        assert Priority.MEDIUM != Priority.LOW


class TestAcceptanceCriteria:
    """Test all acceptance criteria are met."""

    def test_ac1_todo_model_has_priority_enum(self):
        """AC1: Todo model has priority field with enum values (high, medium, low)."""
        repo = TodoRepository()

        # Create todos with each priority level
        high_todo = repo.create(title="High", priority=Priority.HIGH)
        medium_todo = repo.create(title="Medium", priority=Priority.MEDIUM)
        low_todo = repo.create(title="Low", priority=Priority.LOW)

        assert high_todo.priority == Priority.HIGH
        assert medium_todo.priority == Priority.MEDIUM
        assert low_todo.priority == Priority.LOW

    def test_ac2_api_accept_return_priority(self):
        """AC2: API can accept and return priority values."""
        # Simulating API request/response
        todo_create = TodoCreate(title="Test", priority=Priority.HIGH)
        assert todo_create.priority == Priority.HIGH

        repo = TodoRepository()
        created = repo.create(
            title=todo_create.title,
            priority=todo_create.priority
        )

        response = TodoResponse(
            id=created.id,
            title=created.title,
            description=created.description,
            completed=created.completed,
            priority=created.priority,
            created_at=created.created_at
        )
        assert response.priority == Priority.HIGH

    def test_ac3_database_persistence(self):
        """AC3: Database persistence preserves priority settings."""
        repo = TodoRepository()
        todo1 = repo.create(title="Task 1", priority=Priority.HIGH)
        todo2 = repo.create(title="Task 2", priority=Priority.LOW)

        # Verify persistence (retrieve from repository)
        retrieved_todo1 = repo.get_by_id(todo1.id)
        retrieved_todo2 = repo.get_by_id(todo2.id)

        assert retrieved_todo1.priority == Priority.HIGH
        assert retrieved_todo2.priority == Priority.LOW

    def test_ac4_default_priority_medium(self):
        """AC4: Unspecified priority defaults to 'medium'."""
        repo = TodoRepository()
        service = TodoService(repo)

        # Create without specifying priority
        todo = service.create_todo(title="Default Priority")
        assert todo.priority == Priority.MEDIUM

    def test_ac5_service_handles_priority(self):
        """AC5: Todo service properly handles priority operations."""
        repo = TodoRepository()
        service = TodoService(repo)

        # Create with priority
        todo = service.create_todo(title="Task", priority=Priority.HIGH)
        assert todo.priority == Priority.HIGH

        # Update priority
        updated = service.update_todo(todo.id, priority=Priority.LOW)
        assert updated.priority == Priority.LOW

        # Verify it's updated in repository
        verified = service.get_todo(todo.id)
        assert verified.priority == Priority.LOW

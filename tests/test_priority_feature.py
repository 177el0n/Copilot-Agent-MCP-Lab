"""Tests for the priority feature."""

import pytest
from fastapi.testclient import TestClient
from app.repositories.todo_repository import TodoRepository, Todo, Priority
from app.services.todo_service import TodoService
from app.models import TodoCreate, TodoResponse, Priority as ModelPriority
from app.main import app


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


class TestPriorityErrorCases:
    """Test error handling for priority feature."""

    def test_update_nonexistent_todo_returns_none(self):
        """Test that updating a non-existent todo returns None."""
        repo = TodoRepository()
        result = repo.update(999, priority=Priority.HIGH)
        assert result is None

    def test_service_update_nonexistent_todo_returns_none(self):
        """Test that service update returns None for non-existent todo."""
        repo = TodoRepository()
        service = TodoService(repo)
        result = service.update_todo(999, priority=Priority.HIGH)
        assert result is None

    def test_create_todo_with_empty_title_raises_error(self):
        """Test that creating a todo with empty title raises ValueError."""
        repo = TodoRepository()
        service = TodoService(repo)
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.create_todo(title="")

    def test_create_todo_with_whitespace_only_title_raises_error(self):
        """Test that creating a todo with whitespace-only title raises ValueError."""
        repo = TodoRepository()
        service = TodoService(repo)
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.create_todo(title="   ")

    def test_create_todo_with_none_title_raises_error(self):
        """Test that creating a todo with None title raises error."""
        repo = TodoRepository()
        service = TodoService(repo)
        with pytest.raises((TypeError, ValueError)):
            service.create_todo(title=None)


class TestPriorityBoundaryConditions:
    """Test boundary conditions for priority feature."""

    def test_first_todo_gets_default_priority(self):
        """Test that the first created todo (ID=1) has default priority."""
        repo = TodoRepository()
        todo = repo.create(title="First Todo")
        assert todo.id == 1
        assert todo.priority == Priority.MEDIUM

    def test_priority_persists_across_multiple_updates(self):
        """Test that priority persists through multiple non-priority updates."""
        repo = TodoRepository()
        todo = repo.create(title="Test", priority=Priority.HIGH)
        
        # Update other fields multiple times
        update1 = repo.update(todo.id, title="New Title")
        assert update1.priority == Priority.HIGH
        
        update2 = repo.update(todo.id, description="Description")
        assert update2.priority == Priority.HIGH
        
        update3 = repo.update(todo.id, completed=True)
        assert update3.priority == Priority.HIGH

    def test_update_only_priority_preserves_other_fields(self):
        """Test that updating only priority preserves other fields."""
        repo = TodoRepository()
        todo = repo.create(
            title="Original Title",
            description="Description",
            completed=True,
            priority=Priority.LOW
        )
        
        updated = repo.update(todo.id, priority=Priority.HIGH)
        assert updated.title == "Original Title"
        assert updated.description == "Description"
        assert updated.completed == True
        assert updated.priority == Priority.HIGH

    def test_multiple_sequential_priority_updates(self):
        """Test multiple sequential priority updates."""
        repo = TodoRepository()
        todo = repo.create(title="Test")
        
        # Update priority multiple times
        todo1 = repo.update(todo.id, priority=Priority.HIGH)
        assert todo1.priority == Priority.HIGH
        
        todo2 = repo.update(todo.id, priority=Priority.LOW)
        assert todo2.priority == Priority.LOW
        
        todo3 = repo.update(todo.id, priority=Priority.MEDIUM)
        assert todo3.priority == Priority.MEDIUM

    def test_multiple_todos_maintain_independent_priorities(self):
        """Test that multiple todos maintain independent priorities."""
        repo = TodoRepository()
        todo1 = repo.create(title="Todo1", priority=Priority.HIGH)
        todo2 = repo.create(title="Todo2", priority=Priority.LOW)
        todo3 = repo.create(title="Todo3", priority=Priority.MEDIUM)
        
        # Update one shouldn't affect others
        repo.update(todo1.id, priority=Priority.LOW)
        
        assert repo.get_by_id(todo1.id).priority == Priority.LOW
        assert repo.get_by_id(todo2.id).priority == Priority.LOW
        assert repo.get_by_id(todo3.id).priority == Priority.MEDIUM


class TestPriorityComplexScenarios:
    """Test complex scenarios involving priority."""

    def test_service_with_explicit_none_priority_defaults_to_medium(self):
        """Test that explicitly passing None for priority defaults to medium."""
        repo = TodoRepository()
        service = TodoService(repo)
        todo = service.create_todo(title="Test", priority=None)
        assert todo.priority == Priority.MEDIUM

    def test_full_lifecycle_create_update_delete_with_priority(self):
        """Test complete lifecycle: create with priority, update, and delete."""
        repo = TodoRepository()
        service = TodoService(repo)
        
        # Create
        todo = service.create_todo(title="Lifecycle Test", priority=Priority.HIGH)
        created_id = todo.id
        assert todo.priority == Priority.HIGH
        
        # Update
        updated = service.update_todo(created_id, priority=Priority.LOW)
        assert updated.priority == Priority.LOW
        
        # Verify
        verified = service.get_todo(created_id)
        assert verified.priority == Priority.LOW
        
        # Delete
        deleted = service.delete_todo(created_id)
        assert deleted == True
        
        # Verify deletion
        not_found = service.get_todo(created_id)
        assert not_found is None

    def test_all_priority_levels_can_be_retrieved(self):
        """Test that all priority levels can be created and retrieved."""
        repo = TodoRepository()
        service = TodoService(repo)
        
        todos = []
        for priority in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            todo = service.create_todo(title=f"Todo-{priority.value}", priority=priority)
            todos.append(todo)
        
        all_todos = service.get_all_todos()
        assert len(all_todos) == 3
        
        priorities = [t.priority for t in all_todos]
        assert Priority.HIGH in priorities
        assert Priority.MEDIUM in priorities
        assert Priority.LOW in priorities


class TestPriorityAPIConcerns:
    """Test API-level concerns for priority feature."""

    def test_todo_model_serialization_with_priority(self):
        """Test that TodoResponse correctly serializes priority."""
        repo = TodoRepository()
        created = repo.create(title="Test", priority=Priority.HIGH)
        
        response = TodoResponse(
            id=created.id,
            title=created.title,
            description=created.description,
            completed=created.completed,
            priority=created.priority,
            created_at=created.created_at
        )
        
        # Should be able to convert to dict (Pydantic model_dump)
        response_dict = response.model_dump()
        assert response_dict["priority"] == Priority.HIGH

    def test_todo_model_json_serialization(self):
        """Test that priority is JSON serializable."""
        todo_data = TodoCreate(title="Test", priority=Priority.MEDIUM)
        json_str = todo_data.model_dump_json()
        assert "medium" in json_str

    def test_integration_create_via_api_endpoint(self):
        """Test creating a todo with priority via FastAPI endpoint."""
        client = TestClient(app)
        
        response = client.post(
            "/todos",
            json={
                "title": "API Test Todo",
                "description": "Test description",
                "completed": False,
                "priority": "high"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "API Test Todo"
        assert data["priority"] == "high"

    def test_integration_get_via_api_endpoint(self):
        """Test retrieving a todo with priority via FastAPI endpoint."""
        client = TestClient(app)
        
        # Create
        create_response = client.post(
            "/todos",
            json={
                "title": "Get Test",
                "priority": "low"
            }
        )
        created_id = create_response.json()["id"]
        
        # Get
        get_response = client.get(f"/todos/{created_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["priority"] == "low"

    def test_integration_list_todos_with_priorities(self):
        """Test listing todos returns priority for each."""
        client = TestClient(app)
        
        # Create multiple todos
        client.post(
            "/todos",
            json={"title": "High Priority", "priority": "high"}
        )
        client.post(
            "/todos",
            json={"title": "Low Priority", "priority": "low"}
        )
        
        # List all
        response = client.get("/todos")
        assert response.status_code == 200
        todos = response.json()
        
        # Each should have priority
        for todo in todos:
            assert "priority" in todo
            assert todo["priority"] in ["high", "medium", "low"]

    def test_integration_update_via_api_endpoint(self):
        """Test updating a todo's priority via FastAPI endpoint."""
        client = TestClient(app)
        
        # Create
        create_response = client.post(
            "/todos",
            json={"title": "Update Test", "priority": "low"}
        )
        created_id = create_response.json()["id"]
        
        # Update
        update_response = client.put(
            f"/todos/{created_id}",
            json={
                "title": "Update Test",
                "priority": "high",
                "completed": False
            }
        )
        
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["priority"] == "high"


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

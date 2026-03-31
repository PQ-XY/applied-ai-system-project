import pytest
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task, TaskType


@pytest.fixture
def owner():
    """Create a test owner"""
    return Owner(
        name="Test Owner",
        email="test@example.com",
        phone="555-1234",
        address="123 Test St"
    )


@pytest.fixture
def pet(owner):
    """Create a test pet"""
    return Pet(
        pet_id="pet_001",
        name="Buddy",
        species="Dog",
        breed="Labrador",
        age=3,
        health_info="Healthy",
        owner=owner
    )


@pytest.fixture
def scheduler(owner):
    """Create a test scheduler"""
    return Scheduler(scheduler_id="sched_001", owner=owner)


@pytest.fixture
def task(pet):
    """Create a test task"""
    return Task(
        task_id="task_001",
        task_type=TaskType.FEEDING,
        pet=pet,
        due_time=datetime.now() + timedelta(hours=1),
        priority=2,
        description="Feed Buddy",
        completed=False
    )


class TestTaskCompletion:
    """Test suite for task completion functionality"""
    
    def test_mark_complete_changes_status(self, task):
        """Verify that mark_complete() changes the task's completed status"""
        # Initially task should not be completed
        assert task.completed is False
        assert task.completed_time is None
        
        # Call mark_complete (to be implemented)
        task.mark_complete()
        
        # After calling mark_complete, task should be completed
        assert task.completed is True
        assert task.completed_time is not None
        assert isinstance(task.completed_time, datetime)
    
    def test_completed_time_is_set_on_mark_complete(self, task):
        """Verify that completed_time is set when task is marked complete"""
        before_completion = datetime.now()
        task.mark_complete()
        after_completion = datetime.now()
        
        # completed_time should be set and be current
        assert task.completed_time is not None
        assert before_completion <= task.completed_time <= after_completion


class TestTaskAddition:
    """Test suite for task addition functionality"""
    
    def test_adding_task_to_scheduler(self, scheduler, task):
        """Verify that adding a task to scheduler is tracked"""
        # Initially scheduler should have no tasks
        assert len(scheduler.tasks) == 0
        
        # Add task to scheduler
        scheduler.add_task(task)
        
        # Scheduler should now have the task
        assert len(scheduler.tasks) == 1
        assert task in scheduler.tasks
    
    def test_task_associated_with_correct_pet(self, scheduler, pet, task):
        """Verify that added task is correctly associated with the pet"""
        # Add task to scheduler
        scheduler.add_task(task)
        
        # Task should reference the correct pet
        assert task.pet == pet
        assert task.pet.name == "Buddy"
    
    def test_multiple_tasks_for_same_pet(self, scheduler, pet):
        """Verify that multiple tasks can be added for the same pet"""
        # Create multiple tasks for the same pet
        task_1 = Task(
            task_id="task_001",
            task_type=TaskType.FEEDING,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=1),
            priority=2,
            description="Morning feeding",
            completed=False
        )
        task_2 = Task(
            task_id="task_002",
            task_type=TaskType.WALK,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=4),
            priority=2,
            description="Afternoon walk",
            completed=False
        )
        
        # Add both tasks to scheduler
        scheduler.add_task(task_1)
        scheduler.add_task(task_2)
        
        # Verify both tasks are in scheduler
        assert len(scheduler.tasks) == 2
        
        # Verify both tasks reference the same pet
        pet_tasks = [t for t in scheduler.tasks if t.pet == pet]
        assert len(pet_tasks) == 2
    
    def test_multiple_pets_multiple_tasks(self, scheduler, owner):
        """Verify that tasks can be added for multiple pets"""
        # Create two pets
        dog = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            health_info="Healthy",
            owner=owner
        )
        cat = Pet(
            pet_id="pet_002",
            name="Luna",
            species="Cat",
            breed="Siamese",
            age=3,
            health_info="Healthy",
            owner=owner
        )
        
        # Create tasks for each pet
        task_dog = Task(
            task_id="task_001",
            task_type=TaskType.WALK,
            pet=dog,
            due_time=datetime.now() + timedelta(hours=1),
            priority=2,
            description="Walk Max",
            completed=False
        )
        task_cat = Task(
            task_id="task_002",
            task_type=TaskType.MEDICATION,
            pet=cat,
            due_time=datetime.now() + timedelta(hours=2),
            priority=1,
            description="Luna's medication",
            completed=False
        )
        
        # Add tasks to scheduler
        scheduler.add_task(task_dog)
        scheduler.add_task(task_cat)
        
        # Verify both tasks are in scheduler
        assert len(scheduler.tasks) == 2
        
        # Verify tasks are associated with correct pets
        dog_tasks = [t for t in scheduler.tasks if t.pet == dog]
        cat_tasks = [t for t in scheduler.tasks if t.pet == cat]
        assert len(dog_tasks) == 1
        assert len(cat_tasks) == 1
        assert dog_tasks[0].pet.name == "Max"
        assert cat_tasks[0].pet.name == "Luna"

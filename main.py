from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task, TaskType


def print_todays_schedule(scheduler: Scheduler) -> None:
    """Print today's scheduled tasks in chronological order"""
    today = datetime.now().date()
    
    # Filter tasks for today
    todays_tasks = [
        task for task in scheduler.tasks
        if task.due_time.date() == today
    ]
    
    # Sort by due time
    todays_tasks.sort(key=lambda t: t.due_time)
    
    print("\n" + "=" * 60)
    print(f"TODAY'S SCHEDULE - {today.strftime('%A, %B %d, %Y')}")
    print("=" * 60)
    
    if not todays_tasks:
        print("No tasks scheduled for today.")
    else:
        for task in todays_tasks:
            status = "✓" if task.completed else "○"
            time_str = task.due_time.strftime('%H:%M')
            print(f"\n{status} {time_str} - {task.task_type.value.upper()}")
            print(f"   Pet: {task.pet.name}")
            print(f"   {task.description}")
            print(f"   Priority: {'*' * task.priority}")
    
    print("=" * 60)


def main():
    """Main function to demonstrate PawPal+ system with an Owner and Pets"""
    
    # Create an Owner
    owner = Owner(
        name="Sarah Chen",
        email="sarah.chen@email.com",
        phone="555-0123",
        address="123 Oak Street, Portland, OR 97201"
    )
    
    # Create the first Pet - a dog
    dog = Pet(
        pet_id="pet_001",
        name="Max",
        species="Dog",
        breed="Golden Retriever",
        age=5,
        health_info="Healthy, up to date on vaccinations. Slight arthritis in rear left leg.",
        owner=owner
    )
    
    # Create the second Pet - a cat
    cat = Pet(
        pet_id="pet_002",
        name="Luna",
        species="Cat",
        breed="Siamese",
        age=3,
        health_info="Healthy. Prone to hairballs.",
        owner=owner
    )
    
    # Add pets to the owner
    owner.pets.append(dog)
    owner.pets.append(cat)
    
    # Create a Scheduler for the owner
    owner.scheduler = Scheduler(scheduler_id="sched_001", owner=owner)
    
    # Create Tasks with different times
    now = datetime.now()
    
    # Task 1: Feed Max (Morning)
    task_1 = Task(
        task_id="task_001",
        task_type=TaskType.FEEDING,
        pet=dog,
        due_time=now.replace(hour=8, minute=0),
        priority=3,
        description="Feed Max his morning kibble (2 cups)",
        completed=False
    )
    
    # Task 2: Walk Max (Afternoon)
    task_2 = Task(
        task_id="task_002",
        task_type=TaskType.WALK,
        pet=dog,
        due_time=now.replace(hour=15, minute=30),
        priority=2,
        description="Walk Max around the park (30-45 minutes)",
        completed=False
    )
    
    # Task 3: Luna's Medication (Evening)
    task_3 = Task(
        task_id="task_003",
        task_type=TaskType.MEDICATION,
        pet=cat,
        due_time=now.replace(hour=20, minute=0),
        priority=1,
        description="Give Luna her daily thyroid medication with food",
        completed=False
    )
    
    # Add tasks to the scheduler
    owner.scheduler.tasks.extend([task_1, task_2, task_3])
    
    # Display owner and pets information
    print(f"Owner: {owner.name}")
    print(f"Email: {owner.email}")
    print(f"Phone: {owner.phone}")
    print(f"Address: {owner.address}")
    print(f"\nPets ({len(owner.pets)}):")
    
    for pet in owner.pets:
        print(f"  - {pet.name} ({pet.species}, {pet.breed}, {pet.age} years old)")
        print(f"    Health: {pet.health_info}")
    
    print(f"\nScheduler ID: {owner.scheduler.scheduler_id}")
    print(f"Active Tasks: {len(owner.scheduler.tasks)}")
    print(f"Completed Tasks: {len(owner.scheduler.completed_tasks)}")
    
    # Print today's schedule
    print_todays_schedule(owner.scheduler)


if __name__ == "__main__":
    main()


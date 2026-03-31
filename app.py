import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task, TaskType

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, your pet care management system.

This app helps you plan and organize your pet's daily routine with intelligent task scheduling.
"""
)

st.divider()

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

if "pets" not in st.session_state:
    st.session_state.pets = []

# Owner Setup
st.subheader("👤 Owner Information")
col1, col2, col3, col4 = st.columns(4)

with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    owner_email = st.text_input("Email", value="jordan@example.com")
with col3:
    owner_phone = st.text_input("Phone", value="555-0000")
with col4:
    owner_address = st.text_input("Address", value="123 Main St")

if st.button("Initialize Owner & Scheduler"):
    st.session_state.owner = Owner(
        name=owner_name,
        email=owner_email,
        phone=owner_phone,
        address=owner_address
    )
    st.session_state.scheduler = Scheduler(
        scheduler_id="sched_001",
        owner=st.session_state.owner
    )
    st.success(f"✅ Owner '{owner_name}' and Scheduler initialized!")

if st.session_state.owner:
    st.info(f"Owner: **{st.session_state.owner.name}** | Email: {st.session_state.owner.email}")

st.divider()

# Pet Management
st.subheader("🐕 Manage Pets")

if st.session_state.owner:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        pet_species = st.selectbox("Species", ["Dog", "Cat", "Rabbit", "Bird", "Other"])
    with col3:
        pet_breed = st.text_input("Breed", value="Labrador")
    with col4:
        pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
    
    pet_health = st.text_area("Health info", value="Healthy, up to date on vaccinations")
    
    if st.button("Add Pet"):
        pet = Pet(
            pet_id=f"pet_{len(st.session_state.pets) + 1:03d}",
            name=pet_name,
            species=pet_species,
            breed=pet_breed,
            age=pet_age,
            health_info=pet_health,
            owner=st.session_state.owner
        )
        st.session_state.pets.append(pet)
        st.session_state.owner.pets.append(pet)
        st.success(f"✅ Pet '{pet_name}' added!")
    
    if st.session_state.pets:
        st.markdown("### Current Pets")
        for pet in st.session_state.pets:
            st.info(f"🐾 **{pet.name}** ({pet.species}, {pet.breed}, {pet.age} years) - {pet.health_info}")
else:
    st.warning("⚠️ Please initialize an Owner first.")

st.divider()

# Task Scheduling
st.subheader("📋 Schedule Tasks")

if st.session_state.owner and st.session_state.pets:
    st.markdown("### Add a Task")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_pet = st.selectbox(
            "Select pet",
            options=st.session_state.pets,
            format_func=lambda p: f"{p.name} ({p.species})"
        )
        task_type = st.selectbox(
            "Task type",
            options=[t.value for t in TaskType],
            format_func=lambda x: x.upper()
        )
        task_description = st.text_input("Task description", value="Feed pet")
    
    with col2:
        task_time = st.time_input("Time", value=datetime.now().time())
        task_priority = st.slider("Priority (1=Low, 5=High)", min_value=1, max_value=5, value=3)
    
    if st.button("Schedule Task"):
        due_datetime = datetime.combine(datetime.now().date(), task_time)
        
        task = Task(
            task_id=f"task_{len(st.session_state.scheduler.tasks) + 1:03d}",
            task_type=TaskType(task_type),
            pet=selected_pet,
            due_time=due_datetime,
            priority=task_priority,
            description=task_description,
            completed=False
        )
        
        st.session_state.scheduler.add_task(task)
        st.success(f"✅ Task '{task_description}' scheduled for {selected_pet.name} at {task_time}!")
    
    if st.session_state.scheduler.tasks:
        st.markdown("### Current Schedule")
        
        # Sort tasks by time
        sorted_tasks = sorted(st.session_state.scheduler.tasks, key=lambda t: t.due_time)
        
        for task in sorted_tasks:
            status_icon = "✅" if task.completed else "⏳"
            priority_stars = "⭐" * task.priority
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"{status_icon} **[{task.task_type.value.upper()}]** {task.description}")
                st.caption(f"Pet: {task.pet.name} | Time: {task.due_time.strftime('%H:%M')}")
            with col2:
                st.write(f"Priority: {priority_stars}")
            with col3:
                if st.button("✓ Complete", key=f"complete_{task.task_id}"):
                    task.mark_complete()
                    st.rerun()
    else:
        st.info("No tasks scheduled yet. Add one above.")

elif st.session_state.owner:
    st.warning("⚠️ Please add at least one pet before scheduling tasks.")

else:
    st.warning("⚠️ Please initialize an Owner first.")

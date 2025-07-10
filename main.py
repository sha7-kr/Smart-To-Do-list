import streamlit as st
# Store tasks in session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "task_id_counter" not in st.session_state:
    st.session_state.task_id_counter = 1

# Keywords for auto-priority detection
high_priority_keywords = ["exam", "deadline", "submit", "interview", "study", "urgent", "important"]
medium_priority_keywords = ["meeting", "homework", "project", "exercise"]
low_priority_keywords = ["clean", "watch", "nap", "scroll", "music", "chat", "walk"]

def detect_priority(description):
    desc = description.lower()
    for word in high_priority_keywords:
        if word in desc:
            return "🔴 High"
    for word in medium_priority_keywords:
        if word in desc:
            return "🟡 Medium"
    for word in low_priority_keywords:
        if word in desc:
            return "🟢 Low"
    return "⚪ Unknown"

def priority_value(priority):
    if "🔴" in priority:
        return 1
    elif "🟡" in priority:
        return 2
    elif "🟢" in priority:
        return 3
    else:
        return 4

st.set_page_config(page_title="🧠 Smart To-Do List", page_icon="📝", layout="centered")

st.title("🧠 Smart To-Do List by Shahd")
st.markdown("Organize your day with soft colors and smart priority detection! ✨")

# --- Add Task Form ---
with st.form("add_task_form", clear_on_submit=True):
    description = st.text_input("📝 Task Description")
    time_period = st.selectbox("🕒 Time Period", ["Morning 🌤️", "Afternoon ☀️", "Evening 🌇", "Night 🌙"])
    submitted = st.form_submit_button("Add Task ➕")
    
    if submitted:
        if description.strip() == "":
            st.warning("Please enter a task description.")
        else:
            priority = detect_priority(description)
            task = {
                "id": st.session_state.task_id_counter,
                "description": description,
                "time_period": time_period,
                "priority": priority
            }
            st.session_state.tasks.append(task)
            st.session_state.task_id_counter += 1
            st.success(f"Task added with priority {priority}!")

# --- Delete Task ---
def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]

# --- Edit Task ---
def edit_task(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            with st.form(f"edit_form_{task_id}"):
                new_desc = st.text_input("📝 Edit Description", value=task["description"])
                new_time = st.selectbox("🕒 Edit Time Period", ["Morning 🌤️", "Afternoon ☀️", "Evening 🌇", "Night 🌙"], 
                                        index=["Morning 🌤️", "Afternoon ☀️", "Evening 🌇", "Night 🌙"].index(task["time_period"]))
                submitted = st.form_submit_button("Save Changes 💾")
                if submitted:
                    task["description"] = new_desc
                    task["time_period"] = new_time
                    task["priority"] = detect_priority(new_desc)
                    st.success("Task updated!")
                    st.experimental_rerun()
            break

# --- Display Tasks ---
if st.session_state.tasks:
    st.markdown("## 📋 Your Tasks (Sorted by Priority):")
    tasks_sorted = sorted(st.session_state.tasks, key=lambda x: priority_value(x["priority"]))
    
    for task in tasks_sorted:
        with st.expander(f"🆔 {task['id']} | {task['time_period']} | {task['priority']} | {task['description']}"):
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                if st.button("✏️ Edit", key=f"edit_{task['id']}"):
                    edit_task(task["id"])
            with col2:
                if st.button("❌ Delete", key=f"delete_{task['id']}"):
                    delete_task(task["id"])
                    st.experimental_rerun()
else:
    st.info("📭 No tasks yet. Add some tasks to get started!")

# --- Clear All Tasks ---
if st.button("🔄 Clear All Tasks"):
    st.session_state.tasks = []
    st.session_state.task_id_counter = 1
    st.success("All tasks cleared!")
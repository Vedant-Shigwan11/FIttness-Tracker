import streamlit as st
import pandas as pd
import os

# File for saving data
DATA_FILE = "workouts.csv"

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Exercise Type", "Duration (min)", "Calories Burned"])

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Load workouts
workouts = load_data()

# Streamlit UI
st.set_page_config(page_title="Personal Fitness Tracker", layout="wide")
st.markdown("""
    <style>
        .big-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #FF5733;
        }
        .sub-title {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #2E86C1;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-family: Arial; font-weight: bold; color: hue'>🏋️ Personal Fitness Tracker</h1>", unsafe_allow_html=True)

# Workout Entry Section
st.markdown("<p class='sub-title'>Add New Workout</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
date = col1.date_input("Date")
exercise_type = col2.text_input("Exercise Type")
duration = col3.number_input("Duration (min)", min_value=1, step=1)
calories_burned = col4.number_input("Calories Burned", min_value=1, step=1)

if st.button("➕ Add Workout", use_container_width=True):
    new_data = pd.DataFrame([[date, exercise_type, duration, calories_burned]],
                            columns=["Date", "Exercise Type", "Duration (min)", "Calories Burned"])
    workouts = pd.concat([workouts, new_data], ignore_index=True)
    save_data(workouts)
    st.success("✅ Workout Added Successfully!")

# Display Workouts
st.markdown("<p class='sub-title'>📜 Workout History</p>", unsafe_allow_html=True)

if not workouts.empty:
    with st.expander("View Workouts", expanded=True):
        st.dataframe(workouts, use_container_width=True)

    # Delete option
    if st.button("🗑️ Clear All Workouts", use_container_width=True):
        workouts = pd.DataFrame(columns=["Date", "Exercise Type", "Duration (min)", "Calories Burned"])
        save_data(workouts)
        st.warning("⚠️ All workouts deleted!")
else:
    st.info("No workouts recorded yet.")

# Statistics Section
if not workouts.empty:
    st.markdown("<p class='sub-title'>📊 Workout Statistics</p>", unsafe_allow_html=True)
    total_workouts = len(workouts)
    total_duration = workouts["Duration (min)"].sum()
    total_calories = workouts["Calories Burned"].sum()
    avg_duration = total_duration / total_workouts if total_workouts else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Workouts", total_workouts)
    col2.metric("Total Duration", f"{total_duration} min")
    col3.metric("Total Calories Burned", f"{total_calories} kcal")
    col4.metric("Avg Duration per Workout", f"{avg_duration:.2f} min")

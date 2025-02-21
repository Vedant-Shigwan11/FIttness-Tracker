import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import os

# Workout Class
class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

# User Class
class User:
    def __init__(self):
        self.workouts = []
        self.load_data()

    def add_workout(self, workout):
        self.workouts.append(workout)

    def delete_workout(self, index):
        if 0 <= index < len(self.workouts):
            del self.workouts[index]

    def save_data(self, filename="workouts.txt"):
        with open(filename, "w") as file:
            for workout in self.workouts:
                file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")

    def load_data(self, filename="workouts.txt"):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.workouts.clear()
                for line in file:
                    date, exercise_type, duration, calories_burned = line.strip().split(',')
                    self.workouts.append(Workout(date, exercise_type, int(duration), int(calories_burned)))

# GUI Application
class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏋️ Personal Fitness Tracker")
        self.root.geometry("900x800")
        self.root.configure(bg="#1e1e2e")  # Dark Purple Theme

        self.user = User()

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=8, relief="flat", font=("Arial", 10, "bold"), background="#7b68ee")
        self.style.configure("TLabel", background="#1e1e2e", foreground="white", font=("Arial", 11))
        self.style.configure("TFrame", background="#292943")
        self.style.configure("Treeview", background="#f0f0f0", foreground="black", rowheight=30)
        self.style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#4b0082", foreground="white")

        # Title
        title_label = tk.Label(root, text="🏋️ Personal Fitness Tracker", font=("Helvetica", 18, "bold"), fg="white", bg="#7b68ee", padx=20, pady=10, relief="raised", borderwidth=3)
        title_label.pack(pady=15)

        # Workout Entry Box
        entry_frame = tk.Frame(root, bg="#292943", padx=15, pady=15, relief="groove", borderwidth=3)
        entry_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(entry_frame, text="📅 Date:", fg="white", bg="#292943", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = DateEntry(entry_frame, width=12, background="blue", foreground="white", borderwidth=2)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(entry_frame, text="🏃‍♂️ Exercise Type:", fg="white", bg="#292943", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.exercise_entry = tk.Entry(entry_frame, width=20, font=("Arial", 10))
        self.exercise_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(entry_frame, text="⏳ Duration (min):", fg="white", bg="#292943", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = tk.Entry(entry_frame, width=5, font=("Arial", 10))
        self.duration_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(entry_frame, text="🔥 Calories Burned:", fg="white", bg="#292943", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.calories_entry = tk.Entry(entry_frame, width=5, font=("Arial", 10))
        self.calories_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(entry_frame, text="➕ Add Workout", command=self.add_workout, bg="#7b68ee", fg="white", font=("Arial", 10, "bold"), relief="raised", padx=10).grid(row=4, columnspan=2, pady=10)

        # Workout List Table
        self.tree = ttk.Treeview(root, columns=("Date", "Exercise", "Duration", "Calories"), show="headings", height=8)
        self.tree.heading("Date", text="📅 Date")
        self.tree.heading("Exercise", text="🏃‍♂️ Exercise")
        self.tree.heading("Duration", text="⏳ Duration (min)")
        self.tree.heading("Calories", text="🔥 Calories Burned")
        self.tree.pack(pady=10, padx=10, fill="x")

        # Buttons
        button_frame = tk.Frame(root, bg="#1e1e2e")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🗑 Delete Workout", command=self.delete_workout, bg="#ff6347", fg="white", font=("Arial", 10, "bold"), relief="raised", padx=10).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="💾 Save Workouts", command=self.save_workouts, bg="#32cd32", fg="white", font=("Arial", 10, "bold"), relief="raised", padx=10).grid(row=0, column=1, padx=10)

        # Statistics
        self.stats_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="white", bg="#292943", padx=10, pady=5)
        self.stats_label.pack(pady=10, fill="x", padx=20)

        self.update_workout_list()
        self.update_statistics()

    def add_workout(self):
        date = self.date_entry.get()
        exercise_type = self.exercise_entry.get()
        duration = self.duration_entry.get()
        calories_burned = self.calories_entry.get()

        if not exercise_type or not duration.isdigit() or not calories_burned.isdigit():
            messagebox.showerror("Error", "Please enter valid workout details.")
            return

        workout = Workout(date, exercise_type, int(duration), int(calories_burned))
        self.user.add_workout(workout)
        self.update_workout_list()
        self.update_statistics()
        messagebox.showinfo("Success", "Workout added successfully!")

    def delete_workout(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a workout to delete.")
            return
        self.tree.delete(selected_item)
        self.user.delete_workout(int(selected_item[0]))
        self.update_statistics()
        messagebox.showinfo("Success", "Workout deleted successfully!")

    def save_workouts(self):
        self.user.save_data()
        messagebox.showinfo("Success", "Workouts saved successfully!")

    def update_workout_list(self):
        self.tree.delete(*self.tree.get_children())
        for idx, workout in enumerate(self.user.workouts):
            self.tree.insert("", "end", iid=idx, values=(workout.date, workout.exercise_type, workout.duration, workout.calories_burned))

    def update_statistics(self):
        self.stats_label.config(text=f"📊 Total Workouts: {len(self.user.workouts)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()

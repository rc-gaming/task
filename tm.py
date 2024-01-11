import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import json

class Task:
    def __init__(self, name, priority, due_date):
        self.name = name
        self.priority = priority
        self.due_date = due_date

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.tasks = []

        self.task_name_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.due_date_var = tk.StringVar()

        self.create_widgets()
        self.load_tasks_from_file()

    def create_widgets(self):
        # Task Name Label and Entry
        tk.Label(self.root, text="Task Name:").grid(row=0, column=0, sticky="w")
        task_name_entry = tk.Entry(self.root, textvariable=self.task_name_var)
        task_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Priority Label and Dropdown
        tk.Label(self.root, text="Priority:").grid(row=1, column=0, sticky="w")
        priority_values = ["Low", "Medium", "High"]
        priority_dropdown = ttk.Combobox(self.root, textvariable=self.priority_var, values=priority_values)
        priority_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Due Date Label and Calendar
        tk.Label(self.root, text="Due Date:").grid(row=2, column=0, sticky="w")

        # Use the validate method for date validation
        validate_date = (self.root.register(self.validate_date), '%P')

        due_date_entry = DateEntry(self.root, textvariable=self.due_date_var, date_pattern="yyyy-mm-dd")
        due_date_entry.grid(row=2, column=1, padx=10, pady=5)
        due_date_entry.config(validate='key', validatecommand=validate_date)

        # Add Task Button
        add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_task_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Task List Treeview
        self.task_list_treeview = ttk.Treeview(self.root, columns=("Priority", "Due Date"))
        self.task_list_treeview.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.task_list_treeview.heading("#0", text="Task Name")
        self.task_list_treeview.heading("Priority", text="Priority")
        self.task_list_treeview.heading("Due Date", text="Due Date")

        # Delete Task Button
        delete_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_task_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        # Clear Task Button
        clear_task_button = tk.Button(self.root, text="Clear Task", command=self.clear_task)
        clear_task_button.grid(row=5, column=1, padx=10, pady=5, sticky="e")

        save_tasks_button = tk.Button(self.root, text="Save Tasks", command=self.save_tasks_to_file)
        save_tasks_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def validate_date(self, new_value):
        try:
            # Try to parse the entered value as a date
            datetime.strptime(new_value, "%Y-%m-%d")
            return True
        except ValueError:
            # If parsing fails, return False
            return False
    def add_task(self):
        # Get task details from the entry widgets
        task_name = self.task_name_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()

        # Validate task details
        if not task_name or not priority or not due_date:
            messagebox.showwarning("Warning", "Please fill in all task details.")
            return

        # Create a Task object and add it to the task list
        new_task = Task(name=task_name, priority=priority, due_date=due_date)
        self.tasks.append(new_task)

        # Update the task list display
        self.update_task_list()

        # Clear the entry widgets after adding the task
        self.clear_task()

    def update_task_list(self):
        # Clear existing items in the Treeview
        for item in self.task_list_treeview.get_children():
            self.task_list_treeview.delete(item)

        # Populate the Treeview with the current task list
        for task in self.tasks:
            self.task_list_treeview.insert("", "end", text=task.name, values=(task.priority, task.due_date))
    def delete_task(self):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            task_name = self.task_list_treeview.item(selected_item)["text"]
            for task in self.tasks:
                if task.name == task_name:
                    self.tasks.remove(task)
                    self.task_list_treeview.delete(selected_item)
                    break
        self.save_tasks_to_file()

    def save_tasks_to_file(self):
        with open("tasks.json", "w") as json_file:
            tasks_data = [{"name": task.name, "priority": task.priority, "due_date": task.due_date} for task in self.tasks]
            json.dump(tasks_data, json_file)

    def load_tasks_from_file(self):
        try:
            with open("tasks.json", "r") as json_file:
                tasks_data = json.load(json_file)
                self.tasks = []

            for data in tasks_data:
                if all(key in data for key in ("name", "priority", "due_date")):
                    task = Task(data["name"], data["priority"], data["due_date"])
                    self.tasks.append(task)

                    # Populate the Treeview with loaded tasks
                    self.task_list_treeview.insert("", tk.END, text=task.name, values=(task.priority, task.due_date))
                else:
                    print("Skipping incomplete task:", data)
        except FileNotFoundError:
            # If the file doesn't exist, create an empty list of tasks
            self.tasks = []

    def clear_task(self):
        self.task_name_var.set("")
        self.priority_var.set("")
        self.due_date_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.configure(bg="#F39C12")  # Set your desired background color
    root.mainloop()

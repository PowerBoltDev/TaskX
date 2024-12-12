import tkinter as tk
from tkinter import ttk, messagebox
from enum import Enum
from datetime import datetime, timedelta
import uuid

# Equivalent Python Enum for Priority
class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

# Python equivalent of Task class
class Task:
    def __init__(self, title, description, priority, due_date):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.total_tracked_time = timedelta()
        self.timer_start = None
        self.is_timer_running = False

    def start_timer(self):
        if not self.is_timer_running:
            self.timer_start = datetime.now()
            self.is_timer_running = True

    def stop_timer(self):
        if self.is_timer_running:
            now = datetime.now()
            session_time = now - self.timer_start
            self.total_tracked_time += session_time
            self.is_timer_running = False
            return session_time
        return timedelta()

    def add_manual_time(self, duration):
        self.total_tracked_time += duration

class TaskXApp:
    def __init__(self, master):
        self.master = master
        master.title("Personal Task Manager")
        master.geometry("800x600")

        # Task storage
        self.tasks = []

        # Create main frames
        self.create_task_list_frame()
        self.create_task_entry_frame()

    def create_task_list_frame(self):
        # Task List Frame (left side)
        list_frame = tk.Frame(self.master, width=350)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Task List Label
        tk.Label(list_frame, text="Task List", font=("Helvetica", 14)).pack()

        # Treeview for tasks
        self.task_tree = ttk.Treeview(list_frame, columns=('Title', 'Priority', 'Time'), show='headings')
        self.task_tree.heading('Title', text='Title')
        self.task_tree.heading('Priority', text='Priority')
        self.task_tree.heading('Time', text='Time Spent')
        self.task_tree.pack(fill=tk.BOTH, expand=True)

        # Buttons frame
        button_frame = tk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=5)

        # Action Buttons
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Start Timer", command=self.start_timer).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Stop Timer", command=self.stop_timer).pack(side=tk.LEFT, padx=5)

    def create_task_entry_frame(self):
        # Task Entry Frame (right side)
        entry_frame = tk.Frame(self.master, width=350)
        entry_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title Entry
        tk.Label(entry_frame, text="Task Title:").pack(anchor='w')
        self.title_entry = tk.Entry(entry_frame, width=50)
        self.title_entry.pack(fill=tk.X)

        # Description Entry
        tk.Label(entry_frame, text="Description:").pack(anchor='w')
        self.desc_entry = tk.Text(entry_frame, height=3, width=50)
        self.desc_entry.pack(fill=tk.X)

        # Priority Dropdown
        tk.Label(entry_frame, text="Priority:").pack(anchor='w')
        self.priority_var = tk.StringVar(value=Priority.MEDIUM.value)
        priority_dropdown = ttk.Combobox(entry_frame, textvariable=self.priority_var, 
                                         values=[p.value for p in Priority])
        priority_dropdown.pack(fill=tk.X)

        # Due Date Entry
        tk.Label(entry_frame, text="Due Date:").pack(anchor='w')
        self.due_date_entry = tk.Entry(entry_frame, width=50)
        self.due_date_entry.insert(0, "YYYY-MM-DD")
        self.due_date_entry.pack(fill=tk.X)

        # Add Task Button
        tk.Button(entry_frame, text="Add Task", command=self.add_task).pack(pady=10)

        # Summary Area
        tk.Label(entry_frame, text="Task Summary:").pack(anchor='w')
        self.summary_text = tk.Text(entry_frame, height=5, width=50)
        self.summary_text.pack(fill=tk.X)
        tk.Button(entry_frame, text="Refresh Summary", command=self.refresh_summary).pack(pady=5)

    def add_task(self):
        try:
            title = self.title_entry.get()
            description = self.desc_entry.get("1.0", tk.END).strip()
            priority = Priority(self.priority_var.get())
            
            # Parse due date
            try:
                due_date = datetime.strptime(self.due_date_entry.get(), "%Y-%m-%d")
            except ValueError:
                due_date = datetime.now() + timedelta(days=7)

            # Create task
            task = Task(title, description, priority, due_date)
            self.tasks.append(task)

            # Update treeview
            self.task_tree.insert('', 'end', values=(task.title, task.priority.value, '0:00'))

            # Clear entries
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete("1.0", tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, "YYYY-MM-DD")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            # Remove from treeview
            self.task_tree.delete(selected_item)
            # Remove from tasks list (would need to match by ID in a real implementation)

    def start_timer(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            # In a full implementation, you'd match the selected task and start its timer
            task = self.tasks[self.task_tree.index(selected_item)]
            task.start_timer()

    def stop_timer(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            # In a full implementation, you'd match the selected task and stop its timer
            task = self.tasks[self.task_tree.index(selected_item)]
            task.stop_timer()

    def refresh_summary(self):
        summary = "Daily Task Summary:\n"
        for task in self.tasks:
            summary += f"Task: {task.title}, Time Spent: {task.total_tracked_time}\n"
        
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)

def main():
    root = tk.Tk()
    app = TaskXApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()




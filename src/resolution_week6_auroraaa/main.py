import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
 
TASKS_FILE = "tasks.json"
 
COLORS = {
    "High": "#e74c3c",
    "Medium": "#f39c12",
    "Low": "#27ae60"
}
 
LABEL = {
    "High": "[H]",
    "Medium": "[M]",
    "Low": "[L]"
}
 
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
 
class TodoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("TODO List")
        self.root.geometry("640x580")
        self.root.minsize(500, 400)
        self.bg = "#f0f2f5"
        self.panel_bg = "#ffffff"
        self.accent = "#4a6cf7"
        self.text_color = "#2d3436"
        self.done_color = "#b2bec3"
        self.root.configure(bg = self.bg)
        self.tasks = load_tasks()
        self.filter_var = tk.StringVar(value = "All")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_list())
        self._build_ui()
        self.refresh_list()
        self.refresh_stats()
    def _build_ui(self):
        root = self.root
        root.columnconfigure(0, weight = 1)
        root.rowconfigure(1, weight = 1)
        header = tk.Frame(root, bg = self.accent, padx = 16, pady = 10)
        header.grid(row = 0, column = 0, sticky = "ew")
        header.columnconfigure(1, weight = 1)
        tk.Label(
            header, text = "Todo List", font = ("Segoe UI", 16, "bold"), bg = self.accent, fg = "white"
        ).grid(row = 0, column = 0, sticky = "w")
        self.stats_label = tk.Label(
            header, text = "", font = ("Segoe UI", 9), bg = self.accent, fg = "#d0d8ff"
        )
        self.stats_label.grid(row = 0, column = 1, sticky="e")
        body = tk.Frame(root, bg=self.bg)
        body.grid(row = 1, column = 0, sticky="nsew", padx = 12)
        body.columnconfigure(0, weight = 1)
        body.rowconfigure(2, weight = 1)
        input_frame = tk.LabelFrame(
            body, text = "New task", font = ("Segoe UI", 9, "bold"), bg = self.panel_bg, fg = self.text_color, padx = 8, pady = 6, bd = 1, relief = "solid"
        )
        input_frame.grid(row = 0, column = 0, sticky = "ew", pady = (0, 8))
        input_frame.columnconfigure(1, weight = 1)
        tk.Label(
            input_frame, text = "Task:", font = ("Segoe UI", 9), bg = self.panel_bg, fg = self.text_color
        ).grid(row = 0, column = 0, sticky = "w", padx = (0, 6))
        self.task_entry = tk.Entry(
            input_frame, font=("Segoe UI", 10), relief = "solid", bd = 1
        )
        self.task_entry.grid(row = 0, column = 1, sticky = "ew", padx = (0, 8))
        self.task_entry.bind("<Return>", lambda _: self.add_task())
        tk.Label(
            input_frame, text = "Priority:", font = ("Segoe UI", 9), bg = self.panel_bg, fg = self.text_color
        ).grid(row = 0, column = 2, sticky = "w", padx=(0, 4))
        self.priority_var = tk.StringVar(value = "Medium")
        priority_menu = ttk.Combobox(
            input_frame, textvariable = self.priority_var, values = ["High", "Medium", "Low"], width = 8, state = "readonly"
        )
        priority_menu.grid(row = 0, column = 3, padx = (0, 8))
        tk.Label(
            input_frame, text = "Due:", font=("Segoe UI", 9), bg = self.panel_bg, fg = self.text_color
        ).grid(row = 1, column = 0, sticky = "w", padx = (0, 6), pady = (6, 0))
        self.due_entry = tk.Entry(
            input_frame, font = ("Segoe UI", 10), width = 12, relief = "solid", bd = 1
        )
        self.due_entry.grid(row = 1, column = 1, sticky = "w", pady = (6, 0))
        self.due_entry.insert(0, "YYYY-MM-DD")
        self.due_entry.bind("<FocusIn>", self._clear_due_placeholder)
        self.due_entry.bind("<FocusOut>", self._restore_due_placeholder)
        tk.Button(
            input_frame, text = "Add task", command = self.add_task, bg = self.accent, fg = "white", font = ("Segoe UI", 9, "bold"), relief = "flat", cursor = "hand2", padx = 10, pady = 4
        ).grid(row = 0, column = 4, rowspan = 2, padx = (0, 4), sticky = "ew", pady = (0, 4))
        filter_frame = tk.Frame(body, bg = self.bg)
        filter_frame.grid(row = 1, column = 0, sticky = "ew", pady = (0, 4))
        filter_frame.columnconfigure(6, weight = 1)
        tk.Label(
            filter_frame, text = "Show:", font = ("Segoe UI", 9), bg = self.bg, fg = self.text_color
        ).grid(row = 0, column = 0, sticky = "w",padx = (0, 4))
        for i, label in enumerate(["All", "Active", "Done"]):
            tk.Radiobutton(
                filter_frame, text = label, variable = self.filter_var, value = label, command = self.refresh_list, bg = self.bg, fg = self.text_color, selectcolor = self.bg, font = ("Segoe UI", 9), cursor = "hand2"
            ).grid(row = 0, column = i + 1, padx = 4)
        tk.Label(
            filter_frame, text = "Search:", font = ("Segoe UI", 9), bg = self.bg, fg = self.text_color
        ).grid(row = 0, column = 5, padx = (16, 4))
        tk.Entry(
            filter_frame, textvariable = self.search_var, font = ("Segoe UI", 9), relief = "solid", bd = 1, width = 20
        ).grid(row = 0, column = 6, sticky = "ew")
        list_frame = tk.Frame(body, bg = self.panel_bg, bd = 1, relief = "solid")
        list_frame.grid(row = 2, column = 0, sticky = "nsew")
        list_frame.columnconfigure(0, weight = 1)
        list_frame.rowconfigure(0, weight = 1)
        scrollbar = tk.Scrollbar(list_frame, orient = "vertical")
        scrollbar.grid(row = 0, column  = 1, sticky = "ns")
        self.listbox = tk.Listbox(
            list_frame, yscrollcommand = scrollbar.set, font = ("Segoe UI", 10), selectbackground = self.accent, selectforeground = "white", activestyle = "none", bd = 0, highlightthickness = 0, bg = self.panel_bg, fg = self.text_color
        )
        self.listbox.grid(row = 0, column = 0, sticky = "nsew")
        scrollbar.config(command = self.listbox.yview)
        self.listbox.bind("<Double-Button-1>", lambda _: self.toggle_task())
        btn_frame = tk.Frame(body, bg = self.bg)
        btn_frame.grid(row = 3, column = 0, sticky = "ew", pady = (6, 0))
        buttons = [
            ("Toggle Done", self.toggle_task, "#27ae60", "white"),
            ("Delete", self.delete_task, "#e74c3c", "white"),
            ("Clear Task", self.clear_completed, "#636e72", "white"),
            ("Task Info", self.show_task_info, self.accent, "white")
        ]
        for col, (label, cmd, bg, fg) in enumerate(buttons):
            tk.Button(
                btn_frame, text = label, command = cmd, bg = bg, fg = fg, font = ("Segoe UI", 9, "bold"), relief = "flat", cursor = "hand2", padx = 8, pady = 5
            ).grid(row = 0, column = col, padx = (0, 6))
    def _clear_due_placeholder(self, _event = None):
        if self.due_entry.get() == "YYYY-MM-DD":
            self.due_entry.delete(0, "end")
    def _restore_due_placeholder(self, _event = None):
        if not self.due_entry.get().strip():
            self.due_entry.insert(0, "YYYY-MM-DD")
    def _get_visible_tasks(self):
        f = self.filter_var.get()
        search = self.search_var.get().strip().lower()
        result = []
        for t in self.tasks:
            if f == "Active" and t["done"]:
                continue
            if f == "Done" and not t["done"]:
                continue
            if search and search not in t["text"].lower():
                continue
            result.append(t)
        return result
    _PRIO_ORDER = {"High": 0, "Medium": 1, "Low": 2}
    def _sort_key(self, t):
        return (int(t["done"]), self._PRIO_ORDER.get(t.get("priority", "Medium"), 1))
    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning("Empty task", "Please enter a task description :3")
            return
        due = self.due_entry.get().strip()
        if due == "YYYY-MM-DD":
            due = ""
        if due:
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid date", "Due date must be YYYY-MM-DD")
                return
        task = {
            "text": text,
            "done": False,
            "priority": self.priority_var.get(),
            "due": due,
            "added": datetime.now().strftime("%Y-%m-%d"),
        }
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.task_entry.delete(0, "end")
        self.due_entry.delete(0, "end")
        self.due_entry.insert(0, "YYYY-MM-DD")
        self.filter_var.set("All")
        self.refresh_list()
        self.refresh_stats()
    def toggle_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("No selection", "Please select a task to toggle")
            return
        visible = self._get_visible_tasks()
        task = visible[sel[0]]
        task["done"] = not task["done"]
        save_tasks(self.tasks)
        self.refresh_list()
        self.refresh_stats()
    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("No selection", "Please select a task to delete")
            return
        visible = self._get_visible_tasks()
        task = visible[sel[0]]
        if messagebox.askyesno("Delete task?", f"Delete \"{task['text']}\"?"):
            self.tasks.remove(task)
            save_tasks(self.tasks)
            self.refresh_list()
            self.refresh_stats()
    def clear_completed(self):
        done = [t for t in self.tasks if t["done"]]
        if not done:
            messagebox.showinfo("Nothing to be clear", "No completed tasks to remove")
            return
        if messagebox.askyesno("Clear completed", f"Remove all {len(done)} completed task(s)?"):
            self.tasks = [t for t in self.tasks if not t["done"]]
            save_tasks(self.tasks)
            self.refresh_list()
            self.refresh_stats()
    def show_task_info(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("No selection", "Please select a task to inspect")
            return
        visible = self._get_visible_tasks()
        t = visible[sel[0]]
        status = "Done" if t["done"] else "Active"
        priority = t.get("priority", "Medium")
        due = t.get("due") or "None"
        added = t.get("added") or "Unknown"
        messagebox.showinfo(
            "Tasks Details",
            f"Task: {t['text']}\n\n"
            f"Status: {status}\n"
            f"Priority: {priority}\n"
            f"Due: {due}\n"
            f"Added: {added}",
        )
    def refresh_list(self):
        self.listbox.delete(0, "end")
        visible = sorted(self._get_visible_tasks(), key=self._sort_key)
        for task in visible:
            prio = task.get("priority", "Medium")
            badge = LABEL[prio]
            due = f"(due: {task['due']})" if task.get("due") else ""
            check = "[x]" if task["done"] else "[ ]"
            label = f"{check}{badge}{task['text']}{due}"
            self.listbox.insert("end", label)
            if task["done"]:
                self.listbox.itemconfig("end", fg=self.done_color)
            else:
                self.listbox.itemconfig("end", fg=COLORS[prio])
    def refresh_stats(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["done"])
        active = total - done
        self.stats_label.config(
            text = f"{active} active | {done} done | {total} total"
        )
def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
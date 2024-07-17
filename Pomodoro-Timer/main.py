import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class PomodoroTimer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro Timer")
        self.geometry("600x600")
        self.configure(bg="#2E2E2E")

        self.pomodoro_time = 25 * 60  # 25 minutes
        self.short_break_time = 5 * 60  # 5 minutes
        self.long_break_time = 15 * 60  # 15 minutes
        self.current_time = self.pomodoro_time
        self.running = False
        self.on_break = False
        self.cycle = 0

        self.create_widgets()

    def create_widgets(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Helvetica", 14))
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)

        # Timer label style
        self.style.configure("Timer.TLabel", font=("Helvetica", 48, "bold"), padding=20)

        # Creating the timer label
        timer_frame = ttk.Frame(self, style="TFrame")
        timer_frame.pack(pady=20)

        self.timer_label = ttk.Label(timer_frame, text=self.format_time(self.current_time), style="Timer.TLabel")
        self.timer_label.pack()

        # Time settings frame
        time_frame = ttk.Frame(self, style="TFrame")
        time_frame.pack(pady=10)

        ttk.Label(time_frame, text="Pomodoro Time (min):").grid(row=0, column=0, padx=10)
        self.pomodoro_spinbox = ttk.Spinbox(time_frame, from_=1, to=60, width=5, font=("Helvetica", 12))
        self.pomodoro_spinbox.grid(row=0, column=1, padx=10)
        self.pomodoro_spinbox.delete(0, tk.END)
        self.pomodoro_spinbox.insert(0, "25")

        ttk.Label(time_frame, text="Short Break (min):").grid(row=1, column=0, padx=10)
        self.short_break_spinbox = ttk.Spinbox(time_frame, from_=1, to=30, width=5, font=("Helvetica", 12))
        self.short_break_spinbox.grid(row=1, column=1, padx=10)
        self.short_break_spinbox.delete(0, tk.END)
        self.short_break_spinbox.insert(0, "5")

        ttk.Label(time_frame, text="Long Break (min):").grid(row=2, column=0, padx=10)
        self.long_break_spinbox = ttk.Spinbox(time_frame, from_=1, to=60, width=5, font=("Helvetica", 12))
        self.long_break_spinbox.grid(row=2, column=1, padx=10)
        self.long_break_spinbox.delete(0, tk.END)
        self.long_break_spinbox.insert(0, "15")

        # Buttons frame
        button_frame = ttk.Frame(self, style="TFrame")
        button_frame.pack(pady=20)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer, style="TButton")
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_timer, style="TButton")
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer, style="TButton")
        self.reset_button.grid(row=0, column=2, padx=10)

        # To-do list
        self.todo_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=50, height=10, bg="#424242", fg="#FFFFFF",
                                       font=("Helvetica", 12), highlightthickness=0, bd=0, selectbackground="#FF5722",
                                       selectforeground="#FFFFFF")
        self.todo_listbox.pack(pady=20)

        task_button_frame = ttk.Frame(self, style="TFrame")
        task_button_frame.pack(pady=10)

        self.add_task_button = ttk.Button(task_button_frame, text="Add Task", command=self.add_task, style="TButton")
        self.add_task_button.grid(row=0, column=0, padx=10)

        self.complete_task_button = ttk.Button(task_button_frame, text="Complete Task", command=self.complete_task,
                                               style="TButton")
        self.complete_task_button.grid(row=0, column=1, padx=10)

        self.delete_task_button = ttk.Button(task_button_frame, text="Delete Task", command=self.delete_task,
                                             style="TButton")
        self.delete_task_button.grid(row=0, column=2, padx=10)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def update_timer(self):
        if self.running:
            if self.current_time > 0:
                self.current_time -= 1
                self.timer_label.config(text=self.format_time(self.current_time))
                self.after(1000, self.update_timer)
            else:
                self.running = False
                self.on_break = not self.on_break
                self.cycle += 1
                if self.cycle % 4 == 0:
                    self.current_time = self.long_break_time
                    messagebox.showinfo("Pomodoro Timer", "Long Break!")
                elif self.on_break:
                    self.current_time = self.short_break_time
                    messagebox.showinfo("Pomodoro Timer", "Short Break!")
                else:
                    self.current_time = self.pomodoro_time
                    messagebox.showinfo("Pomodoro Timer", "Pomodoro Session!")

                self.timer_label.config(text=self.format_time(self.current_time))

    def start_timer(self):
        self.pomodoro_time = int(self.pomodoro_spinbox.get()) * 60
        self.short_break_time = int(self.short_break_spinbox.get()) * 60
        self.long_break_time = int(self.long_break_spinbox.get()) * 60

        if not self.running:
            self.running = True
            self.current_time = self.pomodoro_time if not self.on_break else self.short_break_time if self.cycle % 4 != 0 else self.long_break_time
            self.update_timer()

    def pause_timer(self):
        self.running = False

    def reset_timer(self):
        self.running = False
        self.current_time = self.pomodoro_time
        self.on_break = False
        self.timer_label.config(text=self.format_time(self.current_time))

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter task:")
        if task:
            self.todo_listbox.insert(tk.END, task)

    def complete_task(self):
        selected_tasks = self.todo_listbox.curselection()
        for task_index in selected_tasks[::-1]:
            task = self.todo_listbox.get(task_index)
            self.todo_listbox.delete(task_index)
            self.todo_listbox.insert(tk.END, f"[Completed] {task}")

    def delete_task(self):
        selected_tasks = self.todo_listbox.curselection()
        for task_index in selected_tasks[::-1]:
            self.todo_listbox.delete(task_index)


if __name__ == "__main__":
    app = PomodoroTimer()
    app.mainloop()

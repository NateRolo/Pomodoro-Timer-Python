import tkinter as tk
from tkinter import messagebox, ttk
from threading import Timer
from pynput import keyboard, mouse
import threading

# Default durations moved to class for customization
class PomodoroApp:
    def __init__(self, master):
        """
        Initialize the Pomodoro Timer application.
        """
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.geometry("400x500")  
        self.input_blocked = False
        self.failsafe_triggered = False

        # Default timer settings
        self.work_duration = 25
        self.short_break_duration = 5
        self.long_break_duration = 15

        # Timer settings
        self.current_time = 0
        self.current_phase = "Work"
        self.running = False
        self.cycle_count = 0

        # UI components
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components.
        """
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.master, text="Timer Settings (minutes)", padding=10)
        settings_frame.pack(pady=10, padx=10, fill="x")

        # Work Duration
        ttk.Label(settings_frame, text="Work Duration:").grid(row=0, column=0, padx=5, pady=5)
        self.work_entry = ttk.Entry(settings_frame, width=10)
        self.work_entry.insert(0, str(self.work_duration))
        self.work_entry.grid(row=0, column=1, padx=5, pady=5)

        # Short Break Duration
        ttk.Label(settings_frame, text="Short Break:").grid(row=1, column=0, padx=5, pady=5)
        self.short_break_entry = ttk.Entry(settings_frame, width=10)
        self.short_break_entry.insert(0, str(self.short_break_duration))
        self.short_break_entry.grid(row=1, column=1, padx=5, pady=5)

        # Long Break Duration
        ttk.Label(settings_frame, text="Long Break:").grid(row=2, column=0, padx=5, pady=5)
        self.long_break_entry = ttk.Entry(settings_frame, width=10)
        self.long_break_entry.insert(0, str(self.long_break_duration))
        self.long_break_entry.grid(row=2, column=1, padx=5, pady=5)

        # Apply Settings Button
        apply_button = ttk.Button(settings_frame, text="Apply Settings", command=self.apply_settings)
        apply_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Timer Display
        self.timer_label = tk.Label(self.master, text="Pomodoro Timer", font=("Helvetica", 18))
        self.timer_label.pack(pady=20)

        self.time_display = tk.Label(self.master, text="00:00", font=("Helvetica", 36), fg="red")
        self.time_display.pack(pady=20)

        # Control buttons
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer, width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_timer, width=10)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer, width=10)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.update_timer_display()

    def apply_settings(self):
        """
        Validate and apply new timer settings.
        """
        try:
            new_work = int(self.work_entry.get())
            new_short = int(self.short_break_entry.get())
            new_long = int(self.long_break_entry.get())

            if any(duration <= 0 for duration in [new_work, new_short, new_long]):
                raise ValueError("Duration must be positive")

            self.work_duration = new_work
            self.short_break_duration = new_short
            self.long_break_duration = new_long

            # Reset timer if it's not running
            if not self.running:
                self.reset_timer()

            messagebox.showinfo("Success", "Settings updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid positive numbers for all durations")

    def start_timer(self):
        """
        Start or resume the Pomodoro timer.
        """
        if not self.running:
            self.running = True
            if self.current_time == 0:
                self.set_timer()
            self.run_timer()

    def pause_timer(self):
        """
        Pause the Pomodoro timer.
        """
        self.running = False

    def reset_timer(self):
        """
        Reset the Pomodoro timer.
        """
        self.running = False
        self.current_time = 0
        self.cycle_count = 0
        self.current_phase = "Work"
        self.update_timer_display()

    def set_timer(self):
        """
        Set the timer duration based on the current phase.
        """
        phase_durations = {
            "Work": self.work_duration * 60,
            "Short Break": self.short_break_duration * 60,
            "Long Break": self.long_break_duration * 60
        }
        self.current_time = phase_durations.get(self.current_phase, self.work_duration * 60)

    def run_timer(self):
        """
        Run the Pomodoro timer countdown.
        """
        if self.running and self.current_time > 0:
            mins, secs = divmod(self.current_time, 60)
            self.time_display.config(text=f"{mins:02d}:{secs:02d}")
            self.current_time -= 1
            self.master.after(1000, self.run_timer)
        elif self.current_time == 0:
            self.switch_phase()

    def switch_phase(self):
        """
        Switch to the next phase of the Pomodoro cycle.
        """
        self.running = False

        if self.current_phase == "Work":
            self.cycle_count += 1
            self.current_phase = "Short Break" if self.cycle_count < 4 else "Long Break"
            self.block_inputs()
        else:
            self.current_phase = "Work"
            self.unblock_inputs()

        if self.cycle_count == 4 and self.current_phase == "Long Break":
            messagebox.showinfo("Pomodoro Complete", "You've completed 4 Pomodoro cycles!")
            self.reset_timer()
        else:
            messagebox.showinfo("Timer Complete", f"{self.current_phase} phase starting!")
            self.set_timer()
            self.update_timer_display()

    def show_password_dialog(self):
        """
        Show a password dialog to unlock the system during breaks.
        """
        dialog = tk.Toplevel(self.master)
        dialog.title("Unlock System")
        dialog.geometry("300x150")
        dialog.transient(self.master)

        ttk.Label(dialog, text="Enter password to unlock:").pack(pady=10)
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.pack(pady=10)
    

    def update_timer_display(self):
        """
        Update the timer display with the current time.
        """
        mins, secs = divmod(self.current_time, 60)
        self.time_display.config(text=f"{mins:02d}:{secs:02d}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
    
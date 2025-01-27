import tkinter as tk
from tkinter import messagebox
from threading import Timer

WORK_DURATION = 25 * 60  # 25 minutes in seconds
SHORT_BREAK_DURATION = 5 * 60  # 5 minutes in seconds
LONG_BREAK_DURATION = 15 * 60  # 15 minutes in seconds

class PomodoroApp:
    def __init__(self, master):
        """
        Initialize the Pomodoro Timer application.
        """
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.geometry("300x300")

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
        self.timer_label = tk.Label(self.master, text="Pomodoro Timer", font=("Helvetica", 18))
        self.timer_label.pack(pady=20)

        self.time_display = tk.Label(self.master, text="00:00", font=("Helvetica", 36), fg="red")
        self.time_display.pack(pady=20)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer, width=10)
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause_timer, width=10)
        self.pause_button.pack(pady=10)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_timer, width=10)
        self.reset_button.pack(pady=10)

        self.update_timer_display()

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
            "Work": WORK_DURATION,
            "Short Break": SHORT_BREAK_DURATION,
            "Long Break": LONG_BREAK_DURATION
        }
        self.current_time = phase_durations.get(self.current_phase, WORK_DURATION)

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
        else:
            self.current_phase = "Work"

        if self.cycle_count == 4 and self.current_phase == "Long Break":
            messagebox.showinfo("Pomodoro Complete", "You've completed 4 Pomodoro cycles!")
            self.reset_timer()
        else:
            messagebox.showinfo("Timer Complete", f"{self.current_phase} phase starting!")
            self.set_timer()
            self.update_timer_display()

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
    
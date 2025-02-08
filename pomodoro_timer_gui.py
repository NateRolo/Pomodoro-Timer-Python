import tkinter as tk
from tkinter import messagebox, ttk
from pynput import keyboard, mouse

class PomodoroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.geometry("400x500")
        self.input_blocked = False

        # Toggle for enabling/disabling input blocking (default is enabled)
        self.input_blocking_enabled = True
        self.input_blocking_var = tk.BooleanVar(value=True)

        # Default timer settings (in minutes)
        self.work_duration = 25
        self.short_break_duration = 5
        self.long_break_duration = 15

        # Timer state
        self.current_time = 0
        self.current_phase = "Work"
        self.running = False
        self.cycle_count = 0

        # Setup UI components and menu
        self.setup_ui()
        self.setup_menu()

        # Global failsafe listener that is always running.
        # It listens for Ctrl+Alt+U to restore inputs.
        self.failsafe_listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+u': self.failsafe_restore
        })
        self.failsafe_listener.start()

    def setup_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
        options_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_checkbutton(
            label="Enable Input Blocking",
            variable=self.input_blocking_var,
            command=self.toggle_input_blocking
        )

    def toggle_input_blocking(self):
        self.input_blocking_enabled = self.input_blocking_var.get()
        if not self.input_blocking_enabled:
            # If the user turns off input blocking, immediately unblock any active blockers.
            self.unblock_inputs()

    def setup_ui(self):
        # --- Settings Frame ---
        settings_frame = ttk.LabelFrame(self.master, text="Timer Settings (minutes)", padding=10)
        settings_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(settings_frame, text="Work Duration:").grid(row=0, column=0, padx=5, pady=5)
        self.work_entry = ttk.Entry(settings_frame, width=10)
        self.work_entry.insert(0, str(self.work_duration))
        self.work_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Short Break:").grid(row=1, column=0, padx=5, pady=5)
        self.short_break_entry = ttk.Entry(settings_frame, width=10)
        self.short_break_entry.insert(0, str(self.short_break_duration))
        self.short_break_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Long Break:").grid(row=2, column=0, padx=5, pady=5)
        self.long_break_entry = ttk.Entry(settings_frame, width=10)
        self.long_break_entry.insert(0, str(self.long_break_duration))
        self.long_break_entry.grid(row=2, column=1, padx=5, pady=5)

        apply_button = ttk.Button(settings_frame, text="Apply Settings", command=self.apply_settings)
        apply_button.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Timer Display ---
        self.timer_label = tk.Label(self.master, text="Pomodoro Timer", font=("Helvetica", 18))
        self.timer_label.pack(pady=20)

        self.time_display = tk.Label(self.master, text="00:00", font=("Helvetica", 36), fg="red")
        self.time_display.pack(pady=20)
        
        # --- Input Status Label ---
        # This label shows a message when inputs are blocked.
        self.input_status_label = tk.Label(self.master, text="", font=("Helvetica", 12), fg="blue")
        self.input_status_label.pack(pady=5)

        # --- Control Buttons ---
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer, width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_timer, width=10)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer, width=10)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Test button (for development/testing only)
        self.test_button = ttk.Button(self.master, text="Test Input Block (5s)", command=self.test_input_blocking)
        self.test_button.pack(pady=5)

        self.update_timer_display()

    def apply_settings(self):
        try:
            new_work = int(self.work_entry.get())
            new_short = int(self.short_break_entry.get())
            new_long = int(self.long_break_entry.get())

            if any(duration <= 0 for duration in [new_work, new_short, new_long]):
                raise ValueError("Duration must be positive")

            self.work_duration = new_work
            self.short_break_duration = new_short
            self.long_break_duration = new_long

            if not self.running:
                self.reset_timer()

            messagebox.showinfo("Success", "Settings updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid positive numbers for all durations")

    def start_timer(self):
        if not self.running:
            self.running = True
            if self.current_time == 0:
                self.set_timer()
            self.run_timer()

    def pause_timer(self):
        self.running = False

    def reset_timer(self):
        self.running = False
        self.current_time = 0
        self.cycle_count = 0
        self.current_phase = "Work"
        self.unblock_inputs()
        self.update_timer_display()

    def set_timer(self):
        phase_durations = {
            "Work": self.work_duration * 60,
            "Short Break": self.short_break_duration * 60,
            "Long Break": self.long_break_duration * 60
        }
        self.current_time = phase_durations.get(self.current_phase, self.work_duration * 60)

    def run_timer(self):
        if self.running and self.current_time > 0:
            mins, secs = divmod(self.current_time, 60)
            self.time_display.config(text=f"{mins:02d}:{secs:02d}")
            self.current_time -= 1
            self.master.after(1000, self.run_timer)
        elif self.current_time == 0:
            self.switch_phase()

    def switch_phase(self):
        self.running = False
        previous_phase = self.current_phase  # Remember the phase that just ended

        if self.current_phase == "Work":
            self.cycle_count += 1
            if self.cycle_count < 4:
                self.current_phase = "Short Break"
                messagebox.showinfo("Timer Complete", "Short Break phase starting!")
                self.block_inputs()
            else:
                self.current_phase = "Long Break"
                messagebox.showinfo("Timer Complete", "Long Break phase starting!")
                self.block_inputs()
        else:
            # End of a break phase: unblock inputs first.
            self.unblock_inputs()
            if previous_phase == "Long Break":
                messagebox.showinfo("Pomodoro Complete", "You've completed 4 Pomodoro cycles!")
                self.reset_timer()
                return  # Do not restart a new work session immediately.
            else:
                self.current_phase = "Work"
                messagebox.showinfo("Timer Complete", "Work phase starting!")

        self.set_timer()
        self.update_timer_display()
        self.start_timer()

    def pause_input_blocking(self):
        """
        Temporarily stop the blocking keyboard and mouse listeners without changing the input_blocked flag.
        """
        if hasattr(self, 'block_keyboard_listener'):
            self.block_keyboard_listener.stop()
        if hasattr(self, 'mouse_listener'):
            self.mouse_listener.stop()

    def failsafe_restore(self):
        """
        Restore input immediately when failsafe combination is pressed and notify the user.
        """
        if self.input_blocked:
            self.unblock_inputs()
            messagebox.showinfo("Input Restored", "Input blocking has been disabled and inputs restored.")

    def update_timer_display(self):
        mins, secs = divmod(self.current_time, 60)
        self.time_display.config(text=f"{mins:02d}:{secs:02d}")

    def block_inputs(self):
        # Only block inputs if the toggle is enabled.
        if not self.input_blocking_enabled:
            return

        # Inform the user before blocking input.
        messagebox.showwarning(
            "Input Blocking",
            "Your keyboard and mouse inputs will be blocked during the break.\n\n"
            "To regain control, press Ctrl+Alt+U."
        )

        self.input_blocked = True
        # Update the UI status label.
        self.input_status_label.config(text="Inputs are blocked during break timer.")

        # Create a custom keyboard listener that suppresses all keys
        # but checks for the failsafe combination (Ctrl+Alt+U) manually.
        self.block_pressed_keys = set()

        def block_on_press(key):
            try:
                self.block_pressed_keys.add(key)
                ctrl_pressed = any(k in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r)
                                   for k in self.block_pressed_keys)
                alt_pressed = any(k in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r)
                                  for k in self.block_pressed_keys)
                u_pressed = any(
                    isinstance(k, keyboard.KeyCode) and k.char and k.char.lower() == 'u'
                    for k in self.block_pressed_keys
                )
                if ctrl_pressed and alt_pressed and u_pressed:
                    # Failsafe combination detected.
                    self.failsafe_restore()
                    self.block_pressed_keys.clear()
            except Exception as e:
                print("Error in block_on_press:", e)

        def block_on_release(key):
            try:
                if key in self.block_pressed_keys:
                    self.block_pressed_keys.remove(key)
            except Exception as e:
                print("Error in block_on_release:", e)

        self.block_keyboard_listener = keyboard.Listener(
            on_press=block_on_press,
            on_release=block_on_release,
            suppress=True  # Blocks all key events from reaching other apps.
        )
        self.block_keyboard_listener.start()

        # Create a mouse listener that suppresses mouse input.
        self.mouse_listener = mouse.Listener(suppress=True)
        self.mouse_listener.start()

    def unblock_inputs(self):
        self.input_blocked = False
        # Clear the UI status label.
        self.input_status_label.config(text="")
        if hasattr(self, 'block_keyboard_listener'):
            self.block_keyboard_listener.stop()
        if hasattr(self, 'mouse_listener'):
            self.mouse_listener.stop()

    def test_input_blocking(self):
        self.block_inputs()
        self.master.after(5000, self.unblock_inputs)  # Automatically unblock after 5 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()

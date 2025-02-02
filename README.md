# Pomodoro Timer

This project is a simple Pomodoro Timer application built using Python's `tkinter` library for the GUI and a command-line version for terminal use. The Pomodoro technique is a time management method that uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks.

## Features

- **Graphical User Interface (GUI):** A user-friendly interface to start, pause, and reset the timer.
- **Command-Line Interface (CLI):** A terminal-based version for users who prefer command-line interaction.
- **Customizable Settings:** Users can configure work duration, short break duration, long break duration, and the number of cycles.
- **Cycle Management:** Automatically switches between work and break phases, with notifications for phase changes.

## Getting Started

### Prerequisites

- Python 3.x
- `tkinter` library (usually included with Python installations)
- `pynput` library (can be installed from pip)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NateRolo/Pomodoro-Timer-Python.git
   cd Pomodoro-Timer-Python
   ```

2. Run the GUI version:
   ```bash
   python pomodoro_timer_gui.py
   ```

3. Run the CLI version:
   ```bash
   python pomodoro_timer.py
   ```

## Usage

### GUI Version

- **Start:** Click the "Start" button to begin the timer.
- **Pause:** Click the "Pause" button to pause the timer.
- **Reset:** Click the "Reset" button to reset the timer to the initial state.

### CLI Version

- Follow the prompts to enter your desired settings for work duration, short break, long break, and cycles.
- The timer will automatically start and switch between phases.

## Code Structure

- **`pomodoro_timer_gui.py`:** Contains the GUI implementation using `tkinter`.
  - Key classes and functions:
    - `PomodoroApp`: Main class for the GUI application.
    - `setup_ui`, `start_timer`, `pause_timer`, `reset_timer`, `switch_phase`, `update_timer_display`.

- **`pomodoro_timer.py`:** Contains the CLI implementation.
  - Key functions:
    - `get_user_settings`, `start_timer`, `pomodoro`, `main`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.

## Acknowledgments

- Inspired by the Pomodoro Technique for productivity.
- Built with Python and `tkinter`.

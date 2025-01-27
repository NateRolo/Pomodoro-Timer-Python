import time
from typing import Tuple

SECONDS_PER_MINUTE = 60

def get_user_settings() -> Tuple[int, int, int, int]:
    """
    Prompt the user to configure their Pomodoro timer settings.

    Returns:
        A tuple containing:
        - Work duration in minutes
        - Short break duration in minutes
        - Long break duration in minutes
        - Number of cycles
    """
    print("Configure your Pomodoro Timer:")
    work_minutes = int(input("Enter work duration (in minutes): "))
    short_break_minutes = int(input("Enter short break duration (in minutes): "))
    long_break_minutes = int(input("Enter long break duration (in minutes): "))
    cycles = int(input("Enter the number of cycles: "))
    return work_minutes, short_break_minutes, long_break_minutes, cycles

def start_timer(duration_minutes: int, message: str) -> None:
    """
    Run the timer for the specified duration with a countdown.

    Args:
        duration_minutes (int): Duration of the timer in minutes.
        message (str): Message displayed at the start of the timer.
    """
    print(f"\n{message} for {duration_minutes} minute(s).")
    total_seconds = duration_minutes * SECONDS_PER_MINUTE

    while total_seconds > 0:
        mins, secs = divmod(total_seconds, 60)
        time_display = f"{mins:02d}:{secs:02d}"
        print(f"\rTime left: {time_display}", end="")
        time.sleep(1)
        total_seconds -= 1

    print("\nTime's up!")

def pomodoro(work: int, short_break: int, long_break: int, cycles: int) -> None:
    """
    Execute the Pomodoro cycles based on the provided settings.

    Args:
        work (int): Work duration in minutes.
        short_break (int): Short break duration in minutes.
        long_break (int): Long break duration in minutes.
        cycles (int): Number of Pomodoro cycles.
    """
    for cycle in range(1, cycles + 1):
        print(f"\n--- Cycle {cycle}/{cycles} ---")
        start_timer(work, "Work session")

        if cycle < cycles:
            start_timer(short_break, "Short break")
        else:
            start_timer(long_break, "Long break")

def main() -> None:
    """
    Main function to start the Pomodoro timer application.
    """
    settings = get_user_settings()
    pomodoro(*settings)

if __name__ == "__main__":
    main()

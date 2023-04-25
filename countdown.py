import time
import threading
import msvcrt

def countdown():
    # Set the timer to 60 seconds
    seconds = 60
    while seconds > 0:
        # Print remaining time
        print(f"Time left: {seconds}")
        # Wait for 1 second
        time.sleep(1)
        # Decrease remaining time by 1 second
        seconds -= 1
        # Check for input
        if msvcrt.kbhit():
            # If there is input, reset the timer to 60 seconds
            msvcrt.getch()
            seconds = 60

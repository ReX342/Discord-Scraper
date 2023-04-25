import time
import threading

def countdown():
    # Set the timer to 60 seconds
    seconds = 60
    while seconds > 0:
        # Decrease remaining time by 1 second
        seconds -= 1
        # Wait for 1 second
        time.sleep(1)
    return seconds

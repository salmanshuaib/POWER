import json
import sched
import time
import winsound

# Load the JSON data from the 'time.json' file
with open('time.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize the tally for 'YES' answers and total tasks completed
yes_count = 0
total_count = 0

# Create a scheduler
s = sched.scheduler(time.time, time.sleep)

# Define a function to beep and prompt the user
def beep_and_prompt(hour, task, start_time=None, next_time=None):
    if start_time is not None and next_time is not None:
        formatted_start_time = time.strftime("%H:%M", start_time)
        formatted_next_time = time.strftime("%H:%M", next_time)  # magic
        print(f"Time to {task} (Starts at {formatted_start_time} and ends one minute prior to {formatted_next_time})")
    else:
        print(f"Time to {task}")

    winsound.Beep(500, 1000)  # Beep for 1 second (you can adjust frequency and duration)

    try:
        user_input = int(input("Did you accomplish POWER's Test? Enter 1 for YES, 0 for NO or CTRL+C to EXIT: "))
        if user_input == 1:
            global yes_count
            yes_count += 1
        global total_count
        total_count += 1
        if total_count > 0:
            print(f"Progress: Concurrent score [Tasks Completed / Total Tasks]:- {yes_count / total_count * 100:.2f}%")
    except KeyboardInterrupt:
        exit()

# Function to convert a struct_time to a 24-hour format string
def struct_time_to_24hr_str(time_struct):
    return time.strftime('%H%M', time_struct)

# Function to find the next scheduled time based on the current time
# Function to convert a struct_time to a 24-hour format string
def struct_time_to_24hr_str(time_struct):
    return time.strftime('%H%M', time_struct)

# Function to find the next scheduled time based on the current time
# Function to convert a struct_time to a 24-hour format string
def struct_time_to_24hr_str(time_struct):
    return time.strftime('%H%M', time_struct)

# Function to find the next scheduled time based on the current time
def find_next_time(current_time):
    next_time = None
    current_time_str = struct_time_to_24hr_str(current_time)
    
    for entry in data["scheduled_hours"]:
        start_time_str = entry["start_time"].replace(":", "")

        start_time = time.strptime(start_time_str, "%H%M")

        # Convert times to seconds for comparison
        current_time_seconds = current_time.tm_hour * 3600 + current_time.tm_min * 60
        start_time_seconds = start_time.tm_hour * 3600 + start_time.tm_min * 60

        # Check if the current time is before the start time of the task
        if current_time_seconds < start_time_seconds:
            next_time = start_time
            break

    return next_time

def GO():
    mono = time.localtime()
    clear_mono = time.strftime('%H%M', mono)

    Major_Only_Nukes_Oligopolies = find_next_time(mono)
    Monos = Major_Only_Nukes_Oligopolies

    if Monos is not None:
        clear_monos = struct_time_to_24hr_str(Monos)
        print(f"POWER's Test is starting at {clear_monos}. Be prepared!")
    else:
        print("No upcoming tasks found in time.json.")

try:
    GO()
    s.run()
    # Print the tally of 'YES' answers and the percentage
    if total_count > 0:
        print(f"POWER's Test completed. Total 'YES' answers: {yes_count}; out of {total_count} Tasks = Your score {yes_count / total_count * 100:.2f}%")
    else:
        print("No tasks completed yet.")

    input("Press ENTER to exit...")

except KeyboardInterrupt:
    pass

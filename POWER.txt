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
        formatted_next_time = time.strftime("%H:%M", next_time)
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

# Schedule beeping alarms for each specified time range using only start times
for i, entry in enumerate(data["scheduled_hours"]):
    hour = entry["hour"]
    task = entry["task"]
    time_range = entry["time_range"].split(" to ")

    start_time = time.strptime(time_range[0], "%H%M hours")

    # Calculate the index of the next entry
    next_index = (i + 1) % len(data["scheduled_hours"])
    next_start_time = time.strptime(data["scheduled_hours"][next_index]["time_range"].split(" to ")[0], "%H%M hours")

    current_time = time.localtime()
    current_time_seconds = current_time.tm_hour * 3600 + current_time.tm_min * 60

    start_time_seconds = start_time.tm_hour * 3600 + start_time.tm_min * 60

    if current_time_seconds >= start_time_seconds:
        delay = 86400 - (current_time_seconds - start_time_seconds)  # Delay to the next occurrence
    else:
        delay = start_time_seconds - current_time_seconds

    s.enter(delay, 1, beep_and_prompt, argument=(hour, task, start_time, next_start_time))

print("POWER's Test is starting. Be prepared!")

try:
    s.run()
except KeyboardInterrupt:
    pass

# Print the tally of 'YES' answers and the percentage
if total_count > 0:
    print(f"POWER's Test completed. Total 'YES' answers: {yes_count}; out of {total_count} Tasks = Your score {yes_count / total_count * 100:.2f}%")
else:
    print("No tasks completed.")
    
input("Press ENTER to exit...")
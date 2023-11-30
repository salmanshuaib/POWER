import json
import sched
import time
import winsound

# Load the JSON data from the 'time.json' file
with open('time.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize the tally for 'YES' answers
yes_count = 0

# Create a scheduler
s = sched.scheduler(time.time, time.sleep)

# Define a function to beep and prompt the user
def beep_and_prompt(hour, task, start_time=None):
    if start_time is not None:
        formatted_start_time = time.strftime("%H:%M", start_time)
        print(f"Time to {task} (Starts at {formatted_start_time})")
    else:
        print(f"Time to {task}")
    
    winsound.Beep(500, 1000)  # Beep for 1 second (you can adjust frequency and duration)
    
    try:
        user_input = int(input("Did you accomplish POWER's Test? Enter 1 for YES, 0 for NO or CTRL+C to EXIT: "))
        if user_input == 1:
            global yes_count
            yes_count += 1
    except KeyboardInterrupt:
        exit()

# Schedule beeping alarms for each specified time range using only start times
for entry in data["scheduled_hours"]:
    hour = entry["hour"]
    task = entry["task"]
    time_range = entry["time_range"].split(" to ")

    start_time = time.strptime(time_range[0], "%H%M hours")

    current_time = time.localtime()
    current_time_seconds = current_time.tm_hour * 3600 + current_time.tm_min * 60

    start_time_seconds = start_time.tm_hour * 3600 + start_time.tm_min * 60

    if current_time_seconds >= start_time_seconds:
        delay = 86400 - (current_time_seconds - start_time_seconds)  # Delay to the next occurrence
    else:
        delay = start_time_seconds - current_time_seconds

    if " to " in entry["time_range"]:
        s.enter(delay, 1, beep_and_prompt, argument=(hour, task, start_time))
    else:
        s.enter(delay, 1, beep_and_prompt, argument=(hour, task))

# Run the scheduler
print("POWER's Test is starting. Be prepared!")

try:
    s.run()
except KeyboardInterrupt:
    pass

# Print the tally of 'YES' answers
print(f"POWER's Test completed. Total 'YES' answers: {yes_count}")

# Avatar Of Power: TAYLOR ALISON SWIFT
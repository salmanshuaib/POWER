import json
import sched
import time
import winsound
import os

Grace = (40/100)*100  #Incase gamer starts late or the progream if offline; the initial score is 40%  [ref: Lorde:- "TEAM: We've not yet lost all our graces"]
print("POWER is a phenomenon, otherwise known as FEELING, that seeks to extricate one from the Task Precedent. Unit: Excalibur. Superunit: Watt.")
print("^")
print("^")
print("Grace == your starting mark == 40%  //You are starting out as a four-Hat officer.")
print("^")
print("^")


# Function to find the next scheduled time
def find_next_scheduled_time(data, current_time):
    current_time_seconds = current_time.tm_hour * 3600 + current_time.tm_min * 60
    closest_time = None
    closest_delay = float('inf')

    for entry in data["scheduled_hours"]:
        scheduled_time = time.strptime(entry["time_range"].split(" ")[0], "%H%M")
        scheduled_time_seconds = scheduled_time.tm_hour * 3600 + scheduled_time.tm_min * 60

        delay = (scheduled_time_seconds - current_time_seconds) % 86400
        if delay < closest_delay:
            closest_delay = delay
            closest_time = scheduled_time

    return closest_time

# Check if 'time.json' is available in the same directory
json_file_path = 'time.json'
if not os.path.exists(json_file_path):
    print("Diligent officer: POWER.exe requires time.json file in same directory.\nPlease retrieve from FlowerEconomics.com/Downloads")
    exit()

# Load the JSON data from the 'time.json' file
with open('time.json', 'r') as json_file:
    data = json.load(json_file)

# Calculate the next scheduled time
current_time = time.localtime()
next_scheduled_time = find_next_scheduled_time(data, current_time)

# Format the next scheduled time
formatted_next_time = time.strftime("%H%M hours", next_scheduled_time)

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
        print(f"\nTime to {task} (Starts at {formatted_start_time} and ends one minute prior to {formatted_next_time})")
    else:
        print(f"Time to {task}")
    
    winsound.Beep(500, 1000)  # Beep for 1 second (you can adjust frequency and duration)

    while True:
        try:
            user_input = input("Did you accomplish POWER's Test? Enter 1 for YES, 0 for NO or CTRL+C to EXIT: ")
            if user_input == "1":
                global yes_count
                yes_count += 1
                break
            elif user_input == "0":
                break
            else:
                print("Invalid input. Please enter only 1 or 0.")
        except KeyboardInterrupt:
            print("\nExiting...")
            exit()

    global total_count
    total_count += 1
    if total_count > 0:
        ConcurrentScore = ((yes_count / total_count) * 100) - Grace
        print(f"Progress: Concurrent score [Tasks Completed / Total Tasks]:- {ConcurrentScore:.2f}%")

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

# Announce the test start time
print(f"POWER's Test is starting at {formatted_next_time}. Be prepared!\nIndeed! TAYLOR SWIFT is Goddess Of Power!!\nSource: Meditation on breath.")

try:
    s.run()
except KeyboardInterrupt:
    pass

# Print the tally of 'YES' answers and the percentage
if total_count > 0:
    FinalScore = ((yes_count / total_count) * 100) - Grace
    print(f"POWER's Test completed. Total 'YES' answers: {yes_count}; out of {total_count} Tasks = Your final score {FinalScore:.2f}%")
else:
    print("No tasks completed.")
    
input("Press ENTER to exit...")

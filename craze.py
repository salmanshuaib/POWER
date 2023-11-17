import csv
import datetime
import time
import winsound  # For Windows systems, for beeping

# Function to parse the time format in Scheduler.csv and convert it to a datetime object
def parse_time(time_str):
    try:
        # Remove "hours" and spaces from the time string
        time_str = time_str.replace(" hours", "").replace(" ", "")
        time_format = "%H%M"
        if "to" in time_str:
            time_parts = time_str.split("to")
            start_time = datetime.datetime.strptime(time_parts[0], time_format)
            end_time = datetime.datetime.strptime(time_parts[1], time_format)
            return start_time, end_time
        else:
            return datetime.datetime.strptime(time_str, time_format)
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")

# Function to check if the current time matches the scheduled time
def is_time_to_execute(scheduled_time):
    current_time = datetime.datetime.now().time()
    if isinstance(scheduled_time, tuple):
        return scheduled_time[0].time() <= current_time <= scheduled_time[1].time()
    else:
        return scheduled_time.time() == current_time

# Function to read tasks from the 'tasks' file
def read_tasks():
    with open('TaskList', 'r') as tasks_file:
        tasks = tasks_file.read().splitlines()
    return tasks

# Function to count the number of YES answers
def count_yes_answers():
    yes_count = 0
    for i, task in enumerate(tasks):
        question = f"Did you complete TASK{i + 1}: 1/0?"
        user_input = input(question)
        if user_input == "1":
            yes_count += 1
    return yes_count

# Read tasks from the 'tasks' file
tasks = read_tasks()

# Read scheduled tasks from 'Scheduler.csv' and store them in a list of tuples
scheduled_tasks = []
with open('Scheduler.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        task = row['Task']
        time_range = row['Time']
        time_range = parse_time(time_range)
        scheduled_tasks.append((task, time_range))

# Check if it's time to execute each task
for task, time_range in scheduled_tasks:
    while not is_time_to_execute(time_range):
        time.sleep(22)  # Sleep for 22 seconds before checking again

    # Beep to notify the user
    winsound.Beep(1000, 1000)  # Beep for 1 second

    # Ask the question and count YES answers
    yes_count = count_yes_answers()
    print(f"Task {task}: You answered YES {yes_count} times out of {len(tasks)}")

print("All tasks completed!")
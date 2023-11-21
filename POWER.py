import os
import json
import csv
import datetime
import time
import winsound  # For Windows systems, for beeping

# Get today's date
current_date = datetime.date.today()

# Print the present day
print("Present day:", current_date)

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the path to config.json inside the "data" directory
config_file_path = os.path.join(script_dir, 'data', 'time.json')

# Load configuration from time.json
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

# Extract scheduled hours from the configuration
scheduled_hours = config.get("scheduled_hours", [])

# Extract tasks from the configuration
tasks = config.get("tasks", [])

# Function to parse the time format in Scheduler.csv and convert it to a datetime object
# (Your existing code for parsing time)

# Function to check if the current time matches the scheduled time
# (Your existing code for checking time)

ClassSize = 0  # Initialize ClassSize
Tasks = []
iteration = 0

# Check if it's time to execute each hour
def is_time_to_execute(time_range):
    current_time = datetime.datetime.now().time()
    start_time = datetime.datetime.strptime(time_range[0], "%H:%M").time()
    end_time = datetime.datetime.strptime(time_range[1], "%H:%M").time()
    return start_time <= current_time <= end_time

print("finir!")

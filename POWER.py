import csv
import datetime
import time
import winsound  # For Windows systems, for beeping

# Get today's date
current_date = datetime.date.today()

# Print the present day
print("Present day:", current_date)

# Function to parse the time format in Scheduler.csv and convert it to a datetime object
def parse_time(time_str):
    try:
        # Remove "hours" and spaces from the time string
        time_str = time_str.replace(" hours", "").replace(" ", "")
        time_format = "%H%M"
        if "to" in time_str:
            time_parts = time_str.split("to")
            start_time = datetime.datetime.combine(current_date, datetime.time(int(time_parts[0][:2]), int(time_parts[0][2:])))
            end_time = datetime.datetime.combine(current_date, datetime.time(int(time_parts[1][:2]), int(time_parts[1][2:])))
            
            # Check if the end time is before the start time, indicating a time period crossing midnight
            if end_time < start_time:
                end_time += datetime.timedelta(days=1)  # Add one day to end_time
                
            return start_time, end_time
        else:
            time_obj = datetime.datetime.combine(current_date, datetime.time(int(time_str[:2]), int(time_str[2:])))
            return time_obj
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")

# Function to check if the current time matches the scheduled time
def is_time_to_execute(scheduled_time):
    current_time = datetime.datetime.now().time()
    if isinstance(scheduled_time, tuple):
        start_time, end_time = scheduled_time
        current_datetime = datetime.datetime.now()
        return start_time.time() <= current_time <= end_time.time() and start_time <= current_datetime <= end_time
    else:
        return scheduled_time.time() == current_time

# Function to read hours from the 'hours' file
def read_hours():
    with open('Energy.txt', 'r') as hours_file:
        hours = hours_file.read().splitlines()
    return hours

# Read hours from the 'hours' file
hours = read_hours()
print("hours:", hours)  # Debugging statement

# Read scheduled hours from 'time.csv' and store them in a list of tuples
scheduled_hours = []
with open('time.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        hour = row['HOUR']  # Updated here to lowercase 'hour'
        time_range = row['TIME']
        time_range = parse_time(time_range)
        scheduled_hours.append((hour, time_range))

print("Scheduled hours:", scheduled_hours)  # Debugging statement

ClassSize = 0  # Initialize ClassSize
Tasks = []
iteration = 0
# Check if it's time to execute each hour
for hour, time_range in scheduled_hours:
    while not is_time_to_execute(time_range):
        print("Waiting for the scheduled time...")  # Debugging statement
        time.sleep(8)  # You have pressed CTRL+C to exit your Constancy routine: Pronoia - the Avatar of your Heart that perpetuates POWER into realizing its UNLIMITED Self! POWER is increasingly resident in your Third Eye as the Avatar of your Sphere Of Consciousness (Anima) and reflects the Light of your Heart into your Mind.

    # Beep to notify the user
    winsound.Beep(1000, 1000)  # Beep for 1 second
    print("Beeped!")  # Debugging statement
    Tests = input("Did you accomplish POWER's Test? Enter 1 for YES, 0 for NO or CTRL+C to EXIT: ") # You have pressed CTRL+C to exit your Constancy routine: Pronoia - the Avatar of your Heart that perpetuates POWER into realizing its UNLIMITED Self! POWER is increasingly resident in your Third Eye as the Avatar of your Sphere Of Consciousness (Anima) and reflects the Light of your Heart into your Mind. Ty: GitHub: CoPilot.
    Tasks.append(int(Tests))
    ClassSize = sum(Tasks)
    print("You have synchronized with", ClassSize, "Hours of POWER out of median: 22 Hours!")
    iteration = iteration + 1
        
print("Grade: ", (ClassSize/22)*100, "%")
print("finir!")

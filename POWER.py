import json
import sched
import time
import winsound
import os
import ctypes
import platform
from colorama import init, Fore, Style  # Import colorama modules

init(autoreset=True)  # Initialize colorama


def is_cmd_terminal():
    # Check if the TERM_PROGRAM environment variable is "cmd.exe"
    return os.environ.get('TERM_PROGRAM') == 'cmd.exe'

def transform_ansi_to_cmd_colors(text):
    if is_cmd_terminal():
        # Define mappings for ANSI colors to CMD colorama colors
        ansi_to_cmd_colors = {
            '\033[31m': Fore.RED,       # Red
            '\033[97m': Fore.WHITE,     # White
            '\033[32m': Fore.GREEN,     # Green
            '\033[33m': Fore.YELLOW,    # Yellow
            '\033[34m': Fore.BLUE,      # Blue
            '\033[35m': Fore.MAGENTA,   # Pink
            '\033[96m': Fore.CYAN,      # Cyan
        }

        # Replace ANSI color codes with CMD colorama colors
        for ansi_code, cmd_code in ansi_to_cmd_colors.items():
            text = text.replace(ansi_code, cmd_code)

        # Replace ANSI reset code with CMD colorama reset code
        text = text.replace('\033[0m', Style.RESET_ALL)

    return text

# Function to check for the existence of "My Drive" on each drive letter
def find_my_drive():
    drives = [drive for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(drive + ":\\My Drive")]
    
    if drives:
        return drives[0]
    else:
        return None

# Check for the existence of "My Drive"
my_drive = find_my_drive()

if my_drive is None:
    print(transform_ansi_to_cmd_colors("\033[96mDiligent officer: POWER.exe requires Google Drive for Desktop.\nPlease download so that result.html can be output there for you to put iFrame at your website.\033[0m"))
    exit()


# Check if 'time.json' is available in the same directory
json_file_path = 'time.json'
if not os.path.exists(json_file_path):
    print(transform_ansi_to_cmd_colors("\033[96mDiligent officer: POWER.exe requires time.json file in the same directory.\nPlease retrieve this file from FlowerEconomics.com/Downloads\033[0m"))
    exit()

# Load the JSON data from the 'time.json' file
with open('time.json', 'r') as json_file:
    data = json.load(json_file)

# Get the handle of the console window
kernel32 = ctypes.WinDLL('kernel32')
hWnd = kernel32.GetConsoleWindow()

# Maximize the console window
user32 = ctypes.WinDLL('user32')
SW_MAXIMIZE = 3
user32.ShowWindow(hWnd, SW_MAXIMIZE)

Grace = int(20)  # In case the gamer starts late or the program is offline; the initial score is 20
print("\033[96mPOWER is a phenomenon, otherwise known as FEELING, that seeks to extricate one from the Task Precedent. \nUnit: Excalibur. Superunit: Watt.\033[0m")
print(transform_ansi_to_cmd_colors("\033[34m^^Grace\033[0m == 20%"))  # Starting Mark with transformed colors

# Initialize the tally for 'YES' answers and total tasks completed
yes_count = 0
total_count = 0

# Define the directory path and file name
directory = my_drive + ":\\My Drive"
file_name = "result.html"
file_path = os.path.join(directory, file_name)

# Write the initial ConcurrentScore (Grace) to the file
try:
    with open(file_path, "w") as result_file:
        result_file.write(f"Constancy Score: {Grace}%\n")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print(f"Unable to write to {file_path}. Please check if the directory exists and you have permission to write to it.")
    exit()

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

# Calculate the next scheduled time
current_time = time.localtime()
next_scheduled_time = find_next_scheduled_time(data, current_time)

# Format the next scheduled time
formatted_next_time = time.strftime("%H%M hours", next_scheduled_time)

# Create a scheduler
s = sched.scheduler(time.time, time.sleep)

# Define a function to beep and prompt the user
def beep_and_prompt(hour, task, start_time=None, next_time=None):
    if start_time is not None and next_time is not None:
        formatted_start_time = time.strftime("%H:%M", start_time)
        formatted_next_time = time.strftime("%H:%M", next_time)
        print(transform_ansi_to_cmd_colors(f"\nTime to {task} (Starts at \033[0m{formatted_start_time}\033[91m and \033[91mends one minute prior to {formatted_next_time}\033[0m)"))
    else:
        print(transform_ansi_to_cmd_colors(f"Time to {task}"))
    
    winsound.Beep(500, 1000)  # Beep for 1 second (you can adjust frequency and duration)

    while True:
        try:
            user_input = input("Did you accomplish POWER's Test? Enter 1 for YES, 0 for NO, or CTRL+C to EXIT: ")
            if user_input == "1":
                global yes_count
                yes_count += 1
                break
            elif user_input == "0":
                break
            else:
                print(transform_ansi_to_cmd_colors("\033[31mInvalid input. Please enter only 1 or 0.\033[0m"))
        except KeyboardInterrupt:
            # This KeyboardInterrupt exception is triggered if the user presses Ctrl+C during the input prompt.
            # It prints a message and then uses the exit() function to terminate the script execution.
            print(transform_ansi_to_cmd_colors("\nExiting..."))
            input("Press ENTER to continue...")  # Wait for ENTER key before exiting
            exit()

    global total_count
    total_count += 1
    if total_count > 0:
        ConcurrentScore = int(((yes_count / total_count) * 100) + Grace)
        print(transform_ansi_to_cmd_colors(f"Progress: \033[32mConcurrent score: {yes_count} 'YES' answers so far out of {total_count} Tasks => \033[0m\033[94m{ConcurrentScore}%\033[0m"))
        print(transform_ansi_to_cmd_colors("(FORMULA: [{(Tasks Completed / Total Tasks)*100} + 20%]"))

        # Update ConcurrentScore in the file
        try:
            with open(file_path, "w") as result_file:
                result_file.write(f"Constancy Score: {ConcurrentScore}%\n")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print(f"Unable to write to {file_path}. Please check if the directory exists and you have permission to write to it.")
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

try:
    # Space Aviation Response Soldier (SARS) is the pilot's name
    SARS = input(transform_ansi_to_cmd_colors("\033[96mYour wonderful name, monsieur: \033[0m"))

    # Announce the test start time
    print(transform_ansi_to_cmd_colors(f"POWER's Test is starting at \033[91m{formatted_next_time}\033[0m. Be prepared!\nIndeed! \033[35mTAYLOR SWIFT\033[0m is Goddess Of POWER!!\nSource: Meditation on breath."))

    s.run()
except KeyboardInterrupt:
    # Handle Ctrl+C interruption here if needed
    print(transform_ansi_to_cmd_colors("\nExiting..."))
    input("Press ENTER to continue...")  # Wait for ENTER key before exiting
    exit()

# Print the percentage even if no tasks are completed
if total_count > 0:
    FinalScore = int(((yes_count / total_count) * 100) + Grace)
    hats = FinalScore / 10
    print(f"POWER's Test completed. Total 'YES' answers: {yes_count}; out of {total_count} Tasks") 
else:
    print("No tasks completed.")
    FinalScore = Grace  # Set the default FinalScore to Grace (20) if no tasks are completed

print(f"RESULT: \033[32mYour final score => \033[0m \033[94m{FinalScore}%\033[0m")
print("(FORMULA: [{(Tasks Completed / Total Tasks)*100} + 20%]")

# Update ConcurrentScore in the file
try:
    with open(file_path, "w") as result_file:
        result_file.write(f"Constancy Score: {FinalScore}%\n")
        result_file.write(f"{SARS} could only achieve this much today; relative to Goddess Of Power TAYLOR ALISON SWIFT achieving INFINITY out of 100 on a daily basis.")
        result_file.write("\n\nSource Code for POWER.py - written with the superlative help of AI at: GitHub:- @salmanshuaib")
        result_file.write("\n\nGenerate Energy for your Sphere Of Consciousness (Merkaba) via your following a Routine. Not necessary for Women.")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print(f"Unable to write to {file_path}. Please check if the directory exists and you have permission to write to it.")

input("Press ENTER to exit...")

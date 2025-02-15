import datetime
import os

current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # logs the current time 
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # get parent dir of the dir this script is in
FILE_PATH = os.path.join(BASE_DIR, "out", f"{current_time}_parking_data.csv")
SCHEDULE_PATH = os.path.join(BASE_DIR, "out", f"{current_time}_schedule.txt")

# Write to file using entries in garages list
def file_write(garages):
    global current_time
    try:
        with open(FILE_PATH, "a") as file:
            for entry in garages:
                file.write(",".join(entry) + "\n")
        print(f"Data appended to {current_time}_parking_data.csv \n")
    except IOError as e:
        print(f"Error writing to file: {e}")

def write_schedule(schedule: list):
    global current_time
    try:
        with open(SCHEDULE_PATH, "a") as file:
            file.write(f"Schedule made on {current_time}:\n")
            for task in schedule:
                file.write(task + "\n")
        print(f"Schedule file create at out/{current_time}_schedule.txt \n")
    except IOError as e:
        print(f"Error writing to file: {e}")
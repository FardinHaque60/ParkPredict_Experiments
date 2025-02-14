import datetime

current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # logs the current time 

# Write to file using entries in garages list
def file_write(garages):
    global current_time
    try:
        with open(f"out/{current_time}_parking_data.csv", "a") as file:
            for entry in garages:
                file.write(",".join(entry) + "\n")
        print(f"Data appended to {current_time}_parking_data.csv \n")
    except IOError as e:
        print(f"Error writing to file: {e}")
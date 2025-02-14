from lib import fetch_parking_data
import schedule
import random
import time
import datetime

count = 0 # count how many times task has run
req = None
user_limit = 1

def run_task():
    global count, req
    print(f"Request made on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_parking_data(req)
    count += 1 

def schedule_tasks():
    global user_limit
    schedule.clear()  # Clear previous schedules
    print(f"Task schedule everyday from 6 AM to 11 PM until {user_limit} data points are reached:")
    for hour in range(6, 24):  # 6 AM to 11 PM
        minutes = random.sample(range(0, 60), 2)  # Pick two random minutes
        for minute in minutes:
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(run_task)
            print(f"Task scheduled for {hour:02d}:{minute:02d}")

if __name__ == "__main__":
    req = input("Would you like to mock scrape the request (0), get live data once (1), or schedule the script to run (2)?: ")
    while req not in ("0", "1", "2"):
        req = input("Please enter 0, 1, or 2: ")

    if (req == "2"):
        user_limit = int(input("Please enter the number of data points to scrape: "))
        while user_limit < 1: # add protection to ensure it is a number, greater than 0
            user_limit = int(input("Please enter a number greater than 0: "))

        schedule_tasks()  # Set up the schedule initially
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            if (count >= user_limit):
                print(f"Reached user limit {user_limit}. Exiting...")
                break

    run_task()  # Run the task once if not in schedule mode
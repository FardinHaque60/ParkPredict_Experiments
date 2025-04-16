import os
import pandas as pd

TIMESTAMP_FORMAT = "%Y-%m-%d %I:%M:%S %p"

# TODO modify data load so it normalized timestamps in return dataframe
def load_data( 
        date_start=pd.to_datetime("2025-03-10 12:00:00 AM", format=TIMESTAMP_FORMAT), 
        date_end=pd.to_datetime("2025-03-14 12:00:00 AM", format=TIMESTAMP_FORMAT)
    ):
    wdir = os.path.dirname(os.path.abspath(__file__))
    data_folder_dir = wdir + "/../scrape/out/"  
    column_headers = ["timestamp", "garage name", "fullness"]

    all_data = pd.concat(
        pd.read_csv(
            os.path.join(data_folder_dir, file),
            names=column_headers, 
            header=None 
        )
        for file in os.listdir(data_folder_dir) if file.endswith(".csv")
    )

    # sort data in ascending order by timestamp
    all_data['timestamp'] = pd.to_datetime(all_data['timestamp'], format=TIMESTAMP_FORMAT)
    # apply date filtering
    all_data = all_data[(all_data['timestamp'] >= date_start) & (all_data['timestamp'] <= date_end)]
    
    all_data = all_data.sort_values(by='timestamp')
    return all_data

# takes in a date start and garage name
# loads data in 5 week slides from date_start to end of data set for specific garage
def load_week_data(
        date_start=pd.to_datetime("2025-02-17 12:00:00 AM", format=TIMESTAMP_FORMAT),
        date_end=pd.to_datetime("2025-12-31 12:00:00 AM", format=TIMESTAMP_FORMAT)
        ):
    start_dates  = []
    end_dates = []
    all_data = load_data(date_start=date_start, date_end=date_end)
    while any(all_data['timestamp'] >= date_start):
        start_dates.append(date_start)
        end_date = date_start + pd.Timedelta(days=5)
        end_dates.append(end_date)
        date_start += pd.Timedelta(days=7)
    print("Start Dates:", start_dates)
    print("End Dates:", end_dates)
    # return list
    week_data_by_garage = {
        "North Garage": [],
        "South Garage": [],
        "South Campus Garage": [],
        "West Garage": []
    }
    # add data for each week for each garage into week_data_by_garage
    for start_date, end_date in zip(start_dates, end_dates):
        week_data = all_data[(all_data['timestamp'] >= start_date) & (all_data['timestamp'] <= end_date)]
        for garage in week_data_by_garage.keys():
            garage_data = week_data[week_data['garage name'] == garage]
            if not garage_data.empty:
                week_data_by_garage[garage].append(garage_data)
                
    return week_data_by_garage    
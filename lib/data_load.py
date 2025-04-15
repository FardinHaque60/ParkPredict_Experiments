import os
import pandas as pd

def load_data(
        data_folder_dir, 
        garage='all', 
        date_start=pd.to_datetime("2025-03-10 12:00:00 AM"), 
        date_end = pd.to_datetime("2025-03-14 12:00:00 AM")
    ):
    column_headers = ["timestamp", "garage name", "fullness"]
    garage_names = ["South", "South Campus", "North", "West"]

    all_data = pd.concat(
        pd.read_csv(
            os.path.join(data_folder_dir, file),
            names=column_headers, 
            header=None 
        )
        for file in os.listdir(data_folder_dir) if file.endswith(".csv")
    )

    # sort data in ascending order by timestamp
    all_data['timestamp'] = pd.to_datetime(all_data['timestamp'], format="%Y-%m-%d %I:%M:%S %p")
    # apply filters (garage name, date range etc.)
    if (garage in garage_names):
        all_data = all_data[all_data['garage name'] == garage + " Garage"]
    all_data = all_data[(all_data['timestamp'] >= date_start) & (all_data['timestamp'] <= date_end)]
    
    all_data = all_data.sort_values(by='timestamp')
    return all_data
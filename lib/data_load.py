import os
import pandas as pd

def load_data(data_folder_dir):
    column_headers = ["timestamp", "garage name", "fullness"]
    garages = ["South", "South Campus", "North", "West"]
    garages = [s + " Garage" for s in garages]

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
    all_data = all_data.sort_values(by='timestamp')
    return all_data
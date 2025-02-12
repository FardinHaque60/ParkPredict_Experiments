import requests
import re
from bs4 import BeautifulSoup

def fetch_parking_data(request):
    # final static variables for mock or network request
    MOCK_FILE = "temp.html"
    URL = "https://sjsuparkingstatus.sjsu.edu/"
    HEADERS = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request

    response_text = None  # Initialize response_text variable

    if request == "0":
        try:
            with open(MOCK_FILE, "r", encoding="utf-8") as file:
                response_text = file.read()
        except IOError as e:
            print(f"Error reading mock data file: {e}")
            return
    elif request == "1":
        try:
            response = requests.get(URL, headers=HEADERS, verify=False)
            response_text = response.text
            response.raise_for_status()  # Raise an error for bad status codes
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return
    else: 
        print("Invalid input. Please enter 0 or 1.")
        return

    if (not response_text):
        print("Error getting response text.")
        return
    
    soup = BeautifulSoup(response_text, 'html.parser')
    
    # Extract timestamp
    timestamp_element = soup.find("p", class_="timestamp")
    timestamp = None  # Initialize timestamp variable

    if timestamp_element:
        timestamp_text = timestamp_element.get_text(strip=True, separator=" ")  # Get only text content
        timestamp = timestamp_text.replace("Last updated ", "").replace(" Refresh", "")  # Remove "Last updated" and "Refresh" 
        
        timestamp_pattern = r"^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{2}:\d{2} [APM]{2}$"

        if not re.match(timestamp_pattern, timestamp):  # Ensure expected format
            print(f"Timestamp format is incorrect: {timestamp_text}")
            timestamp = None

    # parse garage fullness data
    garages = []
    for garage in soup.find_all("h2", class_="garage__name"):
        name = garage.text.strip()

        fullness_tag = garage.find_next("span", class_="garage__fullness")  # Find fullness relative to name
        fullness = fullness_tag.text.strip().split(" ")[0]  # Get the text content of the fullness tag
        if fullness == "Full":
            fullness = "100"

        garages.append([timestamp, name, fullness])
    
    # Write to file using entries in garages list
    try:
        with open("parking_data.csv", "a") as file:
            for entry in garages:
                file.write(",".join(entry) + "\n")
        print(f"Data appended to parking_data.csv for time {timestamp} \n")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    req = input("Would you like to mock scrape the request (0) or get live data (1)?: ")
    # TODO write loop for this to run every hour between 9am - 6pm
    # TODO allow user to specify interval, time range to take data points
    fetch_parking_data(req)

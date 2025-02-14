import requests
from bs4 import BeautifulSoup
import re
from .file_writer import file_write

# global count var to timeout scraping after a while
limit = 0

# final static variables for mock or network request
MOCK_FILE = "static/temp.html"
URL = "https://sjsuparkingstatus.sjsu.edu/"
HEADERS = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request

# take in user input and based on mock, live, or schedule return response data
def splitter(user_input):
    if user_input == "0":
        print("Mocking request...")
        try:
            with open(MOCK_FILE, "r", encoding="utf-8") as file:
                return file.read()
        except IOError as e:
            print(f"Error reading mock data file: {e}")
            return
    elif user_input in ("1", "2"): # if user requests to get live data or schedule
        print("Fetching live data...")
        try:
            response = requests.get(URL, headers=HEADERS, verify=False)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return
    else: 
        print("Something went wrong.")
        return

# writes to csv based on data fetch
def fetch_parking_data(request):
    response_text = splitter(request) # take the request and fetch the data accordingly

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
    
    print(f"Website timestamp: {timestamp}.")
    for garage in garages:
        print(f"Garage: {garage[1]}, Fullness: {garage[2]}%")
    file_write(garages)  # Call file_write function to write data to file
    print("---------------------------------------")
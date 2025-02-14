import requests
import os
from bs4 import BeautifulSoup

# final static vars
MOCK_FILE = os.path.join(os.path.dirname(__file__), "temp.html")
URL = "https://sjsuparkingstatus.sjsu.edu/"
HEADERS = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request

def file_write(text):
    global MOCK_FILE
    try:
        with open(MOCK_FILE, "w", encoding="utf-8") as file:
            file.write(text.prettify())
    except IOError as e:
        print(f"Error writing to file: {e}")

def write_mock():
    try:
        response = requests.get(URL, headers=HEADERS, verify=False, timeout=10) 
        response.raise_for_status()  # Raise an error for bad status codes
        file_write(BeautifulSoup(response.text, 'html.parser'))
        print(f"Request written to {MOCK_FILE}.")
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

if __name__=="__main__":
    write_mock()
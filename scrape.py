import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums"

# Add headers to avoid being blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the webpage!")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables and select the largest one
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    # Find the table with the most rows (largest table)
    table = None
    max_rows = 0
    for t in tables:
        row_count = len(t.find_all('tr'))
        if row_count > max_rows:
            max_rows = row_count
            table = t
    
    print(f"Found largest table with {max_rows} rows")
    
    if table:
        # Extract table headers
        headers = []
        for th in table.find_all('th'):
            headers.append(th.text.strip())
        
        print(f"\nTable Headers: {headers}\n")
        
        # Extract table rows
        rows = []
        for tr in table.find_all('tr')[1:]:  # Skip the header row
            cells = tr.find_all(['td', 'th'])
            row_data = [cell.text.strip() for cell in cells]
            if row_data:  # Only add non-empty rows
                rows.append(row_data)
        
        # Display the data
        print(f"Found {len(rows)} stadiums\n")
        
        # Create a pandas DataFrame for better visualization
        df = pd.DataFrame(rows, columns=headers[:len(rows[0])] if rows else headers)
        print(df)
        
        # Optionally, save to CSV
        df.to_csv('nfl_stadiums.csv', index=False)
        print("\nData saved to 'nfl_stadiums.csv'")
        
    else:
        print("Could not find the table on the page")
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")

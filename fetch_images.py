import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums"

# Add headers to avoid being blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

print("Fetching Wikipedia page...")

if response.status_code == 200:
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
        # Extract image URLs from the table
        stadium_images = {}
        
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            
            if len(cells) > 0:
                # First cell should contain the image
                img_cell = cells[0]
                img_tag = img_cell.find('img')
                
                # Second cell should contain the stadium name
                if len(cells) > 1:
                    name_cell = cells[1]
                    stadium_name = name_cell.text.strip()
                    
                    # Extract image URL
                    if img_tag and img_tag.get('src'):
                        img_url = img_tag['src']
                        # Convert relative URLs to absolute URLs
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = 'https://en.wikipedia.org' + img_url
                        
                        stadium_images[stadium_name] = img_url
                        print(f"✓ {stadium_name}")
                    else:
                        print(f"✗ {stadium_name} - no image found")
        
        print(f"\n{'='*60}")
        print(f"Extracted {len(stadium_images)} stadium images")
        print(f"{'='*60}")
        
        # Connect to the database
        conn = sqlite3.connect('stadiums.db')
        df = pd.read_sql_query("SELECT * FROM Stadiums", conn)
        
        # Update image URLs
        print("\nUpdating database with extracted images...")
        for idx, row in df.iterrows():
            stadium_name = row['Name']
            if stadium_name in stadium_images:
                df.at[idx, 'Image'] = stadium_images[stadium_name]
                print(f"✓ Updated {stadium_name}")
            else:
                print(f"✗ No match for {stadium_name}")
        
        # Write back to database
        df.to_sql('Stadiums', conn, if_exists='replace', index=False)
        print(f"\n✓ Database updated with Wikipedia images")
        
        # Verify
        verify_df = pd.read_sql_query("SELECT Name, Image FROM Stadiums WHERE Image IS NOT NULL LIMIT 3", conn)
        print("\nVerification - Sample images:")
        print(verify_df)
        
        conn.close()

else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")

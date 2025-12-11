import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

# Initialize the geocoder
geolocator = Nominatim(user_agent="nfl_stadium_locator")

def get_coordinates(location, retry=3):
    """
    Get latitude and longitude for a given location string.
    Includes retry logic for handling timeouts.
    """
    try:
        time.sleep(1)  # Be respectful to the geocoding service
        loc = geolocator.geocode(location)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None, None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        if retry > 0:
            print(f"Timeout or error, retrying... ({retry} attempts left)")
            time.sleep(2)
            return get_coordinates(location, retry - 1)
        else:
            print(f"Failed to geocode: {location}")
            return None, None

# Connect to the database
conn = sqlite3.connect('stadiums.db')

# Read the Stadiums table
df = pd.read_sql_query("SELECT * FROM Stadiums", conn)

print(f"Loaded {len(df)} stadiums from database")
print("\nSample locations:")
print(df[['Name', 'Location']].head())

# Add new columns for coordinates
df['Latitude'] = None
df['Longitude'] = None

# Geocode each stadium based on its location
print("\nGeocoding stadiums...")
for idx, row in df.iterrows():
    location = row['Location']
    print(f"Processing {idx + 1}/{len(df)}: {row['Name']} - {location}")
    
    lat, lon = get_coordinates(location)
    df.at[idx, 'Latitude'] = lat
    df.at[idx, 'Longitude'] = lon
    
    if lat and lon:
        print(f"  ✓ Coordinates: ({lat:.4f}, {lon:.4f})")
    else:
        print(f"  ✗ Could not geocode")

# Display summary
successful = df['Latitude'].notna().sum()
print(f"\n{'='*60}")
print(f"Geocoding complete: {successful}/{len(df)} stadiums successfully geocoded")
print(f"{'='*60}")

# Show sample results
print("\nSample results:")
print(df[['Name', 'Location', 'Latitude', 'Longitude']].head(10))

# Write the updated DataFrame back to the database
df.to_sql('Stadiums', conn, if_exists='replace', index=False)
print(f"\n✓ Updated Stadiums table with Latitude and Longitude columns")

# Verify the update
verify_df = pd.read_sql_query("SELECT Name, Location, Latitude, Longitude FROM Stadiums LIMIT 5", conn)
print("\nVerification - First 5 rows from updated database:")
print(verify_df)

# Close the connection
conn.close()
print("\nDatabase connection closed.")

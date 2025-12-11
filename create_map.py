import pandas as pd
import sqlite3
import folium
from folium import Marker, Popup

# Connect to the database
conn = sqlite3.connect('stadiums.db')

# Read the Stadiums table
df = pd.read_sql_query("SELECT * FROM Stadiums", conn)

print(f"Loaded {len(df)} stadiums from database")

# Close the database connection
conn.close()

# Create a map centered on the United States
# Use the mean of all stadium coordinates as the center
center_lat = df['Latitude'].mean()
center_lon = df['Longitude'].mean()

print(f"\nMap center: ({center_lat:.4f}, {center_lon:.4f})")

# Create the map
stadium_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=4,
    tiles='OpenStreetMap'
)

# Add markers for each stadium
print("\nAdding markers to map...")
for idx, row in df.iterrows():
    # Skip rows without coordinates
    if pd.isna(row['Latitude']) or pd.isna(row['Longitude']):
        print(f"Skipping {row['Name']} - missing coordinates")
        continue
    
    # Create popup HTML with stadium information
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; width: 300px;">
        <h4 style="margin-bottom: 10px; color: #2c3e50;">{row['Name']}</h4>
        <table style="width: 100%; font-size: 12px; margin-bottom: 10px;">
            <tr>
                <td style="font-weight: bold; padding: 3px;">Team:</td>
                <td style="padding: 3px;">{row['Team(s)']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; padding: 3px;">Location:</td>
                <td style="padding: 3px;">{row['Location']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; padding: 3px;">Capacity:</td>
                <td style="padding: 3px;">{row['Capacity']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; padding: 3px;">Surface:</td>
                <td style="padding: 3px;">{row['Surface']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; padding: 3px;">Roof:</td>
                <td style="padding: 3px;">{row['Roof']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; padding: 3px;">Opened:</td>
                <td style="padding: 3px;">{row['Opened']}</td>
            </tr>
        </table>"""
    
    # Add image if available
    if pd.notna(row['Image']):
        popup_html += f"""
        <img src="{row['Image']}" alt="{row['Name']}" style="width: 280px; height: auto; border-radius: 5px; margin-top: 10px;">
    """
    
    popup_html += """
    </div>
    """
    
    # Add marker to map
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_html, max_width=350),
        tooltip=row['Name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(stadium_map)
    
    print(f"  ✓ Added marker for {row['Name']}")

# Save the map to an HTML file
output_file = 'stadiums_map.html'
stadium_map.save(output_file)

print(f"\n{'='*60}")
print(f"✓ Map successfully created and saved as '{output_file}'")
print(f"  Total markers: {len(df)}")
print(f"{'='*60}")
print(f"\nOpen '{output_file}' in a web browser to view the interactive map!")

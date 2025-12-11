import pandas as pd
import sqlite3

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('nfl_stadiums.csv')

# Display the DataFrame info
print("DataFrame Info:")
print(df.info())
print(f"\nLoaded {len(df)} rows from nfl_stadiums.csv")

# Create a connection to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('stadiums.db')

# Write the DataFrame to SQLite database
# if_exists='replace' will drop the table if it exists and recreate it
df.to_sql('Stadiums', conn, if_exists='replace', index=False)

print(f"\nSuccessfully wrote {len(df)} rows to 'Stadiums' table in stadiums.db")

# Verify the data was written correctly
query_result = pd.read_sql_query("SELECT * FROM Stadiums LIMIT 5", conn)
print("\nFirst 5 rows from database:")
print(query_result)

# Close the connection
conn.close()
print("\nDatabase connection closed.")

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Connect to the database
conn = sqlite3.connect('stadiums.db')

# Get column names
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(Stadiums)")
columns_info = cursor.fetchall()

# Extract column names and types
column_names = [col[1] for col in columns_info]
column_types = [col[2] for col in columns_info]

conn.close()

# Create a dataframe for display
df = pd.DataFrame({
    'Column Name': column_names,
    'Data Type': column_types
})

print("Stadiums Table Variables:")
print("=" * 50)
print(df.to_string(index=False))
print("=" * 50)
print(f"\nTotal Variables: {len(column_names)}")

# Create a visual chart
fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('tight')
ax.axis('off')

# Create table
table = ax.table(cellText=df.values, 
                colLabels=df.columns,
                cellLoc='left',
                loc='center',
                colWidths=[0.6, 0.4])

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2)

# Header styling
for i in range(len(df.columns)):
    cell = table[(0, i)]
    cell.set_facecolor('#4472C4')
    cell.set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(1, len(df) + 1):
    for j in range(len(df.columns)):
        cell = table[(i, j)]
        if i % 2 == 0:
            cell.set_facecolor('#E7E6E6')
        else:
            cell.set_facecolor('#FFFFFF')

plt.title('NFL Stadiums Database - Column Names', fontsize=16, weight='bold', pad=20)
plt.savefig('variables_chart.png', dpi=300, bbox_inches='tight')
print("\n✓ Chart saved as 'variables_chart.png'")
plt.show()

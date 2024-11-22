import sqlite3

# Source database (from where data is copied)
source_db = "D:\\telegramBot\\apps\\apps\\Tele-Bot-Api-Py\\app\\full_bots.db"
# Destination database (to where data is copied)
destination_db = "D:\\telegramBot\\apps\\apps\\Tele-Bot-Api-Py\\app\\bots.db"

# Connect to both databases
source_conn = sqlite3.connect(source_db)
destination_conn = sqlite3.connect(destination_db)

try:
    # Create cursors for both databases
    source_cursor = source_conn.cursor()
    destination_cursor = destination_conn.cursor()

    # Fetch data from the source database
    source_cursor.execute("SELECT * FROM bots")  # Replace 'table_name' with your actual table
    data = source_cursor.fetchall()

    for raw in data:
        # Insert data into the destination database
        # Adjust column names and table structure as needed
        destination_cursor.execute(
            "INSERT INTO bots (session, phone,created_at) VALUES (?, ?, ?)",  # Adjust the query
            (raw[1],raw[2],raw[4])
        )
        
    # Commit the changes
    destination_conn.commit()
    print("Data successfully copied!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close connections
    source_conn.close()
    destination_conn.close()

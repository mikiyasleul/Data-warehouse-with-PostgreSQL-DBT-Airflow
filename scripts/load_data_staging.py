import pandas as pd
import psycopg2

# Define your database connection parameters
db_name = 'staging_data_warehouse'
db_user = 'postgres'
db_password = '0933624757'
db_host = 'localhost'
db_port = '5432'

# Define the path to your data file
data_file_path = r'C:\Users\o876\Desktop\City traffic data.csv'

# Database connection using psycopg2
def db_connection_psycopg():
    pgconn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    return pgconn

# Read the data file
data = pd.read_csv(data_file_path)

# Perform data transformations or manipulations if needed
# For example, you can clean or preprocess the data, apply filters, etc.

# Load the data into the database
def load_data_to_db():
    conn = db_connection_psycopg()
    cur = conn.cursor()

    # Create the target table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS datawarehouse_table (
        track_id INTEGER,
        type VARCHAR(255),
        traveled_d FLOAT,
        avg_speed FLOAT,
        lat FLOAT,
        lon FLOAT,
        speed FLOAT,
        lon_acc FLOAT,
        lat_acc FLOAT,
        time TIMESTAMP
    )
    """
    cur.execute(create_table_query)
    
    # Insert the data into the table
    for index, row in data.iterrows():
        insert_query = """
        INSERT INTO datawarehouse_table (track_id, type, traveled_d, avg_speed, lat, lon, speed, lon_acc, lat_acc, time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            row['track_id'],
            row['type'],
            row['traveled_d'],
            row['avg_speed'],
            row['lat'],
            row['lon'],
            row['speed'],
            row['lon_acc'],
            row['lat_acc'],
            row['time']
        )
        cur.execute(insert_query, values)

    # Commit the changes and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()

load_data_to_db()

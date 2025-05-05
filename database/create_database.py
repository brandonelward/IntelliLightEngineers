import sqlite3
import pandas as pd
import os



DATABASE_NAME = 'simulation_data.db'


def create_database_and_table():
    """Creates the database and the traffic_data table if they don't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS traffic_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_name TEXT UNIQUE,
            step INTEGER,
            vehicle_id TEXT,
            speed REAL,
            acceleration REAL,
            distance_traveled REAL,
            date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database '{DATABASE_NAME}' and table 'traffic_data' created (if they didn't exist).")

 
def save_simulation_data_to_db(csv_filepath, simulation_name):
    """
    Reads simulation data from a CSV file and saves it to the database.

    Args:
        csv_filepath (str): The path to the CSV file containing the simulation data.
        simulation_name (str): A unique name for this simulation run.
    """
    try:
        df = pd.read_csv(csv_filepath)
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        for index, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT INTO traffic_data (simulation_name, step, vehicle_id, speed, acceleration, distance_traveled)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (simulation_name, row['step'], row['vehicle_id'], row['speed'], row['acceleration'], row['distance_traveled']))
            except sqlite3.IntegrityError:
                print(f"Warning: Simulation with name '{simulation_name}' already exists in the database. Skipping insertion.")
                conn.rollback()
                conn.close()
                return

        conn.commit()
        conn.close()
        print(f"Data from '{csv_filepath}' saved to the database as '{simulation_name}'.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_filepath}'.")
    except KeyError as e:
        print(f"Error: Column '{e}' not found in the CSV file. Please ensure the CSV has the expected columns.")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


def fetch_all_simulations():
    """Fetches a list of all unique simulation names from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT simulation_name FROM traffic_data")
    simulations = [row[0] for row in cursor.fetchall()]
    conn.close()
    return simulations


def fetch_simulation_data(simulation_name):
    """Fetches all data for a specific simulation."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM traffic_data WHERE simulation_name=?", (simulation_name,))
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return pd.DataFrame(data, columns=columns)

def fetch_simulations_by_date_range(start_date, end_date):
    """Fetches simulations recorded within a specific date range (YYYY-MM-DD)."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT simulation_name, date_recorded FROM traffic_data WHERE date(date_recorded) BETWEEN ? AND ?", (start_date, end_date,))
    simulations = [(row[0], row[1]) for row in cursor.fetchall()]
    conn.close()
    return simulations


if __name__ == "__main__":
    create_database_and_table()

    
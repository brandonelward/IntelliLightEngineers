import sqlite3
import pandas as pd
import os



DATABASE_NAME = 'simulation_data.db'


def initialise_database():
    """Ensures the database file exists."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.close()
    print(f"Database file '{DATABASE_NAME}' initialised (or already exists).")


def save_dataframe_to_new_table(df_to_save, table_name):
    """
    Saves a Pandas DataFrame to a new table in the database.
    The table name will be the provided 'table_name' (which is the simulation name).
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        # Check if a table with this name already exists
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone():
            print(f"Warning (DB): Table '{table_name}' already exists. Data will NOT be overwritten or appended.")
            conn.close()
            return

        # Use pandas to_sql to create the table and insert data
        # 'if_exists'='fail' ensures it won't overwrite if the table exists
        # 'index=False' prevents pandas from writing its DataFrame index as a column
        df_to_save.to_sql(table_name, conn, if_exists='fail', index=False)

        conn.close()
        print(f"(DB) Data saved to new table '{table_name}' in '{DATABASE_NAME}'.")

    except ValueError as ve: # to_sql raises ValueError if if_exists='fail' and table exists
        print(f"Error (DB Save): Table '{table_name}' already exists and could not be created/saved: {ve}")
    except Exception as e:
        print(f"Error (General DB Save): An error occurred while saving data to table '{table_name}': {e}")




def save_simulation_data_to_db(df_to_save, simulation_name):
    """
    Saves a Pandas DataFrame of simulation data to the database.

    Args:
        df_to_save (pd.DataFrame): The DataFrame containing the simulation data.
        simulation_name (str): A unique name for this simulation run.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        # Print the absolute path of the database for debugging
        print(f"DEBUG: Saving data to database at: {os.path.abspath(DATABASE_NAME)}")
        cursor = conn.cursor()


        # Check if a simulation with this name already exists
        cursor.execute("SELECT COUNT(*) FROM traffic_data WHERE simulation_name = ?", (simulation_name,))
        if cursor.fetchone()[0] > 0:
            print(f"Warning (DB): Simulation with name '{simulation_name}' already exists. Skipping insertion.")
            conn.close()
            return

        # Prepare data for insertion
        # Ensure column order matches the CREATE TABLE statement
        for index, row in df_to_save.iterrows():
            try:
                cursor.execute('''
                    INSERT INTO traffic_data (
                        simulation_name, step, vehicle_id, speed, acceleration,
                        distance_traveled, position_x, position_y, co2_emissions,
                        noise_emissions, waiting_time, lane_id, emission_class, time_loss
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    simulation_name,
                    row['step'],
                    row['vehicle_id'],
                    row['speed'],
                    row['acceleration'],
                    row['distance_traveled'],
                    row['position_x'],
                    row['position_y'],
                    row['co2_emissions'],
                    row['noise_emissions'],
                    row['waiting_time'],
                    row['lane_id'],
                    row['emission_class'],
                    row['time_loss']
                ))
            except sqlite3.Error as db_err:
                print(f"Error (DB) during row insertion for vehicle {row.get('vehicle_id', 'N/A')} at step {row.get('step', 'N/A')}: {db_err}")
                conn.rollback()
                conn.close()
                return
            except KeyError as ke:
                print(f"Error (CSV Column Missing): Column '{ke}' not found in DataFrame. Please check your CSV column names.")
                conn.rollback()
                conn.close()
                return

        conn.commit()
        conn.close()
        print(f"(DB) Data for '{simulation_name}' saved to the database.")

    except Exception as e:
        print(f"Error (General DB Save): An error occurred while saving data: {e}")


def fetch_all_simulations():
    """Fetches a list of all unique simulation names from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT simulation_name FROM traffic_data")
    simulations = [row[0] for row in cursor.fetchall()]
    conn.close()
    return simulations

def fetch_simulation_data_from_table(table_name):
    """Fetches all data from a specific simulation table."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except pd.io.sql.DatabaseError as e:
        print(f"Error: Table '{table_name}' not found or could not be read: {e}")
        return pd.DataFrame() # Return empty DataFrame on error
    except Exception as e:
        print(f"An unexpected error occurred fetching data from '{table_name}': {e}")
        return pd.DataFrame()


def get_all_simulation_table_names():
    """Fetches a list of all table names in the database (which represent simulation runs)."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Select names of all tables, excluding internal SQLite tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    table_names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return table_names


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
    initialise_database()
    print("Database functions for dynamic tables ready.")
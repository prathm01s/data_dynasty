"""
Phase 4: Main Application Interface (main_app.py)
This script provides a clean, professional command-line interface (CLI) 
to interact with the 'chimera_db' database.
"""

import sys
import pymysql
from getpass import getpass

# --- Database Connection ---

def get_db_connection(db_user, db_pass, db_host, db_name):
    """
    Establishes a connection to the MySQL database.
    """
    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        print("[SUCCESS] Database connection established.")
        return connection
    except pymysql.Error as e:
        print(f"\n[ERROR] Failed to connect to MySQL Database: {e}", file=sys.stderr)
        return None

# --- READ (QUERY) OPERATIONS ---

def find_personnel_by_rank(connection):
    """
    READ 1: Finds all personnel matching a user-specified rank.
    """
    print("\n--- 1. Find Personnel by Rank ---")
    try:
        valid_ranks = ('Boss', 'Grunt', 'Scientist')
        rank = input("  > Enter Rank (Boss, Grunt, Scientist): ").strip().capitalize()

        if rank not in valid_ranks:
            print(f"\n[ERROR] Invalid rank '{rank}'. Please choose from {valid_ranks}.")
            return

        with connection.cursor() as cursor:
            sql = "SELECT Personnel_ID, FName, LName, StartDate FROM PERSONNEL WHERE Rank = %s ORDER BY LName"
            cursor.execute(sql, (rank,))
            results = cursor.fetchall()

            if not results:
                print(f"\n[INFO] No personnel found with rank '{rank}'.")
            else:
                print(f"\nFound {len(results)} personnel with rank '{rank}':")
                print("  " + "-"*52)
                print(f"  {'ID':<5} | {'Name':<25} | {'Start Date':<15}")
                print("  " + "-"*52)
                for row in results:
                    full_name = f"{row['FName']} {row['LName']}"
                    print(f"  {row['Personnel_ID']:<5} | {full_name:<25} | {str(row['StartDate']):<15}")
                print("  " + "-"*52)

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)

def find_grunt_pokemon(connection):
    """
    READ 2: Lists all Pokémon owned by a specific Grunt (via JOIN).
    """
    print("\n--- 2. Find a Grunt's Pokémon ---")
    try:
        name = input("  > Enter Grunt's First Name: ").strip().capitalize()

        with connection.cursor() as cursor:
            sql = """
                SELECT p.Name, p.HP, p.Attack, p.Defense
                FROM POKEMON p
                JOIN OWNERSHIP o ON p.Pokemon_ID = o.Pokemon_ID
                JOIN PERSONNEL per ON o.Personnel_ID = per.Personnel_ID
                WHERE per.FName = %s AND per.Rank = 'Grunt'
            """
            cursor.execute(sql, (name,))
            results = cursor.fetchall()

            if not results:
                print(f"\n[INFO] No Pokémon found for a Grunt named '{name}'.")
            else:
                print(f"\nPokémon owned by Grunt {name}:")
                for row in results:
                    print(f"  - {row['Name']:<18} (HP: {row['HP']:<3}, Atk: {row['Attack']:<3}, Def: {row['Defense']:<3})")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)

def show_active_missions(connection):
    """
    READ 3: Shows all 'Active' missions and their assigned personnel (multi-JOIN).
    """
    print("\n--- 3. Show Active Missions and Assignments ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT m.Mission_ID, m.Objective, p.FName, p.LName, ma.Role
                FROM MISSION m
                JOIN MISSION_ASSIGNMENT ma ON m.Mission_ID = ma.Mission_ID
                JOIN PERSONNEL p ON ma.Personnel_ID = p.Personnel_ID
                WHERE m.Status = 'Active'
                ORDER BY m.Mission_ID, p.LName
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                print("\n[INFO] No active missions with assigned personnel found.")
            else:
                print("\nCurrent Active Missions:")
                current_mission_id = None
                for row in results:
                    if row['Mission_ID'] != current_mission_id:
                        print(f"\n  [Mission {row['Mission_ID']}] {row['Objective']}")
                        current_mission_id = row['Mission_ID']
                    print(f"    - {row['FName']} {row['LName']} (Role: {row['Role']})")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)

def find_project_scientists(connection):
    """
    READ 4: Finds all scientists working on a specific research project (using LIKE).
    """
    print("\n--- 4. Find Scientists on a Project ---")
    try:
        search_title = input("  > Enter a keyword from the project title (e.g., 'Apex'): ").strip()
        
        with connection.cursor() as cursor:
            sql = """
                SELECT p.Title, p.Status, s.FName, s.LName, sc.Specialization
                FROM RESEARCH_PROJECT p
                JOIN SCIENTIST sc ON p.Project_ID = sc.Project_ID
                JOIN PERSONNEL s ON sc.Scientist_Personnel_ID = s.Personnel_ID
                WHERE p.Title LIKE %s
                ORDER BY p.Title, s.LName
            """
            cursor.execute(sql, (f"%{search_title}%",))
            results = cursor.fetchall()

            if not results:
                print(f"\n[INFO] No projects found matching '{search_title}'.")
            else:
                print(f"\nScientists on projects matching '{search_title}':")
                current_project = None
                for row in results:
                    if row['Title'] != current_project:
                        print(f"\n  [Project] {row['Title']} (Status: {row['Status']})")
                        current_project = row['Title']
                    print(f"    - Dr. {row['FName']} {row['LName']} ({row['Specialization']})")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)

def calculate_pending_mission_risk(connection):
    """
    READ 5: Calculates total notoriety of trainers targeted in 'Pending' missions (Aggregate).
    """
    print("\n--- 5. Calculate Pending Mission Risk ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT COUNT(m.Mission_ID) as Mission_Count, SUM(t.NotorietyScore) AS Total_Risk
                FROM MISSION m
                JOIN TRAINER t ON t.Trainer_ID = m.Target_Trainer_ID
                WHERE m.Status = 'Pending' AND t.NotorietyScore > 0
            """
            cursor.execute(sql)
            result = cursor.fetchone()

            if not result or result['Total_Risk'] is None:
                print("\n[INFO] No pending missions are targeting trainers with a notoriety score.")
            else:
                print(f"\n[RESULT] Total Notoriety Risk for {result['Mission_Count']} pending mission(s): {result['Total_Risk']}")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)


# --- WRITE (C/U/D) OPERATIONS ---

def add_new_asset(connection):
    """
    WRITE 1 (INSERT): Adds a new asset to the ASSET table.
    """
    print("\n--- 6. (INSERT) Add New Asset ---")
    try:
        asset_code = input("  > Enter Asset Code (e.g., 'VEH-003'): ").strip().upper()
        asset_type = input("  > Enter Asset Type (e.g., 'Jeep'): ").strip()
        value = float(input("  > Enter Value Estimate (e.g., 45000.00): "))

        if not asset_code or not asset_type or value < 0:
            print("\n[ERROR] Asset Code, Type, and a non-negative Value are required.")
            return

        with connection.cursor() as cursor:
            sql = "INSERT INTO ASSET (Asset_Code, Asset_Type, Value_Estimate) VALUES (%s, %s, %s)"
            cursor.execute(sql, (asset_code, asset_type, value))
        
        connection.commit()
        print(f"\n[SUCCESS] Asset '{asset_code}' added to the database.")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during insert: {e}", file=sys.stderr)
        connection.rollback()
    except ValueError:
        print("\n[ERROR] Invalid value. Please enter a number for the estimate.")
        connection.rollback()

def update_mission_status(connection):
    """
    WRITE 2 (UPDATE): Updates the status of an existing mission.
    """
    print("\n--- 7. (UPDATE) Update Mission Status ---")
    try:
        mission_id = int(input("  > Enter Mission ID to update: "))
        
        valid_statuses = ('Pending', 'Active', 'Completed', 'Failed', 'Aborted')
        print(f"  Valid statuses are: {valid_statuses}")
        new_status = input("  > Enter new status: ").strip().capitalize()

        if new_status not in valid_statuses:
            print(f"\n[ERROR] Invalid status '{new_status}'.")
            return

        # If mission is ending, set EndDate.
        end_date_sql = ", EndDate = CURDATE()" if new_status in ('Completed', 'Failed', 'Aborted') else ""
        
        with connection.cursor() as cursor:
            # Note: f-string is safe here *only* because we are not using user input in it.
            # The user input (new_status, mission_id) is still parameterized.
            sql = f"UPDATE MISSION SET Status = %s{end_date_sql} WHERE Mission_ID = %s"
            rows_affected = cursor.execute(sql, (new_status, mission_id))

        if rows_affected == 0:
            print(f"\n[INFO] No mission found with ID {mission_id}. No updates made.")
        else:
            connection.commit()
            print(f"\n[SUCCESS] Mission {mission_id} status updated to '{new_status}'.")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during update: {e}", file=sys.stderr)
        connection.rollback()
    except ValueError:
        print("\n[ERROR] Invalid Mission ID. Please enter a number.")
        connection.rollback()

def remove_asset_from_mission(connection):
    """
    WRITE 3 (DELETE): Removes an asset's assignment from a mission.
    """
    print("\n--- 8. (DELETE) Remove Asset from Mission ---")
    try:
        mission_id = int(input("  > Enter Mission ID: "))
        asset_code = input("  > Enter Asset Code to remove (e.g., 'CH-HELI-01'): ").strip().upper()

        if not asset_code:
            print("\n[ERROR] Asset Code cannot be empty.")
            return

        with connection.cursor() as cursor:
            sql = "DELETE FROM MISSION_ASSETS WHERE Mission_ID = %s AND Asset_Code = %s"
            rows_affected = cursor.execute(sql, (mission_id, asset_code))

        if rows_affected == 0:
            print(f"\n[INFO] No asset '{asset_code}' found assigned to mission {mission_id}. No changes made.")
        else:
            connection.commit()
            print(f"\n[SUCCESS] Asset '{asset_code}' removed from mission {mission_id}.")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during delete: {e}", file=sys.stderr)
        connection.rollback()
    except ValueError:
        print("\n[ERROR] Invalid Mission ID. Please enter a number.")
        connection.rollback()


# --- Main Application Loop ---

def main_cli(connection):
    """
    The main command-line interface loop.
    """
    try:
        while True:
            print("\n" + "="*42)
            print("    C H I M E R A  DB  I N T E R F A C E")
            print("="*42)
            print(" [READ OPERATIONS]")
            print("   1. Find Personnel by Rank")
            print("   2. Find a Grunt's Pokémon")
            print("   3. Show Active Missions and Assignments")
            print("   4. Find Scientists on a Project")
            print("   5. Calculate Pending Mission Risk")
            print("\n [WRITE OPERATIONS]")
            print("   6. (INSERT) Add New Asset")
            print("   7. (UPDATE) Update Mission Status")
            print("   8. (DELETE) Remove Asset from Mission")
            print("\n [SYSTEM]")
            print("   q. Quit")
            print("="*42)
            
            choice = input("  > Enter choice: ").strip().lower()

            if choice == '1':
                find_personnel_by_rank(connection)
            elif choice == '2':
                find_grunt_pokemon(connection)
            elif choice == '3':
                show_active_missions(connection)
            elif choice == '4':
                find_project_scientists(connection)
            elif choice == '5':
                calculate_pending_mission_risk(connection)
            elif choice == '6':
                add_new_asset(connection)
            elif choice == '7':
                update_mission_status(connection)
            elif choice == '8':
                remove_asset_from_mission(connection)
            elif choice == 'q':
                print("\n[INFO] Exiting application...")
                break
            else:
                print("\n[ERROR] Invalid choice. Please try again.")
    
    finally:
        if connection:
            connection.close()
            print("[INFO] Database connection closed.")


# --- Application Entry Point ---

if __name__ == "__main__":
    """
    Main entry point for the application.
    """
    DB_HOST = 'localhost'
    DB_NAME = 'chimera_db'
    
    print("--- Chimera Database Login ---")
    DB_USER = input("  > Username: ").strip()
    DB_PASS = getpass("  > Password: ")

    db_conn = get_db_connection(DB_USER, DB_PASS, DB_HOST, DB_NAME)

    if db_conn:
        main_cli(db_conn)
    else:
        print("\n[FATAL] Application cannot start without a database connection.")
        sys.exit(1)
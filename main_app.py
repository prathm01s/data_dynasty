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

def find_top_performing_personnel(connection):
    """
    READ 6: Find personnel who have participated in the most 'Completed' missions.
    Uses JOIN, GROUP BY, ORDER BY, LIMIT.
    """
    print("\n--- 6. Top Performing Personnel ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT p.FName, p.LName, COUNT(ma.Mission_ID) as Mission_Count
                FROM PERSONNEL p
                JOIN MISSION_ASSIGNMENT ma ON p.Personnel_ID = ma.Personnel_ID
                JOIN MISSION m ON ma.Mission_ID = m.Mission_ID
                WHERE m.Status = 'Completed'
                GROUP BY p.Personnel_ID, p.FName, p.LName
                ORDER BY Mission_Count DESC
                LIMIT 5
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                print("\n[INFO] No completed missions found.")
            else:
                print("\nTop 5 Personnel by Completed Missions:")
                print(f"  {'Name':<30} | {'Missions Completed':<20}")
                print("  " + "-"*53)
                for row in results:
                    full_name = f"{row['FName']} {row['LName']}"
                    print(f"  {full_name:<30} | {row['Mission_Count']:<20}")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)

def list_unassigned_assets(connection):
    """
    READ 7: List assets that are not currently assigned to any active mission.
    Uses Nested Query (NOT IN).
    """
    print("\n--- 7. List Unassigned Assets ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT a.Asset_Code, a.Asset_Type, a.Value_Estimate
                FROM ASSET a
                WHERE a.Asset_Code NOT IN (
                    SELECT ma.Asset_Code 
                    FROM MISSION_ASSETS ma
                    JOIN MISSION m ON ma.Mission_ID = m.Mission_ID
                    WHERE m.Status = 'Active'
                )
                ORDER BY a.Value_Estimate DESC
                LIMIT 10
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                print("\n[INFO] All assets are currently assigned to active missions.")
            else:
                print("\nTop 10 High-Value Unassigned Assets:")
                print(f"  {'Code':<15} | {'Type':<20} | {'Value':<15}")
                print("  " + "-"*54)
                for row in results:
                    print(f"  {row['Asset_Code']:<15} | {row['Asset_Type']:<20} | {row['Value_Estimate']:<15}")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)

def analyze_pokemon_stats_by_type(connection):
    """
    READ 8: Average HP, Attack, Defense for each Pokemon type.
    Uses JOIN, GROUP BY, AVG.
    """
    print("\n--- 8. Analyze Pokemon Stats by Type ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT pt.Type, AVG(p.HP) as Avg_HP, AVG(p.Attack) as Avg_Atk, AVG(p.Defense) as Avg_Def
                FROM POKEMON p
                JOIN POKEMON_TYPE pt ON p.Pokemon_ID = pt.Pokemon_ID
                GROUP BY pt.Type
                ORDER BY Avg_Atk DESC
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                print("\n[INFO] No Pokemon data available.")
            else:
                print("\nAverage Stats by Pokemon Type:")
                print(f"  {'Type':<15} | {'Avg HP':<10} | {'Avg Atk':<10} | {'Avg Def':<10}")
                print("  " + "-"*53)
                for row in results:
                    print(f"  {row['Type']:<15} | {row['Avg_HP']:<10.2f} | {row['Avg_Atk']:<10.2f} | {row['Avg_Def']:<10.2f}")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)

def find_trainers_with_high_notoriety_no_mission(connection):
    """
    READ 9: Find trainers with NotorietyScore > X who are not targeted by any mission.
    Uses LEFT JOIN with NULL check.
    """
    print("\n--- 9. High Notoriety Trainers (Untargeted) ---")
    try:
        score_threshold = input("  > Enter Minimum Notoriety Score (e.g., 50): ").strip()
        if not score_threshold.isdigit():
            print("[ERROR] Please enter a valid number.")
            return
        
        with connection.cursor() as cursor:
            sql = """
                SELECT t.Name, t.Affiliation, t.NotorietyScore
                FROM TRAINER t
                LEFT JOIN MISSION m ON t.Trainer_ID = m.Target_Trainer_ID
                WHERE t.NotorietyScore > %s AND m.Mission_ID IS NULL
                ORDER BY t.NotorietyScore DESC
            """
            cursor.execute(sql, (int(score_threshold),))
            results = cursor.fetchall()

            if not results:
                print(f"\n[INFO] No untargeted trainers found with score > {score_threshold}.")
            else:
                print(f"\nUntargeted Trainers with Notoriety > {score_threshold}:")
                print(f"  {'Name':<25} | {'Affiliation':<20} | {'Score':<10}")
                print("  " + "-"*60)
                for row in results:
                    print(f"  {row['Name']:<25} | {row['Affiliation']:<20} | {row['NotorietyScore']:<10}")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)

def mission_success_rate_by_base(connection):
    """
    READ 10: Calculate the percentage of completed missions for personnel from each base.
    Uses Complex JOIN, GROUP BY, Conditional Aggregation.
    """
    print("\n--- 10. Mission Success Rate by Base ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT b.Name as Base_Name, 
                       COUNT(DISTINCT m.Mission_ID) as Total_Missions,
                       SUM(CASE WHEN m.Status = 'Completed' THEN 1 ELSE 0 END) as Completed_Missions
                FROM BASE b
                JOIN PERSONNEL p ON b.Base_ID = p.Base_ID
                JOIN MISSION_ASSIGNMENT ma ON p.Personnel_ID = ma.Personnel_ID
                JOIN MISSION m ON ma.Mission_ID = m.Mission_ID
                GROUP BY b.Base_ID, b.Name
                ORDER BY Total_Missions DESC
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                print("\n[INFO] No mission data available for bases.")
            else:
                print("\nMission Statistics by Base:")
                print(f"  {'Base Name':<25} | {'Total':<10} | {'Completed':<10} | {'Success Rate':<15}")
                print("  " + "-"*68)
                for row in results:
                    total = row['Total_Missions']
                    completed = row['Completed_Missions']
                    rate = (completed / total * 100) if total > 0 else 0
                    print(f"  {row['Base_Name']:<25} | {total:<10} | {completed:<10} | {rate:<6.2f}%")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)


# --- WRITE (C/U/D) OPERATIONS ---

def add_new_asset(connection):
    """
    WRITE 1 (INSERT): Adds a new asset to the ASSET table.
    """
    print("\n--- 11. (INSERT) Add New Asset ---")
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
    print("\n--- 12. (UPDATE) Update Mission Status ---")
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
    print("\n--- 13. (DELETE) Remove Asset from Mission ---")
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

def recruit_new_personnel(connection):
    """
    WRITE 4 (INSERT): Recruits new personnel and assigns them a rank.
    """
    print("\n--- 14. (INSERT) Recruit New Personnel ---")
    try:
        fname = input("  > First Name: ").strip()
        lname = input("  > Last Name: ").strip()
        rank = input("  > Rank (Boss, Grunt, Scientist): ").strip().capitalize()
        
        if rank not in ('Boss', 'Grunt', 'Scientist'):
            print("[ERROR] Invalid rank.")
            return

        # For simplicity, we'll assign them to the first available Base ID or ask for it.
        # Let's ask for Base ID.
        base_id = input("  > Base ID (Enter for default/NULL): ").strip()
        base_id = int(base_id) if base_id else None

        with connection.cursor() as cursor:
            # 1. Insert into PERSONNEL
            sql_personnel = "INSERT INTO PERSONNEL (FName, LName, Rank, StartDate, Base_ID) VALUES (%s, %s, %s, CURDATE(), %s)"
            cursor.execute(sql_personnel, (fname, lname, rank, base_id))
            personnel_id = cursor.lastrowid

            # 2. Insert into Subclass Table
            if rank == 'Grunt':
                # Assign to a squad? Let's leave it NULL for now or ask.
                cursor.execute("INSERT INTO GRUNT (Grunt_Personnel_ID) VALUES (%s)", (personnel_id,))
            elif rank == 'Scientist':
                spec = input("  > Specialization: ").strip()
                cursor.execute("INSERT INTO SCIENTIST (Scientist_Personnel_ID, Specialization) VALUES (%s, %s)", (personnel_id, spec))
            elif rank == 'Boss':
                region = input("  > Region Managed: ").strip()
                cursor.execute("INSERT INTO BOSS (Boss_Personnel_ID, Region_Managed) VALUES (%s, %s)", (personnel_id, region))
        
        connection.commit()
        print(f"\n[SUCCESS] Recruited {rank} {fname} {lname} (ID: {personnel_id}).")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during recruitment: {e}", file=sys.stderr)
        connection.rollback()
    except ValueError:
        print("\n[ERROR] Invalid input.")
        connection.rollback()

def assign_pokemon_to_personnel(connection):
    """
    WRITE 5 (INSERT): Assigns a Pokemon to a personnel member.
    """
    print("\n--- 15. (INSERT) Assign Pokemon to Personnel ---")
    try:
        personnel_id = int(input("  > Personnel ID: "))
        pokemon_id = int(input("  > Pokemon ID: "))

        with connection.cursor() as cursor:
            sql = "INSERT INTO OWNERSHIP (Personnel_ID, Pokemon_ID) VALUES (%s, %s)"
            cursor.execute(sql, (personnel_id, pokemon_id))
        
        connection.commit()
        print(f"\n[SUCCESS] Pokemon {pokemon_id} assigned to Personnel {personnel_id}.")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during assignment: {e}", file=sys.stderr)
        connection.rollback()
    except ValueError:
        print("\n[ERROR] Invalid ID.")

def update_pokemon_stats(connection):
    """
    WRITE 6 (UPDATE): Updates a Pokemon's stats.
    """
    print("\n--- 16. (UPDATE) Update Pokemon Stats ---")
    try:
        pokemon_id = int(input("  > Pokemon ID: "))
        new_hp = int(input("  > New HP: "))
        new_atk = int(input("  > New Attack: "))
        new_def = int(input("  > New Defense: "))

        if new_hp <= 0 or new_atk <= 0 or new_def <= 0:
            print("[ERROR] Stats must be positive.")
            return

        with connection.cursor() as cursor:
            sql = "UPDATE POKEMON SET HP = %s, Attack = %s, Defense = %s WHERE Pokemon_ID = %s"
            rows = cursor.execute(sql, (new_hp, new_atk, new_def, pokemon_id))
        
        if rows == 0:
            print(f"\n[INFO] No Pokemon found with ID {pokemon_id}.")
        else:
            connection.commit()
            print(f"\n[SUCCESS] Pokemon {pokemon_id} stats updated.")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during update: {e}", file=sys.stderr)
        connection.rollback()
    except ValueError:
        print("\n[ERROR] Invalid input.")

def fire_personnel(connection):
    """
    WRITE 7 (DELETE): Fires (deletes) a personnel member.
    """
    print("\n--- 17. (DELETE) Fire Personnel ---")
    try:
        personnel_id = int(input("  > Personnel ID to Fire: "))
        confirm = input(f"  > Are you sure you want to fire ID {personnel_id}? (y/n): ").lower()

        if confirm != 'y':
            print("[INFO] Operation cancelled.")
            return

        with connection.cursor() as cursor:
            # ON DELETE CASCADE should handle the subclass tables
            sql = "DELETE FROM PERSONNEL WHERE Personnel_ID = %s"
            rows = cursor.execute(sql, (personnel_id,))
        
        if rows == 0:
            print(f"\n[INFO] No personnel found with ID {personnel_id}.")
        else:
            connection.commit()
            print(f"\n[SUCCESS] Personnel {personnel_id} has been fired.")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during deletion: {e}", file=sys.stderr)
        connection.rollback()
    except ValueError:
        print("\n[ERROR] Invalid ID.")

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
            print("   6. Top Performing Personnel")
            print("   7. List Unassigned Assets")
            print("   8. Analyze Pokemon Stats by Type")
            print("   9. High Notoriety Trainers (Untargeted)")
            print("   10. Mission Success Rate by Base")
            print("\n [WRITE OPERATIONS]")
            print("   11. (INSERT) Add New Asset")
            print("   12. (UPDATE) Update Mission Status")
            print("   13. (DELETE) Remove Asset from Mission")
            print("   14. (INSERT) Recruit New Personnel")
            print("   15. (INSERT) Assign Pokemon to Personnel")
            print("   16. (UPDATE) Update Pokemon Stats")
            print("   17. (DELETE) Fire Personnel")
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
                find_top_performing_personnel(connection)
            elif choice == '7':
                list_unassigned_assets(connection)
            elif choice == '8':
                analyze_pokemon_stats_by_type(connection)
            elif choice == '9':
                find_trainers_with_high_notoriety_no_mission(connection)
            elif choice == '10':
                mission_success_rate_by_base(connection)
            elif choice == '11':
                add_new_asset(connection)
            elif choice == '12':
                update_mission_status(connection)
            elif choice == '13':
                remove_asset_from_mission(connection)
            elif choice == '14':
                recruit_new_personnel(connection)
            elif choice == '15':
                assign_pokemon_to_personnel(connection)
            elif choice == '16':
                update_pokemon_stats(connection)
            elif choice == '17':
                fire_personnel(connection)
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
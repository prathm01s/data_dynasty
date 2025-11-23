"""
Phase 4 & 1: Main Application Interface (main_app.py)
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

# --- WRITE QUERIES (8-12) ---

def recruit_new_personnel(connection):
    """WRITE 8 (INSERT): Recruits new personnel and assigns them a rank."""
    print("\n--- 8. (INSERT) Recruit New Personnel ---")
    try:
        fname = input("  > First Name: ").strip()
        lname = input("  > Last Name: ").strip()
        rank = input("  > Rank (Boss, Grunt, Scientist): ").strip().capitalize()
        
        if rank not in ('Boss', 'Grunt', 'Scientist'):
            print("[ERROR] Invalid rank.")
            return

        base_id = input("  > Base ID (Press Enter for keeping NULL): ").strip()
        base_id = int(base_id) if base_id else None

        with connection.cursor() as cursor:
            sql_personnel = "INSERT INTO PERSONNEL (FName, LName, `Rank`, StartDate, Base_ID) VALUES (%s, %s, %s, CURDATE(), %s)"
            cursor.execute(sql_personnel, (fname, lname, rank, base_id))
            personnel_id = cursor.lastrowid

            if rank == 'Grunt':
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
    """WRITE 9 (INSERT): Assigns a Pokemon to a personnel member."""
    print("\n--- 9. (INSERT) Assign Pokemon to Personnel ---")
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

def update_mission_status(connection):
    """WRITE 10 (UPDATE): Updates the status of an existing mission."""
    print("\n--- 10. (UPDATE) Update Mission Status ---")
    try:
        mission_id = int(input("  > Enter Mission ID to update: "))
        
        valid_statuses = ('Pending', 'Active', 'Completed', 'Failed', 'Aborted')
        print(f"  Valid statuses are: {valid_statuses}")
        new_status = input("  > Enter new status: ").strip().capitalize()

        if new_status not in valid_statuses:
            print(f"\n[ERROR] Invalid status '{new_status}'.")
            return

        end_date_sql = ", EndDate = CURDATE()" if new_status in ('Completed', 'Failed', 'Aborted') else ""
        
        with connection.cursor() as cursor:
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

# --- READ QUERIES (1-7) ---

def get_genetics_scientists(connection):
    """READ 1: Retrieve all Scientists whose specialization includes Genetics."""
    print("\n--- 1. Scientists with 'Genetics' Specialization ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT p.FName, p.LName, s.Specialization, b.Name as Base
                FROM SCIENTIST s
                JOIN PERSONNEL p ON s.Scientist_Personnel_ID = p.Personnel_ID
                LEFT JOIN BASE b ON p.Base_ID = b.Base_ID
                WHERE s.Specialization LIKE '%Genetics%'
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            
            if not results:
                print("[INFO] No genetics specialists found.")
            else:
                print(f"  {'Name':<25} | {'Specialization':<20} | {'Base':<20}")
                print("  " + "-"*69)
                for row in results:
                    full_name = f"{row['FName']} {row['LName']}"
                    print(f"  {full_name:<25} | {row['Specialization']:<20} | {row['Base']:<20}")
    except pymysql.Error as e:
        print(f"[ERROR] {e}")

def get_grunts_by_base(connection):
    """READ 2: Display Grunts assigned to a specific Base."""
    print("\n--- 2. List Grunts by Base ---")
    base_name = input("  > Enter Base Name ('Chimera HQ', 'Minos Station', 'Outpost Delta', 'Aether Lab', 'Castelia Stronghold'): ").strip()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT p.FName, p.LName, p.Rank, g.Squad_ID
                FROM GRUNT g
                JOIN PERSONNEL p ON g.Grunt_Personnel_ID = p.Personnel_ID
                JOIN BASE b ON p.Base_ID = b.Base_ID
                WHERE b.Name = %s
            """
            cursor.execute(sql, (base_name,))
            results = cursor.fetchall()
            
            if not results:
                print(f"[INFO] No Grunts found at '{base_name}' (or base does not exist).")
            else:
                print(f"\nGrunts stationed at {base_name}:")
                print(f"  {'Name':<25} | {'Rank':<10} | {'Squad ID':<10}")
                print("  " + "-"*49)
                for row in results:
                    full_name = f"{row['FName']} {row['LName']}"
                    print(f"  {full_name:<25} | {row['Rank']:<10} | {row['Squad_ID']:<10}")
    except pymysql.Error as e:
        print(f"[ERROR] {e}")

def get_project_combat_rating(connection):
    """READ 3: Compute average Combat Rating (Atk+Def) of Pokemon in a Project."""
    print("\n--- 3. Project Combat Rating Analysis ---")
    project_title = input("  > Enter Project Title ('Project Chimera', 'Project Apex', 'Project Vesper', 'Project Abyss' etc.): ").strip()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT AVG(p.Attack + p.Defense) as Avg_Rating
                FROM POKEMON p
                JOIN RESEARCH_PROJECT rp ON p.Project_ID = rp.Project_ID
                WHERE rp.Title = %s
            """
            cursor.execute(sql, (project_title,))
            result = cursor.fetchone()
            
            if not result or result['Avg_Rating'] is None:
                print(f"[INFO] No Pokemon found for project '{project_title}'.")
            else:
                print(f"\n[RESULT] Average Combat Rating (Atk + Def) for {project_title}: {result['Avg_Rating']:.2f}")
    except pymysql.Error as e:
        print(f"[ERROR] {e}")

def search_mission_assets(connection):
    """READ 4: Find specific assets for a mission."""
    print("\n--- 4. Search Mission Assets ---")
    try:
        m_id = input("  > Mission ID: ")
        a_type = input("  > Asset Type (e.g., 'Stealth Helicopter'): ").strip()
        status = input("  > Acquisition Status (e.g., 'Acquired'): ").strip()
        
        with connection.cursor() as cursor:
            sql = """
                SELECT ma.Asset_Code, a.Asset_Type, ma.Acquisition_Status, a.Value_Estimate
                FROM MISSION_ASSETS ma
                JOIN ASSET a ON ma.Asset_Code = a.Asset_Code
                WHERE ma.Mission_ID = %s AND a.Asset_Type = %s AND ma.Acquisition_Status = %s
            """
            cursor.execute(sql, (m_id, a_type, status))
            results = cursor.fetchall()
            
            if not results:
                print("[INFO] No matching assets found.")
            else:
                print(f"\nMatching Assets for Mission {m_id}:")
                for row in results:
                    print(f"  - {row['Asset_Code']} ({row['Asset_Type']}) - Value: {row['Value_Estimate']}")
    except pymysql.Error as e:
        print(f"[ERROR] {e}")

# ==========================================
# PHASE 1: ANALYSIS REPORTS (NEW)
# ==========================================

def report_mission_readiness(connection):
    """READ 5: Mission Readiness overview."""
    print("\n--- 5. Mission Readiness Report ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT m.Mission_ID, m.Objective, p.LName, pok.Name as PokeName, pt.Type
                FROM MISSION m
                JOIN MISSION_ASSIGNMENT ma ON m.Mission_ID = ma.Mission_ID
                JOIN PERSONNEL p ON ma.Personnel_ID = p.Personnel_ID
                LEFT JOIN OWNERSHIP o ON p.Personnel_ID = o.Personnel_ID
                LEFT JOIN POKEMON pok ON o.Pokemon_ID = pok.Pokemon_ID
                LEFT JOIN POKEMON_TYPE pt ON pok.Pokemon_ID = pt.Pokemon_ID
                WHERE m.Status = 'Pending'
                ORDER BY m.Mission_ID, p.LName
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            
            if not results:
                print("[INFO] No pending missions with assigned personnel.")
                return

            print(f"\n{'Mission ID':<10} | {'Objective':<30} | {'Personnel':<15} | {'Pokemon':<15} | {'Type':<10}")
            print("-" * 90)
            for row in results:
                m_obj = (row['Objective'][:27] + '..') if len(row['Objective']) > 27 else row['Objective']
                p_name = row['LName']
                poke = row['PokeName'] if row['PokeName'] else "None"
                p_type = row['Type'] if row['Type'] else "-"
                print(f"{row['Mission_ID']:<10} | {m_obj:<30} | {p_name:<15} | {poke:<15} | {p_type:<10}")

    except pymysql.Error as e:
        print(f"[ERROR] {e}")

def report_experimental_subjects(connection):
    """READ 6: Experimental Subject analysis."""
    print("\n--- 6. Experimental Subject Analysis ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT pok.Name, COUNT(ee.Serum_ID) as Exp_Count, 
                       pok.HP, pok.Attack, pok.Defense, rp.Title as Project
                FROM POKEMON pok
                JOIN EXPERIMENTATION_EVENT ee ON pok.Pokemon_ID = ee.Pokemon_ID
                LEFT JOIN RESEARCH_PROJECT rp ON pok.Project_ID = rp.Project_ID
                GROUP BY pok.Pokemon_ID, pok.Name, pok.HP, pok.Attack, pok.Defense, rp.Title
                ORDER BY Exp_Count DESC
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            
            if not results:
                print("[INFO] No subjects found with more than 5 experiments.")
            else:
                print(f"\n{'Pokemon':<20} | {'Exp Count':<10} | {'Stats (H/A/D)':<15} | {'Project':<20}")
                print("-" * 70)
                for row in results:
                    stats = f"{row['HP']}/{row['Attack']}/{row['Defense']}"
                    print(f"{row['Name']:<20} | {row['Exp_Count']:<10} | {stats:<15} | {row['Project']:<20}")
    except pymysql.Error as e:
        print(f"[ERROR] {e}")

def report_regional_strength(connection):
    """READ 7: Regional Strength assessment."""
    print("\n--- 7. Regional Strength Assessment ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT b.Name as Base, boss.LName as Boss,
                       COUNT(DISTINCT g.Grunt_Personnel_ID) as Grunt_Count,
                       AVG(pok.Attack + pok.Defense) as Avg_Combat_Rating
                FROM BASE b
                LEFT JOIN BOSS ON b.Boss_ID = BOSS.Boss_Personnel_ID
                LEFT JOIN PERSONNEL boss ON BOSS.Boss_Personnel_ID = boss.Personnel_ID
                LEFT JOIN PERSONNEL p_grunt ON p_grunt.Base_ID = b.Base_ID
                LEFT JOIN GRUNT g ON p_grunt.Personnel_ID = g.Grunt_Personnel_ID
                LEFT JOIN OWNERSHIP o ON p_grunt.Personnel_ID = o.Personnel_ID
                LEFT JOIN POKEMON pok ON o.Pokemon_ID = pok.Pokemon_ID
                GROUP BY b.Base_ID, b.Name, boss.LName
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            
            print(f"\n{'Base':<25} | {'Boss':<15} | {'Grunts':<10} | {'Avg Pkmn Rating':<15}")
            print("-" * 70)
            for row in results:
                rating = f"{row['Avg_Combat_Rating']:.2f}" if row['Avg_Combat_Rating'] else "N/A"
                print(f"{row['Base']:<25} | {row['Boss']:<15} | {row['Grunt_Count']:<10} | {rating:<15}")

    except pymysql.Error as e:
        print(f"[ERROR] {e}")

# ==========================================
# PHASE 1: ADVANCED MODIFICATION (NEW)
# ==========================================

def add_new_pokemon_strict(connection):
    """WRITE 11 (INSERT): Add Pokemon with strict type validation."""
    print("\n--- 11. (INSERT) Add New Pokemon (Strict) ---")
    VALID_TYPES = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 
                   'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 
                   'Dragon', 'Steel', 'Dark', 'Fairy']
    
    try:
        name = input("  > Pokemon Name: ").strip()
        p_type = input(f"  > Type ({', '.join(VALID_TYPES[:5])}...): ").strip().capitalize()
        
        if p_type not in VALID_TYPES:
            print(f"[REJECTED] '{p_type}' is not a pre-approved Pokemon Type.")
            return

        hp = int(input("  > HP: "))
        atk = int(input("  > Attack: "))
        defn = int(input("  > Defense: "))
        
        with connection.cursor() as cursor:
            sql_p = "INSERT INTO POKEMON (Name, HP, Attack, Defense) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_p, (name, hp, atk, defn))
            new_id = cursor.lastrowid
            
            sql_t = "INSERT INTO POKEMON_TYPE (Pokemon_ID, Type) VALUES (%s, %s)"
            cursor.execute(sql_t, (new_id, p_type))
        
        connection.commit()
        print(f"[SUCCESS] Added {name} (ID: {new_id}) with type {p_type}.")

    except ValueError:
        print("[ERROR] Invalid number format.")
    except pymysql.Error as e:
        connection.rollback()
        print(f"[ERROR] Database error: {e}")

def safe_delete_operations(connection):
    """WRITE 12 (DELETE/ARCHIVE): Safe administrative operations."""
    print("\n--- 12. (DELETE/ARCHIVE) Safe Operations ---")
    print("  a. Archive Project")
    print("  b. Delete Base")
    choice = input("  > Selection: ").lower()
    
    try:
        with connection.cursor() as cursor:
            if choice == 'a':
                p_id = input("  > Project ID to Archive: ")
                cursor.execute("UPDATE RESEARCH_PROJECT SET Status='Archived' WHERE Project_ID=%s", (p_id,))
                connection.commit()
                print(f"[SUCCESS] Project {p_id} marked as Archived.")
                
            elif choice == 'b':
                b_id = input("  > Base ID to Delete: ")
                try:
                    cursor.execute("DELETE FROM BASE WHERE Base_ID=%s", (b_id,))
                    connection.commit()
                    print(f"[SUCCESS] Base {b_id} deleted.")
                except pymysql.err.IntegrityError as ie:
                    print(f"\n[REJECTED] Cannot delete Base. Personnel are still assigned.\nDetails: {ie.args[1]}")
                    connection.rollback()
            else:
                print("Invalid selection.")

    except pymysql.Error as e:
        connection.rollback()
        print(f"[ERROR] {e}")

# --- Main Application Loop ---

def main_cli(connection):
    try:
        while True:
            print("\n" + "="*50)
            print("    C H I M E R A  DB  -  O P E R A T I O N S")
            print("="*50)
            print(" [READ QUERIES]")
            print("   1. Scientists with Genetics Focus")
            print("   2. Grunts by Base")
            print("   3. Project Combat Rating")
            print("   4. Search Mission Assets")
            print("   5. Mission Readiness Report")
            print("   6. Experimental Subject Analysis")
            print("   7. Regional Strength Assessment")
            
            print("\n [WRITE QUERIES]")
            print("   8. Recruit New Personnel")
            print("   9. Assign Pokemon to Personnel")
            print("   10. Update Mission Status")
            print("   11. Insert Pokemon (Strict Check)")
            print("   12. Safe Delete (Project/Base)")
            
            print("\n [SYSTEM]")
            print("   q. Quit")
            print("="*50)
            
            choice = input("  > Enter choice: ").strip().lower()

            if choice == '1': get_genetics_scientists(connection)
            elif choice == '2': get_grunts_by_base(connection)
            elif choice == '3': get_project_combat_rating(connection)
            elif choice == '4': search_mission_assets(connection)
            elif choice == '5': report_mission_readiness(connection)
            elif choice == '6': report_experimental_subjects(connection)
            elif choice == '7': report_regional_strength(connection)
            
            elif choice == '8': recruit_new_personnel(connection)
            elif choice == '9': assign_pokemon_to_personnel(connection)
            elif choice == '10': update_mission_status(connection)
            elif choice == '11': add_new_pokemon_strict(connection)
            elif choice == '12': safe_delete_operations(connection)
            
            elif choice == 'q':
                print("\n[INFO] Exiting application...")
                break
            else:
                print("\n[ERROR] Invalid choice.")
    
    finally:
        if connection:
            connection.close()
            print("[INFO] Database connection closed.")

if __name__ == "__main__":
    DB_HOST = 'localhost'
    DB_NAME = 'chimera_db'
    
    print("--- Chimera Database Login ---")
    DB_USER = input("  > Username: ").strip()
    DB_PASS = getpass("  > Password: ")

    db_conn = get_db_connection(DB_USER, DB_PASS, DB_HOST, DB_NAME)

    if db_conn:
        main_cli(db_conn)
    else:
        sys.exit(1)
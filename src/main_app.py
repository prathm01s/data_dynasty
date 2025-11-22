"""
Phase 4 & 5: Main Application Interface (main_app.py)
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

# ==========================================
# PHASE 4: ORIGINAL READ OPERATIONS (1-7)
# ==========================================

def show_active_missions(connection):
    """READ 1: Shows all 'Active' missions and their assigned personnel."""
    print("\n--- 1. Show Active Missions and Assignments ---")
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

def calculate_pending_mission_risk(connection):
    """READ 2: Calculates total notoriety of trainers targeted in 'Pending' missions."""
    print("\n--- 2. Calculate Pending Mission Risk ---")
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
    """READ 3: Find personnel who have participated in the most 'Completed' missions."""
    print("\n--- 3. Top Performing Personnel ---")
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
    """READ 4: List assets that are not currently assigned to any active mission."""
    print("\n--- 4. List Unassigned Assets ---")
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
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                print("\n[INFO] All assets are currently assigned to active missions.")
            else:
                print("\n All Unassigned Assets:")
                print(f"  {'Code':<15} | {'Type':<20} | {'Value':<15}")
                print("  " + "-"*54)
                for row in results:
                    print(f"  {row['Asset_Code']:<15} | {row['Asset_Type']:<20} | {row['Value_Estimate']:<15}")

    except pymysql.Error as e:
        print(f"\n[ERROR] Error during query: {e}", file=sys.stderr)

def analyze_pokemon_stats_by_type(connection):
    """READ 5: Average HP, Attack, Defense for each Pokemon type."""
    print("\n--- 5. Analyze Pokemon Stats by Type ---")
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
    """READ 6: Find trainers with NotorietyScore > X who are not targeted."""
    print("\n--- 6. High Notoriety Trainers (Untargeted) ---")
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
    """READ 7: Calculate percentage of completed missions for personnel from each base."""
    print("\n--- 7. Mission Success Rate by Base ---")
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


# ==========================================
# PHASE 4: ORIGINAL WRITE OPERATIONS (8-12)
# ==========================================

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

def update_pokemon_stats(connection):
    """WRITE 11 (UPDATE): Updates a Pokemon's stats."""
    print("\n--- 11. (UPDATE) Update Pokemon Stats ---")
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
    """WRITE 12 (DELETE): Fires (deletes) a personnel member."""
    print("\n--- 12. (DELETE) Fire Personnel ---")
    try:
        personnel_id = int(input("  > Personnel ID to Fire: "))
        confirm = input(f"  > Are you sure you want to fire ID {personnel_id}? (y/n): ").lower()

        if confirm != 'y':
            print("[INFO] Operation cancelled.")
            return

        with connection.cursor() as cursor:
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

# ==========================================
# PHASE 5: ADVANCED RETRIEVAL (NEW)
# ==========================================

def get_genetics_scientists(connection):
    """Selection: Retrieve all Scientists whose specialization includes Genetics."""
    print("\n--- 13. Scientists with 'Genetics' Specialization ---")
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
    """Projection: Display Grunts assigned to a specific Base."""
    print("\n--- 14. List Grunts by Base ---")
    base_name = input("  > Enter Base Name (e.g., 'Chimera HQ', 'Minos Station'): ").strip()
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
    """Aggregate: Compute average Combat Rating (Atk+Def) of Pokemon in a Project."""
    print("\n--- 15. Project Combat Rating Analysis ---")
    project_title = input("  > Enter Project Title (e.g., 'Project Chimera'): ").strip()
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
    """Search: Find specific assets for a mission."""
    print("\n--- 16. Search Mission Assets ---")
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
# PHASE 5: ANALYSIS REPORTS (NEW)
# ==========================================

def report_mission_readiness(connection):
    """Report: Mission Readiness."""
    print("\n--- 17. Mission Readiness Report ---")
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
    """Report: Experimental Subject Analysis."""
    print("\n--- 18. Experimental Subject Analysis (>5 Experiments) ---")
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT pok.Name, COUNT(ee.Serum_ID) as Exp_Count, 
                       pok.HP, pok.Attack, pok.Defense, rp.Title as Project
                FROM POKEMON pok
                JOIN EXPERIMENTATION_EVENT ee ON pok.Pokemon_ID = ee.Pokemon_ID
                LEFT JOIN RESEARCH_PROJECT rp ON pok.Project_ID = rp.Project_ID
                GROUP BY pok.Pokemon_ID, pok.Name, pok.HP, pok.Attack, pok.Defense, rp.Title
                HAVING Exp_Count > 5
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
    """Report: Regional Strength Assessment."""
    print("\n--- 19. Regional Strength Assessment ---")
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
# PHASE 5: ADVANCED MODIFICATION (NEW)
# ==========================================

def add_new_pokemon_strict(connection):
    """Insertion with Integrity Check: Pre-approved Type List."""
    print("\n--- 20. (INSERT) Add New Pokemon (Strict) ---")
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

def mark_personnel_mia(connection):
    """
    Update with Cascading Rule (MIA):
    Triggers side effects: Updates assignments to Compromised, transfers Pokemon to Boss.
    """
    print("\n--- 21. (UPDATE) Mark Personnel MIA ---")
    try:
        p_id = input("  > Personnel ID to mark MIA: ")
        
        with connection.cursor() as cursor:
            # 1. Check existence and get Base info
            cursor.execute("SELECT Base_ID FROM PERSONNEL WHERE Personnel_ID = %s", (p_id,))
            res = cursor.fetchone()
            if not res:
                print("[ERROR] Personnel not found.")
                return
            
            base_id = res['Base_ID']
            cursor.execute("SELECT Boss_ID FROM BASE WHERE Base_ID = %s", (base_id,))
            res_boss = cursor.fetchone()
            boss_id = res_boss['Boss_ID'] if res_boss else None

            # 2. Update Missions
            cursor.execute("UPDATE MISSION_ASSIGNMENT SET Status = 'Compromised' WHERE Personnel_ID = %s", (p_id,))
            
            # 3. Transfer Pokemon
            if boss_id and int(p_id) != boss_id:
                row_count = cursor.execute("UPDATE OWNERSHIP SET Personnel_ID = %s WHERE Personnel_ID = %s", (boss_id, p_id))
                print(f"[INFO] Transferred {row_count} Pokemon to Boss ID {boss_id}.")
            else:
                print("[INFO] No Boss found (or MIA is Boss). Pokemon not transferred.")

        connection.commit()
        print(f"[SUCCESS] Personnel {p_id} processed as MIA. Side effects applied.")

    except pymysql.Error as e:
        connection.rollback()
        print(f"[ERROR] {e}")

def safe_delete_operations(connection):
    """Safe Delete: Archive Project or Delete Base (Strict)."""
    print("\n--- 22. (DELETE/ARCHIVE) Safe Operations ---")
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
            print(" [PHASE 4: ORIGINAL READ]")
            print("   1. Show Active Missions")
            print("   2. Calculate Pending Mission Risk")
            print("   3. Top Performing Personnel")
            print("   4. List Unassigned Assets")
            print("   5. Analyze Pokemon Stats by Type")
            print("   6. High Notoriety Trainers (Untargeted)")
            print("   7. Mission Success Rate by Base")
            
            print("\n [PHASE 4: ORIGINAL WRITE]")
            print("   8. Recruit New Personnel")
            print("   9. Assign Pokemon to Personnel")
            print("   10. Update Mission Status")
            print("   11. Update Pokemon Stats")
            print("   12. Fire Personnel")

            print("\n [PHASE 5: ADVANCED RETRIEVAL & REPORTS]")
            print("   13. Selection: Scientists (Genetics)")
            print("   14. Projection: Grunts by Base")
            print("   15. Aggregate: Project Combat Rating")
            print("   16. Search: Mission Assets")
            print("   17. Report: Mission Readiness")
            print("   18. Report: Experimental Subjects")
            print("   19. Report: Regional Strength")

            print("\n [PHASE 5: ADVANCED MODIFICATION]")
            print("   20. Insert Pokemon (Strict Check)")
            print("   21. Mark Personnel MIA (Cascade)")
            print("   22. Safe Delete (Project/Base)")
            
            print("\n [SYSTEM]")
            print("   q. Quit")
            print("="*50)
            
            choice = input("  > Enter choice: ").strip().lower()

            if choice == '1': show_active_missions(connection)
            elif choice == '2': calculate_pending_mission_risk(connection)
            elif choice == '3': find_top_performing_personnel(connection)
            elif choice == '4': list_unassigned_assets(connection)
            elif choice == '5': analyze_pokemon_stats_by_type(connection)
            elif choice == '6': find_trainers_with_high_notoriety_no_mission(connection)
            elif choice == '7': mission_success_rate_by_base(connection)
            
            elif choice == '8': recruit_new_personnel(connection)
            elif choice == '9': assign_pokemon_to_personnel(connection)
            elif choice == '10': update_mission_status(connection)
            elif choice == '11': update_pokemon_stats(connection)
            elif choice == '12': fire_personnel(connection)
            
            elif choice == '13': get_genetics_scientists(connection)
            elif choice == '14': get_grunts_by_base(connection)
            elif choice == '15': get_project_combat_rating(connection)
            elif choice == '16': search_mission_assets(connection)
            elif choice == '17': report_mission_readiness(connection)
            elif choice == '18': report_experimental_subjects(connection)
            elif choice == '19': report_regional_strength(connection)
            
            elif choice == '20': add_new_pokemon_strict(connection)
            elif choice == '21': mark_personnel_mia(connection)
            elif choice == '22': safe_delete_operations(connection)
            
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
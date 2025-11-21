# Chimera DB Interface

This project is a command-line interface (CLI) for interacting with the `chimera_db`, a database designed to manage the operations of a clandestine organization. It allows users to perform various read and write operations to track personnel, missions, assets, and Pokémon.

## Prerequisites

- Python 3.x
- `pymysql` library (`pip install pymysql`)
- A running MySQL server instance.

## Database Setup

1.  **Create the Database**: Ensure you have a database named `chimera_db` on your MySQL server.
2.  **Run the Schema**: Execute the contents of `schema.sql` to create the table structure.
    ```sql
    -- Example using MySQL CLI:
    mysql -u your_username -p chimera_db < schema.sql
    ```
3.  **Populate Data**: Execute the contents of `populate.sql` to insert initial data into the tables.
    ```sql
    -- Example using MySQL CLI:
    mysql -u your_username -p chimera_db < populate.sql
    ```

## How to Run

1.  Navigate to the project directory.
2.  Run the main application script from your terminal:
    ```bash
    python3 main_app.py
    ```
3.  You will be prompted to enter your MySQL username and password to connect to the database.
4.  Once connected, a menu of available commands will be displayed.

## Features

The application provides the following commands, grouped by Read (query) and Write (create/update/delete) operations.

### Read Operations

1.  **Show Active Missions and Assignments** - Lists all missions currently marked as 'Active' and shows the personnel assigned to each.
2.  **Calculate Pending Mission Risk** - Calculates the total notoriety score of all trainers targeted in 'Pending' missions, providing a cumulative risk assessment.
3.  **Top Performing Personnel** - Displays the top 5 personnel members who have completed the most missions.
4.  **List Unassigned Assets** - Shows a list of all assets that are not currently assigned to any active mission.
5.  **Analyze Pokemon Stats by Type** - Calculates and displays the average HP, Attack, and Defense for each Pokémon type.
6.  **High Notoriety Trainers (Untargeted)** - Prompts for a minimum notoriety score and lists trainers who exceed that score and are not currently targeted by any mission.
7.  **Mission Success Rate by Base** - Shows statistics for each base, including total missions, completed missions, and the overall success rate.

### Write Operations

8.  **Recruit New Personnel** - Guides you through adding a new member (Boss, Grunt, or Scientist) to the organization.
9.  **Assign Pokemon to Personnel** - Assigns an existing Pokémon to a personnel member via their respective IDs.
10. **Update Mission Status** - Allows you to change the status of a mission (e.g., to 'Completed', 'Failed').
11. **Update Pokemon Stats** - Updates the HP, Attack, and Defense stats for a specific Pokémon.
12. **Fire Personnel** - Removes a personnel member from the database. This action will cascade and remove related records.

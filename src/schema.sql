-- Phase 4: Database Implementation
-- schema.sql: This script defines the structure for the "Mini World" database.

-- 1. Database Creation
-- Create and select the database as required [cite: 24, 25]
DROP DATABASE IF EXISTS chimera_db;
CREATE DATABASE chimera_db;
USE chimera_db;

-- 2. Table Creation
-- Tables are created in an order that respects foreign key dependencies.

-- ====== GROUP 1: Independent Entities ======
-- These tables have no foreign keys and can be created first.

CREATE TABLE TRAINER (
    Trainer_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Affiliation VARCHAR(100) DEFAULT 'Unknown',
    NotorietyScore INT NOT NULL DEFAULT 0
        CHECK (NotorietyScore >= 0)
);

CREATE TABLE RESEARCH_PROJECT (
    Project_ID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL UNIQUE,
    `Status` ENUM('Planning', 'Active', 'On Hold', 'Completed', 'Cancelled', 'Archived') NOT NULL,
    StartDate DATE,
    EndDate DATE,
    CHECK (EndDate IS NULL OR EndDate >= StartDate)
);

CREATE TABLE ASSET (
    Asset_Code VARCHAR(50) PRIMARY KEY,
    Asset_Type VARCHAR(100) NOT NULL,
    Value_Estimate DECIMAL(12, 2)
        CHECK (Value_Estimate >= 0)
);

-- ====== GROUP 2: Core Entities (Part 1) ======
-- These tables depend on Group 1 or are part of the core personnel structure.

CREATE TABLE MISSION (
    Mission_ID INT AUTO_INCREMENT PRIMARY KEY,
    Objective TEXT NOT NULL,
    `Status` ENUM('Pending', 'Active', 'Completed', 'Failed', 'Aborted') NOT NULL,
    StartDate DATE,
    EndDate DATE,
    Target_Trainer_ID INT,
    FOREIGN KEY (Target_Trainer_ID) REFERENCES TRAINER(Trainer_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CHECK (EndDate IS NULL OR EndDate >= StartDate)
);

CREATE TABLE POKEMON (
    Pokemon_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    HP INT NOT NULL CHECK (HP > 0),
    Attack INT NOT NULL CHECK (Attack > 0),
    Defense INT NOT NULL CHECK (Defense > 0),
    Project_ID INT,
    FOREIGN KEY (Project_ID) REFERENCES RESEARCH_PROJECT(Project_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- This is the superclass for Boss, Grunt, and Scientist
-- The Base_ID FK is added later via ALTER TABLE to break a circular dependency
CREATE TABLE PERSONNEL (
    Personnel_ID INT AUTO_INCREMENT PRIMARY KEY,
    FName VARCHAR(50) NOT NULL,
    LName VARCHAR(50) NOT NULL,
    `Rank` ENUM('Boss', 'Grunt', 'Scientist') NOT NULL,
    StartDate DATE,
    Base_ID INT -- FK constraint added at the end
);

-- ====== GROUP 3: Specialization & Dependent Entities ======
-- These tables implement the inheritance (specialization) from PERSONNEL
-- and other entities that depend on Groups 1 & 2.

CREATE TABLE BOSS (
    Boss_Personnel_ID INT PRIMARY KEY,
    Region_Managed VARCHAR(100) NOT NULL,
    FOREIGN KEY (Boss_Personnel_ID) REFERENCES PERSONNEL(Personnel_ID)
        ON DELETE CASCADE -- If the personnel record is gone, the boss role is gone
        ON UPDATE CASCADE
);

CREATE TABLE BASE (
    Base_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Location VARCHAR(255),
    `Status` ENUM('Active', 'Inactive', 'Under Construction', 'Destroyed') NOT NULL DEFAULT 'Active',
    Boss_ID INT UNIQUE, -- A base is managed by one boss
    FOREIGN KEY (Boss_ID) REFERENCES BOSS(Boss_Personnel_ID)
        ON DELETE SET NULL -- If boss is removed, base remains, needs new boss
        ON UPDATE CASCADE
);

CREATE TABLE SQUADS (
    Squad_ID INT AUTO_INCREMENT PRIMARY KEY,
    Boss_ID INT,
    FOREIGN KEY (Boss_ID) REFERENCES BOSS(Boss_Personnel_ID)
        ON DELETE SET NULL -- If boss is removed, squad may report to someone else
        ON UPDATE CASCADE
);

CREATE TABLE GRUNT (
    Grunt_Personnel_ID INT PRIMARY KEY,
    Squad_ID INT,
    FOREIGN KEY (Grunt_Personnel_ID) REFERENCES PERSONNEL(Personnel_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Squad_ID) REFERENCES SQUADS(Squad_ID)
        ON DELETE SET NULL -- If squad is disbanded, grunt is unassigned
        ON UPDATE CASCADE
);

CREATE TABLE SCIENTIST (
    Scientist_Personnel_ID INT PRIMARY KEY,
    Specialization VARCHAR(100),
    Project_ID INT,
    FOREIGN KEY (Scientist_Personnel_ID) REFERENCES PERSONNEL(Personnel_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Project_ID) REFERENCES RESEARCH_PROJECT(Project_ID)
        ON DELETE SET NULL -- If project ends, scientist is unassigned
        ON UPDATE CASCADE
);

CREATE TABLE SERUM (
    Serum_ID INT AUTO_INCREMENT PRIMARY KEY,
    Serum_Name VARCHAR(100) NOT NULL UNIQUE,
    Formula_Code VARCHAR(50) NOT NULL UNIQUE,
    Target_Effect TEXT,
    Creation_Date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- This table represents a multi-valued attribute for Pokemon
CREATE TABLE POKEMON_TYPE (
    Pokemon_ID INT,
    Type VARCHAR(50) NOT NULL,
    PRIMARY KEY (Pokemon_ID, Type), -- Composite Primary Key
    FOREIGN KEY (Pokemon_ID) REFERENCES POKEMON(Pokemon_ID)
        ON DELETE CASCADE -- If Pokemon is deleted, its type data is deleted
        ON UPDATE CASCADE
);

-- This table represents a log of experiments for a project
CREATE TABLE EXPERIMENTAL_LOG (
    Project_ID INT,
    Log_ID INT,
    Objective TEXT,
    `Status` Enum('Planned', 'In Progress', 'Successful', 'Failed', 'Cancelled') DEFAULT 'Planned',
    StartDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (Project_ID, Log_ID), -- Composite Primary Key
    FOREIGN KEY (Project_ID) REFERENCES RESEARCH_PROJECT(Project_ID)
        ON DELETE CASCADE -- If project is deleted, its logs are deleted
        ON UPDATE CASCADE
);

-- ====== GROUP 4: Associative Entities (Junction Tables) ======
-- These tables model the M:N relationships from the ERD.

-- Simple M:N relationship between PERSONNEL and MISSION (Redundant but requested)
CREATE TABLE ASSIGNED_TO (
    Personnel_ID INT,
    Mission_ID INT,
    PRIMARY KEY (Personnel_ID, Mission_ID),
    FOREIGN KEY (Personnel_ID) REFERENCES PERSONNEL(Personnel_ID)
        ON DELETE CASCADE -- If person is removed, assignment is removed
        ON UPDATE CASCADE,
    FOREIGN KEY (Mission_ID) REFERENCES MISSION(Mission_ID)
        ON DELETE CASCADE -- If mission is removed, assignment is removed
        ON UPDATE CASCADE
);

-- M:N relationship between MISSION and PERSONNEL
CREATE TABLE MISSION_ASSIGNMENT (
    Mission_ID INT,
    Personnel_ID INT,
    Role VARCHAR(100),
    AssignedDate DATE,
    `Status` ENUM('Assigned', 'Engaged', 'Battle Lost', 'Travelling', 'Compromised') DEFAULT 'Assigned',
    PRIMARY KEY (Mission_ID, Personnel_ID),
    FOREIGN KEY (Mission_ID) REFERENCES MISSION(Mission_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Personnel_ID) REFERENCES PERSONNEL(Personnel_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- M:N relationship between MISSION and ASSET
CREATE TABLE MISSION_ASSETS (
    Mission_ID INT,
    Asset_Code VARCHAR(50),
    Acquisition_Status ENUM('Pending', 'Acquired', 'Lost', 'Returned') DEFAULT 'Pending',
    PRIMARY KEY (Mission_ID, Asset_Code),
    FOREIGN KEY (Mission_ID) REFERENCES MISSION(Mission_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Asset_Code) REFERENCES ASSET(Asset_Code)
        ON DELETE RESTRICT -- Don't delete an asset if it's tied to a mission log
        ON UPDATE CASCADE
);

-- M:N relationship between PERSONNEL and POKEMON
CREATE TABLE OWNERSHIP (
    Personnel_ID INT,
    Pokemon_ID INT,
    PRIMARY KEY (Personnel_ID, Pokemon_ID),
    FOREIGN KEY (Personnel_ID) REFERENCES PERSONNEL(Personnel_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Pokemon_ID) REFERENCES POKEMON(Pokemon_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Ternary (3-way) relationship between GRUNT, TRAINER, and MISSION
CREATE TABLE FIELD_ENGAGEMENT (
    Grunt_Personnel_ID INT,
    Trainer_ID INT,
    Mission_ID INT,
    Pokemon_ID INT,
    PRIMARY KEY (Grunt_Personnel_ID, Trainer_ID, Mission_ID),
    FOREIGN KEY (Grunt_Personnel_ID) REFERENCES GRUNT(Grunt_Personnel_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Trainer_ID) REFERENCES TRAINER(Trainer_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Mission_ID) REFERENCES MISSION(Mission_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Pokemon_ID) REFERENCES POKEMON(Pokemon_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 4-way relationship for logging experiment events
CREATE TABLE EXPERIMENTATION_EVENT (
    Scientist_Personnel_ID INT,
    Serum_ID INT,
    Pokemon_ID INT,
    Project_ID INT,
    PRIMARY KEY (Scientist_Personnel_ID, Serum_ID, Pokemon_ID, Project_ID),
    FOREIGN KEY (Scientist_Personnel_ID) REFERENCES SCIENTIST(Scientist_Personnel_ID)
        ON DELETE RESTRICT -- Can't delete entities that are part of a logged event
        ON UPDATE CASCADE,
    FOREIGN KEY (Serum_ID) REFERENCES SERUM(Serum_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (Pokemon_ID) REFERENCES POKEMON(Pokemon_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (Project_ID) REFERENCES RESEARCH_PROJECT(Project_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


-- ====== GROUP 5: Resolving Circular Dependencies ======
-- Now that the BASE table exists, we can add the foreign key
-- constraint to the PERSONNEL table, completing the loop.

ALTER TABLE PERSONNEL
ADD CONSTRAINT fk_personnel_base
    FOREIGN KEY (Base_ID) REFERENCES BASE(Base_ID)
    ON DELETE SET RESTRICT -- (This enforces that a Base cannot be deleted if personnel are still assigned)
    ON UPDATE CASCADE;

-- --- End of schema.sql ---
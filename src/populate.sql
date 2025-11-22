-- Phase 4: Data Population (Enhanced Dataset)
-- populate.sql: Populates chimera_db with dense, interconnected data.
-- Includes 1:N, N:1, and M:N relationships to fully test system logic.

USE chimera_db;

-- ============================================================
-- GROUP 1: Independent Entities
-- ============================================================

INSERT INTO TRAINER (Name, Affiliation, NotorietyScore) VALUES
('Red', 'Kanto Champion', 950),
('Blue', 'Viridian Gym Leader', 800),
('Cynthia', 'Sinnoh Champion', 1200),
('Lance', 'Dragon Master', 900),
('Steven', 'Hoenn Champion', 920),
('Wallace', 'Sootopolis Gym Leader', 700),
('Alder', 'Unova Champion', 850),
('Diantha', 'Kalos Champion', 880),
('Leon', 'Galar Champion', 930),
('Geeta', 'Paldea Champion', 870),
('Brock', 'Pewter Gym Leader', 300),
('Misty', 'Cerulean Gym Leader', 320),
('Lt. Surge', 'Vermilion Gym Leader', 350),
('Erika', 'Celadon Gym Leader', 330),
('Sabrina', 'Saffron Gym Leader', 400),
('Koga', 'Fuchsia Gym Leader', 380),
('Blaine', 'Cinnabar Gym Leader', 360),
('Falkner', 'Violet Gym Leader', 250),
('Bugsy', 'Azalea Gym Leader', 260),
('Whitney', 'Goldenrod Gym Leader', 280),
('Morty', 'Ecruteak Gym Leader', 290),
('Chuck', 'Cianwood Gym Leader', 310),
('Jasmine', 'Olivine Gym Leader', 300),
('Pryce', 'Mahogany Gym Leader', 340),
('Clair', 'Blackthorn Gym Leader', 390),
('Roxanne', 'Rustboro Gym Leader', 270),
('Brawly', 'Dewford Gym Leader', 280),
('Wattson', 'Mauville Gym Leader', 290),
('Flannery', 'Lavaridge Gym Leader', 300),
('Norman', 'Petalburg Gym Leader', 350);

INSERT INTO RESEARCH_PROJECT (Title, `Status`, StartDate, EndDate) VALUES
('Project Apex', 'Active', '2023-01-15', NULL),
('Project Vesper', 'On Hold', '2023-06-01', '2024-01-15'),
('Project Chimera', 'Completed', '2022-03-10', '2022-12-31'),
('Project Abyss', 'Active', '2024-02-20', NULL),
('Project Nova', 'Planning', '2025-01-01', NULL),
('Project Umbra', 'Cancelled', '2023-03-01', '2023-04-01'),
('Project Genesis', 'Completed', '2021-01-01', '2022-01-01'),
('Project Overlord', 'Active', '2024-05-15', NULL),
('Project Aegis', 'On Hold', '2024-07-01', NULL),
('Project Midas', 'Planning', '2025-03-01', NULL);

INSERT INTO ASSET (Asset_Code, Asset_Type, Value_Estimate) VALUES
('CH-HELI-01', 'Stealth Helicopter', 1500000.00),
('MB-PROTO-01', 'Master Ball Prototype', 750000.00),
('LAB-EQUIP-A', 'Genetic Sequencer', 300000.00),
('VEH-TRN-01', 'Armored Transport Truck', 180000.00),
('VEH-TRN-02', 'Armored Transport Truck', 180000.00),
('DRN-SC-01', 'Scout Drone', 15000.00),
('DRN-SC-02', 'Scout Drone', 15000.00),
('DRN-SC-03', 'Scout Drone', 15000.00),
('DRN-CM-01', 'Combat Drone', 75000.00),
('DRN-CM-02', 'Combat Drone', 75000.00),
('WPN-SYS-A', 'EM Pulse Generator', 450000.00),
('WPN-SYS-B', 'Sonar Disruptor', 220000.00),
('COMP-SYS-01', 'Mainframe Supercomputer', 2000000.00),
('COMP-SYS-02', 'Data Encryption Node', 50000.00),
('INTEL-001', 'Sinnoh League Data', 100000.00),
('INTEL-002', 'Silph Co. Schematics', 250000.00),
('INTEL-003', 'Trainer Red Pathing', 30000.00),
('SAFE-001', 'Vibranium-Alloy Safe', 80000.00),
('SAFE-002', 'Vibranium-Alloy Safe', 80000.00),
('CHEM-001', 'Rare Candy Synthesis Kit', 120000.00),
('CHEM-002', 'Ability Capsule Formula', 300000.00),
('ARMOR-001', 'Grunt Body Armor (Set of 10)', 20000.00),
('ARMOR-002', 'Grunt Body Armor (Set of 10)', 20000.00),
('ARMOR-003', 'Grunt Body Armor (Set of 10)', 20000.00),
('SUB-001', 'Deep-Sea Submarine', 3500000.00),
('SAT-UPLINK-01', 'Satellite Uplink', 900000.00),
('KEY-001', 'Silph Co. Master Keycard', 500000.00),
('KEY-002', 'Cinnabar Lab Keycard', 150000.00),
('GEM-001', 'Large Diamond Cluster', 400000.00),
('GEM-002', 'Ancient Amber', 200000.00);

INSERT INTO SERUM (Serum_Name, Formula_Code, Target_Effect) VALUES
('S-22 (Growth)', 'FOR-GRO-022', 'Accelerates subject growth.'),
('X-05 (Aggression)', 'FOR-AGGRO-005', 'Induces heightened aggression.'),
('R-01 (Pacify)', 'FOR-PAC-001', 'Calming agent for subduing subjects.'),
('E-12 (Evolve)', 'FOR-EVO-012', 'Forces premature evolution.'),
('D-09 (Devolve)', 'FOR-DEV-009', 'Reverts evolution. Unstable.'),
('P-01 (Power)', 'FOR-PWR-001', 'Temporary boost to Attack/Defense.'),
('S-03 (Speed)', 'FOR-SPD-003', 'Temporary boost to Speed.'),
('I-07 (Intellect)', 'FOR-INT-007', 'Boosts psychic potential.'),
('C-04 (Clone)', 'FOR-CLO-004', 'Stabilizes cloning process.'),
('H-11 (Heal)', 'FOR-REG-011', 'Rapid cellular regeneration.'),
('S-30 (Stealth)', 'FOR-STL-030', 'Camouflage properties.'),
('F-01 (Fear)', 'FOR-FER-001', 'Induces panic in target.'),
('B-02 (Befriend)', 'FOR-BND-002', 'Increases loyalty/docility.'),
('T-08 (Toxic)', 'FOR-TOX-008', 'Potent, fast-acting poison.'),
('A-06 (Antidote)', 'FOR-ANT-006', 'Universal antidote base.'),
('F-10 (Flame)', 'FOR-FLM-010', 'Compound for fire-type boost.'),
('W-10 (Water)', 'FOR-AQA-010', 'Compound for water-type boost.'),
('E-10 (Electric)', 'FOR-ELC-010', 'Compound for electric-type boost.'),
('G-10 (Grass)', 'FOR-GRS-010', 'Compound for grass-type boost.'),
('I-10 (Ice)', 'FOR-ICE-010', 'Compound for ice-type boost.'),
('P-10 (Psychic)', 'FOR-PSY-010', 'Compound for psychic-type boost.'),
('D-10 (Dark)', 'FOR-DRK-010', 'Compound for dark-type boost.'),
('S-10 (Steel)', 'FOR-STL-010', 'Compound for steel-type boost.'),
('F-11 (Fairy)', 'FOR-FAY-011', 'Compound for fairy-type boost.'),
('D-11 (Dragon)', 'FOR-DRA-011', 'Compound for dragon-type boost.'),
('G-11 (Ghost)', 'FOR-GST-011', 'Compound for ghost-type boost.'),
('R-11 (Rock)', 'FOR-RCK-011', 'Compound for rock-type boost.'),
('G-12 (Ground)', 'FOR-GRD-012', 'Compound for ground-type boost.'),
('F-12 (Flying)', 'FOR-FLY-012', 'Compound for flying-type boost.'),
('N-12 (Normal)', 'FOR-NOR-012', 'Placebo, no effect.');


-- ============================================================
-- GROUP 2: Core Entities (Personnel & Pokemon)
-- ============================================================

INSERT INTO PERSONNEL (Personnel_ID, FName, LName, `Rank`, StartDate) VALUES
-- Bosses (3)
(1, 'Silas', 'Vane', 'Boss', '2020-01-01'),
(2, 'Serena', 'Kross', 'Boss', '2021-06-01'),
(3, 'Marcus', 'Grave', 'Boss', '2020-03-01'),
(31, 'Silva', 'Kane', 'Boss', '2020-03-01'),
(32, 'Poseidon', 'Payne', 'Boss', '2020-03-01'),
-- Scientists (12)
(4, 'Aris', 'Thorne', 'Scientist', '2020-03-15'),
(5, 'Evelyn', 'Reed', 'Scientist', '2021-05-10'),
(6, 'Dr. Kenji', 'Nomura', 'Scientist', '2022-02-01'),
(7, 'Elara', 'Vance', 'Scientist', '2022-07-15'),
(8, 'Felix', 'Hale', 'Scientist', '2023-01-20'),
(9, 'Gideon', 'Marr', 'Scientist', '2023-08-01'),
(10, 'Inara', 'Sol', 'Scientist', '2023-11-11'),
(11, 'Jonas', 'Wren', 'Scientist', '2024-03-01'),
(12, 'Lyra', 'Chen', 'Scientist', '2024-06-10'),
(13, 'Milo', 'Iskra', 'Scientist', '2024-09-01'),
(14, 'Nadia', 'Petrov', 'Scientist', '2025-01-15'),
(15, 'Orion', 'Black', 'Scientist', '2025-05-20'),
-- Grunts (15)
(16, 'Kai', 'Orion', 'Grunt', '2023-01-20'),
(17, 'Ria', 'Volkov', 'Grunt', '2023-01-20'),
(18, 'Jax', 'Hammer', 'Grunt', '2024-02-10'),
(19, 'Anya', 'Mishka', 'Grunt', '2023-04-15'),
(20, 'Bram', 'Stoker', 'Grunt', '2023-04-15'),
(21, 'Cora', 'Lin', 'Grunt', '2023-07-01'),
(22, 'Dax', 'Roland', 'Grunt', '2023-07-01'),
(23, 'Ezra', 'Finn', 'Grunt', '2024-01-30'),
(24, 'Faye', 'Valen', 'Grunt', '2024-01-30'),
(25, 'Garrus', 'Vak', 'Grunt', '2024-05-05'),
(26, 'Hana', 'Oda', 'Grunt', '2024-05-05'),
(27, 'Ivan', 'Dragov', 'Grunt', '2024-08-10'),
(28, 'Jett', 'Kuso', 'Grunt', '2024-08-10'),
(29, 'Kara', 'Sorel', 'Grunt', '2025-01-01'),
(30, 'Leon', 'S.', 'Grunt', '2025-01-01');

INSERT INTO POKEMON (Pokemon_ID, Name, HP, Attack, Defense, Project_ID) VALUES
(1, 'Chimera-001', 120, 110, 90, 1),   -- Project Apex
(2, 'Mewtwo-C', 106, 154, 90, 3),      -- Project Chimera
(3, 'Test Subject Rattata', 30, 56, 35, 2), -- Project Vesper
(4, 'Test Subject Pidgey', 40, 45, 40, 2), -- Project Vesper
(5, 'Persian', 65, 70, 60, NULL),
(6, 'Zubat', 40, 45, 35, NULL),
(7, 'Ekans', 35, 60, 44, NULL),
(8, 'Abyss-001', 150, 80, 130, 4),    -- Project Abyss
(9, 'Genesis-001', 100, 100, 100, 7), -- Project Genesis
(10, 'Overlord-001', 130, 130, 80, 8), -- Project Overlord
(11, 'Machamp', 90, 130, 80, NULL),
(12, 'Alakazam', 55, 50, 45, NULL),
(13, 'Golem', 80, 120, 130, NULL),
(14, 'Magneton', 50, 60, 95, NULL),
(15, 'Arcanine', 90, 110, 80, NULL),
(16, 'Gyarados', 95, 125, 79, NULL),
(17, 'Houndoom', 75, 90, 50, NULL),
(18, 'Tyranitar', 100, 134, 110, NULL),
(19, 'Rhydon', 105, 130, 120, NULL),
(20, 'Koffing', 40, 65, 95, NULL),
(21, 'Weezing', 65, 90, 120, NULL),
(22, 'Gengar', 60, 65, 60, NULL),
(23, 'Scyther', 70, 110, 80, NULL),
(24, 'Pinsir', 65, 125, 100, NULL),
(25, 'Tauros', 75, 100, 95, NULL),
(26, 'Aerodactyl', 80, 105, 65, 7), -- Project Genesis (revived)
(27, 'Kabutops', 60, 115, 105, 7), -- Project Genesis (revived)
(28, 'Omastar', 70, 60, 125, 7), -- Project Genesis (revived)
(29, 'Vesper-001', 1, 1, 1, 2), -- Project Vesper (failed)
(30, 'Apex-002', 100, 100, 100, 1); -- Project Apex


-- ============================================================
-- GROUP 3: Hierarchy & Specialization
-- ============================================================

INSERT INTO BOSS (Boss_Personnel_ID, Region_Managed) VALUES
(1, 'Kanto & Johto'),
(2, 'Hoenn & Sinnoh'),
(3, 'Unova'),
(31, 'Alola'),
(32, 'Galar');

INSERT INTO BASE (Name, Location, `Status`, Boss_ID) VALUES
('Chimera HQ', 'Unknown Island, Kanto', 'Active', 1),
('Outpost Delta', 'Johto Route 45', 'Inactive', 2),
('Minos Station', 'Hoenn, Mt. Chimney', 'Active', 3),
('Aether Lab', 'Sinnoh, Veilstone', 'Under Construction', 31),
('Castelia Stronghold', 'Unova, Castelia Sewers', 'Active', 32);

-- 1:N Relationship (One Boss manages multiple Squads)
INSERT INTO SQUADS (Boss_ID) VALUES
(1), (1), (1), (1), -- 4 Kanto/Johto Squads
(2), (2), (2), -- 3 Hoenn/Sinnoh Squads
(3), (3), (3); -- 3 Unova Squads

INSERT INTO GRUNT (Grunt_Personnel_ID, Squad_ID) VALUES
(16, 1), (17, 1), -- Kai, Ria (Squad 1)
(18, 2), -- Jax (Squad 2)
(19, 2), -- Anya (Squad 2)
(20, 3), -- Bram (Squad 3)
(21, 3), -- Cora (Squad 3)
(22, 4), -- Dax (Squad 4)
(23, 5), -- Ezra (Squad 5)
(24, 5), -- Faye (Squad 5)
(25, 6), -- Garrus (Squad 6)
(26, 6), -- Hana (Squad 6)
(27, 7), -- Ivan (Squad 7)
(28, 8), -- Jett (Squad 8)
(29, 9), -- Kara (Squad 9)
(30, 10); -- Leon (Squad 10)

-- 1:N Relationship (One Project has multiple Scientists)
INSERT INTO SCIENTIST (Scientist_Personnel_ID, Specialization, Project_ID) VALUES
(4, 'Genetics', 1),  -- Aris on Apex
(5, 'Biochemistry', 2),         -- Evelyn on Vesper
(6, 'Cloning', 3),              -- Kenji on Chimera
(7, 'Marine Biology', 4),       -- Elara on Abyss
(8, 'Physics', 5),              -- Felix on Nova
(9, 'Data Science', 8),         -- Gideon on Overlord
(10, 'Robotics', 9),            -- Inara on Aegis
(11, 'Paleontology', 7),        -- Jonas on Genesis
(12, 'Biochemistry', 1),        -- Lyra on Apex
(13, 'Genetics', 1), -- Milo on Apex
(14, 'Cloning', 3),             -- Nadia on Chimera
(15, 'Weaponry', 8);            -- Orion on Overlord

INSERT INTO POKEMON_TYPE (Pokemon_ID, Type) VALUES
(1, 'Dark'), (1, 'Psychic'),
(2, 'Psychic'),
(3, 'Normal'),
(4, 'Normal'), (4, 'Flying'),
(5, 'Normal'),
(6, 'Poison'), (6, 'Flying'),
(7, 'Poison'),
(8, 'Water'), (8, 'Dark'),
(9, 'Normal'),
(10, 'Fire'), (10, 'Fighting'),
(11, 'Fighting'),
(12, 'Psychic'),
(13, 'Rock'), (13, 'Ground'),
(14, 'Electric'), (14, 'Steel'),
(15, 'Fire'),
(16, 'Water'), (16, 'Flying'),
(17, 'Dark'), (17, 'Fire'),
(18, 'Rock'), (18, 'Dark'),
(19, 'Ground'), (19, 'Rock'),
(20, 'Poison'),
(21, 'Poison'),
(22, 'Ghost'), (22, 'Poison'),
(23, 'Bug'), (23, 'Flying'),
(24, 'Bug'),
(25, 'Normal'),
(26, 'Rock'), (26, 'Flying'),
(27, 'Rock'), (27, 'Water'),
(28, 'Rock'), (28, 'Water'),
(29, 'Normal'),
(30, 'Psychic');

INSERT INTO EXPERIMENTAL_LOG (Project_ID, Log_ID, Objective, `Status`) VALUES
(1, 1, 'Initial gene splicing stability test.', 'Successful'),
(1, 2, 'Introduce external stimulus.', 'In Progress'),
(1, 3, 'Test S-22 (Growth) serum.', 'Planned'),
(2, 1, 'Test X-05 (Aggression) on Subject Rattata.', 'Failed'),
(2, 2, 'Test R-01 (Pacify) on Subject Pidgey.', 'Successful'),
(2, 3, 'Subject 001 (Vesper) failed to vitalize.', 'Failed'),
(3, 1, 'Initial DNA sequencing from fossil.', 'Successful'),
(3, 2, 'Cloning vat stability check.', 'Successful'),
(3, 3, 'Subject Mewtwo-C vitalized.', 'Successful'),
(4, 1, 'Deep sea pressure vessel test.', 'Successful'),
(4, 2, 'Subject Abyss-001 capture.', 'Successful'),
(4, 3, 'Sonar disruption test.', 'Planned'),
(5, 1, 'Theoretical calculations for wormhole.', 'In Progress'),
(7, 1, 'Amber sample 1 revival.', 'Successful'),
(7, 2, 'Amber sample 2 revival.', 'Failed'),
(7, 3, 'Dome fossil 1 revival.', 'Successful'),
(7, 4, 'Helix fossil 1 revival.', 'Successful'),
(7, 5, 'Test E-12 (Evolve) on revived subjects.', 'Cancelled'),
(8, 1, 'Network infiltration of Silph Co.', 'Successful'),
(8, 2, 'AI "Overlord" protocol boot-up.', 'In Progress'),
(8, 3, 'Test WPN-SYS-A.', 'Planned'),
(9, 1, 'Design combat drone housing.', 'Successful'),
(9, 2, 'Integrate AI with drone chassis.', 'In Progress'),
(10, 1, 'Analyze market data for Rare Candy.', 'In Progress'),
(10, 2, 'Formulate business plan.', 'Planned'),
(1, 4, 'Test P-01 (Power) on Apex-002.', 'Successful'),
(1, 5, 'Test I-07 (Intellect) on Apex-002.', 'In Progress'),
(3, 4, 'Test C-04 (Clone) stability.', 'Successful'),
(3, 5, 'Psychic potential test for Mewtwo-C.', 'Successful'),
(8, 4, 'Steal Master Ball prototype.', 'Successful');


-- ============================================================
-- GROUP 4: Missions & M:N Relationships
-- ============================================================

INSERT INTO MISSION (Objective, `Status`, StartDate, Target_Trainer_ID) VALUES
('Capture Legendary Pokemon in Mt. Moon.', 'Active', '2025-11-10', NULL),
('Ambush and battle Trainer Red at Indigo Plateau.', 'Pending', '2025-11-20', 1),
('Steal research from Cinnabar Lab.', 'Completed', '2024-08-15', NULL),
('Disrupt Viridian Gym Leader Blue.', 'Failed', '2024-05-01', 2),
('Steal Silph Co. Master Keycard.', 'Active', '2025-11-01', NULL),
('Capture test subjects from Safari Zone.', 'Completed', '2024-09-10', NULL),
('Infiltrate a meeting of regional Champions.', 'Pending', '2025-12-01', 3),
('Sabotage Hoenn League computer systems.', 'Active', '2025-10-15', 5),
('Steal data from Devon Corporation.', 'Completed', '2024-11-20', NULL),
('Ambush Trainer Lance at Dragon''s Den.', 'Failed', '2024-06-01', 4),
('Monitor Gym Leader Sabrina.', 'Completed', '2024-07-07', 15),
('Test WPN-SYS-B at Cerulean Cape.', 'Active', '2025-11-12', NULL),
('Deliver package to Outpost Delta.', 'Aborted', '2024-10-01', NULL),
('Extract "Project Midas" scientist.', 'Pending', '2025-04-01', NULL),
('Ambush Gym Leader Whitney.', 'Failed', '2024-03-10', 20),
('Scout Petalburg Gym.', 'Completed', '2024-12-01', 30),
('Test S-03 (Speed) in a field test.', 'Completed', '2024-08-01', NULL),
('Test F-01 (Fear) in Viridian Forest.', 'Active', '2025-11-05', NULL),
('Steal fossils from Pewter Museum.', 'Completed', '2020-11-01', 11),
('Capture a rare Pokemon for Project Abyss.', 'Completed', '2024-02-19', NULL),
('Observe Trainer Leon in Galar.', 'Completed', '2024-05-05', 9),
('Place tracking device on Trainer Geeta.', 'Pending', '2025-11-18', 10),
('Guard Chimera HQ - Rotation 1.', 'Active', '2025-11-01', NULL),
('Guard Minos Station - Rotation A.', 'Active', '2025-11-01', NULL),
('Guard Castelia Stronghold - Week 45.', 'Active', '2025-11-01', NULL),
('Transport assets to Aether Lab.', 'Pending', '2025-11-25', NULL),
('Test X-05 (Aggression) in the field.', 'Failed', '2023-07-04', NULL),
('Acquire CHEM-001 from supplier.', 'Completed', '2024-09-09', NULL),
('Ambush Gym Leader Flannery.', 'Active', '2025-11-13', 29),
('Recover lost drone DRN-SC-03.', 'Pending', '2025-11-19', NULL);

-- M:N Relation: ASSIGNED_TO
-- NOTE: This data is a SUPERSET of MISSION_ASSIGNMENT.
-- It includes everyone with a specific role, PLUS additional oversight/backup personnel.

INSERT INTO ASSIGNED_TO (Personnel_ID, Mission_ID) VALUES
-- ==========================================================
-- SUBSET 1: Direct Mapping (Matches MISSION_ASSIGNMENT)
-- ==========================================================
(16, 1), (17, 1),         -- Mission 1
(18, 2),                  -- Mission 2
(4, 3),                   -- Mission 3
(16, 4),                  -- Mission 4
(19, 5), (20, 5), (2, 5), (9, 5), (23, 5), -- Mission 5
(21, 6), (22, 6),         -- Mission 6
(1, 7),                   -- Mission 7
(9, 8),                   -- Mission 8
(10, 9),                  -- Mission 9
(18, 10), (23, 10),       -- Mission 10
(24, 11),                 -- Mission 11
(15, 12),                 -- Mission 12
(25, 13),                 -- Mission 13
(26, 15), (27, 15),       -- Mission 15
(28, 16),                 -- Mission 16
(5, 17),                  -- Mission 17
(16, 18),                 -- Mission 18
(11, 19),                 -- Mission 19
(7, 20),                  -- Mission 20
(29, 21), (30, 21),       -- Mission 21
(25, 22),                 -- Mission 22
(16, 23), (17, 23),       -- Mission 23
(23, 24), (24, 24),       -- Mission 24
(27, 25), (28, 25),       -- Mission 25
(10, 26), (25, 26),       -- Mission 26
(5, 27),                  -- Mission 27
(5, 28),                  -- Mission 28
(18, 29), (26, 29),       -- Mission 29
(22, 30),                 -- Mission 30

-- ==========================================================
-- SUBSET 2: Superset Additions (Oversight & Backup)
-- These personnel are assigned but have no specific role in MISSION_ASSIGNMENT
-- ==========================================================
(4, 1),  -- Scientist Aris observing Mission 1 (Apex field test)
(1, 1),  -- Boss Silas overseeing Mission 1
(3, 2),  -- Boss Marcus monitoring the failed ambush on Red
(30, 2), -- Grunt Leon providing backup for Mission 2
(31, 4), -- Boss Silva monitoring the sabotage in Hoenn
(1, 5),  -- Boss Silas attached to the "All Hands" mission (Strategic Command)
(15, 8), -- Scientist Orion reviewing data from Mission 8
(3, 10), -- Boss Marcus reviewing the failure at Dragon's Den
(32, 12),-- Boss Poseidon authorizing WPN-SYS-B test
(14, 17),-- Scientist Nadia analyzing speed serum field data
(2, 19), -- Boss Serena overseeing fossil theft
(3, 20), -- Boss Marcus overseeing Project Abyss capture
(1, 23), -- Boss Silas doing a surprise inspection of HQ Guards
(8, 25), -- Scientist Felix checking Castelia Stronghold defenses
(31, 26);-- Boss Silva waiting for assets at Aether Lab

-- M:N Relation: MISSION_ASSIGNMENT
-- Demonstration: One Mission with MANY personnel (Mission 5).
-- Demonstration: One Person with MANY missions (Grunt Kai - ID 16).
INSERT INTO MISSION_ASSIGNMENT (Mission_ID, Personnel_ID, Role, `Status`) VALUES
(1, 16, 'Field Operative', 'Engaged'), (1, 17, 'Field Operative', 'Travelling'),
(2, 18, 'Field Leader', 'Assigned'),
(3, 4, 'Infiltrator', 'Engaged'),
(4, 16, 'Saboteur', 'Battle Lost'),
-- Mission 5: "All Hands on Deck" (Boss, Scientist, Grunts)
(5, 19, 'Infiltrator', 'Engaged'), (5, 20, 'Lookout', 'Engaged'),
(5, 2, 'Tactical Overseer', 'Engaged'), (5, 9, 'Cyber Warfare', 'Engaged'), (5, 23, 'Crowd Control', 'Engaged'),
(6, 21, 'Wrangler', 'Engaged'), (6, 22, 'Wrangler', 'Engaged'),
(7, 1, 'Observer', 'Assigned'),
(8, 9, 'Hacker', 'Engaged'),
(9, 10, 'Infiltrator', 'Engaged'),
(10, 18, 'Field Leader', 'Battle Lost'), (10, 23, 'Field Operative', 'Battle Lost'),
(11, 24, 'Surveillance', 'Engaged'),
(12, 15, 'Technician', 'Engaged'),
(13, 25, 'Courier', 'Travelling'),
(15, 26, 'Field Operative', 'Battle Lost'), (15, 27, 'Field Operative', 'Battle Lost'),
(16, 28, 'Scout', 'Engaged'),
(17, 5, 'Field Scientist', 'Engaged'),
(18, 16, 'Field Operative', 'Engaged'),
(19, 11, 'Acquisition', 'Engaged'),
(20, 7, 'Field Scientist', 'Engaged'),
(21, 29, 'Scout', 'Engaged'), (21, 30, 'Scout', 'Engaged'),
(22, 25, 'Scout', 'Assigned'),
-- Mission 23: Guard Rotation (Many personnel)
(23, 16, 'Guard', 'Engaged'), (23, 17, 'Guard', 'Engaged'),
(24, 23, 'Guard', 'Engaged'), (24, 24, 'Guard', 'Engaged'),
(25, 27, 'Guard', 'Engaged'), (25, 28, 'Guard', 'Engaged'),
(26, 10, 'Technician', 'Assigned'), (26, 25, 'Security', 'Assigned'),
(27, 5, 'Field Scientist', 'Battle Lost'),
(28, 5, 'Logistics', 'Engaged'),
(29, 18, 'Field Leader', 'Engaged'), (29, 26, 'Field Operative', 'Engaged'),
(30, 22, 'Recovery', 'Assigned');

-- M:N Relation: MISSION_ASSETS
-- Demonstration: One Asset used in MANY missions (CH-HELI-01).
-- Demonstration: One Mission using MANY assets (Mission 25).
INSERT INTO MISSION_ASSETS (Mission_ID, Asset_Code, Acquisition_Status) VALUES
(1, 'CH-HELI-01', 'Acquired'),
(2, 'MB-PROTO-01', 'Pending'),
(3, 'KEY-002', 'Acquired'),
(4, 'DRN-SC-01', 'Lost'),
-- Mission 5 Asset Heavy
(5, 'KEY-001', 'Pending'), (5, 'CH-HELI-01', 'Acquired'),
(6, 'VEH-TRN-01', 'Returned'),
(7, 'INTEL-001', 'Pending'),
(8, 'COMP-SYS-02', 'Acquired'),
(9, 'INTEL-002', 'Acquired'),
(10, 'DRN-CM-01', 'Lost'), (10, 'DRN-CM-02', 'Acquired'),
(11, 'DRN-SC-02', 'Returned'),
(12, 'WPN-SYS-B', 'Acquired'),
(13, 'VEH-TRN-02', 'Returned'),
(15, 'ARMOR-001', 'Lost'),
(16, 'INTEL-003', 'Acquired'),
(17, 'CHEM-002', 'Acquired'),
(18, 'CHEM-001', 'Acquired'),
(19, 'GEM-002', 'Acquired'),
(20, 'SUB-001', 'Acquired'),
(21, 'SAT-UPLINK-01', 'Acquired'),
(22, 'DRN-SC-01', 'Pending'),
(23, 'ARMOR-002', 'Acquired'), (23, 'CH-HELI-01', 'Acquired'),
(24, 'ARMOR-003', 'Acquired'),
-- Mission 25: Heavy Defense (Multiple assets)
(25, 'COMP-SYS-02', 'Acquired'), (25, 'WPN-SYS-A', 'Acquired'), (25, 'DRN-CM-01', 'Acquired'), (25, 'DRN-CM-02', 'Acquired'),
(26, 'VEH-TRN-01', 'Pending'), (26, 'VEH-TRN-02', 'Pending'),
(27, 'WPN-SYS-A', 'Acquired'),
(28, 'CHEM-001', 'Acquired'),
(29, 'GEM-001', 'Pending'), (29, 'CH-HELI-01', 'Pending'),
(30, 'DRN-SC-03', 'Pending');

-- M:N Relation: OWNERSHIP
-- Demonstration: One Person owning MANY Pokemon.
-- Demonstration: One Pokemon owned by MANY Personnel (Shared Custody).
INSERT INTO OWNERSHIP (Personnel_ID, Pokemon_ID) VALUES
(1, 5), -- Boss Silas, Persian
(1, 18), -- Boss Silas, Tyranitar
(1, 2), -- Boss Silas, Mewtwo-C (Shared Oversight)
(4, 1), -- Scientist Aris, Chimera-001
(4, 30), -- Scientist Aris, Apex-002
(4, 2), -- Scientist Aris, Mewtwo-C (Shared Oversight)
(6, 2), -- Scientist Kenji, Mewtwo-C (Original Creator)
(5, 3), -- Scientist Evelyn, Rattata
(5, 4), -- Scientist Evelyn, Pidgey
(5, 29), -- Scientist Evelyn, Vesper-001
(7, 8), -- Scientist Elara, Abyss-001
(9, 14), -- Scientist Gideon, Magneton
(11, 26), (11, 27), (11, 28), -- Scientist Jonas, Fossils
(8, 10), -- Scientist Felix, Overlord-001
(16, 6), -- Grunt Kai, Zubat
(17, 7), -- Grunt Ria, Ekans
(18, 11), -- Grunt Jax, Machamp
(19, 17), -- Grunt Anya, Houndoom
(20, 13), -- Grunt Bram, Golem
(21, 22), -- Grunt Cora, Gengar
(22, 19), -- Grunt Dax, Rhydon
(23, 12), -- Grunt Ezra, Alakazam
(24, 23), -- Grunt Faye, Scyther
(25, 24), -- Grunt Garrus, Pinsir
(25, 16), -- Grunt Garrus, Gyarados (Shared Transport)
(26, 25), -- Grunt Hana, Tauros
(27, 21), -- Grunt Ivan, Weezing
(27, 16), -- Grunt Ivan, Gyarados (Shared Transport)
(28, 20), -- Grunt Jett, Koffing
(28, 16), -- Grunt Jett, Gyarados (Shared Transport)
(29, 16), -- Grunt Kara, Gyarados
(30, 15), -- Grunt Leon, Arcanine
(2, 17), -- Boss Serena, Houndoom
(3, 11); -- Boss Marcus, Machamp

-- Ternary Relation: FIELD_ENGAGEMENT
-- Demonstration: Grunt Kai fighting Trainer Red across MULTIPLE missions.
INSERT INTO FIELD_ENGAGEMENT (Grunt_Personnel_ID, Trainer_ID, Mission_ID, Pokemon_ID) VALUES
(16, 2, 4, 6), -- Grunt Kai vs Trainer Blue on Mission 4 with Zubat
(18, 4, 10, 11), -- Grunt Jax vs Trainer Lance on Mission 10 with Machamp
(23, 4, 10, 12), -- Grunt Ezra vs Trainer Lance on Mission 10 with Alakazam
(26, 20, 15, 25), -- Grunt Hana vs Trainer Whitney on Mission 15 with Tauros
(27, 20, 15, 21), -- Grunt Ivan vs Trainer Whitney on Mission 15 with Weezing
(16, 11, 1, 6), -- Grunt Kai vs Trainer Brock on Mission 1 with Zubat
(17, 11, 1, 7), -- Grunt Ria vs Trainer Brock on Mission 1 with Ekans
(16, 12, 1, 6), -- Grunt Kai vs Trainer Misty on Mission 1 with Zubat
(17, 12, 1, 7), -- Grunt Ria vs Trainer Misty on Mission 1 with Ekans
(16, 13, 1, 6), -- Grunt Kai vs Trainer Lt. Surge on Mission 1 with Zubat
(17, 13, 1, 7), -- Grunt Ria vs Trainer Lt. Surge on Mission 1 with Ekans
(16, 14, 1, 6), -- Grunt Kai vs Trainer Erika on Mission 1 with Zubat
(17, 14, 1, 7), -- Grunt Ria vs Trainer Erika on Mission 1 with Ekans
(16, 15, 1, 6), -- Grunt Kai vs Trainer Sabrina on Mission 1 with Zubat
(17, 15, 1, 7), -- Grunt Ria vs Trainer Sabrina on Mission 1 with Ekans
(16, 16, 1, 6), -- Grunt Kai vs Trainer Koga on Mission 1 with Zubat
(17, 16, 1, 7), -- Grunt Ria vs Trainer Koga on Mission 1 with Ekans
-- The Kai vs Red Saga (Mission 2, 7, 20)
(16, 1, 2, 6), -- Grunt Kai vs Trainer Red on Mission 2
(16, 1, 7, 6), -- Grunt Kai vs Trainer Red on Mission 7 (Rivalry)
(16, 1, 20, 6), -- Grunt Kai vs Trainer Red on Mission 20 (Rivalry)
(17, 1, 2, 7), -- Grunt Ria vs Trainer Red on Mission 2
(18, 1, 2, 11), -- Grunt Jax vs Trainer Red on Mission 2
(19, 1, 2, 17), -- Grunt Anya vs Trainer Red on Mission 2
(20, 1, 2, 13), -- Grunt Bram vs Trainer Red on Mission 2
(21, 1, 2, 22), -- Grunt Cora vs Trainer Red on Mission 2
(22, 1, 2, 19), -- Grunt Dax vs Trainer Red on Mission 2
(23, 1, 2, 12), -- Grunt Ezra vs Trainer Red on Mission 2
(24, 1, 2, 23), -- Grunt Faye vs Trainer Red on Mission 2
(25, 1, 2, 24), -- Grunt Garrus vs Trainer Red on Mission 2
(26, 1, 2, 25), -- Grunt Hana vs Trainer Red on Mission 2
(27, 1, 2, 21), -- Grunt Ivan vs Trainer Red on Mission 2
(28, 1, 2, 20); -- Grunt Jett vs Trainer Red on Mission 2

INSERT INTO EXPERIMENTATION_EVENT (Scientist_Personnel_ID, Serum_ID, Pokemon_ID, Project_ID) VALUES
(5, 2, 3, 2), -- Evelyn, X-05 (Aggression), Rattata, Project Vesper
(5, 3, 4, 2), -- Evelyn, R-01 (Pacify), Pidgey, Project Vesper
(4, 1, 1, 1), -- Aris, S-22 (Growth), Chimera-001, Project Apex
(12, 1, 30, 1), -- Lyra, S-22 (Growth), Apex-002, Project Apex
(13, 4, 30, 1), -- Milo, E-12 (Evolve), Apex-002, Project Apex
(6, 9, 2, 3), -- Kenji, C-04 (Clone), Mewtwo-C, Project Chimera
(14, 9, 2, 3), -- Nadia, C-04 (Clone), Mewtwo-C, Project Chimera
(11, 4, 26, 7), -- Jonas, E-12 (Evolve), Aerodactyl, Project Genesis
(11, 4, 27, 7), -- Jonas, E-12 (Evolve), Kabutops, Project Genesis
(11, 4, 28, 7), -- Jonas, E-12 (Evolve), Omastar, Project Genesis
(4, 6, 1, 1), -- Aris, P-01 (Power), Chimera-001, Project Apex
(4, 7, 1, 1), -- Aris, S-03 (Speed), Chimera-001, Project Apex
(4, 8, 1, 1), -- Aris, I-07 (Intellect), Chimera-001, Project Apex
(5, 5, 3, 2), -- Evelyn, D-09 (Devolve), Rattata, Project Vesper
(12, 10, 30, 1), -- Lyra, H-11 (Heal), Apex-002, Project Apex
(13, 11, 30, 1), -- Milo, S-30 (Stealth), Apex-002, Project Apex
(6, 12, 2, 3), -- Kenji, F-01 (Fear), Mewtwo-C, Project Chimera
(14, 13, 2, 3), -- Nadia, B-02 (Befriend), Mewtwo-C, Project Chimera
(7, 14, 8, 4), -- Elara, T-08 (Toxic), Abyss-001, Project Abyss
(7, 15, 8, 4), -- Elara, A-06 (Antidote), Abyss-001, Project Abyss
(4, 16, 1, 1), -- Aris, F-10 (Flame), Chimera-001, Project Apex
(4, 17, 1, 1), -- Aris, W-10 (Water), Chimera-001, Project Apex
(4, 18, 1, 1), -- Aris, E-10 (Electric), Chimera-001, Project Apex
(4, 19, 1, 1), -- Aris, G-10 (Grass), Chimera-001, Project Apex
(4, 20, 1, 1), -- Aris, I-10 (Ice), Chimera-001, Project Apex
(4, 21, 1, 1), -- Aris, P-10 (Psychic), Chimera-001, Project Apex
(4, 22, 1, 1), -- Aris, D-10 (Dark), Chimera-001, Project Apex
(4, 23, 1, 1), -- Aris, S-10 (Steel), Chimera-001, Project Apex
(4, 24, 1, 1), -- Aris, F-11 (Fairy), Chimera-001, Project Apex
(4, 25, 1, 1); -- Aris, D-11 (Dragon), Chimera-001, Project Apex


-- ============================================================
-- GROUP 5: Circular Dependencies Fix
-- ============================================================

UPDATE PERSONNEL SET Base_ID = 1 WHERE Personnel_ID IN (1, 4, 5, 16, 17, 18, 19);
UPDATE PERSONNEL SET Base_ID = 2 WHERE Personnel_ID IN (20, 21, 22, 31);
UPDATE PERSONNEL SET Base_ID = 3 WHERE Personnel_ID IN (2, 6, 7, 23, 24, 25, 26);
UPDATE PERSONNEL SET Base_ID = 4 WHERE Personnel_ID IN (8, 9, 10, 11, 32);
UPDATE PERSONNEL SET Base_ID = 5 WHERE Personnel_ID IN (3, 12, 13, 14, 15, 27, 28, 29, 30);

-- --- End of populate.sql ---
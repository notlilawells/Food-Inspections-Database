-- opening the database
.open food-inspections.db

-- Creating TABLE: Inspection Results 
CREATE TABLE Inspection_Results(
  Result_ID INT NOT NULL,
  Results TEXT NOT NULL,
  PRIMARY KEY (Result_ID),
  FOREIGN KEY (Result_ID) REFERENCES Inspections (Result_ID));

-- Creating TABLE: Inspection Types
CREATE TABLE Inspection_Types(
  Inspection_Type_ID INT NOT NULL,
  Inspection_Type TEXT NOT NULL,
  PRIMARY KEY (Inspection_Type_ID),
  FOREIGN KEY (Inspection_Type_ID) REFERENCES Inspections (Inspection_Type_ID));

-- Creating TABLE: Risks
CREATE TABLE Risks(
  Risk_ID INT NOT NULL,
  Risk TEXT NOT NULL,
  PRIMARY KEY (Risk_ID),
  FOREIGN KEY (Risk_ID) REFERENCES Inspections (Risk_ID));

-- Creating TABLE: Store_Types
CREATE TABLE Store_Types(
  Store_Type_ID INT NOT NULL,
  Store_Type TEXT NOT NULL,
  PRIMARY KEY (Store_Type_ID),
  FOREIGN KEY (Store_Type_ID) REFERENCES Stores (Store_Type_ID));

-- Creating TABLE: Violations
CREATE TABLE Violations(
  Violation_ID INT NOT NULL,
  Violations TEXT NOT NULL,
  PRIMARY KEY (Violation_ID),
  FOREIGN KEY (Violation_ID) REFERENCES Inspections (Violation_ID));

-- -- Creating TABLE: Stores
CREATE TABLE Stores(
  Store_ID INT NOT NULL,
  Store_Name TEXT NOT NULL,
  License_Number INT NOT NULL,
  Address TEXT NOT NULL,
  Store_Type_ID INT NOT NULL,
  Zip_Code INT NOT NULL,
  Latitude INT NOT NULL,
  Longitude INT NOT NULL,
  PRIMARY KEY (Store_ID),
  FOREIGN KEY (Store_ID) REFERENCES Inspections (Store_ID),
  FOREIGN KEY (Store_Type_ID) REFERENCES Store_Types (Store_Type_ID));

-- -- Creating TABLE: Inspections
CREATE TABLE Inspections(
  Inspection_ID INT NOT NULL,
  Store_ID INT NOT NULL, 
  Inspection_Type_ID INT NOT NULL,
  Inspection_Year INT NOT NULL, 
  Violation_ID INT NOT NULL, 
  Risk_ID INT NOT NULL,
  Result_ID INT NOT NULL,
  PRIMARY KEY (Inspection_ID),
  FOREIGN KEY (Store_ID) REFERENCES Stores (Store_ID)
  FOREIGN KEY (Inspection_Type_ID) REFERENCES Inspection_Types (Inspection_Type_ID),
  FOREIGN KEY (Violation_ID) REFERENCES Violations (Violation_ID),
  FOREIGN KEY (Risk_ID) REFERENCES Risks (Risk_ID),
  FOREIGN KEY (Result_ID) REFERENCES Inspection_Results (Result_ID));


-- Importing the CSV filex
.mode csv

.import Inspection_Results.csv Inspection_Results
.import Inspection_Types.csv Inspection_Types 
.import Inspections.csv Inspections
.import Risks.csv Risks
.import Store_Types.csv Store_Types
.import Stores.csv Stores
.import Violations.csv Violations
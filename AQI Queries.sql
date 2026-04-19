-- 1. Create and use the Database
CREATE DATABASE AgriAura_DB;
USE AgriAura_DB;

-- 2. Create the Clean AQI Table
-- Matches your 'Clean_AQI_Final.csv'
CREATE TABLE Clean_AQI (
    Dist_Name VARCHAR(100),
    Year INT,
    Avg_O3 FLOAT,
    PRIMARY KEY (Dist_Name, Year)
);

-- 3. Create the Clean Crop Table
-- Matches your 'Clean_Crops_Final.csv'
CREATE TABLE Clean_Crops (
    Dist_Name VARCHAR(100),
    Year INT,
    Crop_Type VARCHAR(50),
    Yield_kg_per_ha FLOAT,
    PRIMARY KEY (Dist_Name, Year, Crop_Type)
);
SELECT 
    A.Dist_Name, 
    A.Year, 
    C.Crop_Type, 
    A.Avg_O3 as Ozone_Level, 
    C.Yield_kg_per_ha
FROM Clean_AQI A
JOIN Clean_Crops C ON A.Dist_Name = C.Dist_Name AND A.Year = C.Year;
SELECT 
    Dist_Name, 
    Year, 
    Avg_O3,
    -- Stress Logic: If Ozone > 40, show the impact
    CASE 
        WHEN Avg_O3 > 40 THEN ROUND((Avg_O3 - 40) * 0.8, 2) 
        ELSE 0 
    END AS Yield_Impact_Percent,
    -- Carbon Credit Logic: Based on yield (Oxygen output)
    ROUND(Avg_O3 * 0.15, 4) AS Carbon_Credit_Score
FROM Clean_AQI;
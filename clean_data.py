import pandas as pd

# --- CONFIGURATION ---
AQI_FILE = 'indian_cities_aqi.csv' 
CROP_FILE = 'Custom_Crops_yield_Historical_Dataset.csv'

def clean_data():
    print("🚀 Starting Data Cleaning...")

    # 1. Load AQI Data
    print("Reading AQI dataset...")
    aqi_df = pd.read_csv(AQI_FILE)
    
    # 2. Extract Year from datetime
    # We use the exact name you found: 'datetime'
    date_col = 'datetime' 
    
    print(f"Processing dates in '{date_col}' column...")
    aqi_df[date_col] = pd.to_datetime(aqi_df[date_col])
    aqi_df['Year'] = aqi_df[date_col].dt.year
    
    # 3. Standardize City Names
    # Check if your file uses 'city' or 'City' - standardizing to 'city' here
    city_col = 'city' if 'city' in aqi_df.columns else 'City'
    aqi_df.rename(columns={city_col: 'Dist Name'}, inplace=True)
    
    aqi_df['Dist Name'] = aqi_df['Dist Name'].str.strip().str.title()
    
    # 4. Load Crop Data
    print("Reading Crop dataset...")
    crop_df = pd.read_csv(CROP_FILE)
    crop_df['Dist Name'] = crop_df['Dist Name'].str.strip().str.title()

    # 5. Fix Spelling Mismatches
    mapping = {
        'Ahmadabad': 'Ahmedabad',
        'Bangalore': 'Bengaluru',
        'Bombay': 'Mumbai',
        'Calcutta': 'Kolkata'
    }
    aqi_df['Dist Name'] = aqi_df['Dist Name'].replace(mapping)
    crop_df['Dist Name'] = crop_df['Dist Name'].replace(mapping)

    # --- UPDATED STEP 6: Find the Ozone column dynamically ---
    # We look for any column containing 'o3' or 'ozone' (case insensitive)
    o3_options = [c for c in aqi_df.columns if 'o3' in c.lower() or 'ozone' in c.lower()]
    
    if not o3_options:
        print(f"❌ Error: Could not find an Ozone/O3 column. Available columns are: {list(aqi_df.columns)}")
        return
    
    o3_col = o3_options[0]
    print(f"✅ Found Ozone data in column: '{o3_col}'")

    # Filter and Remove Nulls
    aqi_clean = aqi_df.dropna(subset=[o3_col, 'Dist Name', 'Year'])
    crop_clean = crop_df.dropna(subset=['Yield_kg_per_ha', 'Dist Name', 'Year'])

    # --- UPDATED STEP 7: Aggregate ---
    print("Aggregating daily AQI to annual averages...")
    aqi_yearly = aqi_clean.groupby(['Dist Name', 'Year'])[o3_col].mean().reset_index()
    
    # Rename for the final SQL table
    aqi_yearly.rename(columns={o3_col: 'Avg_O3'}, inplace=True)

   

    # 8. Save the Clean Files
    print("Saving cleaned files...")
    aqi_yearly.to_csv('Clean_AQI_Final.csv', index=False)
    crop_clean.to_csv('Clean_Crops_Final.csv', index=False)
    
    print("✅ Done! Files are ready for MySQL.")

if __name__ == "__main__":
    clean_data()
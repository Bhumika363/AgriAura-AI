import mysql.connector
import pandas as pd
# --- ADD THESE SETTINGS ---
pd.set_option('display.max_columns', None)  # Don't hide columns
pd.set_option('display.expand_frame_repr', False)  # Don't wrap to a new line
pd.set_option('display.max_colwidth', None)  # Don't cut off long text in cells
import warnings

# Suppress the SQLAlchemy warning for a cleaner output
warnings.filterwarnings("ignore", category=UserWarning)

# --- NEW AI LOGIC BLOCK ---
def generate_recommendation(ozone, soil_condition):
    if soil_condition == "Acidification Risk":
        if ozone > 65:
            return "CRITICAL: Apply 2.5 tons/ha of Agricultural Lime and switch to Ozone-resistant Wheat varieties."
        else:
            return "WARNING: Increase organic mulch to protect soil microbial activity and monitor pH levels."
    else:
        return "OPTIMAL: Maintain current crop cycle. Consider nitrogen-fixing cover crops for the next season."

def run_agriaura_analysis():
    print("--- 🌾 AgriAura: AI-Driven AQI & Crop Analyzer 🌾 ---")
    
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="", 
            database="agriaura_db",
            port=3307
        )
        print("✅ Status: Connected to MariaDB (Port 3307)")

        # We use LEFT JOIN and TRIM to fix the "Empty DataFrame" issue
        query = """
        SELECT A.`Dist Name`, A.Year, A.Avg_O3, C.Yield_kg_per_ha 
        FROM clean_aqi_final A 
        LEFT JOIN clean_crops_final C ON TRIM(A.`Dist Name`) = TRIM(C.`Dist Name`) AND A.Year = C.Year
        LIMIT 20;
        """
        
        df = pd.read_sql(query, conn)
        
        # Match the column name in AI logic too
        # Fetch the data
        df = pd.read_sql(query, conn)
# --- ADD THE FILLNA LINE HERE ---
        df['Yield_kg_per_ha'] = df['Yield_kg_per_ha'].fillna(0)
        # --- THE FIX LINE ---
        # Convert Avg_O3 to numeric, turning any errors into 'NaN' (Not a Number)
        df['Avg_O3'] = pd.to_numeric(df['Avg_O3'], errors='coerce')
        # --------------------
        df['Soil_Condition'] = df['Avg_O3'].apply(
            lambda x: "Acidification Risk" if x > 42 else "Healthy/Balanced"
        )
        # Apply the AI Recommendation logic
        df['AI_Recommendation'] = df.apply(lambda x: generate_recommendation(x['Avg_O3'], x['Soil_Condition']), axis=1)

        # 1. Calculate Carbon Credits (Formula remains the same)
        df['Carbon_Credits'] = (df['Yield_kg_per_ha'] * 0.01) * (1 - (df['Avg_O3'] / 100))

        print("\n--- ANALYSIS COMPLETE: RELATIONAL DATA RETRIEVED ---")
        print("-" * 110)
    
       # 2. Updated Print Line including Carbon Credits AND Recommendations
    # We choose the most important columns for the final display
        cols_to_show = ['Dist Name', 'Year', 'Avg_O3', 'Soil_Condition', 'Carbon_Credits', 'AI_Recommendation']
        print(df[cols_to_show].head(20))
    
        print("-" * 110)
        print("\nINSIGHT: Carbon balancing and prescriptive solutions generated.")

        #print("\n--- ANALYSIS COMPLETE: RELATIONAL DATA RETRIEVED ---")
        #print("-" * 95)
        # Use backticks or the exact string for printing
        #print(df[['Dist Name', 'Year', 'Avg_O3', 'Soil_Condition', 'AI_Recommendation']])
        #print("-" * 95)
        #print("\nINSIGHT: Carbon balancing is required in high-ozone districts.")

    except mysql.connector.Error as err:
        print(f"❌ DBMS Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    run_agriaura_analysis()
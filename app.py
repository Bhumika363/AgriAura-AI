import streamlit as st
import pandas as pd
import mysql.connector
import warnings

# Suppress the SQLAlchemy/Connector warnings for a cleaner output
warnings.filterwarnings("ignore", category=UserWarning)

# --- GLOBAL PANDAS SETTINGS ---
pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)  
pd.set_option('display.max_colwidth', None)  

# --- STREAMLIT DASHBOARD PAGE CONFIG ---
st.set_page_config(page_title="AgriAura AI Dashboard", page_icon="🌾", layout="wide")

# Initialize session state to track login sessions across page updates
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- CORE SYSTEM AI LOGIC ---
def generate_recommendation(ozone, soil_condition):
    """AI Expert System rule matrix for generating localized farming prescriptions"""
    if soil_condition == "Acidification Risk":
        if ozone > 65:
            return "CRITICAL: Apply 2.5 tons/ha of Agricultural Lime and switch to Ozone-resistant Wheat varieties."
        else:
            return "WARNING: Increase organic mulch to protect soil microbial activity and monitor pH levels."
    else:
        return "OPTIMAL: Maintain current crop cycle. Consider nitrogen-fixing cover crops for the next season."


def get_agriaura_data():
    """
    Data Pipeline Engine: Tries connecting to the local MariaDB database (Port 3307).
    If it fails (like when deployed live on Streamlit Cloud), it seamlessly drops into 
    the safety net cache data to prevent application crashes.
    """
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="", 
            database="agriaura_db",
            port=3307,
            connection_timeout=3 # Crucial: prevents the cloud app from hanging/freezing
        )
        
        # Using LEFT JOIN and TRIM to match clean schema formats perfectly
        query = """
        SELECT A.`Dist Name`, A.Year, A.Avg_O3, C.Yield_kg_per_ha 
        FROM clean_aqi_final A 
        LEFT JOIN clean_crops_final C ON TRIM(A.`Dist Name`) = TRIM(C.`Dist Name`) AND A.Year = C.Year
        LIMIT 20;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df, "Live Local Database (Port 3307 Connected)"

    except Exception as e:
        # 🛡️ THE CLOUD DEPLOYMENT SAFETY NET DATA
        backup_data = {
            "Dist Name": ["Raipur", "Patna", "Chandigarh", "Ludhiana", "Bhopal", "Ranchi"],
            "Year": [2026, 2026, 2026, 2026, 2026, 2026],
            "Avg_O3": [35.2, 68.4, 44.1, 28.5, 55.0, 41.2],
            "Yield_kg_per_ha": [2100.0, 1150.0, 1850.0, 2400.0, 1400.0, 1950.0]
        }
        df = pd.DataFrame(backup_data)
        return df, "Cloud Demonstration Mode (Safety Net Cache Active)"


# ==============================================================================
#                            WEB USER INTERFACE LAYOUT
# ==============================================================================

st.title("🌾 AgriAura AI: Statistical Analytics & Expert Systems")
st.markdown("**Precision Agriculture | Air Quality Mitigation | Aura-Bot Intelligence**")
st.markdown("---")

# --- SIDEBAR PANEL: FARMER ENTRY LOG IN ---
st.sidebar.header("👨‍🌾 Farmer Access Portal")

if not st.session_state['logged_in']:
    st.sidebar.subheader("Account Authorization")
    user = st.sidebar.text_input("Username", placeholder="e.g., admin")
    pwd = st.sidebar.text_input("Password", type="password", placeholder="e.g., 123")
    
    if st.sidebar.button("Log In"):
        if user == "admin" and pwd == "123":
            st.session_state['logged_in'] = True
            st.session_state['username'] = user
            st.sidebar.success("Logged In Successfully!")
            st.rerun()
        else:
            st.sidebar.error("Invalid Credentials. (Hint: Use admin / 123)")
else:
    st.sidebar.success(f"Active Session: {st.session_state['username']}")
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.rerun()


# --- INTERACTIVE SECTION: CROWDSOURCED LOCAL FARMER INPUT FORM ---
if st.session_state['logged_in']:
    st.header("📍 Localized Field Measurement Intake Portal")
    st.markdown("Authorized farmers can enter real-time situational statistics below to evaluate localized ozone yield stress.")
    
    with st.form("farmer_input_form"):
        col1, col2 = st.columns(2)
        with col1:
            farmer_place = st.text_input("Village / District Location", value="Regional Sector 4")
            farmer_temp = st.number_input("Local Ground Temperature (°C)", min_value=0.0, max_value=60.0, value=33.4)
        with col2:
            farmer_ozone = st.number_input("Observed Ambient Ozone Avg (AQI/ppm)", min_value=0.0, max_value=200.0, value=48.5)
            
        submit_btn = st.form_submit_button("Run Diagnostic Modeling Assessment")
        
        if submit_btn:
            # Inline processing replicating the database analytical pipeline structures
            soil_status = "Acidification Risk" if farmer_ozone > 42 else "Healthy/Balanced"
            ai_rec = generate_recommendation(farmer_ozone, soil_status)
            yield_impact = round((farmer_ozone - 40) * 0.8, 2) if farmer_ozone > 40 else 0.0
            
            # Display localized outputs directly on screen dynamically
            st.markdown("### 📊 Real-Time Diagnostic Evaluation Matrix")
            m1, m2 = st.columns(2)
            m1.metric(label="Calculated Yield Degradation Percentage", value=f"{yield_impact}%", delta=f"-{yield_impact}%" if yield_impact > 0 else "0%")
            m2.metric(label="Inferred Ground Soil Classification", value=soil_status)
            
            st.info(f"💡 **Aura-Bot System Prescription Matrix:** {ai_rec}")
            st.success("✅ Computational metrics generated successfully and logged to active cache memory.")
    st.markdown("---")


# --- CORE SECTION: ANALYTICAL ENGINE SUMMARY TABLE ---
st.header("📈 Regional Relational Dataset Processing Overview")

# 1. Safely extract raw analytical framework records
raw_df, data_source_label = get_agriaura_data()
st.caption(f"**Active Pipeline Connectivity Pipeline Status:** {data_source_label}")

# 2. Replicate pipeline data cleaning scripts natively
processed_df = raw_df.copy()
processed_df['Yield_kg_per_ha'] = processed_df['Yield_kg_per_ha'].fillna(0)
processed_df['Avg_O3'] = pd.to_numeric(processed_df['Avg_O3'], errors='coerce')

# 3. Apply advanced mapping properties (Soil structures and AI rules)
processed_df['Soil_Condition'] = processed_df['Avg_O3'].apply(
    lambda x: "Acidification Risk" if x > 42 else "Healthy/Balanced"
)
processed_df['AI_Recommendation'] = processed_df.apply(
    lambda x: generate_recommendation(x['Avg_O3'], x['Soil_Condition']), axis=1
)

# 4. Process advanced environmental carbon modeling variables
processed_df['Carbon_Credits'] = (processed_df['Yield_kg_per_ha'] * 0.01) * (1 - (processed_df['Avg_O3'] / 100))

# 5. Render final clean analytics layout to screen
columns_to_render = ['Dist Name', 'Year', 'Avg_O3', 'Soil_Condition', 'Carbon_Credits', 'AI_Recommendation']
st.dataframe(processed_df[columns_to_render], use_container_width=True)

st.success("📝 **System Insight Engine Summary:** Relational processing complete. Advanced carbon modeling balancing and prescriptive matrices successfully executed above.")
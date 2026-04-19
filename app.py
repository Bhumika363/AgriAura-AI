import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import numpy as np

# 1. Page Configuration & UI Styling
st.set_page_config(page_title="AgriAura AI Pro", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-bottom: 3px solid #00d4ff; }
    .stChatFloatingInputContainer { background-color: #1e2130; }
    h1 { color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 AgriAura AI: Statistical Analytics & Expert Systems")
st.caption("Precision Agriculture | Air Quality Mitigation | Aura-Bot Intelligence")
st.write("---")

# 2. Database Connection (Using Port 3307 for MariaDB)
@st.cache_data
def load_agri_data():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1", user="root", password="", 
            database="agriaura_db", port=3307
        )
        query = """
        SELECT A.`Dist Name`, A.Year, A.Avg_O3, C.Yield_kg_per_ha 
        FROM clean_aqi_final A 
        LEFT JOIN clean_crops_final C ON TRIM(A.`Dist Name`) = TRIM(C.`Dist Name`) AND A.Year = C.Year
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Connection Failed: {e}")
        return None

# 3. Main Data Pipeline & Expert Logic
df_raw = load_agri_data()

if df_raw is not None and not df_raw.empty:
    df = df_raw.copy()
    
    # Safely convert to numeric to avoid Mean calculation errors
    df['Avg_O3'] = pd.to_numeric(df['Avg_O3'], errors='coerce')
    df['Yield_kg_per_ha'] = pd.to_numeric(df['Yield_kg_per_ha'], errors='coerce').fillna(0)
    
    # Fill missing Ozone with mean or standard default
    avg_val = df['Avg_O3'].mean()
    df['Avg_O3'] = df['Avg_O3'].fillna(avg_val if not pd.isna(avg_val) else 40.0)
    
    # SOLUTION FOR 0.00: Use 1500kg baseline if database yield is 0 or NaN
    calc_yield = df['Yield_kg_per_ha'].apply(lambda x: x if x > 0 else 1500)
    
    # CRITICAL FIX: Ensure credits are never negative using .clip(lower=0)
    # This prevents the Plotly 'ValueError' for bubble size
    df['Carbon_Credits'] = ((calc_yield * 0.01) * (1 - (df['Avg_O3'] / 100))).clip(lower=0)
    
    def get_advice(o3):
        if o3 > 65: return "🆘 CRITICAL: Acidification Risk High."
        if o3 > 42: return "⚠️ WARNING: Moderate Risk."
        return "✅ OPTIMAL: Healthy Environment."
    df['Advice'] = df['Avg_O3'].apply(get_advice)

    # 4. Sidebar: THE EXPERT AURA-BOT
    st.sidebar.title("🤖 Aura-Bot Expert")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "I am Aura-Bot. Ask me about AQI solutions, crops, weather, or soil!"}]

    for msg in st.session_state.messages:
        st.sidebar.chat_message(msg["role"]).write(msg["content"])

    if chat_input := st.sidebar.chat_input("Ask Aura-Bot..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        st.sidebar.chat_message("user").write(chat_input)
        
        q = chat_input.lower()
        if "aqi" in q or "ozone" in q:
            ans = "High O3 stresses plants. Apply antioxidant sprays (e.g., Vitamin C) or plant resistant Wheat varieties like PBW-343."
        elif "crop" in q or "grow" in q:
            ans = "In high-ozone regions, focus on leafy greens with organic mulch. Avoid sensitive varieties of Soy or Cotton during summer peaks."
        elif "weather" in q:
            ans = "Sunlight and stagnant air trap Ozone near the ground. Ensure extra irrigation during peak hours to protect plant stomata."
        elif "soil" in q or "acid" in q:
            ans = "Pollution correlates with soil acidification. Apply Agricultural Lime (CaCO3) to neutralize pH and restore phosphorus availability."
        elif "credit" in q:
            ans = f"Calculated as (Yield * 0.01) adjusted for Ozone. Total Portfolio: {df['Carbon_Credits'].sum():.2f} credits."
        else:
            ans = "I specialize in AQI, Soil, and Crops. Try asking: 'What should I grow if Ozone is high?'"
            
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.sidebar.chat_message("assistant").write(ans)

    # 5. Dashboard Filters
    st.sidebar.write("---")
    dist_list = sorted(df['Dist Name'].unique())
    selected_dist = st.sidebar.multiselect("Select Districts", dist_list, default=dist_list[:3] if len(dist_list) > 3 else dist_list)
    view_df = df[df['Dist Name'].isin(selected_dist)] if selected_dist else df

    # 6. Tabbed Analytics (Statistical Approach)
    tab1, tab2, tab3 = st.tabs(["📊 Statistical Insights", "📈 Trend Analysis", "🔍 Master Data Stream"])

    with tab1:
        # Row 1: KPI Statistics
        k1, k2, k3 = st.columns(3)
        k1.metric("Mean Ozone (μ)", f"{view_df['Avg_O3'].mean():.2f} ppb")
        k2.metric("Ozone Std Dev (σ)", f"{view_df['Avg_O3'].std():.2f}")
        k3.metric("Total Carbon Credits", f"{view_df['Carbon_Credits'].sum():.2f}")

        # Row 2: Statistical Charts
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Ozone Distribution (Histogram)")
            st.plotly_chart(px.histogram(view_df, x="Avg_O3", nbins=15, template="plotly_dark", color_discrete_sequence=['#00d4ff']), use_container_width=True)
        with c2:
            st.subheader("Ozone vs Credit Correlation (Scatter)")
            # Fix: .clip(lower=0) on line 59 ensures 'size' is always positive
            st.plotly_chart(px.scatter(view_df, x="Avg_O3", y="Carbon_Credits", color="Dist Name", size="Carbon_Credits", template="plotly_dark"), use_container_width=True)

    with tab2:
        st.subheader("Longitudinal Environmental Trends")
        st.plotly_chart(px.line(view_df.sort_values('Year'), x="Year", y="Avg_O3", color="Dist Name", markers=True, template="plotly_dark"), use_container_width=True)

    with tab3:
        st.subheader("Relational Database Output")
        st.dataframe(view_df[['Dist Name', 'Year', 'Avg_O3', 'Carbon_Credits', 'Advice']], use_container_width=True, hide_index=True)

elif df_raw is not None and df_raw.empty:
    st.warning("⚠️ Database is connected but returned no records. Please check your SQL tables.")
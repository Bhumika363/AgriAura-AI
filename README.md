# 🌿 AgriAura AI: Statistical Analytics & Expert System 📈

An automated precision agriculture dashboard designed to intelligently analyze the correlation between air quality and crop health. This project integrates a relational database with a specialized AI assistant, **Aura-Bot**, to provide real-time agricultural strategies and economic forecasting.

## 📘 Project Overview

Environmental stressors like ground-level Ozone often go unnoticed by farmers, leading to massive yield losses. **AgriAura AI** solves this by mapping AQI data against crop performance. It uses statistical imputation to handle missing data and calculates "Carbon Credits" to show the economic impact of clean air on farming.

## 🧩 Features

* **Aura-Bot Expert System:** A built-in intelligent assistant that provides prescriptive solutions for soil acidification and AQI mitigation.
* **Predictive Carbon Credit Engine:** Automatically calculates economic credits based on yield efficiency and pollution levels.
* **Statistical Imputation:** Uses regional baselines to ensure the dashboard remains functional even when specific datasets are incomplete.
* **Interactive Visualizations:** High-performance relational scatter plots and histograms to compare environmental trends across districts.
* **Automated Risk Assessment:** Dynamically tags districts with status alerts (Optimal, Warning, or Critical) based on current O3 levels.

## ⚙️ Components & Technologies

* **Python 3.x:** Core programming logic and data processing.
* **Streamlit:** Modern web framework for the interactive dashboard interface.
* **MariaDB / MySQL:** Relational database management for storing AQI and Crop records.
* **Pandas & NumPy:** Used for statistical calculations and data cleaning.
* **Plotly Express:** Advanced engine for rendering interactive, professional-grade charts.

## 🧠 Working Principle

1. **Data Ingestion:** The system pulls environmental and agricultural records from a local MariaDB instance via **Port 3307**.
2. **Processing Layer:** The backend converts raw data into numeric formats and applies a **1500kg baseline** for missing yield values.
3. **Algorithmic Calculation:** It applies the Carbon Credit formula: $$(Yield \times 0.01) \times (1 - \frac{Ozone}{100})$$ while ensuring no negative values are passed to the UI.
4. **Expert Logic:** **Aura-Bot** parses user queries related to "soil," "weather," or "crops" and matches them against a pre-defined agricultural knowledge base.
5. **Data Visualization:** The results are rendered into a tabbed interface, providing both high-level statistical KPIs and detailed relational data streams.

## 🚀 Future Enhancements

* **Live Sensor Integration:** Connecting IoT sensors to pull real-time AQI data directly into the dashboard.
* **Machine Learning Predictions:** Moving from statistical logic to predictive ML models for yield forecasting.
* **Multi-Crop Support:** Expanding the database to include diverse crop types beyond current wheat/grain cycles.
* **Deployment:** Hosting the application on Streamlit Cloud for public accessibility.

## 📄 License

© 2026 Bhumika. All Rights Reserved.

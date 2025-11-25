import streamlit as st
import pandas as pd
import re
import time
import requests

st.set_page_config(page_title="Global Threat Map", layout="wide")

st.title("🌍 Sentinel SIEM: Geo-Location Threat Map")

LOG_FILE = "server_logs.txt"

# Cache the IP location so we don't spam the API for the same IP
@st.cache_data
def get_location(ip):
    try:
        # Using ip-api.com (Free, no API key required for low volume)
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response['status'] == 'success':
            return response['lat'], response['lon'], response['country']
        else:
            return None, None, "Unknown"
    except:
        return None, None, "Error"

def parse_logs():
    data = []
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            
        for line in lines:
            # We are only looking for FAILED logins for the threat map
            match = re.search(r"Failed password for (\w+) from ([\d\.]+)", line)
            if match:
                user = match.group(1)
                ip = match.group(2)
                
                # Enrich with Geo-Data
                lat, lon, country = get_location(ip)
                
                if lat and lon:
                    data.append({
                        "User": user, 
                        "IP Address": ip, 
                        "lat": lat, 
                        "lon": lon,
                        "Country": country
                    })
    except FileNotFoundError:
        return []
        
    return data

# Placeholder for dynamic updates
placeholder = st.empty()

while True:
    data = parse_logs()
    
    # We need a DataFrame
    df = pd.DataFrame(data)

    with placeholder.container():
        if not df.empty:
            # MAP SECTION
            st.subheader("⚠️ Live Threat Map")
            # Streamlit looks for columns named 'lat' and 'lon' automatically
            st.map(df)

            # METRICS SECTION
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Attacks by Country")
                st.bar_chart(df['Country'].value_counts())
            
            with col2:
                st.subheader("Detailed Attack Feed")
                # Show the latest 5 attacks
                st.table(df[["Country", "IP Address", "User"]].tail(5))
        else:
            st.info("Waiting for attack data...")

    time.sleep(5) # Update every 5 seconds
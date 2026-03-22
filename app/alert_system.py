import streamlit as st
import pandas as pd

# ---------- UI STYLE ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #3cc5d7, #47d16c);
}

h1, h2, h3, p, label {
    color: #0a1f44 !important;
}

div.stButton > button {
    background-color: white;
    color: #0a1f44;
    border-radius: 10px;
    height: 40px;
    width: 120px;
    font-weight: bold;
    border: 2px solid #0a1f44;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: white !important;
}

div[data-baseweb="select"] *,
div[data-baseweb="input"] input {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)


def get_aqi_status(aqi):
    if aqi <= 50:
        return "Good ", "#00C853", "Air quality is excellent."
    elif aqi <= 100:
        return "Satisfactory ", "#64DD17", "Air quality is acceptable."
    elif aqi <= 200:
        return "Moderate ", "#FFD600", "Limit outdoor activity."
    elif aqi <= 300:
        return "Poor ", "#FF6D00", "Wear a mask outdoors."
    elif aqi <= 400:
        return "Very Poor ", "#D50000", "Stay indoors."
    else:
        return "Severe ", "#6A1B9A", "Health emergency!"


def extract_city(row):
    for col in row.index:
        if col.startswith("City_") and row[col] == 1:
            return col.replace("City_", "")
    return "Unknown"


pollution_sources = {
    "Ahmedabad": "Dust + Industrial Emissions",
    "Aizawl": "Biomass Burning + Vehicle Emissions",
    "Amaravati": "Construction Dust + Traffic",
    "Amritsar": "Crop Burning + Traffic + Dust",
    "Bengaluru": "Vehicle Emissions + Traffic",
    "Bhopal": "Industrial Pollution + Traffic",
    "Chandigarh": "Vehicle Emissions + Construction Dust",
    "Chennai": "Traffic + Industrial Emissions",
    "Delhi": "Vehicle Emissions + Industrial Pollution + Dust",
    "Gurugram": "Traffic + Construction",
    "Hyderabad": "Vehicle Emissions + Urban Growth",
    "Jaipur": "Dust + Traffic",
    "Kolkata": "Traffic + Coal Burning",
    "Lucknow": "Traffic + Dust",
    "Mumbai": "Traffic + Coastal Pollution",
    "Patna": "Dust + Construction"
}

def show_alerts():

    
    st.markdown(
        "<h2 style='text-align:center; color:#0a1f44;'> Smart Alert System</h2>",
        unsafe_allow_html=True
    )

    
    st.markdown(
        "<p style='text-align:center; color:#0a1f44;'>Check AQI, causes & health advice</p>",
        unsafe_allow_html=True
    )

    
    df = pd.read_csv("data/aqi_data.csv")
    df.columns = df.columns.str.strip()

    df["City"] = df.apply(extract_city, axis=1)
    df["Date"] = pd.to_datetime(df[["year", "month", "day"]]).dt.date

    
    col1, col2 = st.columns(2)

    with col1:
        selected_city = st.selectbox(" Select City", sorted(df["City"].unique()))

    city_df = df[df["City"] == selected_city]
    available_dates = sorted(city_df["Date"].unique())

    with col2:
        selected_date = st.date_input(
            " Select Date",
            value=available_dates[0],
            min_value=min(available_dates),
            max_value=max(available_dates),
            format="DD/MM/YYYY"
        )

    check = st.button("Check")

    st.markdown("---")

    
    if check:

        if selected_date not in available_dates:
            st.error(" No data available for selected date.")
            return

        filtered = city_df[city_df["Date"] == selected_date]

        if not filtered.empty:
            row = filtered.iloc[-1]
            aqi = float(row["AQI"])

            status, color, message = get_aqi_status(aqi)

            formatted_date = pd.to_datetime(selected_date).strftime("%d %B %Y")

            # AQI CARD
            st.markdown(f"""
            <div style="
                background-color:{color};
                padding:30px;
                border-radius:15px;
                text-align:center;
                color:white;
                font-size:22px;
                font-weight:600;
            ">
                AQI: {aqi:.0f} <br>
                {selected_city} <br>
                {formatted_date} <br><br>
                {status}
            </div>
            """, unsafe_allow_html=True)

            
            st.markdown("### Health Advice")

            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:10px;
                color:black;
                font-size:16px;
                font-weight:500;
                border:2px solid #0a1f44;
            ">
                {message}
            </div>
            """, unsafe_allow_html=True)

            
            st.markdown("###  Reason")

            reason = pollution_sources.get(selected_city, "General Urban Pollution")

            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:10px;
                color:black;
                font-size:16px;
                font-weight:500;
                border:2px solid #0a1f44;
            ">
                {reason}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.error("No data found.")
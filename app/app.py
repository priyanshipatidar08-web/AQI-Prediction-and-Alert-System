import streamlit as st
import pandas as pd
import alert_system
import aqi_guide
import aqi_predictor
import pydeck as pdk

st.set_page_config(page_title="Air Quality System", layout="wide")


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #52a4ff, #2bbcff, #00d4aa, #50ff7f);
    font-family: 'Poppins', sans-serif;
}

html, body, [class*="css"] {
    color: #0A1F44 !important;
}

div.stButton > button {
    background-color: white;
    color: #0A1F44;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 600;
    border: 2px solid #0A1F44;
    width: 100%;
    white-space: nowrap;
}

div[data-baseweb="select"] {
    background-color: white !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: #0A1F44 !important;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

df = pd.read_csv("data/aqi_data.csv")
df.columns = df.columns.str.strip()

def extract_city(row):
    for col in row.index:
        if col.startswith("City_") and row[col] == 1:
            return col.replace("City_", "")
    return "Unknown"

df["City"] = df.apply(extract_city, axis=1)
df["Date"] = pd.to_datetime(df[["year", "month", "day"]])

if st.session_state.page == "home":

    col_logo, col_title, col_btn = st.columns([1,7,1])

    with col_logo:
        st.markdown("<h1 style='font-size:110px; margin:0;'>🌍</h1>", unsafe_allow_html=True)

    with col_title:
        st.markdown(
            "<h1 style='color:#0A1F44; margin-bottom:0;'>Air Quality Prediction & Smart Alert System</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='color:#0A1F44; font-size:18px; margin-top:0;'>Predicting pollution. Protecting lives.</p>",
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns([3,2,3])

    with col2:
        if st.button(" Alerts", use_container_width=True):
            st.session_state.page = "alerts"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(" AQI Guide", use_container_width=True):
            st.session_state.page = "guide"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(" AQI Predictor", use_container_width=True):
            st.session_state.page = "predictor"
            st.rerun()

    st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] + div {
    margin-top: -60px;
}
</style>
""", unsafe_allow_html=True)

    st.subheader(" Air Quality Map")

    city_coords = {
        "Delhi": [28.61, 77.20],
        "Mumbai": [19.07, 72.87],
        "Bhopal": [23.25, 77.41],
        "Ahmedabad": [23.02, 72.57],
        "Jaipur": [26.91, 75.78],
        "Lucknow": [26.84, 80.94],
        "Chennai": [13.08, 80.27],
        "Kolkata": [22.57, 88.36],
        "Hyderabad": [17.38, 78.48],
        "Bangalore": [12.97, 77.59],
        "Aizawl": [23.73, 92.71],
        "Amaravati": [16.57, 80.36]
    }

    latest_data = df.sort_values("Date").groupby("City").tail(1)

    def get_color(aqi):
        if aqi <= 100:
            return [0, 200, 0]
        elif aqi <= 200:
            return [255, 200, 0]
        else:
            return [255, 80, 80]

    map_data = []

    for _, row in latest_data.iterrows():
        city = row["City"]
        if city in city_coords:
            lat, lon = city_coords[city]
            map_data.append({
                "City": city,
                "AQI": row["AQI"],
                "lat": lat,
                "lon": lon,
                "color": get_color(row["AQI"])
            })

    map_df = pd.DataFrame(map_data)

    if not map_df.empty:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position='[lon, lat]',
            get_color='color',
            get_radius=40000,
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=22.5,
            longitude=80,
            zoom=4,
        )

        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{City}\\nAQI: {AQI}"}
        ))

    st.markdown("---")


    st.subheader(" AQI Trend")

    selected_city = st.selectbox("Select City", df["City"].unique())

    trend_data = df[df["City"] == selected_city].sort_values("Date")

    st.line_chart(trend_data.set_index("Date")["AQI"])


elif st.session_state.page == "alerts":

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    alert_system.show_alerts()


elif st.session_state.page == "guide":

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    aqi_guide.show_guide()


elif st.session_state.page == "predictor":

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    aqi_predictor.show_predictor()
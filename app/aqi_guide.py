import streamlit as st

def show_guide():

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #3cc5d7, #47d18c);
    }

    h1, h2, h3, p, label {
        color: #0A1F44 !important;
    }

    input, input[type="number"] {
        color: black !important;
        -webkit-text-fill-color: black !important;
    }

    div[data-baseweb="select"] > div > div {
        color: black !important;
    }

    div[data-baseweb="select"] span {
        color: black !important;
    }

    ul[role="listbox"] li {
        background-color: white !important;
        color: black !important;
    }

    div[data-baseweb="select"] > div {
        background-color: white !important;
    }

    div[data-baseweb="input"] > div {
        background-color: white;
        border-radius: 8px;
    }

    div.stButton > button {
        background-color: white !important;
        color: #0A1F44 !important;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
        border: 2px solid #0A1F44;
    }

    div.stButton > button:hover {
        background-color: white !important;
        color: #0A1F44 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # TITLE
    st.markdown("<h1 style='text-align:center;'>📘 AQI Guide</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Know your air. Act smart.</h3>", unsafe_allow_html=True)

    st.markdown("---")

    # INPUTS
    aqi = st.number_input("Enter AQI Value", min_value=0, max_value=500, value=50)

    user_type = st.selectbox(
        "Select User Type",
        ["Normal Person", "Asthma Patient", "Child", "Old Age"]
    )

    st.markdown("---")

    if st.button("Check Advice"):

        # LOGIC (UNCHANGED)
        if aqi <= 50:
            message = "Air quality is Good 😊"
            color = "#00C853"

        elif 51 <= aqi <= 100:
            message = "Air quality is Moderate 🙂"
            color = "#FFD600"

        elif 101 <= aqi <= 200:
            message = "Limit outdoor activities 😷"
            color = "#FF8F00"

        else:
            message = "Avoid outdoor exposure 🚫"
            color = "#D50000"

        # 🔥 NEW PREMIUM CARD UI
        st.markdown(f"""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            border-left: 8px solid {color};
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-top: 20px;
        ">
            <h3 style="color:#0A1F44; margin-bottom:10px;">🌿 Air Quality Advice</h3>
            <p style="font-size:18px; color:#0A1F44; font-weight:500;">
                {message}
            </p>
        </div>
        """, unsafe_allow_html=True)
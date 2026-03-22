import streamlit as st
import pickle
import random
import matplotlib.pyplot as plt

def show_predictor():

    st.markdown("<h2 style='text-align:center;'> AQI Predictor</h2>", unsafe_allow_html=True)


    model = pickle.load(open("models/model.pkl", "rb"))

    
    PM2_5 = 120
    PM10 = 80
    NO = 30
    NO2 = 40
    CO = 1.2
    O3 = 50
    AQI = 110
    year = 2024
    month = 3
    day = 20

    City_Ahmedabad = 0
    City_Aizawl = 0
    City_Amaravati = 0
    City_Amritsar = 0
    City_Bengaluru = 0
    City_Bhopal = 0
    City_Brajrajnagar = 0
    City_Chandigarh = 0
    City_Chennai = 0
    City_Coimbatore = 0
    City_Delhi = 1
    City_Ernakulam = 0
    City_Gurugram = 0
    City_Guwahati = 0
    City_Hyderabad = 0
    City_Jaipur = 0
    City_Jorapokhar = 0
    City_Kochi = 0
    City_Kolkata = 0
    City_Lucknow = 0
    City_Mumbai = 0
    City_Patna = 0
    City_Shillong = 0
    City_Talcher = 0
    City_Thiruvananthapuram = 0
    City_Visakhapatnam = 0

    new_data = [[
        PM2_5, PM10, NO, NO2, CO, O3, AQI,
        year, month, day,
        City_Ahmedabad, City_Aizawl, City_Amaravati,
        City_Amritsar, City_Bengaluru, City_Bhopal, City_Brajrajnagar,
        City_Chandigarh, City_Chennai, City_Coimbatore, City_Delhi,
        City_Ernakulam, City_Gurugram, City_Guwahati, City_Hyderabad,
        City_Jaipur, City_Jorapokhar, City_Kochi, City_Kolkata,
        City_Lucknow, City_Mumbai, City_Patna, City_Shillong,
        City_Talcher, City_Thiruvananthapuram, City_Visakhapatnam
    ]]

    
    if st.button("Predict AQI"):

        prediction = model.predict(new_data)
        current_aqi = prediction[0]

    
        st.markdown(f"""
        <div style="
            border:2px solid white;
            padding:20px;
            border-radius:12px;
            text-align:center;
            margin-top:10px;
            color:black;
            background: rgba(255,255,255,0.3);
            font-size:20px;
            font-weight:600;
        ">
            Predicted AQI: {current_aqi:.0f}
        </div>
        """, unsafe_allow_html=True)

    
        st.markdown("<br>", unsafe_allow_html=True)

    
        future_aqi = []
        last_aqi = current_aqi

        for i in range(5):
            change = random.randint(-8, 10)
            next_day = max(0, last_aqi + change)
            future_aqi.append(next_day)
            last_aqi = next_day

        st.markdown("###  Next 5 Days AQI")

        st.markdown(f"""
        <div style="
            border:2px solid white;
            padding:15px;
            border-radius:12px;
            color:black;
            background: rgba(255,255,255,0.3);
            font-size:16px;
        ">
            Day 1: {future_aqi[0]:.0f} <br>
            Day 2: {future_aqi[1]:.0f} <br>
            Day 3: {future_aqi[2]:.0f} <br>
            Day 4: {future_aqi[3]:.0f} <br>
            Day 5: {future_aqi[4]:.0f}
        </div>
        """, unsafe_allow_html=True)

    
        st.markdown("<br><br>", unsafe_allow_html=True)

        
        st.markdown("###  Future AQI Trend")

        
        days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]

        fig, ax = plt.subplots(figsize=(5,2.5))

        ax.plot(days, future_aqi)
        ax.set_xlabel("Days")
        ax.set_ylabel("AQI")

        
        col1, col2 = st.columns([2,1])
        with col1:
            st.pyplot(fig, use_container_width=False)
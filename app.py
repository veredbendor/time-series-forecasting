import streamlit as st
import pandas as pd

st.title("Weather Data Anomaly Detection")

# Example dataframe to test the app
data = {
    "Date": ["2024-12-18", "2024-12-19", "2024-12-20"],
    "Temperature": [22, 21, 25],
    "Humidity": [65, 60, 70],
    "Pressure": [1012, 1013, 1011],
}
df = pd.DataFrame(data)

st.write("Sample Weather Data")
st.dataframe(df)

st.line_chart(df.set_index("Date"))

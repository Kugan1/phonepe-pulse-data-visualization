import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px
import json
 
connect = sqlite3.connect('pulse.db')
df = pd.read_sql_query("SELECT * from aggregated_transaction", connect)

 
 # Define a function to create the dashboard

st.title("PhonePe Pulse Data visualization")
     
     # Filter data based on user input
state = st.selectbox("Select a State", df['aggregate_name'].unique())
year = st.selectbox("Select a Year", df['year'].unique())
payment = st.selectbox("Select a payment type", df['name'].unique())
     
     # Filter the data based on user input
filtered_df = df[(df['aggregate_name'] == state) & (df['year'] == year) & (df['name'] == payment)]
     
     # Create a bar chart to show transaction type distribution
fig = px.bar(filtered_df, x="name", y="amount", color="count",
            height=500, title="Transaction Type Distribution")
st.plotly_chart(fig)

india_states = json.load(open("states_india.geojson", "r"))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]



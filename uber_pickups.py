import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
 
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
 
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(30000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')
 
#data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
 
st.subheader('Raw data')
st.write(data)
 
#Figure 1: Table of Number of Uber pickups in NYC by hour
st.subheader('Number of Uber pickups in NYC by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
 
#hist_values
st.bar_chart(hist_values)

#Figure 2: 2D Map
st.subheader('2D Map of all Uber pickups in NYC')
st.map(data)

#Date Handling
import datetime  

#Exercise 2 - Date Input
st.subheader('Date Input')
d = st.date_input("Please input required date", value=None)
st.write("Date input is:", d)

df = data 

#Hour Filter
st.subheader('Hour Filter')
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_by_hour = df[df['date/time'].dt.hour == hour_to_filter]
st.metric("Uber Pickups this Hour", len(filtered_by_hour))

#Filter Date & hour
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter] #and [data[DATE_COLUMN].date == d.date()]]

if d:
    filtered_data = data[
        (data[DATE_COLUMN].dt.date == d) &
        (data[DATE_COLUMN].dt.hour == hour_to_filter)
    ]
else:
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    

#Figure 3: Convert 2D map to 3D map using PyDeck (Exercise 1)
st.subheader(f'3D Map by PyDeck of all pickups at {hour_to_filter}:00 on {d}')
st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=40.730610,
            longitude=-73.935242,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=filtered_data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=filtered_data,  #chart_data
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)

# Exercise 3 - Selectbox
st.subheader('Select Data Column')

# Dynamically get column names from the dataframe
column_options = list(data.columns)

option = st.selectbox(
    "Which column would you like to display?",
    column_options,
    index=None,
    placeholder="Select a column...",
)

# Display selected column values
if option:
    st.write(f"You selected: `{option}`")
    st.write(data[[option]])

if option and pd.api.types.is_numeric_dtype(data[option]):
    st.bar_chart(data[option].value_counts().sort_index())

#Figure 4: Plotly
st.subheader('Uber Pickup Locations with Clustering in NYC by Plotly')

df = data

df.columns = df.columns.str.lower().str.strip()
df['date/time'] = pd.to_datetime(df['date/time'])
df['hour'] = df['date/time'].dt.hour

# Create scatter_mapbox with clustering and black color
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="base",
    hover_data={"date/time": True, "hour": True},
    zoom=10,
    height=600,
    #title="Uber Pickup Locations in NYC"
)

# Use open-source map style
fig.update_layout(mapbox_style="open-street-map")

fig.update_traces(
    cluster=dict(enabled=True),
    marker=dict(color="yellow")
)

st.plotly_chart(fig)

#Exercise 5: Counter

#st.subheader('Exercise 5 - Counter')
if "counter" not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1
st.header(f"This page has run {st.session_state.counter} times.")
# st.button("Run it again")
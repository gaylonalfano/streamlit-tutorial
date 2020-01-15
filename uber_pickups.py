import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC")

# Let's add some data
DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


# Let's cache the data loading using @st.cache
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Test the function and review output
# Create a text element and let the reader know the data is loading.
data_load_state = st.text("Loading data...")
# Load 10,000 rows of data into the dataframe
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Loading data... done!")
# st.write("Done! (using st.cache)")

# Let's inspect the raw data if toggle button checked
if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

# Let's add a histogram to see busiest hours
st.subheader("Number of pickups by hour")

# Use numpy to generate a histogram
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]

# Draw the histogram using Streamlit's st.bar_chart() method
st.bar_chart(hist_values)

# Let's now map out the pickup locations
# st.subheader("Map of all pickups")
# st.map(data)

hour_to_filter = st.slider("hour", 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)

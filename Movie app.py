import streamlit as st
import pandas as pd

st.title("My Movie Database 🎬")
st.write("Welcome to my interactive dashboard!")

# 1. Create the Sidebar and Slider
st.sidebar.header("Filter Options")
min_rating = st.sidebar.slider("Minimum IMDB Rating:", 0.0, 10.0, 8.0)

# 2. Load the real data from your CSV file
data = pd.read_csv("movies.csv")

# 3. Filter the data using the slider's current number
filtered_data = data[data['IMDB Rating'] >= min_rating]

# 4. Display the filtered table
st.write(f"Showing movies with a rating of {min_rating} or higher:")
st.dataframe(filtered_data)

# 5. Display the chart
st.subheader("Movie Ratings Chart")
st.bar_chart(filtered_data, x="Movie Title", y="IMDB Rating")

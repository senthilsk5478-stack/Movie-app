import streamlit as st
import pandas as pd

st.title("Senthil's Movie Database 🎬")
st.write("Welcome to my interactive dashboard!")

# 1. Create the Sidebar and Slider
st.sidebar.header("Filter Options")
min_rating = st.sidebar.slider("Minimum IMDB Rating:", 0.0, 10.0, 8.0)

# 2. Create the Data (I added a few more movies!)
data = pd.DataFrame({
    'Movie Title': ['The Dark Knight', 'Inception', 'Dune', 'Avatar', 'Iron Man'],
    'Director': ['Christopher Nolan', 'Christopher Nolan', 'Denis Villeneuve', 'James Cameron', 'Jon Favreau'],
    'IMDB Rating': [9.0, 8.8, 8.0, 7.8, 7.9]
})

# 3. Filter the data using the slider's current number
filtered_data = data[data['IMDB Rating'] >= min_rating]

# 4. Display the filtered table
st.write(f"Showing movies with a rating of {min_rating} or higher:")
st.dataframe(filtered_data)

# 5. Display the chart (which will also update!)
st.subheader("Movie Ratings Chart")
st.bar_chart(filtered_data, x="Movie Title", y="IMDB Rating")

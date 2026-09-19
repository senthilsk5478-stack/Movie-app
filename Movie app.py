import streamlit as st
import pandas as pd

# Make the app take up the full screen width
st.set_page_config(layout="wide") 

st.title("My Movie Database 🎬")
st.write("Welcome to my interactive dashboard!")

# 1. Load the real data
data = pd.read_csv("movies.csv")

# 2. Sidebar Controls
st.sidebar.header("Filter Options")
search_term = st.sidebar.text_input("Search for a Movie or Director:")
min_rating = st.sidebar.slider("Minimum IMDB Rating:", 0.0, 10.0, 7.0)

# 3. Filter the data based on the slider
filtered_data = data[data['IMDB Rating'] >= min_rating]

# 4. Filter the data based on the search box (if the user typed something)
if search_term:
    filtered_data = filtered_data[
        filtered_data['Movie Title'].str.contains(search_term, case=False) |
        filtered_data['Director'].str.contains(search_term, case=False)
    ]

# 5. Sort the movies from highest rating to lowest
filtered_data = filtered_data.sort_values(by="IMDB Rating", ascending=False)

# 6. Display the table and chart
st.write(f"Found {len(filtered_data)} movies:")
st.dataframe(filtered_data, use_container_width=True)

st.subheader("Movie Ratings Chart")
st.bar_chart(filtered_data, x="Movie Title", y="IMDB Rating")

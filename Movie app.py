import streamlit as st
import pandas as pd

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

# 4. Filter the data based on the search box
if search_term:
    filtered_data = filtered_data[
        filtered_data['Movie Title'].str.contains(search_term, case=False) |
        filtered_data['Director'].str.contains(search_term, case=False)
    ]

# 5. Sort the movies from highest rating to lowest
filtered_data = filtered_data.sort_values(by="IMDB Rating", ascending=False)

# --- NEW FEATURE: DASHBOARD METRICS ---
st.subheader("Dashboard Summary")

# Create 3 columns for our metric widgets
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Movies Found", len(filtered_data))
with col2:
    # Calculate the average rating of the filtered movies
    avg_rating = round(filtered_data['IMDB Rating'].mean(), 1)
    st.metric("Average Rating", avg_rating)
with col3:
    # Find the highest rating in the filtered list
    highest_rating = filtered_data['IMDB Rating'].max()
    st.metric("Highest Rating", highest_rating)
    
st.divider() # Adds a clean visual separator line
# --------------------------------------

# 6. Display the table and chart
st.dataframe(filtered_data, use_container_width=True)

st.subheader("Movie Ratings Chart")
st.bar_chart(filtered_data, x="Movie Title", y="IMDB Rating")

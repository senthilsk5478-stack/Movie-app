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

# 3. Filter the data
filtered_data = data[data['IMDB Rating'] >= min_rating]

if search_term:
    filtered_data = filtered_data[
        filtered_data['Movie Title'].str.contains(search_term, case=False) |
        filtered_data['Director'].str.contains(search_term, case=False)
    ]

# 4. Sort the movies
filtered_data = filtered_data.sort_values(by="IMDB Rating", ascending=False)

# 5. Display the table with images!
st.write(f"Found {len(filtered_data)} movies:")

st.dataframe(
    filtered_data, 
    use_container_width=True,
    column_config={
        "Poster": st.column_config.ImageColumn("Movie Poster")
    }
)

st.subheader("Movie Ratings Chart")
st.bar_chart(filtered_data, x="Movie Title", y="IMDB Rating")

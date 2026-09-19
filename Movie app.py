import streamlit as st
import pandas as pd

st.set_page_config(layout="wide") 

st.title("My Movie Database 🎬")

# 1. Load data and clean any hidden spaces
data = pd.read_csv("movies.csv")
data.columns = data.columns.str.strip()
data['Poster'] = data['Poster'].str.strip()

# 2. Sidebar Controls
st.sidebar.header("Filter Options")
search_term = st.sidebar.text_input("Search for a Movie or Director:")
min_rating = st.sidebar.slider("Minimum IMDB Rating:", 0.0, 10.0, 7.0)

# 3. Filter the data based on slider
filtered_data = data[data['IMDB Rating'] >= min_rating]

# 4. Filter based on the search box
if search_term:
    filtered_data = filtered_data[
        filtered_data['Movie Title'].str.contains(search_term, case=False) |
        filtered_data['Director'].str.contains(search_term, case=False)
    ]

# Sort the movies highest to lowest
filtered_data = filtered_data.sort_values(by="IMDB Rating", ascending=False)

# 5. Display the Poster Gallery
st.subheader(f"Movie Gallery ({len(filtered_data)} found)")
cols = st.columns(3) 

for index, row in enumerate(filtered_data.iterrows()):
    movie_data = row[1]
    col_to_use = cols[index % 3] 
    with col_to_use:
        # use_container_width forces the browser to load the image smoothly
        st.image(movie_data["Poster"], use_container_width=True, caption=movie_data["Movie Title"])

st.divider()

# 6. Display the Bar Chart
st.subheader("Movie Ratings Chart")
st.bar_chart(filtered_data, x="Movie Title", y="IMDB Rating")

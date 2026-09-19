import streamlit as st
import pandas as pd

st.set_page_config(layout="wide") 

st.title("My Movie Database 🎬")

# 1. Load data and clean any hidden spaces in the CSV
data = pd.read_csv("movies.csv")
data.columns = data.columns.str.strip()
data['Poster'] = data['Poster'].str.strip()

# 2. Sidebar Controls
st.sidebar.header("Filter Options")
min_rating = st.sidebar.slider("Minimum IMDB Rating:", 0.0, 10.0, 7.0)

# 3. Filter the data based on the slider
filtered_data = data[data['IMDB Rating'] >= min_rating]

# 4. Display a Netflix-style Poster Gallery!
st.subheader("Movie Gallery")

# Create 3 columns across the screen
cols = st.columns(3) 

# Loop through the movies and place them in the columns
for index, row in enumerate(filtered_data.iterrows()):
    movie_data = row[1]
    col_to_use = cols[index % 3] # Cycles through column 1, 2, 3
    
    with col_to_use:
        # Display the image and the title
        st.image(movie_data["Poster"], width=200, caption=movie_data["Movie Title"])

# 5. Display the raw data table below it
st.divider() # Adds a nice visual line
st.subheader("Raw Data Table")
st.dataframe(filtered_data, use_container_width=True)

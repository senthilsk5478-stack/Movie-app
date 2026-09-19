import streamlit as st
import pandas as pd

st.title("My First Movie App 🍿")
st.write("Welcome to my own IMDB-style dashboard!")

data = pd.DataFrame({
    'Movie Title': ['The Dark Knight', 'Inception', 'Dune'],
    'Director': ['Christopher Nolan', 'Christopher Nolan', 'Denis Villeneuve'],
    'IMDB Rating': [9.0, 8.8, 8.0]
})

st.dataframe(data)
st.subheader("Movie Ratings Chart")
st.bar_chart(data, x="Movie Title", y="IMDB Rating")

# Create a sidebar
st.sidebar.header("User Controls")

# Add a slider widget to the sidebar
user_rating = st.sidebar.slider("Rate your favorite movie out of 10:", 0.0, 10.0, 5.0)

# Display the result in the main app
st.write(f"**You selected a rating of:** {user_rating}")

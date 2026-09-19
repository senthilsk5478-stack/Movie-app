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

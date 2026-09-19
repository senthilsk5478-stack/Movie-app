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

filtered_data = filtered_data.sort_values(by="IMDB Rating", ascending=False)

# 4. Dashboard Metrics
st.subheader("Dashboard Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Movies Found", len(filtered_data))
with col2:
    avg_rating = round(filtered_data['IMDB Rating'].mean(), 1)
    st.metric("Average Rating", avg_rating)
with col3:
    highest_rating = filtered_data['IMDB Rating'].max()
    st.metric("Highest Rating", highest_rating)
    
st.divider()

# --- NEW FEATURE: INTERACTIVE TABS ---
# 5. Create the tabs
tab1, tab2 = st.tabs(["📊 Data Table", "📈 Visual Chart"])

# Put the table in the first tab
with tab1:
    st.dataframe(filtered_data, use_container_width=True)

# Put the chart in the second tab
with tab2:
    st.bar_chart(filtered_data, x="Movie Title", y="IMDB Rating")

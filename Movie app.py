import streamlit as st
import pandas as pd

st.set_page_config(layout="wide") 

st.title("My Advanced Movie Dashboard 🎬")

# 1. Load data
data = pd.read_csv("movies.csv")

# 2. Sidebar Filters
st.sidebar.header("Filter Options")
min_rating = st.sidebar.slider("Minimum IMDB Rating:", 0.0, 10.0, 7.0)
filtered_data = data[data['IMDB Rating'] >= min_rating]

# 3. Top Summary Text
st.write(f"**Displaying {len(filtered_data)} movies matching your criteria (out of {len(data)} total movies).**")

# 4. Visualizations Header
st.header("Interactive Visualizations 📈")

# 5. Top 10 Charts (Side by Side)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top Movies by Rating")
    top_rating = filtered_data.nlargest(10, 'IMDB Rating')
    st.bar_chart(top_rating, x="Movie Title", y="IMDB Rating")

with col2:
    st.subheader("Top Movies by Voting Counts")
    top_votes = filtered_data.nlargest(10, 'Votes')
    st.bar_chart(top_votes, x="Movie Title", y="Votes")

# 6. Genre Distributions (Side by Side)
col3, col4 = st.columns(2)
with col3:
    st.subheader("Genre Distribution")
    genre_counts = filtered_data['Genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']
    st.bar_chart(genre_counts, x="Genre", y="Count")

with col4:
    st.subheader("Average Duration by Genre")
    avg_duration = filtered_data.groupby('Genre')['Duration'].mean().reset_index()
    st.bar_chart(avg_duration, x="Genre", y="Duration")

st.divider()

# 7. Duration Extremes
st.header("Duration Extremes: Shortest and Longest Movies")

if not filtered_data.empty:
    # Find the rows with the minimum and maximum duration
    shortest = filtered_data.loc[filtered_data['Duration'].idxmin()]
    longest = filtered_data.loc[filtered_data['Duration'].idxmax()]

    ext1, ext2 = st.columns(2)
    with ext1:
        st.subheader("Shortest Movie 📉")
        st.write(f"**Movie:** {shortest['Movie Title']}")
        st.write(f"**Genre:** {shortest['Genre']}")
        st.write(f"**Duration:** {shortest['Duration']} minutes")
        st.write(f"**Rating:** {shortest['IMDB Rating']}")

    with ext2:
        st.subheader("Longest Movie 📈")
        st.write(f"**Movie:** {longest['Movie Title']}")
        st.write(f"**Genre:** {longest['Genre']}")
        st.write(f"**Duration:** {longest['Duration']} minutes")
        st.write(f"**Rating:** {longest['IMDB Rating']}")

st.divider()

# 8. Correlation Scatter Plot
st.subheader("Rating vs. Voting Counts (Correlation)")
st.scatter_chart(filtered_data, x="IMDB Rating", y="Votes")

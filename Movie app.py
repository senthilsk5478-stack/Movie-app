import streamlit as st
import pandas as pd

st.set_page_config(layout="wide") 

# --- TITLE ---
st.title("Multi-Region Cinema Analytics Portal 🌍")

# 1. Load data
data = pd.read_csv("movies.csv")

# --- ADVANCED SIDEBAR FILTERS ---
st.sidebar.header("Filter Movies 📊")
st.sidebar.write("Use the controls below to refine the dataset.")

search_term = st.sidebar.text_input("🔍 Search Title or Director:")

all_genres = sorted(data['Genre'].dropna().unique().tolist())
selected_genres = st.sidebar.multiselect("🎭 Select Genre(s):", all_genres, placeholder="Choose genres...")

min_rating, max_rating = float(data['IMDB Rating'].min()), float(data['IMDB Rating'].max())
rating_range = st.sidebar.slider("⭐ Rating Range:", min_value=0.0, max_value=10.0, value=(min_rating, max_rating), step=0.1)

min_dur, max_dur = int(data['Duration'].min()), int(data['Duration'].max())
duration_range = st.sidebar.slider("⏱️ Duration (minutes):", min_value=min_dur, max_value=max_dur, value=(min_dur, max_dur))

min_votes, max_votes = int(data['Votes'].min()), int(data['Votes'].max())
votes_range = st.sidebar.slider("🗳️ Voting Counts:", min_value=min_votes, max_value=max_votes, value=(min_votes, max_votes), step=1000)

min_bo, max_bo = int(data['Box Office'].min()), int(data['Box Office'].max())
bo_range = st.sidebar.slider("💰 Box Office ($ Millions):", min_value=min_bo, max_value=max_bo, value=(min_bo, max_bo))

# 3. Apply the filters
filtered_data = data.copy()

if search_term:
    filtered_data = filtered_data[
        filtered_data['Movie Title'].str.contains(search_term, case=False) |
        filtered_data['Director'].str.contains(search_term, case=False)
    ]

if selected_genres:
    filtered_data = filtered_data[filtered_data['Genre'].isin(selected_genres)]

filtered_data = filtered_data[
    (filtered_data['IMDB Rating'] >= rating_range[0]) & (filtered_data['IMDB Rating'] <= rating_range[1]) &
    (filtered_data['Duration'] >= duration_range[0]) & (filtered_data['Duration'] <= duration_range[1]) &
    (filtered_data['Votes'] >= votes_range[0]) & (filtered_data['Votes'] <= votes_range[1]) &
    (filtered_data['Box Office'] >= bo_range[0]) & (filtered_data['Box Office'] <= bo_range[1])
]

filtered_data = filtered_data.sort_values(by="IMDB Rating", ascending=False)

# --- SUMMARY TEXT & KPI DELTAS ---
st.write(f"**Filtered View: Showing {len(filtered_data)} cinematic records matching your parameters (out of {len(data)} total records).**")

global_avg_rating = data['IMDB Rating'].mean()
global_avg_votes = data['Votes'].mean()
global_avg_bo = data['Box Office'].mean()

col1, col2, col3, col4 = st.columns(4)
with col1:
    movies_diff = len(filtered_data) - len(data)
    st.metric("Total Records Found", len(filtered_data), delta=f"{movies_diff} from total", delta_color="off")
    
with col2:
    filtered_avg_rating = filtered_data['IMDB Rating'].mean() if not filtered_data.empty else 0
    rating_delta = filtered_avg_rating - global_avg_rating
    st.metric("Average Rating", f"{filtered_avg_rating:.1f} ⭐", delta=f"{rating_delta:.1f}")
    
with col3:
    filtered_avg_votes = filtered_data['Votes'].mean() if not filtered_data.empty else 0
    votes_delta = filtered_avg_votes - global_avg_votes
    st.metric("Average Votes", f"{filtered_avg_votes:,.0f}", delta=f"{votes_delta:,.0f}")
    
with col4:
    filtered_avg_bo = filtered_data['Box Office'].mean() if not filtered_data.empty else 0
    bo_delta = filtered_avg_bo - global_avg_bo
    st.metric("Avg Revenue", f"${filtered_avg_bo:,.0f}M", delta=f"{bo_delta:,.0f}M")
    
st.divider()

# --- THE MASTER TABS ---
tab1, tab2 = st.tabs(["Data & Extremes 📁", "Charts & Visualizations 📈"])

# ---------------------------------------------------------
# TAB 1: THE RAW DATA AND THE EXTREMES
# ---------------------------------------------------------
with tab1:
    st.subheader("Raw Data Table")
    
    display_data = filtered_data.copy()
    display_data.insert(0, 'S.No', range(1, len(display_data) + 1))
    
    st.dataframe(
        display_data, 
        hide_index=True, 
        use_container_width=True,
        column_config={
            "IMDB Rating": st.column_config.ProgressColumn(
                "IMDB Rating",
                format="%f",
                min_value=0,
                max_value=10,
            ),
            "Votes": st.column_config.NumberColumn(
                "Total Votes",
                format="%d 🗳️",
            ),
            "Duration": st.column_config.NumberColumn(
                "Duration (mins)",
                format="%d ⏱️"
            ),
            "Year": st.column_config.NumberColumn(
                "Year",
                format="%d"
            ),
            "Box Office": st.column_config.NumberColumn(
                "Box Office",
                format="$%d M 💰"
            )
        }
    )
    
    if not filtered_data.empty:
        csv = display_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Dataset as CSV",
            data=csv,
            file_name="filtered_movies.csv",
            mime="text/csv",
        )
    
    st.divider()
    
    st.header("Dataset Extremes")
    if not filtered_data.empty:
        highest_grossing = filtered_data.loc[filtered_data['Box Office'].idxmax()]
        
        st.subheader("💰 Revenue Extremes")
        st.success(f"**Highest Grossing Film:** {highest_grossing['Movie Title']} (${highest_grossing['Box Office']} Million)")
        st.write("")

        shortest = filtered_data.loc[filtered_data['Duration'].idxmin()]
        longest = filtered_data.loc[filtered_data['Duration'].idxmax()]

        st.subheader("⏱️ Duration Extremes")
        ext1, ext2 = st.columns(2)
        with ext1:
            st.info(f"**Shortest Film:** {shortest['Movie Title']} ({shortest['Duration']} mins)")
        with ext2:
            st.info(f"**Longest Film:** {longest['Movie Title']} ({longest['Duration']} mins)")
            
        st.write("")

        oldest = filtered_data.loc[filtered_data['Year'].idxmin()]
        newest = filtered_data.loc[filtered_data['Year'].idxmax()]
        
        st.subheader("📅 Age Extremes")
        ext3, ext4 = st.columns(2)
        with ext3:
            st.info(f"**Oldest Film:** {oldest['Movie Title']} ({oldest['Year']})")
        with ext4:
            st.info(f"**Newest Film:** {newest['Movie Title']} ({newest['Year']})")

# ---------------------------------------------------------
# TAB 2: UNIQUE REDESIGNED ANALYTICS CHARTS
# ---------------------------------------------------------
with tab2:
    if not filtered_data.empty:
        
        # Chart 1: Temporal Trend Line
        st.subheader("📈 Temporal Trend: Cinematic Output Volume Over Time")
        yearly_counts = filtered_data.groupby('Year').size().reset_index(name='Movie Count')
        st.line_chart(yearly_counts, x="Year", y="Movie Count", color="#1f77b4")
        
        st.divider()

        # Charts 2 & 3: Genre Performance Split (Rating vs Revenue)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("⭐ Average IMDB Rating by Genre")
            genre_rating = filtered_data.groupby('Genre')['IMDB Rating'].mean().reset_index()
            st.bar_chart(genre_rating, x="Genre", y="IMDB Rating", color="#ff7f0e")

        with col2:
            st.subheader("💰 Cumulative Revenue by Genre ($M)")
            genre_bo = filtered_data.groupby('Genre')['Box Office'].sum().reset_index()
            st.bar_chart(genre_bo, x="Genre", y="Box Office", color="#2ca02c")

        st.divider()

        # Charts 4 & 5: Director Productivity & Runtime vs Rating Scatter
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("🎬 Most Featured Directors in View")
            director_counts = filtered_data['Director'].value_counts().head(10).reset_index()
            director_counts.columns = ['Director', 'Movie Count']
            st.bar_chart(director_counts, x="Director", y="Movie Count", color="#9467bd")

        with col4:
            st.subheader("⏱️ Runtime vs. Critical Reception")
            st.scatter_chart(filtered_data, x="Duration", y="IMDB Rating", color="#d62728")
    else:
        st.warning("No records match your active parameters. Please broaden your filter criteria.")

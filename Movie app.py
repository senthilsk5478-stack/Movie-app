import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide") 

# --- TITLE ---
st.title("Multi-Region Cinema Analytics Portal 🌍")

# 1. Load data
@st.cache_data
def load_data():
    return pd.read_csv("movies.csv")

data = load_data()

# --- ADVANCED SIDEBAR FILTERS ---
st.sidebar.header("Filter Movies 📊")
st.sidebar.write("Use the controls below to refine the dataset.")

search_term = st.sidebar.text_input("🔍 Search Title, Director, or Cast:")

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

# --- ACTOR & ACTRESS MAPPING DICTIONARY ---
actor_mapping = {
    "The Dark Knight": "Christian Bale & Maggie Gyllenhaal",
    "Inception": "Leonardo DiCaprio & Marion Cotillard",
    "The Matrix": "Keanu Reeves & Carrie-Anne Moss",
    "Interstellar": "Matthew McConaughey & Anne Hathaway",
    "Avatar": "Sam Worthington & Zoe Saldana",
    "Dune": "Timothée Chalamet & Zendaya",
    "Gladiator": "Russell Crowe & Connie Nielsen",
    "The Godfather": "Marlon Brando & Diane Keaton",
    "The Shawshank Redemption": "Tim Robbins & Morgan Freeman",
    "Pulp Fiction": "John Travolta & Uma Thurman",
    "Forrest Gump": "Tom Hanks & Robin Wright",
    "Fight Club": "Brad Pitt & Helena Bonham Carter",
    "The Empire Strikes Back": "Mark Hamill & Carrie Fisher",
    "The Lord of the Rings: The Return of the King": "Elijah Wood & Liv Tyler",
    "Star Wars": "Mark Hamill & Carrie Fisher",
    "The Silence of the Lambs": "Jodie Foster & Anthony Hopkins",
    "Se7en": "Brad Pitt & Gwyneth Paltrow",
    "Saving Private Ryan": "Tom Hanks & Matt Damon",
    "The Green Mile": "Tom Hanks & Bonnie Hunt",
    "Terminator 2: Judgment Day": "Arnold Schwarzenegger & Linda Hamilton",
    "Back to the Future": "Michael J. Fox & Lea Thompson",
    "Psycho": "Anthony Perkins & Janet Leigh",
    "The Departed": "Leonardo DiCaprio & Vera Farmiga",
    "Whiplash": "Miles Teller & Melissa Benoist",
    "The Lion King": "Matthew Broderick & Moira Kelly",
    "Alien": "Sigourney Weaver & Veronica Cartwright",
    "Memento": "Guy Pearce & Carrie-Anne Moss",
    "Apocalypse Now": "Martin Sheen & Marlon Brando",
    "Raiders of the Lost Ark": "Harrison Ford & Karen Allen",
    "Joker": "Joaquin Phoenix & Zazie Beetz",
    "Vikram": "Kamal Haasan & Vasanthi",
    "Nayakan": "Kamal Haasan & Saranya",
    "Pariyerum Perumal": "Kathir & Anandhi",
    "Kaithi": "Karthi & Narain",
    "Asuran": "Dhanush & Manju Warrier",
    "96": "Vijay Sethupathi & Trisha",
    "Thani Oruvan": "Jayam Ravi & Nayanthara",
    "Vada Chennai": "Dhanush & Aishwarya Rajesh",
    "Super Deluxe": "Vijay Sethupathi & Samantha",
    "Ratsasan": "Vishnu Vishal & Amala Paul",
    "Jai Bhim": "Suriya & Lijo Mol Jose",
    "Karnan": "Dhanush & Rajisha Vijayan",
    "Anbe Sivam": "Kamal Haasan & Kiran Rathod",
    "Thevar Magan": "Kamal Haasan & Revathi",
    "Roja": "Arvind Swami & Madhoo",
    "Bombay": "Arvind Swami & Manisha Koirala",
    "Baasha": "Rajinikanth & Nagma",
    "Mankatha": "Ajith Kumar & Trisha",
    "Vinnaithaandi Varuvaayaa": "Silambarasan & Trisha",
    "Sarpatta Parambarai": "Arya & Dushara Vijayan",
    "Kumbalangi Nights": "Shane Nigam & Anna Ben",
    "Drishyam": "Mohanlal & Meena",
    "Premam": "Nivin Pauly & Sai Pallavi",
    "Manjummel Boys": "Soubin Shahir & Ganapathi",
    "Aavesham": "Fahadh Faasil & Mithun Jai Shankar",
    "Bangalore Days": "Dulquer Salmaan & Nazriya Nazim",
    "Lucifer": "Mohanlal & Manju Warrier",
    "Trance": "Fahadh Faasil & Nazriya Nazim",
    "Angamaly Diaries": "Antony Varghese & Reshma Rajan",
    "Ayyappanum Koshiyum": "Prithviraj Sukumaran & Biju Menon",
    "Maheshinte Prathikaaram": "Fahadh Faasil & Anusree",
    "Thondimuthalum Driksakshiyum": "Fahadh Faasil & Nimisha Sajayan",
    "Ustad Hotel": "Dulquer Salmaan & Nithya Menen",
    "Sudani from Nigeria": "Soubin Shahir & Samuel Abiola Robinson",
    "Joji": "Fahadh Faasil & Unnimaya Prasad",
    "Minnal Murali": "Tovino Thomas & Guru Somasundaram",
    "Charlie": "Dulquer Salmaan & Parvathy Thiruvothu",
    "Mumbai Police": "Prithviraj Sukumaran & Jayasurya",
    "Memories": "Prithviraj Sukumaran & Meghana Raj",
    "Churuli": "Chemban Vinod Jose & Joju George",
    "Baahubali: The Beginning": "Prabhas & Tamannaah",
    "Baahubali 2: The Conclusion": "Prabhas & Anushka Shetty",
    "RRR": "NTR Jr. & Ram Charan",
    "Jersey": "Nani & Shraddha Srinath",
    "Arjun Reddy": "Vijay Deverakonda & Shalini Pandey",
    "Eega": "Nani & Samantha",
    "Mahanati": "Keerthy Suresh & Dulquer Salmaan",
    "Pushpa: The Rise": "Allu Arjun & Rashmika Mandanna",
    "Ala Vaikunthapurramuloo": "Allu Arjun & Pooja Hegde",
    "Sita Ramam": "Dulquer Salmaan & Mrunal Thakur",
    "Rangasthalam": "Ram Charan & Samantha",
    "Magadheera": "Ram Charan & Kajal Aggarwal",
    "Athadu": "Mahesh Babu & Trisha",
    "Pokiri": "Mahesh Babu & Ileana D'Cruz",
    "Bommarillu": "Siddharth & Genelia D'Souza",
    "C/o Kancharapalem": "Subba Rao & Radha Bessy",
    "Mathu Vadalara": "Sri Simha & Naresh Agastya",
    "Agent Sai Srinivasa Athreya": "Naveen Polishetty & Shruti Sharma",
    "Dangal": "Aamir Khan & Fatima Sana Shaikh",
    "3 Idiots": "Aamir Khan & Kareena Kapoor",
    "Lagaan": "Aamir Khan & Gracy Singh",
    "Sholay": "Amitabh Bachchan & Hema Malini",
    "Andhadhun": "Ayushmann Khurrana & Tabu",
    "Tumbbad": "Sohum Shah & Jyoti Malshe",
    "K.G.F: Chapter 1": "Yash & Srinidhi Shetty",
    "Kantara": "Rishab Shetty & Sapthami Gowda",
    "Parasite": "Song Kang-ho & Cho Yeo-jeong",
    "Spirited Away": "Rumi Hiiragi & Miyu Irino",
    "Spider-Man: Into the Spider-Verse": "Shameik Moore & Hailee Steinfeld"
}

# 3. Apply the filters
filtered_data = data.copy()
filtered_data['Lead Actor / Actress'] = filtered_data['Movie Title'].map(actor_mapping).fillna('Ensemble Cast')

if search_term:
    filtered_data = filtered_data[
        filtered_data['Movie Title'].str.contains(search_term, case=False) |
        filtered_data['Director'].str.contains(search_term, case=False) |
        filtered_data['Lead Actor / Actress'].str.contains(search_term, case=False)
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

# ---------------------------------------------------------
# SINGLE PAGE CONTENT LAYOUT
# ---------------------------------------------------------

if not filtered_data.empty:
    st.subheader("Raw Data Table & Scale Categorization")
    
    display_data = filtered_data.copy()
    
    def get_bo_scale(revenue):
        if revenue >= 500:
            return "Mega Blockbuster"
        elif revenue >= 100:
            return "Major Hit"
        else:
            return "Standard Revenue"

    display_data['Box Office Scale'] = display_data['Box Office'].apply(get_bo_scale)
    display_data.insert(0, 'S.No', range(1, len(display_data) + 1))
    
    st.dataframe(
        display_data, 
        hide_index=True, 
        use_container_width=True,
        column_config={
            "IMDB Rating": st.column_config.ProgressColumn("IMDB Rating", format="%f", min_value=0, max_value=10),
            "Lead Actor / Actress": st.column_config.TextColumn("Lead Actor / Actress"),
            "Votes": st.column_config.NumberColumn("Total Votes", format="%d"),
            "Duration": st.column_config.NumberColumn("Duration", format="%d mins"),
            "Year": st.column_config.NumberColumn("Year", format="%d"),
            "Box Office": st.column_config.NumberColumn("Box Office 💰", format="$%d M"),
            "Box Office Scale": st.column_config.TextColumn("Box Office Scale")
        }
    )
    
    csv = display_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Dataset as CSV",
        data=csv,
        file_name="filtered_movies.csv",
        mime="text/csv",
    )
    
    st.divider()
    
    # --- QUICK BREAKDOWN BY GENRE ---
    st.subheader("📋 Quick Breakdown by Genre")
    genre_summary = filtered_data.groupby('Genre').agg(
        Movie_Count=('Movie Title', 'count'),
        Avg_Rating=('IMDB Rating', 'mean'),
        Total_Revenue_M=('Box Office', 'sum')
    ).reset_index()
    genre_summary['Avg_Rating'] = genre_summary['Avg_Rating'].round(1)
    st.dataframe(genre_summary, hide_index=True, use_container_width=True)
        
    st.divider()

    # --- DATASET HIGHLIGHTS & EXTREMES ---
    st.header("Dataset Highlights & Extremes")
    highest_grossing = filtered_data.loc[filtered_data['Box Office'].idxmax()]
    
    st.subheader("💰 Revenue Highlight")
    st.success(f"**Highest Grossing Film:** {highest_grossing['Movie Title']} (${highest_grossing['Box Office']} Million)")
    st.write("")

    shortest = filtered_data.loc[filtered_data['Duration'].idxmin()]
    longest = filtered_data.loc[filtered_data['Duration'].idxmax()]

    st.subheader("⏱️ Runtime Extremes")
    ext1, ext2 = st.columns(2)
    with ext1:
        st.info(f"**Shortest Film:** {shortest['Movie Title']} ({shortest['Duration']} mins)")
    with ext2:
        st.info(f"**Longest Film:** {longest['Movie Title']} ({longest['Duration']} mins)")

    st.divider()

    # --- VISUAL INSIGHTS (DIVERSIFIED CHART TYPES) ---
    st.header("📈 Visual Insights")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌟 Top 10 Rated Films (Horizontal Ranking)")
        top_rating = filtered_data.nsmallest(10, 'IMDB Rating').sort_values('IMDB Rating', ascending=True) if len(filtered_data) >= 10 else filtered_data.sort_values('IMDB Rating', ascending=True)
        top_rating = filtered_data.nlargest(10, 'IMDB Rating').sort_values('IMDB Rating', ascending=True)
        fig_rating = px.bar(top_rating, x='IMDB Rating', y='Movie Title', orientation='h', text='IMDB Rating', color='IMDB Rating', color_continuousScale='sunset')
        fig_rating.update_layout(xaxis_title="IMDB Rating", yaxis_title="")
        st.plotly_chart(fig_rating, use_container_width=True)

    with col2:
        st.subheader("💰 Rating vs. Box Office Correlation (Bubble Scatter)")
        fig_scatter = px.scatter(
            filtered_data, 
            x='IMDB Rating', 
            y='Box Office', 
            size='Votes', 
            color='Genre',
            hover_name='Movie Title',
            labels={'Box Office': 'Box Office ($M)', 'IMDB Rating': 'IMDB Rating'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🎭 Genre Proportions (Donut Chart)")
        genre_counts = filtered_data['Genre'].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        fig_donut = px.pie(genre_counts, names='Genre', values='Count', hole=0.4)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col4:
        st.subheader("🗳️ Most Voted Films (Horizontal Ranking)")
        top_votes = filtered_data.nlargest(10, 'Votes').sort_values('Votes', ascending=True)
        fig_votes = px.bar(top_votes, x='Votes', y='Movie Title', orientation='h', color='Votes', color_continuousScale='purples')
        fig_votes.update_layout(xaxis_title="Total Votes", yaxis_title="")
        st.plotly_chart(fig_votes, use_container_width=True)

    st.divider()

    st.subheader("📊 Historical Quality Trajectory (Filled Area Trend)")
    yearly_trend = filtered_data.groupby('Year')['IMDB Rating'].mean().reset_index()
    fig_area = px.area(yearly_trend, x='Year', y='IMDB Rating', markers=True, line_shape='spline')
    fig_area.update_layout(xaxis_title="Release Year", yaxis_title="Average IMDB Rating")
    st.plotly_chart(fig_area, use_container_width=True)
    
else:
    st.warning("No records match your active parameters. Please broaden your filter criteria.")

# --- PROFESSIONAL FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>"
    "Multi-Region Cinema Analytics Portal | Built with Python, Pandas & Streamlit | Professional Portfolio Edition"
    "</p>", 
    unsafe_allow_html=True
)

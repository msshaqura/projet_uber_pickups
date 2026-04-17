# dashboard_folium.py - Working dashboard with Folium
"""
Uber Pickups Hot Zones Dashboard - NYC
Using Folium for reliable map visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from sklearn.cluster import KMeans

# Page configuration
st.set_page_config(
    page_title="Uber Hot Zones - NYC",
    page_icon="🚕",
    layout="wide"
)

st.title("🚕 Uber Pickups Hot Zones - New York City")
st.markdown("*Data-driven recommendations for Uber drivers*")

# Colors for clusters (defined outside sidebar)
cluster_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue']

# Sidebar
with st.sidebar:
    
    # Logo 
    st.image("../images/uber_logo.png", width=200)

    # Title
    st.markdown("""
        <h1 style='color:#0071CE;'>Uber Pickups Dashboard</h1>
        """, unsafe_allow_html=True)

    # Separator
    st.markdown("---")

    # Author section
    st.markdown("### 👨‍💻 Présenté par")
    st.markdown("**Mohammed SHAQURA**")
    st.markdown("Data Analyst | Uber Pickups Project")
    st.markdown("**Jedha Bootcamp**")

    # Separator
    st.markdown("---")

    st.header("⚙️ Filters")
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    
    selected_day_name = st.selectbox("Select Day of Week", list(day_names.values()))
    selected_day_num = {v: k for k, v in day_names.items()}[selected_day_name]
    selected_hour = st.slider("Select Hour (0-23)", 0, 23, 18)
    k_clusters = st.selectbox("Number of Clusters (K)", [3, 4, 5, 6, 7], index=2)
    max_points = st.slider("Max points for visualization", 1000, 15000, 5000)

@st.cache_data
def load_filtered_data(day_num, hour, max_points):
    """Load data in chunks"""
    data_folder = "../uber_trip_data"
    months = [
        "uber-raw-data-apr14.csv",
        "uber-raw-data-may14.csv",
        "uber-raw-data-jun14.csv",
        "uber-raw-data-jul14.csv",
        "uber-raw-data-aug14.csv",
        "uber-raw-data-sep14.csv"
    ]
    
    filtered_rows = []
    total = 0
    
    for month in months:
        file_path = f"{data_folder}/{month}"
        
        for chunk in pd.read_csv(file_path, chunksize=50000, usecols=['Date/Time', 'Lat', 'Lon']):
            chunk['DateTime'] = pd.to_datetime(chunk['Date/Time'], errors='coerce')
            chunk['Hour'] = chunk['DateTime'].dt.hour
            chunk['DayOfWeek'] = chunk['DateTime'].dt.dayofweek
            
            mask = (chunk['DayOfWeek'] == day_num) & (chunk['Hour'] == hour)
            filtered = chunk[mask]
            
            if len(filtered) > 0:
                filtered_rows.append(filtered[['Lat', 'Lon']])
                total += len(filtered)
            
            if total >= max_points:
                break
        
        if total >= max_points:
            break
    
    if not filtered_rows:
        return pd.DataFrame(columns=['Lat', 'Lon'])
    
    result = pd.concat(filtered_rows, ignore_index=True)
    
    # NYC bounds
    result = result[
        (result['Lat'].between(40.5, 41.0)) & 
        (result['Lon'].between(-74.5, -73.7))
    ]
    
    if len(result) > max_points:
        result = result.sample(max_points, random_state=42)
    
    return result

# Load data
with st.spinner(f"Loading data for {selected_day_name} at {selected_hour}:00..."):
    df = load_filtered_data(selected_day_num, selected_hour, max_points)

if len(df) < 50:
    st.warning(f"⚠️ Only {len(df)} pickups found. Please select another day/hour.")
else:
    st.success(f"✓ Loaded {len(df):,} pickups")
    
    # Apply clustering
    with st.spinner("Applying KMeans clustering..."):
        X = df[['Lat', 'Lon']].values
        kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        centroids = kmeans.cluster_centers_
    
    # Add cluster labels
    df['Cluster'] = labels
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pickups", f"{len(df):,}")
    with col2:
        st.metric("Clusters (K)", k_clusters)
    with col3:
        unique, counts = np.unique(labels, return_counts=True)
        best_pct = (counts.max() / len(df)) * 100
        st.metric("Hottest Zone", f"{best_pct:.1f}%")
    with col4:
        st.metric("Selected Time", f"{selected_day_name} {selected_hour}:00")
    
    # Create Folium map
    st.markdown("### 🗺️ Hot Zones Map")
    
    # Base map
    m = folium.Map(
        location=[40.73, -73.98],
        zoom_start=11.5,
        tiles='CartoDB positron'
    )
    
    # Add title to map
    title_html = f'''
    <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
                z-index: 1000; background: white; padding: 8px 16px;
                border-radius: 8px; border: 2px solid black;
                font-weight: bold; font-size: 14px;">
        {selected_day_name} at {selected_hour}:00 - K={k_clusters}
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Add pickup points for each cluster
    for i in range(k_clusters):
        cluster_df = df[df['Cluster'] == i]
        if len(cluster_df) > 0:
            # Use MarkerCluster to group nearby points (better performance)
            marker_cluster = MarkerCluster(name=f'Cluster {i} ({len(cluster_df)} pickups)')
            
            for _, row in cluster_df.iterrows():
                folium.CircleMarker(
                    location=[row['Lat'], row['Lon']],
                    radius=3,
                    color=cluster_colors[i % len(cluster_colors)],
                    fill=True,
                    fill_opacity=0.5,
                    popup=f'Cluster {i}'
                ).add_to(marker_cluster)
            
            marker_cluster.add_to(m)
    
    # Add centroids with star markers
    for i, (lat, lon) in enumerate(centroids):
        # Star marker using DivIcon
        star_html = f'''
        <div style="text-align: center;">
            <span style="font-size: 22px; color: black;">★</span>
            <br>
            <span style="font-size: 11px; font-weight: bold; background: white;
                       padding: 2px 5px; border-radius: 10px; border: 1px solid black;">
                C{i}
            </span>
        </div>
        '''
        
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(html=star_html),
            popup=f'Centroid C{i}: ({lat:.4f}, {lon:.4f})',
            tooltip=f'★ C{i} - Recommended position'
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Display map
    folium_static(m, width=1000, height=600)
    
    # Statistics table
    st.markdown("### 📊 Cluster Statistics")
    stats = []
    for i in range(k_clusters):
        cluster_df = df[df['Cluster'] == i]
        pct = (len(cluster_df) / len(df)) * 100
        stats.append({
            'Cluster': i,
            'Pickups': len(cluster_df),
            'Percentage': f"{pct:.1f}%",
            'Centroid': f"({centroids[i][0]:.4f}, {centroids[i][1]:.4f})"
        })
    
    st.dataframe(pd.DataFrame(stats), use_container_width=True)
    
    # Recommendation
    best_cluster = max(stats, key=lambda x: x['Pickups'])
    st.success(f"""
    **📌 Driver Recommendation for {selected_day_name} at {selected_hour}:00**  
    Position yourself near **Cluster {best_cluster['Cluster']}** at coordinates {best_cluster['Centroid']}.  
    This zone contains **{best_cluster['Percentage']}** of all pickups in this time slot.
    """)


# ============================================
# FOOTER 
# ============================================
# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'> Uber Pickups Dashboard | Created by Streamlit </p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: gray;'> Project developed as part of the BLOC 3 certification | Jedha Bootcamp </p>",
    unsafe_allow_html=True
)
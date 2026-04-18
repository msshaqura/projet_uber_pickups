# 📧 Conversion Rate Prediction - Data Science Weekly
[![Hugging Face Spaces](https://img.shields.io/badge/🤗-Live%20App-yellow)]
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.8.0-orange)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-Container-blue)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
## 🎯 Live Demo
https://huggingface.co/spaces/msshaqura/uber_pickups_project


# 🚕 Uber Pickups Hot Zones - New York City

## Project Overview

This project analyzes **4.5 million Uber pickups** in New York City (April - September 2014) to identify **hot zones** for drivers using **KMeans clustering**.

The goal is to help Uber drivers position themselves where demand is highest, reducing passenger wait times from 10-15 minutes to under 7 minutes.

## Features

- ✅ **Interactive Dashboard** built with Streamlit & Folium
- ✅ **Real-time clustering** with adjustable K (3-7 clusters)
- ✅ **Filter by day of week** (Monday - Sunday)
- ✅ **Filter by hour** (0-23)
- ✅ **Centroid markers (★)** showing optimal driver positions
- ✅ **Cluster statistics** with pickups count and percentage

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Pandas | Data manipulation & chunked loading |
| Scikit-learn | KMeans clustering |
| Folium | Interactive maps (CARTO Positron) |
| Streamlit | Web dashboard |
| Plotly | Additional visualizations |

## Project Structure
projet_uber_pickups/
│
├── uber_trip_data/ # Raw CSV files (not on GitHub)
├── notebooks/ # Jupyter notebooks for analysis
│ └── uber_pickups_analysis.ipynb
├── dashboard/ # Streamlit application
│ └── app.py
├── images/ # Assets
│ └── uber_logo.png
├── requirements.txt # Python dependencies
├── README.md # This file
└── .gitignore # Git ignore rules


## Installation & Local Run

### 1. Clone the repository
git clone https://github.com/msshaqura/projet_uber_pickups.git


### 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the dashboard
cd dashboard
streamlit run app.py

### Dashboard Preview
The dashboard allows you to:

Select day of week and hour

Adjust number of clusters (K)

View interactive map with colored clusters and centroids

See cluster statistics and driver recommendations

### Key Findings
| Day	| Peak Hour |	Hot Zones |
|-------|-----------|-------------|
| Saturday | 6:00 PM | Downtown Manhattan (40.8%), Midtown (34.2%) |
| Friday | 6:00 PM | Manhattan clusters dominate |
| Thursday | 5:00 PM | Strong mid-week demand | 

Best time for drivers: Saturday at 6:00 PM (1.31M pickups across 15 months)

### Future Improvements
Add predictive model (demand forecasting per zone)

Integrate real-time traffic data

Expand to other cities (Chicago, San Francisco)

### Author
Mohammed SHAQURA
Data Analyst | Jedha Bootcamp

### License
This project is for educational purposes as part of the Jedha Bootcamp certification.

### Acknowledgments
Data source: Uber NYC pickups (2014-2015)

Map tiles: CARTO Positron
		
		
		
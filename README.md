# Starlink Satellite Tracker

An interactive Streamlit application to monitor and visualize the real-time positions of Elon Musk's Starlink satellites. This app fetches the latest orbital data, calculates satellite positions using Skyfield, and displays them on an interactive world map with Plotly. Users can:

- View current positions of all Starlink satellites.
- Filter satellites over a specific location by latitude, longitude, and radius.
- Visualize satellite data in tabular form and on an interactive map.
- Experience real-time data updates each time the app runs.

**Features:**

- **Interactive Interface**: User-friendly web application built with Streamlit.
- **Real-Time Data**: Fetches up-to-date TLE data from Celestrak to ensure accurate satellite positioning.
- **Dynamic Visualization**: Utilizes Plotly for interactive map displays and data visualization.
- **Custom Filtering**: Allows users to input specific coordinates and radius to find satellites over a particular area.

**Getting Started:**

1. **Prerequisites**:

   - Python 3.7 or higher
   - Packages: `streamlit`, `skyfield`, `requests`, `pandas`, `plotly`

2. **Installation**:

   ```bash
   git clone https://github.com/yourusername/starlink-satellite-tracker.git
   cd starlink-satellite-tracker
   pip install -r requirements.txt
  ```

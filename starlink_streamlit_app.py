import streamlit as st
from skyfield.api import Loader, EarthSatellite
import requests
import pandas as pd
import plotly.express as px

def fetch_tle_data():
    tle_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle'
    try:
        response = requests.get(tle_url)
        response.raise_for_status()
        tle_data = response.text.strip().split('\n')
        return tle_data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching TLE data: {e}")
        return None

def parse_tle_data(tle_data, ts):
    satellites = []
    for i in range(0, len(tle_data), 3):
        try:
            name = tle_data[i].strip()
            line1 = tle_data[i + 1].strip()
            line2 = tle_data[i + 2].strip()
            satellite = EarthSatellite(line1, line2, name, ts)
            satellites.append(satellite)
        except IndexError:
            st.warning(f"Incomplete TLE data for satellite starting at line {i}")
        except Exception as e:
            st.warning(f"Error parsing TLE data at line {i}: {e}")
    return satellites

def get_satellite_positions(satellites, ts):
    t = ts.now()
    data = []
    for sat in satellites:
        try:
            geocentric = sat.at(t)
            subpoint = geocentric.subpoint()
            data.append({
                'Name': sat.name,
                'Latitude': subpoint.latitude.degrees,
                'Longitude': subpoint.longitude.degrees,
                'Altitude': subpoint.elevation.km
            })
        except Exception as e:
            st.warning(f"Error computing position for {sat.name}: {e}")
    return pd.DataFrame(data)

def main():
    st.title("Starlink Satellites Tracker")
    st.markdown("""
    This application fetches and displays the current positions of Elon Musk's Starlink satellites.
    """)

    # Initialize the Skyfield loader
    load = Loader('~/skyfield-data')
    ts = load.timescale()

    # Fetch TLE data
    with st.spinner("Fetching TLE data..."):
        tle_data = fetch_tle_data()
    if not tle_data:
        st.error("Failed to retrieve TLE data.")
        return

    # Parse TLE data
    with st.spinner("Parsing TLE data..."):
        satellites = parse_tle_data(tle_data, ts)

    # Get satellite positions
    with st.spinner("Computing satellite positions..."):
        df = get_satellite_positions(satellites, ts)

    # Display data
    st.subheader("Satellite Positions")
    st.dataframe(df)

    # Interactive Map
    st.subheader("Satellites on World Map")
    fig = px.scatter_geo(df,
                         lat='Latitude',
                         lon='Longitude',
                         hover_name='Name',
                         projection="natural earth",
                         title='Starlink Satellites Positions')
    st.plotly_chart(fig, use_container_width=True)

    # Filter satellites over a specific location
    st.subheader("Filter Satellites Over a Specific Location")
    lat = st.number_input("Latitude (-90 to 90)", min_value=-90.0, max_value=90.0, value=0.0)
    lon = st.number_input("Longitude (-180 to 180)", min_value=-180.0, max_value=180.0, value=0.0)
    radius = st.number_input("Radius in Degrees", min_value=0.1, max_value=180.0, value=10.0)

    if st.button("Filter Satellites"):
        filtered_df = df[
            (df['Latitude'] >= lat - radius) & (df['Latitude'] <= lat + radius) &
            (df['Longitude'] >= lon - radius) & (df['Longitude'] <= lon + radius)
        ]
        st.write(f"Satellites within {radius}° of ({lat}°, {lon}°):")
        st.dataframe(filtered_df)

        # Map of filtered satellites
        fig_filtered = px.scatter_geo(filtered_df,
                                      lat='Latitude',
                                      lon='Longitude',
                                      hover_name='Name',
                                      projection="natural earth",
                                      title='Filtered Starlink Satellites')
        st.plotly_chart(fig_filtered, use_container_width=True)

if __name__ == "__main__":
    main()

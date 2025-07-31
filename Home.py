import streamlit as st
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium, folium_static
import requests
import random
import pandas as pd

# -----------------------
st.set_page_config(page_title="Petrol Station Finder", layout="centered")
st.title("⛽ Petrol Station Finder")
st.markdown("This application is designed to help you find the nearest petrol station to your chosen location, and compare the prices around you so that you can make a more informed decision!")
st.write("👉 Click on the map to set your location.")

# --- Map Setup ---
default_location = [-33.918861, 18.4233]  # Cape Town center
map_ = folium.Map(location=default_location, zoom_start=12)
map_data = st_folium(map_, width=700, height=400)

# --- Radius Input ---
st.write("👉 How many kilometres around your location do you want to search?")
radius = st.number_input("📏 Radius (km)", min_value=1, max_value=50, value=5)

# --- Fuel Type Input ---
fuel_type = st.selectbox("⛽ Select fuel type", ["93", "95", "Diesel 50", "Diesel 500"])

# --- User Inputs ---
fuel_eff = st.number_input("🚗 Fuel consumption (L/100km)", value=7.0)
litres_needed = st.number_input("🛢️ Litres to fill", value=30.0)

# --- Function: Fetch Real Stations from OpenStreetMap ---
def fetch_stations(lat, lng, radius_km=radius):
    overpass_url = "http://overpass-api.de/api/interpreter"
    radius_m = radius_km * 1000
    query = f"""
    [out:json];
    (
      node["amenity"="fuel"](around:{radius_m},{lat},{lng});
    );
    out center;
    """
    response = requests.get(overpass_url, params={"data": query})
    data = response.json()

    fuel_types = ["93", "95", "Diesel 50", "Diesel 500"]

    stations = []
    for element in data["elements"]:
        name = element.get("tags", {}).get("name", "Unnamed Station")
        station_lat = element["lat"]
        station_lng = element["lon"]
        prices = {
            ft: round(random.uniform(21.5, 23.5), 2) for ft in fuel_types
        }
        stations.append({
            "name": name,
            "lat": station_lat,
            "lng": station_lng,
            "prices": prices
        })

    return stations

# --- Process after user selects location ---
if map_data and map_data.get("last_clicked"):
    user_lat = map_data["last_clicked"]["lat"]
    user_lng = map_data["last_clicked"]["lng"]
    user_location = (user_lat, user_lng)

    st.success(f"📍 Selected Location: {user_lat:.5f}, {user_lng:.5f}")
    stations = fetch_stations(user_lat, user_lng, radius_km=radius)

    if not stations:
        st.warning("⚠️ No stations found in this radius.")
    else:
        # --- Calculate Costs ---
        for station in stations:
            station_loc = (station["lat"], station["lng"])
            distance_km = geodesic(user_location, station_loc).km
            station["distance_km"] = round(distance_km, 2)

            price = station["prices"][fuel_type]
            litres_used = (fuel_eff / 100) * distance_km
            travel_cost = litres_used * price
            fill_cost = litres_needed * price
            total_cost = travel_cost + fill_cost

            station["price"] = price
            station["travel_cost"] = round(travel_cost, 2)
            station["fill_cost"] = round(fill_cost, 2)
            station["total_cost"] = round(total_cost, 2)

        # --- Sort and Display ---
        stations = sorted(stations, key=lambda s: s["total_cost"])

        st.subheader("📊 Station Comparison")
        data = [{
            "Station": s["name"],
            "Distance (km)": s["distance_km"],
            "Price (R/L)": f"R{s['price']:.2f}",
            "Travel Cost (R)": f"R{s['travel_cost']:.2f}",
            "Fill Cost (R)": f"R{s['fill_cost']:.2f}",
            "Total Cost (R)": f"R{s['total_cost']:.2f}"
        } for s in stations]

        df = pd.DataFrame(data)
        st.table(df)

        best = stations[0]
        st.success(f"🏆 Best option: **{best['name']}** with total cost R{best['total_cost']:.2f}")

        # --- Map with Stations ---
        map2 = folium.Map(location=user_location, zoom_start=13)
        folium.Marker(user_location, tooltip="You", icon=folium.Icon(color="blue")).add_to(map2)

        for s in stations:
            folium.Marker(
                location=(s["lat"], s["lng"]),
                popup=f"{s['name']} - R{s['price']:.2f}/L - Total: R{s['total_cost']:.2f}",
                icon=folium.Icon(color="green")
            ).add_to(map2)

        folium_static(map2)

else:
    st.info("📌 Waiting for you to click your location on the map above.")

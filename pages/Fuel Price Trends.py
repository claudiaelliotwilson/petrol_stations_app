import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 Historical Fuel Price Trends")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/fuel_prices.csv", parse_dates=["date"])
    return df

df = load_data()

# Sidebar filter
fuel_type = st.selectbox("Select Fuel Type", df["fuel_type"].unique())

filtered_df = df[df["fuel_type"] == fuel_type]

# Line chart
st.subheader(f"Price Trend for {fuel_type}")
fig, ax = plt.subplots()
sns.lineplot(data=filtered_df, x="date", y="price", ax=ax)
ax.set_ylabel("Price (R/litre)")
ax.set_xlabel("Date")
st.pyplot(fig)

# Summary statistics
st.subheader("📌 Summary Statistics")
st.write(filtered_df["price"].describe())

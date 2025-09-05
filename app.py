import streamlit as st
import pandas as pd
from vod_data import df


# Filters
st.title("📺 VOD Error Health Dashboard")
platform = st.sidebar.selectbox("Platform", ["All"] + sorted(df["platform"].unique()))
check = st.sidebar.selectbox("Check", ["All"] + sorted(df["check"].unique()))
date_range = st.sidebar.date_input("Date Range", [])

# Filter data
filtered_df = df.copy()
if platform != "All":
    filtered_df = filtered_df[filtered_df["platform"] == platform]
if check != "All":
    filtered_df = filtered_df[filtered_df["check"] == check]
if date_range and len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["first_seen"].dt.date >= date_range[0]) &
        (filtered_df["first_seen"].dt.date <= date_range[1])
    ]

# Ensure datetime
filtered_df["first_seen"] = pd.to_datetime(filtered_df["first_seen"])
filtered_df["last_seen"] = pd.to_datetime(filtered_df["last_seen"])

# KPIs
total_errors = len(filtered_df)
awaiting_fix = len(filtered_df[filtered_df["status"] == "Awaiting Fix"])
noise = len(filtered_df[filtered_df["status"] == "No Fault Found"])

# Avg Time to Fix
fixed_df = filtered_df[filtered_df["status"] == "Awaiting Fix"]
if not fixed_df.empty:
    avg_fix_time = (fixed_df["last_seen"] - fixed_df["first_seen"]).mean()
    avg_fix_str = f"{avg_fix_time.total_seconds() / 3600:.1f} hrs"
else:
    avg_fix_str = "0 hrs"

# KPI Display
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Errors", total_errors)
col2.metric("% Awaiting Fix", f"{awaiting_fix / total_errors * 100:.1f}%" if total_errors else "0%")
col3.metric("% Noise", f"{noise / total_errors * 100:.1f}%" if total_errors else "0%")
col4.metric("Avg Time to Fix", avg_fix_str)

# Charts
st.subheader("🔍 Top 10 Noisiest Checks")
noisiest = filtered_df[filtered_df["status"] == "No Fault Found"]["check"].value_counts().head(10)
if not noisiest.empty:
    st.bar_chart(noisiest)
else:
    st.info("No noisy checks for this filter.")

st.subheader("📡 Errors by Platform")
platform_summary = filtered_df.groupby("platform")["status"].value_counts().unstack(fill_value=0)
if not platform_summary.empty:
    st.dataframe(platform_summary)
else:
    st.warning("No platform data for this filter.")

# Raw data toggle
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)

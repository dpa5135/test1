import streamlit as st
import pandas as pd

# ------------------------------
# CONFIG
# ------------------------------
st.set_page_config(page_title="Case Dashboard", layout="wide")

st.title("📊 Case Dashboard Demo")

# ------------------------------
# LOAD DATA
# ------------------------------
@st.cache_data
def load_data():
    file_path = "data.xlsx"
    df = pd.read_excel(file_path)
    return df

df = load_data()

# ------------------------------
# FILTERS
# ------------------------------
st.sidebar.header("Filters")

# Case ID search
case_id_search = st.sidebar.text_input("Search Case ID")

# Category filter
category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique()
)

# Risk filter
risk_filter = st.sidebar.multiselect(
    "Select Risk Level",
    options=df["Risk_Flag"].unique()
)

# Narrative search
text_search = st.sidebar.text_input("Search Narrative")

# ------------------------------
# APPLY FILTERS
# ------------------------------
filtered_df = df.copy()

if case_id_search:
    filtered_df = filtered_df[
        filtered_df["Case_ID"].astype(str).str.contains(case_id_search, case=False)
    ]

if category_filter:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(category_filter)
    ]

if risk_filter:
    filtered_df = filtered_df[
        filtered_df["Risk_Flag"].isin(risk_filter)
    ]

if text_search:
    filtered_df = filtered_df[
        filtered_df["Narrative"].str.contains(text_search, case=False, na=False)
    ]

# ------------------------------
# METRICS
# ------------------------------
st.subheader("Summary")

col1, col2 = st.columns(2)
col1.metric("Total Records", len(filtered_df))
col2.metric("High Risk Cases", len(filtered_df[filtered_df["Risk_Flag"] == "High"]))

# ------------------------------
# TABLE
# ------------------------------
st.subheader("Case Data")

st.dataframe(filtered_df, use_container_width=True)

# ------------------------------
# DOWNLOAD BUTTON
# ------------------------------
st.subheader("Download Filtered Data")

st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_cases.csv",
    mime="text/csv"
)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# PAGE CONFIG (IMPORTANT)
# -----------------------------
st.set_page_config(
    page_title="Africa Climate Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🌍 Africa Climate Trends Dashboard")
st.markdown("Climate analysis across Ethiopia, Kenya, Nigeria, Sudan, and Tanzania (2015–2026)")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.concat([
        pd.read_csv("data/ethiopia_clean.csv").assign(Country="Ethiopia"),
        pd.read_csv("data/kenya_clean.csv").assign(Country="Kenya"),
        pd.read_csv("data/nigeria_clean.csv").assign(Country="Nigeria"),
        pd.read_csv("data/sudan_clean.csv").assign(Country="Sudan"),
        pd.read_csv("data/tanzania_clean.csv").assign(Country="Tanzania"),
    ])

    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🎛 Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    df["Country"].unique(),
    default=df["Country"].unique()
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2015, 2026)
)

variable = st.sidebar.selectbox(
    "Select Climate Variable",
    ["T2M", "PRECTOTCORR", "RH2M", "WS2M"]
)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df[
    (df["Country"].isin(countries)) &
    (df["Year"].between(year_range[0], year_range[1]))
]

# -----------------------------
# KPI METRICS (TOP SECTION)
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries Selected", len(countries))
col2.metric("Avg Temperature", f"{filtered_df['T2M'].mean():.2f} °C")
col3.metric("Avg Rainfall", f"{filtered_df['PRECTOTCORR'].mean():.2f} mm")
col4.metric("Records", len(filtered_df))

st.divider()

# -----------------------------
# TEMPERATURE TREND
# -----------------------------
st.subheader("🌡 Temperature Trends")

monthly_temp = filtered_df.groupby(["Country", "Month"])["T2M"].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,5))

for c in monthly_temp["Country"].unique():
    temp_data = monthly_temp[monthly_temp["Country"] == c]
    ax.plot(temp_data["Month"], temp_data["T2M"], label=c)

ax.set_xlabel("Month")
ax.set_ylabel("Temperature (°C)")
ax.legend()

st.pyplot(fig)

# -----------------------------
# RAINFALL DISTRIBUTION
# -----------------------------
st.subheader("🌧 Rainfall Distribution")

fig, ax = plt.subplots(figsize=(10,5))
sns.boxplot(data=filtered_df, x="Country", y="PRECTOTCORR", ax=ax)

st.pyplot(fig)

# -----------------------------
# VARIABLE DISTRIBUTION
# -----------------------------
st.subheader(f"📊 Distribution of {variable}")

fig, ax = plt.subplots()
sns.histplot(filtered_df[variable], bins=30, kde=True, ax=ax)

st.pyplot(fig)

# -----------------------------
# CORRELATION HEATMAP
# -----------------------------
st.subheader("🔗 Correlation Heatmap")

numeric_cols = ["T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR", "RH2M", "WS2M"]

fig, ax = plt.subplots(figsize=(8,5))
sns.heatmap(filtered_df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("📌 Built for COP32 Climate Analysis – Africa Data Science Project")
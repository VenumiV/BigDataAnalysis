import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="IMovie Dashboard",
    layout="wide",
    page_icon="🎬"
)

# Load Data
df = pd.read_csv("cleaned_film_data.csv")

# Preprocessing
df["Viewing_Month"] = pd.to_datetime(df["Viewing_Month"])
df["Year"] = df["Viewing_Month"].dt.year
df["Popularity_Score"] = df["Viewer_Rate"] * df["Number_of_Views"]

# ======== Sidebar ========
st.sidebar.title("Filters")

years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

categories = df["Category"].unique()
selected_categories = st.sidebar.multiselect(
    "Select Category", categories, default=categories
)

languages = df["Language"].unique()
selected_languages = st.sidebar.multiselect(
    "Select Language", languages, default=languages
)

# Filter Main Data
filtered_df = df[
    (df["Year"] == selected_year) &
    (df["Category"].isin(selected_categories)) &
    (df["Language"].isin(selected_languages))
]

# ======== Title ========
st.title("IMovie – December 2025 Marketing Strategy Dashboard")
st.write("**Interactive dashboard for category insights, language trends, top films & future predictions.**")
st.markdown("---")

# ======== KPI CARDS ========
total_views = df["Number_of_Views"].sum()
avg_rating = round(df["Viewer_Rate"].mean(), 2)
top_category = df.groupby("Category")["Number_of_Views"].sum().idxmax()
top_language = df.groupby("Language")["Number_of_Views"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.metric("📈 Total Views", f"{total_views:,}")
col2.metric("⭐ Average Viewer Rate", avg_rating)
col3.metric("🏆 Most Popular Category", top_category)
col4.metric("🌍 Top Language", top_language)




# ======== TABS ========
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Category Insights",
    "🌍 Language Insights",
    "🔥 Top Films",
    "📈 Prediction for 2026"
])

# ========================= TAB 1 =========================
with tab1:
    st.subheader("Views by Category")
    category_views = filtered_df.groupby("Category")["Number_of_Views"].sum()
    st.bar_chart(category_views)

    st.subheader("Average Viewer Rate by Category")
    category_ratings = filtered_df.groupby("Category")["Viewer_Rate"].mean()
    st.line_chart(category_ratings)

# ========================= TAB 2 =========================

with tab2:
    st.subheader("Language Performance Overview")



    # LANGUAGE PERFORMANCE
    st.markdown("### Views by Language")
    lang_views = filtered_df.groupby("Language")["Number_of_Views"].sum()

    if not lang_views.empty:
        st.bar_chart(lang_views)
    else:
        st.warning("No data available for selected filters.")




# ========================= TAB 3 =========================
with tab3:
    st.subheader("Top 10 Films by Popularity Score")
    top_films = (
        filtered_df.groupby("Film_Name")["Popularity_Score"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.write(top_films)
    st.bar_chart(top_films)

# ========================= TAB 4 =========================
with tab4:
    st.subheader("Predicted Most-Loved Films for 2026")


    # ================= CATEGORY PREDICTION =================
    st.markdown("### Predicted Best-Performing Categories in 2026")
    cat_pred = (
        df.groupby("Category")["Popularity_Score"]
        .mean()
        .sort_values(ascending=False)
    )

    cat_pred_df = cat_pred.reset_index()
    cat_pred_df.columns = ["Category", "Predicted_Popularity"]

    st.write(cat_pred_df)
    st.bar_chart(cat_pred_df.set_index("Category"))

    # ================= LANGUAGE PREDICTION =================
    st.markdown("### 🔹 Predicted Best-Performing Languages in 2026")
    lang_pred = (
        df.groupby("Language")["Popularity_Score"]
        .mean()
        .sort_values(ascending=False)
    )

    lang_pred_df = lang_pred.reset_index()
    lang_pred_df.columns = ["Language", "Predicted_Popularity"]

    st.write(lang_pred_df)
    st.bar_chart(lang_pred_df.set_index("Language"))

    st.info("""
    Predictive Method Used:
    • Popularity Score = Viewer_Rate × Number_of_Views  
    • Higher average popularity indicates higher demand for 2026.
    """)

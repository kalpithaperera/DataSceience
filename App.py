import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Setting page configuration
st.set_page_config(
    page_title="Global Superstore Data Sales Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",  # Adjust layout as needed
)

# Load data
def load_data(file_path: str) -> pd.DataFrame | None:
    """Load data from CSV file"""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

# Sample data (replace with your CSV path)
df = load_data("Processed_GlobalSuperstore.csv")

if df is None:
    st.stop()

# Create sidebar for interactive filters
def create_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Create filters for data"""
    with st.sidebar:
        # Filter by category
        category_filter = st.multiselect(
            "Filter by Category",
            options=df["Category"].unique(),
            default=df["Category"].unique(),
        )
        df_filtered = df[df["Category"].isin(category_filter)]

        # Filter by sales channel (if applicable)
        if "Sales Channel" in df.columns:
            sales_channel_filter = st.multiselect(
                "Filter by Sales Channel",
                options=df["Sales Channel"].unique(),
                default=df["Sales Channel"].unique(),
            )
            df_filtered = df_filtered[df_filtered["Sales Channel"].isin(sales_channel_filter)]

        return df_filtered

df_filtered = create_filters(df)

# Key Performance Indicators (KPIs)
def calculate_kpis(df: pd.DataFrame) -> tuple:
    """Calculate KPIs"""
    total_sales = df["Sales"].sum().astype(float)
    average_profit_margin = df["Profit"].mean().astype(float)
    return total_sales, average_profit_margin

def create_kpi_metrics(kpi_values: tuple) -> None:
    """Create Streamlit metrics"""
    kpi1 = st.metric(label="Total Sales", value=kpi_values[0])
    kpi2 = st.metric(label="Average Profit Margin", value=kpi_values[1])

kpi_values = calculate_kpis(df_filtered)
create_kpi_metrics(kpi_values)

# Visualizations
def create_visualizations(df: pd.DataFrame) -> None:
    """Create visualizations"""
    # Visualization 1: Sales by Region
    ax = df.groupby("Region")["Sales"].sum().plot(kind="bar", title="Sales by Region")
    st.pyplot(ax)
    st.markdown("---")

    # Visualization 2: Sales by Category (Pie Chart)
    ax = df_filtered.groupby("Category")["Sales"].sum().plot(kind="pie", title="Sales by Category")
    st.pyplot(ax)
    st.markdown("---")

    # Visualization 3: Sales by Sub-Category
    ax = df.groupby("Sub-Category")["Sales"].sum().plot(kind="bar", title="Sales by Sub-Category")
    st.pyplot(ax)
    st.markdown("---")

    # Visualization 4: Profit by Country
    ax = df.groupby("Country")["Profit"].sum().plot(kind="bar", title="Profit by Country")
    st.pyplot(ax)

create_visualizations(df_filtered)


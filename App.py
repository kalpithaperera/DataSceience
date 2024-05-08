import streamlit as st
import pandas as pd
import plotly as px

# Setting page configuration
st.set_page_config(
    page_title="Global Superstore Data Sales Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide", 
)

# Load data (with improved error handling)
def load_data(file_path: str) -> pd.DataFrame | None:
    """Load data from CSV file"""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("CSV file not found. Please check the file path.")
        return None
    except Exception as e:  # Catch more general errors
        st.error(f"An error occurred while loading data: {e}")
        return None

# Sample data (replace with your CSV path)
df = load_data("Processed_GlobalSuperstore_data.csv")

if df is None:
    st.stop()

# Sidebar for filters
def create_filters(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        category_filter = st.multiselect(
            "Filter by Category",
            options=df["Category"].unique(),
            default=df["Category"].unique(),
        )
        df_filtered = df[df["Category"].isin(category_filter)]

        if "Sales Channel" in df.columns:
            sales_channel_filter = st.multiselect(
                "Filter by Sales Channel",
                options=df["Sales Channel"].unique(),
                default=df["Sales Channel"].unique(),
            )
            df_filtered = df_filtered[df_filtered["Sales Channel"].isin(sales_channel_filter)]

        return df_filtered

df_filtered = create_filters(df)

# KPIs 
def calculate_kpis(df: pd.DataFrame) -> tuple:
    total_sales = df["Sales"].sum().astype(float)
    average_profit_margin = df["Profit"].mean().astype(float)
    return total_sales, average_profit_margin

def create_kpi_metrics(kpi_values: tuple) -> None:
    col1, col2 = st.columns(2)  # Arrange metrics in columns
    with col1:
        st.metric(label="Total Sales", value=f"${kpi_values[0]:,.2f}")
    with col2:
        st.metric(label="Average Profit Margin", value=f"{kpi_values[1] * 100:.2f}%") 

kpi_values = calculate_kpis(df_filtered)
create_kpi_metrics(kpi_values)

# Visualizations
def create_visualizations(df: pd.DataFrame) -> None:
    st.header("Visualizations")  # Add a header for the section
    # Visualization 1: Sales by Region
    sales_by_region = px.bar(df, x="Region", y="Sales", color="Region", title="Sales by Region")
    st.plotly_chart(sales_by_region)
    st.markdown("---")

    # Other visualizations (same as your original code)
    # ... 

create_visualizations(df_filtered) 

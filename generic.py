import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import plotly.express as px

st.set_page_config(
    page_title="Excel File Analyzer & Incident Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    r"""
    <style>
    .stAppDeployButton {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("CSV File Report Generator")

# Add a image to the sidebar
st.sidebar.image(
    "./images/logo.png",
)
st.sidebar.header("Data profiler and visualizer")
st.sidebar.markdown(
    """
    This app allows you to upload a CSV file and generate a data profiling report using YData Profiling.
    You can also create custom charts based on the uploaded data.
    """
)

st.sidebar.markdown(
    """
    ---
    """
)

st.sidebar.header("Upload and Options")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    report_type = st.sidebar.radio(
        "Choose a report type:",
        ["YData Profiling", "Custom Report"],
        index=0,
    )

    st.subheader("Uploaded Data Preview")
    st.write(df.head())

    if report_type == "YData Profiling":
        st.subheader("YData Profiling Report")
        profile = ProfileReport(df, explorative=True)
        st_profile_report(profile)

    elif report_type == "Custom Report":
        st.subheader("Custom Report - Chart Customization")

        st.sidebar.header("Chart Options")

        selected_columns = st.sidebar.multiselect(
            "Select columns for the charts",
            df.columns,
            default=df.columns[:2],
        )

        chart_type = st.sidebar.selectbox(
            "Select a chart type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"],
        )

        if selected_columns:
            for column in selected_columns:
                st.write(f"### {chart_type} for {column}")
                
                if chart_type == "Bar Chart":
                    fig = px.bar(df, x=df.index, y=column, title=f"Bar Chart - {column}")
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=df.index, y=column, title=f"Line Chart - {column}")
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=df.index, y=column, title=f"Scatter Plot - {column}")
                elif chart_type == "Pie Chart":
                    fig = px.pie(df, names=column, title=f"Pie Chart - {column}")
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select at least one column to generate charts.")
else:
    st.info("Please upload a CSV file to generate a report.")

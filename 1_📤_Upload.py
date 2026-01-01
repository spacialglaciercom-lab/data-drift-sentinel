"""
Upload Page - Upload baseline and current datasets
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Upload - Data Drift Sentinel",
    page_icon="📤"
)

st.title("📤 Upload Datasets")

st.markdown("""
Upload your baseline (reference) and current (production) datasets to begin drift analysis.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Baseline Dataset")
    baseline_file = st.file_uploader(
        "Upload baseline dataset",
        type=['csv', 'xlsx', 'parquet'],
        key="baseline"
    )
    
    if baseline_file is not None:
        try:
            if baseline_file.name.endswith('.csv'):
                df_baseline = pd.read_csv(baseline_file)
            elif baseline_file.name.endswith('.xlsx'):
                df_baseline = pd.read_excel(baseline_file)
            elif baseline_file.name.endswith('.parquet'):
                df_baseline = pd.read_parquet(baseline_file)
            
            st.session_state['baseline_df'] = df_baseline
            st.success(f"✅ Baseline dataset loaded: {df_baseline.shape[0]} rows, {df_baseline.shape[1]} columns")
            st.dataframe(df_baseline.head(), use_container_width=True)
        except Exception as e:
            st.error(f"Error loading file: {e}")

with col2:
    st.subheader("Current Dataset")
    current_file = st.file_uploader(
        "Upload current dataset",
        type=['csv', 'xlsx', 'parquet'],
        key="current"
    )
    
    if current_file is not None:
        try:
            if current_file.name.endswith('.csv'):
                df_current = pd.read_csv(current_file)
            elif current_file.name.endswith('.xlsx'):
                df_current = pd.read_excel(current_file)
            elif current_file.name.endswith('.parquet'):
                df_current = pd.read_parquet(current_file)
            
            st.session_state['current_df'] = df_current
            st.success(f"✅ Current dataset loaded: {df_current.shape[0]} rows, {df_current.shape[1]} columns")
            st.dataframe(df_current.head(), use_container_width=True)
        except Exception as e:
            st.error(f"Error loading file: {e}")

# Show status
if 'baseline_df' in st.session_state and 'current_df' in st.session_state:
    st.success("✅ Both datasets are loaded and ready for analysis!")
    st.info("👉 Navigate to **Schema & Quality** to view schema differences, or go to **Drift Report** to compute drift metrics.")

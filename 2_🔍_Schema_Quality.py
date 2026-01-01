"""
Schema & Quality Page - View schema differences and configure drift detection
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Schema & Quality - Data Drift Sentinel",
    page_icon="🔍"
)

st.title("🔍 Schema & Quality")

if 'baseline_df' not in st.session_state or 'current_df' not in st.session_state:
    st.warning("⚠️ Please upload datasets in the **Upload** page first.")
    st.info("👉 Go to the **Upload** page to load your baseline and current datasets.")
else:
    baseline_df = st.session_state['baseline_df']
    current_df = st.session_state['current_df']
    
    # Schema Comparison
    st.subheader("📋 Schema Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Baseline Schema**")
        baseline_info = pd.DataFrame({
            'Column': baseline_df.columns,
            'Type': [str(dtype) for dtype in baseline_df.dtypes],
            'Non-Null Count': baseline_df.count().values,
            'Null Count': baseline_df.isnull().sum().values
        })
        st.dataframe(baseline_info, use_container_width=True, hide_index=True)
    
    with col2:
        st.write("**Current Schema**")
        current_info = pd.DataFrame({
            'Column': current_df.columns,
            'Type': [str(dtype) for dtype in current_df.dtypes],
            'Non-Null Count': current_df.count().values,
            'Null Count': current_df.isnull().sum().values
        })
        st.dataframe(current_info, use_container_width=True, hide_index=True)
    
    # Schema Differences
    st.subheader("🔍 Schema Differences")
    
    baseline_cols = set(baseline_df.columns)
    current_cols = set(current_df.columns)
    
    added_cols = current_cols - baseline_cols
    removed_cols = baseline_cols - current_cols
    common_cols = baseline_cols & current_cols
    
    if added_cols:
        st.warning(f"⚠️ **Added Columns ({len(added_cols)}):** {', '.join(added_cols)}")
    if removed_cols:
        st.error(f"❌ **Removed Columns ({len(removed_cols)}):** {', '.join(removed_cols)}")
    if not added_cols and not removed_cols:
        st.success(f"✅ **No column changes detected.** All {len(common_cols)} columns are present in both datasets.")
    
    # Type changes
    type_changes = []
    for col in common_cols:
        if str(baseline_df[col].dtype) != str(current_df[col].dtype):
            type_changes.append({
                'Column': col,
                'Baseline Type': str(baseline_df[col].dtype),
                'Current Type': str(current_df[col].dtype)
            })
    
    if type_changes:
        st.warning(f"⚠️ **Type Changes ({len(type_changes)}):**")
        st.dataframe(pd.DataFrame(type_changes), use_container_width=True, hide_index=True)
    else:
        st.success("✅ **No type changes detected.**")
    
    # Data Quality Metrics
    st.subheader("📊 Data Quality Metrics")
    
    quality_metrics = pd.DataFrame({
        'Metric': ['Total Rows', 'Total Columns', 'Missing Values', 'Missing %'],
        'Baseline': [
            len(baseline_df),
            len(baseline_df.columns),
            baseline_df.isnull().sum().sum(),
            f"{baseline_df.isnull().sum().sum() / (len(baseline_df) * len(baseline_df.columns)) * 100:.2f}%"
        ],
        'Current': [
            len(current_df),
            len(current_df.columns),
            current_df.isnull().sum().sum(),
            f"{current_df.isnull().sum().sum() / (len(current_df) * len(current_df.columns)) * 100:.2f}%"
        ]
    })
    st.dataframe(quality_metrics, use_container_width=True, hide_index=True)

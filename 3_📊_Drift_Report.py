"""
Drift Report Page - Compute and visualize drift with interactive charts
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Drift Report - Data Drift Sentinel",
    page_icon="📊"
)

st.title("📊 Drift Report")

if 'baseline_df' not in st.session_state or 'current_df' not in st.session_state:
    st.warning("⚠️ Please upload datasets in the **Upload** page first.")
    st.info("👉 Go to the **Upload** page to load your baseline and current datasets.")
else:
    baseline_df = st.session_state['baseline_df']
    current_df = st.session_state['current_df']
    
    st.info("""
    **Note:** This is a placeholder page. To compute actual drift metrics, you'll need to:
    1. Import the `compute_drift` function from `src.compute_drift`
    2. Call it with your baseline and current dataframes
    3. Display the results
    """)
    
    # Placeholder for drift computation
    if st.button("🔄 Compute Drift Report", type="primary"):
        try:
            # Try to import and use the actual drift computation
            from src.compute_drift import compute_drift
            
            with st.spinner("Computing drift metrics..."):
                report = compute_drift(baseline_df, current_df)
                st.session_state['drift_report'] = report
                st.success("✅ Drift report computed successfully!")
                
                # Display results
                st.subheader("📈 Dataset Overview")
                st.json({
                    "baseline_rows": report.dataset_metadata.baseline_rows,
                    "current_rows": report.dataset_metadata.current_rows,
                    "baseline_columns": report.dataset_metadata.baseline_columns,
                    "current_columns": report.dataset_metadata.current_columns,
                    "common_columns": len(report.dataset_metadata.common_columns)
                })
                
                # Top changed columns
                if report.top_changed_columns:
                    st.subheader("🔴 Top Changed Columns")
                    top_changed = pd.DataFrame([
                        {
                            "Column": col.column_name,
                            "PSI": col.psi,
                            "Severity": col.severity
                        }
                        for col in report.top_changed_columns[:10]
                    ])
                    st.dataframe(top_changed, use_container_width=True, hide_index=True)
        except ImportError:
            st.error("""
            **Error:** Could not import `compute_drift` from `src.compute_drift`.
            
            Please ensure:
            1. The `src` directory exists with the required modules
            2. All dependencies are installed: `pip install -r requirements.txt`
            """)
        except Exception as e:
            st.error(f"Error computing drift: {e}")
            st.exception(e)
    
    # Show stored report if available
    if 'drift_report' in st.session_state:
        st.success("✅ Drift report is available. Use the **Export** page to download results.")

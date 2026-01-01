"""
Export Page - Export results as JSON or CSV
"""

import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="Export - Data Drift Sentinel",
    page_icon="💾"
)

st.title("💾 Export Results")

if 'drift_report' not in st.session_state:
    st.warning("⚠️ No drift report available. Please compute a drift report first.")
    st.info("👉 Go to the **Drift Report** page to compute drift metrics.")
else:
    report = st.session_state['drift_report']
    
    st.subheader("📥 Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export as JSON
        try:
            json_str = report.model_dump_json(indent=2)
            st.download_button(
                label="📄 Download JSON Report",
                data=json_str,
                file_name="drift_report.json",
                mime="application/json",
                type="primary"
            )
        except Exception as e:
            st.error(f"Error generating JSON: {e}")
    
    with col2:
        # Export as CSV (top changed columns)
        try:
            if report.top_changed_columns:
                df_export = pd.DataFrame([
                    {
                        "column_name": col.column_name,
                        "psi": col.psi,
                        "severity": col.severity,
                        "missing_delta": col.missing_delta if hasattr(col, 'missing_delta') else None
                    }
                    for col in report.top_changed_columns
                ])
                csv = df_export.to_csv(index=False)
                st.download_button(
                    label="📊 Download CSV (Top Changed Columns)",
                    data=csv,
                    file_name="top_changed_columns.csv",
                    mime="text/csv"
                )
            else:
                st.info("No changed columns to export.")
        except Exception as e:
            st.error(f"Error generating CSV: {e}")
    
    # Preview
    st.subheader("👀 Preview")
    
    tab1, tab2 = st.tabs(["JSON Preview", "Summary"])
    
    with tab1:
        try:
            st.json(json.loads(json_str))
        except:
            st.code(json_str, language="json")
    
    with tab2:
        st.write("**Dataset Metadata:**")
        st.json({
            "baseline_rows": report.dataset_metadata.baseline_rows,
            "current_rows": report.dataset_metadata.current_rows,
            "baseline_columns": report.dataset_metadata.baseline_columns,
            "current_columns": report.dataset_metadata.current_columns
        })
        
        if report.top_changed_columns:
            st.write("**Top 5 Changed Columns:**")
            top5 = pd.DataFrame([
                {
                    "Column": col.column_name,
                    "PSI": f"{col.psi:.4f}",
                    "Severity": col.severity
                }
                for col in report.top_changed_columns[:5]
            ])
            st.dataframe(top5, use_container_width=True, hide_index=True)

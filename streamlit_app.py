"""
Streamlit App Entry Point for Data Drift Sentinel
This file serves as the main entry point for Streamlit Cloud deployment.
"""

import streamlit as st
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configure the page
st.set_page_config(
    page_title="Data Drift Sentinel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main welcome page
st.title("📊 Data Drift Sentinel")
st.markdown("""
A comprehensive application for monitoring data drift between baseline and current datasets 
using Population Stability Index (PSI) and other statistical measures.
""")

st.info("""
👈 **Use the sidebar to navigate between pages:**
- **📤 Upload** - Upload baseline and current datasets
- **🔍 Schema & Quality** - View schema differences and configure drift detection
- **📊 Drift Report** - Compute and visualize drift with interactive charts
- **🤖 LLM Summary** - Generate AI-powered summaries (optional)
- **💾 Export** - Export results as JSON or CSV
""")

# Check if pages directory exists
pages_dir = os.path.join(project_root, "pages")
if not os.path.exists(pages_dir):
    st.warning("⚠️ Pages directory not found. The app may not function correctly.")
    st.code("""
    Expected structure:
    ├── streamlit_app.py (this file)
    ├── pages/
    │   ├── 1_📤_Upload.py
    │   ├── 2_🔍_Schema_Quality.py
    │   ├── 3_📊_Drift_Report.py
    │   ├── 4_🤖_LLM_Summary.py
    │   └── 5_💾_Export.py
    """, language="text")

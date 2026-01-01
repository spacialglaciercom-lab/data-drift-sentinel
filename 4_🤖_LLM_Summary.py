"""
LLM Summary Page - Generate AI-powered summaries (optional)
"""

import streamlit as st
import os

st.set_page_config(
    page_title="LLM Summary - Data Drift Sentinel",
    page_icon="🤖"
)

st.title("🤖 LLM Summary")

# Check for API key
api_key = None
if 'LLM_API_KEY' in os.environ:
    api_key = os.environ['LLM_API_KEY']
elif 'OPENAI_API_KEY' in os.environ:
    api_key = os.environ['OPENAI_API_KEY']
else:
    # Try to get from Streamlit secrets
    try:
        api_key = st.secrets.get("LLM_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    except:
        pass

if not api_key:
    st.warning("""
    ⚠️ **LLM Summary is disabled** — API key not found.
    
    To enable LLM summaries, add your API key using one of these methods:
    
    1. **Streamlit Secrets** (Recommended):
       - Create `.streamlit/secrets.toml`
       - Add: `LLM_API_KEY = "your-api-key-here"`
    
    2. **Environment Variable**:
       - Set `LLM_API_KEY` or `OPENAI_API_KEY` environment variable
    """)
else:
    st.success("✅ API key detected. LLM summary features are enabled.")
    
    if 'drift_report' not in st.session_state:
        st.warning("⚠️ Please compute a drift report first in the **Drift Report** page.")
        st.info("👉 Go to the **Drift Report** page to compute drift metrics.")
    else:
        st.info("""
        **Note:** This is a placeholder page. To generate actual LLM summaries, you'll need to:
        1. Import the LLM summary function from `src.llm_summary`
        2. Pass the drift report to generate a summary
        3. Display the generated summary
        """)
        
        if st.button("🤖 Generate LLM Summary", type="primary"):
            try:
                from src.llm_summary import generate_summary
                
                with st.spinner("Generating AI summary..."):
                    summary = generate_summary(st.session_state['drift_report'], api_key)
                    st.session_state['llm_summary'] = summary
                    st.success("✅ Summary generated successfully!")
                    
                    st.subheader("📝 Executive Summary")
                    st.markdown(summary)
            except ImportError:
                st.error("""
                **Error:** Could not import `generate_summary` from `src.llm_summary`.
                
                Please ensure the `src/llm_summary.py` module exists and is properly configured.
                """)
            except Exception as e:
                st.error(f"Error generating summary: {e}")
                st.exception(e)
        
        # Show stored summary if available
        if 'llm_summary' in st.session_state:
            st.subheader("📝 Generated Summary")
            st.markdown(st.session_state['llm_summary'])

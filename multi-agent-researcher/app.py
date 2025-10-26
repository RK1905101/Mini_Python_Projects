# streamlit_app.py

import streamlit as st
from ai import run_research_graph # Import the main function from your backend

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Research Paper Generator",
    page_icon="🔬",
    layout="wide"
)

# --- App Header ---
st.title("🔬 AI-Powered Research Paper Generator")
st.markdown("""
Welcome! This application uses a powerful team of AI agents, orchestrated by LangGraph, to automate the entire research
process. Just provide a detailed research topic, and the AI will conduct a literature review, run a dynamic simulation,
perform a statistical analysis, and write a professional, arXiv-style report.
""")

# --- Main Application Logic ---
# Use a form for a cleaner user experience
with st.form(key='research_form'):
    st.subheader("Enter Your Research Topic")
    topic = st.text_area(
        "Provide a detailed research topic below. The more specific, the better the report!",
        height=150,
        placeholder="e.g., 'Investigate the efficacy of using Graph Neural Networks (GNNs) for molecular property prediction compared to traditional machine learning models like Random Forests.'"
    )
    submit_button = st.form_submit_button(label='🚀 Generate Report')

# --- Execution and Display ---
if submit_button:
    if not topic.strip():
        st.error("Please enter a research topic to begin.")
    else:
        # Use st.session_state to store the report content
        if 'report_content' in st.session_state:
            del st.session_state['report_content']

        # Show a spinner while the backend is working
        with st.spinner('The AI Research Crew is on the job... This may take a few minutes.'):
            try:
                # Call the main function from your ai_backend.py file
                report_content = run_research_graph(topic)
                
                # Store the report in the session state to persist it across reruns
                st.session_state['report_content'] = report_content
                
                st.success("Research complete! The final report is ready below.")
            except Exception as e:
                st.error(f"A critical error occurred: {e}")

# --- Display Results ---
# Only show this section if a report has been generated and stored in the session state
if 'report_content' in st.session_state:
    st.markdown("---")
    st.header("Generated Research Report")
    
    report = st.session_state['report_content']
    
    # Display the final report content
    st.markdown(report)

    # Provide a download button for the report
    st.download_button(
        label="⬇️ Download Report as Markdown",
        data=report,
        file_name=f"research_report_{topic.replace(' ', '_')[:20]}.md",
        mime="text/markdown",
    )
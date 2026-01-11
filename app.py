"""
Career Referee - Main Streamlit Application
A neutral career comparison tool that helps users make informed decisions.
"""

import streamlit as st
from ui import render_input_page, render_comparison_page, apply_custom_styling
from referee_agent import run_referee


def main():
    """Main application entry point with page routing."""
    st.set_page_config(
        page_title="Career Referee",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom styling
    apply_custom_styling()
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "input"
    
    # Main header
    st.title("⚖️ Career Referee")
    st.markdown("*Compare careers objectively. Decide confidently.*")
    
    # Page routing
    if st.session_state.page == "input":
        render_input_page_handler()
    elif st.session_state.page == "comparison":
        render_comparison_page_handler()


def render_input_page_handler():
    """Handles the input page logic and navigation."""
    result = render_input_page()
    
    if result is not None:
        user_name, career_a, career_b = result
        
        # Store inputs in session state
        st.session_state.user_name = user_name
        st.session_state.career_a = career_a
        st.session_state.career_b = career_b
        
        # Show loading message
        with st.spinner("Analyzing careers... This may take a moment."):
            # Get comparison data from AI
            comparison_data = run_referee(career_a, career_b)
            st.session_state.comparison_data = comparison_data
        
        # Navigate to comparison page
        st.session_state.page = "comparison"
        st.rerun()


def render_comparison_page_handler():
    """Handles the comparison page logic."""
    # Check if we have all required data
    required_keys = ["user_name", "career_a", "career_b", "comparison_data"]
    if not all(key in st.session_state for key in required_keys):
        # If missing data, go back to input page
        st.session_state.page = "input"
        st.rerun()
        return
    
    # Render comparison page
    render_comparison_page(
        user_name=st.session_state.user_name,
        career_a_name=st.session_state.career_a,
        career_b_name=st.session_state.career_b,
        comparison_data=st.session_state.comparison_data
    )


if __name__ == "__main__":
    main()
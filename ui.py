"""
UI Components and Styling Helpers
Reusable UI components for the Career Referee application.
"""

import streamlit as st
from typing import Dict, List, Optional, Tuple
from models import validate_career_input, validate_user_name


def render_input_page() -> Optional[Tuple[str, str, str]]:
    """
    Renders the input page with form fields for user name and career options.
    
    Returns:
        Tuple of (user_name, career_a, career_b) if form is submitted with valid data,
        None otherwise
    """
    st.markdown("### Tell us about yourself and the careers you're considering")
    st.markdown("We'll provide you with an objective comparison to help guide your decision.")
    
    # Create input form
    with st.form("career_input_form", clear_on_submit=False):
        # User name input
        user_name = st.text_input(
            "Your Name",
            placeholder="Enter your name",
            help="This will personalize your comparison results"
        )
        
        # Career options
        col1, col2 = st.columns(2)
        
        with col1:
            career_a = st.text_input(
                "First Career Option",
                placeholder="e.g., Software Engineer",
                help="Enter the first career you're considering"
            )
        
        with col2:
            career_b = st.text_input(
                "Second Career Option", 
                placeholder="e.g., Data Scientist",
                help="Enter the second career you're considering"
            )
        
        # Submit button
        submitted = st.form_submit_button(
            "Compare Careers",
            type="primary",
            use_container_width=True
        )
        
        # Validation and submission handling
        if submitted:
            # Validate inputs
            errors = []
            
            if not validate_user_name(user_name):
                errors.append("Please enter a valid name")
            
            if not validate_career_input(career_a):
                errors.append("Please enter a valid first career option")
                
            if not validate_career_input(career_b):
                errors.append("Please enter a valid second career option")
            
            if career_a.strip().lower() == career_b.strip().lower():
                errors.append("Please enter two different career options")
            
            # Display errors or return valid data
            if errors:
                for error in errors:
                    st.error(error)
                return None
            else:
                # Return validated inputs
                return (user_name.strip(), career_a.strip(), career_b.strip())
    
    return None


def render_career_card(career_name: str, career_data: Dict) -> None:
    """
    Renders a styled career information card.
    
    Args:
        career_name: Name of the career
        career_data: Dictionary containing career information
    """
    with st.container():
        # Career title
        st.markdown(f"### {career_name}")
        
        # Overview section
        st.markdown("**Overview**")
        st.write(career_data.get("overview", "No overview available"))
        
        # Skills section
        st.markdown("**Required Skills**")
        st.write(career_data.get("skills", "No skills information available"))
        
        # Salary and timing info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Salary Range**")
            salary = career_data.get("salary", "unknown").title()
            st.write(f"💰 {salary}")
        
        with col2:
            st.markdown("**Time to Enter**")
            time_to_enter = career_data.get("time_to_enter", "Unknown")
            st.write(f"⏱️ {time_to_enter}")
        
        # Pros and cons
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Advantages**")
            pros = career_data.get("pros", [])
            for pro in pros:
                st.write(f"✅ {pro}")
        
        with col2:
            st.markdown("**Challenges**")
            cons = career_data.get("cons", [])
            for con in cons:
                st.write(f"⚠️ {con}")


def render_comparison_page(user_name: str, career_a_name: str, career_b_name: str, comparison_data: Dict) -> None:
    """
    Renders the comparison page with side-by-side career comparison.
    
    Args:
        user_name: User's name for personalization
        career_a_name: Name of first career
        career_b_name: Name of second career
        comparison_data: ComparisonResult data
    """
    # Personalized header
    st.markdown(f"## Career Comparison for {user_name}")
    st.markdown(f"Comparing **{career_a_name}** vs **{career_b_name}**")
    
    # Side-by-side career comparison
    col1, col2 = st.columns(2)
    
    with col1:
        render_career_card(career_a_name, comparison_data.career_a.__dict__)
    
    with col2:
        render_career_card(career_b_name, comparison_data.career_b.__dict__)
    
    # Decision guide section
    render_decision_guide(comparison_data.decision_guide)
    
    # Back button
    if st.button("Compare Different Careers", type="secondary"):
        # Reset session state to go back to input page
        st.session_state.page = "input"
        st.session_state.pop("user_name", None)
        st.session_state.pop("career_a", None)
        st.session_state.pop("career_b", None)
        st.session_state.pop("comparison_data", None)
        st.rerun()


def render_decision_guide(guide_items: List[str]) -> None:
    """
    Renders the decision guidance section.
    
    Args:
        guide_items: List of guidance statements
    """
    st.markdown("---")
    st.markdown("## 🎯 Decision Guide")
    st.markdown("*Choose the career that aligns with your values and priorities*")
    
    # Create styled decision guide container
    with st.container():
        for i, item in enumerate(guide_items):
            # Add some styling to make it more visually appealing
            if i == 0:
                st.markdown(f"### 🅰️ {item}")
            elif i == 1:
                st.markdown(f"### 🅱️ {item}")
            else:
                st.markdown(f"### ➡️ {item}")
            
            # Add some spacing
            if i < len(guide_items) - 1:
                st.markdown("")


def apply_custom_styling() -> None:
    """Injects custom CSS for modern UI styling."""
    # Load CSS from styles.css file
    try:
        with open("styles.css", "r") as f:
            css_content = f.read()
        
        st.markdown(f"""
        <style>
        {css_content}
        
        /* Additional Streamlit-specific styling */
        .stForm {{
            background: var(--card-background);
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 24px;
        }}
        
        .stTextInput > div > div > input {{
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(46, 134, 171, 0.2);
        }}
        
        /* Career card styling */
        .element-container {{
            margin-bottom: 16px;
        }}
        
        /* Decision guide styling */
        .decision-guide-container {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            padding: 20px;
            margin-top: 24px;
        }}
        </style>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        # Fallback CSS if styles.css is not found
        st.markdown("""
        <style>
        .stApp {
            background-color: #F8F9FA;
        }
        
        .stForm {
            background: white;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 24px;
        }
        
        .stButton > button {
            background-color: #2E86AB;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        
        .stButton > button:hover {
            background-color: #A23B72;
            border: none;
        }
        </style>
        """, unsafe_allow_html=True)
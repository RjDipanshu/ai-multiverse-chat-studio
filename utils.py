import streamlit as st
from pathlib import Path


def load_style(path: str) -> None:
    try:
        css = Path(path).read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Style file not found: {path}")


def render_sidebar(personalities, languages):
    st.sidebar.markdown("<h2 class='sidebar-title'>⚙️ Studio Dashboard</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("Configure the AI Multiverse settings below.")
    
    selected_name = st.sidebar.selectbox(
        "Choose Persona", [item["name"] for item in personalities]
    )
    selected_language = st.sidebar.selectbox("Choose Language", languages)
    
    selected_personality = next(
        item for item in personalities if item["name"] == selected_name
    )
    
    # Render a beautiful styled box for description
    st.sidebar.markdown(
        f"<div class='persona-card'>"
        f"<h4>{selected_personality['name']}</h4>"
        f"<p>{selected_personality['description']}</p>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    return (
        selected_personality["name"],
        selected_personality["description"],
        selected_personality["behavior"],
        selected_language
    )

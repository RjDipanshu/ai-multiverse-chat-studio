import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from personalities import PERSONALITIES
from prompts import LANGUAGES, build_personality_prompt
from utils import load_style, render_sidebar

# Load environment variables from .env
load_dotenv()

st.set_page_config(
    page_title="AI Multiverse Chat Studio",
    page_icon="🤖",
    layout="centered",
)

# Load premium CSS styling
load_style("style.css")

# Main Title (using custom CSS gradient title)
st.markdown("<h1 class='app-title'>🤖 AI Multiverse Chat Studio</h1>", unsafe_allow_html=True)
st.write("Unleash the multiverse of personas. Configure your settings, enter a query, and explore tailored responses.")

# Retrieve the API key
api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is missing or set to placeholder
is_key_missing = (not api_key) or (api_key.strip() in ("", "your_gemini_api_key_here"))

if is_key_missing:
    # Render a premium, styled warning container with instructions
    st.markdown(
        "<div class='setup-container'>"
        "<div class='setup-title'>⚠️ Workspace Action Required: Configure API Key</div>"
        "<p>To start using the Multiverse Chat Studio, you need to configure your Google Gemini API Key. Please complete the following steps:</p>"
        "<ol>"
        "<li>Open the <b>.env</b> file located in your project root folder:</li>"
        "<code>c:\\Users\\dipan\\OneDrive\\Desktop\\ai-multiverse-chat-studio\\.env</code>"
        "<li style='margin-top: 10px;'>Replace <code>your_gemini_api_key_here</code> with your actual key from "
        "<a href='https://aistudio.google.com/' target='_blank' style='color:#38bdf8; font-weight:600;'>Google AI Studio</a>.</li>"
        "<li style='margin-top: 10px;'>Save the file. Streamlit will automatically detect the changes and reload the studio dashboard.</li>"
        "</ol>"
        "</div>",
        unsafe_allow_html=True
    )
    
    st.info("💡 A template `.env` file has been created in your project workspace for your convenience.")

else:
    # Render sidebar and extract selected persona configurations
    personality_name, personality_description, personality_behavior, language = render_sidebar(
        PERSONALITIES, LANGUAGES
    )

    with st.form("chat_form"):
        st.subheader("Type Message")
        user_message = st.text_area("Your message", placeholder="Ask anything to the selected persona...", height=140)
        send_button = st.form_submit_button("SEND TO THE MULTIVERSE")

    if send_button:
        if not user_message.strip():
            st.warning("Please type a message before sending.")
        else:
            prompt_preview = build_personality_prompt(
                personality_name, personality_description, personality_behavior, language, user_message
            )
            
            # Show the generated prompt inside an expander for debugging/transparency
            with st.expander("🛠️ View Built Prompt Profile", expanded=False):
                st.code(prompt_preview)
                
            with st.spinner("🌌 Channeling the Multiverse..."):
                try:
                    # Initialize the Gemini client
                    client = genai.Client(api_key=api_key)
                    
                    # Generate the response
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_preview,
                    )
                    
                    st.markdown("### 🌌 Response")
                    st.markdown(response.text)
                    st.success("Response generated successfully!")
                    
                except errors.APIError as e:
                    st.error(f"Gemini API Error: {e.message}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")

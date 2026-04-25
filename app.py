import streamlit as st
from supabase import create_client

# --- PASTE YOUR KEYS HERE ---
url = "https://tlaudcreihxtdmzgnxul.supabase.co"
key = "sb_publishable_Q19svQb0Xa0B0IY61_iCsA_GGYZbhQA"
supabase = create_client(url, key)

# --- THE REST OF THE CODE ---
st.set_page_config(page_title="Unsent: The Void", page_icon="🌙", layout="centered")

# Custom CSS for the Dark Immersive look
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .stButton>button { width: 100%; border-radius: 20px; }
    .feed-card { background: #161b22; border-radius: 20px; padding: 25px; margin-bottom: 20px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State for navigation
if 'page' not in st.session_state:
    st.session_state.page = "onboarding"

# --- SCREEN: ONBOARDING ---
if st.session_state.page == "onboarding":
    st.title("🌙 Who are you today?")
    st.write("Select your shadow to enter the void.")
    if st.button("💔 Heartbroken"):
        st.session_state.mood = "Heartbroken"
        st.session_state.page = "write"
        st.rerun()
    if st.button("🤫 Silent Lover"):
        st.session_state.mood = "Silent Lover"
        st.session_state.page = "write"
        st.rerun()

# --- SCREEN: WRITE ---
elif st.session_state.page == "write":
    st.title("Write what you never said...")
    content = st.text_area("", placeholder="Type your truth here...", height=200)
    if st.button("Release into the Void →"):
        if content:
            supabase.table("messages").insert({"content": content, "category": st.session_state.mood}).execute()
            st.success("Released.")
            st.session_state.page = "feed"
            st.rerun()
import streamlit as st
from supabase import create_client
import time
from datetime import datetime

# --- 1. SETUP & CORE ---
URL = "https://tlaudcreihxtdmzgnxul.supabase.co"
KEY = "sb_publishable_Q19svQb0Xa0B0IY61_iCsA_GGYZbhQA"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="THE VOID", page_icon="🌙", layout="wide")

# Custom CSS for Premium Dark Feel
st.markdown("""
    <style>
    .stApp { background: #050505; color: #eee; }
    .main-card { background: #111; border: 1px solid #222; padding: 25px; border-radius: 20px; margin-bottom: 20px; }
    .target-card { border-left: 4px solid #00ffcc; background: #0a0a0a; padding: 15px; margin-top: 10px; }
    .stButton>button { border-radius: 50px; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# Navigation System
if 'screen' not in st.session_state:
    st.session_state.screen = "discovery"

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("VOID OS")
    if st.button("🌌 Global Feed"): st.session_state.screen = "discovery"
    if st.button("📝 Release Words"): st.session_state.screen = "write"
    if st.button("🎯 My Targets"): st.session_state.screen = "targets"
    st.markdown("---")
    st.caption("v2.0 Advanced Build")

# --- 3. PAGE: GLOBAL FEED (Discovery) ---
if st.session_state.screen == "discovery":
    st.title("Echoes from the Void")
    st.write("What others are whispering right now...")
    
    # Filter by Mood
    mood_filter = st.tabs(["All", "Heartbroken", "Silent Lover", "Dreamer", "Overthinker"])
    
    # Fetch data (Only public ones)
    res = supabase.table("messages").select("*").eq("is_private", False).order("created_at", desc=True).limit(15).execute()
    
    for msg in res.data:
        with st.container():
            st.markdown(f"""
                <div class="main-card">
                    <small style="color: #666;">{msg['category'].upper()}</small>
                    <p style="font-size: 1.3rem; margin: 15px 0;">{msg['content']}</p>
                </div>
            """, unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1,1,4])
            with c1: 
                if st.button(f"❤️ {msg.get('likes', 0)}", key=f"lk_{msg['id']}"):
                    supabase.table("messages").update({"likes": msg.get('likes', 0) + 1}).eq("id", msg['id']).execute()
                    st.rerun()
            with c2: st.button("💬 Reply", key=f"rp_{msg['id']}")

# --- 4. PAGE: WRITE (Release) ---
elif st.session_state.screen == "write":
    st.title("Release into the Void")
    
    col_a, col_b = st.columns(2)
    with col_a:
        mood = st.selectbox("Your Current Shadow", ["Dreamer", "Heartbroken", "Silent Lover", "Overthinker", "Secret Admirer", "The Griever"])
    with col_b:
        to_who = st.text_input("To:", placeholder="A name or 'Self'")

    text = st.text_area("Your truth...", height=300)
    
    is_private = st.toggle("Private (Only for my eyes)")
    
    if st.button("SEND TO THE UNIVERSE"):
        if text:
            supabase.table("messages").insert({
                "content": text, 
                "category": mood, 
                "recipient": to_who,
                "is_private": is_private
            }).execute()
            st.success("Released.")
            time.sleep(1)
            st.session_state.screen = "discovery"
            st.rerun()

# --- 5. PAGE: TARGETS (The Reminder System) ---
elif st.session_state.screen == "targets":
    st.title("🎯 Personal Targets")
    st.write("Set goals that haunt you until they are done.")
    
    new_target = st.text_input("What is your mission today?")
    if st.button("Set Target"):
        if new_target:
            supabase.table("messages").insert({
                "content": new_target,
                "category": "Target",
                "is_private": True,
                "is_done": False
            }).execute()
            st.rerun()

    st.markdown("---")
    
    # Logic to show pending targets
    targets = supabase.table("messages").select("*").eq("category", "Target").eq("is_done", False).execute()
    
    if targets.data:
        st.warning(f"You have {len(targets.data)} active targets. They will reappear every hour.")
        for t in targets.data:
            st.markdown(f"""<div class="target-card">{t['content']}</div>""", unsafe_allow_html=True)
            if st.button("Mark as Done", key=f"done_{t['id']}"):
                supabase.table("messages").update({"is_done": True}).eq("id", t['id']).execute()
                st.success("Target cleared.")
                st.rerun()
import streamlit as st
from supabase import create_client

# 1. Setup
url = "https://tlaudcreihxtdmzgnxul.supabase.co"
key = "sb_publishable_Q19svQb0Xa0B0IY61_iCsA_GGYZbhQA"
supabase = create_client(url, key)

st.set_page_config(page_title="Unsent", page_icon="☁️", layout="centered")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.2rem !important; }
    .stInfo { background-color: #f8f9fa; border: none; border-radius: 15px; padding: 20px; color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("☁️ Unsent")
st.caption("Release the words you never said.")

menu = ["Explore the Feed", "Write an Unsent Letter"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Write an Unsent Letter":
    st.write("### To whom are you writing?")
    cat = st.selectbox("Category", ["A Lost Love", "A Friend", "My Past Self", "Someone I Miss", "General"])
    
    content = st.text_area("", placeholder="Start typing...", height=300)
    
    if st.button("Release into the Void"):
        if content:
            supabase.table("messages").insert({"content": content, "category": cat}).execute()
            st.toast("Message sent.")
            st.balloons()
        else:
            st.error("The void requires words.")

else:
    st.write("### Recent Whispers")
    response = supabase.table("messages").select("*").order("created_at", desc=True).execute()
    
    for item in response.data:
        with st.container():
            st.markdown(f"**{item['category']}**")
            st.info(item['content'])
            st.caption(f"Released on {item['created_at'][:10]}")
            st.write("") # Adds space
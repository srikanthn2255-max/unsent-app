import streamlit as st
from supabase import create_client

# 1. Setup (Keep your same keys here!)
url = "https://tlaudcreihxtdmzgnxul.supabase.co"
key = "sb_publishable_Q19svQb0Xa0B0IY61_iCsA_GGYZbhQA"
supabase = create_client(url, key)

st.set_page_config(page_title="Unsent", page_icon="☁️", layout="centered")

# --- CUSTOM BEAUTIFUL DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville&family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="st-at"] { font-family: 'Inter', sans-serif; }
    h1 { font-family: 'Libre Baskerville', serif; color: #1e1e1e; font-size: 3rem !important; }
    
    .stTextArea textarea { 
        border-radius: 15px; 
        border: 1px solid #eee; 
        padding: 20px;
        font-size: 1.1rem;
    }
    
    .message-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 25px;
    }
    
    .category-tag {
        color: #888;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    .main-text {
        font-size: 1.25rem;
        line-height: 1.6;
        color: #2c2c2c;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("☁️ Unsent")
st.write("Words held back, finally released.")

menu = ["Explore Feed", "Write a Letter"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Write a Letter":
    st.write("### To whom are you writing?")
    cat = st.selectbox("", ["A Lost Love", "A Friend", "My Past Self", "Someone I Miss", "The Universe"])
    
    content = st.text_area("", placeholder="What did you never say?...", height=250)
    
    if st.button("Release into the Void"):
        if content:
            supabase.table("messages").insert({"content": content, "category": cat}).execute()
            st.toast("Released.")
            st.balloons()
        else:
            st.error("Please write something.")

else:
    response = supabase.table("messages").select("*").order("created_at", desc=True).execute()
    
    for item in response.data:
        # This creates the "Card" look
        st.markdown(f"""
            <div class="message-card">
                <div class="category-tag">{item['category']}</div>
                <div class="main-text">{item['content']}</div>
                <div style="color: #ccc; font-size: 0.7rem; margin-top: 15px;">
                    {item['created_at'][:10]}
                </div>
            </div>
        """, unsafe_allow_html=True)
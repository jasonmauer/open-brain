"""Open Brain Dashboard - Enhanced Design"""

import streamlit as st
import requests
import pandas as pd
import yaml
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIG & STYLING
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🧠 Open Brain",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    
    /* Cards */
    .card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #fff !important;
        font-weight: 600 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(0,0,0,0.3) !important;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        border: none;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        color: white;
        font-weight: 600;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    /* Search */
    input[type="text"] {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# API CLIENT
# ═══════════════════════════════════════════════════════════════
API_BASE = "http://localhost:8000"

def get_stats():
    try:
        return requests.get(f"{API_BASE}/stats", timeout=5).json()
    except:
        return {"total": 0, "by_source": {}, "top_tags": {}, "this_week": 0}

def search_memories(query, limit=20):
    try:
        return requests.get(f"{API_BASE}/memories/search", params={"query": query, "limit": limit}, timeout=10).json()
    except:
        return []

def create_memory(content, source="dashboard", tags=None):
    try:
        return requests.post(f"{API_BASE}/memories", json={"content": content, "source": source, "tags": tags or []}, timeout=10).json()
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 3rem; margin: 0;">🧠</h1>
        <h2 style="margin: 0; background: linear-gradient(90deg, #00d4ff, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Open Brain</h2>
        <p style="color: #888;">Personal Semantic Memory</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats in sidebar
    stats = get_stats()
    st.metric("Total Memories", f"{stats.get('total', 0):,}")
    st.metric("This Week", f"{stats.get('this_week', 0):,}")
    
    st.markdown("---")
    
    # Navigation
    page = st.radio("Navigate", ["🔍 Search", "➕ Create", "📊 Stats", "⚙️ Settings"])
    
    st.markdown("---")
    st.caption(f"🕐 Last updated: {datetime.now().strftime('%H:%M')}")

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════

if page == "🔍 Search":
    st.title("🔍 Search Memories")
    
    # Search box
    query = st.text_input("", placeholder="Ask anything... (e.g., 'what did I build today?')", label_visibility="collapsed")
    
    if query:
        with st.spinner("Searching..."):
            results = search_memories(query)
            
            if results:
                st.markdown(f"**Found {len(results)} results**")
                
                for i, mem in enumerate(results):
                    with st.container():
                        st.markdown(f"""
                        <div class="card">
                            <p style="font-size: 1.1rem; margin-bottom: 10px;">{mem.get('content', '')[:300]}</p>
                            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                                <span style="background: #00d4ff20; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">📤 {mem.get('source', 'unknown')}</span>
                                {''.join(f'<span style="background: #7c3aed20; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">#{t}</span>' for t in (mem.get('tags', [])[:3]))}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No memories found. Try a different query.")

elif page == "➕ Create":
    st.title("➕ Create Memory")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        content = st.text_area("What do you want to remember?", height=150, placeholder="Enter any information you want to store...")
    
    with col2:
        source = st.selectbox("Source", ["manual", "telegram", "whatsapp", "email", "claude", "chatgpt"])
        tags = st.text_input("Tags (comma separated)", placeholder="ai, project, idea")
    
    if st.button("💾 Save Memory", use_container_width=True):
        if content:
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            result = create_memory(content, source, tag_list)
            if result.get("id"):
                st.success("✅ Memory saved!")
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")
        else:
            st.warning("Please enter some content")

elif page == "📊 Stats":
    st.title("📊 Statistics")
    
    stats = get_stats()
    
    # Top row metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Memories", f"{stats.get('total', 0):,}")
    with c2:
        st.metric("This Week", f"{stats.get('this_week', 0):,}")
    with c3:
        sources = len(stats.get('by_source', {}))
        st.metric("Sources", f"{sources}")
    with c4:
        tags = len(stats.get('top_tags', {}))
        st.metric("Unique Tags", f"{tags}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("By Source")
        source_data = stats.get('by_source', {})
        if source_data:
            df = pd.DataFrame(list(source_data.items()), columns=["Source", "Count"])
            st.bar_chart(df.set_index("Source"))
    
    with col2:
        st.subheader("Top Tags")
        tag_data = stats.get('top_tags', {})
        if tag_data:
            df = pd.DataFrame(list(tag_data.items())[:10], columns=["Tag", "Count"])
            st.bar_chart(df.set_index("Tag"))

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.info("Settings page coming soon! Edit config/settings.yaml directly for now.")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 20px;">
    🧠 Open Brain v1.0 | Personal Semantic Memory System
</div>
""", unsafe_allow_html=True)

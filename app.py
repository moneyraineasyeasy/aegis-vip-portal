import os
import time
import pandas as pd
import streamlit as st
from datetime import datetime

# Prevent PyArrow segmentation faults on local systems
os.environ["ARROW_DEFAULT_MEMORY_POOL"] = "system"

# 1. Page Configuration (Forcing collapsed sidebar for cleaner mobile entry)
st.set_page_config(
    page_title="雨姐VIP推薦庫 | Aegis Terminal",
    page_icon="static/logo.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. THE MASTER CSS INJECTION (Glassmorphism, Animations, Scrollbars, Anti-aliasing)
st.markdown("""
    <style>
    /* Global Typography & Font Smoothing */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Custom Obsidian Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: transparent; 
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b; 
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #334155; 
    }

    /* Global Background - Deep space with radial gradient */
    .stApp {
        background-color: #030712 !important;
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, transparent 80%);
    }
    
    /* Glowing Trophy & Gradient Title Wrapper */
    .header-container {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 10px;
        margin-bottom: 2px;
    }
    .glowing-trophy {
        font-size: 2.6rem;
        filter: drop-shadow(0 0 15px rgba(245, 158, 11, 0.4)) drop-shadow(0 2px 4px rgba(0,0,0,0.6));
    }
    .vip-header-text {
        font-size: 2.3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #FFFFFF 20%, #F59E0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }
    .vip-subtitle {
        font-size: 1rem;
        color: #475569;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0px;
        margin-bottom: 25px;
        padding-left: 4px;
    }
    
    /* Welcome User Card - True Frosted Glass */
    .user-welcome-card {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #F59E0B;
        padding: 18px 22px;
        border-radius: 8px;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    
    /* --- CUSTOM COLOR-CODED ACCORDION CONTAINERS --- */
    .custom-match-card {
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
    }
    .custom-match-card:hover {
        transform: translateY(-2px);
    }

    /* 1. Standard Match Box Styling */
    .card-standard {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .card-standard:hover {
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.12), 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }

    /* 2. 重心 (Heavy) Match Box Styling */
    .card-heavy {
        background: linear-gradient(135deg, rgba(35, 24, 12, 0.5) 0%, rgba(15, 23, 42, 0.65) 100%);
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .card-heavy:hover {
        border-color: rgba(245, 158, 11, 0.7);
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.2), 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }

    /* 3. 完場 (Ended) Match Box Styling */
    .card-ended {
        background: rgba(10, 15, 26, 0.4);
        border: 1px solid rgba(148, 163, 184, 0.12);
    }
    .card-ended:hover {
        border-color: rgba(148, 163, 184, 0.3);
        box-shadow: 0 0 25px rgba(148, 163, 184, 0.05), 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    
    .custom-match-summary {
        padding: 16px 20px;
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        cursor: pointer;
        list-style: none;
        display: flex;
        justify-content: space-between;
        align-items: center;
        user-select: none;
    }
    .custom-match-summary::-webkit-details-marker {
        display: none;
    }
    .custom-match-body {
        padding: 4px 16px 16px 16px;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        background: rgba(0, 0, 0, 0.2);
    }
    
    /* Ticket Stub Design */
    .ticket-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(0, 0, 0, 0.3);
        padding: 10px 14px;
        border-radius: 6px 6px 0 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    /* Breathing Animation for Standard Pill */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    .rec-pill {
        display: inline-block;
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        color: #FFFFFF;
        font-size: 1.25rem;
        font-weight: 800;
        padding: 6px 18px;
        border-radius: 6px;
        letter-spacing: 0.5px;
        animation: pulse-glow 2.5s infinite;
    }

    /* 🔥 Breathing Animation for HIGHLY RECOMMENDED (重心) Pill */
    @keyframes pulse-glow-heavy {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.5); }
        70% { box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    
    .rec-pill-heavy {
        display: inline-block;
        background: linear-gradient(135deg, #DC2626 0%, #F59E0B 100%);
        color: #FFFFFF;
        font-size: 1.25rem;
        font-weight: 900;
        padding: 6px 18px;
        border-radius: 6px;
        letter-spacing: 1px;
        animation: pulse-glow-heavy 2s infinite;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    
    /* Inset Depth Executive Commentary Box */
    .commentary-box {
        background: rgba(0, 0, 0, 0.4);
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.6);
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-left: 3px solid #38BDF8;
        padding: 18px;
        border-radius: 0 0 6px 6px;
        color: #cbd5e1;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 12px;
    }

    /* Inset Border Modification for Heavy Picks */
    .heavy-border {
        border-left: 3px solid #F59E0B !important;
    }
    
    /* Custom Input fields for Login */
    div[data-testid="stTextInput"] input {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 0 1px #f59e0b !important;
    }
    
    /* Tabs Overrides for clean Obsidian Aesthetics */
    button[data-baseweb="tab"] {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #64748B !important;
        padding: 12px 20px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #F59E0B !important;
        border-bottom-color: #F59E0B !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Secure Data Loader
SHEET_ID = st.secrets["sheets"]["sheet_id"]

@st.cache_data(ttl=30)
def fetch_sheet_data():
    try:
        users_csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=users"
        recs_csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=recommendations"
        return pd.read_csv(users_csv_url), pd.read_csv(recs_csv_url)
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame()

users_df, recs_df = fetch_sheet_data()

# 4. Session State Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- APP HEADER ---
st.markdown("""
    <div class="header-container">
        <span class="glowing-trophy">🏆</span>
        <span class="vip-header-text">雨姐VIP足球 analysis</span>
    </div>
""", unsafe_allow_html=True)
st.markdown('<div class="vip-subtitle">自研 AEGIS 模型 V5</div>', unsafe_allow_html=True)

# 5. AUTHENTICATION PORTAL
if not st.session_state.logged_in:
    st.markdown("### 🔐 會員登入 / Client Login")
    
    input_user = st.text_input("用戶名 (Username)", placeholder="輸入會員帳號...").strip()
    input_pass = st.text_input("密碼 (Password)", type="password", placeholder="******").strip()
    
    if st.button("驗證並登入系統", use_container_width=True, type="primary"):
        if not users_df.empty:
            users_df.columns = [c.strip().lower() for c in users_df.columns]
            user_row = users_df[users_df["username"].astype(str).str.strip().str.lower() == input_user.lower()]
            
            if not user_row.empty:
                if input_pass == str(user_row.iloc[0]["password"]).strip():
                    try:
                        db_expiry = str(user_row.iloc[0]["expiry_date"]).strip()
                        if datetime.now().date() > datetime.strptime(db_expiry, "%Y-%m-%d").date():
                            st.error(f"❌ 您的會員已於 {db_expiry} 過期。請聯絡雨姐續費。")
                            st.stop()
                    except ValueError:
                        st.error("❌ 系統錯誤：用戶過期日期格式不正確。")
                        st.stop()
                    
                    if str(user_row.iloc[0]["status"]).strip().lower() != "active":
                        st.error("❌ 您的帳戶已被暫停。")
                        st.stop()

                    # -- THE BOOT SEQUENCE --
                    status_box = st.empty()
                    status_box.info("🛡️ 驗證成功 (Authentication Success)...")
                    time.sleep(0.5)
                    status_box.warning("⚙️ 啟動 Aegis V5 引擎 (Initializing Engine)...")
                    time.sleep(0.6)
                    status_box.success("✅ 正在建立安全連線 (Establishing Secure Connection)...")
                    time.sleep(0.5)
                    status_box.empty()
                    
                    st.session_state.logged_in = True
                    st.session_state.username = input_user
                    st.session_state.expiry_date = db_expiry
                    st.rerun()
                else:
                    st.error("❌ 密碼錯誤，請重新輸入。")
            else:
                st.error("❌ 找不到該用戶，請檢查用戶名。")
        else:
            st.error("❌ 無法讀取用戶數據，請稍後再試。")

# 6. SECURE CLIENT DASHBOARD
else:
    st.sidebar.markdown("### 🛡️ 帳戶安全中心")
    st.sidebar.markdown(f"**目前用戶:** `{st.session_state.username}`")
    st.sidebar.markdown(f"**會員到期:** `{st.session_state.expiry_date}`")
    st.sidebar.write("---")
    if st.sidebar.button("登出系統 / Log Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Fixed rogue 'br>' bug here
    st.markdown(f"""
        <div class="user-welcome-card">
            <span style="font-size: 1.35rem; font-weight: 700; color: #F8FAFC;">👋 歡迎回來，尊貴會員 <span style="color: #F59E0B;">{st.session_state.username}</span>！</span><br>
            <span style="color: #94A3B8; font-size: 0.95rem; display: inline-block; margin-top: 6px;">以下是 Aegis 模型今日為您精確計算出的優質配對推薦：</span>
        </div>
    """, unsafe_allow_html=True)
    
    if not recs_df.empty:
        recs_df.columns = [c.strip().lower() for c in recs_df.columns]
        
        valid_statuses = ["published", "ended"]
        visible_recs = recs_df[recs_df["status"].astype(str).str.strip().str.lower().isin(valid_statuses)]
        
        if not visible_recs.empty:
            unique_matches = visible_recs["match_name"].unique()
            
            # Separate active recommendations vs historical ended matches for Tab configuration
            active_matches = []
            historical_matches = []
            
            for match_name in unique_matches:
                match_data = visible_recs[visible_recs["match_name"] == match_name]
                if "published" in match_data["status"].astype(str).str.strip().str.lower().values:
                    active_matches.append(match_name)
                else:
                    historical_matches.append(match_name)
            
            # --- TABBED LAYOUT ARCHITECTURE ---
            tab_active, tab_historical = st.tabs([f"🎯 今日核心推薦 ({len(active_matches)})", f"📜 歷史賽事紀錄 ({len(historical_matches)})"])
            
            # Shared rendering logic for cleaner containment
            def render_matches(match_list_to_render):
                st.write("")
                for match_name in match_list_to_render:
                    match_data = visible_recs[visible_recs["match_name"] == match_name]
                    
                    has_heavy_pick = False
                    has_hit_win = False
                    is_match_ended = False
                    
                    for row in match_data.itertuples():
                        is_heavy_val = str(getattr(row, "is_heavy", "false")).strip().lower()
                        if is_heavy_val in ["true", "1", "yes", "重心"]:
                            has_heavy_pick = True
                            
                        row_status = str(getattr(row, "status", "published")).strip().lower()
                        if row_status == "ended":
                            is_match_ended = True
                            row_res = str(getattr(row, "result", "")).strip().lower()
                            if row_res in ["hit", "win", "中", "收錢"]:
                                has_hit_win = True

                    # Determine title headers and color-coded box classes dynamically
                    title_prefix = "⚽"
                    box_class = "card-standard"
                    
                    if is_match_ended:
                        title_prefix = "✅ [已完場]" if has_hit_win else "⚪ [已完場]"
                        box_class = "card-ended"
                    elif has_heavy_pick:
                        title_prefix = "🔥 [🔥 重心推薦]"
                        box_class = "card-heavy"

                    # Custom Outer Accordion Construction
                    inner_content_html = ""
                    for i, row in enumerate(match_data.itertuples()):
                        match_id = getattr(row, "id", i)
                        rec_title = getattr(row, "rec_title", "查看推薦詳情")
                        commentary_text = getattr(row, "commentary", "暫無分析內容。")
                        
                        row_status = str(getattr(row, "status", "published")).strip().lower()
                        row_result = str(getattr(row, "result", "")).strip().lower()
                        is_heavy_pick = str(getattr(row, "is_heavy", "false")).strip().lower() in ["true", "1", "yes", "重心"]
                        
                        try:
                            stars_val = int(getattr(row, "stars", 4))
                            star_emojis = "⭐️" * stars_val
                        except ValueError:
                            star_emojis = "⭐️⭐️⭐️⭐️"
                        
                        spacing_style = "margin-top: 15px;" if i > 0 else ""
                        opacity_style = "opacity: 0.65;" if row_status == "ended" and row_result != "hit" else "opacity: 1.0;"
                        commentary_border_class = "heavy-border" if is_heavy_pick else ""
                        
                        if is_heavy_pick and row_status != "ended":
                            pill_html = f'<span class="rec-pill-heavy">🔥 重心推薦：{rec_title}</span>'
                        else:
                            pill_html = f'<span class="rec-pill">{rec_title}</span>'
                            
                        status_banner_html = ""
                        if row_status == "ended":
                            if row_result in ["hit", "win", "中", "收錢"]:
                                status_banner_html = '<div style="margin-top: 8px; color: #2ecc71; font-weight: 900; font-size: 1.15rem;">🟢 完美命中，輕鬆收錢！</div>'
                            else:
                                status_banner_html = '<div style="margin-top: 8px; color: #94A3B8; font-weight: 700; font-size: 1rem;"><s>⚪ 已完場 (賽事結束)</s></div>'

                        inner_content_html += f"""
                            <div style="{opacity_style} {spacing_style}">
                                <div class="ticket-header">
                                    <span style="font-size: 0.95rem; font-weight: 700; color: #94A3B8;">
                                        📋 推薦方案 {i+1} ｜ 信心指數：<span style="color:#F59E0B; letter-spacing:2px;">{star_emojis}</span>
                                    </span>
                                    <span style="font-size: 0.8rem; color: #475569; font-weight: 600;">#{match_id}</span>
                                </div>
                                <div style="background: rgba(15, 23, 42, 0.4); padding: 16px 14px 4px 14px; border-left: 1px solid rgba(255,255,255,0.03); border-right: 1px solid rgba(255,255,255,0.03);">
                                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px; flex-wrap: wrap;">
                                        <span style="font-size: 1rem; font-weight: 700; color: #64748B;">🎯 核心推薦：</span>
                                        {pill_html}
                                    </div>
                                    {status_banner_html}
                                    <div style="font-size: 0.9rem; font-weight: 700; color: #38BDF8; display: flex; align-items: center; gap: 4px; margin-bottom: 6px; margin-top: 10px;">
                                        🗣️ 雨姐短評 (Commentary)：
                                    </div>
                                </div>
                                <div class="commentary-box {commentary_border_class}">
                                    {commentary_text}
                                </div>
                            </div>
                        """

                    # Render the beautiful custom colored-coded disclosure box
                    st.html(f"""
                        <details class="custom-match-card {box_class}">
                            <summary class="custom-match-summary">
                                <span>{title_prefix} {match_name}</span>
                                <span style="font-size: 0.85rem; color: #475569; font-weight:600;">查看詳情 ▾</span>
                            </summary>
                            <div class="custom-match-body">
                                {inner_content_html}
                            </div>
                        </details>
                    """)

            # Populate Current Active tab
            with tab_active:
                if active_matches:
                    render_matches(active_matches)
                else:
                    st.info("☘️ 今日暫未有最新發佈的推薦，請密切留意更新！")

            # Populate Completed Archive tab
            with tab_historical:
                if historical_matches:
                    render_matches(historical_matches)
                else:
                    st.info("📜 目前暫無已完場的歷史賽事紀錄。")
        else:
            st.info("☘️ 今日暫未有最新發佈的推薦，請密切留意更新！")
    else:
        st.warning("⚠️ 數據庫暫無推薦數據，請聯絡後台管理員。")

# 7. Minimal Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.write("---")
st.caption("🛡️ Powered by Aegis Core Engine V5. Premium Secure Architecture.")

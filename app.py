import streamlit as st
import requests
from PIL import Image
import os

# === 1. 页面基础配置 ===
st.set_page_config(
    page_title="5Gnu Command Center",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === 2. 全局 CSS 样式表 (修复Bug & 提升科技感) ===
st.markdown("""
<style>
    /* --- 全局背景设置 --- */
    .stApp {
        background-color: #0f172a; /* 改为深色背景，符合Command Center定位 */
        color: #e2e8f0;
    }
    
    /* --- 修复 Streamlit 图标显示 Bug (隐藏 keyboard_double...) --- */
    button[kind="header"] {
        display: none !important;
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 0px; 
    }
    /* 强制隐藏可能出现的异常文字 */
    span:contains("keyboard_double_arrow_right") {
        display: none !important;
        opacity: 0;
    }
    
    /* --- 侧边栏美化 (科技深蓝风格) --- */
    [data-testid="stSidebar"] {
        background-color: #020617; /* 更黑的背景 */
        border-right: 1px solid #1e293b;
    }
    
    /* 侧边栏文字颜色 */
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }

    /* Logo 区域容器 */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px 0;
        background: radial-gradient(circle at center, #1e293b 0%, transparent 70%);
        margin-bottom: 20px;
        border-bottom: 1px solid #1e293b;
    }
    
    /* 侧边栏按钮 - 危险操作 (Reset) */
    .reset-btn button {
        background-color: #7f1d1d !important;
        color: #fca5a5 !important;
        border: 1px solid #991b1b !important;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s;
    }
    .reset-btn button:hover {
        background-color: #b91c1c !important;
        box-shadow: 0 0 10px #ef4444;
    }

    /* --- 侧边栏仪表盘数据框 --- */
    .metric-box {
        background: rgba(15, 23, 42, 0.6);
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
        border: 1px solid #334155;
        position: relative;
        overflow: hidden;
    }
    /* 增加一个扫描线动画效果 */
    .metric-box::after {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.1), transparent);
        animation: scan 3s infinite;
    }
    @keyframes scan {
        0% { left: -100%; }
        100% { left: 200%; }
    }

    .metric-value {
        font-size: 1.4em;
        font-weight: bold;
        color: #38bdf8; /* 天蓝色 */
        font-family: 'Courier New', monospace;
    }
    .metric-label {
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
    }

    /* --- 主区域样式重构 --- */
    
    /* 主标题样式 */
    .main-header {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -1px;
        text-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
    }

    /* 通用卡片 (改为深色磨砂玻璃感) */
    .css-card {
        background-color: #1e293b; /* 深蓝灰色 */
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
        border: 1px solid #334155;
        color: #e2e8f0;
    }

    /* 右侧信息面板 - 赛博朋克边框 */
    .cyber-card {
        background-color: rgba(30, 41, 59, 0.8);
        border: 1px solid #0ea5e9;
        box-shadow: 0 0 10px rgba(14, 165, 233, 0.2);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .cyber-title {
        color: #0ea5e9;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        border-bottom: 1px solid #0f172a;
        padding-bottom: 5px;
        margin-bottom: 10px;
        font-size: 0.9em;
    }
    .cyber-data-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
    }
    .cyber-value { color: #fff; }

    /* 聊天气泡优化 (深色模式) */
    .stChatMessage {
        background-color: #1e293b;
        border: 1px solid #334155;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #334155;
    }
    
    /* 隐藏 footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# === 3. 侧边栏 (Mission Control Center) ===
with st.sidebar:
    # --- LOGO 区域 (优化版) ---
    # 使用一个专门的容器来居中和衬托 Logo，解决看不清的问题
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        if os.path.exists("Logo抠图版.png"):
            # 使用 container width 撑满容器
            st.image("Logo抠图版.png", width=180) 
        else:
            # 备用文字 Logo
            st.markdown("<h1 style='text-align:center; color:#38bdf8;'>5Gnu</h1>", unsafe_allow_html=True)
    except:
        st.markdown("Logo File Missing")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 模块 1: 系统模式 ---
    st.markdown("### 🎛️ SYSTEM MODE")
    app_mode = st.radio(
        "Mode Selection",
        ["🏆 Bett 2026 Strategy", "🎓 AOPA Exam Prep", "🚁 Drone Tech Support"],
        label_visibility="collapsed"
    )
    
    if app_mode == "🏆 Bett 2026 Strategy":
        st.markdown("""
        <div style="background:#172554; padding:10px; border-radius:4px; border-left:3px solid #facc15;">
            <small>TARGET: Sky & Earth Tournament</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    # --- 模块 2: 实时遥测 (Telemetry) ---
    st.markdown("### 📡 TELEMETRY DATA")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">5G LINK</div>
            <div class="metric-value">98%</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">LATENCY</div>
            <div class="metric-value">12ms</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">AGENT STATUS</div>
        <div style="color:#4ade80; font-weight:bold;">● ONLINE / LISTENING</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # --- 模块 3: 重置按钮 (高亮显眼) ---
    st.markdown("### ⚠️ DANGER ZONE")
    # 使用 container 来应用 CSS 类
    with st.container():
        st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
        if st.button("☢️ RESET SYSTEM / 清空记录"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("🌐 Access Web Portal", "http://ltexpo2023.5gnumultimedia.com", use_container_width=True)


# === 4. 主界面逻辑 ===

# 标题区 (改名)
st.markdown("<h1 class='main-header'>5Gnu LAE Command Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; margin-top:-15px;'>AOPA Authorized Low Altitude Economy Control System</p>", unsafe_allow_html=True)

# 定义两栏布局
col_main, col_info = st.columns([7, 3])

# --- 右侧信息面板 (科技感升级) ---
with col_info:
    # 面板 1: 飞行参数
    st.markdown("""
    <div class="cyber-card">
        <div class="cyber-title">✈️ FLIGHT PARAMETERS</div>
        <div class="cyber-data-row"><span>UNIT ID:</span> <span class="cyber-value">X-200-PRO</span></div>
        <div class="cyber-data-row"><span>MODE:</span> <span class="cyber-value">AUTO-PILOT</span></div>
        <div class="cyber-data-row"><span>BATTERY:</span> <span class="cyber-value" style="color:#4ade80">87%</span></div>
        <div class="cyber-data-row"><span>ALTITUDE:</span> <span class="cyber-value">0.0m (GND)</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # 面板 2: 快捷指令
    st.markdown("""
    <div class="cyber-card">
        <div class="cyber-title">⌨️ QUICK COMMANDS</div>
        <ul style="padding-left:15px; margin:0; color:#cbd5e1; font-size:0.85em;">
            <li style="margin-bottom:5px;">Mission: Bett 2026 Overview</li>
            <li style="margin-bottom:5px;">Tech: Sky & Earth Sync</li>
            <li style="margin-bottom:5px;">Edu: AOPA License Path</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 左侧主对话区域 ---
with col_main:
    # 比赛通告栏 (保持设计，但微调颜色适应深色模式)
    st.markdown("""
    <div class="css-card" style="border-left: 4px solid #f59e0b; background: linear-gradient(90deg, #1e293b 0%, #172554 100%);">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <h3 style="color: #fbbf24; margin: 0; font-size: 1.1em;">🏆 ALERT: Bett 2026 & Sky/Earth Soccer</h3>
            <span style="background:#451a03; color:#fbbf24; padding:2px 8px; border-radius:4px; font-size:0.7em; border:1px solid #b45309;">FEATURED</span>
        </div>
        <p style="margin-top: 10px; color: #cbd5e1; font-size: 0.9em;">
            Deploying <strong>5G Remote Control</strong> tech: UK Star controlling HK Robots.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 聊天记录区
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Command Center Online. Awaiting instructions regarding Bett 2026 or Flight Missions."}
        ]

    chat_container = st.container()
    
    # 输入框
    prompt = st.chat_input("Enter command or query...")

    with chat_container:
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user").write(prompt)

        # API 调用
        API_URL = "https://cloud.flowiseai.com/api/v1/prediction/46e17ecb-9ace-46ce-91ed-f7332554b78c"
        
        with chat_container:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                # 模拟打字机效果或加载状态
                message_placeholder.markdown("`PROCESSING DATA STREAM...`")
                
                try:
                    response = requests.post(API_URL, json={"question": prompt})
                    if response.status_code == 200:
                        ai_reply = response.json().get("text", "Error: Empty Response")
                    else:
                        ai_reply = f"System Error: {response.status_code}"
                except Exception as e:
                    ai_reply = f"Link Failure: {e}"
                
                message_placeholder.write(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})


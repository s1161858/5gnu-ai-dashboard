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

# === 2. 全局 CSS (赛博朋克/指挥中心风格) ===
st.markdown("""
<style>
    /* --- 全局背景：深空黑蓝 --- */
    .stApp {
        background-color: #020617; /* Very Dark Blue/Black */
        color: #e2e8f0;
    }

    /* --- 修复 Streamlit 图标 Bug (隐藏 keyboard_double...) --- */
    button[kind="header"] { display: none !important; }
    span:contains("keyboard_double_arrow_right") { display: none !important; opacity: 0; }
    div[data-testid="stSidebarNav"] { padding-top: 0px; }

    /* --- 侧边栏样式 --- */
    [data-testid="stSidebar"] {
        background-color: #0f172a; /* Slate 900 */
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important; /* 浅灰文字 */
    }

    /* --- Logo 专属光舱 (解决看不清问题) --- */
    .logo-box {
        background-color: rgba(255, 255, 255, 0.95); /* 亮白背景 */
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.3); /* 青色辉光 */
        border: 2px solid #38bdf8;
    }

    /* --- 重置按钮 (核按钮风格) --- */
    .reset-box button {
        background: repeating-linear-gradient(
            45deg,
            #7f1d1d,
            #7f1d1d 10px,
            #991b1b 10px,
            #991b1b 20px
        ) !important;
        color: #ffffff !important;
        border: 2px solid #ef4444 !important;
        font-weight: 900 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        width: 100%;
        padding: 15px 0 !important;
        transition: transform 0.2s;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
    }
    .reset-box button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(220, 38, 38, 0.8);
    }

    /* --- 仪表盘数据框 --- */
    .metric-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        position: relative;
        overflow: hidden;
    }
    .metric-val {
        font-family: 'Courier New', monospace;
        font-size: 1.5em;
        font-weight: bold;
        color: #38bdf8; /* Neon Cyan */
        text-shadow: 0 0 5px rgba(56, 189, 248, 0.6);
    }
    .metric-lbl {
        font-size: 0.7em;
        color: #94a3b8;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* --- 主区域样式 --- */
    .main-header {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin-bottom: 0px;
    }
    
    /* 右侧信息面板 - 赛博边框 */
    .cyber-panel {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid #0ea5e9; /* Cyan Border */
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 0 10px rgba(14, 165, 233, 0.1);
        backdrop-filter: blur(5px);
    }
    
    /* 比赛通告栏 - 霓虹橙警示 */
    .event-banner {
        background: linear-gradient(90deg, rgba(67, 20, 7, 0.6) 0%, rgba(30, 41, 59, 0) 100%);
        border-left: 4px solid #f97316; /* Neon Orange */
        padding: 20px;
        border-radius: 8px;
        border: 1px solid rgba(249, 115, 22, 0.3);
        margin-bottom: 20px;
    }

    /* 输入框样式微调 */
    .stTextInput input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #475569 !important;
    }
    
    /* 隐藏 Footer */
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# === 3. 侧边栏 (Mission Control) ===
with st.sidebar:
    # [Logo 区域] - 白色光舱
    st.markdown('<div class="logo-box">', unsafe_allow_html=True)
    try:
        if os.path.exists("Logo抠图版.png"):
            # 略微调小宽度以适应边距
            st.image("Logo抠图版.png", width=160)
        else:
            st.markdown("<h2 style='color:#0f172a; margin:0;'>5Gnu</h2>", unsafe_allow_html=True)
    except:
        st.error("Logo Error")
    st.markdown('</div>', unsafe_allow_html=True)

    # [模式选择]
    st.markdown("### 💠 SYSTEM PROTOCOL")
    mode = st.radio(
        "Protocol",
        ["🏆 Bett 2026 Strategy", "🎓 AOPA Exam Prep", "🔧 Drone Tech Support"],
        label_visibility="collapsed"
    )
    
    # 动态提示条
    if "Bett" in mode:
        st.markdown("""
        <div style="margin-top:5px; padding:8px; background:rgba(234, 179, 8, 0.1); border:1px solid #eab308; border-radius:4px; color:#facc15;">
            <small>⚡ <strong>ACTIVE MISSION:</strong> Sky & Earth Tournament Setup</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    # [实时遥测]
    st.markdown("### 📡 LIVE TELEMETRY")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-lbl">5G SIGNAL</div>
            <div class="metric-val">📶 -38dB</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-lbl">LATENCY</div>
            <div class="metric-val">⚡ 9ms</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # [核按钮 - 重置]
    st.markdown("### ⚠️ DANGER ZONE")
    # 使用 container 包裹以应用 CSS
    with st.container():
        st.markdown('<div class="reset-box">', unsafe_allow_html=True)
        if st.button("☢️ RESET SYSTEM / 重置系统"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("v3.0.1 | 5Gnu Low Altitude Economy Center")


# === 4. 主界面逻辑 ===

# 标题 (改名)
st.markdown("<h1 class='main-header'>5Gnu LAE Command Center</h1>", unsafe_allow_html=True)
st.caption("AOPA Authorized | Low Altitude Economy Intelligent System")

col_main, col_info = st.columns([7, 3])

# --- 右侧信息面板 (Cyber Style) ---
with col_info:
    # 面板 1
    st.markdown("""
    <div class="cyber-panel">
        <h4 style="color:#0ea5e9; margin-top:0; border-bottom:1px solid #1e293b; padding-bottom:5px;">✈️ DRONE STATUS</h4>
        <div style="font-family:'Courier New'; font-size:0.9em; line-height:1.6;">
            <div>ID: <span style="color:#fff;">X-200-PRO</span></div>
            <div>MODE: <span style="color:#4ade80;">AUTO-PILOT</span></div>
            <div>BATTERY: <span style="color:#facc15;">87%</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 面板 2 (快捷指令)
    st.markdown("""
    <div class="cyber-panel">
        <h4 style="color:#a78bfa; margin-top:0; border-bottom:1px solid #1e293b; padding-bottom:5px;">⌨️ QUICK COMMS</h4>
        <ul style="padding-left:15px; margin:0; font-size:0.85em; color:#cbd5e1;">
            <li>Bett 2026 Overview</li>
            <li>Sky & Earth Sync Detail</li>
            <li>AOPA Exam Syllabus</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 左侧主对话区域 ---
with col_main:
    # 比赛通告栏 (Neon Orange Theme)
    st.markdown("""
    <div class="event-banner">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="color:#f97316; margin:0; font-size:1.2rem;">🏆 ALERT: Bett 2026 & Sky/Earth Soccer</h3>
            <span style="background:#f97316; color:black; padding:2px 8px; border-radius:4px; font-weight:bold; font-size:0.7rem;">PRIORITY</span>
        </div>
        <p style="color:#fdba74; margin-top:10px; margin-bottom:5px;">
            <strong>Mission Objective:</strong> Demonstrate 5G Remote Control capabilities.
        </p>
        <div style="font-size:0.9em; color:#e2e8f0;">
            <span style="color:#f97316;">★ WOW FACTOR:</span> UK Star controlling HK Robots remotely via 5G.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Command Center Online. Ready for mission instructions."}
        ]

    chat_container = st.container()
    
    # 输入框
    prompt = st.chat_input("Enter command code or query...")

    with chat_container:
        for msg in st.session_state.messages:
            # 区分用户和AI的样式
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(msg["content"])

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user").write(prompt)

        # API 调用
        API_URL = "https://cloud.flowiseai.com/api/v1/prediction/46e17ecb-9ace-46ce-91ed-f7332554b78c"
        
        with chat_container:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                placeholder.markdown("`TRANSMITTING DATA...`")
                
                try:
                    response = requests.post(API_URL, json={"question": prompt})
                    if response.status_code == 200:
                        text = response.json().get("text", "")
                        placeholder.write(text)
                        st.session_state.messages.append({"role": "assistant", "content": text})
                    else:
                        placeholder.error(f"Error {response.status_code}")
                except Exception as e:
                    placeholder.error(f"Link Down: {e}")


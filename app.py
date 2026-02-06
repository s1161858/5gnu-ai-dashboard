import streamlit as st
import requests
from PIL import Image
import os

# === 1. 页面基础配置 ===
st.set_page_config(
    page_title="5Gnu Command Center",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded" # 确保侧边栏默认展开
)

# === 2. 全局 CSS (侧边栏深色 + 主界面白色清晰版) ===
st.markdown("""
<style>
    /* --- 1. 主区域恢复白色背景，保证清晰度 --- */
    .stApp {
        background-color: #f8fafc; /* 极淡的灰白色，清晰护眼 */
        color: #1e293b; /* 深色文字，对比度高 */
    }

    /* --- 2. 修复：恢复侧边栏开关按钮 (左上角箭头) --- */
    button[kind="header"] {
        display: block !important; /* 强制显示 */
        color: #0f172a !important; /* 按钮颜色设为深色以便在白底可见 */
    }
    div[data-testid="collapsedControl"] {
        display: block !important;
        color: #0f172a !important;
    }
    
    /* 仅隐藏那个错误的 keyboard_double 图标文字，保留箭头图形 */
    span:contains("keyboard_double_arrow_right") { 
        display: none !important; 
        opacity: 0; 
    }

    /* --- 3. 侧边栏保持深色科技感 --- */
    section[data-testid="stSidebar"] {
        background-color: #0f172a; /* 深邃夜空蓝 */
        border-right: 1px solid #1e293b;
    }
    
    /* 侧边栏内的所有文字强制变白 */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] div {
        color: #cbd5e1 !important;
    }

    /* --- Logo 区域优化 (白底光舱，清晰可见) --- */
    .logo-box {
        background-color: #ffffff; /* 纯白背景 */
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #3b82f6; /* 蓝色边框 */
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); /* 蓝色光晕 */
    }

    /* --- 重置按钮 (红色醒目) --- */
    .reset-box button {
        background-color: #dc2626 !important;
        color: white !important;
        border: 1px solid #ef4444 !important;
        font-weight: bold !important;
        width: 100%;
        transition: 0.3s;
    }
    .reset-box button:hover {
        background-color: #b91c1c !important;
    }

    /* --- 仪表盘数据框 (侧边栏内) --- */
    .metric-container {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 8px;
    }
    .metric-val {
        font-family: 'Courier New', monospace;
        font-size: 1.4em;
        font-weight: bold;
        color: #38bdf8; /* 亮青色数字 */
    }
    .metric-lbl {
        font-size: 0.75em;
        color: #94a3b8;
    }

    /* --- 主界面卡片 (回到清爽的白色卡片) --- */
    .css-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #e2e8f0;
    }

    /* 比赛通告栏 (保留醒目设计，但适应白底) */
    .event-banner {
        background-color: #fff7ed; /* 淡橙色背景 */
        border-left: 5px solid #f97316; /* 橙色左边框 */
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #ffedd5;
    }
    
    /* 聊天气泡 */
    .stChatMessage {
        background-color: white;
        border: 1px solid #e2e8f0;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #eff6ff; /* 淡蓝 */
    }
    
    /* 隐藏 Footer */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)


# === 3. 侧边栏 (Mission Control) ===
with st.sidebar:
    # [Logo 区域] - 白底光舱，确保Logo绝对清晰
    st.markdown('<div class="logo-box">', unsafe_allow_html=True)
    try:
        if os.path.exists("Logo抠图版.png"):
            st.image("Logo抠图版.png", width=150)
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
    
    if "Bett" in mode:
        st.info("⚡ ACTIVE: Sky & Earth Tournament Setup")
    
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

    # [重置按钮]
    st.markdown("### ⚠️ DANGER ZONE")
    with st.container():
        st.markdown('<div class="reset-box">', unsafe_allow_html=True)
        if st.button("☢️ RESET SYSTEM / 重置系统"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("🌐 Go to Website", "http://ltexpo2023.5gnumultimedia.com", use_container_width=True)


# === 4. 主界面逻辑 (回归白色清爽风格) ===

# 标题
st.markdown("<h1 style='color:#1e40af;'>5Gnu LAE Command Center</h1>", unsafe_allow_html=True)
st.caption("AOPA Authorized | Low Altitude Economy Intelligent System")

col_main, col_info = st.columns([7, 3])

# --- 右侧信息面板 ---
with col_info:
    st.markdown("""
    <div class="css-card">
        <h4 style="color:#0ea5e9; border-bottom:1px solid #eee; padding-bottom:5px;">✈️ DRONE STATUS</h4>
        <p><strong>ID:</strong> X-200-PRO</p>
        <p><strong>MODE:</strong> AUTO-PILOT</p>
        <p><strong>BATTERY:</strong> <span style="color:green">87%</span></p>
    </div>
    
    <div class="css-card">
        <h4 style="color:#8b5cf6; border-bottom:1px solid #eee; padding-bottom:5px;">⌨️ QUICK COMMS</h4>
        <ul>
            <li>Bett 2026 Overview</li>
            <li>Sky & Earth Sync Detail</li>
            <li>AOPA Exam Syllabus</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 左侧主对话区域 ---
with col_main:
    # 比赛通告栏 (淡橙色背景，黑字，清晰易读)
    st.markdown("""
    <div class="event-banner">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="color:#c2410c; margin:0; font-size:1.2rem;">🏆 ALERT: Bett 2026 & Sky/Earth Soccer</h3>
            <span style="background:#ffedd5; color:#c2410c; padding:2px 8px; border-radius:4px; font-weight:bold; border:1px solid #c2410c;">FEATURED</span>
        </div>
        <p style="color:#431407; margin-top:10px;">
            <strong>Mission Objective:</strong> Demonstrate 5G Remote Control capabilities.
        </p>
        <div style="font-size:0.9em; color:#7c2d12;">
            ★ <strong>WOW FACTOR:</strong> UK Star controlling HK Robots remotely via 5G.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "您好！指挥中心在线。请指示飞行任务或询问 Bett 2026 赛事详情。"}
        ]

    chat_container = st.container()
    
    # 输入框
    prompt = st.chat_input("在此输入指令...")

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
                placeholder = st.empty()
                placeholder.markdown("`Connecting to 5G Node...`")
                
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


import streamlit as st
import requests
from PIL import Image
import os
import base64
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# === 1. 页面基础配置 ===
st.set_page_config(
    page_title="5Gnu Command Center",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)


# === 辅助函数：将图片转换为 HTML 可用的 Base64 格式 ===
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None


# === 2. 全局 CSS (样式定义) ===
st.markdown("""
<style>
    /* --- 1. 强制显示侧边栏开关按钮 --- */
    header[data-testid="stHeader"] {
        background: transparent !important;
        visibility: visible !important;
        z-index: 99999 !important;
    }
    button[kind="header"] {
        visibility: visible !important;
        display: block !important;
        color: #0f172a !important;
    }
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        color: #0f172a !important;
    }
    span:contains("keyboard_double_arrow_right") { 
        display: none !important; 
    }


    /* --- 2. 布局颜色 --- */
    .stApp {
        background-color: #f8fafc; /* 主区域白 */
        color: #1e293b;
    }
    section[data-testid="stSidebar"] {
        background-color: #0f172a; /* 侧边栏深蓝 */
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] * {
        color: #cbd5e1 !important; /* 侧边栏文字白 */
    }


    /* --- 3. 侧边栏 Logo 容器 (纯白底色) --- */
    .sidebar-logo-box {
        background-color: #ffffff !important; /* 强制纯白 */
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #3b82f6; /* 蓝边框 */
        box-shadow: 0 4px 10px rgba(0,0,0,0.5); /* 阴影 */
    }
    .sidebar-logo-box img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 0 auto;
    }


    /* --- 4. 仪表盘数据 (侧边栏) --- */
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
        color: #38bdf8;
    }
    .metric-lbl {
        font-size: 0.75em;
        color: #94a3b8;
    }


    /* --- 5. 右侧功能区样式 --- */
    .danger-zone-card {
        background-color: #fef2f2;
        border: 1px solid #fee2e2;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    /* 红色重置按钮 */
    .reset-btn-right button {
        background-color: #dc2626 !important;
        color: white !important;
        width: 100%;
        border: none !important;
        font-weight: bold;
    }
    .reset-btn-right button:hover {
        background-color: #b91c1c !important;
    }
    
    /* 蓝色官网按钮容器 */
    .web-btn-container {
        margin-top: 10px;
    }
    /* 针对 st.link_button 的样式覆盖 */
    .web-btn-container a {
        background-color: #eff6ff !important;
        color: #1d4ed8 !important;
        border: 1px solid #bfdbfe !important;
        width: 100%;
        display: flex;
        justify-content: center;
        font-weight: bold !important;
    }
    .web-btn-container a:hover {
        background-color: #dbeafe !important;
        border-color: #3b82f6 !important;
    }


    /* --- 6. 通告栏 --- */
    .event-banner {
        background-color: #fff7ed;
        border-left: 5px solid #f97316;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #ffedd5;
    }
    
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)



# === 3. 侧边栏逻辑 ===
with st.sidebar:
    # [Logo] - 使用 HTML+Base64 强行嵌入白盒子
    logo_path = "Logo抠图版.png"
    img_b64 = get_base64_image(logo_path)
    
    if img_b64:
        st.markdown(f"""
        <div class="sidebar-logo-box">
            <img src="data:image/png;base64,{img_b64}" alt="5Gnu Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sidebar-logo-box">
            <h2 style='color:#0f172a !important; margin:0;'>5Gnu</h2>
        </div>
        """, unsafe_allow_html=True)


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
    
    st.markdown("<div style='margin-top:20px; font-size:0.8em; color:#64748b;'>System v3.2.0</div>", unsafe_allow_html=True)



# === 4. 主界面逻辑 ===


# [主界面顶部 Logo]
col_top_logo, _ = st.columns([1, 10])
with col_top_logo:
    if os.path.exists("Logo抠图版.png"):
        st.image("Logo抠图版.png", width=100)
    else:
        st.markdown("🚁")


# 标题
st.markdown("<h1 style='color:#1e40af; margin-top:-10px;'>5Gnu LAE Command Center</h1>", unsafe_allow_html=True)
st.caption("AOPA Authorized | Low Altitude Economy Intelligent System")


col_main, col_info = st.columns([7, 3])


# --- 右侧信息面板 ---
with col_info:
    # 1. 飞行状态
    st.markdown("""
    <div style="background:white; padding:15px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05);">
        <h4 style="color:#0ea5e9; margin-top:0; border-bottom:1px solid #eee; padding-bottom:5px;">✈️ DRONE STATUS</h4>
        <p style="margin:5px 0;"><strong>ID:</strong> X-200-PRO</p>
        <p style="margin:5px 0;"><strong>MODE:</strong> AUTO-PILOT</p>
        <p style="margin:5px 0;"><strong>BATTERY:</strong> <span style="color:green">87%</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 快捷指令
    st.markdown("""
    <div style="background:white; padding:15px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05);">
        <h4 style="color:#8b5cf6; margin-top:0; border-bottom:1px solid #eee; padding-bottom:5px;">⌨️ QUICK COMMS</h4>
        <ul style="padding-left:20px; margin:0;">
            <li>Bett 2026 Overview</li>
            <li>Sky & Earth Sync Detail</li>
            <li>AOPA Exam Syllabus</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


    # 3. Danger Zone + 官网入口
    st.markdown('<div class="danger-zone-card">', unsafe_allow_html=True)
    st.markdown("<h5 style='color:#991b1b; margin-top:0;'>⚠️ System Actions</h5>", unsafe_allow_html=True)
    
    # 重置按钮
    st.markdown('<div class="reset-btn-right">', unsafe_allow_html=True)
    if st.button("☢️ RESET SYSTEM / 清空记录"):
        st.session_state.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # [新增] 官网按钮
    st.markdown('<div class="web-btn-container">', unsafe_allow_html=True)
    st.link_button("🌐 Visit Web Portal / 进入官网", "http://ltexpo2023.5gnumultimedia.com", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)



# --- 左侧主对话区域 ---
with col_main:
    # 比赛通告栏
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
                    response = requests.post(
                        API_URL, 
                        json={"question": prompt},
                        verify=False,  # 禁用 SSL 验证
                        timeout=30  # 设置超时
                    )
                    
                    if response.status_code == 200:
                        text = response.json().get("text", "无回应")
                        placeholder.write(text)
                        st.session_state.messages.append({"role": "assistant", "content": text})
                    else:
                        error_msg = f"❌ API Error {response.status_code}"
                        placeholder.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        
                except requests.exceptions.Timeout:
                    error_msg = "⏱️ 连接超时,请稍后重试"
                    placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                except Exception as e:
                    error_msg = f"🔌 连接失败: {str(e)[:100]}"
                    placeholder.error(error_msg)
                    st.session_st


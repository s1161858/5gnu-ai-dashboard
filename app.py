import streamlit as st
import requests
from PIL import Image
import os

# === 1. 页面基础配置 ===
st.set_page_config(
    page_title="5Gnu AI Drone Center",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === 2. 全局 CSS 样式表 (包含科技感侧边栏 & 通告栏样式) ===
st.markdown("""
<style>
    /* --- 全局背景设置 --- */
    .stApp {
        background-color: #f8fafc; /* 极淡的灰蓝色背景，护眼且专业 */
    }
    
    /* --- 侧边栏美化 (科技深蓝风格) --- */
    [data-testid="stSidebar"] {
        background-color: #0f172a; /* 深邃夜空蓝 */
        border-right: 1px solid #1e293b;
    }
    
    /* 侧边栏文字颜色强制变白 */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* 侧边栏输入组件美化 */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #334155;
        color: white;
        border: 1px solid #475569;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: #60a5fa;
        color: #60a5fa;
    }
    
    /* --- 状态指示灯动画 --- */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #10b981; /* 荧光绿 */
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }

    /* --- 侧边栏仪表盘数据框 --- */
    .metric-box {
        background: rgba(255,255,255,0.05);
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid #3b82f6;
    }
    .metric-value {
        font-size: 1.2em;
        font-weight: bold;
        color: #60a5fa;
    }
    .metric-label {
        font-size: 0.8em;
        color: #94a3b8;
    }

    /* --- 主区域卡片通用样式 --- */
    .css-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #e2e8f0;
    }

    /* 标题样式 */
    .header-title {
        font-family: 'Helvetica Neue', sans-serif;
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 5px;
    }

    /* 聊天气泡优化 */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        padding: 10px;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #eff6ff; /* 用户气泡淡蓝 */
    }
    
    /* 状态Badge */
    .status-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# === 3. 侧边栏 (Mission Control Center) ===
with st.sidebar:
    # --- LOGO 区域 ---
    try:
        # 尝试加载 Logo，如果找不到文件则显示文字 Logo
        if os.path.exists("Logo抠图版.png"):
            image = Image.open("Logo抠图版.png")
            st.image(image, use_container_width=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 10px 0;'>
                <h1 style='color: #60a5fa; margin:0; font-size: 2.5rem;'>5Gnu</h1>
                <p style='color: #94a3b8; margin:0; letter-spacing: 2px;'>AI SYSTEM</p>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Logo Error: {e}")

    st.markdown("---")

    # --- 模块 1: 系统模式选择 ---
    st.markdown("### 🎛️ Operation Mode (模式)")
    
    # 使用 Radio 组件模拟系统切换
    app_mode = st.radio(
        "Select AI Protocol:",
        ["🏆 Bett 2026 Strategy", "🎓 AOPA Exam Prep", "🚁 Drone Tech Support"],
        label_visibility="collapsed"
    )

    # 模式反馈提示
    if app_mode == "🏆 Bett 2026 Strategy":
        st.info("💡 **Active:** Sky & Earth Tournament Data Loaded.")
    elif app_mode == "🎓 AOPA Exam Prep":
        st.success("📚 **Active:** EDB Syllabus & Exam Bank Loaded.")
    
    st.markdown("---")

    # --- 模块 2: 实时遥测数据 (Mock Data) ---
    st.markdown("### 📡 Telemetry (实时遥测)")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Signal (5G)</div>
            <div class="metric-value">📶 -42dB</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">System Latency</div>
            <div class="metric-value">⚡ 12ms</div>
        </div>
        """, unsafe_allow_html=True)

    # 系统在线状态指示
    st.markdown("""
    <div style='background: rgba(16, 185, 129, 0.1); padding: 10px; border-radius: 5px; margin-top: 10px; border: 1px solid rgba(16, 185, 129, 0.3);'>
        <div style="display:flex; align-items:center;">
            <span class="live-indicator"></span>
            <span style="color: #6ee7b7; font-weight: bold; font-size: 0.9em;">SYSTEM ONLINE</span>
        </div>
        <div style="font-size: 0.75em; color: #94a3b8; margin-top: 5px;">
            Flowise Agent: <strong>Connected</strong><br>
            Vector DB: <strong>Synced</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 模块 3: 底部功能区 ---
    st.markdown("### ⚙️ Actions")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Reset", use_container_width=True, help="清空聊天记录并重启"):
            st.session_state.clear()
            st.rerun()
    with col_btn2:
        st.link_button("🌐 Web", "http://ltexpo2023.5gnumultimedia.com", use_container_width=True)

    # 底部版本信息
    st.markdown("""
    <div style='text-align: center; margin-top: 20px; color: #475569; font-size: 0.8em;'>
        5Gnu AI Console v2.4.0<br>Powered by AOPA LAE
    </div>
    """, unsafe_allow_html=True)


# === 4. 主界面逻辑 ===

# 标题区
col_title, col_logo_placeholder = st.columns([4, 1])
with col_title:
    st.markdown("<h1 class='header-title'>Drone AI Tutor Dashboard</h1>", unsafe_allow_html=True)
    st.caption("AOPA LAE School Center | 智能教学辅助系统 | Low Altitude Economy")

# 定义两栏布局：左侧聊天 (70%)，右侧信息面板 (30%)
col_main, col_info = st.columns([7, 3])

# --- 右侧信息面板 (Static Info Panel) ---
with col_info:
    st.markdown("""
    <div class="css-card">
        <h3>📊 任务参数 (Mission Params)</h3>
        <p><strong>Mode:</strong> AI Auto-Pilot</p>
        <p><strong>Drone:</strong> 5Gnu-X200</p>
        <p><strong>Alt Limit:</strong> 100m</p>
        <hr>
        <p style="color:#ef4444; font-size:0.8rem; font-weight:bold;">⚠️ Safety Check: Active</p>
    </div>
    
    <div class="css-card">
        <h3>📝 快捷指令</h3>
        <ul style="padding-left: 20px; color: #334155;">
            <li>介绍天地足球 (Sky & Earth)</li>
            <li>Bett 2026 有什么亮点？</li>
            <li>如何考取 AOPA 证书</li>
            <li>生成无人机编队代码</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 左侧主对话区域 (Chat Interface) ---
with col_main:
    # [新增] 🏆 比赛高亮通告栏 (Event Banner)
    st.markdown("""
    <div class="css-card" style="border-left: 5px solid #f59e0b; background-color: #fffbeb;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <h3 style="color: #b45309; margin: 0;">🏆 Upcoming: Bett 2026 & Sky & Earth Soccer</h3>
            <span class="status-badge" style="background-color:#fcd34d; color:#78350f;">Featured Event</span>
        </div>
        <p style="margin-top: 10px; color: #4b5563;">
            <strong>The Ultimate 5G LAE Showcase:</strong>
            Experience the fusion of <em>"Sky Soccer"</em> (Drone Soccer) and <em>"Earth Soccer"</em> (Robot Soccer).
        </p>
        <div style="background-color: rgba(255,255,255,0.6); padding: 10px; border-radius: 8px; font-size: 0.9em; border: 1px dashed #b45309; color: #b45309;">
            <strong>🚀 WOW Factor:</strong> A UK football star will use 5G technology to 
            <strong>remotely control robots in Hong Kong</strong> from the UK!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 任务输入框标题
    st.markdown('<div class="css-card" style="padding: 10px 20px; margin-bottom: 10px;"><h4>1. Mission Input & Strategy (任务输入)</h4></div>', unsafe_allow_html=True)
    
    # 聊天记录初始化
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "您好！我是 5Gnu 智能导师。关于 **Bett 2026**、**天地足球比赛** 或 **AOPA 考证**，请随时向我提问。"}
        ]

    # 聊天历史显示容器
    chat_container = st.container()
    
    # 底部输入框
    prompt = st.chat_input("在此输入您的飞行任务、考证问题或关于 Bett 2026 的咨询...")

    # 渲染历史消息
    with chat_container:
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    # 处理用户输入
    if prompt:
        # 显示用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user").write(prompt)

        # 调用 Flowise API
        # 注意：这里使用的是您提供的 API 地址
        API_URL = "https://cloud.flowiseai.com/api/v1/prediction/46e17ecb-9ace-46ce-91ed-f7332554b78c"
        
        with chat_container:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("🔄 **AI Analysis & Safety Check (正在分析策略)...**")
                
                try:
                    # 发送请求
                    response = requests.post(API_URL, json={"question": prompt})
                    if response.status_code == 200:
                        ai_reply = response.json().get("text", "Error: No text returned")
                    else:
                        ai_reply = f"Server Error: {response.status_code}"
                except Exception as e:
                    ai_reply = f"Connection Failed: {e}"
                
                # 更新显示并保存历史
                message_placeholder.write(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})


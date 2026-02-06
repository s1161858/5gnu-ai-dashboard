import streamlit as st
import requests
from PIL import Image
import os

# === 1. 页面基础配置 ===
st.set_page_config(
    page_title="5Gnu AI Drone Center",
    page_icon="🚁",
    layout="wide", # 使用宽屏模式，更像仪表盘
    initial_sidebar_state="expanded"
)

# === 2. 高级自定义 CSS (复刻设计图风格) ===
st.markdown("""
<style>
    /* 全局背景色 - 模仿图中的淡米色/浅灰色背景 */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* 卡片通用样式 */
    .css-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #3B81F6; /* 模仿图中的蓝色侧边栏 */
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: white; /* 侧边栏文字变白 */
    }

    /* 标题样式 */
    .header-title {
        font-family: 'Helvetica Neue', sans-serif;
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 10px;
    }

    /* 聊天气泡优化 */
    .stChatMessage {
        background-color: #f8fafc;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #eff6ff; /* 用户气泡淡蓝 */
    }

    /* 状态指示灯 */
    .status-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .status-ok { background-color: #dcfce7; color: #166534; border: 1px solid #166534; }
    .status-wait { background-color: #fef9c3; color: #854d0e; border: 1px solid #854d0e; }
</style>
""", unsafe_allow_html=True)

# === 3. 侧边栏 (Branding & Status) ===
with st.sidebar:
    # 尝试加载本地 Logo
    try:
        if os.path.exists("Logo抠图版.png"):
            image = Image.open("Logo抠图版.png")
            st.image(image, width=200)
        else:
            st.warning("⚠️ 未找到 'Logo抠图版.png'，请确认文件位置。")
            st.title("5Gnu AI") # 如果没图显示文字
    except Exception as e:
        st.error(f"Logo 加载失败: {e}")

    st.markdown("### 🚁 5Gnu Drone System")
    st.markdown("---")
    
    # 模拟图中的状态检查
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;'>
        <div class='status-badge status-ok'>✅ EDB Data Synced</div>
        <p style='font-size: 0.8rem; margin: 0;'>教育部数据已同步</p>
        <br>
        <div class='status-badge status-ok'>✅ Agent 1 Ready</div>
        <p style='font-size: 0.8rem; margin: 0;'>策略专家就绪</p>
        <br>
        <div class='status-badge status-wait'>🔄 Connecting to Flowise...</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🛠️ 控制面板")
    st.button("清除历史记录", on_click=lambda: st.session_state.clear(), use_container_width=True)

# === 4. 主界面逻辑 ===

# 标题区
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.markdown("<h1 class='header-title'>Drone AI Tutor Dashboard</h1>", unsafe_allow_html=True)
    st.caption("AOPA LAE School Center | 智能教学辅助系统")

# 定义两栏布局：左边是主对话，右边是信息面板（模仿你的图）
col_main, col_info = st.columns([7, 3])

# --- 右侧信息面板 (静态展示或辅助信息) ---
with col_info:
    st.markdown("""
    <div class="css-card">
        <h3>📊 任务参数 (Mission Params)</h3>
        <p><strong>Mode:</strong> AI Auto-Pilot</p>
        <p><strong>Drone:</strong> 5Gnu-X200</p>
        <p><strong>Alt Limit:</strong> 100m</p>
        <hr>
        <p style="color:red; font-size:0.8rem;">⚠️ Safety Check: Active</p>
    </div>
    
    <div class="css-card">
        <h3>📝 快捷指令</h3>
        <ul>
            <li>介绍无人机足球</li>
            <li>如何考取 AOPA 证书</li>
            <li>生成飞行路径代码</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 左侧主对话区域 ---
with col_main:
    # 1. 顶部：任务输入框 (模仿图中 "Mission Input")
    st.markdown('<div class="css-card" style="padding-bottom: 0px;"><h4>1. Mission Input & Strategy (任务输入)</h4></div>', unsafe_allow_html=True)
    
    # 聊天记录初始化
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "您好！我是 5Gnu 智能导师。准备好开始今天的无人机课程任务了吗？您可以输入任务指令，例如：**'帮我规划一个穿越障碍的飞行路径'**。"}
        ]

    # 聊天历史显示容器
    chat_container = st.container()
    
    # 输入框 (放在底部或顶部皆可，Streamlit默认在底部，这里用 chat_input)
    prompt = st.chat_input("在此输入您的飞行任务或问题...")

    with chat_container:
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    # 处理逻辑
    if prompt:
        # 显示用户输入
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user").write(prompt)

        # 调用 API
        API_URL = "https://cloud.flowiseai.com/api/v1/prediction/46e17ecb-9ace-46ce-91ed-f7332554b78c"
        
        with chat_container:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("🔄 **AI Analysis & Safety Check (正在分析策略)...**")
                
                try:
                    response = requests.post(API_URL, json={"question": prompt})
                    if response.status_code == 200:
                        ai_reply = response.json().get("text", "Error: No text returned")
                    else:
                        ai_reply = f"Error: {response.status_code}"
                except Exception as e:
                    ai_reply = f"Connection Failed: {e}"
                
                # 最终显示回答
                message_placeholder.write(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})


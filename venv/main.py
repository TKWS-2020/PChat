import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain.callbacks import StreamlitCallbackHandler
from PIL import Image as image
import os

cwd = os.getcwd()
img = image.open(cwd + "/venv/static/donpenprof03.png")

def init_page():
    st.set_page_config(
        page_title="PPIH ChatGPT"
    )
    # Markdownで画像とテキストを埋め込む
    st.markdown(
        """S
    <h1>
        <img src="./app/static/donpenProf03.png" alt="header image" width="50">
        PPIHサービスチャット
    </h1>
    """,
    unsafe_allow_html=True
    )
    st.sidebar.title("Options")

def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="丁寧に詳細に回答してください。")
        ]
        st.session_state.costs = []


def select_model():
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo"
    else:
        model_name = "gpt-4"

    # サイドバーにスライダーを追加し、temperatureを0から2までの範囲で選択可能にする
    # 初期値は0.0、刻み幅は0.1とする
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
    return ChatOpenAI(temperature=temperature, model_name=model_name, streaming=True)


def main():
    init_page()

    llm = select_model()
    init_messages()

    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)

    # ユーザーの入力を監視
    user_input = st.chat_input("聞きたいことを入力してね！")
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.chat_message("user").markdown(user_input)
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = llm(messages, callbacks=[st_callback])
        st.session_state.messages.append(AIMessage(content=response.content))

if __name__ == '__main__':
    main()
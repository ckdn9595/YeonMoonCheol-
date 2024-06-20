import os
from openai import OpenAI
import streamlit as st
from utils.session_state import initialize_session_state
from utils.styles import apply_styles

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# 세션 상태 초기화
initialize_session_state()

# 전역 스타일 설정
apply_styles()

# Load the appropriate step module
if st.session_state.step == 1:
    from views.first_input_names import display_page1
    display_page1()
elif st.session_state.step == 2:
    from views.second_input_chat import display_page2
    display_page2()

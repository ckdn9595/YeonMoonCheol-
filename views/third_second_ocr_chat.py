import streamlit as st
from PIL import Image
import os
from openai import OpenAI
import streamlit.components.v1 as components

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def file_uploader():
    uploaded_files = st.file_uploader(
        "대화 내용 사진을 업로드해주세요!", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    if uploaded_files is not None:
        st.session_state.ocr_input = uploaded_files
    else:
        st.session_state.uploaded_files = []
        st.session_state.ocr_result = []


def ocr_page_button():
    if st.button('대화 내용 추출하기'):
        with st.spinner("추출 중.."):
            st.session_state.step = 3.3
            st.rerun()


def display_page3_2():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    file_uploader()

    if st.session_state.ocr_input:
        ocr_page_button()

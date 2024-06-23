import cv2
from PIL import Image, ImageDraw
import base64
import streamlit as st
import io
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)



def file_uploader():
    uploaded_files = st.file_uploader("대화 내용 사진을 업로드해주세요!()", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    if uploaded_files is not None:
        pil_images = []
        encoded_images = []
        for uploaded_file in uploaded_files:
            pil_image = Image.open(uploaded_file)
            pil_images.append(pil_image)
            buffered = io.BytesIO()
            pil_image.save(buffered, format="PNG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            encoded_images.append(encoded_image)
            st.session_state.ocr_input.append(encoded_images)
    

def ocr_page_button():
    if st.button('대화 내용 추출하기'):
        with st.spinner("추출 중.."):
            st.session_state.step = 3.3
            st.experimental_rerun()




def display_page3_2():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    st.write("사진의 우측 대화가 본인이 보낸 메시지로 인식됩니다!")
    file_uploader()
    
    if st.session_state.ocr_input:
        ocr_page_button()
    



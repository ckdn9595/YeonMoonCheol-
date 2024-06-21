import streamlit as st
from PIL import Image
import os
import re
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)



def ocr_prompting(image_url):
    ## open api 사용 시 주석 풀기
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #     {
    #       "role": "user",
    #       "content": [
    #         {"type": "text", "text": "What’s in this image?"},
    #         {
    #           "type": "image_url",
    #           "image_url": {
    #             "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
    #           },
    #         },
    #       ],
    #     }
    #   ],
    #     model="gpt-4o",
    # )
    # result = chat_completion.choices[0].message.content
    result = "예시용 ocr 문구입니다.."
    st.session_state.ocr_result.append(result)
    return result

def file_uploader():
    uploaded_files = st.file_uploader("대화 내용 사진을 업로드해주세요!", accept_multiple_files=True)
    if uploaded_files is not None:
        st.session_state.uploaded_files = uploaded_files
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            ocr_prompting(image)
            st.image(image, caption=uploaded_file.name)
            
    else:
        st.session_state.uploaded_files = []


def reset_button():
    col1, col2, col3 = st.columns([8, 2, 3])
    with col3:
        if st.button('🗑️ 대화 사진 초기화'):
            st.session_state.uploaded_files = []
            st.session_state.ocr_result = []
            st.session_state.person1 = ""
            st.session_state.person2 = ""


def extract_name(chat_message):
    name_part = chat_message.split(':')[0]
    name = name_part.split('채팅')[-1].strip()
    return name


def remove_pattern(text):
    pattern = r'\d+번째 채팅\s+\S+\s+:'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def verify_button():
    if st.button('검증 하기'):
        if 'uploaded_files' in st.session_state and st.session_state.uploaded_files:
            with st.spinner("사건 정리중.."):
                ocr_results = ocr_prompting(st.session_state.uploaded_files)
                st.session_state.summary_data = summary_prompting(ocr_results)
                st.session_state.step = 4





def summary_prompting(data):
    data_string = ", ".join(data)
    ## open api 사용 시 주석 풀기
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": f"{data_string}",
    #         },
    #         {
    #             "role": "system",
    #             "content": """
    #                 입력된 데이터는 ([순서]번째 채팅 [주체] : [주체가 전송한 문자내용]) 형식이야.
    #                 대화에는 두 명의 주체가 있는데, 이 둘은 커플이야.
    #                 위 커플의 대화를 읽고, 잘못한 상황들을 예시와 같이 객관적으로!! 요약해줘.
    #                 중요: 각 요약이 문장의 글자 수가 30글자를 넘기지 말 것.
    #                 예시: "여자가 남자의 휴대폰을 마음대로 가져가서 검사했습니다.
    #                 """,
    #         }
    #     ],
    #     model="gpt-4o",
    # )
    # result = chat_completion.choices[0].message.content
    result = "예시용 문자 데이터"
    return result


def display_page3_2():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    file_uploader()

    if st.session_state.ocr_result:
        ocr_result_html = '<div class="conversation-container">'
        for idx, ocr_result in enumerate(st.session_state.ocr_result, start=1):
            clean_ocr_result = remove_pattern(ocr_result)
            name = extract_name(ocr_result)
            person_class = "person1" if st.session_state.person1 in ocr_result else "person2"
            ocr_result_html += f'<div class="profile {person_class}">{name}</div>'
            ocr_result_html += f'<div class="fixed-width-auto-height {person_class}">{clean_ocr_result}</div>'
        ocr_result_html += '</div>'
        st.markdown(ocr_result_html, unsafe_allow_html=True)
    else:
        st.warning("입력값이 없습니다")
        
    # reset_button()

    verify_button()


st.markdown( (
    """
    <style>
        
    </style>
    """
), unsafe_allow_html=True)

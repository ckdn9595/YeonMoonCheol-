import streamlit as st
from PIL import Image
import os
import re
from openai import OpenAI
import streamlit.components.v1 as components

def extract_name(chat_message):
    name_part = chat_message.split(':')[0]
    name = name_part.split('채팅')[-1].strip()
    return name

def remove_pattern(text):
    pattern = r'\d+번째 채팅\s+\S+\s+:'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def ocr_prompting(img_url):
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
    st.session_state.conversations.append(result)
    return result



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


def verify_button():
    if st.button('검증 하기'):
        with st.spinner("사건 정리중.."):
            st.session_state.summary_data = summary_prompting(st.session_state.conversations)
            st.session_state.step = 4
            st.experimental_rerun()
                


def display_page3_3():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    
    
    if st.session_state.ocr_input:
        ocr_prompting(st.session_state.ocr_input)
        # 세션 상태 출력
        # st.write("현재 세션 상태:")
        # st.json(st.session_state)
        with st.container(height=500, border=True):
            for idx, conversation in enumerate(st.session_state.conversations, start=1):
                clean_conversation = remove_pattern(conversation)
                name = extract_name(conversation)
                person_class = "person1" if st.session_state.person1 in conversation else "person2"
                cols = st.columns([1, 8, 1])
                with cols[0]:
                    if st.session_state.get('edit_mode', False):
                        selected = st.checkbox("", key=f"checkbox_{idx}")
                        if selected:
                            st.session_state.selected_conversations.append(idx)
                        else:
                            if idx in st.session_state.selected_conversations:
                                st.session_state.selected_conversations.remove(
                                    idx)
                with cols[1]:

                    st.markdown(

                        f'''
                            <div class="{person_class}_container">
                                <div>
                                    <div class="profile{person_class}">{name}</div>
                                    <div class="fixed-width-auto-height {person_class}">{clean_conversation}</div>
                                </div>
                            </div>
                        ''',
                        unsafe_allow_html=True
                    )
    else:
        st.warning("입력값이 없습니다")

        
    verify_button()
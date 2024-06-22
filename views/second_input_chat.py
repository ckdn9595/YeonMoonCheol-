import streamlit as st
import re
import os
from openai import OpenAI
import streamlit.components.v1 as components

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False


# def ui_reset_button():
#     col1, col2, col3 = st.columns([8, 2, 3])
#     with col3:
#         if st.button('🗑️ 대화 내용 초기화'):
#             st.session_state.inputs = {"text": "", "type": ""}
#             st.session_state.conversations = []
#             st.session_state.step = 1
#             st.session_state.person1 = ""
#             st.session_state.person2 = ""


def ui_edit_button():
    col1, col2, col3 = st.columns([8, 2, 3])
    with col3:
        if st.session_state.get('edit_mode', False):
            if st.button('편집 취소'):
                st.session_state.edit_mode = not st.session_state.get(
                    'edit_mode', False)
                st.rerun()
        else :
            if st.button('🗑️ 대화 내용 편집'):
                st.session_state.edit_mode = not st.session_state.get(
                    'edit_mode', False)
                st.rerun()

def extract_name(chat_message):
    name_part = chat_message.split(':')[0]
    name = name_part.split('채팅')[-1].strip()
    return name


def remove_pattern(text):
    pattern = r'\d+번째 채팅\s+\S+\s+:'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def ui_verify_button():
    # 버튼 생성
    if st.button('검증 하기'):
        with st.spinner("사건 정리중.."):
            st.session_state.summary_data = summary_prompting(
                st.session_state.conversations)
            st.session_state.step = 4


def summary_prompting(data):
    data_string = ", ".join(data)
    # open api 사용 시 주석 풀기
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


def set_checkbox_evt():
    html_code = """
            <script>
            console.log('ss')
            function deleteCheckedConversations() {
               let checkboxes = parent.document.querySelectorAll('input[type="checkbox"]');
                checkboxes.forEach((checkbox, index) => {
                    if (checkbox.checked) {
                        parent.document.querySelector('#' + checkbox.id).parentElement.previousElementSibling.remove()
                        parent.document.querySelector('#' + checkbox.id).parentElement.remove()
                    }
                });
                parent.document.querySelector('button[data-testid="baseButton-secondary"]').click();
            }
            </script>
            """
    html_code += """<button style="
                    background-color: #FFFFFF;
                    color: #FF0056;
                    border-radius: 12px;
                    border: solid 0.5px #FF0056;
                    padding: 5px 10px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    cursor: pointer;
                    width: auto;
                    padding: 0.6rem;
                    margin: 0 auto;
                    display: block;
                " onclick="deleteCheckedConversations()">선택한 대화 삭제</button>
                <style>
                body {
                    margin:0
                }
                </style>
            """
    return html_code


def display_page2():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    input_field = st.session_state.inputs
    with st.form(key='input_form'):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            input_field["type"] = st.radio(
                "사람 선택", [st.session_state.person1, st.session_state.person2], key="type")
            input_field["text"] = st.text_input("대화 입력", key="text")
            col1, col2, col3 = st.columns([2.125, 4, 1])
            with col2:
                submitted = st.form_submit_button(label='대화 추가하기')
            if submitted:
                if input_field["text"]:
                    idx = len(st.session_state.conversations) + 1
                    st.session_state.conversations.append(
                        f"{idx}번째 채팅 {input_field['type']} : {input_field['text']}")
                    st.session_state.inputs = {"text": "", "type": ""}
                    st.experimental_rerun()
                else:
                    st.warning("입력된 대화가 없습니다. 대화를 입력해주세요.")

    # ui_reset_button()
    ui_edit_button()
    print(st.session_state.conversations)
    if st.session_state.conversations:
        conversation_html = '<div class="conversation-container">'
        for idx, conversation in enumerate(st.session_state.conversations, start=1):
            clean_conversation = remove_pattern(conversation)
            name = extract_name(conversation)
            person_class = "person1" if st.session_state.person1 in conversation else "person2"
            conversation_html += f'<div class="profile{person_class}">{name}</div>'
            conversation_html += f'<div class="fixed-width-auto-height {person_class}">'
            if st.session_state.get('edit_mode', False):
                conversation_html += f'<input type="checkbox" id="conv_{idx}" name="conv_{idx}"  value="1"> '
            conversation_html += f'{clean_conversation}</div>'
        conversation_html += '</div>'
        st.markdown(conversation_html, unsafe_allow_html=True)
        if st.session_state.get('edit_mode', False):
            components.html(set_checkbox_evt(), height=60)
            
    else:
        st.warning("입력값이 없습니다")

    # 편집 버튼 클릭 시 삭제 버튼으로 바껴야함
    if not st.session_state.get('edit_mode', False):
        ui_verify_button()

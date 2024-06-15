import os
from openai import OpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# 세션 상태 변수 초기화
if 'inputs' not in st.session_state:
    st.session_state.inputs = [{"text": "", "type": ""}]

if 'conversations' not in st.session_state:
    st.session_state.conversations = []

if 'step' not in st.session_state:
    st.session_state.step = 1

if 'person1' not in st.session_state:
    st.session_state.person1 = ""

if 'person2' not in st.session_state:
    st.session_state.person2 = ""

# if 'summary_data' not in st.session_state:
#     st.session_state.summary_data = ""
# 1화면
# 새로운 입력 필드를 추가하는 함수


def add_input():
    if 'inputs' not in st.session_state:
        st.session_state.inputs = [{"text": "", "type": ""}]
    else:
        st.session_state.inputs = [{"text": "", "type": ""}]


# 오른쪽 상단에 UI 초기화 버튼 추가
def ui_reset_button():
    col1, col2, col3 = st.columns([8, 2, 3])
    with col2:
        if st.button('검증하기'):
            print(st.session_state.conversations)
            st.session_state.step = 3

            # 여기에 사건 프로프팅 들어가야함 곧 여기서 데이터 세팅
    with col3:
        if st.button('🗑️ 대화 내용 초기화'):
            st.session_state.inputs = [{"text": "", "type": ""}]
            st.session_state.conversations = []
            st.session_state.step = 1  # Reset names_set as well
            st.session_state.person1 = ""
            st.session_state.person2 = ""
            st.experimental_rerun()  # 페이지 새로고침


def summary_prompting(data):
    data_string = ", ".join(data)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{data_string}",
            },
            {
                "role": "system",
                "content": """
                    입력된 데이터는 ([순서]번째 채팅 [주체] : [주체가 전송한 문자내용]) 형식이야.
                    대화에는 두 명의 주체가 있는데, 이 둘은 커플이야.
                    위 커플의 대화를 읽고, 잘못한 상황들을 예시와 같이 객관적으로!! 요약해줘.
                    중요: 각 요약이 문장의 글자 수가 30글자를 넘기지 말 것.
                    예시: "여자가 남자의 휴대폰을 마음대로 가져가서 검사했습니다.
                    """,
            }
        ],
        model="gpt-4o",
    )
    result = chat_completion.choices[0].message.content
    return result


def create_true_array(size):
    return [True] * size


# Google Fonts 나눔 명조 적용
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo&display=swap');
    h1 {
        font-family: 'Nanum Myeongjo', serif;
        color: #FF0056;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# Streamlit 앱 레이아웃
# SVG 이미지 표시
with open("./assets/logo.svg", "r") as f:
    svg_content = f.read()
st.markdown(f'<div style="margin-left: 10%; margin-bottom:5%;"align="center">{svg_content}</div>', unsafe_allow_html=True)

st.write("")
st.write("")
# 첫 번째 입력 필드 추가 (처음 한 번만 실행)
if len(st.session_state.inputs) == 0:
    add_input()

# 이름이 설정된 경우와 그렇지 않은 경우에 따라 다른 UI 표시
if st.session_state.step == 1:
    # 상단에서 첫 번째 사람과 두 번째 사람 이름 입력받기
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        person1_name = st.text_input("남자 피의자", key="person1_input")
        person2_name = st.text_input("여자 피의자", key="person2_input")

        # '판결 시작하기' 버튼 추가
        col1, col2, col3 = st.columns([1.75, 2, 1.5])
        with col2:
            if st.button('판결 시작하기'):
                if person1_name and person2_name:
                    st.session_state.step = 2
                    st.session_state.person1 = person1_name
                    st.session_state.person2 = person2_name
                    st.experimental_rerun()
                else:
                    st.warning("두 사람의 이름을 입력해주세요.")
elif st.session_state.step == 2:

    # 이름이 설정된 경우에만 대화 입력 UI 표시
    # 현재 입력 필드
    input_field = st.session_state.inputs[0]

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
                if input_field["text"]:  # 입력된 텍스트가 있을 경우에만 추가
                    idx = len(st.session_state.conversations) + 1
                    st.session_state.conversations.append(
                        f"{idx}번째 채팅 {input_field['type']} : {input_field['text']}")
                    st.session_state.inputs[0] = {"text": "", "type": ""}
                    st.experimental_rerun()  # 페이지 새로고침
                else:
                    st.warning("입력된 대화가 없습니다. 대화를 입력해주세요.")

    # 저장된 대화 목록 표시
    if st.session_state.conversations:
        conversation_html = '<div class="conversation-container">'
        for idx, conversation in enumerate(st.session_state.conversations, start=1):
            person_class = "person1" if st.session_state.person1 in conversation else "person2"
            conversation_html += f'<div class="fixed-width-auto-height {person_class}">{conversation}</div>'
        conversation_html += '</div>'
        st.markdown(conversation_html, unsafe_allow_html=True)
    else:
        st.warning("입력값이 없습니다")
        


    # UI 초기화 버튼
    ui_reset_button()

elif st.session_state.step == 3:
    with st.spinner("사건 정리중.."):
        st.session_state.summary_data = summary_prompting(
            st.session_state.conversations)
    # 줄 바꿈을 기준으로 문자열을 분리하여 배열로 저장
    sentences = st.session_state.summary_data.split('\n')
    print(sentences)
    agree = create_true_array(len(sentences))
    # datas = ["A가 저번 커플 모임 술자리에서 실수를 함",
    #          "B가 A에게 다음은 같은 실수를 하지 않도록 약속받음", "A가 다시 실수를 함", "머라고하느냐"]
    # agree = [True, True, True, True]

    with st.container():
        head1, head2 = st.columns([4, 2])
        with head1:
            st.subheader("사건 정리")
        with head2:
            st.subheader("동의 여부")
    with st.container():
        blank, name1, name2 = st.columns([4, 1, 1])
        with blank:
            st.subheader("")
        with name1:
            st.write(st.session_state.person1)
        with name2:
            st.write(st.session_state.person2)

    for idx, data in enumerate(sentences):
        with st.container():
            col1, blank2, col2, col3 = st.columns(
                [8, 0.8, 2.2, 2])  # 두 개의 컬럼 생성, 비율 3:1
            with col1:
                st.markdown(
                    f'<div class="custom-container">{data}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="custom-checkbox">',
                            unsafe_allow_html=True)
                agree_a = st.checkbox("", key=f"a_agree_{idx}")
                st.markdown('</div>', unsafe_allow_html=True)
                if not agree_a:
                    agree[idx] = False
            with col3:
                st.markdown('<div class="custom-checkbox">',
                            unsafe_allow_html=True)
                agree_b = st.checkbox("", key=f"b_agree_{idx}")
                st.markdown('</div>', unsafe_allow_html=True)
                if not agree_b:
                    agree[idx] = False

    if st.button("검증 완료"):
        print(agree)
        for idx, data in enumerate(agree):
            if agree[idx]:
                print(sentences[idx])
                
                
                
# 스타일을 적용할 CSS 추가
st.markdown(
    """
    <style>
    .custom-container {
        background-color: #FFE6E6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }
    .custom-checkbox {
        display: flex;
        align-items: center;
        height: 100%;
        width: 100%;
        justify-content: center !important;
    }
    .stButton>button, .stForm button {
        background-color: #FFFFFF;
        color: #FF0056;
        border-radius: 12px;
        border: solid 0.5px #FF0056;
        padding: 5px 10px;  /* 패딩을 조절하여 버튼 크기를 내용물에 맞춤 */
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        cursor: pointer;
        width: auto;  /* 너비를 내용물에 맞춤 */
        height: auto; /* 높이를 내용물에 맞춤 */
    }
    .stButton>button:hover, .stForm button:hover {
        background-color: #FF0056;
        color : #FFFFFF;
    }
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo&display=swap');
    h1 {
        font-family: 'Nanum Myeongjo', serif;
        color: #FF0056;
        text-align: center;
    }
    .conversation-container {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .fixed-width-auto-height {
        width: 300px;
        height: auto;
        word-wrap: break-word;
        padding: 10px;
        margin-bottom: 5px;
        border-radius: 5px;
    }
    .person1 {
        background-color: lightblue;
    }
    .person2 {
        background-color: lightpink;
        align-self: flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import os
from openai import OpenAI
from datetime import date
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re

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
if 'verified_sentences' not in st.session_state:
    st.session_state.verified_sentences = []
if 'agree' not in st.session_state:
    st.session_state.agree = []

def extract_name(chat_message):
    name_part = chat_message.split(':')[0]
    name = name_part.split('채팅')[-1].strip()
    return name

def remove_pattern(text):
    pattern = r'\d+번째 채팅\s+\S+\s+:'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def add_input():
    if 'inputs' not in st.session_state:
        st.session_state.inputs = [{"text": "", "type": ""}]
    else:
        st.session_state.inputs = [{"text": "", "type": ""}]

def ui_reset_button():
    col1, col2, col3 = st.columns([8, 2, 3])
    with col3:
        if st.button('🗑️ 대화 내용 초기화'):
            st.session_state.inputs = [{"text": "", "type": ""}]
            st.session_state.conversations = []
            st.session_state.step = 1
            st.session_state.person1 = ""
            st.session_state.person2 = ""



def ui_verify_button():
    # 버튼 생성
    if st.button('검증 하기'):
        print(st.session_state.conversations)
        with st.spinner("사건 정리중.."):
            st.session_state.summary_data = summary_prompting(
                st.session_state.conversations)
            st.session_state.step = 3



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
    .left-image, .right-image {
        position: fixed;
        width: 300px;
        height: 100%;
        top: 0;
        z-index: -1;
    }
    .left-image {
        left: 0;
    }
    .right-image {
        right: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Streamlit 앱 레이아웃
with open("./assets/logo.svg", "r") as f:
    svg_content = f.read()

st.markdown(f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True)


st.write("")
st.write("")

# 첫 번째 입력 필드 추가 (처음 한 번만 실행)
if len(st.session_state.inputs) == 0:
    add_input()

# 이름이 설정된 경우와 그렇지 않은 경우에 따라 다른 UI 표시
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        person1_name = st.text_input("남자 피의자", key="person1_input")
        person2_name = st.text_input("여자 피의자", key="person2_input")
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
                if input_field["text"]:
                    idx = len(st.session_state.conversations) + 1
                    st.session_state.conversations.append(
                        f"{idx}번째 채팅 {input_field['type']} : {input_field['text']}")
                    st.session_state.inputs[0] = {"text": "", "type": ""}
                    st.experimental_rerun()
                else:
                    st.warning("입력된 대화가 없습니다. 대화를 입력해주세요.")

    ui_reset_button()
    if st.session_state.conversations:
        conversation_html = '<div class="conversation-container">'
        for idx, conversation in enumerate(st.session_state.conversations, start=1):
            clean_conversation = remove_pattern(conversation)
            name = extract_name(conversation)
            person_class = "person1" if st.session_state.person1 in conversation else "person2"
            conversation_html += f'<div class="profile{person_class}">{name}</div>'
            conversation_html += f'<div class="fixed-width-auto-height {person_class}">{clean_conversation}</div>'
        conversation_html += '</div>'
        st.markdown(conversation_html, unsafe_allow_html=True)
    else:
        st.warning("입력값이 없습니다")


    ui_verify_button()

elif st.session_state.step == 3:
    sentences = st.session_state.summary_data.split('\n')
    if sentences and sentences[-1] == '':
        sentences.pop()

    st.session_state.agree = create_true_array(len(sentences))



    with st.container():
        head1, head2 = st.columns([4, 2])
        with head1:
            st.markdown(
                '<div class="centered-content"><h3>사건 정리</h3></div>',
                unsafe_allow_html=True
            )
        with head2:
            st.markdown(
                '<div class="centered-content"><h3>동의 여부</h3></div>',
                unsafe_allow_html=True
            )
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
            col1, blank2, col2, col3 = st.columns([8, 0.8, 2.2, 2])
            with col1:
                container_class = "custom-container highlight" if st.session_state.get(
                    f"a_agree_{idx}") and st.session_state.get(f"b_agree_{idx}") else "custom-container"
                st.markdown(
                    f'<div class="{container_class}">{data}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="custom-checkbox">',
                            unsafe_allow_html=True)
                agree_a = st.checkbox("", key=f"a_agree_{idx}")
                st.markdown('</div>', unsafe_allow_html=True)
                if not agree_a:
                    st.session_state.agree[idx] = False
            with col3:
                st.markdown('<div class="custom-checkbox">',
                            unsafe_allow_html=True)
                agree_b = st.checkbox("", key=f"b_agree_{idx}")
                st.markdown('</div>', unsafe_allow_html=True)
                if not agree_b:
                    st.session_state.agree[idx] = False

    if st.button("검증 완료"):
        for idx, data in enumerate(st.session_state.agree):
            if st.session_state.agree[idx]:
                st.session_state.verified_sentences.append(sentences[idx])
        st.session_state.step = 4

elif st.session_state.step == 4:
    verified_str = ", ".join(st.session_state.verified_sentences)

    st.write('본 판결서는 판결서 인터넷열람 사이트에서 열람/출력되었습니다. 본 판결서를 이용하여 사건관계인의 명예나 생활의 평온을 해하는 행위는 관련 법령에 따라 금지됩니다.')
    st.markdown("<h1 style='text-align: center;'>연 애 중 앙 지 방 법 원</h1>",
                unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'></h2>",
                unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'></h2>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>판           결</h3>",
                unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'></h2>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.write("사    건")
    with col2:
        st.write("2024고정999 연애교통법위반(연인갈등)")

    with col1:
        st.write("피 고 인")
    with col2:
        st.write(f"{st.session_state.person1}, {st.session_state.person2}")

    with col1:
        st.write("검    사")
    with col2:
        st.write("연문철(검사직무대리, 기소)\n연명원(공판)")

    with col1:
        st.write("변 호 인")
    with col2:
        st.write("법무법인(연애의 참견) 담당변호사 연문철")

    with col1:
        st.write("판결선고")
    with col2:
        today = date.today()
        today_str = today.strftime("%Y-%m-%d")
        st.write(today_str)

    st.write("  ")
    st.write("  ")


    response_reason = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"{verified_str}"
            },
            {
                "role": "system",
                "content": "입력 받은 내용에 대한 연애전문가로서, 남자와 여자의 싸움의 판결문을 원만히 화해가 되도록 300자 이내로 작성해줘"
            }
        ]
    )

    st.write("  ")
    st.write("  ")

    st.markdown("<h3 style='text-align: center;'>이           유</h3>",
                unsafe_allow_html=True)

    result_reason = response_reason.choices[0].message.content
    st.write(result_reason)

    st.write("  ")
    st.write("  ")
    st.write("  ")
    st.write("  ")


    num_male_mistakes = result_reason.count('남자')
    num_female_mistakes = result_reason.count('여자')

    total_characters = len(result_reason)

    percent_male_mistakes = (num_male_mistakes / total_characters) * 100
    percent_female_mistakes = (num_female_mistakes / total_characters) * 100




    sizes = [percent_male_mistakes, percent_female_mistakes]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)


    fig1, ax1 = plt.subplots(figsize=(2, 2))
    ax1.pie(sizes, explode=explode, labels=None, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 10})
    ax1.axis('equal')

    ax1.legend(labels=['Male', 'Female'], loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)
    
    st.subheader('판결 이유에 대한 남자와 여자의 잘못 비율 (%)')
    st.pyplot(fig1)

    st.markdown("<h3 style='text-align: center;'>결           론</h3>",
                unsafe_allow_html=True)

    response_instruction = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"{verified_str}"
            },
            {
                "role": "system",
                "content": "판결문에 대한 연인 사이의 간단하고 현실적으로 가능한 귀여운 벌칙을 3가지만 만들어주고, '피고인은' 으로 시작해서 '형에 처한다' 라는 양식에 맞게 작성해줘"
            }
        ]
    )
    result_instruction = response_instruction.choices[0].message.content
    st.write(result_instruction)

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
    .highlight {
        background-color: lightgreen !important;
    }
    .custom-checkbox {
        display: flex;
        align-items: center;
        height: 100%;
        width: 100%;
        justify-content: center !important;
    }
    .stCheckbox span {
        -webkit-transform: scale(1.3);
    }
    .stButton{
        display: flex;
        flex-wrap: nowrap;
        justify-content: space-around;
    }
    
    .stButton>button, .stForm button {
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
        height: auto;
    }
    .stButton>button:hover, .stForm button:hover {
        background-color: #FF0056;
        color: #FFFFFF;
    }
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo&display=swap');
    h1 {
        font-family: 'Nanum Myeongjo', serif;
        color: #FF0056;
        text-align: center;
    }
    .st-emotion-cache-ixecyn {
        border-radius: 1em;
        border: none;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .conversation-container {
        width: 100%;
        display: flex;
        margin-bottom: 5%;
        flex-direction: column;
        align-items: flex-start;
        background-color: #9bbbd4;
        padding: 1em;
        border-radius: 1em;
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
        background-color: #FEF01B;
    }
    .person2 {
        background-color: #FEF01B;
        align-self: flex-end;
    }
    .profileperson1 {
    }
    .profileperson2 {

        align-self: flex-end;
    }

    .profileperson1 {
    }
    .profileperson2 {
        align-self: flex-end;
    }
    .centered-content {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;  /* 컬럼의 높이를 맞추기 위해 필요할 수 있습니다 */
    }
    .st-emotion-cache-y2rhx3 {
        padding: 5px 0 0 0;
    }
    .element-container.st-emotion-cache-1aege4m button{
        margin-top: 2rem;
        width: 30% !important;

    }
    </style>
    """,
    unsafe_allow_html=True
)

import streamlit as st
import uuid
import socket
import db.database as db
from views.fifth_judgment import display_page5
import streamlit.components.v1 as components
from streamlit_js_eval import get_page_location


@st.experimental_dialog("연인에게 링크를 전달해주세요!")
def send_summary_dialog(link):
    html_code = f"""
    <div class="link-container">
        <div class="link-box">
            <a href="{link}" target="_blank">{link}</a>
        </div>
        <button class="copy-button" onclick="copyToClipboard('{link}')">Copy Link</button>
    </div>
    <script>
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            alert('링크가 클립보드에 복사되었습니다.');
        }}, function(err) {{
            console.error('클립보드 복사에 실패했습니다.', err);
        }});
    }}
    </script>
    <style>
    .link-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 20px;
    }}
    .link-box {{
        padding: 10px;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        border-radius: 5px;
        width: fit-content;
        margin-bottom: 10px;
        font-size: 1.1em;
    }}
    .copy-button {{
        background-color: #FFFFFF;
        color: #FF0056;
        border-radius: 12px;
        border: solid 0.5px #FF0056;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }}
    </style>
    """
    # Streamlit 애플리케이션에 HTML 삽입
    components.html(html_code, height=180)
    # 추가 설명
    st.write("해당 링크를 통해 연인의 동의 여부를 체크 후 판결이 내려집니다.")


def get_server_url(uuid):
    try:

        # 배포시 url
        deploy_url = "https://yeonmooncheolai.streamlit.app"
        # 로컬 url
        local_url = "http://localhost:8501"
        return f"{local_url}/?casenum={uuid}"
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def boolean_str(bool_array):
    result = ','.join(['T' if value else 'F' for value in bool_array])
    return result


def create_true_array(size):
    return [True] * size


def display_page4_2():

    cur = db.init()

    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    #st.session_state.summary_data = "여자는 남자에게 욕을 했다.\n 남자가 화가 나서 주먹을 휘둘렀다."
    sentences = st.session_state.summary_data.split('\n')
    if sentences and sentences[-1] == '':
        sentences.pop()

    st.session_state.agree = create_true_array(len(sentences))

    with st.container():
        head1, head2 = st.columns([5, 1])
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
        st.write("")
        st.write("두 사람 모두 동의한 사실만 판결에 넘어가요.")
    with st.container():
        blank, name1 = st.columns([5, 1])
        with blank:
            st.write("")

    for idx, data in enumerate(sentences):
        with st.container():
            col1, blank2, col2 = st.columns([9.5, 2, 1.5])
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

    if st.button("검증 완료"):
        if not any(st.session_state.agree):
            st.toast("적어도 하나의 사건은 선택을 해야합니다.", icon="🚨")
        else:
            if st.session_state.case_num_uid:
                link_url = get_server_url(st.session_state.case_num_uid)
                send_summary_dialog(link_url)
                print("이미 생성했으니까 생성한거 보여줬다.")
            else:
                uuid4 = uuid.uuid4()

                # 먼저 데이터베이스를 설계한다. 판결문은 매번 새로 만든다.
                # uuid, sentences, agreeList, person1, person2

                # 데이터베이스에 값을 알맞게 넣어준다.
                db.insert(str(uuid4), st.session_state.summary_data, boolean_str(
                    st.session_state.agree), st.session_state.person1, st.session_state.person2)
                link_url = get_server_url(uuid4)
                send_summary_dialog(link_url)
                st.session_state.case_num_uid = uuid4

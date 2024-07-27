import streamlit as st


def display_page1():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        receiver_name = st.text_input("남자 피의자", key="receiver_input")
        sender_name = st.text_input("여자 피의자", key="sender_input")
        col1, col2, col3 = st.columns([1.75, 2, 1.5])
        with col2:

            if st.button('판결 시작하기'):
                if receiver_name and sender_name:
                    st.session_state.step = 2
                    st.session_state.receiver = receiver_name
                    st.session_state.sender = sender_name
                    st.rerun()
                else:
                    st.warning("두 사람의 이름을 입력해주세요.")

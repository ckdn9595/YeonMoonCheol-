import streamlit as st


class LoginPage:
    def __init__(self):
        pass

    def display(self):
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
                        st.rerun()
                    else:
                        st.warning("두 사람의 이름을 입력해주세요.")


st.markdown(
    """
    <style>
        .st-emotion-cache-1f8d91x  {
            margin-top: 10%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

import streamlit as st


def display_page1():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<p style="font-size : 1em; font-weight : 700; text-align: center;"> 연문철 새로운 버전이 출시됐습니다! <br/> 아래 링크 혹은 버튼을 눌러 이동해주세요!</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center;"><a href="https://yeonmuncheol.site/" target="_blank">https://yeonmuncheol.site/</a></p>', unsafe_allow_html=True)

    with col2:
        if st.button('정식 버전으로 이동하기'):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://yeonmuncheol.site/" />', unsafe_allow_html=True)

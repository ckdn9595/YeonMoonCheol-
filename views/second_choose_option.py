import streamlit as st

def display_page2():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([3,1,3]) 
    
    with col1:
        if st.button('대화 내용 사진 업로드'):
            st.session_state.step = 3.2  #이후 다른 step으로 이동 
            st.experimental_rerun()
            
    with col3:
        if st.button('대화 내용 직접 입력'):
            st.session_state.step = 3   
            st.experimental_rerun()


st.markdown(
    """
    <style>
        st-emotion-cache-13g0a2z ef3psqc12{
            padding : 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
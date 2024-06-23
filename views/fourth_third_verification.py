import streamlit as st


def create_true_array(size):
    return [True] * size

def parse_boolean_string(s):
    return [True if char == 'T' else False for char in s.split(',')]

def display_page4_3():
    param_agree_list = parse_boolean_string(st.session_state.param_agree_list)
    
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    
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
        blank, name1, name2 = st.columns([4, 1.1, 0.9])
        with blank:
            st.subheader("")
        with name1:
            st.write("연인")
        with name2:
            st.write("나")

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
                agree_a = st.checkbox(
                    "", key=f"a_agree_{idx}", value=param_agree_list[idx], disabled=True)
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
        if not any(st.session_state.agree):
            st.toast("적어도 하나의 사건은 선택을 해야합니다.", icon="🚨")
        else:
            for idx, data in enumerate(st.session_state.agree):
                if st.session_state.agree[idx]:
                    st.session_state.verified_sentences.append(sentences[idx])
            print(st.session_state.verified_sentences)
            st.session_state.step = 5
            st.rerun()
            

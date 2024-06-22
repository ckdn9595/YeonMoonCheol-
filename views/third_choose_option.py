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

    ui_reset_button()
    ui_edit_button()

    # 체크박스 상태 저장 및 HTML 생성
    if st.session_state.conversations:
        conversation_html = '<div class="conversation-container">'
        for idx, conversation in enumerate(st.session_state.conversations, start=1):
            clean_conversation = remove_pattern(conversation)
            name = extract_name(conversation)
            person_class = "person1" if st.session_state.person1 in conversation else "person2"
            conversation_html += f'<div class="profile{person_class}">{name}</div>'
            conversation_html += f'<div class="fixed-width-auto-height {person_class}">'
            if st.session_state.get('edit_mode', False):
                conversation_html += f'<input type="checkbox" id="conv_{idx}" name="conv_{idx}" value="1"> '
            conversation_html += f'{clean_conversation}</div>'
        conversation_html += '</div>'
        st.markdown(conversation_html, unsafe_allow_html=True)
    else:
        st.warning("입력값이 없습니다")

    # 선택한 대화 삭제 버튼
    if st.session_state.get('edit_mode', False):
        if st.button('선택한 대화 삭제'):
            # 체크된 체크박스를 추적하여 삭제
            checked_indices = [idx for idx in range(1, len(
                st.session_state.conversations) + 1) if st.session_state.get(f'conv_{idx}', False)]
            st.session_state.conversations = [conv for idx, conv in enumerate(
                st.session_state.conversations, start=1) if idx not in checked_indices]
            st.experimental_rerun()

    ui_verify_button()

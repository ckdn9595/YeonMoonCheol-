import streamlit as st


def initialize_session_state():
    # if 'inputs' not in st.session_state:
    #     st.session_state.inputs = {"text": "", "type": ""}

    if 'conversations' not in st.session_state:
        st.session_state.conversations = []

    if 'step' not in st.session_state:
        st.session_state.step = 1

    if 'person1' not in st.session_state:
        st.session_state.person1 = ""

    if 'sender' not in st.session_state:
        st.session_state.sender = ""

    if 'verified_sentences' not in st.session_state:
        st.session_state.verified_sentences = []

    if 'agree' not in st.session_state:
        st.session_state.agree = []

    if 'ocr_input' not in st.session_state:
        st.session_state.ocr_input = []

    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    if 'summary_data' not in st.session_state:
        st.session_state.summary_data = ""

    if 'case_num_uid' not in st.session_state:
        st.session_state.case_num_uid = ""

    if 'param_agree_list' not in st.session_state:
        st.session_state.param_agree_list = ""

    if 'sender' not in st.session_state:
        st.session_state.sender = ""

    if 'receiver' not in st.session_state:
        st.session_state.receiver = ""

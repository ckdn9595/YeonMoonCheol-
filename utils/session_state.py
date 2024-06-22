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

    if 'person2' not in st.session_state:
        st.session_state.person2 = ""

    if 'verified_sentences' not in st.session_state:
        st.session_state.verified_sentences = []

    if 'agree' not in st.session_state:
        st.session_state.agree = []

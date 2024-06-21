
import streamlit as st
from utils.session_state import initialize_session_state
from utils.styles import apply_styles
from views.first_input_names import display_page1
from views.second_choose_option import display_page2
from views.third_input_chat import display_page3
from views.third_second_ocr_chat import display_page3_2
from views.fourth_verification import display_page4
from views.fifth_judgment import display_page5



# 세션 상태 초기화
initialize_session_state()

# 전역 스타일 설정
apply_styles()

# Load the appropriate step module
if st.session_state.step == 1:
    display_page1()
elif st.session_state.step == 2:
    display_page2()
elif st.session_state.step == 3: 
    display_page3()
elif st.session_state.step == 3.2: 
    display_page3_2()
elif st.session_state.step == 4:
    display_page4()
elif st.session_state.step == 5:
    display_page5()

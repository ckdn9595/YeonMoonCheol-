
import streamlit as st
from utils.session_state import initialize_session_state
from utils.styles import apply_styles
from views.first_input_names import display_page1
from views.second_input_chat import display_page2
# from views.third_choose_option import display_page3
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
# elif st.session_state.step == 3: # 옵션 선택 부분 추후 추가
#     display_page3()
elif st.session_state.step == 4:
    display_page4()
elif st.session_state.step == 5:
    display_page5()


import streamlit as st
from utils.session_state import initialize_session_state
from utils.styles import apply_styles
from views.first_input_names import display_page1
from views.second_choose_option import display_page2
from views.third_input_chat import display_page3
from views.third_second_ocr_chat import display_page3_2
from views.third_third_ocr_text import display_page3_3
from views.fourth_verification import display_page4
from views.fourth_second_verification import display_page4_2
from views.fourth_third_verification import display_page4_3
from views.fifth_judgment import display_page5
import db.database as db


# 세션 상태 초기화
initialize_session_state()

# 전역 스타일 설정
apply_styles()

# URL 쿼리 파라미터를 가져옵니다.
query_data = st.query_params
if 'casenum' in query_data:
    casenum = st.query_params.casenum  # key랑 매칭
    # 특정 쿼리 파라미터 값을 가져옵니다. 여기서는 'name' 파라미터를 예로 들겠습니다.
    # 가져온 값을 사용하여 페이지에 표시합니다.
    st.write(f'Hello, {casenum}!')
    cur = db.init()
    cur = db.read(cur, casenum)
    for row in cur:
        print(row)
    

    # TODO 여기왔다는건 4.3단계라는 것 4.3을 알맞게 연결한다.

# Load the appropriate step module
if st.session_state.step == 1:
    display_page1()
elif st.session_state.step == 2:
    display_page2()
elif st.session_state.step == 3: 
    display_page3()
elif st.session_state.step == 3.2: 
    display_page3_2()
elif st.session_state.step == 3.3:
    display_page3_3()
elif st.session_state.step == 4:
    display_page4()
elif st.session_state.step == 4.2:
    display_page4_2()
elif st.session_state.step == 4.3:
    display_page4_3()
elif st.session_state.step == 5:
    display_page5()

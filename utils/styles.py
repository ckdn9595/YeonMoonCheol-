import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo&display=swap');
        h1 {
            font-family: 'Nanum Myeongjo', serif;
            color: #FF0056;
            text-align: center;
        }
        .left-image, .right-image {
            position: fixed;
            width: 300px;
            height: 100%;
            top: 0;
            z-index: -1;
        }
        .left-image {
            left: 0;
        }
        .right-image {
            right: 0;
        }
        .custom-container {
            background-color: #FFE6E6;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        .highlight {
            background-color: lightgreen !important;
        }
        .custom-checkbox {
            display: flex;
            align-items: center;
            height: 100%;
            width: 100%;
            justify-content: center !important;
        }
        .stCheckbox span {
            -webkit-transform: scale(1.3);
        }
        .stButton{
            display: flex;
            flex-wrap: nowrap;
            justify-content: space-around;
        }

        .stButton>button, .stForm button {
            background-color: #FFFFFF;
            color: #FF0056;
            border-radius: 12px;
            border: solid 0.5px #FF0056;
            padding: 5px 10px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
            width: auto;
            height: auto;
        }
        .stButton>button:hover, .stForm button:hover {
            background-color: #FF0056;
            color: #FFFFFF;
        }
        @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo&display=swap');
        h1 {
            font-family: 'Nanum Myeongjo', serif;
            color: #FF0056;
            text-align: center;
        }
        .st-emotion-cache-35qgtp{
            margin-bottom : 0.5rem;
        }
        .st-emotion-cache-ixecyn {
            border-radius: 1em;
            border: none;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .conversation-container {
            width: 100%;
            display: flex;
            margin-bottom: 5%;
            flex-direction: column;
            align-items: flex-start;
            background-color: #9bbbd4;
            padding: 1em;
            border-radius: 1em;
        }
        .fixed-width-auto-height.receiver {
            width: 80%;
            height: auto;
            word-wrap: break-word;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
            background-color: #FFE6E6;
        }
        .fixed-width-auto-height.sender {
            width: 80%;
            height: auto;
            word-wrap: break-word;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
            background-color: #FFE6E6;
        }
        .receiver {
            
        }
        .sender {
            float : right;
        }
        .profilereceiver {
        }
        .profile sender {
            text-align: right;
        }
        .centered-content {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;  /* 컬럼의 높이를 맞추기 위해 필요할 수 있습니다 */
        }
        .st-emotion-cache-y2rhx3 {
            padding: 5px 0 0 0;
        }
        .element-container.st-emotion-cache-1aege4m button{
            margin-top: 2rem;
            width: 30% !important;

        }
        .scrollable-container {
            max-height: 400px;
            overflow-y: scroll;
            padding-right: 15px; /* 스크롤바가 콘텐츠를 가리지 않도록 패딩 추가 */
        }
        div[data-testid="column"].st-emotion-cache-ytkq5y.e1f1d6gn3 {
            padding: 30px 0px 0px 10px;
        }
        .sender_container {
            display : flex;
            flex-direction : column;
            align-items : flex-end;
            width:100%;
        }
        div[data-testid="toastContainer"] div[role="alert"] {
            background-color: #FFE6E6;
            width: fit-content;
        }
        div[data-testid="toastContainer"] {
            display: flex;
            align-items: center;
        }
         //판결문 상단 div
        .st-emotion-cache-ocqkz7{
            width : 100%;
        }
        .big-font{
            font-size : 1em;
            @media screen and (max-width: 768px) {
                font-size : 0.8em;   
            }
        }
        .small-subheader {
            font-size: 1.5em; /* 폰트 크기를 조정합니다. 원하는 크기로 변경하세요. */
            margin-top: 0;
            margin-bottom: 0.5em;
        }
        .stPageLink div {
            display: flex;
            flex-direction: row;
            justify-content: center;
        }
        .stPageLink div a {
            padding: 0.3rem 2rem;
            background-color: #FFE6E6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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
        .fixed-width-auto-height {
            width: 300px;
            height: auto;
            word-wrap: break-word;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
        }
        .person1 {
            background-color: #FEF01B;
        }
        .person2 {
            background-color: #FEF01B;
            align-self: flex-end;
        }
        .profileperson1 {
        }
        .profileperson2 {

            align-self: flex-end;
        }

        .profileperson1 {
        }
        .profileperson2 {
            align-self: flex-end;
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
        </style>
        """,
        unsafe_allow_html=True
    )

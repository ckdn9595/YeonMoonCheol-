import streamlit as st
import os
from openai import OpenAI
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def judgement(verified_str):
    print(verified_str)
    response_reason = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"{verified_str}"
            },
            {
                "role": "system",
                "content": "입력 받은 내용에 대한 연애전문가로서, 남자와 여자의 싸움의 판결문을 원만히 화해가 되도록 300자 이내로 작성해줘."
            }
        ]
    )
    result_reason = response_reason.choices[0].message.content
    # result_reason = "에시용 판결 이유이다................................."
    return result_reason


def conclusion(verified_str):
    response_instruction = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"{verified_str}"
            },
            {
                "role": "system",
                "content": "판결문에 대한 연인 사이의 간단하고 현실적으로 가능한 귀여운 벌칙을 3가지만 만들어주고, '피고인은' 으로 시작해서 '형에 처한다' 라는 양식에 맞게 작성해줘"
            }
        ]
    )
    result_instruction = response_instruction.choices[0].message.content
    # result_instruction = "예시용 결론이다..............................."
    return result_instruction


def display_page5():
    verified_str = ", ".join(st.session_state.verified_sentences)

    st.write('본 판결서는 판결서 인터넷열람 사이트에서 열람/출력되었습니다. 본 판결서를 이용하여 사건관계인의 명예나 생활의 평온을 해하는 행위는 관련 법령에 따라 금지됩니다.')
    st.markdown("<h1 style='font-size : 2.55em; text-align: center;'>연 애 중 앙 지 방 법 원</h1>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>판결</h3>",
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown('<p class="big-font">사 건</p>', unsafe_allow_html=True)
    with col3:
        st.markdown('<p class="big-font">2024 연애교통법위반(연인갈등)</p>',
                    unsafe_allow_html=True)

    with col1:
        st.markdown('<p class="big-font">피 고 인</p>', unsafe_allow_html=True)
    with col3:
        st.write(f"{st.session_state.receiver}, {st.session_state.sender}")

    with col1:
        st.markdown('<p class="big-font">검 사</p>', unsafe_allow_html=True)
    with col3:
        st.markdown('<p class="big-font">연문철(검사직무대리, 기소) 연명원(공판)</p>',
                    unsafe_allow_html=True)

    with col1:
        st.markdown('<p class="big-font">변 호 인</p>', unsafe_allow_html=True)
    with col3:
        st.markdown('<p class="big-font">법무법인(연애의 참견) 담당변호사 연문철</p>',
                    unsafe_allow_html=True)

    with col1:
        st.markdown('<p class="big-font">판결선고</p>', unsafe_allow_html=True)
    with col3:
        today = date.today()
        today_str = today.strftime("%Y-%m-%d")
        st.write(today_str)

    st.write("  ")
    st.write("  ")

    st.write("  ")
    st.write("  ")

    st.markdown("<h3 style='text-align: center;'>이           유</h3>",
                unsafe_allow_html=True)

    result_reason = judgement(verified_str)
    st.write(result_reason)

    st.write("  ")
    st.write("  ")
    st.write("  ")
    st.write("  ")

    num_male_mistakes = result_reason.count('남자')
    num_female_mistakes = result_reason.count('여자')

    total_characters = len(result_reason)

    percent_male_mistakes = (num_male_mistakes / total_characters) * 100
    percent_female_mistakes = (num_female_mistakes / total_characters) * 100

    sizes = [percent_male_mistakes, percent_female_mistakes]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)

    fig1, ax1 = plt.subplots(figsize=(2, 2))
    ax1.pie(sizes, explode=explode, labels=None, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 10})
    ax1.axis('equal')

    ax1.legend(labels=['Male', 'Female'], loc="center left",
               bbox_to_anchor=(1, 0.5), fontsize=10)

    st.subheader('판결 이유에 대한 남자와 여자의 잘못 비율 (%)')
    st.pyplot(fig1)

    st.markdown("<h3 style='text-align: center;'>결           론</h3>",
                unsafe_allow_html=True)

    result_instruction = conclusion(verified_str)
    st.write(result_instruction)

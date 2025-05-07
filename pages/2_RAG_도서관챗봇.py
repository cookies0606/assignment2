import streamlit as st
from openai import OpenAI

st.title("📘 부경대 도서관 RAG 챗봇")

VECTOR_STORE_ID = "vs_681aed335f108191bdb26bbbf0aef870"  # 위에서 출력된 ID로 대체하세요

# 세션 상태 초기화
if "rag_history" not in st.session_state:
    st.session_state.rag_history = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# API Key 입력
api_key_input = st.text_input("OpenAI API Key 입력", type="password")
if api_key_input:
    st.session_state.api_key = api_key_input

# 질문 입력
user_question = st.text_input("도서관에 대해 궁금한 점을 물어보세요:")

# 대화 초기화 버튼
if st.button("🧹 Clear"):
    st.session_state.rag_history = []

# 이전 대화 출력
for role, msg in st.session_state.rag_history:
    st.markdown(f"**{role.capitalize()}**: {msg}")

# 응답 함수
def get_rag_response(api_key, question):
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4.1-mini-2025-04-14",
        input=question,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID],
                "max_num_results": 5
            }
        ],
        include=["file_search_call.results"]
    )
    return response.output[0].content[0].text

# 응답 처리
if user_question and st.session_state.api_key:
    st.session_state.rag_history.append(("user", user_question))
    try:
        answer = get_rag_response(st.session_state.api_key, user_question)
        st.session_state.rag_history.append(("assistant", answer))
        st.rerun()
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

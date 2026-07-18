import streamlit as st
import pandas as pd
import os

# 웹사이트 기본 설정 및 제목
st.set_page_config(page_title="확통 오답 추천 앱", page_icon="🎲")
st.title("🎲 확률과 통계 오답 극복 추천 앱")
st.write("버튼을 누르면 보관된 모의고사 기출문제 중 하나를 무작위로 추천합니다.")
st.markdown("---")

# 1. 데이터 파일 불러오기
try:
    df = pd.read_csv("problems.csv", encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv("problems.csv", encoding="utf-8-sig")
except FileNotFoundError:
    st.error("앗! 폴더 안에 `problems.csv` 파일이 없습니다.")
    st.stop()

# 2. 새로운 문제 추천받기 버튼
if st.button("🎯 새로운 문제 추천받기", type="primary"):
    if not df.empty:
        selected_problem = df.sample(n=1).iloc[0]
        st.session_state["current_img"] = selected_problem["문제이미지"]
        st.session_state["current_ans"] = str(selected_problem["정답"]).strip()
        st.session_state["current_sol_img"] = selected_problem["해설"]
        
        # 상태 초기화
        st.session_state["user_answer"] = ""
        st.session_state["show_score"] = False   # 채점 결과 보여줄지 여부
        st.session_state["show_solution"] = False # 해설지 보여줄지 여부
    else:
        st.warning("현재 등록된 문제가 없습니다.")

# 3. 문제 표시 및 정답/해설 제어
if "current_img" in st.session_state:
    img_name = st.session_state["current_img"]
    if os.path.exists(img_name):
        st.image(img_name, caption=f"추천된 문제 파일: {img_name}", use_container_width=True)
    else:
        st.error(f"⚠️ `{img_name}` 사진 파일이 없습니다.")
    
    st.markdown("---")
    
    # 4. 정답 입력창
    user_ans = st.text_input("📝 이 문제의 정답 번호를 입력하세요:", key="user_answer")

    # 5. 버튼 분리 배치
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✔️ 정답 확인 및 채점하기"):
            if user_ans.strip() == "":
                st.warning("답을 먼저 입력창에 적어주세요!")
            else:
                st.session_state["show_score"] = True # 채점 결과만 보기 활성화

    with col2:
        if st.button("💡 해설 가이드 확인하기"):
            st.session_state["show_solution"] = True # 해설지만 따로 보기 활성화

    # 6. 결과 출력 (역할 분담)
    correct_ans = st.session_state["current_ans"]
    user_input_clean = user_ans.strip()
    
    # [역할 1] 채점 버튼을 눌렀을 때만 작동
    if st.session_state.get("show_score", False):
        st.markdown("---")
        if user_input_clean == correct_ans:
            st.success(f"🎉 정답입니다! (내가 쓴 답: {user_input_clean} / 실제 정답: {correct_ans})")
        else:
            st.error(f"❌ 아쉽지만 틀렸습니다! 다시 한번 풀어보세요. (내가 쓴 답: {user_input_clean})")
            
    # [역할 2] 해설 확인 버튼을 눌렀을 때만 작동
    if st.session_state.get("show_solution", False):
        st.markdown("---")
        st.subheader("📖 해당 문항 해설 가이드")
        st.info(f"🔑 이 문제의 정답은 **{correct_ans}** 입니다.")
        
        sol_img_name = st.session_state["current_sol_img"]
        if pd.isna(sol_img_name) or str(sol_img_name).strip() == "":
            st.warning("이 문제에는 등록된 해설 이미지가 없습니다.")
        elif os.path.exists(str(sol_img_name).strip()):
            st.image(str(sol_img_name).strip(), caption=f"해설 파일: {sol_img_name}", use_container_width=True)
        else:
            st.error(f"⚠️ 폴더 안에 `{sol_img_name}` 해설 사진 파일이 없습니다.")
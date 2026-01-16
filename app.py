import streamlit as st
import random
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="우리 학교 팀원 구하기",
    page_icon="🎓",
    layout="wide"
)

# 더미 데이터 생성을 위한 기본 데이터
LAST_NAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "류", "홍"]
FIRST_NAMES = ["민준", "서연", "지훈", "수빈", "예준", "서현", "도윤", "민서", "시우", "하은", "주원", "지유", "현우", "소윤", "준서", "다은", "우진", "채원", "지호", "유나"]

COLLEGES = {
    "공과대학": ["컴퓨터공학과", "전자공학과", "기계공학과", "건축학과", "화학공학과"],
    "경영대학": ["경영학과", "회계학과", "국제경영학과", "마케팅학과"],
    "사회과학대학": ["심리학과", "사회학과", "정치외교학과", "미디어커뮤니케이션학과"],
    "인문대학": ["국어국문학과", "영어영문학과", "철학과", "사학과"],
    "자연과학대학": ["수학과", "물리학과", "화학과", "생명과학과"],
    "예술대학": ["시각디자인학과", "산업디자인학과", "미술학과", "음악학과"]
}

INTEREST_AREAS = ["기획", "개발", "디자인", "데이터 분석", "마케팅", "영상제작", "글쓰기", "리서치"]
ACTIVITIES = ["공모전", "대외활동", "창업", "스터디", "프로젝트"]

def generate_dummy_data(count=20):
    """더미 학생 데이터 생성"""
    students = []
    for i in range(count):
        college = random.choice(list(COLLEGES.keys()))
        major = random.choice(COLLEGES[college])
        name = random.choice(LAST_NAMES) + random.choice(FIRST_NAMES)
        interests = random.sample(INTEREST_AREAS, k=random.randint(1, 3))
        activities = random.sample(ACTIVITIES, k=random.randint(1, 2))
        grade = random.randint(1, 4)
        
        students.append({
            "이름": name,
            "학년": f"{grade}학년",
            "단과대": college,
            "전공": major,
            "관심 분야": ", ".join(interests),
            "관심 분야 리스트": interests,
            "희망 활동": ", ".join(activities),
            "희망 활동 리스트": activities
        })
    return students

def filter_students(students, selected_interests, selected_colleges):
    """조건에 맞는 학생 필터링"""
    filtered = []
    for student in students:
        interest_match = not selected_interests or any(i in student["관심 분야 리스트"] for i in selected_interests)
        college_match = not selected_colleges or student["단과대"] in selected_colleges
        
        if interest_match and college_match:
            filtered.append(student)
    return filtered

# 세션 상태 초기화
if "students" not in st.session_state:
    st.session_state.students = []

# 헤더
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1>🎓 우리 학교 팀원 구하기</h1>
    <p style="font-size: 18px; color: #666;">같은 학교 재학생과 함께 팀을 구성하세요!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 입력 영역
st.markdown("### 📝 입력 영역")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🎲 더미 데이터 생성", type="primary", use_container_width=True):
        st.session_state.students = generate_dummy_data(25)
        st.success(f"✅ {len(st.session_state.students)}명의 더미 데이터가 생성되었습니다!")

with col2:
    data_count = len(st.session_state.students)
    st.metric("현재 등록된 학생 수", f"{data_count}명")

with col3:
    if st.button("🗑️ 데이터 초기화", use_container_width=True):
        st.session_state.students = []
        st.rerun()

st.markdown("---")

# 필터 조건 선택
if st.session_state.students:
    st.markdown("### 🔍 팀원 검색 조건")
    
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        selected_interests = st.multiselect(
            "관심 분야 선택",
            options=INTEREST_AREAS,
            placeholder="원하는 관심 분야를 선택하세요"
        )
    
    with filter_col2:
        selected_colleges = st.multiselect(
            "단과대 선택",
            options=list(COLLEGES.keys()),
            placeholder="원하는 단과대를 선택하세요"
        )

    st.markdown("---")
    
    # 결과 영역
    st.markdown("### 📊 결과 영역")
    
    # 필터링된 학생
    filtered_students = filter_students(st.session_state.students, selected_interests, selected_colleges)
    
    # 통계 시각화
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.markdown("#### 단과대별 인원 분포")
        college_counts = {}
        for student in filtered_students:
            college = student["단과대"]
            college_counts[college] = college_counts.get(college, 0) + 1
        
        if college_counts:
            df_college = pd.DataFrame({
                "단과대": list(college_counts.keys()),
                "인원수": list(college_counts.values())
            })
            st.bar_chart(df_college.set_index("단과대"))
        else:
            st.info("조건에 맞는 학생이 없습니다.")
    
    with stat_col2:
        st.markdown("#### 관심 분야별 인원 분포")
        interest_counts = {}
        for student in filtered_students:
            for interest in student["관심 분야 리스트"]:
                interest_counts[interest] = interest_counts.get(interest, 0) + 1
        
        if interest_counts:
            df_interest = pd.DataFrame({
                "관심 분야": list(interest_counts.keys()),
                "인원수": list(interest_counts.values())
            })
            st.bar_chart(df_interest.set_index("관심 분야"))
        else:
            st.info("조건에 맞는 학생이 없습니다.")
    
    st.markdown("---")
    
    # 팀원 추천 결과
    st.markdown(f"#### 🎯 추천 팀원 목록 ({len(filtered_students)}명)")
    
    if filtered_students:
        # 카드 형태로 표시
        cols = st.columns(3)
        for idx, student in enumerate(filtered_students):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background-color: #f8f9fa;
                        border-radius: 10px;
                        padding: 15px;
                        margin-bottom: 15px;
                        border-left: 4px solid #4CAF50;
                    ">
                        <h4 style="margin: 0 0 10px 0;">👤 {student['이름']}</h4>
                        <p style="margin: 5px 0;"><strong>🏫 {student['단과대']}</strong> | {student['전공']}</p>
                        <p style="margin: 5px 0;">📚 {student['학년']}</p>
                        <p style="margin: 5px 0;">💡 <strong>관심:</strong> {student['관심 분야']}</p>
                        <p style="margin: 5px 0;">🎯 <strong>희망:</strong> {student['희망 활동']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("조건에 맞는 팀원이 없습니다. 다른 조건을 선택해 보세요.")
    
    # 표 형태로도 표시 (항상 표시)
    st.markdown("---")
    st.markdown("#### 📋 전체 목록 (표)")
    if filtered_students:
        df_display = pd.DataFrame([{
            "이름": s["이름"],
            "학년": s["학년"],
            "단과대": s["단과대"],
            "전공": s["전공"],
            "관심 분야": s["관심 분야"],
            "희망 활동": s["희망 활동"]
        } for s in filtered_students])
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("표시할 데이터가 없습니다.")

else:
    # 데이터가 없을 때 안내 메시지
    st.markdown("""
    <div style="
        text-align: center;
        padding: 50px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin: 20px 0;
    ">
        <h3>👆 먼저 '더미 데이터 생성' 버튼을 클릭하세요!</h3>
        <p>가상의 재학생 데이터가 생성되면 팀원을 검색할 수 있습니다.</p>
        <br>
        <p style="color: #888;">
            <strong>사용 방법:</strong><br>
            1️⃣ 더미 데이터 생성 → 2️⃣ 조건 선택 → 3️⃣ 팀원 추천 결과 확인
        </p>
    </div>
    """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    <p>🎓 우리 학교 팀원 구하기 POC | 같은 학교에서 팀원을 쉽게 찾을 수 있습니다!</p>
</div>
""", unsafe_allow_html=True)

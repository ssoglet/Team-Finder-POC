import streamlit as st
import random
import pandas as pd
from datetime import datetime

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
GRADES = ["1학년", "2학년", "3학년", "4학년"]

def generate_dummy_data(count=25):
    """더미 학생 데이터 생성"""
    students = []
    for i in range(count):
        college = random.choice(list(COLLEGES.keys()))
        major = random.choice(COLLEGES[college])
        name = random.choice(LAST_NAMES) + random.choice(FIRST_NAMES)
        interests = random.sample(INTEREST_AREAS, k=random.randint(1, 3))
        activities = random.sample(ACTIVITIES, k=random.randint(1, 2))
        grade = random.randint(1, 4)
        
        activity_toggles = {act: random.choice([True, False]) for act in ACTIVITIES}
        if not any(activity_toggles.values()):
            activity_toggles[random.choice(ACTIVITIES)] = True
        
        students.append({
            "id": i,
            "이름": name,
            "학년": f"{grade}학년",
            "학년_숫자": grade,
            "단과대": college,
            "전공": major,
            "관심 분야": ", ".join(interests),
            "관심 분야 리스트": interests,
            "희망 활동": ", ".join([k for k, v in activity_toggles.items() if v]),
            "희망 활동 리스트": [k for k, v in activity_toggles.items() if v],
            "희망 활동 토글": activity_toggles,
            "활성화": any(activity_toggles.values())
        })
    return students

def filter_students(students, selected_interests, selected_colleges):
    """조건에 맞는 학생 필터링"""
    filtered = []
    for student in students:
        if not student.get("활성화", True):
            continue
        interest_match = not selected_interests or any(i in student["관심 분야 리스트"] for i in selected_interests)
        college_match = not selected_colleges or student["단과대"] in selected_colleges
        
        if interest_match and college_match:
            filtered.append(student)
    return filtered

@st.dialog("메시지 보내기")
def send_message_dialog(target):
    """메시지 전송 다이얼로그"""
    st.markdown(f"""
    <div style="
        background-color: #e3f2fd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    ">
        <p><strong>받는 사람:</strong> {target['이름']} ({target['단과대']} {target['전공']})</p>
    </div>
    """, unsafe_allow_html=True)
    
    message_content = st.text_area("메시지 내용", placeholder="메시지를 입력하세요...", key="dialog_message")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 메시지 전송", type="primary", use_container_width=True):
            if message_content:
                sender = st.session_state.my_profile["이름"] if st.session_state.my_profile else "나"
                chat_id = f"chat_{target['id']}"
                
                if chat_id not in st.session_state.chats:
                    st.session_state.chats[chat_id] = {
                        "상대방": target,
                        "메시지": []
                    }
                
                st.session_state.chats[chat_id]["메시지"].append({
                    "발신자": sender,
                    "내용": message_content,
                    "시간": datetime.now().strftime("%H:%M")
                })
                
                st.success(f"✅ {target['이름']}님에게 메시지를 보냈습니다!")
                st.rerun()
            else:
                st.error("메시지를 입력해주세요.")
    
    with col2:
        if st.button("❌ 취소", use_container_width=True):
            st.rerun()

# 세션 상태 초기화
if "students" not in st.session_state:
    st.session_state.students = []
if "posts" not in st.session_state:
    st.session_state.posts = []
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "my_profile" not in st.session_state:
    st.session_state.my_profile = None
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# 헤더
st.markdown("""
<div style="text-align: center; padding: 10px 0;">
    <h1>🎓 우리 학교 팀원 구하기</h1>
    <p style="font-size: 16px; color: #666;">같은 학교 재학생과 함께 팀을 구성하세요!</p>
</div>
""", unsafe_allow_html=True)

# 더미 데이터 생성 버튼 (상단 고정)
col_data1, col_data2, col_data3 = st.columns([1, 1, 1])
with col_data1:
    if st.button("🎲 더미 데이터 생성", type="primary", use_container_width=True):
        st.session_state.students = generate_dummy_data(25)
        st.session_state.posts = []
        st.session_state.chats = {}
        for i in range(3):
            student = random.choice(st.session_state.students)
            st.session_state.posts.append({
                "id": i,
                "작성자": student["이름"],
                "작성자_정보": student,
                "제목": random.choice(["공모전 팀원 모집합니다!", "창업 아이디어 함께할 분!", "대외활동 같이 해요", "프로젝트 팀원 구합니다"]),
                "내용": random.choice([
                    "기획/개발/디자인 가능한 분 환영합니다. 열정 있으신 분 연락주세요!",
                    "아이디어가 있는데 같이 발전시켜 나갈 팀원 구합니다.",
                    "경험 유무 상관없이 열정만 있으면 됩니다!"
                ]),
                "희망_학년": random.sample(GRADES, k=random.randint(1, 4)),
                "희망_단과대": random.sample(list(COLLEGES.keys()), k=random.randint(1, 3)),
                "희망_관심분야": random.sample(INTEREST_AREAS, k=random.randint(1, 3)),
                "댓글": [],
                "작성일": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        st.success(f"✅ {len(st.session_state.students)}명의 더미 데이터와 샘플 게시글이 생성되었습니다!")

with col_data2:
    st.metric("등록된 학생 수", f"{len(st.session_state.students)}명")

with col_data3:
    if st.button("🗑️ 데이터 초기화", use_container_width=True):
        st.session_state.students = []
        st.session_state.posts = []
        st.session_state.chats = {}
        st.session_state.my_profile = None
        st.rerun()

st.markdown("---")

# 탭 네비게이션
tab1, tab2, tab3, tab4 = st.tabs(["🏠 팀원 찾기 커뮤니티", "🔍 팀원 검색", "💬 채팅", "👤 본인 등록"])

# ===== 탭 1: 팀원 찾기 커뮤니티 =====
with tab1:
    st.markdown("### 📋 팀원 모집 게시판")
    st.markdown("공모전, 창업, 대외활동 팀원을 모집하는 공간입니다.")
    
    if not st.session_state.students:
        st.info("👆 먼저 '더미 데이터 생성' 버튼을 클릭해주세요!")
    else:
        # 새 게시글 작성
        with st.expander("✍️ 새 게시글 작성하기", expanded=False):
            if not st.session_state.my_profile:
                st.warning("게시글을 작성하려면 먼저 '본인 등록' 탭에서 프로필을 등록해주세요.")
            else:
                post_title = st.text_input("제목", placeholder="게시글 제목을 입력하세요")
                post_content = st.text_area("내용", placeholder="팀원 모집 내용을 작성하세요", height=100)
                
                post_col1, post_col2 = st.columns(2)
                with post_col1:
                    post_grades = st.multiselect("희망 학년", GRADES, key="post_grades")
                    post_colleges = st.multiselect("희망 단과대", list(COLLEGES.keys()), key="post_colleges")
                with post_col2:
                    post_interests = st.multiselect("희망 관심 분야", INTEREST_AREAS, key="post_interests")
                
                if st.button("📝 게시글 등록", type="primary"):
                    if post_title and post_content:
                        new_post = {
                            "id": len(st.session_state.posts),
                            "작성자": st.session_state.my_profile["이름"],
                            "작성자_정보": st.session_state.my_profile,
                            "제목": post_title,
                            "내용": post_content,
                            "희망_학년": post_grades,
                            "희망_단과대": post_colleges,
                            "희망_관심분야": post_interests,
                            "댓글": [],
                            "작성일": datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        st.session_state.posts.insert(0, new_post)
                        st.success("게시글이 등록되었습니다!")
                        st.rerun()
                    else:
                        st.error("제목과 내용을 모두 입력해주세요.")
        
        st.markdown("---")
        
        # 게시글 리스트
        if st.session_state.posts:
            for post in st.session_state.posts:
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background-color: #f8f9fa;
                        border-radius: 10px;
                        padding: 20px;
                        margin-bottom: 15px;
                        border-left: 4px solid #2196F3;
                    ">
                        <h4 style="margin: 0 0 10px 0;">📌 {post['제목']}</h4>
                        <p style="margin: 5px 0; color: #666;">
                            <strong>작성자:</strong> {post['작성자']} ({post['작성자_정보']['단과대']} {post['작성자_정보']['전공']})
                        </p>
                        <p style="margin: 10px 0;">{post['내용']}</p>
                        <p style="margin: 5px 0; font-size: 12px; color: #888;">
                            희망 학년: {', '.join(post['희망_학년']) if post['희망_학년'] else '무관'} | 
                            희망 단과대: {', '.join(post['희망_단과대']) if post['희망_단과대'] else '무관'} |
                            희망 분야: {', '.join(post['희망_관심분야']) if post['희망_관심분야'] else '무관'}
                        </p>
                        <p style="margin: 5px 0; font-size: 11px; color: #aaa;">작성일: {post['작성일']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 댓글 표시
                    if post['댓글']:
                        st.markdown("**💬 댓글:**")
                        for comment in post['댓글']:
                            st.markdown(f"- **{comment['작성자']}**: {comment['내용']}")
                    
                    # 댓글 입력
                    comment_key = f"comment_{post['id']}"
                    comment_col1, comment_col2 = st.columns([4, 1])
                    with comment_col1:
                        new_comment = st.text_input("댓글 작성", key=comment_key, placeholder="참여 의사를 남겨주세요!", label_visibility="collapsed")
                    with comment_col2:
                        if st.button("댓글 등록", key=f"btn_{post['id']}"):
                            if new_comment:
                                author = st.session_state.my_profile["이름"] if st.session_state.my_profile else "익명"
                                post['댓글'].append({
                                    "작성자": author,
                                    "내용": new_comment
                                })
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("아직 게시글이 없습니다. 첫 게시글을 작성해보세요!")

# ===== 탭 2: 팀원 검색 =====
with tab2:
    st.markdown("### 🔍 팀원 검색")
    
    if not st.session_state.students:
        st.info("👆 먼저 '더미 데이터 생성' 버튼을 클릭해주세요!")
    else:
        # 필터 조건 선택
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            selected_interests = st.multiselect(
                "관심 분야 선택",
                options=INTEREST_AREAS,
                placeholder="원하는 관심 분야를 선택하세요",
                key="search_interests"
            )
        
        with filter_col2:
            selected_colleges = st.multiselect(
                "단과대 선택",
                options=list(COLLEGES.keys()),
                placeholder="원하는 단과대를 선택하세요",
                key="search_colleges"
            )
        
        st.markdown("---")
        
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
            cols = st.columns(3)
            for idx, student in enumerate(filtered_students):
                with cols[idx % 3]:
                    with st.container():
                        st.markdown(f"""
                        <div style="
                            background-color: #f8f9fa;
                            border-radius: 10px;
                            padding: 15px;
                            margin-bottom: 10px;
                            border-left: 4px solid #4CAF50;
                        ">
                            <h4 style="margin: 0 0 10px 0;">👤 {student['이름']}</h4>
                            <p style="margin: 5px 0;"><strong>🏫 {student['단과대']}</strong> | {student['전공']}</p>
                            <p style="margin: 5px 0;">📚 {student['학년']}</p>
                            <p style="margin: 5px 0;">💡 <strong>관심:</strong> {student['관심 분야']}</p>
                            <p style="margin: 5px 0;">🎯 <strong>희망:</strong> {student['희망 활동']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 메시지 보내기 버튼
                        if st.button(f"💬 메시지 보내기", key=f"msg_{student['id']}", use_container_width=True):
                            send_message_dialog(student)
        else:
            st.warning("조건에 맞는 팀원이 없습니다. 다른 조건을 선택해 보세요.")
        
        # 표 형태로도 표시
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
        
# ===== 탭 3: 채팅 =====
with tab3:
    st.markdown("### 💬 채팅")
    
    if not st.session_state.chats:
        st.info("아직 대화가 없습니다. 팀원 검색에서 메시지를 보내보세요!")
    else:
        chat_col1, chat_col2 = st.columns([1, 2])
        
        with chat_col1:
            st.markdown("#### 채팅방 목록")
            for chat_id, chat_data in st.session_state.chats.items():
                other_person = chat_data["상대방"]
                last_msg = chat_data["메시지"][-1]["내용"][:20] + "..." if chat_data["메시지"] else "새 대화"
                
                if st.button(
                    f"👤 {other_person['이름']}\n{last_msg}",
                    key=f"select_{chat_id}",
                    use_container_width=True
                ):
                    st.session_state.current_chat = chat_id
                    st.rerun()
        
        with chat_col2:
            if st.session_state.current_chat and st.session_state.current_chat in st.session_state.chats:
                current = st.session_state.chats[st.session_state.current_chat]
                other = current["상대방"]
                
                st.markdown(f"#### 💬 {other['이름']}님과의 대화")
                st.markdown(f"*{other['단과대']} {other['전공']} | {other['학년']}*")
                st.markdown("---")
                
                # 메시지 표시
                chat_container = st.container()
                with chat_container:
                    for msg in current["메시지"]:
                        sender = st.session_state.my_profile["이름"] if st.session_state.my_profile else "나"
                        is_me = msg["발신자"] == sender
                        
                        if is_me:
                            st.markdown(f"""
                            <div style="
                                text-align: right;
                                margin: 10px 0;
                            ">
                                <span style="
                                    background-color: #2196F3;
                                    color: white;
                                    padding: 8px 15px;
                                    border-radius: 15px;
                                    display: inline-block;
                                    max-width: 70%;
                                ">
                                    {msg['내용']}
                                </span>
                                <br>
                                <span style="font-size: 11px; color: #888;">{msg['시간']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="
                                text-align: left;
                                margin: 10px 0;
                            ">
                                <strong>{msg['발신자']}</strong><br>
                                <span style="
                                    background-color: #e0e0e0;
                                    color: black;
                                    padding: 8px 15px;
                                    border-radius: 15px;
                                    display: inline-block;
                                    max-width: 70%;
                                ">
                                    {msg['내용']}
                                </span>
                                <br>
                                <span style="font-size: 11px; color: #888;">{msg['시간']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # 메시지 입력
                new_msg_col1, new_msg_col2 = st.columns([4, 1])
                with new_msg_col1:
                    new_message = st.text_input("메시지 입력", key="chat_input", placeholder="메시지를 입력하세요...", label_visibility="collapsed")
                with new_msg_col2:
                    if st.button("전송", type="primary", use_container_width=True):
                        if new_message:
                            sender = st.session_state.my_profile["이름"] if st.session_state.my_profile else "나"
                            current["메시지"].append({
                                "발신자": sender,
                                "내용": new_message,
                                "시간": datetime.now().strftime("%H:%M")
                            })
                            st.rerun()
            else:
                st.info("👈 왼쪽에서 채팅방을 선택하세요.")

# ===== 탭 4: 본인 등록 =====
with tab4:
    st.markdown("### 👤 본인 프로필 등록")
    st.markdown("프로필을 등록하면 다른 학생들이 나를 찾을 수 있습니다.")
    
    if st.session_state.my_profile:
        st.success("✅ 프로필이 등록되어 있습니다!")
        st.markdown("---")
        
        profile = st.session_state.my_profile
        st.markdown(f"""
        <div style="
            background-color: #e8f5e9;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #4CAF50;
        ">
            <h3>👤 {profile['이름']}</h3>
            <p><strong>🏫 소속:</strong> {profile['단과대']} {profile['전공']}</p>
            <p><strong>📚 학년:</strong> {profile['학년']}</p>
            <p><strong>💡 관심 분야:</strong> {profile['관심 분야']}</p>
            <p><strong>🎯 희망 활동:</strong> {profile['희망 활동']}</p>
            <p><strong>📌 활성화 상태:</strong> {'활성 (검색 가능)' if profile['활성화'] else '비활성 (검색 불가)'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 프로필 수정")
    
    # 프로필 폼
    with st.form("profile_form"):
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            name = st.text_input(
                "이름",
                value=st.session_state.my_profile["이름"] if st.session_state.my_profile else "",
                placeholder="이름을 입력하세요"
            )
            grade = st.selectbox(
                "학년",
                GRADES,
                index=GRADES.index(st.session_state.my_profile["학년"]) if st.session_state.my_profile else 0
            )
            college = st.selectbox(
                "단과대",
                list(COLLEGES.keys()),
                index=list(COLLEGES.keys()).index(st.session_state.my_profile["단과대"]) if st.session_state.my_profile else 0
            )
        
        with form_col2:
            selected_college_majors = COLLEGES[college]
            major = st.selectbox(
                "전공",
                selected_college_majors,
                index=selected_college_majors.index(st.session_state.my_profile["전공"]) if st.session_state.my_profile and st.session_state.my_profile["전공"] in selected_college_majors else 0
            )
            interests = st.multiselect(
                "관심 분야",
                INTEREST_AREAS,
                default=st.session_state.my_profile["관심 분야 리스트"] if st.session_state.my_profile else []
            )
        
        st.markdown("---")
        st.markdown("#### 🎯 희망 활동 (토글)")
        st.markdown("*모든 활동이 OFF일 경우 팀원 검색/커뮤니티에서 제외됩니다.*")
        
        toggle_cols = st.columns(len(ACTIVITIES))
        activity_toggles = {}
        for i, activity in enumerate(ACTIVITIES):
            with toggle_cols[i]:
                default_val = st.session_state.my_profile["희망 활동 토글"].get(activity, False) if st.session_state.my_profile else True
                activity_toggles[activity] = st.toggle(activity, value=default_val, key=f"toggle_{activity}")
        
        submitted = st.form_submit_button("💾 프로필 저장", type="primary", use_container_width=True)
        
        if submitted:
            if name and interests:
                is_active = any(activity_toggles.values())
                
                new_profile = {
                    "id": len(st.session_state.students),
                    "이름": name,
                    "학년": grade,
                    "학년_숫자": GRADES.index(grade) + 1,
                    "단과대": college,
                    "전공": major,
                    "관심 분야": ", ".join(interests),
                    "관심 분야 리스트": interests,
                    "희망 활동": ", ".join([k for k, v in activity_toggles.items() if v]),
                    "희망 활동 리스트": [k for k, v in activity_toggles.items() if v],
                    "희망 활동 토글": activity_toggles,
                    "활성화": is_active
                }
                
                st.session_state.my_profile = new_profile
                
                # 학생 목록에 추가 (이미 있으면 업데이트)
                existing_idx = None
                for i, s in enumerate(st.session_state.students):
                    if s.get("이름") == name:
                        existing_idx = i
                        break
                
                if existing_idx is not None:
                    st.session_state.students[existing_idx] = new_profile
                else:
                    st.session_state.students.append(new_profile)
                
                if not is_active:
                    st.warning("⚠️ 모든 희망 활동이 OFF입니다. 팀원 검색 및 커뮤니티에서 제외됩니다.")
                else:
                    st.success("✅ 프로필이 저장되었습니다!")
                st.rerun()
            else:
                st.error("이름과 관심 분야를 입력해주세요.")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 10px;">
    <p>🎓 우리 학교 팀원 구하기 POC | 팀원 탐색 → 연결 → 소통</p>
</div>
""", unsafe_allow_html=True)

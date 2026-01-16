# 우리 학교 팀원 구하기 POC

## Overview
같은 학교 재학생 대상 팀원 구하기 플랫폼의 POC(Proof of Concept) 웹 애플리케이션입니다.
공모전, 대외활동 등을 위해 같은 학교 내에서 팀원을 쉽게 찾을 수 있는 서비스의 가능성을 시연합니다.

## Tech Stack
- Python 3.11
- Streamlit (웹 UI 프레임워크)

## Project Structure
```
/
├── app.py                 # 메인 Streamlit 애플리케이션
├── .streamlit/
│   └── config.toml        # Streamlit 서버 설정
├── pyproject.toml         # Python 의존성
└── replit.md              # 프로젝트 문서
```

## Features
1. **더미 데이터 생성**: 가상의 재학생 데이터 25명 자동 생성
   - 이름, 학년, 단과대, 전공, 관심 분야, 희망 활동 포함
2. **필터링 기능**: 관심 분야 및 단과대 기준으로 팀원 검색
3. **시각화**: 단과대별/관심 분야별 인원 분포 차트
4. **결과 표시**: 카드 형태 + 표 형태로 팀원 목록 제공

## Running the App
```bash
streamlit run app.py --server.port 5000
```

## User Flow
1. "더미 데이터 생성" 버튼 클릭
2. 관심 분야/단과대 조건 선택
3. 필터링된 팀원 추천 결과 확인

## Recent Changes
- 2026-01-16: 초기 POC 구현 완료
  - 더미 데이터 생성 기능
  - 필터링 및 검색 기능
  - 차트 시각화 (단과대별, 관심분야별)
  - 카드/표 형태 결과 표시

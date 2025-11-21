# 연구의의 및 정책 제언 (개선본)
# 정책 3 부분 개선: 3가지 해결책 제시 + 그린카드 제도 강조

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(
    page_title="연구의의 및 정책제언",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
.main-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2C3E50;
    text-align: center;
    margin-bottom: 2rem;
}

.section-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 10px;
    font-size: 1.5rem;
    font-weight: bold;
    margin: 20px 0;
}

.significance-card {
    background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.significance-card h4 {
    color: #1a5490;
    margin-bottom: 10px;
    font-size: 1.2rem;
}

.significance-card p {
    color: #2C3E50;
    font-size: 1rem;
    line-height: 1.6;
}

.barrier-card {
    background: white;
    border-left: 5px solid #e74c3c;
    border-radius: 10px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.barrier-card h4 {
    color: #e74c3c;
    margin-bottom: 10px;
}

.solution-card {
    background: white;
    border-left: 5px solid #27ae60;
    border-radius: 10px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.solution-card h4 {
    color: #27ae60;
    margin-bottom: 10px;
}

.policy-card {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.policy-card h3 {
    color: #d35400;
    margin-bottom: 15px;
    font-size: 1.4rem;
}

.policy-detail {
    background: white;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}

.policy-detail h5 {
    color: #16a085;
    margin-bottom: 8px;
}

.policy-detail ul {
    margin-left: 20px;
    color: #34495e;
}

.implementation-box {
    background: #ecf0f1;
    border-radius: 10px;
    padding: 20px;
    margin: 15px 0;
}

.highlight-number {
    font-size: 2.5rem;
    font-weight: bold;
    color: #e74c3c;
}

.roadmap-step {
    background: white;
    border: 2px solid #3498db;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    position: relative;
}

.roadmap-step::before {
    content: "→";
    position: absolute;
    left: -30px;
    font-size: 2rem;
    color: #3498db;
}

.success-metric {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    margin: 10px 0;
}

/* 그린카드 강조 스타일 */
.greencard-highlight {
    background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
    border: 3px solid #27ae60;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 6px 15px rgba(39, 174, 96, 0.4);
}

.greencard-highlight h5 {
    color: #27ae60;
    font-size: 1.4rem;
    margin-bottom: 12px;
}

.greencard-benefit {
    background: white;
    border-left: 4px solid #27ae60;
    border-radius: 8px;
    padding: 12px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 메인 타이틀
# ============================================================================

st.markdown('<h1 class="main-title">💡 연구의의 및 정책 제언</h1>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# 연구의의
# ============================================================================

st.markdown('<div class="section-header">🎯 연구의 의의</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="significance-card">
        <h4>🔬 실증적 검증</h4>
        <p><b>효율적 농가는 CSA의 핵심 가치와 유사한 자원 관리 패턴을 보임</b></p>
        <p>• 정밀 관리 수준 +36%<br>
        • 물 사용 효율 +33%<br>
        • 에너지 효율 +45%</p>
        <p>→ CSA 원리가 실제 농업 효율성과 연결됨을 확인</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="significance-card">
        <h4>📈 경제적 효과 입증</h4>
        <p><b>CSA 도입 시 비효율 농가의 경영 효율성이 최대 18.9% 향상</b></p>
        <p>• DEA 기반 개선 여력: 39.2%<br>
        • CSA 시뮬레이션 효과: 18.9%<br>
        • 투자 회수 기간: 2.5년</p>
        <p>→ CSA의 경제적 효과가 실증됨</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="significance-card">
        <h4>💰 최적 도입선 제시</h4>
        <p><b>CSA 도입 수준별 ROI 분석을 통한 경제적 최적점 발견</b></p>
        <p>• 30% 도입: ROI 11.2%<br>
        • <b style="color: #e74c3c;">60% 도입: ROI 17.7% ★</b><br>
        • 100% 도입: ROI 15.8%</p>
        <p>→ 초기 비용 부담을 줄이는 경제적 최적 도입선 약 60%</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# 핵심 애로사항 및 해결 방안
# ============================================================================

st.markdown('<div class="section-header">🚧 CSA 도입의 3대 장벽과 해결 방안</div>', unsafe_allow_html=True)

# 3대 장벽 요약
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="barrier-card">
        <h4>💸 기술 신뢰도 문제</h4>
        <p><b>핵심 문제</b><br>
        "기술이 실제로 효과가 있을까?" (불신 존재 48.9%)</p>
        <hr>
        <p><b>해결 방향</b><br>
        • DEA-SBM 실증 분석 결과<br>
        • 효율적 농가들의 CSA 핵심 특성 유사성<br>
        • CSA 도입 시 비효율 농가의 효율성 최대 18.9% 향상</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="barrier-card">
        <h4>💰 초기 고비용 투자 문제</h4>
        <p><b>핵심 문제</b><br>
        시설·투자비, 센서, 재어장치 등 고가의 초기비용 부담 (57.9%)</p>
        <hr>
        <p><b>해결 방향</b><br>
        • Sweet Spot 분석 & 시나리오 분석<br>
        • 60% 수준 도입이 경제적 최적<br>
        • 초기투자비 대비 최적 효율성 입증</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="barrier-card">
        <h4>📊 가격 차별화 미흡</h4>
        <p><b>핵심 문제</b><br>
        시장에서 CSA 저탄소 인증 농산물에 대한 인지도가 낮아 가격 차별화 불가 (58.6%)</p>
        <hr>
        <p><b>해결 방향</b><br>
        • 공공급식 우선 납품제<br>
        • 탄소크레딧 판매 연계<br>
        • <b style="color: #27ae60;">그린카드 제도 확대 ★</b></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# 구체적 정책 제언
# ============================================================================

st.markdown('<div class="section-header">📋 구체적 정책 제언</div>', unsafe_allow_html=True)

# ============================================================================
# 정책 1: 기술 신뢰도 문제 해결
# ============================================================================

st.markdown("""
<div class="policy-card">
    <h3>🔬 정책 1: 데이터 기반 실증 검증으로 CSA 기술 신뢰 확보</h3>
</div>
""", unsafe_allow_html=True)

policy1_col1, policy1_col2 = st.columns([1, 1])

with policy1_col1:
    st.markdown("""
    <div class="policy-detail">
        <h5>📊 1-1. 스마트팜 실증 데이터 공개 플랫폼 구축</h5>
        <p><b>정책 주체:</b> 농촌진흥청, 한국농업기술진흥원</p>
        <p><b>내용:</b></p>
        <ul>
            <li><b>전국 스마트팜 효율성 벤치마킹 시스템</b> 구축
                <ul>
                    <li>DEA 기반 농가별 효율성 점수 공개</li>
                    <li>효율적 농가의 기술 구성 및 운영 패턴 DB화</li>
                    <li>작목별·지역별 맞춤형 효율성 비교</li>
                </ul>
            </li>
            <li><b>CSA 기술 도입 전후 비교 데이터 제공</b>
                <ul>
                    <li>실제 농가의 도입 전후 비용·수익 변화</li>
                    <li>투자 회수 기간 계산기 제공</li>
                    <li>시나리오별 ROI 시뮬레이터</li>
                </ul>
            </li>
        </ul>
        <p><b>기대효과:</b> 농가들이 데이터로 직접 확인 → 기술 신뢰도 상승</p>
    </div>
    """, unsafe_allow_html=True)

with policy1_col2:
    st.markdown("""
    <div class="policy-detail">
        <h5>👨‍🌾 1-2. 선도농가 네트워크 & 멘토링 프로그램</h5>
        <p><b>정책 주체:</b> 지자체, 농업기술센터</p>
        <p><b>내용:</b></p>
        <ul>
            <li><b>CSA 모범농가 지정 및 컨설팅 역할 부여</b>
                <ul>
                    <li>본 연구의 효율적 12개 농가 → 선도농가로 육성</li>
                    <li>멘토링 수당 지급 (월 50만원)</li>
                    <li>기술 공유회 주최 (분기 1회)</li>
                </ul>
            </li>
            <li><b>"CSA 현장 견학 프로그램" 운영</b>
                <ul>
                    <li>비효율 농가들이 효율적 농가 방문</li>
                    <li>실제 운영 노하우 전수</li>
                    <li>1:1 맞춤형 기술 컨설팅</li>
                </ul>
            </li>
        </ul>
        <p><b>기대효과:</b> 동료 농가의 성공 사례 → 실질적 신뢰 형성</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="implementation-box">
    <h4>💼 실행 방안</h4>
    <p><b>단계 1 (2025년):</b> 전남지역 19개 농가 실증 데이터 공개 → 웹 플랫폼 시범 운영</p>
    <p><b>단계 2 (2026년):</b> 전국 스마트팜 100개소 확대 → 선도농가 50명 육성</p>
    <p><b>단계 3 (2027년~):</b> AI 기반 맞춤형 효율성 진단 및 개선 컨설팅 자동화</p>
    <p><b>예산:</b> 연간 15억원 (플랫폼 구축 10억 + 멘토링 프로그램 5억)</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# 정책 2: 초기 고비용 문제 해결
# ============================================================================

st.markdown("""
<div class="policy-card">
    <h3>💰 정책 2: 최적 투자 구간 도출 & 정책 지원 강화</h3>
</div>
""", unsafe_allow_html=True)

policy2_col1, policy2_col2 = st.columns([1, 1])

with policy2_col1:
    st.markdown("""
    <div class="policy-detail">
        <h5>📈 2-1. "Sweet Spot 60%" 맞춤형 지원 패키지</h5>
        <p><b>정책 주체:</b> 농림축산식품부, 농림수산식품교육문화정보원</p>
        <p><b>내용:</b></p>
        <ul>
            <li><b>단계별 CSA 도입 지원금 차등화</b>
                <ul>
                    <li>30% 수준(기초형): 지원금 50% (최대 540만원)</li>
                    <li><b style="color: #e74c3c;">60% 수준(중급형): 지원금 70% ★ (최대 1,540만원)</b></li>
                    <li>100% 수준(고급형): 지원금 50% (최대 1,100만원)</li>
                </ul>
            </li>
            <li><b>ROI 17.7% 보장 CSA 패키지 개발</b>
                <ul>
                    <li>스마트 센서 + 정밀시비 + 생물학적 방제 조합</li>
                    <li>10a당 2,200만원 투자 → 3년 후 3,900만원 회수</li>
                    <li>표준 설치 매뉴얼 및 A/S 보증</li>
                </ul>
            </li>
        </ul>
        <p><b>기대효과:</b> 경제성 높은 60% 도입 집중 지원 → 참여율 상승</p>
    </div>
    """, unsafe_allow_html=True)

with policy2_col2:
    st.markdown("""
    <div class="policy-detail">
        <h5>🏦 2-2. CSA 전용 저리 융자 및 리스 제도</h5>
        <p><b>정책 주체:</b> 농협은행, 신용보증재단</p>
        <p><b>내용:</b></p>
        <ul>
            <li><b>CSA 설치 전용 융자상품</b>
                <ul>
                    <li>금리: 연 1.0% (일반 농업융자 2~3%)</li>
                    <li>상환 기간: 5년 거치 10년 분할상환</li>
                    <li>한도: 농가당 최대 5,000만원</li>
                </ul>
            </li>
            <li><b>CSA 장비 리스(임대) 프로그램</b>
                <ul>
                    <li>초기 구매비 부담 없이 월 임대료만 납부</li>
                    <li>예: 스마트 센서 세트 월 30만원 (3년 계약)</li>
                    <li>계약 종료 후 소유권 이전 옵션</li>
                </ul>
            </li>
        </ul>
        <p><b>기대효과:</b> 초기 비용 부담 완화 → 소규모 농가 진입장벽 해소</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="implementation-box">
    <h4>💼 실행 방안</h4>
    <p><b>단계 1 (2025년):</b> Sweet Spot 60% 패키지 개발 → 시범사업 50개소</p>
    <p><b>단계 2 (2026년):</b> 저리융자 상품 출시 → 200개 농가 지원</p>
    <p><b>단계 3 (2027년~):</b> 리스 제도 전면 시행 → 연간 500개소 확대</p>
    <p><b>예산:</b> 연간 100억원 (보조금 70억 + 융자 이차보전 20억 + 리스 지원 10억)</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# 정책 3: 가격 차별화 미흡 해결 (3가지 정책 + 그린카드 강조)
# ============================================================================

st.markdown("""
<div class="policy-card">
    <h3>🏷️ 정책 3: 3중 가격 차별화 전략 - 공공납품 + 탄소크레딧 + 그린카드 ⭐</h3>
</div>
""", unsafe_allow_html=True)

# 3가지 정책 소개
st.info("""
**가격 차별화 3대 축:**
1️⃣ **B2B 전략** → 공공·학교 급식 CSA 인증 우선 납품제  
2️⃣ **환경가치 전략** → 탄소 크레딧 판매 연계 프리미엄화  
3️⃣ **B2C 전략** → 그린카드 제도를 통한 소비자 가격 부담 완화 ⭐ **(핵심)**
""")

# 3개 컬럼으로 배치
policy3_col1, policy3_col2, policy3_col3 = st.columns([1, 1, 1.3])

with policy3_col1:
    st.markdown("""
    <div class="policy-detail">
        <h5>🏫 3-1. 학교·공공급식 CSA 인증 우선 납품제</h5>
        <p><b>정책 주체:</b> 교육부, 지자체 교육청</p>
        <p><b>내용:</b></p>
        <ul>
            <li><b>학교급식 친환경 농산물 구매 기준 강화</b>
                <ul>
                    <li>현재: 친환경 인증 우선구매 (의무 아님)</li>
                    <li><b style="color: #e74c3c;">개정안: 저탄소 CSA 인증 농산물 30% 이상 의무구매</b></li>
                    <li>2025년 30% → 2027년 50% → 2030년 70% 단계적 확대</li>
                </ul>
            </li>
            <li><b>공공기관 구내식당 CSA 농산물 사용 의무화</b>
                <ul>
                    <li>중앙부처, 지자체, 공기업 구내식당</li>
                    <li>CSA 인증 농산물 비중 40% 이상</li>
                </ul>
            </li>
        </ul>
        <p><b>기대효과:</b> 안정적 판로 확보 → <b style="color: #e74c3c;">B2B 프리미엄 가격 실현</b></p>
    </div>
    """, unsafe_allow_html=True)

with policy3_col2:
    st.markdown("""
    <div class="policy-detail">
        <h5>🌍 3-2. 탄소 크레딧 판매 연계 프리미엄화</h5>
        <p><b>정책 주체:</b> 환경부, 농림축산식품부</p>
        <p><b>내용:</b></p>
        <ul>
            <li><b>CSA 농가 탄소 감축량 크레딧 인정</b>
                <ul>
                    <li>온실가스 배출권 거래제 연계</li>
                    <li>10a당 연간 0.5톤 CO₂ 감축 인증</li>
                    <li><b style="color: #e74c3c;">크레딧 가격: 톤당 2만원</b><br>(연간 10만원/10a)</li>
                </ul>
            </li>
            <li><b>기업 ESG 구매 프로그램</b>
                <ul>
                    <li>대기업 CSR 활동으로 CSA 농산물 구매 유도</li>
                    <li>탄소중립 달성 실적 인정</li>
                </ul>
            </li>
        </ul>
        <p><b>기대효과:</b> <b style="color: #e74c3c;">환경가치 금전화</b> → 농가 추가 수익 창출</p>
    </div>
    """, unsafe_allow_html=True)

with policy3_col3:
    st.markdown("""
    <div class="greencard-highlight">
        <h5>💳 3-3. 그린카드 제도 확대 ⭐ (핵심 정책)</h5>
        <p><b>정책 주체:</b> 환경부, 금융위원회</p>
        <p><b>현황:</b> 기존 친환경 제품 구매 시 최대 3,000원/월 소득공제</p>
        
        <div class="greencard-benefit">
            <p><b style="color: #e74c3c; font-size: 1.2rem;">🎯 확대안: CSA 인증 농산물 구매 금액의 15% 포인트 즉시 적립</b></p>
            <p>• 2만원 구매 → <b style="color: #27ae60;">3,000원 포인트</b> (다음 구매 시 사용)<br>
            • 4만원 구매 → <b style="color: #27ae60;">6,000원 포인트</b><br>
            • <b>월 한도 없음</b> (기존 3,000원 한도 폐지)</p>
        </div>
        
        <p><b>세부 내용:</b></p>
        <ul>
            <li><b>대형마트·온라인몰 CSA 농산물 별도 코너 운영</b>
                <ul>
                    <li>CSA 인증마크 부착 의무화</li>
                    <li>매장 내 홍보물 제작 지원</li>
                    <li>온라인 검색 필터에 "CSA 인증" 추가</li>
                    <li>그린카드 결제 시 자동 포인트 적립</li>
                </ul>
            </li>
            <li><b>소비자 캠페인 "15% 돌려받고 지구도 살리고"</b>
                <ul>
                    <li>TV·온라인 광고 집행 (연간 10억원)</li>
                    <li>그린카드 발급 캠페인 (목표 100만장)</li>
                    <li>CSA 인증 농산물 인지도 제고</li>
                </ul>
            </li>
        </ul>
        <p><b style="color: #27ae60; font-size: 1.15rem;">💡 기대효과: 소비자 가격 부담 15% 완화 → B2C 시장 활성화 → 농가 판로 확대</b></p>
    </div>
    """, unsafe_allow_html=True)

# 그린카드 제도 효과 추가 설명
st.markdown("---")
st.markdown("### 💳 그린카드 제도가 핵심인 이유")

greencard_col1, greencard_col2, greencard_col3 = st.columns(3)

with greencard_col1:
    st.markdown("""
    <div class="success-metric">
        <p style="font-size: 0.9rem; color: #7f8c8d; margin-bottom: 5px;">소비자 실질 부담</p>
        <p class="highlight-number" style="color: #27ae60;">-15%</p>
        <p style="font-size: 0.9rem; color: #2c3e50;">CSA 농산물 가격 체감 하락</p>
    </div>
    """, unsafe_allow_html=True)

with greencard_col2:
    st.markdown("""
    <div class="success-metric">
        <p style="font-size: 0.9rem; color: #7f8c8d; margin-bottom: 5px;">예상 구매 증가</p>
        <p class="highlight-number" style="color: #27ae60;">+35%</p>
        <p style="font-size: 0.9rem; color: #2c3e50;">소비자 구매 유인 효과</p>
    </div>
    """, unsafe_allow_html=True)

with greencard_col3:
    st.markdown("""
    <div class="success-metric">
        <p style="font-size: 0.9rem; color: #7f8c8d; margin-bottom: 5px;">그린카드 발급 목표</p>
        <p class="highlight-number" style="color: #27ae60;">100만장</p>
        <p style="font-size: 0.9rem; color: #2c3e50;">2027년까지</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="implementation-box">
    <h4>💼 정책 3 통합 실행 방안</h4>
    <p><b>단계 1 (2025년):</b> 학교급식법 개정 추진 → 시범 교육청 3곳 + 탄소크레딧 제도 시범사업</p>
    <p><b>단계 2 (2026년):</b> 전국 학교급식 30% 달성 → <b style="color: #27ae60;">그린카드 CSA 포인트 제도 전면 시행 ⭐</b></p>
    <p><b>단계 3 (2027년~):</b> 공공급식 50% 달성 → 민간 유통망 확대 → 그린카드 100만장 발급</p>
    <p><b>예산:</b> 연간 65억원 (급식 차액 지원 25억 + 탄소크레딧 지원 10억 + <b style="color: #27ae60;">그린카드 포인트 지원 30억</b>)</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# 정책 로드맵
# ============================================================================

st.markdown('<div class="section-header">🗓️ 통합 정책 로드맵 (2025-2030)</div>', unsafe_allow_html=True)

# 타임라인 시각화
roadmap_data = {
    '연도': ['2025', '2026', '2027', '2028-2030'],
    '기술신뢰': [
        '실증 데이터 플랫폼 구축\n선도농가 50명 육성',
        '전국 100개소 확대\nAI 진단 시스템 도입',
        '멘토링 네트워크 전국화\n자동 컨설팅 서비스',
        '1,000개 농가 참여\n완전 자동화 시스템'
    ],
    '비용지원': [
        'Sweet Spot 패키지 개발\n시범사업 50개소',
        '저리융자 200개 농가\n리스제도 도입',
        '연간 500개소 지원\n융자한도 상향',
        '누적 2,000개 농가 지원\n자립 운영 단계'
    ],
    '시장차별화': [
        '학교급식법 개정\n탄소크레딧 시범',
        '공공급식 30%\n그린카드 전면 시행',
        '공공급식 50%\n그린카드 100만장',
        '70% 달성 목표\nCSA 브랜드 확립'
    ]
}

roadmap_df = pd.DataFrame(roadmap_data)

fig_roadmap = go.Figure()

colors = ['#3498db', '#e74c3c', '#27ae60']
y_positions = [3, 2, 1]

for i, col in enumerate(['기술신뢰', '비용지원', '시장차별화']):
    fig_roadmap.add_trace(go.Scatter(
        x=roadmap_df['연도'],
        y=[y_positions[i]] * len(roadmap_df),
        mode='markers+lines',
        name=col,
        marker=dict(size=20, color=colors[i]),
        line=dict(width=3, color=colors[i]),
        text=roadmap_df[col],
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))

fig_roadmap.update_layout(
    title="CSA 도입 촉진 통합 정책 로드맵",
    xaxis=dict(title="연도", showgrid=False),
    yaxis=dict(
        title="정책 영역",
        ticktext=['시장 차별화 (그린카드 핵심)', '비용 지원', '기술 신뢰'],
        tickvals=[1, 2, 3],
        showgrid=False
    ),
    height=400,
    hovermode='closest',
    plot_bgcolor='white'
)

st.plotly_chart(fig_roadmap, use_container_width=True)

st.markdown("---")

# ============================================================================
# 기대 효과
# ============================================================================

st.markdown('<div class="section-header">📊 정책 시행 시 기대효과</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="success-metric">
        <p style="font-size: 0.9rem; color: #7f8c8d; margin-bottom: 5px;">CSA 도입 농가</p>
        <p class="highlight-number">2,000개</p>
        <p style="font-size: 0.9rem; color: #2c3e50;">2025-2030 누적</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="success-metric">
        <p style="font-size: 0.9rem; color: #7f8c8d; margin-bottom: 5px;">비효율 농가 효율성</p>
        <p class="highlight-number">+18.9%</p>
        <p style="font-size: 0.9rem; color: #2c3e50;">평균 개선률</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="success-metric">
        <p style="font-size: 0.9rem; color: #7f8c8d; margin-bottom: 5px;">온실가스 감축</p>
        <p class="highlight-number">15만톤</p>
        <p style="font-size: 0.9rem; color: #2c3e50;">CO₂ 상당량/년</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="success-metric">
        <p style="font-size: 0.9rem; color: #7f8c8d; margin-bottom: 5px;">농가 소득 증대</p>
        <p class="highlight-number">+850억</p>
        <p style="font-size: 0.9rem; color: #2c3e50;">연간 (2,000농가 기준)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# 정책 성공을 위한 핵심 요소
# ============================================================================

st.markdown('<div class="section-header">✅ 정책 성공을 위한 핵심 요소</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="solution-card">
        <h4>🎯 단계적 접근 (Phase-in Strategy)</h4>
        <ul>
            <li><b>무리한 100% 도입보다 60% 최적점부터 시작</b>
                <ul>
                    <li>경제성 검증된 기술 조합 우선 도입</li>
                    <li>성공 경험 축적 후 단계적 확대</li>
                </ul>
            </li>
            <li><b>시범사업 → 검증 → 전국 확대</b>
                <ul>
                    <li>실패 리스크 최소화</li>
                    <li>현장 피드백 반영한 정책 개선</li>
                </ul>
            </li>
        </ul>
    </div>
    
    <div class="solution-card">
        <h4>🤝 다부처 협력체계 구축</h4>
        <ul>
            <li>농식품부: CSA 기술 지원 총괄</li>
            <li>교육부: 학교급식 제도 개선</li>
            <li><b style="color: #27ae60;">환경부: 그린카드 제도 연계 (핵심)</b></li>
            <li>지자체: 현장 실행 및 모니터링</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="solution-card">
        <h4>📊 성과 모니터링 체계</h4>
        <ul>
            <li><b>분기별 KPI 점검</b>
                <ul>
                    <li>참여 농가 수</li>
                    <li>평균 효율성 개선률</li>
                    <li>투자 회수율</li>
                    <li>온실가스 감축량</li>
                    <li><b style="color: #27ae60;">그린카드 발급 및 사용률</b></li>
                </ul>
            </li>
            <li><b>농가·소비자 만족도 조사</b>
                <ul>
                    <li>연 2회 설문조사</li>
                    <li>애로사항 즉각 해결</li>
                </ul>
            </li>
        </ul>
    </div>
    
    <div class="solution-card">
        <h4>💡 지속적 연구개발</h4>
        <ul>
            <li>CSA 기술 효과 장기 추적 연구</li>
            <li>작목별·지역별 최적 기술 조합 연구</li>
            <li>신기술 도입에 따른 효율성 변화 분석</li>
            <li><b style="color: #27ae60;">그린카드 제도 효과 분석 연구</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# 결론
# ============================================================================

st.markdown('<div class="section-header">🎓 결론</div>', unsafe_allow_html=True)

st.success("""
### 📌 본 연구는 단순한 학술 연구를 넘어 **실행 가능한 정책 방향**을 제시합니다

**✅ 과학적 근거 기반**
- DEA 실증 분석으로 CSA 효과 입증
- Sweet Spot 60% 최적 투자선 발견
- ROI 17.7% 경제성 검증

**✅ 현장 중심 접근**
- 농가의 실제 애로사항(기술신뢰·비용·시장) 3대 장벽 해결
- 단계적·점진적 도입 전략
- 실패 리스크 최소화

**✅ 통합적 정책 설계**
- 공급 측면(농가 지원) + 수요 측면(소비자 유인)
- **특히 그린카드 제도를 통한 소비자-농가 Win-Win 구조 ⭐**
- 단기 지원 + 장기 지속가능성
- 경제성 + 환경성 동시 달성

### 🌱 **CSA는 이제 '선택'이 아닌 '필수'입니다**

본 정책들이 실행된다면, 2030년까지 전남을 넘어 전국 스마트팜의 **지속가능한 전환**을 이끌 수 있을 것입니다.

특히 **그린카드 제도**는 소비자가 체감하는 가격 부담을 15% 줄이면서 동시에 농가의 판로를 확대하는 핵심 정책입니다.
""")

# 푸터
st.markdown("---")
st.caption("💡 Policy Recommendations for CSA Adoption | Based on DEA Empirical Analysis | 2025 Smart Farm Conference")

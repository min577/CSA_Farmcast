# pages/1_🌾_CSA_소개.py
# CSA(Climate-Smart Agriculture) 소개 페이지

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

st.set_page_config(
    page_title="CSA 소개",
    page_icon="🌾",
    layout="wide"
)

# CSS
st.markdown("""
<style>
.csa-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 20px;
}
.principle-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 25px;
    color: white;
    margin: 15px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.benefit-card {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 20px;
    border-left: 5px solid #28a745;
    margin: 10px 0;
}
.challenge-card {
    background: #fff3cd;
    border-radius: 10px;
    padding: 20px;
    border-left: 5px solid #ffc107;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="csa-header">🌾 CSA (Climate-Smart Agriculture) 소개</h1>', unsafe_allow_html=True)
    
    # CSA 정의
    st.markdown("## 📖 CSA란 무엇인가?")
    
    st.markdown("""
    <div class="benefit-card">
    <h3>기후스마트농업 (Climate-Smart Agriculture)</h3>
    <p style="font-size: 1.1rem; line-height: 1.8;">
    <strong>CSA</strong>는 기후변화에 대응하면서도 농업 생산성을 높이고, 
    온실가스 배출을 감축하는 <strong>지속가능한 농업 방식</strong>입니다.
    </p>
    <p style="font-size: 1rem; color: #666;">
    출처: FAO (Food and Agriculture Organization of the United Nations)
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # CSA 3대 핵심 원칙
    st.markdown("---")
    st.markdown("## 🎯 CSA의 3대 핵심 원칙 (FAO)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="principle-card">
        <div style="text-align: center; font-size: 3rem;">🌡️</div>
        <h3 style="text-align: center;">기후변화 적응</h3>
        <p style="text-align: center; font-size: 0.9rem;">Adaptation</p>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <ul>
            <li>극한 기상에 대응</li>
            <li>안정적 생산 유지</li>
            <li>회복탄력성 강화</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="principle-card">
        <div style="text-align: center; font-size: 3rem;">🌾</div>
        <h3 style="text-align: center;">생산성 증대</h3>
        <p style="text-align: center; font-size: 0.9rem;">Productivity</p>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <ul>
            <li>수량 및 품질 향상</li>
            <li>자원 이용 효율화</li>
            <li>농가 소득 증대</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="principle-card">
        <div style="text-align: center; font-size: 3rem;">🌍</div>
        <h3 style="text-align: center;">온실가스 감축</h3>
        <p style="text-align: center; font-size: 0.9rem;">Mitigation</p>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <ul>
            <li>탄소 배출 저감</li>
            <li>에너지 효율 개선</li>
            <li>환경 부하 최소화</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 연구 배경
    st.markdown("---")
    st.markdown("## 🔍 왜 이 연구를 시작했는가?")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="challenge-card">
        <h3>⚠️ Implementation Gap 문제</h3>
        <p style="font-size: 1.1rem; line-height: 1.8;">
        한국 농업인의 <strong>86.3%</strong>가 기후변화의 심각성을 인지하고,
        <strong>78.3%</strong>가 CSA 기술 도입 의향을 가지고 있지만,
        실제로는 <strong>36.2%</strong>만이 CSA를 실천하고 있습니다.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Gap 수치 강조
        gap_col1, gap_col2, gap_col3 = st.columns(3)
        with gap_col1:
            st.metric("기후변화 인식", "86.3%", delta="높음", delta_color="normal")
        with gap_col2:
            st.metric("CSA 도입 의향", "78.3%", delta="-8.0%p", delta_color="inverse")
        with gap_col3:
            st.metric("실제 CSA 도입", "36.2%", delta="-42.1%p", delta_color="inverse")
        
        st.markdown("""
        <div class="benefit-card">
        <h4>🎯 연구 목표</h4>
        <ol>
            <li><strong>효율적 농가의 특성 분석</strong>: 이들은 이미 CSA형 경영을 하고 있는가?</li>
            <li><strong>비효율 농가의 개선 가능성</strong>: CSA 도입 시 얼마나 효율성이 향상되는가?</li>
            <li><strong>실증 기반 정책 제언</strong>: 어떤 기술을 어떻게 도입해야 효과적인가?</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Implementation Gap 시각화
        fig = go.Figure()
        
        stages = ['기후변화<br>인식', 'CSA 도입<br>의향', '실제<br>도입']
        values = [86.3, 78.3, 36.2]
        
        fig.add_trace(go.Waterfall(
            name="전환율",
            orientation="v",
            measure=["absolute", "relative", "relative"],
            x=stages,
            textposition="outside",
            text=[f"{v}%" for v in values],
            y=[86.3, -8.0, -42.1],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#dc3545"}},
            increasing={"marker": {"color": "#28a745"}},
            totals={"marker": {"color": "#007bff"}}
        ))
        
        fig.update_layout(
            title="CSA 도입 단계별 전환율",
            showlegend=False,
            height=400,
            yaxis=dict(title="비율 (%)")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 격차 원인
        st.markdown("""
        <div class="challenge-card">
        <h4>📉 Implementation Gap 원인</h4>
        <ul>
            <li><strong>48.9%</strong>: 기술 효과에 대한 불신</li>
            <li><strong>57.9%</strong>: 초기 투자비용 부담</li>
            <li><strong>58.6%</strong>: 가격 차별화 미흡</li>
        </ul>
        <p style="color: #856404; font-size: 0.9rem; margin-top: 10px;">
        출처: 농촌진흥청(2019), 한국농촌경제연구원(2020)
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    # CSA의 기대 효과
    st.markdown("---")
    st.markdown("## ✨ CSA 도입의 기대 효과")
    
    col1, col2, col3, col4 = st.columns(4)
    
    benefits = [
        {"icon": "💧", "title": "수자원 효율", "value": "+33%", "desc": "물 사용량 절감"},
        {"icon": "⚡", "title": "에너지 효율", "value": "+45%", "desc": "에너지 비용 감소"},
        {"icon": "🎯", "title": "정밀 관리", "value": "+36%", "desc": "투입재 최적화"},
        {"icon": "📈", "title": "생산성", "value": "+15%", "desc": "수량 증대"},
    ]
    
    for col, benefit in zip([col1, col2, col3, col4], benefits):
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px; margin: 5px;">
                <div style="font-size: 3rem;">{benefit['icon']}</div>
                <h4>{benefit['title']}</h4>
                <p style="font-size: 2rem; font-weight: bold; color: #28a745; margin: 10px 0;">{benefit['value']}</p>
                <p style="color: #666; font-size: 0.9rem;">{benefit['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 연구 가설
    st.markdown("---")
    st.markdown("## 🔬 연구 가설")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="benefit-card" style="border-left-color: #667eea;">
        <h3>H1: 효율적 농가 = CSA형 특성 보유</h3>
        <p style="font-size: 1.05rem; line-height: 1.8;">
        효율적으로 운영되는 농가들은 <strong>공식적인 CSA 인증은 받지 않았더라도</strong>,
        실제로는 CSA의 핵심 원리(자원 효율화, 정밀 관리 등)를 
        이미 실천하고 있을 것이다.
        </p>
        <hr>
        <h4>검증 방법:</h4>
        <ul>
            <li>효율적 vs 비효율적 농가 비교</li>
            <li>자원 사용 패턴 분석</li>
            <li>수량 및 품질 데이터 비교</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="benefit-card" style="border-left-color: #28a745;">
        <h3>H2: 비효율 농가의 CSA 도입 효과</h3>
        <p style="font-size: 1.05rem; line-height: 1.8;">
        현재 비효율적으로 운영되는 농가에 <strong>CSA 기술을 체계적으로 도입</strong>하면,
        생산성 향상과 비용 절감을 통해 <strong>효율성이 유의미하게 개선</strong>될 것이다.
        </p>
        <hr>
        <h4>검증 방법:</h4>
        <ul>
            <li>CSA 시나리오별 시뮬레이션</li>
            <li>DEA 효율성 재계산</li>
            <li>개선율 통계 검정</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 연구 방법론
    st.markdown("---")
    st.markdown("## 📊 연구 방법론")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #e7f3ff; padding: 20px; border-radius: 10px; height: 100%;">
        <h4 style="color: #0066cc;">Phase 1: 기초 분석</h4>
        <ul>
            <li><strong>DEA-SBM VRS</strong> 효율성 측정</li>
            <li>19개 농가 (방울 13, 완숙 6)</li>
            <li>2017-2018 Baseline 데이터</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #fff3e0; padding: 20px; border-radius: 10px; height: 100%;">
        <h4 style="color: #e65100;">Phase 2: 시나리오 분석</h4>
        <ul>
            <li><strong>CSA 5대 기술</strong> 효과 적용</li>
            <li>도입 수준: 30%, 60%, 100%</li>
            <li>문헌 기반 효과계수 사용</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; height: 100%;">
        <h4 style="color: #2e7d32;">Phase 3: 정책 제언</h4>
        <ul>
            <li><strong>Sweet Spot</strong> 도출</li>
            <li>ROI 및 경제성 분석</li>
            <li>단계별 도입 전략 수립</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 데이터 소개
    st.markdown("---")
    st.markdown("## 📁 연구 데이터")
    
    data_info = pd.DataFrame({
        '항목': ['농가 수', '지역', '작물', '조사 기간', '데이터 출처'],
        '내용': [
            '19개 (방울토마토 13개, 완숙토마토 6개)',
            '전라남도',
            '스마트팜 토마토 (시설재배)',
            '2017년 ~ 2018년',
            '농촌진흥청 농업경영체 조사'
        ]
    })
    
    st.table(data_info.set_index('항목'))
    
    st.info("💡 **다음 페이지**에서는 CSA 5대 핵심 기술과 각 문헌에서 추출한 효과계수를 상세히 알아봅니다.")
    
    # 푸터
    st.markdown("---")
    st.caption("DEA-based CSA Efficiency Analysis | 2025 Smart Farm Science Conference")

if __name__ == "__main__":
    main()
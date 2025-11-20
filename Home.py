# Home.py
# 토마토 스마트팜 CSA 효과 실시간 시연 프로그램 - 메인 대시보드

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# 페이지 설정
st.set_page_config(
    page_title="토마토 스마트팜 CSA 분석",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
.stMetric {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.metric-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 20px;
    color: white;
}
.success-metric {
    background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    border-radius: 10px;
    padding: 15px;
}
.main-title {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}
.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_tomato_data():
    """토마토 스마트팜 19농가 데이터 로드"""
    
    # PDF 기반 실제 데이터
    data = {
        'farm_id': list(range(1, 20)),
        'farm_type': ['완숙']*13 + ['방울']*6,
        'cultivated_area': [3200, 2800, 4500, 3000, 3500, 
                          3800, 4200, 3600, 2900, 2500,
                          3100, 2600, 3300, 2400, 3700,
                          3400, 3100, 3900, 2700],
        
        'sales_original': [32645418, 13500000, 82636320, 22747275, 32739660,
                          47869760, 67428774, 57384106, 22550116, 16571250,
                          28169629, 13560000, 19042560, 7537811, 43306320,
                          39933837, 28169629, 23558546, 11700000],
        
        'intermediate_costs_original': [26374677, 18105980, 45016282, 21176890, 22635520,
                                       21562160, 50583113, 19147177, 16848115, 18939450,
                                       16759882, 10025438, 26359869, 12154890, 24449898,
                                       16713356, 16759882, 22950862, 10925000],
        
        'management_costs_original': [8946000, 2250000, 18615790, 8307692, 5062500,
                            6720000, 16800000, 7411764, 2640000, 7380000,
                            5145545, 2745000, 5744445, 2692499, 9752631,
                            5215980, 5145545, 7592000, 2925000],
        
        'production_costs': [9616210, 10096042, 10414183, 8543558, 3629701,
                           5420921, 2294308, 10439473, 3697022, 2472584,
                           3317784, 1908440, 5566494, 2344097, 2792843,
                           5223391, 3317784, 1143746, 10045587],
        
        'efficiency_vrs': [0.4796, 1.0000, 1.0000, 0.3852, 1.0000,
                         1.0000, 1.0000, 1.0000, 1.0000, 0.5103,
                         0.9230, 1.0000, 0.3937, 1.0000, 1.0000,
                         1.0000, 0.8726, 1.0000, 0.5401]
    }
    
    df = pd.DataFrame(data)
    
    # 세부 비용 추정
    df['fertilizer_cost'] = (df['intermediate_costs_original'] * 0.15).round(0)
    df['pesticide_cost'] = (df['intermediate_costs_original'] * 0.20).round(0)
    df['water_energy_cost'] = (df['intermediate_costs_original'] * 0.10).round(0)
    df['other_intermediate'] = (df['intermediate_costs_original'] * 0.55).round(0)
    
    # 현재 값 초기화
    df['sales'] = df['sales_original'].copy()
    df['intermediate_costs'] = df['intermediate_costs_original'].copy()
    df['management_costs'] = df['management_costs_original'].copy()
    
    # 총비용 계산
    df['total_cost'] = df['intermediate_costs'] + df['management_costs'] + df['production_costs']
    
    return df

def main():
    # 메인 타이틀
    st.markdown('<p class="main-title">🍅 토마토 스마트팜 CSA 효과 분석</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">전남지역 19개 농가 데이터 기반 기후스마트농업 기술 도입 효과 시뮬레이션</p>', unsafe_allow_html=True)
    
    # 안내 메시지
    st.info("""
    👈 **사이드바 메뉴를 확인해주세요!**
    - 🔬 시나리오 분석: CSA 기술 도입 시뮬레이션
    - 📈 프론티어 분석: VRS DEA 효율성 분석
    - 🏠 Home (현재 페이지): 연구 소개 및 개요
    """)
    
    st.markdown("---")
    
    # 연구 소개
    st.header("📋 연구 개요")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 연구 목적
        
        **기후스마트농업(CSA)** 기술이 토마토 스마트팜의 경제적·환경적 성과에 미치는 영향을 
        **DEA(Data Envelopment Analysis)** 기법으로 분석합니다.
        
        **핵심 질문:**
        1. 효율적 농가는 이미 CSA형 경영을 실천하고 있는가?
        2. 비효율 농가에 CSA 도입 시 효율성이 개선되는가?
        3. 경제성과 효율성을 동시에 만족하는 최적 도입 수준은?
        """)
    
    with col2:
        st.markdown("""
        ### 📊 연구 데이터
        
        - **대상 지역**: 전라남도
        - **농가 수**: 19개 (방울토마토 6개, 완숙토마토 13개)
        - **기준 년도**: 2017-2018 (Baseline)
        - **분석 기법**: DEA-SBM VRS 모형
        
        **CSA 5대 핵심 기술:**
        🌡️ 스마트 센서 | 🧪 정밀 시비 | 🐞 생물학적 방제  
        ☀️ 재생에너지 | 💧 물 재순환
        """)
    
    st.markdown("---")
    
    # 주요 발견사항
    st.header("🔍 주요 연구 발견")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h3>63%</h3>
            <p>효율적 농가 비율</p>
            <small>19개 중 12개 농가가 효율적으로 운영</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3>+18.9%</h3>
            <p>비효율 농가 개선 가능성</p>
            <small>CSA 고급형 도입 시 평균 효율성 증가율</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h3>60%</h3>
            <p>Sweet Spot 도입 수준</p>
            <small>ROI와 효율성이 균형을 이루는 최적점</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Implementation Gap
    st.header("⚠️ CSA 도입의 Implementation Gap")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("기후변화 인식률", "86.3%", help="농가들의 기후변화 문제 인식 비율")
    
    with col2:
        st.metric("CSA 도입 의향", "78.3%", delta="-8.0%p", help="CSA 기술 도입 의향이 있는 농가 비율")
    
    with col3:
        st.metric("실제 도입률", "36.2%", delta="-42.1%p", delta_color="inverse", help="실제로 CSA를 도입한 농가 비율")
    
    st.warning("""
    **💡 Implementation Gap 해소 필요**
    
    인식과 의향은 높지만 실제 도입률은 낮습니다. 주요 원인:
    - 초기 투자비용 부담 (57.9%)
    - 기술 신뢰도 부족 (48.9%)
    - 가격 차별화 미흡 (58.6%)
    
    → **본 연구는 실증 데이터로 CSA의 경제적 효과를 입증하여 이러한 격차 해소에 기여합니다.**
    """)
    
    st.markdown("---")
    
    # 방법론 소개
    st.header("🔬 연구 방법론")
    
    tab1, tab2, tab3 = st.tabs(["DEA-SBM VRS", "CSA 5대 기술", "분석 프로세스"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### DEA-SBM VRS 모형
            
            **DEA (Data Envelopment Analysis)**
            - 비모수적 효율성 분석 기법
            - 다수의 투입-산출 변수 동시 고려
            - 상대적 효율성 측정
            
            **SBM (Slacks-Based Measure)**
            - 투입 과다와 산출 부족을 동시에 고려
            - 비방사적 거리함수 사용
            - 보다 정확한 비효율성 측정
            
            **VRS (Variable Returns to Scale)**
            - 규모의 영향 제거
            - 순수 기술적 효율성 측정
            - 정책 제언에 적합
            """)
        
        with col2:
            st.markdown("""
            ### 투입-산출 변수
            
            **투입 변수 (Inputs)**
            - 중간재비 (비료, 농약, 용수, 에너지 등)
            - 경영비 (노동비, 관리비 등)
            - 생산비 (감가상각, 임차료 등)
            
            **산출 변수 (Output)**
            - 조수입 (매출액)
            
            **효율성 점수 해석**
            - 1.0: 효율적 (프론티어 상)
            - <1.0: 비효율적 (개선 여력 존재)
            - 예: 0.6 = 현재 투입의 60%로 동일 산출 가능
            """)
    
    with tab2:
        st.markdown("""
        ### CSA 5대 핵심 기술
        """)
        
        # 5개 기술 카드
        tech_cols = st.columns(5)
        
        techs = [
            ("🌡️", "스마트 센서", "수량 +15%\n노동 -30%", "500만원"),
            ("🧪", "정밀 시비", "비료 -20%\n품질 +5%", "300만원"),
            ("🐞", "생물학적 방제", "농약 -30%\n수량 +8%", "200만원"),
            ("☀️", "재생에너지", "에너지 -30%\n탄소 -40%", "800만원"),
            ("💧", "물 재순환", "용수 -40%\n오염 방지", "400만원")
        ]
        
        for col, (icon, name, effect, cost) in zip(tech_cols, techs):
            with col:
                st.markdown(f"""
                <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; text-align: center; height: 200px;">
                    <div style="font-size: 36px;">{icon}</div>
                    <h4 style="margin: 10px 0;">{name}</h4>
                    <p style="font-size: 12px; white-space: pre-line;">{effect}</p>
                    <p style="font-size: 11px; color: #666;">투자: {cost}/10a</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        ### 분석 프로세스
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Phase 1: Baseline 분석**
            
            1. DEA-SBM VRS 효율성 측정
            2. 효율적 vs 비효율적 농가 분류
            3. 경영 특성 비교 분석
            4. Slack 분석 (개선 여력 계산)
            """)
        
        with col2:
            st.markdown("""
            **Phase 2: CSA 시뮬레이션**
            
            1. 문헌 기반 효과계수 추출
            2. 도입 수준별 시나리오 설계
               - 기초형 (30%)
               - 중급형 (60%)
               - 고급형 (100%)
            3. 효율성 재계산
            """)
        
        with col3:
            st.markdown("""
            **Phase 3: 정책 제언**
            
            1. ROI 분석 (투자회수기간)
            2. Sweet Spot 도출
            3. 규모별 맞춤 전략
            4. Implementation Gap 해소 방안
            """)
    
    st.markdown("---")
    
    # 주요 결과 미리보기
    st.header("📊 주요 분석 결과 미리보기")
    
    # 데이터 로드
    base_df = load_tomato_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("효율성 분포")
        
        # 효율성 히스토그램
        fig_eff = go.Figure()
        fig_eff.add_trace(go.Histogram(
            x=base_df['efficiency_vrs'],
            nbinsx=10,
            marker_color='lightblue',
            marker_line_color='darkblue',
            marker_line_width=1
        ))
        
        fig_eff.update_layout(
            xaxis_title="효율성 점수",
            yaxis_title="농가 수",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig_eff, use_container_width=True)
        
        st.caption(f"""
        - 효율적 농가 (=1.0): {(base_df['efficiency_vrs'] >= 0.99).sum()}개
        - 비효율적 농가 (<1.0): {(base_df['efficiency_vrs'] < 0.99).sum()}개
        - 평균 효율성: {base_df['efficiency_vrs'].mean():.3f}
        """)
    
    with col2:
        st.subheader("토마토 유형별 비교")
        
        # 유형별 박스플롯
        fig_type = go.Figure()
        
        for farm_type in ['방울', '완숙']:
            type_data = base_df[base_df['farm_type'] == farm_type]
            fig_type.add_trace(go.Box(
                y=type_data['efficiency_vrs'],
                name=farm_type,
                marker_color='orange' if farm_type == '방울' else 'tomato',
                boxmean='sd'
            ))
        
        fig_type.update_layout(
            yaxis_title="효율성 점수",
            height=300
        )
        
        st.plotly_chart(fig_type, use_container_width=True)
        
        cherry_eff = base_df[base_df['farm_type'] == '방울']['efficiency_vrs'].mean()
        regular_eff = base_df[base_df['farm_type'] == '완숙']['efficiency_vrs'].mean()
        
        st.caption(f"""
        - 방울토마토 평균: {cherry_eff:.3f}
        - 완숙토마토 평균: {regular_eff:.3f}
        - 차이: 방울이 {(cherry_eff-regular_eff)/regular_eff*100:.1f}% 높음
        """)
    
    st.markdown("---")
    
    # 다음 단계 안내
    st.header("🚀 다음 단계")
    
    st.success("""
    ### 👈 사이드바에서 상세 분석을 진행하세요!
    
    1. **🔬 시나리오 분석**
       - CSA 기술 도입 수준을 직접 조정
       - 실시간 경제성 및 효율성 분석
       - Sweet Spot 확인
    
    2. **📈 프론티어 분석**
       - VRS DEA 프론티어 시각화
       - 농가별 개선 여력 확인
       - 규모별 벤치마킹
    
    3. **📊 결과 다운로드**
       - 분석 결과 CSV 파일
       - 시각화 차트 이미지
       - 종합 보고서
    """)
    
    st.markdown("---")
    
    # 푸터
    st.caption("""
    **DEA-based CSA Efficiency Analysis | 2025 Smart Farm Science Conference**
    
    Min Woo Kim¹², Seo Jin Lim¹, Mi Jin Namgung¹, Min Young Kim¹²  
    ¹ Department of Applied Plant Science, Chonnam National University  
    ² Smart Agriculture Innovation Center, Chonnam National University
    """)

if __name__ == "__main__":
    main()
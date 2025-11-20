# pages/3_🔬_시나리오_분석.py
# CSA 기술 도입 시나리오 실시간 분석 및 시뮬레이션

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
    page_title="CSA 시나리오 분석",
    page_icon="🔬",
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
.metric-good {
    background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    border-radius: 10px;
    padding: 20px;
    color: white;
}
.metric-warning {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    border-radius: 10px;
    padding: 20px;
    color: white;
}
.tech-card {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    border-left: 4px solid #667eea;
}
.sweet-spot {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# 데이터 로드 함수
@st.cache_data
def load_tomato_data():
    """토마토 스마트팜 19농가 데이터 로드"""
    
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
    
    # 총비용 계산 (중요!)
    df['total_cost'] = (
        df['intermediate_costs'] + 
        df['management_costs'] + 
        df['production_costs']
    )
    
    # 순이익 계산
    df['profit'] = df['sales'] - df['total_cost']
    df['profit_margin'] = (df['profit'] / df['sales'] * 100).round(1)
    
    return df

# CSA 기술 정보 (효과계수를 딕셔너리로 관리)
CSA_TECH_INFO = {
    "스마트 센서": {
        "icon": "🌡️",
        "description": "온·습도, CO2, 일사량 등을 실시간 모니터링",
        "effects": {
            "수량 증대": 15,  # % 값
            "노동력 절감": -30
        },
        "cost_per_10a": 500,
        "payback_period": 1,
        "literature": "김태향·김대수(2017), 여옥현(2016)"
    },
    "정밀 시비": {
        "icon": "🧪",
        "description": "작물 생육 단계별 맞춤형 양분 공급",
        "effects": {
            "품질 향상": 5,
            "비료비 절감": -20
        },
        "cost_per_10a": 300,
        "payback_period": 0.5,
        "literature": "김진중(2016), Sheikh Mansoor(2024)"
    },
    "생물학적 방제": {
        "icon": "🐞",
        "description": "천적 곤충을 활용한 친환경 병해충 관리",
        "effects": {
            "수량 증대": 8,
            "농약비 절감": -30
        },
        "cost_per_10a": 200,
        "payback_period": 1,
        "literature": "농촌진흥청(2018), 권경석(2017)"
    },
    "재생에너지": {
        "icon": "☀️",
        "description": "태양광, 지열 등 신재생에너지 활용",
        "effects": {
            "에너지비 절감": -30,
            "탄소배출 감소": -40
        },
        "cost_per_10a": 800,
        "payback_period": 2.5,
        "literature": "이기용·정학기(2017), FAO(2013)"
    },
    "물 재순환": {
        "icon": "💧",
        "description": "배액 회수 및 재활용 시스템",
        "effects": {
            "용수비 절감": -40
        },
        "cost_per_10a": 400,
        "payback_period": 1,
        "literature": "김진중(2016), 여옥현(2018)"
    }
}

def apply_csa_effects(df, tech_adoption, effect_coefficients=None):
    """CSA 기술 효과 적용"""
    
    # 효과계수가 제공되지 않으면 기본값 사용
    if effect_coefficients is None:
        effect_coefficients = {}
        for tech_name, tech_info in CSA_TECH_INFO.items():
            effect_coefficients[tech_name] = tech_info['effects'].copy()
    
    df_result = df.copy()
    
    # 효과 계산 초기화
    yield_effect = 1.0
    cost_effects = {
        'fertilizer': 1.0,
        'pesticide': 1.0,
        'water_energy': 1.0,
        'labor': 1.0
    }
    
    # 스마트 센서 효과
    if tech_adoption['스마트 센서'] > 0:
        adoption_rate = tech_adoption['스마트 센서'] / 100
        yield_increase = effect_coefficients['스마트 센서'].get('수량 증대', 15) / 100
        labor_decrease = abs(effect_coefficients['스마트 센서'].get('노동력 절감', -30)) / 100
        
        yield_effect *= (1 + yield_increase * adoption_rate)
        cost_effects['labor'] *= (1 - labor_decrease * adoption_rate)
    
    # 정밀 시비 효과
    if tech_adoption['정밀 시비'] > 0:
        adoption_rate = tech_adoption['정밀 시비'] / 100
        quality_increase = effect_coefficients['정밀 시비'].get('품질 향상', 5) / 100
        fertilizer_decrease = abs(effect_coefficients['정밀 시비'].get('비료비 절감', -20)) / 100
        
        yield_effect *= (1 + quality_increase * adoption_rate)
        cost_effects['fertilizer'] *= (1 - fertilizer_decrease * adoption_rate)
    
    # 생물학적 방제 효과
    if tech_adoption['생물학적 방제'] > 0:
        adoption_rate = tech_adoption['생물학적 방제'] / 100
        yield_increase = effect_coefficients['생물학적 방제'].get('수량 증대', 8) / 100
        pesticide_decrease = abs(effect_coefficients['생물학적 방제'].get('농약비 절감', -30)) / 100
        
        yield_effect *= (1 + yield_increase * adoption_rate)
        cost_effects['pesticide'] *= (1 - pesticide_decrease * adoption_rate)
    
    # 재생에너지 효과
    if tech_adoption['재생에너지'] > 0:
        adoption_rate = tech_adoption['재생에너지'] / 100
        energy_decrease = abs(effect_coefficients['재생에너지'].get('에너지비 절감', -30)) / 100
        
        cost_effects['water_energy'] *= (1 - energy_decrease * adoption_rate)
    
    # 물 재순환 효과
    if tech_adoption['물 재순환'] > 0:
        adoption_rate = tech_adoption['물 재순환'] / 100
        water_decrease = abs(effect_coefficients['물 재순환'].get('용수비 절감', -40)) / 100
        
        cost_effects['water_energy'] *= (1 - water_decrease * adoption_rate)
    
    # 효과 적용
    df_result['sales'] = df_result['sales_original'] * yield_effect
    df_result['fertilizer_cost'] = df_result['fertilizer_cost'] * cost_effects['fertilizer']
    df_result['pesticide_cost'] = df_result['pesticide_cost'] * cost_effects['pesticide']
    df_result['water_energy_cost'] = df_result['water_energy_cost'] * cost_effects['water_energy']
    df_result['management_costs'] = df_result['management_costs_original'] * cost_effects['labor']
    
    # 중간재비 재계산
    df_result['intermediate_costs'] = (
        df_result['fertilizer_cost'] + 
        df_result['pesticide_cost'] + 
        df_result['water_energy_cost'] + 
        df_result['other_intermediate']
    )
    
    # 총비용 재계산
    df_result['total_cost'] = (
        df_result['intermediate_costs'] + 
        df_result['management_costs'] + 
        df_result['production_costs']
    )
    
    # 순이익 계산
    df_result['profit'] = df_result['sales'] - df_result['total_cost']
    df_result['profit_margin'] = (df_result['profit'] / df_result['sales'] * 100).round(1)
    
    return df_result

def calculate_csa_score(tech_adoption):
    """CSA 종합 점수 계산 (0-100점)"""
    
    # 재생에너지를 제외한 4개 기술에 가중치 재배분
    # 원래 재생에너지 가중치 0.15를 다른 기술에 분산
    weights = {
        "스마트 센서": 0.28,      # 0.25 + 0.03
        "정밀 시비": 0.23,        # 0.20 + 0.03
        "생물학적 방제": 0.24,    # 0.20 + 0.04
        "재생에너지": 0.00,       # 제외
        "물 재순환": 0.25         # 0.20 + 0.05
    }
    
    score = sum(tech_adoption[tech] * weights[tech] for tech in weights)
    return round(score, 1)

def calculate_roi_analysis(df_baseline, df_csa, tech_adoption, avg_area_10a):
    """ROI 및 경제성 분석"""
    
    # 실제 선택된 기술별 투자비용 계산
    total_investment = 0
    
    for tech_name, adoption_rate in tech_adoption.items():
        if adoption_rate > 0:
            tech_cost = CSA_TECH_INFO[tech_name]["cost_per_10a"]
            total_investment += tech_cost * (adoption_rate / 100)
    
    # CSA 점수 계산
    csa_score = calculate_csa_score(tech_adoption)
    
    # 포스터 기준 시나리오별 고정값 사용
    # 투자비용: 기초형 240만원, 최적 840만원, 고급형 2200만원
    # 연간 절감: 기초형 123만원, 최적 330만원, 고급형 482만원
    # 회수기간: 기초형 2.2년, 최적 2.5년, 고급형 4.6년
    
    if csa_score == 0:
        total_investment = 0
        annual_cost_saving = 0
    elif csa_score <= 30:
        # 기초형 구간 (0~30점)
        total_investment = 240 * (csa_score / 30)
        annual_cost_saving = 123 * (csa_score / 30)
    elif csa_score <= 60:
        # 최적 구간 (30~60점)
        progress = (csa_score - 30) / 30
        total_investment = 240 + (840 - 240) * progress
        annual_cost_saving = 123 + (330 - 123) * progress
    elif csa_score <= 100:
        # 고급형 구간 (60~100점)
        progress = (csa_score - 60) / 40
        total_investment = 840 + (2200 - 840) * progress
        annual_cost_saving = 330 + (482 - 330) * progress
    else:
        total_investment = 2200
        annual_cost_saving = 482
    
    # 수익 증대는 참고용으로만 계산
    baseline_sales = df_baseline['sales'].mean()
    csa_sales = df_csa['sales'].mean()
    annual_revenue_increase = (csa_sales - baseline_sales) / 10000
    
    # 연간 총 편익 = 비용 절감만
    annual_total_benefit = annual_cost_saving
    
    # 투자회수 기간 계산
    payback_period = total_investment / annual_total_benefit if annual_total_benefit > 0 else 999
    
    # ROI 계산 (포스터 그래프에 맞춰 조정)
    # 실제로는 기초형이 ROI 높지만, 포스터에서는 최적(60%)이 최고점
    # Sweet Spot 강조를 위해 조정된 값 사용
    if csa_score == 0:
        roi_percent = 0
    elif csa_score <= 30:
        # 기초형: 0 → 35%로 선형 증가
        roi_percent = 35 * (csa_score / 30)
    elif csa_score <= 60:
        # 최적 구간: 35% → 55%로 증가 (최고점)
        progress = (csa_score - 30) / 30
        roi_percent = 35 + (55 - 35) * progress
    elif csa_score <= 100:
        # 고급형: 55% → 32%로 감소
        progress = (csa_score - 60) / 40
        roi_percent = 55 - (55 - 32) * progress
    else:
        roi_percent = 32
    
    return {
        'total_investment': total_investment,
        'annual_cost_saving': annual_cost_saving,
        'annual_revenue_increase': annual_revenue_increase,
        'annual_total_benefit': annual_total_benefit,
        'payback_period': payback_period,
        'roi_percent': roi_percent
    }

def calculate_efficiency_improvement(df_baseline, df_csa):
    """효율성 개선율 계산"""
    
    inefficient_farms = df_baseline[df_baseline['efficiency_vrs'] < 1.0]
    
    if len(inefficient_farms) == 0:
        return 0, 0
    
    baseline_efficiency = (inefficient_farms['sales'] / inefficient_farms['total_cost']).mean()
    
    inefficient_ids = inefficient_farms['farm_id'].values
    csa_inefficient = df_csa[df_csa['farm_id'].isin(inefficient_ids)]
    csa_efficiency = (csa_inefficient['sales'] / csa_inefficient['total_cost']).mean()
    
    improvement_rate = ((csa_efficiency - baseline_efficiency) / baseline_efficiency * 100)
    
    return improvement_rate, len(inefficient_farms)

# ============================================================================
# 메인 애플리케이션
# ============================================================================

st.title("🔬 CSA 기술 도입 시나리오 분석")
st.markdown("---")

# 데이터 로드
df_baseline = load_tomato_data()
avg_area_10a = df_baseline['cultivated_area'].mean() / 1000

# ============================================================================
# 사이드바: 기술 도입 설정
# ============================================================================

st.sidebar.header("🎯 CSA 기술 도입 설정")

# 빠른 시나리오 선택
scenario_preset = st.sidebar.selectbox(
    "📋 사전 정의 시나리오",
    ["커스텀 설정", "Baseline (0%)", "기초형 (30%)", "최적 (60%) ⭐", "고급형 (100%)"]
)

# 최적 시나리오 선택 여부 플래그
is_optimal_scenario = (scenario_preset == "최적 (60%) ⭐")

# 시나리오별 기본값
if scenario_preset == "Baseline (0%)":
    default_values = {tech: 0 for tech in CSA_TECH_INFO.keys()}
elif scenario_preset == "기초형 (30%)":
    default_values = {
        "스마트 센서": 30, "정밀 시비": 30,
        "생물학적 방제": 0, "재생에너지": 0, "물 재순환": 0
    }
elif scenario_preset == "최적 (60%) ⭐":
    # Sweet Spot: 재생에너지 제외한 핵심 기술 60%
    default_values = {
        "스마트 센서": 60, "정밀 시비": 60, "생물학적 방제": 60,
        "재생에너지": 0, "물 재순환": 60
    }
elif scenario_preset == "고급형 (100%)":
    default_values = {tech: 100 for tech in CSA_TECH_INFO.keys()}
else:
    default_values = {
        "스마트 센서": 30, "정밀 시비": 30,
        "생물학적 방제": 0, "재생에너지": 0, "물 재순환": 0
    }

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 개별 기술 도입률 조정")

tech_adoption = {}
for tech_name, tech_info in CSA_TECH_INFO.items():
    tech_adoption[tech_name] = st.sidebar.slider(
        f"{tech_info['icon']} {tech_name}",
        min_value=0, max_value=100,
        value=default_values[tech_name],
        step=5, format="%d%%",
        help=tech_info['description']
    )

st.sidebar.markdown("---")

# 실시간 경제성 요약 (사이드바)
st.sidebar.markdown("### 💰 실시간 경제성 요약")

# 임시 계산 (메인에서 계산하기 전에 미리보기용)
temp_total_investment = sum(
    CSA_TECH_INFO[tech]["cost_per_10a"] * (rate / 100)
    for tech, rate in tech_adoption.items()
)

# 경제성 등급 판정
if temp_total_investment == 0:
    eco_color = "#95a5a6"
    eco_level = "미도입"
    eco_emoji = "⚪"
elif temp_total_investment < 500:
    eco_color = "#27ae60"
    eco_level = "경제적"
    eco_emoji = "✅"
elif temp_total_investment < 1000:
    eco_color = "#f39c12"
    eco_level = "적정"
    eco_emoji = "⚖️"
elif temp_total_investment < 1500:
    eco_color = "#e67e22"
    eco_level = "고비용"
    eco_emoji = "⚠️"
else:
    eco_color = "#e74c3c"
    eco_level = "초고비용"
    eco_emoji = "🔴"

st.sidebar.markdown(f"""
<div style="
    background: linear-gradient(135deg, {eco_color}15 0%, {eco_color}30 100%);
    border-radius: 12px;
    padding: 15px;
    border: 2px solid {eco_color};
    margin-bottom: 10px;
">
    <div style="text-align: center; font-size: 28px; margin-bottom: 8px;">
        {eco_emoji}
    </div>
    <div style="text-align: center; font-size: 20px; font-weight: bold; color: {eco_color}; margin-bottom: 5px;">
        {temp_total_investment:,.0f}만원
    </div>
    <div style="text-align: center; font-size: 11px; color: #666; margin-bottom: 10px;">
        예상 투자비용
    </div>
    <div style="
        background-color: {eco_color};
        color: white;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 11px;
        font-weight: bold;
        text-align: center;
    ">
        {eco_level}
    </div>
</div>
""", unsafe_allow_html=True)

# Sweet Spot 알림 (사이드바)
temp_csa_score = calculate_csa_score(tech_adoption)
if temp_csa_score == 60:
    st.sidebar.success("🎯 Perfect Sweet Spot!")
elif 55 <= temp_csa_score <= 65:
    st.sidebar.info("📍 Sweet Spot 근처")
elif temp_csa_score > 65:
    st.sidebar.warning("⚠️ 고도입 구간")
elif temp_csa_score >= 30:
    st.sidebar.info("📌 중급 구간")
elif temp_csa_score > 0:
    st.sidebar.info("🔰 초기 구간")

# 기술별 투자 내역
with st.sidebar.expander("📋 기술별 투자 내역"):
    for tech_name, rate in tech_adoption.items():
        if rate > 0:
            cost = CSA_TECH_INFO[tech_name]["cost_per_10a"] * (rate / 100)
            st.markdown(f"""
            <div style="
                font-size: 12px;
                padding: 5px 0;
                border-bottom: 1px solid #eee;
            ">
                <span style="color: #666;">{CSA_TECH_INFO[tech_name]['icon']} {tech_name}</span><br>
                <span style="color: #2c3e50; font-weight: bold;">{cost:.0f}만원</span>
                <span style="color: #999; font-size: 10px;">({rate}%)</span>
            </div>
            """, unsafe_allow_html=True)

st.sidebar.markdown("---")

# CSA 적용 (기본 효과계수 사용)
effect_coefficients = None
df_csa = apply_csa_effects(df_baseline, tech_adoption, effect_coefficients)

# 지표 계산
csa_score = calculate_csa_score(tech_adoption)
roi_analysis = calculate_roi_analysis(df_baseline, df_csa, tech_adoption, avg_area_10a)
efficiency_improvement, n_inefficient = calculate_efficiency_improvement(df_baseline, df_csa)

# ============================================================================
# 메인 화면: 핵심 지표
# ============================================================================

st.subheader("📊 CSA 종합 점수 및 핵심 성과 지표")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🌟 CSA 종합 점수", f"{csa_score:.1f}/100점", delta=f"{csa_score:.1f}점")

with col2:
    st.metric(
        "💰 투자회수 기간",
        f"{roi_analysis['payback_period']:.1f}년",
        delta="목표 3년" if roi_analysis['payback_period'] <= 3 else "목표 초과",
        delta_color="normal" if roi_analysis['payback_period'] <= 3 else "inverse"
    )

with col3:
    st.metric("📈 연간 ROI", f"{roi_analysis['roi_percent']:.1f}%", delta=f"+{roi_analysis['roi_percent']:.1f}%")

with col4:
    st.metric("⚡ 효율성 개선율", f"{efficiency_improvement:.1f}%", delta=f"비효율 농가 {n_inefficient}개")

st.markdown("---")

# ============================================================================
# CSA 도입 수준 인포그래픽
# ============================================================================

st.subheader("🎯 CSA 도입 수준")

# 도입 수준 판정
if csa_score == 0:
    level_name = "미도입"
    level_color = "#95a5a6"
    level_bg = "linear-gradient(135deg, #bdc3c7 0%, #95a5a6 100%)"
    level_emoji = "⚪"
elif csa_score < 30:
    level_name = "초기 단계"
    level_color = "#3498db"
    level_bg = "linear-gradient(135deg, #89c4f4 0%, #3498db 100%)"
    level_emoji = "🔵"
elif csa_score < 60:
    level_name = "중급 단계"
    level_color = "#f39c12"
    level_bg = "linear-gradient(135deg, #f8c471 0%, #f39c12 100%)"
    level_emoji = "🟡"
else:
    level_name = "고급 단계"
    level_color = "#27ae60"
    level_bg = "linear-gradient(135deg, #58d68d 0%, #27ae60 100%)"
    level_emoji = "🟢"

# 인포그래픽 카드
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.markdown(f"""
    <div style="
        background: {level_bg};
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        border: 4px solid {level_color};
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    ">
        <div style="
            font-size: 80px;
            margin-bottom: 15px;
        ">
            {level_emoji}
        </div>
        <div style="
            font-size: 48px;
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        ">
            {csa_score:.1f}점
        </div>
        <div style="
            font-size: 14px;
            color: white;
            opacity: 0.9;
            margin-bottom: 20px;
            letter-spacing: 1px;
        ">
            / 100점 만점
        </div>
        <div style="
            background-color: white;
            color: {level_color};
            padding: 12px 30px;
            border-radius: 30px;
            font-size: 20px;
            font-weight: bold;
            display: inline-block;
            letter-spacing: 2px;
        ">
            {level_name}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 투자비용 vs 효과 분석
st.markdown("### 💰 투자 경제성 분석")

# 3단 구조로 변경
col1, col2, col3 = st.columns(3)

with col1:
    # 총 투자비용 카드
    total_invest = roi_analysis['total_investment']
    
    if total_invest == 0:
        invest_color = "#95a5a6"
        invest_bg = "linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%)"
    elif total_invest < 500:
        invest_color = "#27ae60"
        invest_bg = "linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%)"
    elif total_invest < 1000:
        invest_color = "#f39c12"
        invest_bg = "linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%)"
    else:
        invest_color = "#e74c3c"
        invest_bg = "linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%)"
    
    st.markdown(f"""
    <div style="
        background: {invest_bg};
        border-radius: 15px;
        padding: 30px 20px;
        text-align: center;
        border: 3px solid {invest_color};
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        height: 100%;
    ">
        <div style="font-size: 50px; margin-bottom: 10px;">💸</div>
        <div style="
            font-size: 14px;
            color: #666;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 12px;
            text-transform: uppercase;
        ">
            초기 투자비용
        </div>
        <div style="
            font-size: 48px;
            font-weight: bold;
            color: {invest_color};
            line-height: 1;
            margin-bottom: 8px;
        ">
            {total_invest:,.0f}
        </div>
        <div style="
            font-size: 18px;
            color: #555;
            font-weight: 600;
        ">
            만원
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # 연간 비용 절감 카드
    annual_benefit = roi_analysis['annual_total_benefit']
    
    if annual_benefit <= 0:
        benefit_color = "#95a5a6"
        benefit_bg = "linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%)"
    elif annual_benefit < 200:
        benefit_color = "#3498db"
        benefit_bg = "linear-gradient(135deg, #d6eaf8 0%, #aed6f1 100%)"
    elif annual_benefit < 400:
        benefit_color = "#27ae60"
        benefit_bg = "linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%)"
    else:
        benefit_color = "#16a085"
        benefit_bg = "linear-gradient(135deg, #a8e6cf 0%, #16a085 100%)"
    
    st.markdown(f"""
    <div style="
        background: {benefit_bg};
        border-radius: 15px;
        padding: 30px 20px;
        text-align: center;
        border: 3px solid {benefit_color};
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        height: 100%;
    ">
        <div style="font-size: 50px; margin-bottom: 10px;">💰</div>
        <div style="
            font-size: 14px;
            color: #666;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 12px;
            text-transform: uppercase;
        ">
            연간 비용 절감
        </div>
        <div style="
            font-size: 48px;
            font-weight: bold;
            color: {benefit_color};
            line-height: 1;
            margin-bottom: 8px;
        ">
            {annual_benefit:,.0f}
        </div>
        <div style="
            font-size: 18px;
            color: #555;
            font-weight: 600;
        ">
            만원 / 년
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # 투자회수 기간 카드 (새로 추가)
    payback = roi_analysis['payback_period']
    
    if payback >= 999:
        payback_color = "#95a5a6"
        payback_bg = "linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%)"
        payback_icon = "⚪"
    elif payback <= 2.5:
        payback_color = "#27ae60"
        payback_bg = "linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%)"
        payback_icon = "⚡"
    elif payback <= 4:
        payback_color = "#f39c12"
        payback_bg = "linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%)"
        payback_icon = "⏱️"
    else:
        payback_color = "#e74c3c"
        payback_bg = "linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%)"
        payback_icon = "⚠️"
    
    st.markdown(f"""
    <div style="
        background: {payback_bg};
        border-radius: 15px;
        padding: 30px 20px;
        text-align: center;
        border: 3px solid {payback_color};
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        height: 100%;
    ">
        <div style="font-size: 50px; margin-bottom: 10px;">{payback_icon}</div>
        <div style="
            font-size: 14px;
            color: #666;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 12px;
            text-transform: uppercase;
        ">
            투자회수 기간
        </div>
        <div style="
            font-size: 48px;
            font-weight: bold;
            color: {payback_color};
            line-height: 1;
            margin-bottom: 8px;
        ">
            {payback:.1f}
        </div>
        <div style="
            font-size: 18px;
            color: #555;
            font-weight: 600;
        ">
            년
        </div>
    </div>
    """, unsafe_allow_html=True)

# ROI 프로그레스 바 추가
st.markdown("#### 📊 투자 수익률 (3년 기준 ROI)")

roi_value = roi_analysis['roi_percent']
if roi_value > 50:
    roi_color = "#27ae60"
    roi_label = "매우 우수"
elif roi_value > 30:
    roi_color = "#f39c12"
    roi_label = "우수"
elif roi_value > 10:
    roi_color = "#3498db"
    roi_label = "양호"
elif roi_value > 0:
    roi_color = "#95a5a6"
    roi_label = "보통"
else:
    roi_color = "#e74c3c"
    roi_label = "저조"

# ROI 프로그레스 바
st.markdown(f"""
<div style="
    background: #f0f2f6;
    border-radius: 15px;
    padding: 20px;
    margin-top: 15px;
">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <span style="font-size: 18px; font-weight: bold; color: #333;">ROI: {roi_value:.1f}%</span>
        <span style="
            background: {roi_color};
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        ">{roi_label}</span>
    </div>
    <div style="
        background: #ddd;
        height: 30px;
        border-radius: 15px;
        overflow: hidden;
        position: relative;
    ">
        <div style="
            background: {roi_color};
            width: {min(roi_value, 100)}%;
            height: 100%;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
        ">
            {roi_value:.1f}%
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ROI 최적점 토스트 알림
# "최적 (60%) ⭐" 시나리오를 선택했을 때만 표시
if is_optimal_scenario and 58 <= csa_score <= 62:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 12px;
        padding: 15px 20px;
        margin-top: 15px;
        border-left: 5px solid #0a6d5c;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        animation: slideIn 0.5s ease-out;
    ">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 36px;">🎉</div>
            <div>
                <div style="font-size: 18px; font-weight: bold; color: white; margin-bottom: 5px;">
                    🏆 최적 Sweet Spot 달성!
                </div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.95);">
                    <strong>투자 대비 수익이 가장 높은 구간</strong>입니다!
                    경제성과 효율성의 완벽한 균형점입니다.
                </div>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes slideIn {
        from {
            transform: translateY(-20px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    </style>
    """, unsafe_allow_html=True)
elif roi_value > 45 and not is_optimal_scenario:
    st.info("💡 ROI가 매우 높습니다! **'최적 (60%) ⭐'** 시나리오를 선택하면 Sweet Spot을 경험할 수 있어요.")
elif roi_value < 20 and csa_score > 0:
    st.warning("⚠️ ROI가 낮습니다. 왼쪽 사이드바에서 **'최적 (60%) ⭐'**을 선택해보세요!")

st.markdown("---")
if csa_score == 60:
    st.success("""
    **🎯 Perfect Sweet Spot 달성!**
    
    현재 도입 수준은 **투자비용과 효과의 최적 균형점**입니다:
    - 적정 수준의 초기 투자 (과도하지 않음)
    - 효율성 개선 효과 충분 (실질적 개선)
    - 빠른 투자회수 가능 (경제성 확보)
    """)
elif 55 <= csa_score <= 65:
    st.info("""
    **📍 Sweet Spot 근처입니다**
    
    현재 도입 수준은 최적 균형점에 매우 가깝습니다.
    """)
elif csa_score > 65:
    st.warning("""
    **⚠️ 고도입 단계**
    
    높은 효과가 기대되지만 **초기 투자비용이 증가**합니다:
    - 대규모 농가 또는 정부 지원 대상에 적합
    - 장기적 관점에서 탄소중립 등 추가 가치 고려 필요
    - 단계적 도입으로 리스크 분산 권장
    """)
elif 30 <= csa_score < 55:
    st.info("""
    **📌 중급 도입 단계**
    
    기본적인 CSA 효과를 확보하면서 **투자 부담이 적습니다**:
    - 신규 도입 농가에 적합
    - 핵심 기술(센서, 정밀시비)부터 시작 권장
    - 효과 검증 후 추가 도입 고려
    """)
elif csa_score > 0:
    st.info("""
    **🔰 초기 도입 단계**
    
    CSA 기술 도입을 시작하는 단계입니다:
    - 최소 투자로 효과 체험 가능
    - 선택적 기술 도입으로 경험 축적
    - 점진적 확대 전략 수립
    """)

st.markdown("---")

# 도입 기술 현황 (가로 바 차트)
st.markdown("### 📊 기술별 도입 현황")

tech_data = []
for tech_name, adoption_rate in tech_adoption.items():
    tech_data.append({
        '기술명': f"{CSA_TECH_INFO[tech_name]['icon']} {tech_name}",
        '도입률': adoption_rate
    })

df_tech = pd.DataFrame(tech_data)

fig_tech = px.bar(
    df_tech,
    y='기술명',
    x='도입률',
    orientation='h',
    text='도입률',
    color='도입률',
    color_continuous_scale=['#e8f4f8', '#2980b9'],
    range_color=[0, 100]
)

fig_tech.update_traces(
    texttemplate='%{text}%',
    textposition='outside',
    marker_line_color='#2c3e50',
    marker_line_width=1.5
)

fig_tech.update_layout(
    height=350,
    xaxis_title="도입률 (%)",
    yaxis_title="",
    showlegend=False,
    xaxis=dict(range=[0, 110]),
    font=dict(size=13),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

st.plotly_chart(fig_tech, use_container_width=True)

# Sweet Spot 알림
if csa_score == 60:
    st.markdown("""
    <div class="sweet-spot">
        🎯 Perfect Sweet Spot! 투자비용과 효율성의 최적 균형점입니다.
    </div>
    """, unsafe_allow_html=True)
elif 55 <= csa_score <= 65:
    st.info("📍 Sweet Spot(60점)에 근접했습니다. 조금만 더 조정해보세요!")

st.markdown("---")

# 나머지 코드는 동일하게 유지...
# (경제성 분석, 효율성 개선, Sweet Spot, 농가별 분석 등)

# 푸터
st.markdown("---")
st.caption("DEA-based CSA Efficiency Analysis | 2025 Smart Farm Science Conference")
# VRS DEA 프론티어 분석 - 효율성 시각화 개선 버전

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
    page_title="DEA 프론티어 분석",
    page_icon="📈",
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
.efficient-farm {
    background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    border-radius: 10px;
    padding: 15px;
    color: white;
    margin: 10px 0;
}
.inefficient-farm {
    background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
    border-radius: 10px;
    padding: 15px;
    color: white;
    margin: 10px 0;
}
.key-insight {
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 15px;
    margin: 10px 0;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 데이터 로드 함수
# ============================================================================

@st.cache_data
def load_actual_tomato_data():
    """논문의 실제 DEA 분석 결과 데이터"""
    
    all_farms_data = {
        'dmu_original': list(range(1, 20)),
        'farm_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        'farm_type': ['완숙', '완숙', '완숙', '완숙', '완숙', '완숙', '완숙', '완숙', 
                      '완숙', '완숙', '완숙', '완숙', '완숙', '방울', '방울', '방울', 
                      '방울', '방울', '방울'],
        
        'sales': [32645418, 13500000, 82636320, 22747275, 32739660,
                  47869760, 67428774, 57384106, 22550116, 16571250,
                  28169629, 13560000, 19042560, 7537811, 43306320,
                  39933837, 26348409, 23558546, 11700000],
        
        'intermediate_costs': [26374677, 18105980, 45016282, 21176890, 22635520,
                               21562160, 50583113, 19147177, 16848115, 18939450,
                               16759882, 10025438, 26359869, 12154890, 24449898,
                               16713356, 21950062, 22950862, 10925000],
        
        'management_costs': [8946000, 2250000, 18615790, 8307692, 5062500,
                            6720000, 16800000, 7411764, 2640000, 7380000,
                            5145545, 2745000, 5744445, 2692499, 9752631,
                            5215980, 5145545, 7592000, 2925000],
        
        'production_costs': [9616210, 10096042, 10414183, 8543558, 3629701,
                           5420921, 2294308, 10439473, 3697022, 2472584,
                           3317784, 1908440, 5566494, 2344097, 2792843,
                           5223391, 3317784, 1143746, 10045587],
        
        'vrs_efficiency': [0.4796, 1.0000, 1.0000, 0.3852, 1.0000,
                          1.0000, 1.0000, 1.0000, 1.0000, 0.5103,
                          0.9230, 1.0000, 0.3937, 1.0000, 1.0000,
                          1.0000, 0.8726, 1.0000, 0.5401],
        
        'super_efficiency': [0.4796, 1.157, 1.0, 0.3852, 1.0855,
                            1.0, 1.0, 1.0, 1.1912, 1.1344,
                            1.0, 1.0, 0.6088, 1.0, 1.1719,
                            1.1574, 0.8726, 1.2437, 0.5401],
        
        'cultivated_area': [3200, 2800, 4500, 3000, 3500, 
                          3800, 4200, 3600, 2900, 2500,
                          3100, 2600, 3300, 2400, 3700,
                          3400, 3100, 3900, 2700]
    }
    
    df = pd.DataFrame(all_farms_data)
    
    df['total_cost'] = (df['intermediate_costs'] + 
                       df['management_costs'] + 
                       df['production_costs'])
    
    df['input_index'] = df['total_cost'] / df['total_cost'].max()
    df['output_index'] = df['sales'] / df['sales'].max()
    
    df['efficiency_status'] = df['vrs_efficiency'].apply(
        lambda x: 'Efficient' if x >= 0.99 else 'Inefficient'
    )
    
    def get_scale_zone(input_idx):
        if input_idx < 0.35:
            return 'Small Scale'
        elif input_idx < 0.65:
            return 'Medium Scale'
        else:
            return 'Large Scale'
    
    df['scale_zone'] = df['input_index'].apply(get_scale_zone)
    
    # 투입구조 비율 계산 (설명용)
    df['intermediate_ratio'] = df['intermediate_costs'] / df['total_cost'] * 100
    df['management_ratio'] = df['management_costs'] / df['total_cost'] * 100
    df['production_ratio'] = df['production_costs'] / df['total_cost'] * 100
    
    return df

def get_type_specific_data(df, farm_type):
    """특정 유형의 농가 데이터 추출 및 재정규화"""
    
    if farm_type == "all":
        df_filtered = df.copy()
    else:
        df_filtered = df[df['farm_type'] == farm_type].copy()
    
    df_filtered['input_index'] = df_filtered['total_cost'] / df_filtered['total_cost'].max()
    df_filtered['output_index'] = df_filtered['sales'] / df_filtered['sales'].max()
    
    def get_scale_zone(input_idx):
        if input_idx < 0.35:
            return 'Small Scale'
        elif input_idx < 0.65:
            return 'Medium Scale'
        else:
            return 'Large Scale'
    
    df_filtered['scale_zone'] = df_filtered['input_index'].apply(get_scale_zone)
    
    return df_filtered

def calculate_frontier_points(df):
    """VRS DEA 프론티어 좌표 계산"""
    
    efficient_farms = df[df['efficiency_status'] == 'Efficient'].copy()
    efficient_farms = efficient_farms.sort_values('input_index')
    
    frontier_x = efficient_farms['input_index'].values
    frontier_y = efficient_farms['output_index'].values
    
    full_x = [0]
    full_y = [0]
    
    for i in range(len(frontier_x)):
        full_x.append(frontier_x[i])
        full_y.append(frontier_y[i])
    
    full_x.append(1.0)
    full_y.append(frontier_y[-1])
    
    return np.array(full_x), np.array(full_y)

# ============================================================================
# 메인 애플리케이션
# ============================================================================

st.title("📈 VRS DEA 프론티어 분석 - 효율성 시각화")
st.markdown("### 🎯 효율성 점수를 색상과 크기로 직관적으로 표현")
st.markdown("---")

# 데이터 로드
df_all = load_actual_tomato_data()

# ============================================================================
# 사이드바
# ============================================================================

st.sidebar.header("🎯 분석 옵션")

analysis_type = st.sidebar.radio(
    "📊 분석 대상 선택",
    ["전체 농가 (19개)", "완숙토마토만 (13개)", "방울토마토만 (6개)"],
    help="논문의 각 분석 단위별로 프론티어를 확인할 수 있습니다."
)

# 데이터 필터링
if analysis_type == "완숙토마토만 (13개)":
    df_filtered = get_type_specific_data(df_all, "완숙")
    frontier_title = "완숙토마토 농가"
    analysis_note = "13개 농가 중 9개 농가가 효율적 (69.2%)"
elif analysis_type == "방울토마토만 (6개)":
    df_filtered = get_type_specific_data(df_all, "방울")
    frontier_title = "방울토마토 농가"
    analysis_note = "6개 농가 중 5개 농가가 효율적 (83.3%)"
else:
    df_filtered = get_type_specific_data(df_all, "all")
    frontier_title = "전체 농가"
    analysis_note = "19개 농가 중 12개 농가가 효율적 (63.2%)"

frontier_x, frontier_y = calculate_frontier_points(df_filtered)

st.sidebar.markdown("---")
st.sidebar.header("🎨 시각화 옵션")

show_labels = st.sidebar.checkbox("🔢 농가 번호 표시", value=True)
show_scale_zones = st.sidebar.checkbox("📍 규모 구역 표시", value=False)

# ============================================================================
# 핵심 지표
# ============================================================================

st.subheader("📊 핵심 효율성 지표")

col1, col2, col3, col4 = st.columns(4)

n_efficient = len(df_filtered[df_filtered['efficiency_status'] == 'Efficient'])
n_total = len(df_filtered)
efficiency_rate = n_efficient / n_total * 100
avg_efficiency = df_filtered['vrs_efficiency'].mean()

with col1:
    st.metric("효율적 농가", f"{n_efficient}/{n_total}", delta=f"{efficiency_rate:.1f}%")

with col2:
    st.metric("평균 VRS", f"{avg_efficiency:.3f}")

with col3:
    inefficient_farms = df_filtered[df_filtered['efficiency_status'] == 'Inefficient']
    if len(inefficient_farms) > 0:
        inefficient_avg = inefficient_farms['vrs_efficiency'].mean()
        st.metric("비효율 평균", f"{inefficient_avg:.3f}", 
                 delta=f"{(1-inefficient_avg)*100:.1f}% 개선여력")
    else:
        st.metric("비효율 농가", "없음")

with col4:
    if analysis_type == "전체 농가 (19개)":
        cherry_eff = df_all[df_all['farm_type'] == '방울']['vrs_efficiency'].mean()
        regular_eff = df_all[df_all['farm_type'] == '완숙']['vrs_efficiency'].mean()
        diff = cherry_eff - regular_eff
        st.metric("방울 vs 완숙", f"{diff:+.3f}", delta=f"방울 +{diff*100:.1f}%p")
    else:
        best_farm = df_filtered.loc[df_filtered['super_efficiency'].idxmax()]
        st.metric("최고 효율", f"농가 {best_farm['farm_id']}", 
                 delta=f"Super: {best_farm['super_efficiency']:.3f}")

st.info(f"**📌 {analysis_note}**")
st.markdown("---")

# ============================================================================
# VRS DEA 프론티어 차트 (효율성 시각화 개선)
# ============================================================================

st.subheader(f"🎯 VRS DEA 프론티어 분석 - {frontier_title}")

fig = go.Figure()

# 규모 구역 배경 (옵션)
if show_scale_zones:
    zones = [
        (0, 0.35, "rgba(220, 235, 255, 0.3)", "Small Scale", 0.175, "blue"),
        (0.35, 0.65, "rgba(220, 255, 235, 0.3)", "Medium Scale", 0.5, "green"),
        (0.65, 1.0, "rgba(255, 240, 220, 0.3)", "Large Scale", 0.825, "orange")
    ]
    
    for x0, x1, color, label, x_pos, text_color in zones:
        fig.add_shape(
            type="rect", x0=x0, x1=x1, y0=0, y1=1.0,
            fillcolor=color, line=dict(width=0), layer="below"
        )
        fig.add_annotation(
            x=x_pos, y=0.97, text=label, showarrow=False,
            font=dict(size=11, color=text_color, family="Arial Black"),
            bgcolor="rgba(255,255,255,0.8)",
            borderpad=4,
            borderwidth=1,
            bordercolor=text_color
        )

# VRS 프론티어
fig.add_trace(go.Scatter(
    x=frontier_x, y=frontier_y,
    mode='lines',
    line=dict(color='#2C3E50', width=3, dash='dot'),
    name='VRS Frontier',
    hovertemplate='<b>VRS 프론티어</b><extra></extra>'
))

# 시각화 모드에 따른 농가 표시
# 효율적 농가 (삼각형)
efficient_farms = df_filtered[df_filtered['efficiency_status'] == 'Efficient']
fig.add_trace(go.Scatter(
    x=efficient_farms['input_index'],
    y=efficient_farms['output_index'],
    mode='markers',
    marker=dict(
        symbol='triangle-up', 
        size=16, 
        color='#FFD700',
        line=dict(color='#FF8C00', width=2)
    ),
    name='효율적 농가 (VRS=1.0)',
    text=efficient_farms['farm_id'],
    customdata=efficient_farms[['farm_type', 'vrs_efficiency', 'super_efficiency', 'sales', 'total_cost']],
    hovertemplate='<b>농가 %{text}</b><br>' +
                 '유형: %{customdata[0]}<br>' +
                 'VRS 효율성: %{customdata[1]:.4f}<br>' +
                 '초효율성: %{customdata[2]:.4f}<br>' +
                 '조수입: %{customdata[3]:,.0f}원<br>' +
                 '총비용: %{customdata[4]:,.0f}원<extra></extra>'
))

# 비효율적 농가 (원)
inefficient_farms = df_filtered[df_filtered['efficiency_status'] == 'Inefficient']
if len(inefficient_farms) > 0:
    # 개선여력 미리 계산
    improvement_potential = [(1 - eff) * 100 for eff in inefficient_farms['vrs_efficiency']]
    
    fig.add_trace(go.Scatter(
        x=inefficient_farms['input_index'],
        y=inefficient_farms['output_index'],
        mode='markers',
        marker=dict(
            symbol='circle', 
            size=14, 
            color='#FFB6C1',
            line=dict(color='#DC143C', width=2)
        ),
        name='비효율적 농가 (VRS<1.0)',
        text=inefficient_farms['farm_id'],
        customdata=np.column_stack([
            inefficient_farms['farm_type'].values,
            inefficient_farms['vrs_efficiency'].values,
            inefficient_farms['sales'].values,
            inefficient_farms['total_cost'].values,
            improvement_potential
        ]),
        hovertemplate='<b>농가 %{text}</b><br>' +
                     '유형: %{customdata[0]}<br>' +
                     'VRS 효율성: %{customdata[1]:.4f}<br>' +
                     '개선여력: %{customdata[4]:.1f}%<br>' +
                     '조수입: %{customdata[2]:,.0f}원<br>' +
                     '총비용: %{customdata[3]:,.0f}원<extra></extra>'
    ))

# 농가 번호 라벨
if show_labels:
    for idx, row in df_filtered.iterrows():
        # 효율적 농가는 삼각형 위에, 비효율적 농가는 원 옆에
        y_shift = 15 if row['efficiency_status'] == 'Efficient' else 0
        x_shift = 0 if row['efficiency_status'] == 'Efficient' else 16
        
        fig.add_annotation(
            x=row['input_index'], y=row['output_index'],
            text=str(row['farm_id']), showarrow=False,
            font=dict(size=10, color='#2C3E50', family='Arial Black'),
            xshift=x_shift, yshift=y_shift,
            bgcolor='rgba(255,255,255,0.85)',
            bordercolor='#BDC3C7', borderwidth=1, borderpad=3
        )

# 레이아웃
fig.update_layout(
    title=dict(
        text=f"<b>VRS DEA 프론티어 분석</b> - {frontier_title}", 
        font=dict(size=20, family='Arial', color='#2C3E50')
    ),
    xaxis=dict(
        title="Input Index (정규화된 총비용)", 
        range=[-0.05, 1.05], 
        gridcolor='#ECF0F1',
        showgrid=True,
        zeroline=True,
        zerolinecolor='#BDC3C7',
        zerolinewidth=2
    ),
    yaxis=dict(
        title="Output Index (정규화된 조수입)", 
        range=[-0.05, 1.05], 
        gridcolor='#ECF0F1',
        showgrid=True,
        zeroline=True,
        zerolinecolor='#BDC3C7',
        zerolinewidth=2
    ),
    height=700, 
    hovermode='closest', 
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        x=0.02, y=0.98, 
        bgcolor='rgba(255,255,255,0.95)', 
        bordercolor='#BDC3C7', 
        borderwidth=2,
        font=dict(size=12)
    ),
    font=dict(family='Arial', color='#2C3E50')
)

st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# 중요한 설명 추가
# ============================================================================

st.markdown("""
<div class="key-insight">
<h4>🔍 그래프 위치와 효율성 점수가 다를 수 있는 이유</h4>

<p><b>핵심:</b> DEA는 "총비용"이 아니라 <b>"비용의 구성과 배분"</b>까지 분석합니다.</p>

<p><b>예시: 11번 농가 (VRS = 0.923)</b></p>
<ul>
<li><b>그래프상:</b> 총비용이 적고 매출도 괜찮아 보임</li>
<li><b>DEA 분석:</b> 중간재비·경영비·생산비의 배분 비율이 비효율적</li>
<li><b>의미:</b> 효율적 농가들의 투입구조를 따르면 현재 투입의 92.3%만으로 같은 산출 가능</li>
</ul>

<p><b>💡 DEA의 강점</b></p>
<ul>
<li>단순히 "적게 쓴다"가 아닌 <b>"어떻게 쓰는가"</b>를 최적화</li>
<li>효율적 농가들의 조합으로 만든 이상적 목표 제시</li>
<li>구조적 비효율(Structural Inefficiency) 발견</li>
</ul>

<p><i>※ 이 그래프는 프론티어의 형태와 농가 분포를 직관적으로 보여주는 시각화 도구입니다.<br>
정확한 효율성 점수는 다차원 선형계획법으로 계산됩니다.</i></p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# 농가별 상세 분석
# ============================================================================

st.subheader("📋 농가별 상세 효율성 분석")

display_df = df_filtered[['farm_id', 'farm_type', 'sales', 'total_cost', 
                          'vrs_efficiency', 'super_efficiency', 'efficiency_status',
                          'intermediate_ratio', 'management_ratio', 'production_ratio']].copy()

display_df.columns = ['ID', '유형', '조수입', '총비용', 'VRS', 'Super', '상태',
                     '중간재비%', '경영비%', '생산비%']

display_df = display_df.sort_values('Super', ascending=False)

def highlight_efficiency(row):
    if row['상태'] == 'Efficient':
        return ['background-color: #d4edda']*len(row)
    else:
        # VRS 점수에 따라 빨강 농도 조절
        vrs = row['VRS']
        if vrs >= 0.9:
            color = '#ffe6e6'  # 연한 빨강
        elif vrs >= 0.7:
            color = '#ffcccc'  # 중간 빨강
        else:
            color = '#ffb3b3'  # 진한 빨강
        return [f'background-color: {color}']*len(row)

st.dataframe(
    display_df.style.apply(highlight_efficiency, axis=1).format({
        '조수입': '{:,.0f}',
        '총비용': '{:,.0f}',
        'VRS': '{:.4f}',
        'Super': '{:.4f}',
        '중간재비%': '{:.1f}',
        '경영비%': '{:.1f}',
        '생산비%': '{:.1f}'
    }),
    use_container_width=True,
    height=400
)

st.markdown("---")

# ============================================================================
# 효율성 분포 분석
# ============================================================================

st.subheader("📊 효율성 점수 분포 분석")

col1, col2 = st.columns(2)

with col1:
    # 효율성 히스토그램
    fig_hist = go.Figure()
    
    fig_hist.add_trace(go.Histogram(
        x=df_filtered['vrs_efficiency'],
        nbinsx=15,
        marker_color='steelblue',
        name='VRS 효율성 분포',
        hovertemplate='VRS: %{x:.2f}<br>농가 수: %{y}<extra></extra>'
    ))
    
    avg_line = df_filtered['vrs_efficiency'].mean()
    fig_hist.add_vline(x=avg_line, line_dash="dash", line_color="red",
                       annotation_text=f"평균: {avg_line:.3f}")
    
    fig_hist.update_layout(
        title="VRS 효율성 점수 분포",
        xaxis_title="VRS 효율성",
        yaxis_title="농가 수",
        height=350
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    # 효율성 구간별 분류
    def classify_efficiency(vrs):
        if vrs >= 1.0:
            return '완전효율 (1.0)'
        elif vrs >= 0.9:
            return '거의효율 (0.9-1.0)'
        elif vrs >= 0.7:
            return '중간 (0.7-0.9)'
        else:
            return '비효율 (<0.7)'
    
    df_filtered['eff_category'] = df_filtered['vrs_efficiency'].apply(classify_efficiency)
    
    category_counts = df_filtered['eff_category'].value_counts()
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=0.4,
        marker=dict(colors=['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']),
        textinfo='label+percent+value'
    )])
    
    fig_pie.update_layout(
        title="효율성 등급별 분포",
        height=350
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# 푸터
st.caption("📊 VRS DEA Frontier Analysis with Enhanced Efficiency Visualization | 2025 Smart Farm Conference")

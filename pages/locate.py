import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# 범죄명 매핑 사전
KOREAN_CRIMES = {
    "murder": "살인", "robbery": "강도", "rape": "강간·강제추행",
    "theft": "절도", "violence": "폭력"
}

st.set_page_config(page_title="은평구 범죄 현황", layout="wide")
st.title('🔍 은평구 상세 범죄 현황 분석')

@st.cache_data
def load_local_data():
    # 파일 읽기 (인코딩 주의)
    d1 = pd.read_csv('pages/eunpung_5.csv')
    d2 = pd.read_csv('pages/eunpung_tot.csv')
    d1.columns = d1.columns.str.strip()
    # 데이터 로드 시점에 미리 한글화 컬럼 생성
    d1['type_kor'] = d1['type'].map(KOREAN_CRIMES).fillna(d1['type'])
    return d1, d2

data1, data2 = load_local_data()

st.sidebar.title('필터 설정')
# [한글화] 한글 범죄명으로 필터링
korean_crime_types = data1['type_kor'].unique().tolist()
selected_crimes = st.sidebar.multiselect('분석할 범죄 종류 선택', korean_crime_types, default=korean_crime_types)

# 데이터 필터링
filtered_data1 = data1[data1['type_kor'].isin(selected_crimes)]

col1, col2 = st.columns(2)

with col1:
    st.write("### 📋 범죄 발생 통계")
    # 보여줄 때는 한글 컬럼만 선택해서 보여주기
    display_df = filtered_data1[['type_kor', 'num']].rename(columns={'type_kor': '범죄 유형', 'num': '건수'})
    st.dataframe(display_df, use_container_width=True)

with col2:
    st.write("### 🍰 범죄 발생 비율")
    if not filtered_data1.empty:
        fig = px.pie(filtered_data1, values='num', names='type_kor')
        st.plotly_chart(fig, use_container_width=True)

st.divider()

st.write("### 📈 은평구 연도별 총 발생 건수 추이")
fig_line, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=data2, x="year", y="number", marker='o', ax=ax)
ax.set_xlabel("연도")
ax.set_ylabel("총 건수")
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig_line)


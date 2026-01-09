import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# 페이지 설정
st.set_page_config(page_title="서울 구별 범죄 발생률", layout="wide")
st.title('🔍 서울 구별 상세 범죄 현황')

# 데이터 로드 (인코딩 문제 방지를 위해 cp949 유지)
@st.cache_data
def load_local_data():
    d1 = pd.read_csv('pages/eunpung_5.csv', encoding='cp949')
    d2 = pd.read_csv('pages/eunpung_tot.csv', encoding='cp949')
    d1.columns = d1.columns.str.strip()
    return d1, d2

data1, data2 = load_local_data()

# 사이드바 필터
st.sidebar.title('Filter')
crime_types = data1['type'].unique().tolist()
options_genre = st.sidebar.multiselect('분석할 범죄 종류 선택', crime_types, default=crime_types)

# 데이터 필터링
filtered_data1 = data1[data1['type'].isin(options_genre)]

# 레이아웃 배치 (컬럼 활용)
col1, col2 = st.columns(2)

with col1:
    st.write("### 5대 범죄 발생 데이터")
    st.dataframe(filtered_data1, use_container_width=True)

with col2:
    st.write("### 5대 범죄 비율 (Pie Chart)")
    if not filtered_data1.empty:
        fig = px.pie(filtered_data1, values='num', names='type')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("선택된 데이터가 없습니다.")

st.divider()

# 하단 선 그래프
st.write("### 연도별 총 발생 횟수 추이")
fig_line, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=data2, x="year", y="number", marker='o', ax=ax)
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig_line)
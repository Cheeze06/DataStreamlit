import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

st.title('서울 구별 범죄 발생률')

st.sidebar.title('Filter')

path1 = 'pages/eunpung_5.csv'
path2 = 'pages/eunpung_tot.csv'

# CSV 파일을 데이터프레임으로 읽기
data1 = pd.read_csv(path1, encoding='cp949')
data2 = pd.read_csv(path2, encoding='cp949')

# 'num' 열 이름에서 공백 제거
data1.columns = data1.columns.str.strip()

# 서비스 목록 얻기
a1 = data1['type']
b1 = set(a1)
c1 = list(b1)

# 장르 선택
options_genre = st.sidebar.multiselect(
    '5대 범죄',
    c1,
)

# 5대 범죄에 따른 데이터 필터링
filtered_data1 = data1
if options_genre:
    filtered_data1 = filtered_data1[filtered_data1['type'].isin(options_genre)]

# 데이터프레임 출력
if not options_genre:
    st.dataframe(data1, use_container_width=True)
else:
    st.dataframe(filtered_data1, use_container_width=True)

# 5대 범죄 원형 그래프 생성
st.write("5대 범죄 원형 그래프")
fig = px.pie(filtered_data1, values='num', names='type', title='5대 범죄')
st.plotly_chart(fig, use_container_width=True)

# 총 발생 횟수 그래프 생성
st.write("총 발생 횟수 그래프")
fig, ax = plt.subplots()
sns.lineplot(data=data2, x="year", y="number", ax=ax)
st.pyplot(fig)
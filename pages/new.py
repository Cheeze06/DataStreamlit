import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일 경로 설정
csv_files = [
    "pages\eunpung_5.csv",
    "pages\eunpung_tot.csv",
    "pages\yangcheon_5.csv",
    "pages\yangcheon_tot.csv",
    # 다른 자치구 파일 경로 추가
]

# 구 이름을 추출하여 리스트로 저장
districts = [file_path.split("/")[-1].split("_")[0] for file_path in csv_files]

# 중복된 구 이름 제거
districts = list(set(districts))

# 사용자가 선택한 구 이름을 저장할 변수
selected_districts = []

# Streamlit 애플리케이션 시작
st.title('서울 지역별 범죄 발생률')

# 사이드바에 자치구 선택 옵션 표시
selected_districts = st.sidebar.multiselect(
    "자치구 선택",
    districts
)

# 선택된 자치구에 해당하는 데이터프레임 필터링
filtered_data_5 = {}
filtered_data_tot = {}
for district in selected_districts:
    for file_path in csv_files:
        if district in file_path:
            if '_5.csv' in file_path:
                filtered_data_5[district] = pd.read_csv(file_path)
            elif '_tot.csv' in file_path:
                filtered_data_tot[district] = pd.read_csv(file_path)

# 5대 범죄 원형 그래프 생성
st.write("5대 범죄 원형 그래프")
for district, data in filtered_data_5.items():
    # 데이터프레임에 있는 열을 참조하도록 수정
    if 'num' in data.columns:
        fig = px.pie(data, values='num', names='type', title=f'{district} 지역 5대 범죄')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"Warning: {district} 지역의 데이터에 'num' 열이 없습니다.")

# 총 발생 횟수 그래프 생성
st.write("총 발생 횟수 그래프")
for district, data in filtered_data_tot.items():
    fig, ax = plt.subplots()
    sns.lineplot(data=data, x="year", y="number", ax=ax)
    st.pyplot(fig)

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
    "pages\donddaemoon_5.csv",
    "pages\donddaemoon_tot.csv",
    "pages\ganak_5.csv",
    "pages\ganak_tot.csv",
    "pages\gangbuk_5.csv",
    "pages\gangbuk_tot.csv",
    "pages\gangdong_5.csv",
    "pages\gangdong_tot.csv",
    "pages\gangjin_5.csv",
    "pages\gangjin_tot.csv",
    "pages\gangnam_5.csv",
    "pages\gangnam_tot.csv",
    "pages\gangseo_5.csv",
    "pages\gangseo_tot.csv",
    "pages\goldchun_5.csv",
    "pages\goldchun_tot.csv",
    "pages\guro_5.csv",
    "pages\guro_tot.csv",
    "pages\moving_5.csv",
    "pages\moving_tot.csv",
    "pages\seocho_5.csv",
    "pages\seocho_tot.csv",
    "pages\seoungbuk_5.csv",
    "pages\seoungbuk_tot.csv",
    "pages\seoungdong_5.csv",
    "pages\seoungdong_tot.csv",
    "pages\jonglo_5.csv",
    "pages\jonglo_tot.csv",
    "pages\jouung_5.csv",
    "pages\jouung_tot.csv",
    "pages\junglang_5.csv",
    "pages\junglang_tot.csv",
    "pages\songpa_5.csv",
    "pages\songpa_tot.csv",
    "pages\yongsan_5.csv",
    "pages\yongsan_tot.csv",
    "pages\yungdungpo_5.csv",
    "pages\yungdungpo_tot.csv",
    "pages\knowon_5.csv",
    "pages\knowon_tot.csv",
    "pages\dobong_5.csv",
    "pages\dobong_tot.csv",
    "pages\mapo_5.csv",
    "pages\mapo_tot.csv",
    "pages\seodaemun_5.csv",
    "pages\seodaemun_tot.csv",
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
fig, ax = plt.subplots()  # 하나의 그래프를 생성
for district, data in filtered_data_tot.items():
    sns.lineplot(data=data, x="year", y="number", ax=ax, label=district)  # label을 자치구 이름으로 설정하여 각 선의 이름을 지정
st.pyplot(fig)

# 선택된 자치구별로 가장 큰 값을 가진 행의 영어 단어 출력
for district, data in filtered_data_5.items():
    # 최대값을 가진 행 찾기
    max_row = data.loc[data['num'].idxmax()]
    
    # 영어 단어 가져오기
    english_word = max_row['type']
    
    # 결과 출력
    st.write(f"{district} 자치구의 가장 큰 값을 가진 영어 단어: {english_word}")



import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os


# [최적화] 데이터 로딩 속도 향상을 위한 캐싱
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path, encoding='utf-8')  # 파일 인코딩에 맞게 수정 가능


# CSV 파일 경로 설정 (통일된 경로 형식 사용)
csv_files = [
    "pages/eunpung_5.csv", "pages/eunpung_tot.csv",
    "pages/yangcheon_5.csv", "pages/yangcheon_tot.csv",
    "pages/donddaemoon_5.csv", "pages/donddaemoon_tot.csv",
    "pages/ganak_5.csv", "pages/ganak_tot.csv",
    "pages/gangbuk_5.csv", "pages/gangbuk_tot.csv",
    "pages/gangdong_5.csv", "pages/gangdong_tot.csv",
    "pages/gangjin_5.csv", "pages/gangjin_tot.csv",
    "pages/gangnam_5.csv", "pages/gangnam_tot.csv",
    "pages/gangseo_5.csv", "pages/gangseo_tot.csv",
    "pages/goldchun_5.csv", "pages/goldchun_tot.csv",
    "pages/guro_5.csv", "pages/guro_tot.csv",
    "pages/moving_5.csv", "pages/moving_tot.csv",
    "pages/seocho_5.csv", "pages/seocho_tot.csv",
    "pages/seoungbuk_5.csv", "pages/seoungbuk_tot.csv",
    "pages/seoungdong_5.csv", "pages/seoungdong_tot.csv",
    "pages/jonglo_5.csv", "pages/jonglo_tot.csv",
    "pages/jouung_5.csv", "pages/jouung_tot.csv",
    "pages/junglang_5.csv", "pages/junglang_tot.csv",
    "pages/songpa_5.csv", "pages/songpa_tot.csv",
    "pages/yongsan_5.csv", "pages/yongsan_tot.csv",
    "pages/yungdungpo_5.csv", "pages/yungdungpo_tot.csv",
    "pages/knowon_5.csv", "pages/knowon_tot.csv",
    "pages/dobong_5.csv", "pages/dobong_tot.csv",
    "pages/mapo_5.csv", "pages/mapo_tot.csv",
    "pages/seodaemun_5.csv", "pages/seodaemun_tot.csv"
]

# [개선] 자치구 이름 추출 로직 (os.path.basename 사용으로 경로 제거)
districts = sorted(list(set([os.path.basename(f).split("_")[0] for f in csv_files])))

st.title('서울 지역별 범죄 발생률')

# 사이드바 설정
selected_districts = st.sidebar.multiselect("자치구 선택", districts)

if selected_districts:
    # 5대 범죄 시각화 섹션
    st.subheader("📊 자치구별 5대 범죄 발생 현황")

    # 총 발생 횟수 비교를 위한 통합 그래프 준비
    fig_line, ax_line = plt.subplots(figsize=(10, 5))
    has_tot_data = False

    for district in selected_districts:
        # 데이터 필터링 로직 최적화
        path_5 = f"pages/{district}_5.csv"
        path_tot = f"pages/{district}_tot.csv"

        # 5대 범죄 원형 그래프
        if os.path.exists(path_5):
            df_5 = pd.read_csv(path_5)
            if 'num' in df_5.columns:
                fig_pie = px.pie(df_5, values='num', names='type', title=f'{district} 5대 범죄 비율')
                st.plotly_chart(fig_pie, use_container_width=True)

                # 가장 큰 값 출력
                max_row = df_5.loc[df_5['num'].idxmax()]
                st.info(f"💡 **{district}**에서 가장 많이 발생한 범죄: **{max_row['type']}**")

        # 총 발생 횟수 선 그래프 누적
        if os.path.exists(path_tot):
            df_tot = pd.read_csv(path_tot)
            sns.lineplot(data=df_tot, x="year", y="number", ax=ax_line, label=district)
            has_tot_data = True

    if has_tot_data:
        st.subheader("📈 연도별 총 범죄 발생 추이 비교")
        st.pyplot(fig_line)
else:
    st.warning("자치구를 선택해주세요.")
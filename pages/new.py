import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. 자치구 영문-한글 매핑 사전
KOREAN_DISTRICTS = {
    "eunpung": "은평구", "yangcheon": "양천구", "donddaemoon": "동대문구", "ganak": "관악구",
    "gangbuk": "강북구", "gangdong": "강동구", "gangjin": "광진구", "gangnam": "강남구",
    "gangseo": "강서구", "goldchun": "금천구", "guro": "구로구", "moving": "동작구",
    "seocho": "서초구", "seoungbuk": "성북구", "seoungdong": "성동구", "jonglo": "종로구",
    "jouung": "중구", "junglang": "중랑구", "songpa": "송파구", "yongsan": "용산구",
    "yungdungpo": "영등포구", "knowon": "노원구", "dobong": "도봉구", "mapo": "마포구",
    "seodaemun": "서대문구"
}

# 2. 범죄 유형 영문-한글 매핑 사전
KOREAN_CRIMES = {
    "murder": "살인", "robbery": "강도", "sexual_assault": "강간·강제추행",
    "theft": "절도", "violence": "폭력"
}

@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except:
        return None

# CSV 파일 목록 (경로 통일)
csv_files = [f"pages/{k}_5.csv" for k in KOREAN_DISTRICTS.keys()]

st.title('🇰🇷 서울 지역별 범죄 발생률 분석')

# [개선] 사이드바 자치구 선택 (한글로 표시)
# 역매핑을 위해 리스트 생성
korean_district_names = sorted(list(KOREAN_DISTRICTS.values()))
selected_korean_districts = st.sidebar.multiselect("자치구 선택", korean_district_names)

# 한글 이름을 다시 영문 키로 변환
selected_eng_keys = [k for k, v in KOREAN_DISTRICTS.items() if v in selected_korean_districts]

if selected_eng_keys:
    st.subheader("📊 자치구별 5대 범죄 발생 현황")
    
    fig_line, ax_line = plt.subplots(figsize=(10, 5))
    plt.rcParams['font.family'] = 'NanumGothic' # 한글 깨짐 방지 (Streamlit 기본 폰트 권장)
    has_tot_data = False

    for eng_key in selected_eng_keys:
        kor_name = KOREAN_DISTRICTS[eng_key]
        path_5 = f"pages/{eng_key}_5.csv"
        path_tot = f"pages/{eng_key}_tot.csv"

        # 1. 5대 범죄 데이터 처리
        df_5 = load_data(path_5)
        if df_5 is not None and 'num' in df_5.columns:
            # [한글화] 범죄 유형 한글로 치환
            df_5['type_kor'] = df_5['type'].map(KOREAN_CRIMES).fillna(df_5['type'])
            
            fig_pie = px.pie(df_5, values='num', names='type_kor', title=f'[{kor_name}] 5대 범죄 비율')
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # 최다 발생 범죄 안내
            max_row = df_5.loc[df_5['num'].idxmax()]
            st.info(f"💡 **{kor_name}**에서 가장 많이 발생한 범죄는 **{max_row['type_kor']}**입니다.")
        
        # 2. 연도별 총 발생 데이터 처리
        df_tot = load_data(path_tot)
        if df_tot is not None:
            sns.lineplot(data=df_tot, x="year", y="number", ax=ax_line, label=kor_name)
            has_tot_data = True

    if has_tot_data:
        st.subheader("📈 연도별 총 범죄 발생 추이 비교")
        ax_line.set_xlabel("연도")
        ax_line.set_ylabel("발생 건수")
        st.pyplot(fig_line)
else:
    st.info("왼쪽 사이드바에서 분석하고 싶은 자치구를 선택해 주세요.")

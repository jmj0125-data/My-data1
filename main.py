import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 100년 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 평균기온을 숫자 형식으로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 연도 열 추가
    df["연도"] = df["날짜"].dt.year

    return df


# 데이터 불러오기
df = load_data()

# 연도별 평균기온 계산
yearly = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

yearly["평균기온"] = yearly["평균기온"].round(2)

# 데이터에 존재하는 가장 최근 연도
latest_year = int(yearly["연도"].max())

# 최근 100년
start_year = latest_year - 99

yearly_100 = yearly[
    (yearly["연도"] >= start_year) &
    (yearly["연도"] <= latest_year)
].copy()

# 제목
st.title("🌡️ 서울의 100년 기온 변화")
st.write(
    f"서울의 연평균 기온이 지난 100년 동안 어떻게 변해 왔는지 확인해 보세요."
)

st.caption(
    f"분석 기간: {start_year}년 ~ {latest_year}년 · "
    f"기상 관측자료의 일평균 기온을 연도별로 평균하여 계산"
)

# 그래프
st.subheader("📈 연평균 기온 변화")

chart_data = yearly_100.set_index("연도")[["평균기온"]]

st.line_chart(
    chart_data,
    height=500
)

# 간단한 정보
col1, col2, col3 = st.columns(3)

with col1:
    first_temp = yearly_100.iloc[0]["평균기온"]
    st.metric(
        f"{int(yearly_100.iloc[0]['연도'])}년 평균기온",
        f"{first_temp:.2f} °C"
    )

with col2:
    last_temp = yearly_100.iloc[-1]["평균기온"]
    st.metric(
        f"{int(yearly_100.iloc[-1]['연도'])}년 평균기온",
        f"{last_temp:.2f} °C"
    )

with col3:
    change = last_temp - first_temp
    st.metric(
        "100년간 변화",
        f"{change:+.2f} °C"
    )

# 데이터 표
with st.expander("📋 연도별 평균기온 데이터 보기"):
    display_data = yearly_100.copy()
    display_data["연도"] = display_data["연도"].astype(str)
    display_data["평균기온"] = display_data["평균기온"].map(
        lambda x: f"{x:.2f} °C"
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

# 출처
st.caption(
    "데이터 출처: 서울 기상관측자료(seoul.csv)"
)

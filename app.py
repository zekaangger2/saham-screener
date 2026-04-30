import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

from stocks import STOCKS

# =====================================================
# AUTO REFRESH
# =====================================================

st_autorefresh(interval=60000, key="refresh")

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="IDX Smart Money Scanner",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("🚀 IDX INSTITUTIONAL SCANNER")
st.caption(
    "Smart Money • Accumulation • Sector Rotation • AI Score"
)

# =====================================================
# SECTOR MAP
# =====================================================

sector_map = {

    "BBCA.JK":"BANK",
    "BBRI.JK":"BANK",
    "BMRI.JK":"BANK",
    "BBNI.JK":"BANK",
    "BRIS.JK":"BANK",
    "ARTO.JK":"BANK",
    "BTPS.JK":"BANK",
    "BJBR.JK":"BANK",

    "ANTM.JK":"MINING",
    "ADRO.JK":"MINING",
    "PTBA.JK":"MINING",
    "TINS.JK":"MINING",
    "MDKA.JK":"MINING",
    "ITMG.JK":"MINING",
    "MEDC.JK":"MINING",
    "ADMR.JK":"MINING",

    "TLKM.JK":"TELECOM",
    "ISAT.JK":"TELECOM",
    "EXCL.JK":"TELECOM",

    "ASII.JK":"AUTOMOTIVE",
    "AUTO.JK":"AUTOMOTIVE",

    "UNVR.JK":"CONSUMER",
    "ICBP.JK":"CONSUMER",
    "INDF.JK":"CONSUMER",
    "MYOR.JK":"CONSUMER",
    "ULTJ.JK":"CONSUMER",
    "SIDO.JK":"CONSUMER",

    "CPIN.JK":"POULTRY",
    "JPFA.JK":"POULTRY",
    "MAIN.JK":"POULTRY",

    "PWON.JK":"PROPERTY",
    "BSDE.JK":"PROPERTY",
    "CTRA.JK":"PROPERTY",

    "JSMR.JK":"INFRA",
    "PGAS.JK":"INFRA",

    "HEAL.JK":"HEALTHCARE",
    "KLBF.JK":"HEALTHCARE",

    "ERAA.JK":"TECHNOLOGY",
    "DNET.JK":"TECHNOLOGY",
    "GOTO.JK":"TECHNOLOGY",
    "BUKA.JK":"TECHNOLOGY",

    "SMGR.JK":"CEMENT",
    "INTP.JK":"CEMENT",

    "UNTR.JK":"HEAVY_EQUIPMENT",

    "ADHI.JK":"CONSTRUCTION",
    "PTPP.JK":"CONSTRUCTION",
    "WIKA.JK":"CONSTRUCTION",

    "BIRD.JK":"TRANSPORT",
    "SMDR.JK":"TRANSPORT",

    "ACES.JK":"RETAIL",
    "AMRT.JK":"RETAIL",
    "MAPI.JK":"RETAIL",

    "ELSA.JK":"ENERGY",

    "HMSP.JK":"TOBACCO",

    "BUMI.JK":"MINING"

}

# =====================================================
# DOWNLOAD DATA
# =====================================================

with st.spinner("Scanning institutional activity..."):

    data = yf.download(
        tickers=STOCKS,
        period="6mo",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        threads=True,
        progress=False
    )

# =====================================================
# ANALYSIS
# =====================================================

results = []

for stock in STOCKS:

    try:

        df = data[stock].dropna()

        if len(df) < 40:
            continue

        # =================================================
        # BASIC DATA
        # =================================================

        close_today = df["Close"].iloc[-1]
        close_yesterday = df["Close"].iloc[-2]

        volume_today = df["Volume"].iloc[-1]
        avg_volume_20 = df["Volume"].tail(20).mean()

        price_change = (
            (close_today - close_yesterday)
            / close_yesterday
        ) * 100

        volume_ratio = (
            volume_today / avg_volume_20
        )

        # =================================================
        # TRANSACTION VALUE
        # =================================================

        value_today = close_today * volume_today

        avg_value_20 = (
            (df["Close"] * df["Volume"])
            .tail(20)
            .mean()
        )

        transaction_ratio = (
            value_today / avg_value_20
        )

        # =================================================
        # RELATIVE STRENGTH
        # =================================================

        rs = (
            (
                close_today /
                df["Close"].iloc[-20]
            ) - 1
        ) * 100

        # =================================================
        # BREAKOUT
        # =================================================

        breakout = (
            close_today >=
            df["High"].tail(20).max()
        )

        # =================================================
        # EARLY ACCUMULATION
        # =================================================

        accumulation = (

            volume_ratio > 1.5
            and
            abs(price_change) < 3
            and
            rs > 0

        )

        # =================================================
        # SMART MONEY SCORE
        # =================================================

        score = 0

        # volume score
        if volume_ratio > 3:
            score += 30
        elif volume_ratio > 2:
            score += 20
        elif volume_ratio > 1.5:
            score += 10

        # transaction score
        if transaction_ratio > 3:
            score += 30
        elif transaction_ratio > 2:
            score += 20
        elif transaction_ratio > 1.5:
            score += 10

        # RS score
        if rs > 20:
            score += 20
        elif rs > 10:
            score += 15
        elif rs > 5:
            score += 10

        # breakout score
        if breakout:
            score += 10

        # accumulation score
        if accumulation:
            score += 10

        # =================================================
        # AI SIGNAL
        # =================================================

        signal = "NEUTRAL"

        if score >= 80:
            signal = "🔥 STRONG BUY"

        elif score >= 60:
            signal = "✅ BUY"

        elif score >= 40:
            signal = "🟡 SPEC BUY"

        elif score >= 20:
            signal = "👀 WATCHLIST"

        else:
            signal = "❌ AVOID"

        # =================================================
        # SAVE RESULT
        # =================================================

        results.append({

            "Ticker": stock,

            "Sector":
                sector_map.get(stock, "OTHER"),

            "Price":
                f"{close_today:,.0f}".replace(",", "."),

            "% Change":
                f"{price_change:+.2f}%",

            "Avg Volume 20D":
                f"{int(avg_volume_20):,}".replace(",", "."),

            "Volume Today":
                f"{int(volume_today):,}".replace(",", "."),

            "Volume Ratio":
                round(volume_ratio, 2),

            "Transaction Ratio":
                round(transaction_ratio, 2),

            "Relative Strength":
                round(rs, 2),

            "Breakout":
                "YES" if breakout else "NO",

            "Accumulation":
                "YES" if accumulation else "NO",

            "AI Score":
                score,

            "AI Signal":
                signal

        })

    except:
        continue

# =====================================================
# DATAFRAME
# =====================================================

df_result = pd.DataFrame(results)

# =====================================================
# FILTERS
# =====================================================

st.sidebar.title("FILTER")

search = st.sidebar.text_input(
    "Search Ticker"
)

sector_filter = st.sidebar.selectbox(
    "Sector",
    ["ALL"] + sorted(df_result["Sector"].unique())
)

signal_filter = st.sidebar.selectbox(
    "AI Signal",
    ["ALL"] + sorted(df_result["AI Signal"].unique())
)

acc_filter = st.sidebar.selectbox(
    "Accumulation",
    ["ALL", "YES", "NO"]
)

filtered_df = df_result.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Ticker"]
        .str.contains(search.upper())
    ]

if sector_filter != "ALL":
    filtered_df = filtered_df[
        filtered_df["Sector"] == sector_filter
    ]

if signal_filter != "ALL":
    filtered_df = filtered_df[
        filtered_df["AI Signal"] == signal_filter
    ]

if acc_filter != "ALL":
    filtered_df = filtered_df[
        filtered_df["Accumulation"] == acc_filter
    ]

# =====================================================
# SECTOR ROTATION
# =====================================================

st.subheader("🔥 STRONGEST SECTOR")

sector_strength = (

    filtered_df
    .groupby("Sector")["AI Score"]
    .mean()
    .sort_values(ascending=False)

)

cols = st.columns(4)

for i, (sector, value) in enumerate(
    sector_strength.items()
):

    cols[i % 4].metric(
        sector,
        f"{round(value,1)}"
    )

# =====================================================
# EARLY ACCUMULATION TABLE
# =====================================================

st.subheader("🏦 EARLY ACCUMULATION")

acc_df = filtered_df[
    filtered_df["Accumulation"] == "YES"
]

acc_df = acc_df.sort_values(
    by="AI Score",
    ascending=False
)

st.dataframe(
    acc_df.head(15),
    use_container_width=True
)

# =====================================================
# MAIN TABLE
# =====================================================

st.subheader("🚀 MAIN SCANNER")

filtered_df = filtered_df.sort_values(
    by="AI Score",
    ascending=False
)

st.dataframe(
    filtered_df,
    use_container_width=True
)

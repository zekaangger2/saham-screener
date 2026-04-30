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

st.title("🚀 IDX SMART MONEY SCANNER")
st.caption(
    "Volume Scanner • Relative Strength • AI Signal"
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

with st.spinner("Scanning market..."):

    data = yf.download(
        tickers=STOCKS,
        period="3mo",
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

        if len(df) < 30:
            continue

        volume_today = df["Volume"].iloc[-1]
        avg_volume_20 = df["Volume"].tail(20).mean()

        close_today = df["Close"].iloc[-1]
        close_yesterday = df["Close"].iloc[-2]

        price_change = (
            (close_today - close_yesterday)
            / close_yesterday
        ) * 100

        volume_ratio = (
            volume_today / avg_volume_20
        )

        value_today = close_today * volume_today

        avg_value_20 = (
            (df["Close"] * df["Volume"])
            .tail(20)
            .mean()
        )

        transaction_ratio = (
            value_today / avg_value_20
        )

        rs = (
            (close_today / df["Close"].iloc[-20]) - 1
        ) * 100

        breakout = (
            close_today >= df["High"].tail(20).max()
        )

        accumulation = (
            volume_ratio > 1.5
            and abs(price_change) < 3
        )

        ai_signal = "NEUTRAL"

        if (
            volume_ratio > 2
            and transaction_ratio > 2
            and rs > 10
        ):
            ai_signal = "BUY"

        elif (
            volume_ratio > 1.5
            and rs > 5
        ):
            ai_signal = "SPEC BUY"

        elif (
            price_change < -3
        ):
            ai_signal = "AVOID"

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

            "AI Signal":
                ai_signal

        })

    except:
        continue

# =====================================================
# DATAFRAME
# =====================================================

df_result = pd.DataFrame(results)

# =====================================================
# FILTER
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

# =====================================================
# HEATMAP
# =====================================================

st.subheader("🔥 SECTOR HEATMAP")

heatmap = (
    filtered_df
    .groupby("Sector")["Volume Ratio"]
    .mean()
    .sort_values(ascending=False)
)

cols = st.columns(4)

for i, (sector, value) in enumerate(heatmap.items()):

    cols[i % 4].metric(
        sector,
        f"{round(value,2)}x"
    )

# =====================================================
# MARKET SUMMARY
# =====================================================

st.subheader("📊 MARKET SUMMARY")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Signal",
    len(filtered_df)
)

c2.metric(
    "Breakout",
    len(
        filtered_df[
            filtered_df["Breakout"] == "YES"
        ]
    )
)

c3.metric(
    "Accumulation",
    len(
        filtered_df[
            filtered_df["Accumulation"] == "YES"
        ]
    )
)

c4.metric(
    "BUY Signal",
    len(
        filtered_df[
            filtered_df["AI Signal"] == "BUY"
        ]
    )
)

# =====================================================
# TABLE
# =====================================================

st.subheader("🚀 MAIN SCANNER")

filtered_df = filtered_df.sort_values(
    by="Volume Ratio",
    ascending=False
)

st.dataframe(
    filtered_df,
    use_container_width=True
)

import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from streamlit_autorefresh import st_autorefresh

# =========================================================
# AUTO REFRESH
# =========================================================

st_autorefresh(interval=60000, key="refresh")

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="IDX Smart Money Scanner",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🚀 IDX SMART MONEY SCANNER")
st.caption("Volume Scanner • Relative Strength • AI Signal • Heatmap Sector")

# =========================================================
# STOCK LIST
# =========================================================

stocks = {

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

    "BUMI.JK":"MINING",
    "ELSA.JK":"ENERGY",
    "HMSP.JK":"TOBACCO"

}

# =========================================================
# DOWNLOAD DATA
# =========================================================

ticker_list = list(stocks.keys())

with st.spinner("Scanning market..."):

    data = yf.download(
        ticker_list,
        period="3mo",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        progress=False
    )

# =========================================================
# ANALYSIS
# =========================================================

hasil = []

for ticker in ticker_list:

    try:

        df = data[ticker].dropna()

        if len(df) < 30:
            continue

        close_today = float(df["Close"].iloc[-1])
        close_20 = float(df["Close"].iloc[-20])

        volume_today = float(df["Volume"].iloc[-1])
        avg_volume = float(df["Volume"].tail(20).mean())

        value_today = close_today * volume_today
        avg_value = (df["Close"] * df["Volume"]).tail(20).mean()

        highest_20 = float(df["High"].tail(20).max())

        # =====================================================
        # RATIO
        # =====================================================

        volume_ratio = volume_today / avg_volume
        transaction_ratio = value_today / avg_value

        # =====================================================
        # RELATIVE STRENGTH
        # =====================================================

        rs = ((close_today - close_20) / close_20) * 100

        # =====================================================
        # BREAKOUT
        # =====================================================

        breakout = (
            close_today >= highest_20 * 0.99
            and volume_ratio >= 2
        )

        # =====================================================
        # BANDAR ACCUMULATION
        # =====================================================

        accumulation = (
            volume_ratio >= 1.5
            and transaction_ratio >= 1.5
            and close_today > close_20
        )

        # =====================================================
        # AI SIGNAL
        # =====================================================

        signal = "NEUTRAL"

        if breakout and accumulation:
            signal = "🔥 STRONG BREAKOUT"

        elif accumulation:
            signal = "🟢 ACCUMULATION"

        elif rs > 15:
            signal = "🚀 RELATIVE STRENGTH"

        elif volume_ratio > 2:
            signal = "📈 UNUSUAL VOLUME"

        # =====================================================
        # FILTER
        # =====================================================

        if volume_ratio >= 1.5:

            hasil.append({

                "Ticker": ticker,
                "Sector": stocks[ticker],

                "Avg Volume 20D":
                    f"{int(avg_volume):,}".replace(",", "."),

                "Volume Today":
                    f"{int(volume_today):,}".replace(",", "."),

                "Volume Ratio":
                    round(volume_ratio, 2),

                "Transaction Ratio":
                    round(transaction_ratio, 2),

                "RS %":
                    round(rs, 2),

                "Breakout":
                    "YES" if breakout else "-",

                "Accumulation":
                    "YES" if accumulation else "-",

                "AI Signal":
                    signal

            })

    except:
        pass

# =========================================================
# DATAFRAME
# =========================================================

hasil_df = pd.DataFrame(hasil)

# =========================================================
# SIDEBAR FILTER
# =========================================================

st.sidebar.title("FILTER")

search = st.sidebar.text_input("Search Ticker")

sector_filter = st.sidebar.selectbox(
    "Sector",
    ["ALL"] + sorted(hasil_df["Sector"].unique())
)

signal_filter = st.sidebar.selectbox(
    "AI Signal",
    ["ALL"] + sorted(hasil_df["AI Signal"].unique())
)

# =========================================================
# APPLY FILTER
# =========================================================

filtered_df = hasil_df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Ticker"].str.contains(search.upper())
    ]

if sector_filter != "ALL":
    filtered_df = filtered_df[
        filtered_df["Sector"] == sector_filter
    ]

if signal_filter != "ALL":
    filtered_df = filtered_df[
        filtered_df["AI Signal"] == signal_filter
    ]

# =========================================================
# HEATMAP SECTOR
# =========================================================

st.subheader("🔥 SECTOR HEATMAP")

sector_heatmap = (
    filtered_df
    .groupby("Sector")["Volume Ratio"]
    .mean()
    .sort_values(ascending=False)
)

col1, col2, col3, col4 = st.columns(4)

for i, (sector, value) in enumerate(sector_heatmap.items()):

    emoji = "🟢"

    if value >= 3:
        emoji = "🔥"

    elif value >= 2:
        emoji = "🚀"

    text = f"{emoji} {sector}\n\n{round(value,2)}x"

    if i % 4 == 0:
        col1.metric(sector, f"{round(value,2)}x")

    elif i % 4 == 1:
        col2.metric(sector, f"{round(value,2)}x")

    elif i % 4 == 2:
        col3.metric(sector, f"{round(value,2)}x")

    else:
        col4.metric(sector, f"{round(value,2)}x")

# =========================================================
# MARKET SUMMARY
# =========================================================

st.subheader("📊 MARKET SUMMARY")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Signal", len(filtered_df))

c2.metric(
    "Breakout",
    len(filtered_df[filtered_df["Breakout"] == "YES"])
)

c3.metric(
    "Accumulation",
    len(filtered_df[filtered_df["Accumulation"] == "YES"])
)

c4.metric(
    "Strong RS",
    len(filtered_df[filtered_df["RS %"] > 15])
)

# =========================================================
# MAIN TABLE
# =========================================================

st.subheader("🚀 MAIN SCANNER")

filtered_df = filtered_df.sort_values(
    by="Volume Ratio",
    ascending=False
)

st.dataframe(
    filtered_df,
    use_container_width=True
)

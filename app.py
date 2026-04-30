import streamlit as st
from streamlit_autorefresh import st_autorefresh
import yfinance as yf
import pandas as pd
import numpy as np

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

st.title("🚀 IDX SMART MONEY SCANNER")
st.caption("Volume Scanner • Breakout Detector • Bandar Accumulation")

# =====================================================
# STOCK LIST
# =====================================================

stock_data = {

    # BANK
    "BBCA.JK": "BANK",
    "BBRI.JK": "BANK",
    "BMRI.JK": "BANK",
    "BBNI.JK": "BANK",
    "BRIS.JK": "BANK",
    "ARTO.JK": "BANK",
    "BBTN.JK": "BANK",
    "BJBR.JK": "BANK",
    "BJTM.JK": "BANK",

    # MINING
    "ADRO.JK": "MINING",
    "ADMR.JK": "MINING",
    "ANTM.JK": "MINING",
    "PTBA.JK": "MINING",
    "ITMG.JK": "MINING",
    "MEDC.JK": "MINING",
    "TINS.JK": "MINING",
    "ELSA.JK": "MINING",
    "BUMI.JK": "MINING",

    # TECHNOLOGY
    "GOTO.JK": "TECHNOLOGY",
    "BUKA.JK": "TECHNOLOGY",
    "DCII.JK": "TECHNOLOGY",
    "DNET.JK": "TECHNOLOGY",
    "EMTK.JK": "TECHNOLOGY",

    # CONSUMER
    "ICBP.JK": "CONSUMER",
    "INDF.JK": "CONSUMER",
    "MYOR.JK": "CONSUMER",
    "SIDO.JK": "CONSUMER",
    "ULTJ.JK": "CONSUMER",
    "UNVR.JK": "CONSUMER",
    "KLBF.JK": "CONSUMER",

    # PROPERTY
    "BSDE.JK": "PROPERTY",
    "CTRA.JK": "PROPERTY",
    "PWON.JK": "PROPERTY",
    "SMRA.JK": "PROPERTY",
    "ASRI.JK": "PROPERTY",

    # TELECOM
    "TLKM.JK": "TELECOM",
    "EXCL.JK": "TELECOM",
    "ISAT.JK": "TELECOM",

    # HEALTHCARE
    "HEAL.JK": "HEALTHCARE",
    "MIKA.JK": "HEALTHCARE",
    "SILO.JK": "HEALTHCARE",
    "CARE.JK": "HEALTHCARE",

    # INDUSTRIAL
    "ASII.JK": "INDUSTRIAL",
    "AUTO.JK": "INDUSTRIAL",
    "SMSM.JK": "INDUSTRIAL",
    "UNTR.JK": "INDUSTRIAL",

    # INFRA
    "JSMR.JK": "INFRA",
    "PGAS.JK": "INFRA",
    "TBIG.JK": "INFRA",
    "TOWR.JK": "INFRA",

    # POULTRY
    "CPIN.JK": "POULTRY",
    "JPFA.JK": "POULTRY",
    "MAIN.JK": "POULTRY",

    # RETAIL
    "ACES.JK": "RETAIL",
    "AMRT.JK": "RETAIL",
    "MAPI.JK": "RETAIL",
    "ERAA.JK": "RETAIL",
    "LPPF.JK": "RETAIL",

    # TRANSPORT
    "BIRD.JK": "TRANSPORT",
    "SMDR.JK": "TRANSPORT",
    "TMAS.JK": "TRANSPORT",
    "ASSA.JK": "TRANSPORT"

}

stocks = list(stock_data.keys())

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("FILTER")

search = st.sidebar.text_input("Search Ticker")

all_sector = sorted(list(set(stock_data.values())))

selected_sector = st.sidebar.selectbox(
    "Sector",
    ["ALL"] + all_sector
)

selected_volume_signal = st.sidebar.selectbox(
    "Volume Signal",
    [
        "ALL",
        "🔥 SUPER",
        "🚀 HIGH",
        "⚡ ACTIVE",
        "NORMAL"
    ]
)

selected_bandar = st.sidebar.selectbox(
    "Bandar Signal",
    [
        "ALL",
        "🔥 ACCUMULATION",
        "⚠️ DISTRIBUTION",
        "NORMAL"
    ]
)

selected_breakout = st.sidebar.selectbox(
    "Breakout",
    [
        "ALL",
        "🔥 BREAKOUT",
        "NO"
    ]
)

# =====================================================
# SCANNER
# =====================================================

hasil = []

BATCH_SIZE = 25

batches = [
    stocks[i:i+BATCH_SIZE]
    for i in range(0, len(stocks), BATCH_SIZE)
]

progress = st.progress(0)

status = st.empty()

TOTAL_BATCH = len(batches)

for idx, batch in enumerate(batches):

    try:

        status.text(
            f"Scanning {idx+1}/{TOTAL_BATCH}"
        )

        data = yf.download(
            tickers=batch,
            period="6mo",
            interval="1d",
            auto_adjust=True,
            group_by="ticker",
            threads=True,
            progress=False
        )

        for stock in batch:

            try:

                if stock not in data:
                    continue

                df = data[stock].copy()

                if df.empty:
                    continue

                if len(df) < 30:
                    continue

                # =====================
                # CLEAN DATA
                # =====================

                df["Close"] = (
                    pd.to_numeric(
                        df["Close"],
                        errors="coerce"
                    )
                    .ffill()
                )

                df["Open"] = (
                    pd.to_numeric(
                        df["Open"],
                        errors="coerce"
                    )
                    .ffill()
                )

                df["High"] = (
                    pd.to_numeric(
                        df["High"],
                        errors="coerce"
                    )
                    .ffill()
                )

                df["Low"] = (
                    pd.to_numeric(
                        df["Low"],
                        errors="coerce"
                    )
                    .ffill()
                )

                df["Volume"] = (
                    pd.to_numeric(
                        df["Volume"],
                        errors="coerce"
                    )
                    .fillna(0)
                )

                # =====================
                # CURRENT DATA
                # =====================

                close_today = float(df["Close"].iloc[-1])
                close_yesterday = float(df["Close"].iloc[-2])

                high_today = float(df["High"].iloc[-1])
                low_today = float(df["Low"].iloc[-1])
                open_today = float(df["Open"].iloc[-1])

                volume_today = float(df["Volume"].iloc[-1])

                # =====================
                # CHANGE %
                # =====================

                change_pct = (
                    (
                        close_today -
                        close_yesterday
                    )
                    /
                    close_yesterday
                ) * 100

                # =====================
                # AVG VOLUME
                # =====================

                avg_volume_20 = (
                    df["Volume"]
                    .rolling(20)
                    .mean()
                    .iloc[-1]
                )

                if pd.isna(avg_volume_20):
                    continue

                if avg_volume_20 <= 0:
                    continue

                volume_ratio = (
                    volume_today /
                    avg_volume_20
                )

                # =====================
                # VALUE
                # =====================

                df["value"] = (
                    df["Close"] *
                    df["Volume"]
                )

                value_today = (
                    close_today *
                    volume_today
                )

                avg_value_20 = (
                    df["value"]
                    .rolling(20)
                    .mean()
                    .iloc[-1]
                )

                if pd.isna(avg_value_20):
                    continue

                if avg_value_20 <= 0:
                    continue

                value_ratio = (
                    value_today /
                    avg_value_20
                )

                # =====================
                # VOLUME SIGNAL
                # =====================

                if volume_ratio >= 5:
                    volume_signal = "🔥 SUPER"

                elif volume_ratio >= 3:
                    volume_signal = "🚀 HIGH"

                elif volume_ratio >= 2:
                    volume_signal = "⚡ ACTIVE"

                else:
                    volume_signal = "NORMAL"

                # =====================
                # BREAKOUT DETECTOR
                # =====================

                resistance_20 = (
                    df["High"]
                    .rolling(20)
                    .max()
                    .iloc[-2]
                )

                if (
                    close_today > resistance_20
                    and volume_ratio >= 2
                ):

                    breakout_signal = "🔥 BREAKOUT"

                else:

                    breakout_signal = "NO"

                # =====================
                # BANDAR DETECTOR
                # =====================

                candle_range = (
                    high_today -
                    low_today
                )

                if candle_range == 0:
                    candle_range = 1

                candle_body = abs(
                    close_today -
                    open_today
                )

                body_ratio = (
                    candle_body /
                    candle_range
                )

                # SMART MONEY
                if (
                    volume_ratio >= 2
                    and value_ratio >= 2
                    and abs(change_pct) <= 2
                    and body_ratio <= 0.5
                ):

                    bandar_signal = "🔥 ACCUMULATION"

                # DISTRIBUTION
                elif (
                    volume_ratio >= 2
                    and change_pct <= -3
                ):

                    bandar_signal = "⚠️ DISTRIBUTION"

                else:

                    bandar_signal = "NORMAL"

                # =====================
                # APPEND
                # =====================

                hasil.append({

                    "Ticker":
                        stock,

                    "Sector":
                        stock_data.get(
                            stock,
                            "OTHER"
                        ),

                    "Price":
                        round(close_today, 2),

                    "Change %":
                        f"{change_pct:+.2f}%",

                    "Avg Volume 20":
                        f"{avg_volume_20:,.0f}".replace(",", "."),

                    "Volume Today":
                        f"{volume_today:,.0f}".replace(",", "."),

                    "Volume Ratio":
                        round(volume_ratio, 2),

                    "Avg Transaction":
                        "Rp " +
                        f"{avg_value_20:,.0f}".replace(",", "."),

                    "Transaction Today":
                        "Rp " +
                        f"{value_today:,.0f}".replace(",", "."),

                    "Transaction Ratio":
                        round(value_ratio, 2),

                    "Volume Signal":
                        volume_signal,

                    "Breakout":
                        breakout_signal,

                    "Bandar":
                        bandar_signal

                })

            except:
                continue

        progress.progress(
            (idx + 1) / TOTAL_BATCH
        )

    except:
        continue

status.text("✅ Scan Complete")

# =====================================================
# DATAFRAME
# =====================================================

hasil_df = pd.DataFrame(hasil)

# =====================================================
# FILTER
# =====================================================

if not hasil_df.empty:

    # SEARCH
    if search:

        hasil_df = hasil_df[
            hasil_df["Ticker"]
            .str.contains(
                search.upper()
            )
        ]

    # SECTOR
    if selected_sector != "ALL":

        hasil_df = hasil_df[
            hasil_df["Sector"] ==
            selected_sector
        ]

    # VOLUME SIGNAL
    if selected_volume_signal != "ALL":

        hasil_df = hasil_df[
            hasil_df["Volume Signal"] ==
            selected_volume_signal
        ]

    # BANDAR
    if selected_bandar != "ALL":

        hasil_df = hasil_df[
            hasil_df["Bandar"] ==
            selected_bandar
        ]

    # BREAKOUT
    if selected_breakout != "ALL":

        hasil_df = hasil_df[
            hasil_df["Breakout"] ==
            selected_breakout
        ]

    # SORT
    hasil_df = hasil_df.sort_values(
        by="Transaction Ratio",
        ascending=False
    )

# =====================================================
# TOP RANKING
# =====================================================

st.subheader("🏆 TOP RANKING")

col1, col2, col3 = st.columns(3)

with col1:

    top_volume = hasil_df.nlargest(
        5,
        "Volume Ratio"
    )[
        [
            "Ticker",
            "Volume Ratio"
        ]
    ]

    st.write("🔥 TOP VOLUME")
    st.dataframe(
        top_volume,
        use_container_width=True
    )

with col2:

    top_transaction = hasil_df.nlargest(
        5,
        "Transaction Ratio"
    )[
        [
            "Ticker",
            "Transaction Ratio"
        ]
    ]

    st.write("💰 TOP TRANSACTION")
    st.dataframe(
        top_transaction,
        use_container_width=True
    )

with col3:

    top_breakout = hasil_df[
        hasil_df["Breakout"]
        ==
        "🔥 BREAKOUT"
    ][
        [
            "Ticker",
            "Breakout"
        ]
    ]

    st.write("🚀 BREAKOUT")
    st.dataframe(
        top_breakout,
        use_container_width=True
    )

# =====================================================
# METRICS
# =====================================================

st.subheader("📊 MARKET SUMMARY")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Total Stocks",
        len(stocks)
    )

with m2:

    st.metric(
        "Signals Found",
        len(hasil_df)
    )

with m3:

    accumulation_total = len(
        hasil_df[
            hasil_df["Bandar"]
            ==
            "🔥 ACCUMULATION"
        ]
    )

    st.metric(
        "Accumulation",
        accumulation_total
    )

with m4:

    breakout_total = len(
        hasil_df[
            hasil_df["Breakout"]
            ==
            "🔥 BREAKOUT"
        ]
    )

    st.metric(
        "Breakout",
        breakout_total
    )

# =====================================================
# MAIN TABLE
# =====================================================

st.subheader("📈 MAIN SCANNER")

st.dataframe(
    hasil_df,
    use_container_width=True,
    height=800
)

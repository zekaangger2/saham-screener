import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="IDX Bandar Scanner",
    layout="wide"
)

st.title("🚀 IDX Bandar Activity Scanner")
st.caption("Volume Scanner + Bandar Accumulation Detector")

# =====================================================
# STOCKS + CATEGORY
# =====================================================

stock_data = {

    # =========================
    # BANK
    # =========================

    "BBCA.JK": "BANK",
    "BBRI.JK": "BANK",
    "BMRI.JK": "BANK",
    "BBNI.JK": "BANK",
    "BRIS.JK": "BANK",
    "ARTO.JK": "BANK",
    "BBTN.JK": "BANK",
    "BJBR.JK": "BANK",
    "BJTM.JK": "BANK",

    # =========================
    # MINING
    # =========================

    "ADRO.JK": "MINING",
    "ADMR.JK": "MINING",
    "ANTM.JK": "MINING",
    "PTBA.JK": "MINING",
    "ITMG.JK": "MINING",
    "MEDC.JK": "MINING",
    "TINS.JK": "MINING",
    "ELSA.JK": "MINING",
    "BUMI.JK": "MINING",

    # =========================
    # TECHNOLOGY
    # =========================

    "GOTO.JK": "TECHNOLOGY",
    "BUKA.JK": "TECHNOLOGY",
    "DCII.JK": "TECHNOLOGY",
    "DNET.JK": "TECHNOLOGY",
    "EMTK.JK": "TECHNOLOGY",

    # =========================
    # CONSUMER
    # =========================

    "ICBP.JK": "CONSUMER",
    "INDF.JK": "CONSUMER",
    "MYOR.JK": "CONSUMER",
    "SIDO.JK": "CONSUMER",
    "ULTJ.JK": "CONSUMER",
    "UNVR.JK": "CONSUMER",
    "KLBF.JK": "CONSUMER",

    # =========================
    # PROPERTY
    # =========================

    "BSDE.JK": "PROPERTY",
    "CTRA.JK": "PROPERTY",
    "PWON.JK": "PROPERTY",
    "SMRA.JK": "PROPERTY",
    "ASRI.JK": "PROPERTY",

    # =========================
    # TELECOM
    # =========================

    "TLKM.JK": "TELECOM",
    "EXCL.JK": "TELECOM",
    "ISAT.JK": "TELECOM",

    # =========================
    # HEALTHCARE
    # =========================

    "HEAL.JK": "HEALTHCARE",
    "MIKA.JK": "HEALTHCARE",
    "SILO.JK": "HEALTHCARE",
    "CARE.JK": "HEALTHCARE",

    # =========================
    # INDUSTRIAL
    # =========================

    "ASII.JK": "INDUSTRIAL",
    "AUTO.JK": "INDUSTRIAL",
    "SMSM.JK": "INDUSTRIAL",
    "UNTR.JK": "INDUSTRIAL",

    # =========================
    # INFRA
    # =========================

    "JSMR.JK": "INFRA",
    "PGAS.JK": "INFRA",
    "TBIG.JK": "INFRA",
    "TOWR.JK": "INFRA",

    # =========================
    # POULTRY
    # =========================

    "CPIN.JK": "POULTRY",
    "JPFA.JK": "POULTRY",
    "MAIN.JK": "POULTRY",

    # =========================
    # RETAIL
    # =========================

    "ACES.JK": "RETAIL",
    "AMRT.JK": "RETAIL",
    "MAPI.JK": "RETAIL",
    "ERAA.JK": "RETAIL",
    "LPPF.JK": "RETAIL",

    # =========================
    # TRANSPORT
    # =========================

    "BIRD.JK": "TRANSPORT",
    "SMDR.JK": "TRANSPORT",
    "TMAS.JK": "TRANSPORT",
    "ASSA.JK": "TRANSPORT"

}

stocks = list(stock_data.keys())

# =====================================================
# SIDEBAR FILTER
# =====================================================

st.sidebar.title("FILTER")

# SEARCH
search = st.sidebar.text_input(
    "Search Ticker"
)

# SECTOR FILTER
all_sector = sorted(
    list(set(stock_data.values()))
)

selected_sector = st.sidebar.selectbox(
    "Sector",
    ["ALL"] + all_sector
)

# SIGNAL FILTER
selected_signal = st.sidebar.selectbox(
    "Volume Signal",
    ["ALL", "🔥 SUPER", "🚀 HIGH", "⚡ ACTIVE"]
)

# BANDAR FILTER
selected_bandar = st.sidebar.selectbox(
    "Bandar Detector",
    [
        "ALL",
        "🔥 ACCUMULATION",
        "⚠️ DISTRIBUTION",
        "NORMAL"
    ]
)

# =====================================================
# SCANNER
# =====================================================

hasil = []

BATCH_SIZE = 30

batches = [
    stocks[i:i+BATCH_SIZE]
    for i in range(0, len(stocks), BATCH_SIZE)
]

progress_bar = st.progress(0)

status_text = st.empty()

total_batch = len(batches)

for idx, batch in enumerate(batches):

    try:

        status_text.text(
            f"Scanning {idx+1}/{total_batch}"
        )

        data = yf.download(
            tickers=batch,
            period="3mo",
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

                if len(df) < 20:
                    continue

                # =====================
                # CLEANING
                # =====================

                df["Close"] = (
                    df["Close"]
                    .ffill()
                    .fillna(0)
                )

                df["Open"] = (
                    df["Open"]
                    .ffill()
                    .fillna(0)
                )

                df["High"] = (
                    df["High"]
                    .ffill()
                    .fillna(0)
                )

                df["Low"] = (
                    df["Low"]
                    .ffill()
                    .fillna(0)
                )

                df["Volume"] = (
                    df["Volume"]
                    .fillna(0)
                )

                # =====================
                # PRICE
                # =====================

                close_today = (
                    df["Close"]
                    .iloc[-1]
                )

                close_yesterday = (
                    df["Close"]
                    .iloc[-2]
                )

                change_pct = (
                    (
                        close_today -
                        close_yesterday
                    )
                    /
                    close_yesterday
                ) * 100

                # =====================
                # VOLUME
                # =====================

                avg_volume_20 = (
                    df["Volume"]
                    .rolling(20)
                    .mean()
                    .iloc[-1]
                )

                volume_today = (
                    df["Volume"]
                    .iloc[-1]
                )

                # =====================
                # VALUE
                # =====================

                df["value"] = (
                    df["Close"] *
                    df["Volume"]
                )

                avg_value_20 = (
                    df["value"]
                    .rolling(20)
                    .mean()
                    .iloc[-1]
                )

                value_today = (
                    df["value"]
                    .iloc[-1]
                )

                # =====================
                # VALIDATION
                # =====================

                if pd.isna(avg_volume_20):
                    continue

                if avg_volume_20 <= 0:
                    continue

                # =====================
                # RATIO
                # =====================

                ratio_volume = (
                    volume_today /
                    avg_volume_20
                )

                ratio_value = (
                    value_today /
                    avg_value_20
                )

                # =====================
                # VOLUME SIGNAL
                # =====================

                if ratio_volume >= 5:
                    volume_signal = "🔥 SUPER"

                elif ratio_volume >= 3:
                    volume_signal = "🚀 HIGH"

                elif ratio_volume >= 2:
                    volume_signal = "⚡ ACTIVE"

                else:
                    volume_signal = "NORMAL"

                # =====================
                # BANDAR DETECTOR
                # =====================

                body = abs(
                    close_today -
                    df["Open"].iloc[-1]
                )

                candle_range = (
                    df["High"].iloc[-1] -
                    df["Low"].iloc[-1]
                )

                if candle_range == 0:
                    candle_range = 1

                body_ratio = (
                    body /
                    candle_range
                )

                # ACCUMULATION
                if (
                    ratio_volume >= 2
                    and ratio_value >= 2
                    and abs(change_pct) <= 2
                    and body_ratio <= 0.5
                ):

                    bandar_signal = "🔥 ACCUMULATION"

                # DISTRIBUTION
                elif (
                    ratio_volume >= 2
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
                        round(ratio_volume, 2),

                    "Avg Transaction":
                        "Rp " +
                        f"{avg_value_20:,.0f}".replace(",", "."),

                    "Transaction Today":
                        "Rp " +
                        f"{value_today:,.0f}".replace(",", "."),

                    "Transaction Ratio":
                        round(ratio_value, 2),

                    "Volume Signal":
                        volume_signal,

                    "Bandar Detector":
                        bandar_signal

                })

            except:
                continue

        progress_bar.progress(
            (idx + 1) / total_batch
        )

    except:
        continue

status_text.text("✅ Scan Complete")

# =====================================================
# DATAFRAME
# =====================================================

hasil_df = pd.DataFrame(hasil)

# =====================================================
# FILTERS
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

    # SIGNAL
    if selected_signal != "ALL":

        hasil_df = hasil_df[
            hasil_df["Volume Signal"] ==
            selected_signal
        ]

    # BANDAR
    if selected_bandar != "ALL":

        hasil_df = hasil_df[
            hasil_df["Bandar Detector"] ==
            selected_bandar
        ]

    # SORTING
    hasil_df = hasil_df.sort_values(
        by="Transaction Ratio",
        ascending=False
    )

# =====================================================
# METRICS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Stocks",
        len(stocks)
    )

with col2:

    st.metric(
        "Signals Found",
        len(hasil_df)
    )

with col3:

    accumulation_count = len(
        hasil_df[
            hasil_df["Bandar Detector"]
            ==
            "🔥 ACCUMULATION"
        ]
    )

    st.metric(
        "Accumulation",
        accumulation_count
    )

with col4:

    st.metric(
        "Scanner Status",
        "ONLINE"
    )

# =====================================================
# OUTPUT
# =====================================================

st.dataframe(
    hasil_df,
    use_container_width=True,
    height=750
)

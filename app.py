import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Bandar Activity Scanner",
    layout="wide"
)

st.title("🚀 Bandar Activity Scanner")
st.caption("Scanner Volume & Value Activity Saham Indonesia")

# =====================================================
# LIST SAHAM
# =====================================================

stocks = [

    "BBCA.JK","BBRI.JK","BMRI.JK","BBNI.JK","BRIS.JK",
    "ADRO.JK","ADMR.JK","ANTM.JK","PTBA.JK","ITMG.JK",
    "BUMI.JK","MEDC.JK","PGAS.JK","ICBP.JK","INDF.JK",
    "MYOR.JK","SIDO.JK","ULTJ.JK","UNVR.JK","ACES.JK",
    "AMRT.JK","MAPI.JK","ERAA.JK","TLKM.JK","EXCL.JK",
    "ISAT.JK","GOTO.JK","BUKA.JK","BSDE.JK","CTRA.JK",
    "PWON.JK","PTPP.JK","ADHI.JK","WIKA.JK","ASII.JK",
    "AUTO.JK","SMGR.JK","INTP.JK","CPIN.JK","JPFA.JK",
    "KLBF.JK","HEAL.JK","BIRD.JK","SMDR.JK","JSMR.JK",
    "UNTR.JK","HMSP.JK"

]

# =====================================================
# DOWNLOAD DATA
# =====================================================

with st.spinner("Downloading market data..."):

    data = yf.download(
        stocks,
        period="3mo",
        interval="1d",
        auto_adjust=True,
        group_by="ticker",
        progress=False
    )

# =====================================================
# ANALISA
# =====================================================

hasil = []

for stock in stocks:

    try:

        df = data[stock].copy()

        if df.empty:
            continue

        if len(df) < 20:
            continue

        df["Close"] = df["Close"].fillna(0)
        df["Volume"] = df["Volume"].fillna(0)

        df["avg_volume_20"] = (
            df["Volume"]
            .rolling(20)
            .mean()
        )

        df["value"] = df["Close"] * df["Volume"]

        df["avg_value_20"] = (
            df["value"]
            .rolling(20)
            .mean()
        )

        volume_hari_ini = float(df["Volume"].iloc[-1])
        avg_volume_20 = float(df["avg_volume_20"].iloc[-1])

        value_hari_ini = float(df["value"].iloc[-1])
        avg_value_20 = float(df["avg_value_20"].iloc[-1])

        if np.isnan(avg_volume_20):
            continue

        if np.isnan(avg_value_20):
            continue

        if avg_volume_20 <= 0:
            continue

        if avg_value_20 <= 0:
            continue

        rasio_volume = volume_hari_ini / avg_volume_20
        rasio_value = value_hari_ini / avg_value_20

        # =========================================
        # SIGNAL
        # =========================================

        if rasio_volume >= 3:
            signal = "🔥 EXTREME"

        elif rasio_volume >= 2:
            signal = "🚀 HIGH"

        elif rasio_volume >= 1.5:
            signal = "⚡ ACTIVE"

        else:
            signal = "NORMAL"

        hasil.append({

            "Ticker":
                stock,

            "Signal":
                signal,

            "Avg Volume 20":
                f"{avg_volume_20:,.0f}".replace(",", "."),

            "Volume Today":
                f"{volume_hari_ini:,.0f}".replace(",", "."),

            "Volume Ratio":
                round(rasio_volume, 2),

            "Avg Value 20":
                "Rp " + f"{avg_value_20:,.0f}".replace(",", "."),

            "Value Today":
                "Rp " + f"{value_hari_ini:,.0f}".replace(",", "."),

            "Value Ratio":
                round(rasio_value, 2)

        })

    except:
        continue

# =====================================================
# DATAFRAME
# =====================================================

hasil_df = pd.DataFrame(hasil)

if not hasil_df.empty:

    hasil_df = hasil_df.sort_values(
        by="Value Ratio",
        ascending=False
    )

# =====================================================
# FILTER
# =====================================================

signal_filter = st.selectbox(
    "Filter Signal",
    ["ALL", "🔥 EXTREME", "🚀 HIGH", "⚡ ACTIVE", "NORMAL"]
)

if signal_filter != "ALL":

    hasil_df = hasil_df[
        hasil_df["Signal"] == signal_filter
    ]

# =====================================================
# OUTPUT
# =====================================================

st.dataframe(
    hasil_df,
    use_container_width=True
)

st.metric(
    "Total Saham Terdeteksi",
    len(hasil_df)
)

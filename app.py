import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from stocks import STOCKS

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="IDX Institutional Scanner",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🔥 IDX Institutional Scanner")

# =========================================================
# INFO HEADER
# =========================================================

total_scan = len(STOCKS)

now = datetime.now().strftime("%d %B %Y %H:%M")

st.markdown(
    f"""
    <div style='margin-top:-10px; margin-bottom:20px;'>

    <span style='font-size:13px; color:gray;'>
    Telah di scan dari <b>{total_scan}</b> saham IDX
    </span>

    <br>

    <span style='font-size:11px; color:gray;'>
    Last Market Detection : {now}
    </span>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# MARKET STATUS
# =========================================================

hour = datetime.now().hour

if 9 <= hour <= 16:
    market_status = "🟢 MARKET OPEN"
else:
    market_status = "🔴 MARKET CLOSED"

st.markdown(
    f"""
    <div style='padding:10px;
                border-radius:10px;
                background-color:#111111;
                margin-bottom:20px;
                font-size:15px;'>

    {market_status}

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CATEGORY MAP
# =========================================================

CATEGORY_MAP = {

    "BANK": [
        "BBCA.JK","BBRI.JK","BMRI.JK","BBNI.JK",
        "BRIS.JK","ARTO.JK","BTPS.JK","BJBR.JK"
    ],

    "MINING": [
        "ANTM.JK","ADRO.JK","PTBA.JK","ITMG.JK",
        "MDKA.JK","TINS.JK","ADMR.JK","BUMI.JK"
    ],

    "PROPERTY": [
        "BSDE.JK","PWON.JK","CTRA.JK","SMRA.JK"
    ],

    "TECHNOLOGY": [
        "GOTO.JK","BUKA.JK","DNET.JK","EMTK.JK"
    ],

    "CONSUMER": [
        "ICBP.JK","INDF.JK","UNVR.JK","MYOR.JK"
    ],

    "HEALTHCARE": [
        "KLBF.JK","HEAL.JK","MIKA.JK","SILO.JK"
    ],

    "TELECOM": [
        "TLKM.JK","ISAT.JK","EXCL.JK"
    ],

    "POULTRY": [
        "CPIN.JK","JPFA.JK","MAIN.JK"
    ],

    "INFRA": [
        "PGAS.JK","JSMR.JK","WIKA.JK","PTPP.JK"
    ]
}

# =========================================================
# CREATE CATEGORY
# =========================================================

def get_category(stock):

    for category, members in CATEGORY_MAP.items():

        if stock in members:
            return category

    return "OTHERS"

# =========================================================
# MAIN SCANNER
# =========================================================

hasil = []

st.info(f"Scanning {len(STOCKS)} saham IDX...")

data = yf.download(
    STOCKS,
    period="3mo",
    interval="1d",
    group_by="ticker",
    auto_adjust=True,
    threads=True
)

for stock in STOCKS:

    try:

        df = data[stock].copy()

        if len(df) < 25:
            continue

        # ====================================
        # VOLUME
        # ====================================

        volume_today = float(df["Volume"].iloc[-1])

        avg_volume = float(
            df["Volume"]
            .rolling(20)
            .mean()
            .iloc[-1]
        )

        ratio_volume = volume_today / avg_volume

        # ====================================
        # PRICE
        # ====================================

        close_today = float(df["Close"].iloc[-1])
        close_yesterday = float(df["Close"].iloc[-2])

        pct_change = (
            (close_today - close_yesterday)
            / close_yesterday
        ) * 100

        # ====================================
        # VALUE
        # ====================================

        value_today = volume_today * close_today

        avg_value = (
            (
                df["Volume"] * df["Close"]
            )
            .rolling(20)
            .mean()
            .iloc[-1]
        )

        ratio_value = value_today / avg_value

        # ====================================
        # AI SIGNAL
        # ====================================

        if ratio_volume >= 5 and pct_change > 3:
            ai_signal = "🔥 SUPER STRONG"

        elif ratio_volume >= 3 and pct_change > 0:
            ai_signal = "🚀 STRONG"

        elif ratio_volume >= 2:
            ai_signal = "👀 ACCUMULATION"

        else:
            ai_signal = "-"

        # ====================================
        # FILTER
        # ====================================

        if ratio_volume >= 2:

            hasil.append({

                "Ticker": stock,
                "Sector": get_category(stock),

                "Price": round(close_today, 2),

                "% Change": round(pct_change, 2),

                "Avg Vol 20D": int(avg_volume),

                "Today Vol": int(volume_today),

                "Volume Ratio": round(ratio_volume, 2),

                "Transaction Value": int(value_today),

                "AI Signal": ai_signal

            })

    except:
        continue

# =========================================================
# DATAFRAME
# =========================================================

df_hasil = pd.DataFrame(hasil)

# =========================================================
# EMPTY CHECK
# =========================================================

if df_hasil.empty:

    st.warning("Tidak ada saham memenuhi kriteria.")

else:

    # =====================================
    # SORT
    # =====================================

    df_hasil = df_hasil.sort_values(
        by="Volume Ratio",
        ascending=False
    )

    # =====================================
    # FILTER SECTOR
    # =====================================

    sectors = ["ALL"] + sorted(
        df_hasil["Sector"].unique().tolist()
    )

    selected_sector = st.selectbox(
        "Filter Sector",
        sectors
    )

    if selected_sector != "ALL":

        df_hasil = df_hasil[
            df_hasil["Sector"] == selected_sector
        ]

    # =====================================
    # TOP SECTOR TODAY
    # =====================================

    top_sector = (
        df_hasil.groupby("Sector")["Volume Ratio"]
        .mean()
        .sort_values(ascending=False)
        .head(1)
    )

    if len(top_sector) > 0:

        sector_name = top_sector.index[0]
        sector_value = round(top_sector.iloc[0], 2)

        st.success(
            f"🔥 Strongest Sector Today : {sector_name} ({sector_value}x)"
        )

    # =====================================
    # FORMAT
    # =====================================

    df_display = df_hasil.copy()

    df_display["Avg Vol 20D"] = df_display[
        "Avg Vol 20D"
    ].apply(lambda x: f"{x:,}")

    df_display["Today Vol"] = df_display[
        "Today Vol"
    ].apply(lambda x: f"{x:,}")

    df_display["Transaction Value"] = df_display[
        "Transaction Value"
    ].apply(lambda x: f"{x:,}")

    df_display["Price"] = df_display[
        "Price"
    ].apply(lambda x: f"{x:,.0f}")

    df_display["% Change"] = df_display[
        "% Change"
    ].apply(lambda x: f"{x:+.2f}%")

    # =====================================
    # SHOW TABLE
    # =====================================

    st.dataframe(
        df_display,
        use_container_width=True
    )

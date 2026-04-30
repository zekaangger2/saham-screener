import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from stocks import STOCKS

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="IDX Institutional Scanner",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("🔥 IDX Institutional Scanner")

# =====================================================
# HEADER INFO
# =====================================================

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

# =====================================================
# MARKET STATUS
# =====================================================

hour = datetime.now().hour

if 9 <= hour <= 16:
    market_status = "🟢 MARKET OPEN"
else:
    market_status = "🔴 MARKET CLOSED"

st.markdown(
    f"""
    <div style='padding:10px;
                border-radius:10px;
                background:#111111;
                margin-bottom:20px;'>

    {market_status}

    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# CATEGORY MAP
# =====================================================

CATEGORY_MAP = {

    "BANK": [
        "BBCA.JK","BBRI.JK","BMRI.JK","BBNI.JK",
        "BRIS.JK","ARTO.JK","BTPS.JK","BJBR.JK"
    ],

    "MINING": [
        "ANTM.JK","ADRO.JK","PTBA.JK","ITMG.JK",
        "MDKA.JK","TINS.JK","ADMR.JK"
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

# =====================================================
# GET CATEGORY
# =====================================================

def get_category(stock):

    for category, members in CATEGORY_MAP.items():

        if stock in members:
            return category

    return "OTHERS"

# =====================================================
# DOWNLOAD DATA
# =====================================================

data = yf.download(
    STOCKS,
    period="3mo",
    interval="1d",
    group_by="ticker",
    auto_adjust=True,
    threads=True
)

# =====================================================
# MAIN SCANNER
# =====================================================

hasil = []

for stock in STOCKS:

    try:

        df = data[stock].copy()

        if len(df) < 25:
            continue

        volume_today = float(df["Volume"].iloc[-1])

        avg_volume = float(
            df["Volume"]
            .rolling(20)
            .mean()
            .iloc[-1]
        )

        ratio_volume = volume_today / avg_volume

        close_today = float(df["Close"].iloc[-1])

        close_yesterday = float(df["Close"].iloc[-2])

        pct_change = (
            (close_today - close_yesterday)
            / close_yesterday
        ) * 100

        value_today = volume_today * close_today

        avg_value = (
            (df["Volume"] * df["Close"])
            .rolling(20)
            .mean()
            .iloc[-1]
        )

        ratio_value = value_today / avg_value

        # =================================================
        # RELATIVE STRENGTH
        # =================================================

        ma20 = df["Close"].rolling(20).mean().iloc[-1]

        if close_today > ma20:
            relative_strength = "STRONG"
        else:
            relative_strength = "WEAK"

        # =================================================
        # AI SIGNAL
        # =================================================

        if ratio_volume >= 5 and pct_change > 3:
            ai_signal = "🔥 SUPER STRONG"

        elif ratio_volume >= 3 and pct_change > 0:
            ai_signal = "🚀 STRONG"

        elif ratio_volume >= 2:
            ai_signal = "👀 ACCUMULATION"

        else:
            ai_signal = "-"

        # =================================================
        # FILTER MINIMUM
        # =================================================

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

                "Value Ratio": round(ratio_value, 2),

                "Relative Strength": relative_strength,

                "AI Signal": ai_signal

            })

    except:
        continue

# =====================================================
# DATAFRAME
# =====================================================

df_hasil = pd.DataFrame(hasil)

# =====================================================
# EMPTY CHECK
# =====================================================

if df_hasil.empty:

    st.warning("Tidak ada saham memenuhi kriteria.")

else:

    # =====================================================
    # SIDEBAR FILTER
    # =====================================================

    st.sidebar.title("⚙️ FILTER")

    # =========================================
    # SECTOR FILTER
    # =========================================

    sectors = ["ALL"] + sorted(
        df_hasil["Sector"].unique().tolist()
    )

    selected_sector = st.sidebar.selectbox(
        "📊 Sector",
        sectors
    )

    # =========================================
    # AI SIGNAL FILTER
    # =========================================

    signals = ["ALL"] + sorted(
        df_hasil["AI Signal"].unique().tolist()
    )

    selected_signal = st.sidebar.selectbox(
        "🤖 AI Signal",
        signals
    )

    # =========================================
    # BANDAR FILTER
    # =========================================

    accumulation_only = st.sidebar.checkbox(
        "🏦 Bandar Accumulation Only"
    )

    # =====================================================
    # APPLY FILTER
    # =====================================================

    if selected_sector != "ALL":

        df_hasil = df_hasil[
            df_hasil["Sector"] == selected_sector
        ]

    if selected_signal != "ALL":

        df_hasil = df_hasil[
            df_hasil["AI Signal"] == selected_signal
        ]

    if accumulation_only:

        df_hasil = df_hasil[
            (df_hasil["Value Ratio"] >= 2)
            &
            (df_hasil["% Change"] >= 0)
        ]

    # =====================================================
    # SORT
    # =====================================================

    df_hasil = df_hasil.sort_values(
        by="Volume Ratio",
        ascending=False
    )

    # =====================================================
    # HEATMAP
    # =====================================================

    st.subheader("🔥 Sector Heatmap")

    heatmap = (
        df_hasil.groupby("Sector")["Volume Ratio"]
        .mean()
        .sort_values(ascending=False)
    )

    st.dataframe(
        heatmap.rename("Average Volume Ratio"),
        use_container_width=True
    )

    # =====================================================
    # FORMAT
    # =====================================================

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

    # =====================================================
    # MAIN TABLE
    # =====================================================

    st.subheader("📈 Institutional Volume Scanner")

    st.dataframe(
        df_display,
        use_container_width=True
    )

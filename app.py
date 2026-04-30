import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="IDX Bandar Activity Scanner",
    layout="wide"
)

st.title("🚀 IDX Bandar Activity Scanner")
st.caption("Volume & Transaction Activity Scanner - Indonesia Stock Market")

# =====================================================
# FULL IDX STOCK LIST
# =====================================================

stocks = [

# BANK
"BBCA.JK","BBRI.JK","BMRI.JK","BBNI.JK","BRIS.JK",
"BNGA.JK","BNII.JK","MEGA.JK","NISP.JK","BTPN.JK",
"BJBR.JK","BJTM.JK","AGRO.JK","ARTO.JK","BBKP.JK",
"BBTN.JK","BDMN.JK","BEKS.JK","BINA.JK","DNAR.JK",

# MINING
"ADRO.JK","ADMR.JK","ANTM.JK","PTBA.JK","ITMG.JK",
"BUMI.JK","MEDC.JK","ELSA.JK","TINS.JK","INDY.JK",
"DEWA.JK","DOID.JK","BYAN.JK","HRUM.JK","MBAP.JK",
"KKGI.JK","TOBA.JK","UNTR.JK","GEMS.JK","ESSA.JK",

# CONSUMER
"ICBP.JK","INDF.JK","MYOR.JK","SIDO.JK","ULTJ.JK",
"UNVR.JK","HMSP.JK","GGRM.JK","KLBF.JK","CMRY.JK",
"GOOD.JK","ROTI.JK","STTP.JK","AISA.JK","CEKA.JK",

# RETAIL
"ACES.JK","AMRT.JK","MAPI.JK","ERAA.JK","LPPF.JK",
"RALS.JK","MIDI.JK","CSAP.JK","MPPA.JK","HERO.JK",

# TELECOM
"TLKM.JK","EXCL.JK","ISAT.JK","FREN.JK","MTEL.JK",

# TECHNOLOGY
"GOTO.JK","BUKA.JK","DCII.JK","DNET.JK","EDGE.JK",
"MCAS.JK","EMTK.JK","KIOS.JK","ZYRX.JK","TECH.JK",

# PROPERTY
"BSDE.JK","CTRA.JK","PWON.JK","SMRA.JK","ASRI.JK",
"DMAS.JK","KIJA.JK","JRPT.JK","LPKR.JK","MDLN.JK",

# CONSTRUCTION
"PTPP.JK","ADHI.JK","WIKA.JK","WEGE.JK","WSKT.JK",
"DGIK.JK","TOTL.JK","SSIA.JK","NRCA.JK",

# OTOMOTIF
"ASII.JK","AUTO.JK","IMAS.JK","SMSM.JK",

# INDUSTRY
"SMGR.JK","INTP.JK","ARNA.JK","MARK.JK",

# POULTRY
"CPIN.JK","JPFA.JK","MAIN.JK",

# HEALTHCARE
"HEAL.JK","MIKA.JK","SILO.JK","SRAJ.JK","CARE.JK",

# TRANSPORT
"BIRD.JK","SMDR.JK","WINS.JK","TMAS.JK","ASSA.JK",

# INFRA
"JSMR.JK","PGAS.JK","TBIG.JK","TOWR.JK",

# ENERGY
"AKRA.JK","PGEO.JK","RAJA.JK",

# ADDITIONAL
"AALI.JK","ABMM.JK","ACST.JK","ADES.JK","ADMF.JK",
"AGII.JK","AIMS.JK","AKPI.JK","ALDO.JK","ALKA.JK",
"AMAG.JK","AMFG.JK","AMIN.JK","APIC.JK","APLN.JK",
"ARGO.JK","ARII.JK","ARKA.JK","ARTA.JK","ARTI.JK",
"ASDM.JK","ASGR.JK","ASMI.JK","ASRM.JK","ATIC.JK",
"BAPA.JK","BATA.JK","BAYU.JK","BBHI.JK","BCAP.JK",
"BCIC.JK","BCIP.JK","BDKR.JK","BEST.JK","BFIN.JK",
"BGTG.JK","BIPI.JK","BISI.JK","BKDP.JK","BKSL.JK",
"BLTA.JK","BMAS.JK","BMHS.JK","BMTR.JK","BNBA.JK",
"BNBR.JK","BNLI.JK","BOGA.JK","BOLA.JK","BOSS.JK",
"BRAM.JK","BRMS.JK","BRNA.JK","BRPT.JK","BSIM.JK",
"BSSR.JK","BTPS.JK","BUKK.JK","BULL.JK","CAMP.JK",
"CARS.JK","CASA.JK","CINT.JK","CLEO.JK","CMNP.JK",
"CNKO.JK","CPRO.JK","CSIS.JK","CTBN.JK","CTTH.JK",
"DAYA.JK","DEFI.JK","DEPO.JK","DGNS.JK","DILD.JK",
"DMND.JK","DSFI.JK","DSNG.JK","DSSA.JK","DUTI.JK",
"DYAN.JK","ECII.JK","ELTY.JK","ENRG.JK","EPMT.JK",
"ESTA.JK","ESTI.JK","FAPA.JK","FAST.JK","FASW.JK",
"FILM.JK","FISH.JK","FORU.JK","GAMA.JK","GDST.JK",
"GIAA.JK","GJTL.JK","GLVA.JK","GMFI.JK","GOLD.JK",
"GPRA.JK","GSMF.JK","GWSA.JK","HAIS.JK","HATM.JK",
"HDFA.JK","HELI.JK","HITS.JK","HOTL.JK","HUMI.JK",
"IBFN.JK","IBST.JK","IMJS.JK","IMPC.JK","INAI.JK",
"INCO.JK","INDS.JK","INDX.JK","INKP.JK","INRU.JK",
"INTA.JK","IPCM.JK","ISSP.JK","JECC.JK","JGLE.JK",
"JSKY.JK","JSPT.JK","KAEF.JK","KARW.JK","KBLM.JK",
"KBLI.JK","KDSI.JK","KEEN.JK","KINO.JK","KKES.JK",
"KLAS.JK","KMTR.JK","KOBX.JK","KONI.JK","KPIG.JK",
"KRAS.JK","LABA.JK","LAPD.JK","LCGP.JK","LEAD.JK",
"LINK.JK","LMAS.JK","LMPI.JK","LPCK.JK","LPIN.JK",
"LRNA.JK","LSIP.JK","LTLS.JK","LUCK.JK","MAMI.JK",
"MASA.JK","MAYA.JK","MBSS.JK","MCOL.JK","MDKA.JK",
"MDRN.JK","MERK.JK","META.JK","MGNA.JK","MICE.JK",
"MINA.JK","MLIA.JK","MLPL.JK","MMLP.JK","MPMX.JK",
"MTDL.JK","MTFN.JK","MYRX.JK","NELY.JK","NICL.JK",
"NIKL.JK","OASA.JK","OCAP.JK","OKAS.JK","OMRE.JK",
"PADI.JK","PALM.JK","PANR.JK","PBRX.JK","PEHA.JK",
"PGLI.JK","PICO.JK","PKPK.JK","PLAN.JK","PMJS.JK",
"POLA.JK","POLI.JK","POOL.JK","PPGL.JK","PSAB.JK",
"PTIS.JK","PURE.JK","PYFA.JK","RAAM.JK","RBMS.JK",
"RDTX.JK","RELI.JK","RICY.JK","RMKE.JK","RMKO.JK",
"SAFE.JK","SAME.JK","SCMA.JK","SDMU.JK","SDPC.JK",
"SGRO.JK","SHIP.JK","SICO.JK","SIMP.JK","SMDM.JK",
"SMKL.JK","SMMT.JK","SOHO.JK","SPMA.JK","SPTO.JK",
"SQMI.JK","SRTG.JK","STAR.JK","SUGI.JK","SUPR.JK",
"TAPG.JK","TARA.JK","TAXI.JK","TCID.JK","TEBE.JK",
"TFAS.JK","TGKA.JK","TIFA.JK","TKIM.JK","TMPO.JK",
"TNCA.JK","TOOL.JK","TOYS.JK","TRAM.JK","TRGU.JK",
"TRIN.JK","TRJA.JK","TRUE.JK","TRUK.JK","TSPC.JK",
"TURI.JK","UCID.JK","UNSP.JK","VIVA.JK","WEHA.JK",
"WIFI.JK","WOOD.JK","YULE.JK","ZINC.JK"

]

# REMOVE DUPLICATE
stocks = list(set(stocks))
stocks.sort()

# =====================================================
# CATEGORY MAPPING
# =====================================================

category_map = {

    "BANK": [
        "BBCA.JK","BBRI.JK","BMRI.JK","BBNI.JK","BRIS.JK"
    ],

    "MINING": [
        "ADRO.JK","ADMR.JK","ANTM.JK","PTBA.JK","ITMG.JK"
    ],

    "TECHNOLOGY": [
        "GOTO.JK","BUKA.JK","DCII.JK"
    ],

    "PROPERTY": [
        "BSDE.JK","CTRA.JK","PWON.JK"
    ],

    "CONSUMER": [
        "ICBP.JK","INDF.JK","MYOR.JK","SIDO.JK"
    ]
}

# =====================================================
# SIDEBAR FILTER
# =====================================================

st.sidebar.title("FILTER")

search_ticker = st.sidebar.text_input(
    "Search Ticker"
)

signal_filter = st.sidebar.selectbox(
    "Signal",
    ["ALL", "🔥 SUPER", "🚀 HIGH", "⚡ ACTIVE"]
)

# =====================================================
# FAST BATCH SCANNER
# =====================================================

hasil = []

BATCH_SIZE = 50

batches = [
    stocks[i:i + BATCH_SIZE]
    for i in range(0, len(stocks), BATCH_SIZE)
]

progress_bar = st.progress(0)

status_text = st.empty()

total_batch = len(batches)

for idx, batch in enumerate(batches):

    try:

        status_text.text(
            f"Scanning batch {idx+1}/{total_batch}"
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

                df["Close"] = (
                    df["Close"]
                    .ffill()
                    .fillna(0)
                )

                df["Volume"] = (
                    df["Volume"]
                    .fillna(0)
                )

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

                # VALIDATION

                if pd.isna(avg_volume_20):
                    continue

                if pd.isna(avg_value_20):
                    continue

                if avg_volume_20 <= 0:
                    continue

                if avg_value_20 <= 0:
                    continue

                ratio_volume = (
                    volume_today /
                    avg_volume_20
                )

                ratio_value = (
                    value_today /
                    avg_value_20
                )

                # FILTER ONLY ACTIVE STOCK

                if ratio_volume < 2:
                    continue

                # SIGNAL

                if ratio_volume >= 5:
                    signal = "🔥 SUPER"

                elif ratio_volume >= 3:
                    signal = "🚀 HIGH"

                else:
                    signal = "⚡ ACTIVE"

                # CATEGORY

                category = "OTHER"

                for cat, members in category_map.items():

                    if stock in members:
                        category = cat
                        break

                hasil.append({

                    "Ticker":
                        stock,

                    "Category":
                        category,

                    "Signal":
                        signal,

                    "Avg Volume 20":
                        f"{avg_volume_20:,.0f}".replace(",", "."),

                    "Volume Today":
                        f"{volume_today:,.0f}".replace(",", "."),

                    "Volume Ratio":
                        round(ratio_volume, 2),

                    "Avg Value 20":
                        "Rp " +
                        f"{avg_value_20:,.0f}".replace(",", "."),

                    "Value Today":
                        "Rp " +
                        f"{value_today:,.0f}".replace(",", "."),

                    "Value Ratio":
                        round(ratio_value, 2)

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

    if search_ticker:

        hasil_df = hasil_df[
            hasil_df["Ticker"]
            .str.contains(
                search_ticker.upper()
            )
        ]

    if signal_filter != "ALL":

        hasil_df = hasil_df[
            hasil_df["Signal"] ==
            signal_filter
        ]

    hasil_df = hasil_df.sort_values(
        by="Value Ratio",
        ascending=False
    )

# =====================================================
# METRICS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Signal",
        len(hasil_df)
    )

with col2:

    st.metric(
        "Total Stocks",
        len(stocks)
    )

with col3:

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
    height=700
)

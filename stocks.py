import pandas as pd

# =====================================================
# AMBIL SELURUH SAHAM IDX
# =====================================================

url = "https://www.idx.co.id/primary/TradingSummary/GetStockCode"

try:

    df = pd.read_json(url)

    STOCKS = [
        f"{kode}.JK"
        for kode in df["Code"].tolist()
    ]

except:

    # fallback jika server IDX gagal
    STOCKS = [

        "BBCA.JK",
        "BBRI.JK",
        "BMRI.JK",
        "BBNI.JK",
        "BRIS.JK",

        "ANTM.JK",
        "ADRO.JK",
        "PTBA.JK",
        "TINS.JK",

        "TLKM.JK",
        "ISAT.JK",
        "EXCL.JK",

        "ASII.JK",
        "UNVR.JK",
        "ICBP.JK",
        "INDF.JK",

        "CPIN.JK",
        "JPFA.JK",

        "PWON.JK",
        "BSDE.JK",
        "CTRA.JK"

    ]

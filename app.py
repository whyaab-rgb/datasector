# =========================================================
# IDX AI SCREENER REALTIME - DATASectors/API + TELEGRAM
# Final single-file Streamlit app
# =========================================================
# Cara pakai:
# 1) pip install streamlit pandas numpy requests plotly yfinance
# 2) streamlit run app_datasectors_realtime_final.py
# 3) Isi API Key DataSectors di sidebar / Streamlit Secrets.
#
# Streamlit Secrets opsional (.streamlit/secrets.toml):
# DATASECTORS_API_KEY = "ISI_API_KEY"
# TELEGRAM_BOT_TOKEN = "ISI_TOKEN"
# TELEGRAM_CHAT_ID = "ISI_CHAT_ID"
# =========================================================

from __future__ import annotations

import time
import math
import requests
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, Dict, List, Optional, Tuple

# yfinance hanya fallback, bukan sumber utama.
try:
    import yfinance as yf
except Exception:  # pragma: no cover
    yf = None

# =========================================================
# CONFIG
# =========================================================
WIB = ZoneInfo("Asia/Jakarta")
DEFAULT_BASE_URL = "https://api.datasectors.com/api"
APP_TITLE = "IDX AI SCREENER — REALTIME API FINAL"

# Master kode saham. App juga bisa ambil symbol list dari API kalau endpoint tersedia.
IDX_MASTER = [
    "AALI","ABBA","ABDA","ABMM","ACES","ACST","ADCP","ADES","ADHI","ADMF","ADMG","ADMR","ADRO","AGAR","AGII","AGRO","AGRS","AHAP","AIMS","AISA","AKKU","AKPI","AKRA","AKSI","ALDO","ALKA","ALMI","ALTO","AMAG","AMAR","AMFG","AMIN","AMMN","AMOR","AMRT","ANDI","ANJT","ANTM","APEX","APIC","APII","APLI","APLN","ARCI","ARGO","ARKA","ARMY","ARTA","ARTI","ASBI","ASDM","ASGR","ASII","ASJT","ASMI","ASRI","ASRM","ASSA","ATAP","ATIC","AUTO","AVIA","AXIO",
    "BACA","BAJA","BALI","BANK","BAPA","BAPI","BATA","BBCA","BBHI","BBKP","BBLD","BBMD","BBNI","BBRI","BBTN","BBYB","BCAP","BCIC","BCIP","BDMN","BEKS","BEST","BFIN","BHAT","BHIT","BIKA","BIMA","BINA","BIPI","BJBR","BJTM","BKDP","BKSL","BLTA","BLUE","BMAS","BMRI","BMSR","BMTR","BNBA","BNBR","BNGA","BNII","BNLI","BOLA","BOSS","BPFI","BPII","BRAM","BRIS","BRMS","BRNA","BRPT","BSDE","BSJP","BSSR","BTEL","BTON","BTPN","BTPS","BUKA","BULL","BUMI","BUVA","BVIC",
    "CAMP","CANI","CARE","CARS","CBMF","CBUT","CCSI","CEKA","CENT","CFIN","CGAS","CHEM","CINT","CITA","CITY","CLAY","CLEO","CMNP","CMRY","CNKO","CNMA","COAL","CODE","CPIN","CPRO","CSAP","CSIS","CTBN","CTRA","CTTH","CUAN",
    "DADA","DART","DAYA","DEAL","DEFI","DEPO","DEWA","DGIK","DILD","DKFT","DLTA","DMAS","DNAR","DOID","DPNS","DSFI","DSNG","DSSA","DUTI","DVLA","EDGE","EKAD","ELSA","EMDE","EMTK","ENAK","ENRG","ENVY","EPAC","ERAA","ESSA","ESTA","ETWA",
    "FAPA","FASW","FILM","FINN","FIRE","FISH","FLMC","FMII","FPNI","FREN","GAMA","GDST","GEMS","GGRM","GIAA","GJTL","GLVA","GMFI","GOLD","GOOD","GPRA","GSMF","GTRA","GTSI","GULA",
    "HADI","HAIS","HAPS","HATM","HDFA","HDIT","HEAL","HELI","HERO","HEXA","HITS","HKMU","HKTI","HMSP","HOPE","HRME","HRTA","HUMI","HYAM",
    "IBST","ICBP","ICON","IDEA","IDPR","IFII","IGAR","IIKP","IKAI","IKBI","IKPM","IMAS","IMJS","IMPC","INAF","INAI","INCF","INCI","INCO","INDF","INDR","INDX","INDY","INKP","INOV","INPC","INPP","INTA","INTP","IPCC","IPCM","IPOL","ISAT","ISSP","ITIC","ITMG",
    "JARR","JAST","JAYA","JECC","JGLE","JIHD","JKON","JKSW","JMAS","JPFA","JRPT","JSKY","KAEF","KARW","KAYU","KBAG","KBLM","KBLV","KBRI","KDSI","KICI","KINO","KIOS","KKGI","KLBF","KMDS","KMTR","KOBX","KOIN","KONI","KOPI","KPAS","KPIG","KRAS","KREN",
    "LABA","LAPD","LCGP","LEAD","LIFE","LINK","LION","LMAS","LMPI","LMSH","LPCK","LPIN","LPKR","LPLI","LSIP","LTLS","LUCY",
    "MAIN","MAPA","MAPB","MARK","MASA","MAYA","MBAP","MBSS","MCAS","MCOL","MDIA","MDKA","MDLN","MEDC","MEGA","MERK","META","MFIN","MFMI","MGNA","MGRO","MICE","MIDI","MIKA","MIRA","MITI","MKNT","MLBI","MLIA","MLPL","MLPT","MMIX","MMLP","MNCN","MNCS","MNTO","MPMX","MPPA","MRAT","MREI","MSIN","MSKY","MTDL","MTFN","MTLA","MTMH","MTPS","MTSM","MYOH","MYOR",
    "NANO","NASA","NELY","NFCX","NICK","NICL","NIRO","NISP","NKON","NOBU","NRCA","NTBK","NUSA","OASA","OCAP","OILS","OKAS","OMRE","OPMS","OPTI","ORIN",
    "PACK","PALM","PAMG","PANI","PANS","PBID","PBRX","PCAR","PEGE","PGAS","PGEO","PGLI","PGUN","PICO","PINA","PIPP","PKPK","PLAS","PLIN","PMJS","PNBN","PNBS","PNGO","PNIN","PNLF","POLA","POLI","POLU","POOL","PPGL","PPRE","PRAS","PRDA","PRIM","PSAB","PSDN","PSGO","PSKT","PSSI","PTBA","PTIS","PTPP","PTRO","PTSN","PTSP","PURE","PWON",
    "RAAM","RAJA","RALS","RANC","RBMS","RDTX","REAL","RELI","RICY","RIGS","RISE","RMBA","RODA","ROTI","RUIS","SAME","SAMF","SAPX","SATU","SBAT","SBCO","SBER","SBMA","SCBD","SCMA","SDMU","SDPC","SDRA","SGER","SGRO","SIDO","SILO","SIMA","SIMP","SING","SIPD","SKBM","SKLT","SKRN","SMAR","SMBR","SMCB","SMDR","SMGR","SMIL","SMKL","SMKM","SMMA","SMMT","SMRA","SMSM","SNLK","SOCI","SOHO","SONA","SPMA","SPTO","SRAJ","SRTG","SSIA","SSMS","SSTM","STAR","STTP","SULI","SUPR","SURYA","SWAT",
    "TALF","TAMA","TAMU","TAPG","TARA","TAXI","TBIG","TBLA","TBMS","TCID","TCPI","TDPM","TEBE","TECH","TELE","TFAS","TFCO","TGKA","TGRA","TIFA","TINS","TKIM","TLKM","TMAS","TOBA","TOOL","TOPS","TOTL","TOTO","TOWR","TPIA","TPMA","TRAM","TRIM","TRIN","TRIO","TRIS","TRJA","TRUK","TSPC",
    "UANG","UFOE","ULTJ","UNIC","UNIQ","UNIT","UNSP","UNTR","UNVR","VAST","VICO","VINS","VIVA","VKTR","WAPO","WEGE","WICO","WIDI","WIIM","WIKA","WINE","WINR","WINS","WIRG","WIRY","WOMF","WOOD","YELO","YPAS","YULE","ZBRA","ZINC"
]

WATCHLISTS = {
    "IDX Top 50": IDX_MASTER[:50],
    "IDX Top 100": IDX_MASTER[:100],
    "IDX Top 300": IDX_MASTER[:300],
    "All Master": IDX_MASTER,
    "Custom": [],
}

# =========================================================
# PAGE STYLE
# =========================================================
st.set_page_config(page_title="IDX AI Screener API", layout="wide")
st.markdown(
    """
<style>
.stApp { background: linear-gradient(180deg,#071019 0%,#0a1320 100%); color: white; }
.block-container { max-width: 99%; padding-top: 0.8rem; padding-bottom: 1rem; }
[data-testid="stSidebar"] { background-color: #09111d; }
h1,h2,h3,h4,h5,h6,p,span,div,label { color: #e8f0ff !important; }
.small-note { font-size: 12px; color: #9db1cc !important; }
.warn-box { background:#311b00;border:1px solid #d97706;border-radius:10px;padding:10px;margin:8px 0; }
.ok-box { background:#052e16;border:1px solid #16a34a;border-radius:10px;padding:10px;margin:8px 0; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# GENERAL HELPERS
# =========================================================
def now_wib() -> datetime:
    return datetime.now(WIB)


def fmt_time() -> str:
    return now_wib().strftime("%d-%m-%Y %H:%M:%S WIB")


def normalize_symbol(symbol: str, for_yfinance: bool = False) -> str:
    s = str(symbol or "").strip().upper().replace(".JK", "")
    if not s:
        return ""
    return f"{s}.JK" if for_yfinance else s


def safe_float(x: Any, default: float = np.nan) -> float:
    try:
        if x is None:
            return default
        if isinstance(x, str):
            x = x.replace(",", "").strip()
            if x in ["", "-", "None", "nan"]:
                return default
        return float(x)
    except Exception:
        return default


def latest(series: pd.Series) -> float:
    try:
        return float(series.dropna().iloc[-1])
    except Exception:
        return np.nan


def fmt_price(v: Any) -> str:
    v = safe_float(v)
    if pd.isna(v):
        return "-"
    if abs(v) >= 100:
        return f"{v:,.0f}"
    return f"{v:,.2f}"


def fmt_pct(v: Any) -> str:
    v = safe_float(v)
    if pd.isna(v):
        return "-"
    return f"{v:.1f}%"


def rsi_cell_text(v: Any) -> str:
    v = safe_float(v)
    if pd.isna(v):
        return "-"
    return f"{v:.1f}"


def human_value(v: Any) -> str:
    v = safe_float(v)
    if pd.isna(v):
        return "-"
    if abs(v) >= 1_000_000_000_000:
        return f"{v / 1_000_000_000_000:.1f}T"
    if abs(v) >= 1_000_000_000:
        return f"{v / 1_000_000_000:.1f}B"
    if abs(v) >= 1_000_000:
        return f"{v / 1_000_000:.1f}M"
    return f"{v:,.0f}"


def auto_refresh_fragment(seconds: int):
    st.markdown(
        f"""
        <script>
        setTimeout(function() {{ window.parent.location.reload(); }}, {int(seconds) * 1000});
        </script>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# DATASectors/API CLIENT
# =========================================================
def get_secret(name: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return default


def _extract_payload(json_obj: Any) -> Any:
    """Ambil isi utama dari response API yang bentuknya bisa data/result/items/candles."""
    if isinstance(json_obj, dict):
        for key in ["data", "result", "results", "items", "candles", "rows", "ohlcv", "prices"]:
            if key in json_obj and json_obj[key] is not None:
                return json_obj[key]
    return json_obj


def api_request(base_url: str, api_key: str, endpoint: str, method: str = "POST", payload: Optional[Dict[str, Any]] = None) -> Any:
    url = base_url.rstrip("/") + "/" + endpoint.lstrip("/")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
        headers["Authorization"] = f"Bearer {api_key}"

    method = method.upper()
    if method == "GET":
        r = requests.get(url, headers=headers, params=payload or {}, timeout=20)
    else:
        r = requests.post(url, headers=headers, json=payload or {}, timeout=20)
    r.raise_for_status()
    return r.json()


def try_api_endpoints(base_url: str, api_key: str, endpoints: List[str], payloads: List[Dict[str, Any]], methods: List[str]) -> Tuple[Any, str]:
    last_err = ""
    for endpoint in endpoints:
        for payload in payloads:
            for method in methods:
                try:
                    res = api_request(base_url, api_key, endpoint, method, payload)
                    return res, f"{method} /{endpoint}"
                except Exception as e:
                    last_err = str(e)[:180]
    raise RuntimeError(last_err or "Tidak ada endpoint yang berhasil")


def normalize_ohlcv_dataframe(raw: Any) -> pd.DataFrame:
    payload = _extract_payload(raw)

    # Jika API mengembalikan dict berisi list di salah satu key.
    if isinstance(payload, dict):
        for key in ["candles", "ohlcv", "prices", "items", "rows", "data"]:
            if isinstance(payload.get(key), list):
                payload = payload[key]
                break

    if not isinstance(payload, list) or len(payload) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(payload)
    if df.empty:
        return pd.DataFrame()

    # Mapping nama kolom umum.
    col_map = {}
    lower_cols = {str(c).lower(): c for c in df.columns}

    def pick(names: List[str]) -> Optional[str]:
        for n in names:
            if n.lower() in lower_cols:
                return lower_cols[n.lower()]
        return None

    mapping = {
        "Open": pick(["open", "o", "Open"]),
        "High": pick(["high", "h", "High"]),
        "Low": pick(["low", "l", "Low"]),
        "Close": pick(["close", "c", "last", "price", "Close"]),
        "Volume": pick(["volume", "v", "vol", "Volume"]),
    }
    date_col = pick(["date", "datetime", "time", "timestamp", "t"])

    for target, source in mapping.items():
        if source is not None:
            col_map[source] = target
    df = df.rename(columns=col_map)

    needed = ["Open", "High", "Low", "Close", "Volume"]
    for col in needed:
        if col not in df.columns:
            return pd.DataFrame()
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if date_col is not None and date_col in df.columns:
        dt = pd.to_datetime(df[date_col], errors="coerce", unit="ms")
        if dt.isna().all():
            dt = pd.to_datetime(df[date_col], errors="coerce")
        df.index = dt
    else:
        df.index = pd.RangeIndex(len(df))

    df = df.dropna(subset=["Open", "High", "Low", "Close"]).copy()
    df = df[needed].sort_index()
    return df


@st.cache_data(ttl=60, show_spinner=False)
def get_ohlcv_datasectors(symbol: str, base_url: str, api_key: str, period: str, interval: str, custom_endpoint: str = "") -> Tuple[pd.DataFrame, str]:
    s = normalize_symbol(symbol, for_yfinance=False)
    endpoints = [custom_endpoint] if custom_endpoint else [
        "stock/ohlcv", "stocks/ohlcv", "market/ohlcv", "chart/ohlcv", "ohlcv",
        "stock/chart", "stocks/chart", "market/chart", "chart", "price/ohlcv"
    ]
    payloads = [
        {"symbol": s, "period": period, "interval": interval},
        {"ticker": s, "period": period, "interval": interval},
        {"code": s, "period": period, "interval": interval},
        {"symbol": s, "timeframe": interval, "range": period},
    ]
    try:
        raw, used = try_api_endpoints(base_url, api_key, endpoints, payloads, ["POST", "GET"])
        df = normalize_ohlcv_dataframe(raw)
        return df, used
    except Exception as e:
        return pd.DataFrame(), f"API gagal: {str(e)[:120]}"


@st.cache_data(ttl=60, show_spinner=False)
def get_symbol_list_datasectors(base_url: str, api_key: str, custom_endpoint: str = "") -> Tuple[List[str], str]:
    endpoints = [custom_endpoint] if custom_endpoint else [
        "stock/list", "stocks/list", "symbols", "stock/symbols", "market/symbols", "companies", "emiten/list"
    ]
    try:
        raw, used = try_api_endpoints(base_url, api_key, endpoints, [{}], ["GET", "POST"])
        payload = _extract_payload(raw)
        if isinstance(payload, dict):
            for key in ["items", "rows", "symbols", "stocks", "companies", "data"]:
                if isinstance(payload.get(key), list):
                    payload = payload[key]
                    break
        out: List[str] = []
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, str):
                    out.append(normalize_symbol(item))
                elif isinstance(item, dict):
                    for key in ["symbol", "ticker", "code", "kode"]:
                        if item.get(key):
                            out.append(normalize_symbol(item[key]))
                            break
        out = sorted(list(dict.fromkeys([x for x in out if x])))
        return out, used
    except Exception as e:
        return [], f"symbol API gagal: {str(e)[:120]}"


@st.cache_data(ttl=60, show_spinner=False)
def get_ohlcv_yfinance(symbol: str, period: str, interval: str) -> Tuple[pd.DataFrame, str]:
    if yf is None:
        return pd.DataFrame(), "yfinance tidak terinstall"
    try:
        ysym = normalize_symbol(symbol, for_yfinance=True)
        df = yf.download(ysym, period=period, interval=interval, auto_adjust=False, progress=False, threads=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        required = ["Open", "High", "Low", "Close", "Volume"]
        if df.empty or not all(c in df.columns for c in required):
            return pd.DataFrame(), "yfinance kosong"
        return df[required].dropna(subset=["Open", "High", "Low", "Close"]).copy(), "yfinance fallback"
    except Exception as e:
        return pd.DataFrame(), f"yfinance error: {e}"


def get_ohlcv(symbol: str, source: str, base_url: str, api_key: str, period: str, interval: str, custom_endpoint: str, fallback_yf: bool) -> Tuple[pd.DataFrame, str]:
    if source == "DataSectors/API":
        df, used = get_ohlcv_datasectors(symbol, base_url, api_key, period, interval, custom_endpoint)
        if not df.empty:
            return df, used
        if fallback_yf:
            df2, used2 = get_ohlcv_yfinance(symbol, period, interval)
            return df2, f"{used} → {used2}"
        return df, used
    return get_ohlcv_yfinance(symbol, period, interval)

# =========================================================
# INDICATORS
# =========================================================
def calc_indicators(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        x[col] = pd.to_numeric(x[col], errors="coerce")
    x = x.dropna(subset=["Open", "High", "Low", "Close"])
    if x.empty:
        return x

    x["MA5"] = x["Close"].rolling(5).mean()
    x["MA10"] = x["Close"].rolling(10).mean()
    x["MA20"] = x["Close"].rolling(20).mean()
    x["MA50"] = x["Close"].rolling(50).mean()
    x["EMA9"] = x["Close"].ewm(span=9, adjust=False).mean()
    x["EMA20"] = x["Close"].ewm(span=20, adjust=False).mean()

    delta = x["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean().replace(0, np.nan)
    rs = avg_gain / avg_loss
    x["RSI"] = 100 - (100 / (1 + rs))

    ema12 = x["Close"].ewm(span=12, adjust=False).mean()
    ema26 = x["Close"].ewm(span=26, adjust=False).mean()
    x["MACD"] = ema12 - ema26
    x["MACD_SIGNAL"] = x["MACD"].ewm(span=9, adjust=False).mean()
    x["MACD_HIST"] = x["MACD"] - x["MACD_SIGNAL"]

    x["BB_MID"] = x["Close"].rolling(20).mean()
    std20 = x["Close"].rolling(20).std()
    x["BB_UPPER"] = x["BB_MID"] + 2 * std20
    x["BB_LOWER"] = x["BB_MID"] - 2 * std20

    x["VOL_MA5"] = x["Volume"].rolling(5).mean()
    x["VOL_MA20"] = x["Volume"].rolling(20).mean()
    x["SUPPORT20"] = x["Low"].rolling(20).min()
    x["RESIST20"] = x["High"].rolling(20).max()

    high_low = x["High"] - x["Low"]
    high_close = np.abs(x["High"] - x["Close"].shift())
    low_close = np.abs(x["Low"] - x["Close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    x["ATR14"] = tr.rolling(14).mean()

    upper_wick = x["High"] - x[["Open", "Close"]].max(axis=1)
    lower_wick = x[["Open", "Close"]].min(axis=1) - x["Low"]
    candle_range = (x["High"] - x["Low"]).replace(0, np.nan)
    x["WICK_PCT"] = ((upper_wick.clip(lower=0) + lower_wick.clip(lower=0)) / candle_range) * 100
    return x

# =========================================================
# SIGNAL ENGINE
# =========================================================
def get_phase(df: pd.DataFrame) -> str:
    recent = df.tail(10)
    score = 0
    for _, row in recent.iterrows():
        vol_ma20 = row.get("VOL_MA20", np.nan)
        if pd.isna(vol_ma20) or vol_ma20 <= 0:
            continue
        if row["Close"] > row["Open"] and row["Volume"] > vol_ma20:
            score += 1
        elif row["Close"] < row["Open"] and row["Volume"] > vol_ma20:
            score -= 1
    if score >= 4:
        return "BIG AKUM"
    if score >= 2:
        return "AKUM"
    if score <= -4:
        return "BIG DIST"
    if score <= -2:
        return "DIST"
    return "NEUTRAL"


def get_trend(close_: float, ma20: float, ma50: float) -> str:
    if pd.isna(close_) or pd.isna(ma20) or pd.isna(ma50):
        return "NEUTRAL"
    if close_ > ma20 > ma50:
        return "BULL"
    if close_ < ma20 < ma50:
        return "BEAR"
    return "NEUTRAL"


def get_rsi_signal(rsi: float, macd: float, macd_signal: float) -> str:
    if pd.isna(rsi) or pd.isna(macd) or pd.isna(macd_signal):
        return "WAIT"
    if 48 <= rsi <= 55 and macd > macd_signal:
        return "GOLDEN"
    if rsi >= 58 and macd > macd_signal:
        return "UP"
    if rsi <= 42 and macd < macd_signal:
        return "DEAD"
    return "UP" if rsi >= 50 else "DEAD"


def get_signal_label(close_, ma20, ma50, ema9, rsi, macd, macd_signal, vol, vol_ma20, support, resistance, wick):
    if any(pd.isna(v) for v in [close_, ma20, ema9, rsi, macd, macd_signal]):
        return "WAIT"
    bullish = macd > macd_signal
    near_support = not pd.isna(support) and close_ <= support * 1.04
    near_resistance = not pd.isna(resistance) and close_ >= resistance * 0.985
    vol_ok = not pd.isna(vol_ma20) and vol > vol_ma20
    trend_bull = not pd.isna(ma50) and close_ > ma20 > ma50

    if bullish and vol_ok and near_resistance and rsi >= 58:
        return "ON TRACK"
    if bullish and close_ > ema9 > ma20 and rsi >= 62 and vol_ok:
        return "SUPER"
    if bullish and near_support and rsi < 42:
        return "REBOUND"
    if bullish and vol_ok and close_ > ma20:
        return "AKUM"
    if trend_bull and 50 <= rsi <= 60 and (pd.isna(wick) or wick < 35):
        return "HAKA"
    if rsi >= 72 and (not pd.isna(wick) and wick >= 35):
        return "WASPADA OB"
    if close_ < ma20 and not bullish and rsi < 45:
        return "DIST"
    if 47 <= rsi <= 54 and bullish:
        return "GC NOW"
    return "WAIT"


def get_action_label(signal_label: str, close_: float, entry_low: float, entry_high: float, trend: str) -> str:
    if signal_label == "SUPER":
        return "SIAP BELI"
    if signal_label in ["ON TRACK", "AKUM", "HAKA", "GC NOW", "REBOUND"]:
        if not pd.isna(entry_low) and not pd.isna(entry_high) and entry_low <= close_ <= entry_high:
            return "AT ENTRY"
        return "WATCH"
    if signal_label == "WASPADA OB":
        return "WASPADA OB"
    if trend == "BULL":
        return "HOLD"
    return "WAIT GC"


def build_entry_zone(close_, support, ma20, atr, resistance) -> Dict[str, Any]:
    if pd.isna(close_):
        return {"entry_low": np.nan, "entry_high": np.nan, "entry_zone": "-", "entry_status": "WAIT DATA"}
    if pd.isna(atr) or atr <= 0:
        atr = close_ * 0.03
    if not pd.isna(support) and not pd.isna(ma20):
        base = (support + ma20) / 2
    elif not pd.isna(support):
        base = support
    elif not pd.isna(ma20):
        base = ma20
    else:
        base = close_
    entry_low = round(base - (atr * 0.30))
    entry_high = round(base + (atr * 0.30))
    if close_ < entry_low:
        status = "BELOW ZONE"
    elif entry_low <= close_ <= entry_high:
        status = "IN ZONE"
    elif not pd.isna(resistance) and close_ >= resistance * 0.985:
        status = "BREAKOUT ZONE"
    else:
        status = "ABOVE ZONE"
    return {"entry_low": entry_low, "entry_high": entry_high, "entry_zone": f"{fmt_price(entry_low)} - {fmt_price(entry_high)}", "entry_status": status}


def compute_scores(df: pd.DataFrame) -> Dict[str, int]:
    close_ = latest(df["Close"])
    ma20 = latest(df["MA20"])
    ma50 = latest(df["MA50"])
    ema9 = latest(df["EMA9"])
    rsi = latest(df["RSI"])
    macd = latest(df["MACD"])
    macd_signal = latest(df["MACD_SIGNAL"])
    volume = latest(df["Volume"])
    vol_ma5 = latest(df["VOL_MA5"])
    vol_ma20 = latest(df["VOL_MA20"])
    support = latest(df["SUPPORT20"])
    resistance = latest(df["RESIST20"])
    bb_lower = latest(df["BB_LOWER"])
    wick = latest(df["WICK_PCT"])

    scalping = 0
    if close_ > ema9 > ma20: scalping += 3
    if 55 <= rsi <= 72: scalping += 2
    if macd > macd_signal: scalping += 2
    if not pd.isna(vol_ma5) and volume > vol_ma5: scalping += 2
    if not pd.isna(resistance) and close_ >= resistance * 0.985: scalping += 1
    if pd.isna(wick) or wick < 35: scalping += 1

    bsjp = 0
    if not pd.isna(rsi):
        if rsi < 35: bsjp += 3
        elif 35 <= rsi <= 45: bsjp += 1
    if not pd.isna(bb_lower) and close_ <= bb_lower * 1.03: bsjp += 2
    if not pd.isna(support) and close_ <= support * 1.05: bsjp += 2
    if len(df) > 1 and df["Close"].iloc[-1] > df["Close"].iloc[-2]: bsjp += 1
    if df["MACD_HIST"].iloc[-1] > 0: bsjp += 2

    swing = 0
    if close_ > ma20 > ma50: swing += 3
    if 50 <= rsi <= 65: swing += 2
    if macd > macd_signal: swing += 2
    if not pd.isna(vol_ma20) and volume > vol_ma20: swing += 1
    if (not pd.isna(resistance)) and (not pd.isna(support)) and close_ < resistance * 0.93 and close_ > support * 1.08: swing += 1

    bandar = 0
    phase = get_phase(df)
    if phase == "BIG AKUM": bandar += 4
    elif phase == "AKUM": bandar += 2
    elif phase == "DIST": bandar -= 2
    elif phase == "BIG DIST": bandar -= 4
    if not pd.isna(vol_ma20) and vol_ma20 > 0 and volume > vol_ma20 * 1.2: bandar += 2
    if close_ > ma20: bandar += 1

    return {"scalping": max(0, scalping), "bsjp": max(0, bsjp), "swing": max(0, swing), "bandar": bandar}


def compute_accum_score(close_, ma20, ma50, rsi, rvol, val, phase, signal, gain) -> int:
    score = 0
    if not pd.isna(rvol):
        if rvol >= 250: score += 30
        elif rvol >= 180: score += 24
        elif rvol >= 120: score += 18
        elif rvol >= 100: score += 10
    if not pd.isna(val):
        if val >= 100_000_000_000: score += 20
        elif val >= 50_000_000_000: score += 15
        elif val >= 20_000_000_000: score += 10
        elif val >= 10_000_000_000: score += 6
    if not pd.isna(close_) and not pd.isna(ma20) and close_ > ma20: score += 8
    if not pd.isna(ma20) and not pd.isna(ma50) and ma20 > ma50: score += 8
    if not pd.isna(rsi):
        if 52 <= rsi <= 68: score += 10
        elif 45 <= rsi < 52: score += 5
    if phase == "BIG AKUM": score += 15
    elif phase == "AKUM": score += 10
    elif phase == "DIST": score -= 8
    elif phase == "BIG DIST": score -= 15
    if signal in ["SUPER", "ON TRACK", "AKUM", "HAKA", "GC NOW"]: score += 10
    if not pd.isna(gain):
        if gain > 0: score += 4
        elif gain < -3: score -= 5
    return int(max(0, min(score, 100)))


def build_row(symbol: str, raw_df: pd.DataFrame, source_info: str) -> Optional[Dict[str, Any]]:
    df = calc_indicators(raw_df)
    if len(df) < 30:
        return None

    close_ = latest(df["Close"])
    prev_close = float(df["Close"].dropna().iloc[-2]) if len(df.dropna(subset=["Close"])) > 1 else close_
    gain = ((close_ - prev_close) / prev_close * 100) if prev_close else 0.0
    wick = latest(df["WICK_PCT"])
    rsi = latest(df["RSI"])
    macd = latest(df["MACD"])
    macd_signal = latest(df["MACD_SIGNAL"])
    vol = latest(df["Volume"])
    vol_ma20 = latest(df["VOL_MA20"])
    ma20 = latest(df["MA20"])
    ma50 = latest(df["MA50"])
    ema9 = latest(df["EMA9"])
    support = latest(df["SUPPORT20"])
    resistance = latest(df["RESIST20"])
    atr = latest(df["ATR14"])

    rvol = (vol / vol_ma20 * 100) if not pd.isna(vol_ma20) and vol_ma20 > 0 else np.nan
    zone = build_entry_zone(close_, support, ma20, atr, resistance)
    entry_low = zone["entry_low"]
    entry_high = zone["entry_high"]
    tp1 = round(close_ + (atr * 1.0)) if not pd.isna(atr) else round(close_ * 1.03)
    tp2 = round(close_ + (atr * 2.0)) if not pd.isna(atr) else round(close_ * 1.06)
    tp3 = round(close_ + (atr * 3.0)) if not pd.isna(atr) else round(close_ * 1.10)
    sl = round(entry_low - (atr * 0.70)) if not pd.isna(entry_low) and not pd.isna(atr) else round(close_ * 0.97)

    trend = get_trend(close_, ma20, ma50)
    phase = get_phase(df)
    rsi_sig = get_rsi_signal(rsi, macd, macd_signal)
    sinyal = get_signal_label(close_, ma20, ma50, ema9, rsi, macd, macd_signal, vol, vol_ma20, support, resistance, wick)
    aksi = get_action_label(sinyal, close_, entry_low, entry_high, trend)
    val = close_ * vol if not pd.isna(close_) and not pd.isna(vol) else np.nan
    scores = compute_scores(df)
    total = scores["scalping"] + scores["bsjp"] + scores["swing"] + scores["bandar"]
    accum_score = compute_accum_score(close_, ma20, ma50, rsi, rvol, val, phase, sinyal, gain)
    profit = ((close_ - entry_low) / entry_low * 100) if entry_low else 0.0
    to_tp = ((tp2 - close_) / close_ * 100) if close_ else 0.0

    return {
        "symbol": normalize_symbol(symbol), "full_symbol": normalize_symbol(symbol), "source": source_info,
        "gain": gain, "wick": wick, "aksi": aksi, "sinyal": sinyal, "rvol": rvol,
        "entry": entry_low, "entry_low": entry_low, "entry_high": entry_high, "entry_zone": zone["entry_zone"], "entry_status": zone["entry_status"],
        "now": close_, "support": support, "resistance": resistance,
        "tp": tp2, "tp1": tp1, "tp2": tp2, "tp3": tp3, "tp_zone": f"{fmt_price(tp1)} / {fmt_price(tp2)} / {fmt_price(tp3)}", "sl": sl,
        "profit": profit, "to_tp": to_tp, "rsi": rsi, "rsi_sig": rsi_sig, "rsi_5m": np.nan,
        "val": val, "fase": phase, "trend": trend,
        "score_scalping": scores["scalping"], "score_bsjp": scores["bsjp"], "score_swing": scores["swing"], "score_bandar": scores["bandar"],
        "score_total": total, "score_accum": accum_score, "daily_df": df,
    }

# =========================================================
# COLORS
# =========================================================
def bg_accum_score(v):
    v = safe_float(v, 0)
    return "#9333ea" if v >= 70 else "#16a34a" if v >= 55 else "#2563eb" if v >= 40 else "#374151"

def bg_gain(v):
    v = safe_float(v, 0)
    return "#10b981" if v > 3 else "#15803d" if v > 0 else "#dc2626" if v > -2 else "#991b1b"

def bg_wick(v):
    v = safe_float(v, 999)
    return "#0f766e" if v < 15 else "#2563eb" if v < 25 else "#d97706" if v < 35 else "#dc2626"

def bg_aksi(v):
    return {"AT ENTRY":"#1d4ed8","WATCH":"#b45309","WAIT GC":"#374151","HOLD":"#2563eb","SIAP BELI":"#7c3aed","WASPADA OB":"#d97706"}.get(str(v), "#334155")

def bg_sinyal(v):
    return {"ON TRACK":"#16a34a","REBOUND":"#d97706","AKUM":"#15803d","DIST":"#b91c1c","SUPER":"#7e22ce","HAKA":"#14b8a6","GC NOW":"#9333ea","WASPADA OB":"#ea580c","WAIT":"#111827"}.get(str(v), "#334155")

def bg_rvol(v):
    v = safe_float(v, 0)
    return "#9333ea" if v >= 250 else "#f97316" if v >= 150 else "#2563eb" if v >= 100 else "#374151"

def bg_price(kind):
    return {"entry":"#1d4ed8","now":"#2563eb","tp":"#16a34a","sl":"#b91c1c"}.get(kind, "#243244")

def bg_profit(v):
    v = safe_float(v, 0)
    return "#16a34a" if v > 2 else "#0f766e" if v > 0 else "#92400e" if v > -2 else "#b91c1c"

def bg_to_tp(v):
    v = safe_float(v, 999)
    return "#f97316" if v <= 1 else "#16a34a" if v <= 3 else "#0f766e"

def bg_rsi_sig(v):
    return {"UP":"#16a34a","DEAD":"#dc2626","GOLDEN":"#7c3aed","WAIT":"#111827"}.get(str(v), "#334155")

def bg_rsi(v):
    v = safe_float(v, np.nan)
    if pd.isna(v): return "#243244"
    return "#f59e0b" if v >= 70 else "#16a34a" if v >= 55 else "#2563eb" if v >= 45 else "#7c3aed"

def bg_fase(v):
    return {"BIG AKUM":"#9333ea","AKUM":"#16a34a","NEUTRAL":"#374151","DIST":"#dc2626","BIG DIST":"#991b1b"}.get(str(v), "#334155")

def bg_trend(v):
    return {"BULL":"#16a34a","BEAR":"#dc2626","NEUTRAL":"#6b7280"}.get(str(v), "#334155")

def bg_entry_status(v):
    return {"IN ZONE":"#16a34a","BREAKOUT ZONE":"#9333ea","ABOVE ZONE":"#d97706","BELOW ZONE":"#2563eb","WAIT DATA":"#374151"}.get(str(v), "#374151")

# =========================================================
# TELEGRAM
# =========================================================
def send_telegram_message(bot_token: str, chat_id: str, message: str) -> Tuple[bool, str]:
    if not bot_token or not chat_id:
        return False, "Bot token / chat_id kosong"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            return True, "Terkirim"
        return False, f"HTTP {r.status_code}: {r.text}"
    except Exception as e:
        return False, str(e)


def signal_emoji(row: pd.Series) -> str:
    sig = str(row.get("sinyal", "")).upper()
    if sig in ["SUPER", "ON TRACK", "AKUM", "HAKA"]: return "🔥 BUY"
    if sig in ["GC NOW", "REBOUND"]: return "📈 WATCH BUY"
    if sig in ["DIST", "WASPADA OB"]: return "⚠️ SELL/WASPADA"
    return "⏳ WAIT"


def risk_label(score: Any) -> str:
    s = safe_float(score, 0)
    return "LOW" if s >= 65 else "MEDIUM" if s >= 45 else "HIGH"


def build_box_telegram_message(row: pd.Series) -> str:
    symbol = str(row["symbol"])
    now = fmt_price(row["now"])
    gain = fmt_pct(row["gain"])
    rvol = fmt_pct(row["rvol"])
    value = human_value(row["val"])
    rsi = rsi_cell_text(row["rsi"])
    arah = "▼" if safe_float(row["gain"], 0) < 0 else "▲"
    sig_text = signal_emoji(row)
    risk = risk_label(row["score_accum"])
    message = f"""<pre>
┌──────────────────────────────────────────────┐
│ {symbol:<6} | REALTIME AI SCREENER           │
│ Harga : {now:<7} {arah} {gain:<9}            │
│ RVOL  : {rvol:<7} | Value : {value:<10}      │
│ Time  : {fmt_time():<28}│
├──────────────────────────────────────────────┤
│ Trend      : {str(row['trend']):<28}│
│ Fase       : {str(row['fase']):<28}│
│ Support    : {fmt_price(row['support']):<28}│
│ Resistance : {fmt_price(row['resistance']):<28}│
│ RSI        : {rsi:<28}│
├──────────────────────────────────────────────┤
│ AI Score   : {int(row['score_accum']):<28}│
│ Bandar     : {int(row['score_bandar']):<28}│
│ Momentum   : {int(row['score_total']):<28}│
│ Risiko     : {risk:<28}│
├──────────────────────────────────────────────┤
│ Sinyal     : {sig_text:<28}│
│ Entry Zone : {str(row['entry_zone']):<28}│
│ Status     : {str(row['entry_status']):<28}│
│ Stop Loss  : {fmt_price(row['sl']):<28}│
│ TP1/2/3    : {str(row['tp_zone']):<28}│
└──────────────────────────────────────────────┘
</pre>"""
    # Telegram batas 4096 char. Pesan box ini aman jauh di bawah batas.
    return message[:3900]


def build_alert_df(df: pd.DataFrame, min_score: int, min_rvol: float, top_n: int, only_strong: bool) -> pd.DataFrame:
    if df.empty:
        return df
    x = df.copy()
    x = x[(x["score_accum"] >= min_score) & (x["rvol"].fillna(0) >= min_rvol)]
    if only_strong:
        x = x[x["sinyal"].isin(["SUPER", "ON TRACK", "AKUM", "HAKA", "GC NOW", "REBOUND"])]
    return x.sort_values(["score_accum", "score_total", "rvol", "gain"], ascending=[False, False, False, False]).head(top_n).reset_index(drop=True)


def send_rows_to_telegram(rows_df: pd.DataFrame, bot_token: str, chat_id: str) -> Tuple[int, str]:
    success = 0
    last_msg = ""
    for _, row in rows_df.iterrows():
        ok, msg = send_telegram_message(bot_token, chat_id, build_box_telegram_message(row))
        if ok:
            success += 1
        else:
            last_msg = msg
        time.sleep(0.25)
    return success, last_msg

# =========================================================
# SCREENER RUNNER
# =========================================================
@st.cache_data(ttl=60, show_spinner=False)
def run_screener(symbols: List[str], source: str, base_url: str, api_key: str, period: str, interval: str, custom_ohlcv_endpoint: str, fallback_yf: bool, max_price: float, max_symbols: int) -> Tuple[pd.DataFrame, List[str]]:
    rows: List[Dict[str, Any]] = []
    logs: List[str] = []
    clean_symbols = [normalize_symbol(s) for s in symbols if normalize_symbol(s)]
    clean_symbols = list(dict.fromkeys(clean_symbols))[:max_symbols]
    for sym in clean_symbols:
        try:
            raw_df, used = get_ohlcv(sym, source, base_url, api_key, period, interval, custom_ohlcv_endpoint, fallback_yf)
            if raw_df.empty:
                logs.append(f"{sym}: kosong ({used})")
                continue
            row = build_row(sym, raw_df, used)
            if row is None:
                logs.append(f"{sym}: data kurang dari 30 candle")
                continue
            if not pd.isna(row["now"]) and row["now"] <= max_price:
                rows.append(row)
        except Exception as e:
            logs.append(f"{sym}: {str(e)[:120]}")
            continue
    if not rows:
        return pd.DataFrame(), logs
    df = pd.DataFrame(rows).sort_values(["score_accum", "score_total", "rvol", "gain"], ascending=[False, False, False, False]).reset_index(drop=True)
    return df, logs


def apply_filters(df: pd.DataFrame, min_score: int, min_rvol: float, min_value: float, allowed_signals: List[str], allowed_trends: List[str], allowed_phases: List[str], entry_statuses: List[str]) -> pd.DataFrame:
    if df.empty:
        return df
    x = df.copy()
    x = x[x["score_accum"] >= min_score]
    x = x[x["rvol"].fillna(0) >= min_rvol]
    x = x[x["val"].fillna(0) >= min_value]
    if allowed_signals:
        x = x[x["sinyal"].isin(allowed_signals)]
    if allowed_trends:
        x = x[x["trend"].isin(allowed_trends)]
    if allowed_phases:
        x = x[x["fase"].isin(allowed_phases)]
    if entry_statuses:
        x = x[x["entry_status"].isin(entry_statuses)]
    return x.sort_values(["score_accum", "score_total", "rvol", "gain"], ascending=[False, False, False, False]).reset_index(drop=True)

# =========================================================
# HTML TABLE
# =========================================================
def make_html_table(df: pd.DataFrame, title: str, sub: str) -> str:
    html = f"""
<html><head><style>
body {{ margin:0; background:#07111b; color:white; font-family:Arial,Helvetica,sans-serif; }}
.screen-box {{ border:1px solid #17324d; border-radius:10px; padding:8px; background:#07111b; box-sizing:border-box; width:100%; }}
.screener-title {{ text-align:center; font-weight:800; font-size:13px; color:#eaf2ff; margin-bottom:4px; }}
.screener-sub {{ text-align:center; color:#9fb5d1; font-size:10px; margin-bottom:6px; }}
.table-wrap {{ width:100%; overflow-x:auto; }}
.custom-table {{ width:100%; border-collapse:collapse; font-size:11px; min-width:1900px; }}
.custom-table th {{ background:#184574; color:#ffffff; border:1px solid #2a527b; padding:5px 3px; text-align:center; white-space:nowrap; font-weight:800; }}
.custom-table td {{ border:1px solid #20364e; padding:4px 3px; text-align:center; white-space:nowrap; font-weight:700; }}
.footer-line {{ margin-top:6px; text-align:center; color:#ffd451; font-size:10px; font-weight:700; }}
</style></head><body>
<div class="screen-box"><div class="screener-title">{title}</div><div class="screener-sub">{sub}</div><div class="table-wrap"><table class="custom-table">
<thead><tr>
<th>RANK</th><th>EMITEN</th><th>AI SCORE</th><th>TOTAL</th><th>GAIN</th><th>WICK</th><th>AKSI</th><th>SINYAL</th><th>RVOL</th><th>ENTRY ZONE</th><th>ENTRY STATUS</th><th>NOW</th><th>TP1/2/3</th><th>SL</th><th>PROFIT</th><th>%TO TP</th><th>RSI SIG</th><th>RSI</th><th>VAL</th><th>FASE</th><th>TREND</th><th>SOURCE</th>
</tr></thead><tbody>
"""
    for i, (_, row) in enumerate(df.iterrows(), start=1):
        html += f"""
<tr>
<td style="background:#0f172a;color:#fff;">{i}</td>
<td style="background:#1d4ed8;color:#fff;">{row['symbol']}</td>
<td style="background:{bg_accum_score(row['score_accum'])};color:#fff;">{int(row['score_accum'])}</td>
<td style="background:#0b3b66;color:#fff;">{int(row['score_total'])}</td>
<td style="background:{bg_gain(row['gain'])};color:#fff;">{fmt_pct(row['gain'])}</td>
<td style="background:{bg_wick(row['wick'])};color:#fff;">{fmt_pct(row['wick'])}</td>
<td style="background:{bg_aksi(row['aksi'])};color:#fff;">{row['aksi']}</td>
<td style="background:{bg_sinyal(row['sinyal'])};color:#fff;">{row['sinyal']}</td>
<td style="background:{bg_rvol(row['rvol'])};color:#fff;">{fmt_pct(row['rvol'])}</td>
<td style="background:#1d4ed8;color:#fff;">{row['entry_zone']}</td>
<td style="background:{bg_entry_status(row['entry_status'])};color:#fff;">{row['entry_status']}</td>
<td style="background:{bg_price('now')};color:#fff;">{fmt_price(row['now'])}</td>
<td style="background:{bg_price('tp')};color:#fff;">{row['tp_zone']}</td>
<td style="background:{bg_price('sl')};color:#fff;">{fmt_price(row['sl'])}</td>
<td style="background:{bg_profit(row['profit'])};color:#fff;">{fmt_pct(row['profit'])}</td>
<td style="background:{bg_to_tp(row['to_tp'])};color:#fff;">{fmt_pct(row['to_tp'])}</td>
<td style="background:{bg_rsi_sig(row['rsi_sig'])};color:#fff;">{row['rsi_sig']}</td>
<td style="background:{bg_rsi(row['rsi'])};color:#fff;">{rsi_cell_text(row['rsi'])}</td>
<td style="background:#183b69;color:#fff;">{human_value(row['val'])}</td>
<td style="background:{bg_fase(row['fase'])};color:#fff;">{row['fase']}</td>
<td style="background:{bg_trend(row['trend'])};color:#fff;">{row['trend']}</td>
<td style="background:#0f172a;color:#cbd5e1;">{str(row.get('source',''))[:28]}</td>
</tr>
"""
    html += f"""
</tbody></table></div>
<div class="footer-line">Last scan: {fmt_time()} | API realtime/data server mode | Telegram per saham anti limit 4096 char</div>
</div></body></html>
"""
    return html

# =========================================================
# UI
# =========================================================
st.title(APP_TITLE)
st.markdown('<div class="small-note">Sumber utama DataSectors/API. yfinance hanya fallback jika diaktifkan. Zona entry + Top Signal + Telegram realtime.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("1) Data Server/API")
    source = st.selectbox("Sumber data", ["DataSectors/API", "yfinance fallback"], index=0)
    base_url = st.text_input("Base URL API", value=get_secret("DATASECTORS_BASE_URL", DEFAULT_BASE_URL))
    api_key = st.text_input("API Key", value=get_secret("DATASECTORS_API_KEY", ""), type="password")
    custom_ohlcv_endpoint = st.text_input("Custom OHLC endpoint (opsional)", value=get_secret("DATASECTORS_OHLC_ENDPOINT", ""), placeholder="contoh: stock/ohlcv")
    custom_symbol_endpoint = st.text_input("Custom Symbol List endpoint (opsional)", value=get_secret("DATASECTORS_SYMBOL_ENDPOINT", ""), placeholder="contoh: stock/list")
    fallback_yf = st.checkbox("Fallback ke yfinance jika API kosong", value=True)

    st.header("2) Watchlist")
    use_api_symbols = st.checkbox("Ambil daftar emiten dari API jika tersedia", value=False)
    preset = st.selectbox("Preset", list(WATCHLISTS.keys()), index=1)
    default_symbols = ",".join(WATCHLISTS[preset]) if preset != "Custom" else ""
    custom_symbols_text = st.text_area("Kode saham, pisahkan koma", value=default_symbols, height=130)
    extra_symbol = st.text_input("Tambah 1 emiten", placeholder="Contoh: BSJP")
    max_symbols = st.number_input("Maksimal emiten discan", min_value=1, max_value=1000, value=100, step=10)

    st.header("3) Scan & Filter")
    period = st.selectbox("Periode candle", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)
    interval = st.selectbox("Interval candle", ["1d", "1wk"], index=0)
    max_price = st.number_input("Harga maksimal", min_value=1.0, value=1000.0, step=10.0)
    top_display = st.number_input("Tampilkan Top N", min_value=1, max_value=100, value=30, step=1)
    min_score = st.slider("Minimal AI Score", 0, 100, 40)
    min_rvol = st.slider("Minimal RVOL %", 0, 500, 0)
    min_value = st.number_input("Minimal Value", min_value=0.0, value=0.0, step=1_000_000.0)
    allowed_signals = st.multiselect("Filter Sinyal", ["SUPER", "ON TRACK", "AKUM", "HAKA", "GC NOW", "REBOUND", "WAIT", "DIST", "WASPADA OB"], default=[])
    allowed_trends = st.multiselect("Filter Trend", ["BULL", "BEAR", "NEUTRAL"], default=[])
    allowed_phases = st.multiselect("Filter Fase", ["BIG AKUM", "AKUM", "NEUTRAL", "DIST", "BIG DIST"], default=[])
    entry_statuses = st.multiselect("Filter Entry Status", ["IN ZONE", "BREAKOUT ZONE", "ABOVE ZONE", "BELOW ZONE"], default=[])

    st.header("4) Telegram")
    telegram_enabled = st.checkbox("Aktifkan Telegram", value=False)
    telegram_bot_token = st.text_input("Bot Token", value=get_secret("TELEGRAM_BOT_TOKEN", ""), type="password")
    telegram_chat_id = st.text_input("Chat ID", value=get_secret("TELEGRAM_CHAT_ID", ""))
    telegram_top_n = st.number_input("Kirim Top N", min_value=1, max_value=20, value=5, step=1)
    alert_min_score = st.slider("Minimal Score Telegram", 0, 100, 55)
    alert_min_rvol = st.slider("Minimal RVOL Telegram", 0, 500, 100)
    telegram_only_strong = st.checkbox("Telegram hanya sinyal kuat", value=True)

    st.header("5) Realtime")
    auto_refresh = st.checkbox("Auto refresh", value=False)
    refresh_sec = st.selectbox("Refresh setiap", [15, 30, 60, 120, 300], index=2)
    run_btn = st.button("🚀 Jalankan Screener", use_container_width=True)
    clear_btn = st.button("🧹 Clear Cache", use_container_width=True)

if clear_btn:
    st.cache_data.clear()
    st.session_state.clear()
    st.success("Cache dibersihkan. Jalankan ulang screener.")

# Build symbols
symbols: List[str] = []
if use_api_symbols and source == "DataSectors/API":
    api_symbols, sym_used = get_symbol_list_datasectors(base_url, api_key, custom_symbol_endpoint)
    if api_symbols:
        symbols = api_symbols
        st.sidebar.success(f"Symbol API OK: {len(symbols)} emiten ({sym_used})")
    else:
        st.sidebar.warning(f"Symbol API gagal/kosong, pakai preset. {sym_used}")

if not symbols:
    symbols = [normalize_symbol(x) for x in custom_symbols_text.split(",") if normalize_symbol(x)]
if extra_symbol:
    symbols.append(normalize_symbol(extra_symbol))
symbols = list(dict.fromkeys([s for s in symbols if s]))

if not symbols:
    st.warning("Masukkan minimal 1 emiten atau pilih preset watchlist.")
    st.stop()

# Run screener on button or first load
if run_btn or "raw_screener_df" not in st.session_state:
    with st.spinner("Mengambil data API dan menghitung screener..."):
        df_raw, logs = run_screener(symbols, source, base_url, api_key, period, interval, custom_ohlcv_endpoint, fallback_yf, max_price, int(max_symbols))
        st.session_state["raw_screener_df"] = df_raw
        st.session_state["scan_logs"] = logs[-50:]
        st.session_state["last_run"] = fmt_time()

raw_df = st.session_state.get("raw_screener_df", pd.DataFrame())
if raw_df.empty:
    st.error("Tidak ada data yang berhasil discan. Cek API Key, endpoint OHLC, atau aktifkan fallback yfinance.")
    logs = st.session_state.get("scan_logs", [])
    if logs:
        with st.expander("Log error terakhir"):
            st.write("\n".join(logs[-50:]))
    st.stop()

display_df = apply_filters(raw_df, int(min_score), float(min_rvol), float(min_value), allowed_signals, allowed_trends, allowed_phases, entry_statuses).head(int(top_display)).reset_index(drop=True)
if display_df.empty:
    st.warning("Data ada, tapi tidak lolos filter. Turunkan minimal score/RVOL/value atau kosongkan filter sinyal.")
    st.stop()

alert_df = build_alert_df(display_df, int(alert_min_score), float(alert_min_rvol), int(telegram_top_n), telegram_only_strong)

# Auto Telegram anti-spam
if telegram_enabled and auto_refresh and telegram_bot_token and telegram_chat_id and not alert_df.empty:
    key = "|".join([f"{r['symbol']}-{int(r['score_accum'])}-{r['sinyal']}-{r['entry_status']}" for _, r in alert_df.iterrows()])
    if key != st.session_state.get("last_alert_key", ""):
        success, msg = send_rows_to_telegram(alert_df, telegram_bot_token, telegram_chat_id)
        if success > 0:
            st.session_state["last_alert_key"] = key
            st.success(f"Auto Telegram terkirim: {success} saham")
        else:
            st.warning(f"Gagal auto Telegram: {msg}")

# Metrics
c1, c2, c3, c4, c5, c6 = st.columns(6)
top = display_df.iloc[0]
c1.metric("TOP PICK", top["symbol"])
c2.metric("AI SCORE", int(top["score_accum"]))
c3.metric("SIGNAL", top["sinyal"])
c4.metric("ENTRY", top["entry_zone"])
c5.metric("LAST SCAN", st.session_state.get("last_run", "-"))
c6.metric("DATA", str(top.get("source", ""))[:18])

b1, b2, b3 = st.columns([1, 1, 2])
with b1:
    send_now = st.button("📩 Kirim Top Signal Telegram", use_container_width=True)
with b2:
    st.metric("Alert Top Signal", len(alert_df))
with b3:
    st.caption("Telegram dikirim per saham supaya tidak terkena limit pesan 4096 karakter.")

if telegram_enabled and send_now:
    if alert_df.empty:
        st.warning("Belum ada top signal yang lolos filter Telegram.")
    else:
        success, msg = send_rows_to_telegram(alert_df, telegram_bot_token, telegram_chat_id)
        if success > 0:
            st.success(f"Telegram terkirim: {success} saham")
        else:
            st.error(f"Gagal kirim Telegram: {msg}")

# Table
st.subheader("Top Screener")
components.html(
    make_html_table(display_df, APP_TITLE, "Ranking: AI Score + Total Score + RVOL + Gain + Entry Zone"),
    height=560,
    scrolling=True,
)

# Dataframe ranking
st.subheader("Ranking Data")
rank_cols = ["symbol", "now", "gain", "rvol", "entry_zone", "entry_status", "tp_zone", "sl", "rsi", "val", "fase", "trend", "sinyal", "score_accum", "score_scalping", "score_bsjp", "score_swing", "score_bandar", "score_total", "source"]
rank_df = display_df[[c for c in rank_cols if c in display_df.columns]].copy()
st.dataframe(rank_df, use_container_width=True, height=420)

# Detail panel
st.subheader("Detail Emiten")
selected = st.selectbox("Pilih emiten", display_df["symbol"].tolist())
selected_row = display_df[display_df["symbol"] == selected].iloc[0]
sel_df = selected_row["daily_df"]

d1, d2, d3, d4, d5, d6 = st.columns(6)
d1.metric("EMITEN", selected_row["symbol"])
d2.metric("NOW", fmt_price(selected_row["now"]))
d3.metric("GAIN", fmt_pct(selected_row["gain"]))
d4.metric("RVOL", fmt_pct(selected_row["rvol"]))
d5.metric("ENTRY ZONE", selected_row["entry_zone"])
d6.metric("AI SCORE", int(selected_row["score_accum"]))

fig = go.Figure()
fig.add_trace(go.Candlestick(x=sel_df.index, open=sel_df["Open"], high=sel_df["High"], low=sel_df["Low"], close=sel_df["Close"], name="Candlestick"))
for ma in ["MA20", "MA50"]:
    if ma in sel_df.columns:
        fig.add_trace(go.Scatter(x=sel_df.index, y=sel_df[ma], mode="lines", name=ma))
fig.add_hline(y=safe_float(selected_row["entry_low"]), line_dash="dash", annotation_text="Entry Low")
fig.add_hline(y=safe_float(selected_row["entry_high"]), line_dash="dash", annotation_text="Entry High")
fig.add_hline(y=safe_float(selected_row["sl"]), line_dash="dash", annotation_text="SL")
fig.add_hline(y=safe_float(selected_row["tp2"]), line_dash="dash", annotation_text="TP2")
fig.update_layout(height=520, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

with st.expander("Log scan terakhir"):
    logs = st.session_state.get("scan_logs", [])
    if logs:
        st.text("\n".join(logs[-50:]))
    else:
        st.write("Tidak ada error log.")

st.caption("Catatan: Sinyal ini alat bantu screening, bukan rekomendasi pasti. Tetap gunakan risk management.")

if auto_refresh:
    auto_refresh_fragment(int(refresh_sec))

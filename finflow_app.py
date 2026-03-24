import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, date
import json
import requests

st.set_page_config(
    page_title="FinFlow AI — Intelligent Financial Analysis",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='12' fill='%230f172a'/><text y='.9em' font-size='70' x='15'>F</text></svg>",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*,html,body{font-family:'Inter',sans-serif!important}
.stApp{background:#f8fafc!important}

section[data-testid="stSidebar"]{background:#0f172a!important;border-right:none!important}
section[data-testid="stSidebar"] *{color:#e2e8f0!important}
section[data-testid="stSidebar"] input{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(255,255,255,0.12)!important;color:#fff!important;border-radius:6px!important;font-size:13px!important}
section[data-testid="stSidebar"] [data-testid="stSelectbox"]>div>div{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(255,255,255,0.12)!important;color:#fff!important;border-radius:6px!important}
section[data-testid="stSidebar"] .stRadio label{font-size:13px!important;padding:9px 12px!important;border-radius:6px!important;display:block!important;color:#94a3b8!important;font-weight:500!important}
section[data-testid="stSidebar"] .stRadio label:hover{background:rgba(255,255,255,0.07)!important;color:#fff!important}

main .block-container{padding:1.5rem 2rem!important;max-width:100%!important}

.page-header{background:#0f172a;padding:22px 28px;border-radius:10px;margin-bottom:20px;border-left:4px solid #3b82f6}
.page-header h1{color:#fff!important;font-size:20px!important;font-weight:700!important;margin:0 0 4px!important;letter-spacing:-0.3px!important}
.page-header p{color:#64748b!important;font-size:12px!important;margin:0!important;letter-spacing:0.3px!important}

.card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:24px;margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,0.05)}
.card-title{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid #f1f5f9}

.metric-card{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,0.04)}
.metric-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;color:#64748b;margin:0 0 6px}
.metric-value{font-size:26px;font-weight:700;color:#0f172a;margin:0;line-height:1}
.metric-delta-pos{font-size:12px;color:#16a34a;margin:4px 0 0;font-weight:500}
.metric-delta-neg{font-size:12px;color:#dc2626;margin:4px 0 0;font-weight:500}
.metric-delta-neu{font-size:12px;color:#64748b;margin:4px 0 0;font-weight:500}

.insight-card{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:16px;margin-bottom:10px}
.insight-positive{border-left:3px solid #16a34a;background:#f0fdf4}
.insight-negative{border-left:3px solid #dc2626;background:#fef2f2}
.insight-warning{border-left:3px solid #d97706;background:#fffbeb}
.insight-info{border-left:3px solid #2563eb;background:#eff6ff}

.chat-user{background:#0f172a;color:#fff;border-radius:12px 12px 2px 12px;padding:12px 16px;margin:8px 0;font-size:14px;max-width:80%;margin-left:auto}
.chat-ai{background:#fff;border:1px solid #e2e8f0;border-radius:12px 12px 12px 2px;padding:12px 16px;margin:8px 0;font-size:14px;max-width:85%;line-height:1.7}
.chat-ai-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#2563eb;margin-bottom:6px}
.chat-user-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin-bottom:6px;text-align:right}

.badge-green{background:#dcfce7;color:#166534;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600;border:1px solid #bbf7d0}
.badge-red{background:#fee2e2;color:#991b1b;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600;border:1px solid #fecaca}
.badge-yellow{background:#fef3c7;color:#92400e;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600;border:1px solid #fde68a}
.badge-blue{background:#dbeafe;color:#1e40af;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600;border:1px solid #bfdbfe}

[data-testid="metric-container"]{background:#fff!important;border:1px solid #e2e8f0!important;border-radius:8px!important;padding:16px 20px!important;box-shadow:0 1px 3px rgba(0,0,0,0.04)!important}
[data-testid="metric-container"] label{color:#64748b!important;font-size:11px!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:0.8px!important}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#0f172a!important;font-size:24px!important;font-weight:700!important}

.stButton>button{background:#0f172a!important;color:#fff!important;font-weight:600!important;border:none!important;border-radius:6px!important;padding:10px 20px!important;font-size:13px!important;letter-spacing:0.3px!important}
.stButton>button:hover{background:#1e3a5f!important;box-shadow:0 4px 12px rgba(15,23,42,0.2)!important}

.stTabs [data-baseweb="tab-list"]{background:#f1f5f9!important;border-radius:6px!important;padding:3px!important;border:1px solid #e2e8f0!important}
.stTabs [data-baseweb="tab"]{color:#64748b!important;border-radius:4px!important;font-size:12px!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:0.5px!important;padding:8px 16px!important}
.stTabs [aria-selected="true"]{background:#fff!important;color:#0f172a!important;box-shadow:0 1px 3px rgba(0,0,0,0.1)!important}

.stTextInput input,.stNumberInput input,textarea{background:#fff!important;border:1px solid #d1d5db!important;color:#1e293b!important;border-radius:6px!important;font-size:13px!important}
.stTextInput input:focus{border-color:#2563eb!important;box-shadow:0 0 0 3px rgba(37,99,235,0.08)!important}
[data-testid="stSelectbox"]>div>div{background:#fff!important;border:1px solid #d1d5db!important;border-radius:6px!important;font-size:13px!important}
[data-testid="stFileUploader"]{background:#f8fafc!important;border:1.5px dashed #cbd5e1!important;border-radius:8px!important}
hr{border:none!important;border-top:1px solid #e2e8f0!important;margin:16px 0!important}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:#f1f5f9}
::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:99px}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 16px 16px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:16px;'>
        <div style='display:flex;align-items:center;gap:12px;'>
            <div style='width:36px;height:36px;background:#2563eb;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;'>
                <svg width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'>
                    <polyline points='22 7 13.5 15.5 8.5 10.5 2 17'/>
                    <polyline points='16 7 22 7 22 13'/>
                </svg>
            </div>
            <div>
                <div style='color:#fff;font-size:16px;font-weight:800;letter-spacing:-0.3px;'>FinFlow AI</div>
                <div style='color:#475569;font-size:11px;letter-spacing:0.3px;margin-top:1px;'>FINANCIAL INTELLIGENCE</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size:10px;font-weight:700;color:#334155;text-transform:uppercase;letter-spacing:1.2px;padding:0 4px;margin-bottom:6px;'>Navigation</p>", unsafe_allow_html=True)
    page = st.radio("", [
        "Dashboard",
        "P&L Analyzer",
        "Balance Sheet Analyzer",
        "Bank Statement Analyzer",
        "Ratio Analysis",
        "Cash Flow Insights",
        "AI CFO Chat",
        "Executive Report"
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:10px;font-weight:700;color:#334155;text-transform:uppercase;letter-spacing:1.2px;padding:0 4px;margin-bottom:8px;'>Company Profile</p>", unsafe_allow_html=True)
    company = st.text_input("", "My Company Pvt Ltd", placeholder="Company Name", label_visibility="collapsed")
    industry = st.selectbox("", ["Manufacturing","Trading","Services","Retail","FMCG","Technology","Healthcare","Construction","Finance","Hospitality"], label_visibility="collapsed")
    fy = st.selectbox("", ["FY 2024-25","FY 2023-24","FY 2022-23","FY 2021-22"], label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0;'>", unsafe_allow_html=True)
    openai_key = st.text_input("OpenAI API Key (for AI Chat)", "", type="password", placeholder="sk-...")
    st.markdown("<p style='font-size:11px;color:#334155;padding:0 4px;'>v1.0 | Built by Sanskar Gupta<br><span style='color:#2563eb;'>guptasanskar824@gmail.com</span></p>", unsafe_allow_html=True)

# ── HELPERS ──────────────────────────────────────────────────
def to_excel(df):
    out = BytesIO()
    df.to_excel(out, index=False)
    return out.getvalue()

def header(title, sub):
    st.markdown(f"<div class='page-header'><h1>{title}</h1><p>{sub}</p></div>", unsafe_allow_html=True)

def fmt_inr(val):
    if abs(val) >= 10000000: return f"Rs {val/10000000:.2f} Cr"
    elif abs(val) >= 100000: return f"Rs {val/100000:.2f} L"
    else: return f"Rs {val:,.0f}"

def insight(text, kind="info"):
    icons = {"positive":"↑","negative":"↓","warning":"!","info":"i"}
    colors = {"positive":"#166534","negative":"#991b1b","warning":"#92400e","info":"#1e40af"}
    bgs = {"positive":"#f0fdf4","negative":"#fef2f2","warning":"#fffbeb","info":"#eff6ff"}
    borders = {"positive":"#16a34a","negative":"#dc2626","warning":"#d97706","info":"#2563eb"}
    st.markdown(f"""
    <div style='background:{bgs[kind]};border-left:3px solid {borders[kind]};border-radius:6px;padding:12px 16px;margin-bottom:8px;'>
        <p style='color:{colors[kind]};font-size:13px;margin:0;line-height:1.6;'><strong>{icons[kind]}</strong> {text}</p>
    </div>""", unsafe_allow_html=True)

def get_sample_pl():
    return pd.DataFrame({
        "Particulars": ["Revenue from Operations","Other Income","Total Revenue","Cost of Goods Sold","Gross Profit","Employee Expenses","Rent & Utilities","Marketing Expenses","Administrative Expenses","Depreciation","Total Operating Expenses","EBITDA","EBIT","Interest Expense","PBT","Tax (30%)","PAT"],
        "Current Year (Rs)": [12500000,350000,12850000,7500000,5350000,1800000,480000,620000,380000,250000,3530000,1820000,1570000,320000,1250000,375000,875000],
        "Previous Year (Rs)": [10200000,280000,10480000,6300000,4180000,1550000,420000,480000,320000,210000,2980000,1200000,990000,290000,700000,210000,490000]
    })

def get_sample_bs():
    return pd.DataFrame({
        "Particulars": ["EQUITY & LIABILITIES","Share Capital","Reserves & Surplus","Total Equity","Long Term Borrowings","Deferred Tax Liabilities","Total Non-Current Liabilities","Short Term Borrowings","Trade Payables","Other Current Liabilities","Total Current Liabilities","TOTAL LIABILITIES","ASSETS","Fixed Assets (Net)","Capital Work in Progress","Total Non-Current Assets","Inventories","Trade Receivables","Cash & Bank Balances","Other Current Assets","Total Current Assets","TOTAL ASSETS"],
        "Current Year (Rs)": [0,2000000,4875000,6875000,3200000,180000,3380000,1500000,2100000,895000,4495000,14750000,0,5200000,450000,5650000,3800000,3200000,1100000,0,8100000,14750000],
        "Previous Year (Rs)": [0,2000000,4000000,6000000,3500000,150000,3650000,1800000,1900000,750000,4450000,14100000,0,5100000,600000,5700000,3200000,2800000,850000,0,6850000,12550000]
    })

def get_sample_bank():
    import random
    random.seed(42)
    dates = pd.date_range("2025-04-01","2025-03-31",freq="W")[:52]
    cats = ["Sales Receipt","Vendor Payment","Salary","Rent","Utilities","Tax Payment","Loan EMI","Miscellaneous Income","Office Expenses","Marketing"]
    rows = []
    bal = 500000
    for d in dates:
        for _ in range(random.randint(2,5)):
            cat = random.choice(cats)
            if cat in ["Sales Receipt","Miscellaneous Income"]:
                amt = random.randint(50000,500000)
                typ = "Credit"
                bal += amt
            else:
                amt = random.randint(10000,200000)
                typ = "Debit"
                bal -= amt
            rows.append({"Date":d.strftime("%Y-%m-%d"),"Description":cat,"Type":typ,"Amount":amt,"Balance":max(bal,0),"Category":cat})
    return pd.DataFrame(rows[:100])

def analyze_pl(df):
    try:
        def get_val(label, col):
            row = df[df.iloc[:,0].str.contains(label, case=False, na=False)]
            if len(row): return float(row.iloc[0,col])
            return 0
        rev_cy = get_val("Total Revenue|Revenue from Operations", 1)
        rev_py = get_val("Total Revenue|Revenue from Operations", 2) if df.shape[1] > 2 else 0
        pat_cy = get_val("PAT|Net Profit|Profit After Tax", 1)
        pat_py = get_val("PAT|Net Profit|Profit After Tax", 2) if df.shape[1] > 2 else 0
        cogs_cy = get_val("Cost of Goods|COGS|Cost of Sales", 1)
        ebitda_cy = get_val("EBITDA", 1)
        interest_cy = get_val("Interest", 1)
        tax_cy = get_val("Tax", 1)

        gross_profit = rev_cy - cogs_cy
        gpm = (gross_profit/rev_cy*100) if rev_cy else 0
        npm = (pat_cy/rev_cy*100) if rev_cy else 0
        ebitda_margin = (ebitda_cy/rev_cy*100) if rev_cy else 0
        rev_growth = ((rev_cy-rev_py)/rev_py*100) if rev_py else 0
        pat_growth = ((pat_cy-pat_py)/pat_py*100) if rev_py else 0

        return {
            "revenue": rev_cy, "revenue_py": rev_py, "pat": pat_cy, "pat_py": pat_py,
            "gross_profit": gross_profit, "gpm": gpm, "npm": npm,
            "ebitda": ebitda_cy, "ebitda_margin": ebitda_margin,
            "interest": interest_cy, "tax": tax_cy,
            "rev_growth": rev_growth, "pat_growth": pat_growth
        }
    except: return {}

def analyze_bs(df):
    try:
        def get_val(label, col):
            row = df[df.iloc[:,0].str.contains(label, case=False, na=False)]
            if len(row): return float(row.iloc[0,col])
            return 0
        ca = get_val("Total Current Assets|Current Assets", 1)
        cl = get_val("Total Current Liabilities|Current Liabilities", 1)
        inv = get_val("Inventories|Inventory", 1)
        rec = get_val("Trade Receivables|Debtors", 1)
        cash = get_val("Cash", 1)
        ltb = get_val("Long Term Borrowings", 1)
        equity = get_val("Total Equity|Shareholders", 1)
        total = get_val("TOTAL ASSETS|Total Assets", 1)
        stb = get_val("Short Term Borrowings", 1)
        fa = get_val("Fixed Assets", 1)

        current_ratio = ca/cl if cl else 0
        quick_ratio = (ca-inv)/cl if cl else 0
        debt = ltb + stb
        de_ratio = debt/equity if equity else 0
        return {
            "current_assets": ca, "current_liabilities": cl, "inventory": inv,
            "receivables": rec, "cash": cash, "lt_borrowings": ltb,
            "equity": equity, "total_assets": total, "debt": debt,
            "current_ratio": current_ratio, "quick_ratio": quick_ratio,
            "de_ratio": de_ratio, "fa": fa
        }
    except: return {}

def call_ai(messages, api_key):
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-opus-4-6", "max_tokens": 1000, "messages": messages},
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()["content"][0]["text"]
        return f"API Error: {resp.status_code}"
    except Exception as e:
        return f"Connection error: {str(e)}"

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "Dashboard":
    header("Financial Intelligence Dashboard", f"{company}  |  Industry: {industry}  |  {fy}  |  {date.today().strftime('%d %B %Y')}")

    st.markdown("""
    <div style='background:#0f172a;border-radius:10px;padding:20px 24px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;'>
        <div>
            <p style='color:#fff;font-size:16px;font-weight:700;margin:0;'>Welcome to FinFlow AI</p>
            <p style='color:#475569;font-size:13px;margin:6px 0 0;'>Upload your financial statements to get instant AI-powered analysis, insights, and CFO-level recommendations.</p>
        </div>
        <div style='display:flex;gap:12px;flex-wrap:wrap;'>
            <div style='background:rgba(37,99,235,0.15);border:1px solid rgba(37,99,235,0.3);border-radius:8px;padding:10px 16px;text-align:center;'>
                <p style='color:#93c5fd;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin:0;'>Statements</p>
                <p style='color:#fff;font-size:20px;font-weight:700;margin:4px 0 0;'>3</p>
            </div>
            <div style='background:rgba(22,163,74,0.15);border:1px solid rgba(22,163,74,0.3);border-radius:8px;padding:10px 16px;text-align:center;'>
                <p style='color:#86efac;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin:0;'>AI Powered</p>
                <p style='color:#fff;font-size:20px;font-weight:700;margin:4px 0 0;'>Yes</p>
            </div>
            <div style='background:rgba(217,119,6,0.15);border:1px solid rgba(217,119,6,0.3);border-radius:8px;padding:10px 16px;text-align:center;'>
                <p style='color:#fcd34d;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin:0;'>Ratios</p>
                <p style='color:#fff;font-size:20px;font-weight:700;margin:4px 0 0;'>15+</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-title'>P&L Statement</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748b;font-size:13px;'>Upload your Profit & Loss statement to analyze revenue, expenses, margins and profitability trends.</p>", unsafe_allow_html=True)
        pl_file = st.file_uploader("Upload P&L", type=["xlsx","csv"], key="pl_dash", label_visibility="collapsed")
        st.download_button("Download Sample P&L", to_excel(get_sample_pl()), "Sample_PL.xlsx", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-title'>Balance Sheet</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748b;font-size:13px;'>Upload your Balance Sheet to analyze assets, liabilities, liquidity ratios and financial position.</p>", unsafe_allow_html=True)
        bs_file = st.file_uploader("Upload BS", type=["xlsx","csv"], key="bs_dash", label_visibility="collapsed")
        st.download_button("Download Sample BS", to_excel(get_sample_bs()), "Sample_BS.xlsx", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-title'>Bank Statement</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748b;font-size:13px;'>Upload your bank statement to analyze cash flow patterns, spending categories and liquidity.</p>", unsafe_allow_html=True)
        bank_file = st.file_uploader("Upload Bank", type=["xlsx","csv"], key="bank_dash", label_visibility="collapsed")
        st.download_button("Download Sample Bank Statement", to_excel(get_sample_bank()), "Sample_Bank.xlsx", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if pl_file:
        df = pd.read_excel(pl_file) if pl_file.name.endswith("xlsx") else pd.read_csv(pl_file)
        metrics = analyze_pl(df)
        if metrics:
            st.markdown("#### P&L Summary")
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Total Revenue", fmt_inr(metrics.get("revenue",0)), f"{metrics.get('rev_growth',0):+.1f}% YoY")
            c2.metric("Net Profit (PAT)", fmt_inr(metrics.get("pat",0)), f"{metrics.get('pat_growth',0):+.1f}% YoY")
            c3.metric("Gross Profit Margin", f"{metrics.get('gpm',0):.1f}%")
            c4.metric("Net Profit Margin", f"{metrics.get('npm',0):.1f}%")

    st.markdown("#### Platform Capabilities")
    caps = [
        ("P&L Analyzer","Revenue trend, margin analysis, expense breakdown, YoY comparison, profitability insights"),
        ("Balance Sheet Analyzer","Asset quality, liability structure, working capital, liquidity assessment"),
        ("Bank Statement Analyzer","Cash flow patterns, category-wise spending, unusual transactions, liquidity tracking"),
        ("Ratio Analysis","15+ financial ratios — liquidity, profitability, leverage, efficiency, all benchmarked"),
        ("Cash Flow Insights","Operating, investing, financing cash flows with burn rate and runway analysis"),
        ("AI CFO Chat","Ask any question about your financials in plain English and get expert answers"),
        ("Executive Report","One-click professional PDF-ready report for board presentations and investor meetings"),
    ]
    c1,c2 = st.columns(2)
    for i,(t,d) in enumerate(caps):
        with [c1,c2][i%2]:
            st.markdown(f"""
            <div style='background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:16px;margin-bottom:12px;border-left:3px solid #0f172a;'>
                <p style='font-weight:700;color:#0f172a;font-size:13px;margin:0 0 4px;'>{t}</p>
                <p style='color:#64748b;font-size:12px;margin:0;line-height:1.5;'>{d}</p>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# P&L ANALYZER
# ══════════════════════════════════════════════════════════════
elif page == "P&L Analyzer":
    header("P&L Statement Analyzer", "Revenue, profitability, margins and year-on-year performance analysis")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-title'>Upload P&L Statement</p>", unsafe_allow_html=True)
    pl_file = st.file_uploader("Upload Excel or CSV", type=["xlsx","csv"], label_visibility="collapsed")
    st.download_button("Download Sample P&L", to_excel(get_sample_pl()), "Sample_PL.xlsx")
    st.markdown("</div>", unsafe_allow_html=True)

    df = pd.read_excel(pl_file) if pl_file and pl_file.name.endswith("xlsx") else (pd.read_csv(pl_file) if pl_file else get_sample_pl())
    if not pl_file:
        st.info("Showing sample data. Upload your P&L to see actual analysis.")

    metrics = analyze_pl(df)
    if metrics:
        st.markdown("#### Key Performance Indicators")
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total Revenue", fmt_inr(metrics["revenue"]), f"{metrics['rev_growth']:+.1f}% YoY")
        c2.metric("EBITDA", fmt_inr(metrics["ebitda"]), f"{metrics['ebitda_margin']:.1f}% margin")
        c3.metric("Net Profit", fmt_inr(metrics["pat"]), f"{metrics['pat_growth']:+.1f}% YoY")
        c4.metric("Gross Margin", f"{metrics['gpm']:.1f}%")
        c5.metric("Net Margin", f"{metrics['npm']:.1f}%")

        tab1, tab2, tab3 = st.tabs(["  Revenue & Profit  ","  Margin Analysis  ","  Expense Breakdown  "])
        with tab1:
            if df.shape[1] > 2:
                items = ["Revenue from Operations","Gross Profit","EBITDA","PAT"]
                plot_df = df[df.iloc[:,0].isin(items)][df.columns[:3]].copy()
                plot_df.columns = ["Item","Current Year","Previous Year"]
                plot_df = plot_df[plot_df["Item"].isin(items)]
                if not plot_df.empty:
                    fig = px.bar(plot_df.melt(id_vars="Item",var_name="Year",value_name="Amount"),
                        x="Item",y="Amount",color="Year",barmode="group",
                        title="Revenue & Profit — Year on Year Comparison",
                        color_discrete_map={"Current Year":"#0f172a","Previous Year":"#94a3b8"})
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#f8fafc",font=dict(family="Inter"),font_color="#1e293b")
                    st.plotly_chart(fig, use_container_width=True)

        with tab2:
            margins = {"Gross Profit Margin":metrics["gpm"],"EBITDA Margin":metrics["ebitda_margin"],"Net Profit Margin":metrics["npm"]}
            fig2 = go.Figure()
            for name, val in margins.items():
                color = "#16a34a" if val > 20 else "#d97706" if val > 10 else "#dc2626"
                fig2.add_trace(go.Bar(name=name, x=[name], y=[val], marker_color=color))
            fig2.update_layout(title="Margin Analysis (%)",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#f8fafc",font=dict(family="Inter"),font_color="#1e293b",showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            exp_items = df[df.iloc[:,0].str.contains("Expenses|Expense|Cost|Depreciation|Interest", case=False, na=False)]
            if not exp_items.empty:
                fig3 = px.pie(exp_items, values=df.columns[1], names=df.columns[0],
                    title="Expense Breakdown", hole=0.5,
                    color_discrete_sequence=["#0f172a","#1e3a5f","#2563eb","#3b82f6","#60a5fa","#93c5fd","#bfdbfe"])
                fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(family="Inter"),font_color="#1e293b")
                st.plotly_chart(fig3, use_container_width=True)

        st.markdown("#### AI Insights")
        if metrics["rev_growth"] > 15: insight(f"Strong revenue growth of {metrics['rev_growth']:.1f}% YoY — significantly above industry average of 8-10% for {industry}", "positive")
        elif metrics["rev_growth"] > 0: insight(f"Revenue grew {metrics['rev_growth']:.1f}% YoY — moderate growth, consider strategies to accelerate", "warning")
        else: insight(f"Revenue declined {metrics['rev_growth']:.1f}% YoY — immediate attention required on sales strategy", "negative")

        if metrics["npm"] > 15: insight(f"Excellent net profit margin of {metrics['npm']:.1f}% — well above {industry} sector benchmark of 8-12%", "positive")
        elif metrics["npm"] > 8: insight(f"Healthy net profit margin of {metrics['npm']:.1f}% — within acceptable range for {industry}", "info")
        elif metrics["npm"] > 0: insight(f"Low net profit margin of {metrics['npm']:.1f}% — review cost structure and pricing strategy", "warning")
        else: insight(f"Negative net profit margin — business is loss-making, urgent intervention required", "negative")

        if metrics["ebitda_margin"] > 20: insight(f"Strong EBITDA margin of {metrics['ebitda_margin']:.1f}% — indicates excellent operational efficiency", "positive")
        else: insight(f"EBITDA margin of {metrics['ebitda_margin']:.1f}% — focus on operational efficiency improvements", "warning")

        if metrics["pat_growth"] > metrics["rev_growth"]: insight("Profit growing faster than revenue — improving operational leverage and cost efficiency", "positive")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-title'>Full P&L Statement</p>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("Download Analysis", to_excel(df), "PL_Analysis.xlsx", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# BALANCE SHEET ANALYZER
# ══════════════════════════════════════════════════════════════
elif page == "Balance Sheet Analyzer":
    header("Balance Sheet Analyzer", "Assets, liabilities, equity structure and financial position assessment")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    bs_file = st.file_uploader("Upload Balance Sheet (Excel/CSV)", type=["xlsx","csv"], label_visibility="collapsed")
    st.download_button("Download Sample Balance Sheet", to_excel(get_sample_bs()), "Sample_BS.xlsx")
    st.markdown("</div>", unsafe_allow_html=True)

    df = pd.read_excel(bs_file) if bs_file and bs_file.name.endswith("xlsx") else (pd.read_csv(bs_file) if bs_file else get_sample_bs())
    if not bs_file: st.info("Showing sample data. Upload your Balance Sheet for actual analysis.")

    metrics = analyze_bs(df)
    if metrics:
        st.markdown("#### Balance Sheet Highlights")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Assets", fmt_inr(metrics["total_assets"]))
        c2.metric("Total Equity", fmt_inr(metrics["equity"]))
        c3.metric("Cash & Bank", fmt_inr(metrics["cash"]))
        c4.metric("Total Debt", fmt_inr(metrics["debt"]))

        tab1,tab2,tab3 = st.tabs(["  Asset Structure  ","  Liability Structure  ","  Working Capital  "])
        with tab1:
            asset_data = {"Fixed Assets":metrics["fa"],"Inventory":metrics["inventory"],"Receivables":metrics["receivables"],"Cash":metrics["cash"]}
            asset_data = {k:v for k,v in asset_data.items() if v > 0}
            if asset_data:
                fig = px.pie(values=list(asset_data.values()),names=list(asset_data.keys()),title="Asset Composition",hole=0.5,color_discrete_sequence=["#0f172a","#2563eb","#60a5fa","#bfdbfe"])
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(family="Inter"),font_color="#1e293b")
                st.plotly_chart(fig, use_container_width=True)
        with tab2:
            lib_data = {"Equity":metrics["equity"],"Long Term Debt":metrics["lt_borrowings"],"Current Liabilities":metrics["current_liabilities"]}
            lib_data = {k:v for k,v in lib_data.items() if v > 0}
            if lib_data:
                fig2 = px.bar(x=list(lib_data.keys()),y=list(lib_data.values()),title="Funding Structure",color_discrete_sequence=["#0f172a"])
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#f8fafc",font=dict(family="Inter"),font_color="#1e293b")
                st.plotly_chart(fig2, use_container_width=True)
        with tab3:
            wc = metrics["current_assets"] - metrics["current_liabilities"]
            c1,c2,c3 = st.columns(3)
            c1.metric("Current Assets", fmt_inr(metrics["current_assets"]))
            c2.metric("Current Liabilities", fmt_inr(metrics["current_liabilities"]))
            c3.metric("Working Capital", fmt_inr(wc), "Positive" if wc > 0 else "Negative")

        st.markdown("#### Liquidity & Leverage Ratios")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Current Ratio", f"{metrics['current_ratio']:.2f}x", "Healthy" if metrics['current_ratio'] > 2 else "Low" if metrics['current_ratio'] < 1 else "Adequate")
        c2.metric("Quick Ratio", f"{metrics['quick_ratio']:.2f}x", "Healthy" if metrics['quick_ratio'] > 1 else "Low")
        c3.metric("Debt/Equity Ratio", f"{metrics['de_ratio']:.2f}x", "Low" if metrics['de_ratio'] < 0.5 else "High" if metrics['de_ratio'] > 2 else "Moderate")
        c4.metric("Cash Ratio", f"{metrics['cash']/metrics['current_liabilities']:.2f}x" if metrics['current_liabilities'] else "N/A")

        st.markdown("#### AI Insights")
        if metrics["current_ratio"] >= 2: insight(f"Current ratio of {metrics['current_ratio']:.2f}x is strong — company can comfortably meet short-term obligations", "positive")
        elif metrics["current_ratio"] >= 1: insight(f"Current ratio of {metrics['current_ratio']:.2f}x is adequate but below ideal 2x benchmark — monitor working capital closely", "warning")
        else: insight(f"Current ratio of {metrics['current_ratio']:.2f}x is critically low — immediate liquidity risk, urgent action required", "negative")

        if metrics["de_ratio"] < 0.5: insight(f"Low debt/equity ratio of {metrics['de_ratio']:.2f}x — company is conservatively financed with minimal leverage risk", "positive")
        elif metrics["de_ratio"] < 1.5: insight(f"Moderate debt/equity of {metrics['de_ratio']:.2f}x — leverage is manageable, ensure interest coverage is maintained", "info")
        else: insight(f"High debt/equity ratio of {metrics['de_ratio']:.2f}x — significant leverage risk, focus on debt reduction", "negative")

        equity_pct = metrics["equity"]/metrics["total_assets"]*100 if metrics["total_assets"] else 0
        if equity_pct > 50: insight(f"Strong equity base of {equity_pct:.0f}% of total assets — healthy ownership structure", "positive")
        else: insight(f"Equity is only {equity_pct:.0f}% of total assets — business is predominantly debt-funded", "warning")

    st.dataframe(df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# BANK STATEMENT ANALYZER
# ══════════════════════════════════════════════════════════════
elif page == "Bank Statement Analyzer":
    header("Bank Statement Analyzer", "Cash flow patterns, category analysis, unusual transactions and liquidity tracking")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    bank_file = st.file_uploader("Upload Bank Statement (Excel/CSV)", type=["xlsx","csv"], label_visibility="collapsed")
    st.download_button("Download Sample Bank Statement", to_excel(get_sample_bank()), "Sample_Bank.xlsx")
    st.markdown("</div>", unsafe_allow_html=True)

    df = pd.read_excel(bank_file) if bank_file and bank_file.name.endswith("xlsx") else (pd.read_csv(bank_file) if bank_file else get_sample_bank())
    if not bank_file: st.info("Showing sample data. Upload your bank statement for actual analysis.")

    # Detect columns
    amt_col = next((c for c in df.columns if any(x in c.lower() for x in ["amount","amt","value"])), df.columns[3] if len(df.columns)>3 else df.columns[-1])
    type_col = next((c for c in df.columns if any(x in c.lower() for x in ["type","dr/cr","debit","credit","transaction"])), None)
    cat_col = next((c for c in df.columns if "category" in c.lower() or "description" in c.lower()), df.columns[1] if len(df.columns)>1 else None)
    date_col = next((c for c in df.columns if "date" in c.lower()), df.columns[0])
    bal_col = next((c for c in df.columns if "balance" in c.lower() or "bal" in c.lower()), None)

    total_credits = df[df[type_col]=="Credit"][amt_col].sum() if type_col else df[amt_col].sum()
    total_debits = df[df[type_col]=="Debit"][amt_col].sum() if type_col else 0
    avg_bal = df[bal_col].mean() if bal_col else 0
    min_bal = df[bal_col].min() if bal_col else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Credits", fmt_inr(total_credits))
    c2.metric("Total Debits", fmt_inr(total_debits))
    c3.metric("Net Cash Flow", fmt_inr(total_credits - total_debits), "Positive" if total_credits > total_debits else "Negative")
    c4.metric("Average Balance", fmt_inr(avg_bal) if avg_bal else "N/A")

    tab1,tab2,tab3 = st.tabs(["  Cash Flow Trend  ","  Category Analysis  ","  Transaction Detail  "])
    with tab1:
        if bal_col:
            fig = px.line(df, x=date_col, y=bal_col, title="Bank Balance Trend", color_discrete_sequence=["#0f172a"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#f8fafc",font=dict(family="Inter"),font_color="#1e293b")
            fig.add_hline(y=avg_bal, line_dash="dash", line_color="#2563eb", annotation_text=f"Avg: {fmt_inr(avg_bal)}")
            st.plotly_chart(fig, use_container_width=True)
    with tab2:
        if cat_col:
            if type_col:
                deb_df = df[df[type_col]=="Debit"].groupby(cat_col)[amt_col].sum().reset_index()
            else:
                deb_df = df.groupby(cat_col)[amt_col].sum().reset_index()
            deb_df.columns = ["Category","Amount"]
            deb_df = deb_df.sort_values("Amount", ascending=False)
            fig2 = px.bar(deb_df, x="Category", y="Amount", title="Spending by Category", color_discrete_sequence=["#0f172a"])
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#f8fafc",font=dict(family="Inter"),font_color="#1e293b")
            st.plotly_chart(fig2, use_container_width=True)
    with tab3:
        st.dataframe(df.head(50), use_container_width=True, hide_index=True)
        st.download_button("Download Full Statement Analysis", to_excel(df), "Bank_Analysis.xlsx", use_container_width=True)

    st.markdown("#### AI Insights")
    if total_credits > total_debits: insight(f"Positive net cash flow of {fmt_inr(total_credits-total_debits)} — business is generating more cash than it is spending", "positive")
    else: insight(f"Negative net cash flow of {fmt_inr(abs(total_credits-total_debits))} — cash is being depleted, review spending", "negative")
    if avg_bal > 0 and min_bal < avg_bal * 0.1: insight(f"Balance dropped to {fmt_inr(min_bal)} at its lowest — consider maintaining a minimum cash buffer of {fmt_inr(avg_bal*0.3)}", "warning")

# ══════════════════════════════════════════════════════════════
# RATIO ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "Ratio Analysis":
    header("Financial Ratio Analysis", "15+ ratios across liquidity, profitability, leverage and efficiency — benchmarked against industry")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-title'>Upload Both Statements for Complete Ratio Analysis</p>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        pl_file = st.file_uploader("P&L Statement", type=["xlsx","csv"], key="pl_ratio", label_visibility="collapsed")
        st.caption("P&L Statement")
    with c2:
        bs_file = st.file_uploader("Balance Sheet", type=["xlsx","csv"], key="bs_ratio", label_visibility="collapsed")
        st.caption("Balance Sheet")
    st.markdown("</div>", unsafe_allow_html=True)

    pl_df = pd.read_excel(pl_file) if pl_file and pl_file.name.endswith("xlsx") else (pd.read_csv(pl_file) if pl_file else get_sample_pl())
    bs_df = pd.read_excel(bs_file) if bs_file and bs_file.name.endswith("xlsx") else (pd.read_csv(bs_file) if bs_file else get_sample_bs())
    if not pl_file and not bs_file: st.info("Showing ratios from sample data.")

    pl_m = analyze_pl(pl_df)
    bs_m = analyze_bs(bs_df)

    ratios = []
    if pl_m and bs_m:
        # Profitability
        ratios += [
            {"Category":"Profitability","Ratio":"Gross Profit Margin","Value":f"{pl_m['gpm']:.2f}%","Benchmark":"30-40%","Status":"Good" if pl_m['gpm']>30 else "Review"},
            {"Category":"Profitability","Ratio":"EBITDA Margin","Value":f"{pl_m['ebitda_margin']:.2f}%","Benchmark":"15-25%","Status":"Good" if pl_m['ebitda_margin']>15 else "Review"},
            {"Category":"Profitability","Ratio":"Net Profit Margin","Value":f"{pl_m['npm']:.2f}%","Benchmark":"8-15%","Status":"Good" if pl_m['npm']>8 else "Review"},
            {"Category":"Profitability","Ratio":"Return on Equity","Value":f"{pl_m['pat']/bs_m['equity']*100:.2f}%" if bs_m['equity'] else "N/A","Benchmark":">15%","Status":"Good" if bs_m['equity'] and pl_m['pat']/bs_m['equity']>0.15 else "Review"},
            {"Category":"Profitability","Ratio":"Return on Assets","Value":f"{pl_m['pat']/bs_m['total_assets']*100:.2f}%" if bs_m['total_assets'] else "N/A","Benchmark":">5%","Status":"Good" if bs_m['total_assets'] and pl_m['pat']/bs_m['total_assets']>0.05 else "Review"},
        ]
        # Liquidity
        ratios += [
            {"Category":"Liquidity","Ratio":"Current Ratio","Value":f"{bs_m['current_ratio']:.2f}x","Benchmark":"2x","Status":"Good" if bs_m['current_ratio']>=2 else "Low" if bs_m['current_ratio']<1 else "Adequate"},
            {"Category":"Liquidity","Ratio":"Quick Ratio","Value":f"{bs_m['quick_ratio']:.2f}x","Benchmark":"1x","Status":"Good" if bs_m['quick_ratio']>=1 else "Low"},
            {"Category":"Liquidity","Ratio":"Cash Ratio","Value":f"{bs_m['cash']/bs_m['current_liabilities']:.2f}x" if bs_m['current_liabilities'] else "N/A","Benchmark":"0.5x","Status":"Good" if bs_m['current_liabilities'] and bs_m['cash']/bs_m['current_liabilities']>=0.5 else "Low"},
        ]
        # Leverage
        ratios += [
            {"Category":"Leverage","Ratio":"Debt/Equity Ratio","Value":f"{bs_m['de_ratio']:.2f}x","Benchmark":"<1x","Status":"Good" if bs_m['de_ratio']<1 else "High"},
            {"Category":"Leverage","Ratio":"Interest Coverage","Value":f"{pl_m['ebitda']/pl_m['interest']:.2f}x" if pl_m['interest'] else "N/A","Benchmark":">3x","Status":"Good" if pl_m['interest'] and pl_m['ebitda']/pl_m['interest']>3 else "Low"},
            {"Category":"Leverage","Ratio":"Debt/EBITDA","Value":f"{bs_m['debt']/pl_m['ebitda']:.2f}x" if pl_m['ebitda'] else "N/A","Benchmark":"<3x","Status":"Good" if pl_m['ebitda'] and bs_m['debt']/pl_m['ebitda']<3 else "High"},
        ]
        # Efficiency
        ratios += [
            {"Category":"Efficiency","Ratio":"Asset Turnover","Value":f"{pl_m['revenue']/bs_m['total_assets']:.2f}x" if bs_m['total_assets'] else "N/A","Benchmark":">1x","Status":"Good" if bs_m['total_assets'] and pl_m['revenue']/bs_m['total_assets']>1 else "Low"},
            {"Category":"Efficiency","Ratio":"Inventory Turnover","Value":f"{pl_m['revenue']/bs_m['inventory']:.2f}x" if bs_m['inventory'] else "N/A","Benchmark":">4x","Status":"Good" if bs_m['inventory'] and pl_m['revenue']/bs_m['inventory']>4 else "Low"},
            {"Category":"Efficiency","Ratio":"Receivables Turnover","Value":f"{pl_m['revenue']/bs_m['receivables']:.2f}x" if bs_m['receivables'] else "N/A","Benchmark":">6x","Status":"Good" if bs_m['receivables'] and pl_m['revenue']/bs_m['receivables']>6 else "Low"},
        ]

    ratio_df = pd.DataFrame(ratios)
    def color_status(row):
        if row["Status"] == "Good": return ["background-color:#f0fdf4;color:#166534"]*len(row)
        elif row["Status"] in ["Low","High"]: return ["background-color:#fef2f2;color:#991b1b"]*len(row)
        else: return ["background-color:#fffbeb;color:#92400e"]*len(row)

    for cat in ["Profitability","Liquidity","Leverage","Efficiency"]:
        cat_df = ratio_df[ratio_df["Category"]==cat].drop("Category",axis=1)
        if not cat_df.empty:
            st.markdown(f"#### {cat} Ratios")
            st.dataframe(cat_df.style.apply(color_status,axis=1), use_container_width=True, hide_index=True)

    st.download_button("Download Ratio Report", to_excel(ratio_df), "Ratio_Analysis.xlsx", use_container_width=True)

# ══════════════════════════════════════════════════════════════
# CASH FLOW INSIGHTS
# ══════════════════════════════════════════════════════════════
elif page == "Cash Flow Insights":
    header("Cash Flow Insights", "Operating, investing and financing cash flows with burn rate and runway analysis")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    cf_file = st.file_uploader("Upload Cash Flow Statement or Bank Statement", type=["xlsx","csv"], label_visibility="collapsed")
    st.download_button("Download Sample", to_excel(get_sample_bank()), "Sample_Bank.xlsx")
    st.markdown("</div>", unsafe_allow_html=True)

    df = pd.read_excel(cf_file) if cf_file and cf_file.name.endswith("xlsx") else (pd.read_csv(cf_file) if cf_file else get_sample_bank())
    if not cf_file: st.info("Showing sample bank statement data.")

    amt_col = next((c for c in df.columns if "amount" in c.lower()), df.columns[3] if len(df.columns)>3 else df.columns[-1])
    type_col = next((c for c in df.columns if "type" in c.lower()), None)
    cat_col = next((c for c in df.columns if "category" in c.lower()), df.columns[1] if len(df.columns)>1 else None)

    if type_col:
        inflows = df[df[type_col]=="Credit"][amt_col].sum()
        outflows = df[df[type_col]=="Debit"][amt_col].sum()
    else:
        inflows = df[amt_col].sum()
        outflows = 0

    net = inflows - outflows
    monthly_burn = outflows / max(1, len(df["Date"].unique()) if "Date" in df.columns else 12) * 30

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Inflows", fmt_inr(inflows))
    c2.metric("Total Outflows", fmt_inr(outflows))
    c3.metric("Net Cash Flow", fmt_inr(net), "Positive" if net > 0 else "Negative")
    c4.metric("Monthly Burn Rate", fmt_inr(monthly_burn))

    if cat_col and type_col:
        op_cats = ["Sales Receipt","Vendor Payment","Salary","Rent","Utilities","Office Expenses"]
        inv_cats = ["Asset Purchase","Investment","Loan Given"]
        fin_cats = ["Loan EMI","Loan Receipt","Dividend"]

        op_in = df[(df[type_col]=="Credit") & (df[cat_col].isin(op_cats))][amt_col].sum()
        op_out = df[(df[type_col]=="Debit") & (df[cat_col].isin(op_cats))][amt_col].sum()
        fin_out = df[(df[type_col]=="Debit") & (df[cat_col].isin(fin_cats))][amt_col].sum()

        cf_summary = pd.DataFrame({
            "Activity":["Operating","Investing","Financing"],
            "Inflows":[op_in,0,0],
            "Outflows":[op_out,0,fin_out],
            "Net":[op_in-op_out,0,-fin_out]
        })

        fig = px.bar(cf_summary.melt(id_vars="Activity",value_vars=["Inflows","Outflows"],var_name="Type",value_name="Amount"),
            x="Activity",y="Amount",color="Type",barmode="group",title="Cash Flow by Activity",
            color_discrete_map={"Inflows":"#16a34a","Outflows":"#dc2626"})
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#f8fafc",font=dict(family="Inter"),font_color="#1e293b")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### AI Insights")
    if net > 0: insight(f"Positive net cash flow of {fmt_inr(net)} — business is cash generative", "positive")
    else: insight(f"Negative net cash flow of {fmt_inr(abs(net))} — cash reserves are depleting", "negative")
    if monthly_burn > 0:
        insight(f"Monthly burn rate of {fmt_inr(monthly_burn)} — ensure sufficient working capital buffer of at least 3 months = {fmt_inr(monthly_burn*3)}", "info")

# ══════════════════════════════════════════════════════════════
# AI CFO CHAT
# ══════════════════════════════════════════════════════════════
elif page == "AI CFO Chat":
    header("AI CFO Chat", "Ask any financial question about your business — powered by Claude AI")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "financial_context" not in st.session_state:
        st.session_state.financial_context = ""

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-title'>Upload Financial Statements for Context</p>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        pl_f = st.file_uploader("P&L Statement (optional)", type=["xlsx","csv"], key="pl_chat", label_visibility="collapsed")
        st.caption("P&L Statement")
    with c2:
        bs_f = st.file_uploader("Balance Sheet (optional)", type=["xlsx","csv"], key="bs_chat", label_visibility="collapsed")
        st.caption("Balance Sheet")

    if pl_f or bs_f:
        ctx = f"Company: {company}, Industry: {industry}, Period: {fy}\n"
        if pl_f:
            df = pd.read_excel(pl_f) if pl_f.name.endswith("xlsx") else pd.read_csv(pl_f)
            m = analyze_pl(df)
            if m:
                ctx += f"\nP&L Data: Revenue={fmt_inr(m['revenue'])}, PAT={fmt_inr(m['pat'])}, Gross Margin={m['gpm']:.1f}%, Net Margin={m['npm']:.1f}%, Revenue Growth={m['rev_growth']:.1f}%"
        if bs_f:
            df = pd.read_excel(bs_f) if bs_f.name.endswith("xlsx") else pd.read_csv(bs_f)
            m = analyze_bs(df)
            if m:
                ctx += f"\nBalance Sheet Data: Total Assets={fmt_inr(m['total_assets'])}, Equity={fmt_inr(m['equity'])}, Current Ratio={m['current_ratio']:.2f}x, D/E Ratio={m['de_ratio']:.2f}x"
        st.session_state.financial_context = ctx
        st.success("Financial context loaded — AI now has access to your data")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-title'>Chat with Your CFO</p>", unsafe_allow_html=True)

    # Sample questions
    st.markdown("<p style='font-size:12px;color:#64748b;margin-bottom:8px;font-weight:600;'>SUGGESTED QUESTIONS</p>", unsafe_allow_html=True)
    q_cols = st.columns(3)
    sample_qs = [
        "What is my profit margin and how does it compare to industry?",
        "Where can I reduce costs in my business?",
        "Is my current ratio healthy?",
        "How can I improve my cash flow?",
        "What are the biggest risks in my financials?",
        "Should I take on more debt to expand?"
    ]
    for i, q in enumerate(sample_qs):
        with q_cols[i%3]:
            if st.button(q, key=f"sq_{i}", use_container_width=True):
                st.session_state.pending_question = q

    # Display chat
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user-label'>You</div><div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai-label'>FinFlow AI CFO</div><div class='chat-ai'>{msg['content']}</div>", unsafe_allow_html=True)

    # Input
    user_input = st.text_input("Ask your CFO a question...", key="chat_input", label_visibility="collapsed", placeholder="e.g. What is my debt-to-equity ratio and what does it mean?")
    if hasattr(st.session_state, 'pending_question'):
        user_input = st.session_state.pending_question
        del st.session_state.pending_question

    c1,c2 = st.columns([5,1])
    with c2:
        send = st.button("Send", use_container_width=True)

    if (send or user_input) and user_input:
        st.session_state.chat_history.append({"role":"user","content":user_input})
        system = f"""You are FinFlow AI — an expert CFO and financial advisor with deep knowledge of Indian business finance, accounting standards (Ind AS), GST, and corporate finance.

You are analyzing the financials of: {company}, operating in {industry} sector for {fy}.

{f'Financial Context: {st.session_state.financial_context}' if st.session_state.financial_context else 'No financial statements uploaded yet — provide general advice.'}

Respond in a professional yet accessible tone. Be specific, data-driven, and actionable. Reference specific numbers when available. Keep responses concise but comprehensive. Use Indian financial context (Rs, lakhs, crores, RBI guidelines, SEBI norms where relevant)."""

        messages = [{"role":"user","content":f"{system}\n\nQuestion: {user_input}"}]
        for h in st.session_state.chat_history[-6:-1]:
            messages.append(h)

        if openai_key:
            with st.spinner("FinFlow AI is analyzing..."):
                response = call_ai([{"role":"user","content":f"{system}\n\nQuestion: {user_input}"}], openai_key)
        else:
            response = f"""**FinFlow AI Response** (Demo Mode — Add API Key for Full AI)

Based on your query about "{user_input}" for {company} in the {industry} sector:

**Key Insights:**
- For {industry} companies, industry benchmark margins typically range between 10-20% for net profit
- Maintaining a current ratio above 2x is recommended for healthy liquidity
- Debt/equity ratio below 1x indicates conservative financial management

**Recommendations:**
1. Review your cost structure quarterly against revenue growth
2. Maintain minimum 3 months of operating expenses as cash buffer
3. Monitor receivables turnover — aim for collection within 45 days

*Add your OpenAI/Anthropic API key in the sidebar to get personalized AI analysis based on your actual financial data.*"""

        st.session_state.chat_history.append({"role":"assistant","content":response})
        st.rerun()

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# EXECUTIVE REPORT
# ══════════════════════════════════════════════════════════════
elif page == "Executive Report":
    header("Executive Report Generator", "One-click comprehensive financial report for board meetings and investor presentations")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-title'>Upload Statements to Generate Report</p>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        pl_f = st.file_uploader("P&L Statement", type=["xlsx","csv"], key="pl_rep", label_visibility="collapsed")
        st.caption("P&L Statement")
    with c2:
        bs_f = st.file_uploader("Balance Sheet", type=["xlsx","csv"], key="bs_rep", label_visibility="collapsed")
        st.caption("Balance Sheet")
    st.markdown("</div>", unsafe_allow_html=True)

    pl_df = pd.read_excel(pl_f) if pl_f and pl_f.name.endswith("xlsx") else (pd.read_csv(pl_f) if pl_f else get_sample_pl())
    bs_df = pd.read_excel(bs_f) if bs_f and bs_f.name.endswith("xlsx") else (pd.read_csv(bs_f) if bs_f else get_sample_bs())
    if not pl_f: st.info("Showing report from sample data.")

    pl_m = analyze_pl(pl_df)
    bs_m = analyze_bs(bs_df)

    if pl_m and bs_m:
        st.markdown(f"""
        <div style='background:#0f172a;border-radius:10px;padding:32px;margin-bottom:20px;'>
            <p style='color:#475569;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 8px;'>EXECUTIVE FINANCIAL REPORT</p>
            <h1 style='color:#fff!important;font-size:28px!important;font-weight:800!important;margin:0 0 4px!important;'>{company}</h1>
            <p style='color:#64748b;font-size:14px;margin:0;'>{industry} Sector  |  {fy}  |  Generated {date.today().strftime("%d %B %Y")}</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("### Financial Highlights")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Revenue", fmt_inr(pl_m["revenue"]), f"{pl_m['rev_growth']:+.1f}% YoY")
        c2.metric("Net Profit", fmt_inr(pl_m["pat"]), f"{pl_m['pat_growth']:+.1f}% YoY")
        c3.metric("Total Assets", fmt_inr(bs_m["total_assets"]))
        c4.metric("Return on Equity", f"{pl_m['pat']/bs_m['equity']*100:.1f}%" if bs_m['equity'] else "N/A")

        st.markdown("### Performance Summary")
        summary_data = {
            "Metric":["Revenue","EBITDA","Net Profit","Gross Margin","Net Margin","Current Ratio","D/E Ratio","Total Assets","Total Equity"],
            "Value":[fmt_inr(pl_m["revenue"]),fmt_inr(pl_m["ebitda"]),fmt_inr(pl_m["pat"]),f"{pl_m['gpm']:.1f}%",f"{pl_m['npm']:.1f}%",f"{bs_m['current_ratio']:.2f}x",f"{bs_m['de_ratio']:.2f}x",fmt_inr(bs_m["total_assets"]),fmt_inr(bs_m["equity"])],
            "YoY Change":[f"{pl_m['rev_growth']:+.1f}%","-",f"{pl_m['pat_growth']:+.1f}%","-","-","-","-","-","-"],
            "Assessment":["Strong" if pl_m['rev_growth']>10 else "Moderate","Strong" if pl_m['ebitda_margin']>15 else "Review","Positive" if pl_m['pat']>0 else "Loss","Healthy" if pl_m['gpm']>30 else "Review","Healthy" if pl_m['npm']>8 else "Review","Healthy" if bs_m['current_ratio']>2 else "Review","Conservative" if bs_m['de_ratio']<1 else "High","Growing","Stable"]
        }
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

        st.markdown("### Key Observations & Recommendations")
        observations = []
        if pl_m['rev_growth'] > 10: observations.append(("positive",f"Revenue grew strongly at {pl_m['rev_growth']:.1f}% YoY to {fmt_inr(pl_m['revenue'])} — outperforming sector average"))
        if pl_m['npm'] > 10: observations.append(("positive",f"Healthy net profit margin of {pl_m['npm']:.1f}% demonstrates good cost management"))
        if bs_m['current_ratio'] < 1.5: observations.append(("warning",f"Current ratio of {bs_m['current_ratio']:.2f}x is below ideal — strengthen working capital position"))
        if bs_m['de_ratio'] > 1.5: observations.append(("negative",f"High D/E ratio of {bs_m['de_ratio']:.2f}x — prioritize debt reduction to improve financial stability"))
        if pl_m['pat'] > pl_m['pat_py'] if pl_m['pat_py'] else False: observations.append(("positive","Profit growth outpacing revenue growth — improving operating leverage"))
        observations.append(("info",f"Recommended focus areas for next quarter: Revenue growth, margin improvement, working capital optimization for {industry} sector"))

        for kind, text in observations:
            insight(text, kind)

        report_df = pd.DataFrame(summary_data)
        st.download_button("Download Executive Report", to_excel(report_df), f"FinFlow_Executive_Report_{company}_{fy}.xlsx", use_container_width=True)

# FOOTER
st.markdown("---")
st.markdown(f"""
<div style='text-align:center;padding:8px;'>
    <p style='color:#94a3b8;font-size:11px;margin:0;'>
        FinFlow AI &copy; 2026 &nbsp;|&nbsp; Built by Sanskar Gupta &nbsp;|&nbsp; guptasanskar824@gmail.com &nbsp;|&nbsp; Intelligent Financial Analysis Platform
    </p>
</div>""", unsafe_allow_html=True)

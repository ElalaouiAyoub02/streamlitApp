# ============================================================
#  pip install streamlit plotly pandas wordcloud matplotlib
#  streamlit run app.py
# ============================================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from io import BytesIO

# ════════════════════════════════════════════════════════════
#  CONFIG
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Classification Offres IT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════
#  CACHER TOOLBAR STREAMLIT + MENU + FOOTER
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Cacher toolbar native (bouton thème, fullscreen...) ── */
[data-testid="stToolbar"]          { display: none !important; }
[data-testid="stDecoration"]       { display: none !important; }
[data-testid="stStatusWidget"]     { display: none !important; }
#MainMenu                          { display: none !important; }
footer                             { display: none !important; }
header[data-testid="stHeader"]     { display: none !important; }

/* ── Cacher le bouton settings dans la sidebar ── */
[data-testid="stSidebarNav"]       { display: none !important; }
button[kind="header"]              { display: none !important; }

/* ── Supprimer padding top généré par la toolbar cachée ── */
[data-testid="stAppViewContainer"] > section:first-child {
    padding-top: 0 !important;
}
.block-container {
    padding-top: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  THEME STATE
# ════════════════════════════════════════════════════════════
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def T(dark_val, light_val):
    return dark_val if st.session_state.dark_mode else light_val

# ════════════════════════════════════════════════════════════
#  THEME VARIABLES
# ════════════════════════════════════════════════════════════
BG       = T("#0f1117", "#f8fafc")
SURFACE  = T("#1a1f2e", "#ffffff")
SURFACE2 = T("#1e2538", "#f1f5f9")
BORDER   = T("#2a3347", "#e2e8f0")
TEXT     = T("#e2e8f0", "#0f172a")
MUTED    = T("#64748b", "#94a3b8")
MUTED2   = T("#94a3b8", "#475569")
PLOT_BG  = T("#1a1f2e", "#ffffff")
GRID_COL = T("#1e293b", "#e2e8f0")
ACCENT   = T("#818cf8", "#4f46e5")

# ════════════════════════════════════════════════════════════
#  THEME CSS GLOBAL (réactif au toggle)
# ════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* ── Fond global ── */
[data-testid="stAppViewContainer"] {{
    background: {BG} !important;
}}
[data-testid="stSidebar"] {{
    background: {T("#0d1117","#f1f5f9")} !important;
    border-right: 1px solid {BORDER};
}}

/* ── Métriques ── */
[data-testid="metric-container"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px;
}}
[data-testid="metric-container"] label {{
    color: {MUTED} !important;
    font-size: 0.72rem !important;
}}
[data-testid="stMetricValue"] {{
    color: {ACCENT} !important;
    font-size: 1.8rem !important;
    font-weight: 900 !important;
}}

/* ── Textes ── */
h1  {{ color: {T("#f1f5f9","#0f172a")} !important; }}
h2  {{ color: {T("#e2e8f0","#1e293b")} !important; font-size: 1.1rem !important; }}
h3  {{ color: {T("#cbd5e1","#334155")} !important; font-size: 0.95rem !important; }}
p, li, td, th, label {{ color: {TEXT} !important; }}

/* ── Tabs ── */
[data-testid="stTabs"] button {{
    color: {MUTED};
    font-weight: 600;
    font-size: 0.82rem;
    background: transparent !important;
}}
[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {ACCENT} !important;
    border-bottom: 2px solid {ACCENT} !important;
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}
[data-testid="stExpander"] summary {{
    color: {TEXT} !important;
}}

/* ── Selectbox / slider ── */
[data-baseweb="select"] > div {{
    background: {SURFACE} !important;
    border-color: {BORDER} !important;
    color: {TEXT} !important;
}}
[data-baseweb="select"] div[class*="ValueContainer"] {{
    color: {TEXT} !important;
}}
[data-testid="stSlider"] label {{ color: {TEXT} !important; }}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 10px;
}}

/* ── Radio ── */
[data-testid="stRadio"] label {{ color: {TEXT} !important; }}

/* ── Code ── */
code {{
    background: {SURFACE2} !important;
    color: {T("#a5f3fc","#0369a1")} !important;
    border-radius: 4px;
    padding: 1px 5px;
}}

/* ── Alerts ── */
[data-testid="stInfo"]    {{ border-radius: 10px; }}
[data-testid="stSuccess"] {{ border-radius: 10px; }}
[data-testid="stWarning"] {{ border-radius: 10px; }}
[data-testid="stError"]   {{ border-radius: 10px; }}

/* ── Divider ── */
hr {{ border-color: {BORDER} !important; }}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
}}

/* ── Sidebar labels ── */
[data-testid="stSidebar"] label {{
    color: {TEXT} !important;
}}
[data-testid="stSidebar"] p {{
    color: {MUTED2} !important;
}}

/* ── Toggle button custom ── */
.theme-toggle-btn {{
    width: 100%;
    padding: 10px 0;
    border-radius: 10px;
    border: 1px solid {BORDER};
    background: {SURFACE};
    color: {TEXT};
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    transition: all .2s;
    text-align: center;
    margin-bottom: 8px;
}}
.theme-toggle-btn:hover {{
    border-color: {ACCENT};
    color: {ACCENT};
}}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════
FAM_COLORS = {
    "Data & IA":      "#6366f1",
    "Conseil & Mgmt": "#f59e0b",
    "Développement":  "#10b981",
    "Autres IT":      "#ec4899",
    "Cloud & Infra":  "#3b82f6",
}
FAM_ICONS = {
    "Data & IA":"📊","Conseil & Mgmt":"💼",
    "Développement":"💻","Autres IT":"🔐","Cloud & Infra":"☁️",
}

def dark_layout(**extra):
    base = dict(
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=MUTED2, family="Segoe UI, system-ui, sans-serif"),
    )
    base.update(extra)
    return base

def pchart(fig, height=400):
    fig.update_layout(height=height)
    st.plotly_chart(fig, width="stretch")

def safe_rgb(r, g, b):
    return (f"rgb({int(np.clip(round(r),0,255))},"
            f"{int(np.clip(round(g),0,255))},"
            f"{int(np.clip(round(b),0,255))})")

def jitter_hex(hex_color, amount=0.07):
    r, g, b = mcolors.hex2color(hex_color)
    r = r*255 + np.random.uniform(-amount*255, amount*255)
    g = g*255 + np.random.uniform(-amount*255, amount*255)
    b = b*255 + np.random.uniform(-amount*255, amount*255)
    return safe_rgb(r, g, b)


# ════════════════════════════════════════════════════════════
#  DATA
# ════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    data = {
        "job_type": [
            "Ingénieur IT Généraliste","Intelligence Artificielle","Data Analyst / BI",
            "Cybersécurité","Consultant SAP","Chef de Projet IT","DevOps / SRE",
            "Consultant ERP","Data Scientist / IA","Support / Helpdesk",
            "Data Engineer","Développeur C/C++ Embarqué","Ingénieur Télécom",
            "Développeur Python","Développeur Java","Admin Réseau",
            "Développeur Web / JS","Consultant CRM / Salesforce","Ingénieur Logiciel",
            "Admin Système","UX / Product Designer","Consultant AMOA",
            "DSI / Directeur IT","Product Owner / Manager","Architecte IT",
            "Développeur Mobile","QA / Testeur","Cloud AWS","Développeur PHP",
            "Cloud Azure","Technicien IT","Développeur Fullstack",
            "Développeur .NET / C#","Tech Lead / Eng. Manager",
            "DBA / Base de données","Data Architect","Cloud GCP",
            "Développeur Blockchain","Data Gouvernance","Ingénieur ETL / BI",
        ],
        "count": [
            7638,5935,5729,4461,3291,3072,2969,2008,1817,1315,
            1213,1067,756,733,726,663,659,628,459,387,
            383,361,317,299,284,271,271,253,225,224,
            204,202,195,177,88,67,48,48,43,37,
        ],
        "source": [
            "Auto-classifié","Auto-classifié","Auto-classifié","Auto-classifié",
            "Auto-classifié","Auto-classifié","Auto-classifié","Auto-classifié",
            "LLM-based","Auto-classifié","Auto-classifié","Auto-classifié",
            "Auto-classifié","Auto-classifié","Auto-classifié","Auto-classifié",
            "Auto-classifié","Auto-classifié","LLM-based","Auto-classifié",
            "LLM-based","Auto-classifié","Auto-classifié","LLM-based",
            "Auto-classifié","Auto-classifié","Auto-classifié","Auto-classifié",
            "Auto-classifié","Auto-classifié","LLM-based","LLM-based",
            "Auto-classifié","Auto-classifié","LLM-based","LLM-based",
            "Auto-classifié","LLM-based","LLM-based","LLM-based",
        ],
        "famille": [
            "Conseil & Mgmt","Data & IA","Data & IA","Autres IT","Conseil & Mgmt",
            "Conseil & Mgmt","Cloud & Infra","Conseil & Mgmt","Data & IA","Autres IT",
            "Data & IA","Développement","Autres IT","Développement","Développement",
            "Cloud & Infra","Développement","Conseil & Mgmt","Développement","Cloud & Infra",
            "Autres IT","Conseil & Mgmt","Conseil & Mgmt","Conseil & Mgmt","Conseil & Mgmt",
            "Développement","Autres IT","Cloud & Infra","Développement","Cloud & Infra",
            "Autres IT","Développement","Développement","Conseil & Mgmt","Cloud & Infra",
            "Data & IA","Cloud & Infra","Développement","Data & IA","Data & IA",
        ],
    }
    df = pd.DataFrame(data)
    df["pct"] = (df["count"] / df["count"].sum() * 100).round(2)
    return df

df    = load_data()
TOTAL = int(df["count"].sum())


# ════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Logo ────────────────────────────────────────────────
    st.markdown(f"""
    <div style='padding:4px 0 16px;'>
        <div style='font-size:1.8rem;'>🤖</div>
        <div style='font-size:0.95rem;font-weight:800;
                    color:{TEXT};margin-top:6px;'>Classification IT</div>
        <div style='font-size:0.7rem;color:{MUTED};margin-top:2px;'>
            Projet Job Matching · 2025
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TOGGLE THÈME ────────────────────────────────────────
    # Un seul bouton, pleine largeur, contrôle toute la page
    icon = "☀️ Mode Clair" if st.session_state.dark_mode else "🌙 Mode Sombre"
    label = icon
    if st.button(label, key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.divider()

    # ── Filtres ─────────────────────────────────────────────
    st.markdown(f"<p style='font-size:0.75rem;font-weight:800;text-transform:uppercase;"
                f"letter-spacing:.08em;color:{MUTED};margin-bottom:8px;'>🔧 Filtres</p>",
                unsafe_allow_html=True)

    fam_sel = st.selectbox(
        "Famille métier",
        ["Toutes"] + sorted(df["famille"].unique()),
    )
    src_sel = st.selectbox(
        "Méthode",
        ["Toutes","Auto-classifié (Non LLM)","LLM-based"],
    )
    top_n = st.slider("Top N catégories", 5, 40, 15, 5)

    st.divider()

    # ── Stats rapides ────────────────────────────────────────
    st.markdown(f"<p style='font-size:0.75rem;font-weight:800;text-transform:uppercase;"
                f"letter-spacing:.08em;color:{MUTED};margin-bottom:8px;'>📊 Résumé</p>",
                unsafe_allow_html=True)

    auto_c = int(df[df["source"]=="Auto-classifié"]["count"].sum())
    llm_c  = int(df[df["source"]=="LLM-based"]["count"].sum())

    for lbl, val in [("Offres IT totales", f"{TOTAL:,}"),
                     ("Catégories", "40"),
                     ("Familles", "5")]:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;
                    padding:7px 0;border-bottom:1px solid {BORDER};'>
            <span style='font-size:0.75rem;color:{MUTED};'>{lbl}</span>
            <span style='font-size:0.82rem;font-weight:800;color:{ACCENT};'>{val}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:{SURFACE};border:1px solid {BORDER};
                border-radius:10px;padding:12px;margin-top:4px;'>
        <div style='display:flex;justify-content:space-between;
                    align-items:center;margin-bottom:6px;'>
            <span style='font-size:0.72rem;color:{MUTED};'>⚡ Auto-classifié</span>
            <span style='font-size:0.78rem;font-weight:800;color:#3b82f6;'>{auto_c:,}</span>
        </div>
        <div style='height:4px;background:{BORDER};border-radius:3px;overflow:hidden;margin-bottom:10px;'>
            <div style='width:80%;height:100%;background:#3b82f6;border-radius:3px;'></div>
        </div>
        <div style='display:flex;justify-content:space-between;
                    align-items:center;margin-bottom:6px;'>
            <span style='font-size:0.72rem;color:{MUTED};'>🤖 LLM-based</span>
            <span style='font-size:0.78rem;font-weight:800;color:#6366f1;'>{llm_c:,}</span>
        </div>
        <div style='height:4px;background:{BORDER};border-radius:3px;overflow:hidden;margin-bottom:10px;'>
            <div style='width:15%;height:100%;background:#6366f1;border-radius:3px;'></div>
        </div>
        <div style='display:flex;justify-content:space-between;
                    align-items:center;margin-bottom:6px;'>
            <span style='font-size:0.72rem;color:{MUTED};'>⚠️ Fallback</span>
            <span style='font-size:0.78rem;font-weight:800;color:#f59e0b;'>1 213</span>
        </div>
        <div style='height:4px;background:{BORDER};border-radius:3px;overflow:hidden;'>
            <div style='width:5%;height:100%;background:#f59e0b;border-radius:3px;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown(f"<p style='font-size:0.68rem;color:{MUTED};text-align:center;'>"
                f"💰 Coût LLM : ~0,07 $ · ⏱️ ~160 min · 🚀 gemini-2.5-flash</p>",
                unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  FILTRES APPLIQUÉS
# ════════════════════════════════════════════════════════════
df_f = df.copy()
if fam_sel != "Toutes":
    df_f = df_f[df_f["famille"] == fam_sel]
if src_sel == "LLM-based":
    df_f = df_f[df_f["source"] == "LLM-based"]
elif src_sel == "Auto-classifié (Non LLM)":
    df_f = df_f[df_f["source"] == "Auto-classifié"]

df_top = df_f.nlargest(top_n, "count")


# ════════════════════════════════════════════════════════════
#  HEADER PAGE
# ════════════════════════════════════════════════════════════
hbg  = T("linear-gradient(135deg,#1e1b4b,#1a1f2e)",
          "linear-gradient(135deg,#ede9fe,#f0f9ff)")
hbdr = T("#334155","#c7d2fe")
htag = T("#818cf8","#4f46e5")
hh1  = T("#f1f5f9","#0f172a")
hsub = T("#94a3b8","#475569")

st.markdown(f"""
<div style='background:{hbg};border:1px solid {hbdr};
            border-radius:16px;padding:28px 32px;margin-bottom:24px;'>
    <div style='font-size:0.72rem;color:{htag};text-transform:uppercase;
                letter-spacing:.1em;margin-bottom:8px;'>
        📋 RAPPORT TECHNIQUE · JOB MATCHING IT · 2025
    </div>
    <h1 style='font-size:2rem;font-weight:900;color:{hh1};margin:0 0 8px;'>
        Classification Automatique des Offres IT
    </h1>
    <p style='color:{hsub};font-size:0.88rem;margin:0;'>
        Pipeline hybride · Auto-classification (Non LLM) + LLM-based (Gemini)
        · 66 205 offres · 40 catégories
    </p>
</div>
""", unsafe_allow_html=True)

# KPIs
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("📦 Offres analysées",      "66 205",  help="Dataset brut")
k2.metric("✅ Offres IT classifiées", "50 121",  "75,71 %")
k3.metric("🗂️ Catégories IT",          "40",      help="Métiers identifiés")
k4.metric("⚡ Auto-classifié",          "~80 %",   help="Non LLM · 0 $ · < 5 sec")
k5.metric("💰 Coût LLM",               "0,07 $",  help="14 287 offres Gemini 2.5 Flash")
st.divider()


# ════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════
tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "📊 Distribution",
    "☁️ Nuage de mots",
    "⚙️ Pipeline",
    "⚡ Auto-classification",
    "🤖 LLM-based",
])


# ══════════════════════════════════════════════════════
#  TAB 1 — DISTRIBUTION
# ══════════════════════════════════════════════════════
with tab1:

    st.markdown("### Répartition par famille métier")
    fam_df = (df.groupby("famille")["count"].sum().reset_index()
                .assign(pct=lambda x:(x["count"]/TOTAL*100).round(1))
                .sort_values("count", ascending=False))

    pills = st.columns(len(fam_df))
    for i, row in enumerate(fam_df.itertuples()):
        c  = FAM_COLORS.get(row.famille, "#6366f1")
        ic = FAM_ICONS.get(row.famille, "🔵")
        with pills[i]:
            st.markdown(f"""
            <div style='background:{T("rgba(255,255,255,.04)","rgba(0,0,0,.02)")};
                        border:1px solid {c}44;border-radius:12px;
                        padding:16px;text-align:center;'>
                <div style='font-size:1.6rem;'>{ic}</div>
                <div style='font-size:0.64rem;font-weight:800;text-transform:uppercase;
                            color:{c};margin:6px 0 2px;'>{row.famille}</div>
                <div style='font-size:1.25rem;font-weight:900;color:{c};'>{row.count:,}</div>
                <div style='font-size:0.67rem;color:{MUTED};'>{row.pct} %</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    ca, cb = st.columns(2)
    with ca:
        fig = px.pie(fam_df, names="famille", values="count",
                     color="famille", color_discrete_map=FAM_COLORS,
                     hole=0.65, title="Répartition par famille")
        fig.update_traces(
            textposition="outside", textfont_size=11,
            marker=dict(line=dict(color=BG, width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,} offres<br>%{percent}<extra></extra>",
        )
        fig.update_layout(**dark_layout(
            showlegend=True,
            legend=dict(font=dict(size=11,color=MUTED2),bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=50,b=20,l=20,r=100),
            title=dict(font=dict(color=T("#cbd5e1","#334155"),size=13)),
        ))
        fig.add_annotation(text=f"<b>{TOTAL:,}</b><br>offres IT",
                           x=0.5, y=0.5, showarrow=False,
                           font=dict(size=13,color=TEXT))
        pchart(fig, 340)

    with cb:
        src_map = {"Auto-classifié":"⚡ Auto-classifié (Non LLM)",
                   "LLM-based":"🤖 LLM-based"}
        src_df = (df.groupby("source")["count"].sum().reset_index()
                    .assign(label=lambda x: x["source"].map(src_map)))
        fig = px.pie(src_df, names="label", values="count", color="label",
                     color_discrete_map={"⚡ Auto-classifié (Non LLM)":"#3b82f6",
                                         "🤖 LLM-based":"#6366f1"},
                     hole=0.65, title="Méthode de classification")
        fig.update_traces(
            textposition="outside", textfont_size=11,
            marker=dict(line=dict(color=BG,width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,} offres<br>%{percent}<extra></extra>",
        )
        fig.update_layout(**dark_layout(
            showlegend=True,
            legend=dict(font=dict(size=11,color=MUTED2),bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=50,b=20,l=20,r=130),
            title=dict(font=dict(color=T("#cbd5e1","#334155"),size=13)),
        ))
        pchart(fig, 340)

    st.markdown("---")
    st.markdown(f"### Top {top_n} catégories IT")

    fig = px.bar(
        df_top.sort_values("count"),
        x="count", y="job_type", orientation="h",
        color="famille", color_discrete_map=FAM_COLORS,
        text="count", custom_data=["pct","source","famille"],
        title=f"Top {top_n} catégories",
    )
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        textfont=dict(size=10,color=MUTED),
        marker=dict(line=dict(width=0)), marker_cornerradius=4,
        hovertemplate=(
            "<b>%{y}</b><br>Offres : <b>%{x:,}</b><br>"
            "Part : <b>%{customdata[0]} %</b><br>"
            "Famille : %{customdata[2]}<br>"
            "Méthode : %{customdata[1]}<extra></extra>"
        ),
    )
    fig.update_layout(**dark_layout(
        showlegend=True,
        legend=dict(title=dict(text="Famille",font=dict(color=MUTED,size=11)),
                    font=dict(color=MUTED2,size=11),bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=50,b=20,l=210,r=80),
        title=dict(font=dict(color=T("#cbd5e1","#334155"),size=13)),
        xaxis=dict(title="Nombre d'offres",gridcolor=GRID_COL,zerolinecolor=GRID_COL),
        yaxis=dict(title="",tickfont=dict(size=11),gridcolor=GRID_COL),
    ))
    pchart(fig, max(380, top_n*34))

    st.markdown("---")
    st.markdown("### Distribution complète — 40 catégories")
    fig = px.bar(
        df.sort_values("count"),
        x="count", y="job_type", orientation="h",
        color="famille", color_discrete_map=FAM_COLORS,
        custom_data=["pct","source"],
        title="Les 40 catégories IT · 50 121 offres",
    )
    fig.update_traces(
        marker=dict(line=dict(width=0)), marker_cornerradius=3,
        hovertemplate=(
            "<b>%{y}</b><br>Offres : <b>%{x:,}</b><br>"
            "Part : <b>%{customdata[0]} %</b><br>"
            "Méthode : %{customdata[1]}<extra></extra>"
        ),
    )
    fig.update_layout(**dark_layout(
        showlegend=True,
        legend=dict(title=dict(text="Famille",font=dict(color=MUTED,size=11)),
                    font=dict(color=MUTED2,size=11),bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=50,b=20,l=230,r=40),
        title=dict(font=dict(color=T("#cbd5e1","#334155"),size=13)),
        xaxis=dict(title="Nombre d'offres",gridcolor=GRID_COL,zerolinecolor=GRID_COL),
        yaxis=dict(title="",tickfont=dict(size=10),gridcolor=GRID_COL),
    ))
    pchart(fig, 860)

    st.markdown("---")
    st.markdown("### Treemap — Vue proportionnelle")
    fig = px.treemap(
        df, path=["famille","job_type"], values="count",
        color="famille", color_discrete_map=FAM_COLORS,
        custom_data=["pct","source"],
        title="Répartition hiérarchique : Famille → Catégorie",
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>%{value:,} offres<br>%{customdata[0]} %<extra></extra>",
        textfont=dict(size=11), marker=dict(cornerradius=4),
    )
    fig.update_layout(**dark_layout(
        margin=dict(t=50,b=10,l=10,r=10),
        title=dict(font=dict(color=T("#cbd5e1","#334155"),size=13)),
    ))
    pchart(fig, 480)

    st.markdown("---")
    st.markdown("### 📋 Tableau détaillé")
    df_show = df_f.sort_values("count", ascending=False).reset_index(drop=True)
    df_show.index += 1
    df_show.columns = ["Catégorie","Offres","Méthode","Famille","Part (%)"]
    st.dataframe(
        df_show, width="stretch", height=400,
        column_config={
            "Offres":   st.column_config.NumberColumn(format="%d"),
            "Part (%)": st.column_config.ProgressColumn(
                format="%.2f %%", min_value=0, max_value=float(df["pct"].max())),
            "Méthode":  st.column_config.SelectboxColumn(
                options=["Auto-classifié","LLM-based"]),
        },
    )
    st.download_button(
        "⬇️ Télécharger CSV",
        df_f.to_csv(index=False).encode("utf-8"),
        "distribution_it.csv","text/csv",
    )


# ══════════════════════════════════════════════════════
#  TAB 2 — NUAGE DE MOTS
# ══════════════════════════════════════════════════════
with tab2:

    st.markdown("### ☁️ Nuages de mots")
    wc_choice = st.radio(
        "Choisir le nuage",
        ["Catégories IT (par volume)","Technologies & mots-clés"],
        horizontal=True,
    )

    wc_bg = T("#1a1f2e","#f8fafc")

    def render_wc(wc_obj):
        fig, ax = plt.subplots(figsize=(14, 5.8))
        fig.patch.set_facecolor(wc_bg)
        ax.set_facecolor(wc_bg)
        ax.imshow(wc_obj.to_array(), interpolation="bilinear")
        ax.axis("off")
        plt.tight_layout(pad=0)
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=150,
                    bbox_inches="tight", facecolor=wc_bg)
        plt.close(fig)
        buf.seek(0)
        return buf

    @st.cache_data
    def wc_categories(dark):
        freq    = dict(zip(df["job_type"], df["count"]))
        fam_map = dict(zip(df["job_type"], df["famille"]))
        bg      = "#1a1f2e" if dark else "#f8fafc"
        def color_func(word, **kw):
            return jitter_hex(FAM_COLORS.get(fam_map.get(word,"Data & IA"),"#6366f1"), 0.07)
        wc = WordCloud(
            width=1400, height=580, background_color=bg,
            max_words=60, prefer_horizontal=0.75,
            color_func=color_func, margin=12,
            relative_scaling=0.6, min_font_size=10,
        ).generate_from_frequencies(freq)
        return render_wc(wc)

    @st.cache_data
    def wc_tech(dark):
        tech_freq = {
            "Python":3800,"Java":3500,"JavaScript":3200,"TypeScript":2600,
            "C++":1800,"PHP":1100,"C#":1000,"Go":550,"Kotlin":750,"SQL":4500,
            "Spring Boot":3000,"React":2800,"Angular":2100,"Vue.js":1000,
            "Node.js":1700,"Django":1300,"FastAPI":850,".NET":900,
            "Docker":4200,"Kubernetes":3600,"Terraform":2700,"AWS":2500,
            "Azure":2300,"CI/CD":2900,"Jenkins":1700,"Ansible":1500,
            "GitLab":2100,"GCP":1100,"Machine Learning":4800,"TensorFlow":2600,
            "PyTorch":2400,"Apache Spark":2000,"Kafka":1800,"Airflow":1600,
            "Databricks":1400,"Power BI":3200,"BigQuery":1100,"LLM":1900,
            "Scikit-learn":1300,"Pandas":2000,"NumPy":1600,"SAP":4000,
            "ABAP":1700,"Pentest":1100,"Salesforce":1200,"Scrum":2600,"Agile":3000,
        }
        _d="#6366f1";_l="#10b981";_c="#f59e0b";_f="#3b82f6";_e="#ec4899"
        color_map = {
            **dict.fromkeys(["Machine Learning","TensorFlow","PyTorch","Apache Spark","Kafka",
                              "Airflow","Databricks","Power BI","BigQuery","LLM",
                              "Scikit-learn","Pandas","NumPy","SQL"],_d),
            **dict.fromkeys(["Python","Java","JavaScript","TypeScript","C++","PHP","C#","Go","Kotlin"],_l),
            **dict.fromkeys(["Docker","Kubernetes","Terraform","AWS","Azure","CI/CD",
                              "Jenkins","Ansible","GitLab","GCP"],_c),
            **dict.fromkeys(["Spring Boot","React","Angular","Vue.js","Node.js","Django","FastAPI",".NET"],_f),
            **dict.fromkeys(["SAP","ABAP","Pentest","Salesforce","Scrum","Agile"],_e),
        }
        bg = "#1a1f2e" if dark else "#f8fafc"
        def color_func(word, **kw):
            return jitter_hex(color_map.get(word,"#64748b"), 0.07)
        wc = WordCloud(
            width=1400, height=580, background_color=bg,
            max_words=80, prefer_horizontal=0.70,
            color_func=color_func, margin=10,
            relative_scaling=0.55, min_font_size=10,
        ).generate_from_frequencies(tech_freq)
        return render_wc(wc)

    dark_flag = st.session_state.dark_mode

    if wc_choice == "Catégories IT (par volume)":
        st.info("💡 La **taille** est proportionnelle au nombre d'offres. La **couleur** correspond à la famille.")
        st.image(wc_categories(dark_flag), use_container_width=True)
        leg = st.columns(5)
        for i,(fam,color) in enumerate(FAM_COLORS.items()):
            with leg[i]:
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:6px;"
                    f"font-size:0.73rem;color:{MUTED2};'>"
                    f"<div style='width:12px;height:12px;border-radius:3px;"
                    f"background:{color};'></div>"
                    f"{FAM_ICONS.get(fam,'🔵')} {fam}</div>",
                    unsafe_allow_html=True)
    else:
        st.info("💡 Technologies et mots-clés détectés par l'auto-classification (règles regex).")
        st.image(wc_tech(dark_flag), use_column_width=True)
        leg2 = st.columns(5)
        for i,(color,label) in enumerate([
            ("#6366f1","Data & IA"),("#10b981","Langages"),
            ("#f59e0b","Cloud & DevOps"),("#3b82f6","Frameworks"),("#ec4899","ERP/Sécu")
        ]):
            with leg2[i]:
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:6px;"
                    f"font-size:0.72rem;color:{MUTED2};'>"
                    f"<span style='width:10px;height:10px;border-radius:3px;"
                    f"background:{color};display:inline-block;'></span>{label}</div>",
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Top technologies — fréquence estimée")
    tech_df = pd.DataFrame([
        {"tech":"Machine Learning","freq":4800,"cat":"Data & IA"},
        {"tech":"SQL",             "freq":4500,"cat":"Data & IA"},
        {"tech":"Docker",          "freq":4200,"cat":"Cloud & DevOps"},
        {"tech":"SAP",             "freq":4000,"cat":"ERP / Sécu"},
        {"tech":"Python",          "freq":3800,"cat":"Langages"},
        {"tech":"Kubernetes",      "freq":3600,"cat":"Cloud & DevOps"},
        {"tech":"Java",            "freq":3500,"cat":"Langages"},
        {"tech":"Power BI",        "freq":3200,"cat":"Data & IA"},
        {"tech":"Spring Boot",     "freq":3000,"cat":"Frameworks"},
        {"tech":"CI/CD",           "freq":2900,"cat":"Cloud & DevOps"},
        {"tech":"React",           "freq":2800,"cat":"Frameworks"},
        {"tech":"Terraform",       "freq":2700,"cat":"Cloud & DevOps"},
        {"tech":"TensorFlow",      "freq":2600,"cat":"Data & IA"},
        {"tech":"TypeScript",      "freq":2600,"cat":"Langages"},
    ]).sort_values("freq")
    fig = px.bar(tech_df, x="freq", y="tech", orientation="h", color="cat",
                 color_discrete_map={"Data & IA":"#6366f1","Langages":"#10b981",
                                     "Cloud & DevOps":"#f59e0b","Frameworks":"#3b82f6",
                                     "ERP / Sécu":"#ec4899"},
                 title="Fréquence estimée des technologies",
                 labels={"freq":"Fréquence","tech":"","cat":"Catégorie"})
    fig.update_traces(marker=dict(line=dict(width=0)),marker_cornerradius=4,
                      hovertemplate="<b>%{y}</b><br>%{x:,}<extra></extra>")
    fig.update_layout(**dark_layout(
        showlegend=True,
        legend=dict(font=dict(color=MUTED2,size=11),bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=50,b=20,l=160,r=30),
        title=dict(font=dict(color=T("#cbd5e1","#334155"),size=13)),
        xaxis=dict(title="Offres concernées (estimé)",gridcolor=GRID_COL,zerolinecolor=GRID_COL),
        yaxis=dict(title="",gridcolor=GRID_COL),
    ))
    pchart(fig, 480)


# ══════════════════════════════════════════════════════
#  TAB 3 — PIPELINE
# ══════════════════════════════════════════════════════
with tab3:

    st.markdown("### ⚡ Pipeline de traitement complet")
    fig = go.Figure(go.Funnel(
        y=["CSV Brut","→ Parquet Nettoyé","GCS Upload","BigQuery Import",
           "⚡ Auto-classifié (~80 %)","🤖 LLM-based (~20 %)","✅ Dataset Final"],
        x=[66205,66205,66205,66205,52000,14287,50121],
        textposition="inside", textinfo="value+percent initial",
        marker=dict(color=["#334155","#475569","#64748b","#3b82f6","#6366f1","#8b5cf6","#10b981"]),
        connector=dict(line=dict(color=BORDER,dash="dot",width=2)),
        hovertemplate="<b>%{y}</b><br>Offres : %{x:,}<extra></extra>",
    ))
    fig.update_layout(**dark_layout(margin=dict(t=30,b=20,l=20,r=20)))
    pchart(fig, 440)

    st.markdown("---")
    st.markdown("### 📐 Étapes détaillées")

    steps = [
        ("1","📄 CSV → Parquet","#3b82f6",
         "Le CSV avait des **sauts de ligne** et **virgules** dans le texte. "
         "Conversion Parquet via PyArrow + Snappy. Zéro problème d'encodage.",
         "python","df.to_parquet('jobs.parquet', engine='pyarrow',\n    compression='snappy', index=False)"),
        ("2","☁️ GCS Upload","#6366f1",
         "Upload `gsutil cp` vers `gs://jobmatching/`. Source BigQuery + backup.",
         "bash","gsutil cp jobs_for_bigquery.parquet gs://jobmatching/"),
        ("3","⚡ Auto-classification","#10b981",
         "`REGEXP_CONTAINS` sur `matching_text`. CASE WHEN hiérarchique. "
         "**~52 000 offres · < 5 sec · 0 $.**",
         "sql",
         "CREATE OR REPLACE TABLE jobs_classified AS\nSELECT *,\n  CASE\n"
         "    WHEN REGEXP_CONTAINS(LOWER(matching_text),\n"
         "         r'\\bsap\\b|abap') THEN 'Consultant SAP'\n"
         "    ...\n    ELSE 'Divers IT'\n  END AS job_type\nFROM jobs_raw;"),
        ("4","🤖 LLM-based (Gemini)","#8b5cf6",
         "14 287 offres 'Divers IT' → Gemini 2.5 Flash. "
         "Prompt numérique (1-42). Temperature=0. **~0,07 $.**",
         "python",
         "response = model.generate_content(\n    prompt,\n"
         "    generation_config=GenerationConfig(\n        temperature=0,\n        max_output_tokens=5)\n)"),
        ("5","🔗 Fusion finale","#10b981",
         "LEFT JOIN Auto + LLM sur `offer_id`. Priorité : Auto > LLM > Fallback.",
         "sql",
         "SELECT *,\n  CASE\n"
         "    WHEN job_type != 'Divers IT' THEN job_type    -- auto\n"
         "    WHEN gemini IS NOT NULL      THEN gemini      -- LLM\n"
         "    ELSE 'Ingénieur IT Généraliste'               -- fallback\n"
         "  END AS job_type_FINAL\nFROM jobs_classified\nLEFT JOIN gemini_results USING (offer_id);"),
    ]

    for num,title,color,desc,lang,code in steps:
        with st.expander(f"**Étape {num} — {title}**", expanded=(num=="1")):
            c1,c2 = st.columns([1.2,1])
            with c1:
                st.markdown(
                    f"<div style='border-left:3px solid {color};padding:12px 16px;"
                    f"background:{SURFACE2};border-radius:0 8px 8px 0;'>"
                    f"<p style='color:{TEXT};font-size:0.83rem;line-height:1.75;margin:0;'>"
                    f"{desc}</p></div>", unsafe_allow_html=True)
            with c2:
                st.code(code, language=lang)


# ══════════════════════════════════════════════════════
#  TAB 4 — AUTO-CLASSIFICATION
# ══════════════════════════════════════════════════════
with tab4:

    st.markdown("### ⚡ Auto-classification — Non LLM-based")
    c1,c2,c3 = st.columns(3)
    c1.metric("Offres traitées",  "66 205")
    c2.metric("Auto-classifiées", "~52 000","≈ 80 %")
    c3.metric("Résidu LLM",       "14 287", "-21,6 %")
    st.markdown("---")

    st.info("""
    **Principe :** `REGEXP_CONTAINS(LOWER(matching_text), pattern)`

    `matching_text` = **job_title × 2** + **skills × 2** + description + profile + experience

    Coût : **0 $** · Vitesse : **< 5 secondes** · Méthode : **Non LLM-based**
    """)

    st.markdown("#### 📐 Règles CASE WHEN")
    rules = [
        ("1","Consultant SAP","#f59e0b",
         [r"\bsap\b","abap","s/4hana","sap hana"],
         "SAP en premier — très spécifique."),
        ("2","Cybersécurité","#ec4899",
         ["cybersécurité","pentest",r"\bsoc\b","siem","iso 27001"],
         "Mots très spécifiques → faible collision."),
        ("3","Data Scientist / IA","#6366f1",
         ["data scientist","machine learning","tensorflow","pytorch"],
         "Avant Python — 'python' seul trop générique."),
        ("4","DevOps / SRE","#10b981",
         [r"\bdevops\b","terraform","kubernetes","ci/cd","docker"],
         "Combinaison pour éviter les faux positifs Docker."),
        ("5","Développeur Java","#22c55e",
         [r"\bjava\b","spring boot",r"\bhibernate\b"],
         r"\bjava\b → évite 'javascript'."),
    ]
    for num,cat,color,kws,note in rules:
        with st.expander(f"Règle {num} — **{cat}**"):
            c1,c2 = st.columns([1,1.2])
            with c1:
                st.markdown(
                    f"<div style='border-left:3px solid {color};padding:10px 14px;"
                    f"background:{SURFACE2};border-radius:0 8px 8px 0;margin-bottom:10px;'>"
                    f"<p style='color:{MUTED2};font-size:0.77rem;line-height:1.65;margin:0;'>"
                    f"💡 {note}</p></div>", unsafe_allow_html=True)
                kw_html = "".join(
                    f"<code style='background:rgba(99,102,241,.15);color:#818cf8;"
                    f"padding:2px 8px;border-radius:5px;font-size:0.71rem;margin:2px;'>{k}</code>"
                    for k in kws)
                st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:4px;'>{kw_html}</div>",
                            unsafe_allow_html=True)
            with c2:
                st.code(
                    f"WHEN REGEXP_CONTAINS(LOWER(matching_text),\n"
                    f"     r'{chr(124).join(kws)}')\n"
                    f"THEN '{cat}'", language="sql")

    st.markdown("---")
    ca2,cl2 = st.columns(2)
    with ca2:
        st.success("""**✅ Avantages Non LLM-based**
- Gratuit — 0 $ · Instantané < 5 s
- Déterministe · Traçable · Scalable
- +1 règle = +1 ligne SQL""")
    with cl2:
        st.error("""**❌ Limites → nécessite LLM-based**
- Contexte ignoré
- Titres ambigus non résolus
- Nouveaux rôles non prévus""")


# ══════════════════════════════════════════════════════
#  TAB 5 — LLM-BASED
# ══════════════════════════════════════════════════════
with tab5:

    st.markdown("### 🤖 LLM-based vs Non LLM-based")

    cc1,cc2 = st.columns(2)
    with cc1:
        st.markdown(f"""
        <div style='background:{SURFACE};border:1px solid #6366f144;
                    border-radius:14px;padding:20px;height:100%;'>
            <div style='font-size:0.74rem;font-weight:800;text-transform:uppercase;
                        color:#818cf8;margin-bottom:12px;letter-spacing:.08em;'>
                🤖 LLM-BASED · Gemini 2.5 Flash
            </div>
            <div style='font-size:0.82rem;color:{TEXT};line-height:1.85;'>
                ✅ Comprend le <strong>contexte complet</strong><br>
                ✅ Titres ambigus résolus<br>
                ✅ Multilingue nativement<br>
                ✅ NON-IT détectés (cat. 42)<br>
                ✅ Nouveaux rôles compris<br>
                ⚠️ Coût : ~0,07 $ / 14 287 offres<br>
                ⚠️ Vitesse : ~94 offres/min
            </div>
        </div>""", unsafe_allow_html=True)
    with cc2:
        st.markdown(f"""
        <div style='background:{SURFACE};border:1px solid #3b82f644;
                    border-radius:14px;padding:20px;height:100%;'>
            <div style='font-size:0.74rem;font-weight:800;text-transform:uppercase;
                        color:#60a5fa;margin-bottom:12px;letter-spacing:.08em;'>
                ⚡ NON LLM-BASED · Auto-classification SQL
            </div>
            <div style='font-size:0.82rem;color:{TEXT};line-height:1.85;'>
                ✅ <strong>Coût zéro</strong> — 0 $<br>
                ✅ <strong>Instantané</strong> — &lt; 5 secondes<br>
                ✅ Déterministe · Traçable<br>
                ✅ Scalable (BigQuery)<br>
                ✅ Maintenable facilement<br>
                ❌ Contexte ignoré<br>
                ❌ Titres ambigus non résolus
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    params = [
        ("Modèle","gemini-2.5-flash","Rapide et économique"),
        ("Temperature","0","100 % déterministe"),
        ("max_output_tokens","5","Juste le numéro"),
        ("Offres","14 287","Résidu Non LLM"),
        ("Vitesse","~94 / min","Pause 0,1 s"),
        ("Durée","~160 min","2h40"),
        ("Coût","~0,07 $","600 tokens × 14 287"),
        ("Safety","BLOCK_NONE","Évite blocages"),
        ("Pause","0,1 sec","Quotas API"),
    ]
    cols = st.columns(3)
    for i,(lbl,val,hlp) in enumerate(params):
        with cols[i%3]:
            st.metric(lbl, val, help=hlp)

    st.markdown("---")
    st.markdown("#### 📊 Résultats LLM-based — 14 287 offres")

    gc1,gc2 = st.columns([1,1.2])
    with gc1:
        gem_df = pd.DataFrame({
            "Résultat":["✅ IT classifiées","🔴 NON-IT","⚠️ Fallback"],
            "Offres":  [9500,3574,1213],
        })
        fig = px.pie(gem_df, names="Résultat", values="Offres",
                     color="Résultat",
                     color_discrete_map={"✅ IT classifiées":"#10b981",
                                         "🔴 NON-IT":"#ef4444","⚠️ Fallback":"#f59e0b"},
                     hole=0.60)
        fig.update_traces(
            textposition="outside", textfont_size=11,
            marker=dict(line=dict(color=BG,width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>",
        )
        fig.update_layout(**dark_layout(
            showlegend=True,
            legend=dict(font=dict(color=MUTED2,size=11),bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=20,b=20,l=20,r=20),
        ))
        pchart(fig, 300)

    with gc2:
        for label,val,pct,color in [
            ("✅ IT classifiées", 9500, 66.5,"#10b981"),
            ("🔴 NON-IT",        3574, 25.0,"#ef4444"),
            ("⚠️ Fallback",       1213,  8.5,"#f59e0b"),
        ]:
            st.markdown(
                f"<div style='background:{SURFACE};border:1px solid {BORDER};"
                f"border-radius:10px;padding:14px;margin-bottom:10px;'>"
                f"<div style='font-size:0.73rem;color:{MUTED};margin-bottom:3px;'>{label}</div>"
                f"<div style='font-size:1.35rem;font-weight:900;color:{color};'>{val:,}</div>"
                f"<div style='font-size:0.67rem;color:{MUTED};margin-bottom:7px;'>{pct} %</div>"
                f"<div style='height:5px;background:{BORDER};border-radius:3px;overflow:hidden;'>"
                f"<div style='width:{pct}%;height:100%;background:{color};border-radius:3px;'>"
                f"</div></div></div>",
                unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔄 Code — Retry + Fallback Non LLM")
    st.code("""
def classifier_llm(job_title, texte, retry=0):
    \"\"\"LLM-based : Gemini 2.5 Flash\"\"\"
    if retry > 3:
        return classifier_non_llm(job_title)   # → Non LLM fallback

    try:
        response = model.generate_content(
            construire_prompt(job_title, texte),
            generation_config=GenerationConfig(
                temperature=0,
                max_output_tokens=5,
            )
        )
        nums = re.findall(r'\\b(\\d{1,2})\\b', response.text.strip())
        if nums and int(nums[0]) in categories_dict:
            return categories_dict[int(nums[0])]
        return classifier_non_llm(job_title)

    except Exception as e:
        if "429" in str(e):
            time.sleep(extraire_delai(e) + 10)
            return classifier_llm(job_title, texte, retry + 1)
        return classifier_non_llm(job_title)


def classifier_non_llm(job_title):
    \"\"\"Non LLM-based : regex sur job_title (fallback rapide)\"\"\"
    titre = str(job_title).lower()
    regles = [
        ("Chef de Projet IT",    [r'chef de projet', r'project manager']),
        ("DevOps / SRE",         [r'devops', r'platform engineer']),
        ("Cybersécurité",        [r'security analyst', r'\\biam\\b']),
        ("DBA / Base de données",[r'\\bdba\\b', r'database admin']),
        ("Ingénieur Logiciel",   [r'software engineer']),
    ]
    for categorie, patterns in regles:
        for p in patterns:
            if re.search(p, titre):
                return categorie
    return 'Ingénieur IT Généraliste'
""", language="python")

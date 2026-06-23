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
#  THEME TOGGLE
# ════════════════════════════════════════════════════════════
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# Couleurs selon le thème
def T(dark_val, light_val):
    return dark_val if st.session_state.dark_mode else light_val

BG        = T("#0f1117", "#f8fafc")
SURFACE   = T("#1a1f2e", "#ffffff")
SURFACE2  = T("#1e2538", "#f1f5f9")
BORDER    = T("#2a3347", "#e2e8f0")
TEXT      = T("#e2e8f0", "#0f172a")
MUTED     = T("#64748b", "#94a3b8")
MUTED2    = T("#94a3b8", "#475569")
PLOT_BG   = T("#1a1f2e", "#ffffff")
GRID_COL  = T("#1e293b", "#e2e8f0")

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{ background:{BG}; }}
[data-testid="stSidebar"]          {{ background:{T("#0d1117","#f1f5f9")}; border-right:1px solid {BORDER}; }}
[data-testid="metric-container"]   {{
    background:{SURFACE}; border:1px solid {BORDER};
    border-radius:12px; padding:16px;
}}
[data-testid="metric-container"] label {{
    color:{MUTED} !important; font-size:0.72rem !important;
}}
[data-testid="stMetricValue"] {{
    color:{T("#818cf8","#4f46e5")} !important;
    font-size:1.8rem !important; font-weight:900 !important;
}}
h1  {{ color:{T("#f1f5f9","#0f172a")} !important; }}
h2  {{ color:{T("#e2e8f0","#1e293b")} !important; font-size:1.1rem !important; }}
h3  {{ color:{T("#cbd5e1","#334155")} !important; font-size:0.95rem !important; }}
p, li, td, th {{ color:{TEXT}; }}
[data-testid="stTabs"] button {{
    color:{MUTED}; font-weight:600; font-size:0.82rem;
}}
[data-testid="stTabs"] button[aria-selected="true"] {{
    color:{T("#818cf8","#4f46e5")} !important;
    border-bottom:2px solid {T("#6366f1","#4f46e5")} !important;
}}
[data-testid="stExpander"] {{
    background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px;
}}
[data-testid="stDataFrame"] {{
    border:1px solid {BORDER}; border-radius:10px;
}}
hr {{ border-color:{BORDER} !important; }}
code {{
    background:{SURFACE2} !important;
    color:{T("#a5f3fc","#0369a1")} !important;
    border-radius:4px; padding:1px 5px;
}}
.stAlert {{ border-radius:10px; }}
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
    return f"rgb({int(np.clip(round(r),0,255))},{int(np.clip(round(g),0,255))},{int(np.clip(round(b),0,255))})"

def jitter_hex(hex_color, amount=0.07):
    r, g, b = mcolors.hex2color(hex_color)
    r = r*255 + np.random.uniform(-amount*255, amount*255)
    g = g*255 + np.random.uniform(-amount*255, amount*255)
    b = b*255 + np.random.uniform(-amount*255, amount*255)
    return safe_rgb(r, g, b)

def card(content_html, border_color="#6366f1"):
    st.markdown(f"""
    <div style='background:{SURFACE};border:1px solid {BORDER};
                border-left:3px solid {border_color};
                border-radius:0 12px 12px 0;padding:16px 20px;margin-bottom:14px;'>
        {content_html}
    </div>""", unsafe_allow_html=True)


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
    # ── Toggle dark/light ────────────────────────────────
    st.markdown("## 🤖 Classification IT")
    st.markdown(f"**Projet Job Matching · 2025**")

    col_tog1, col_tog2 = st.columns([1,1])
    with col_tog1:
        if st.button("☀️ Light" if st.session_state.dark_mode else "🌙 Dark",
                     use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.divider()

    st.markdown("### 🔧 Filtres")
    fam_sel = st.selectbox("Famille métier",  ["Toutes"] + sorted(df["famille"].unique()))
    src_sel = st.selectbox(
        "Source classif.",
        ["Toutes", "Auto-classifié", "LLM-based", "Non LLM-based"]
    )
    top_n = st.slider("Top N catégories", 5, 40, 15, 5)

    st.divider()
    st.markdown("### 📊 Résumé")
    st.metric("Offres IT",  f"{TOTAL:,}".replace(",", " "))
    st.metric("Catégories", "40")
    st.metric("Familles",   "5")

    st.divider()
    auto_count = int(df[df["source"]=="Auto-classifié"]["count"].sum())
    llm_count  = int(df[df["source"]=="LLM-based"]["count"].sum())
    st.markdown(f"""
| Méthode | Offres | % |
|---------|--------|---|
| ⚡ Auto-classifié | {auto_count:,} | ~80 % |
| 🤖 LLM-based | {llm_count:,} | ~15 % |
| ⚠️ Fallback | 1 213 | ~5 % |
""")
    st.caption("💰 Coût LLM : ~0,07 $")
    st.caption("⏱️ Durée : ~160 min")
    st.caption("🚀 gemini-2.0-flash")


# ════════════════════════════════════════════════════════════
#  FILTRES
# ════════════════════════════════════════════════════════════
df_f = df.copy()
if fam_sel != "Toutes":
    df_f = df_f[df_f["famille"] == fam_sel]

# Gestion "Non LLM-based" = Auto-classifié
if src_sel == "LLM-based":
    df_f = df_f[df_f["source"] == "LLM-based"]
elif src_sel == "Non LLM-based":
    df_f = df_f[df_f["source"] == "Auto-classifié"]
elif src_sel == "Auto-classifié":
    df_f = df_f[df_f["source"] == "Auto-classifié"]

df_top = df_f.nlargest(top_n, "count")


# ════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════
header_bg  = T("linear-gradient(135deg,#1e1b4b,#1a1f2e)", "linear-gradient(135deg,#ede9fe,#f0f9ff)")
header_bdr = T("#334155", "#c7d2fe")
header_tag = T("#818cf8", "#4f46e5")
header_h1  = T("#f1f5f9", "#0f172a")
header_sub = T("#94a3b8", "#475569")

st.markdown(f"""
<div style='background:{header_bg};border:1px solid {header_bdr};
            border-radius:16px;padding:28px 32px;margin-bottom:24px;'>
    <div style='font-size:0.72rem;color:{header_tag};text-transform:uppercase;
                letter-spacing:.1em;margin-bottom:8px;'>
        📋 RAPPORT TECHNIQUE · JOB MATCHING IT · 2025
    </div>
    <h1 style='font-size:2rem;font-weight:900;color:{header_h1};margin:0 0 8px;'>
        Classification Automatique des Offres IT
    </h1>
    <p style='color:{header_sub};font-size:0.88rem;margin:0;'>
        Pipeline hybride · Auto-classification par règles + LLM-based (Gemini) · 66 205 offres · 40 catégories
    </p>
</div>
""", unsafe_allow_html=True)

# KPIs
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("📦 Offres analysées",      "66 205", help="Dataset brut")
k2.metric("✅ Offres IT classifiées", "50 121", "75,71 %")
k3.metric("🗂️ Catégories IT",          "40",    help="Métiers identifiés")
k4.metric("⚡ Auto-classifié",          "~80 %", help="Règles regex BigQuery — 0 $ de coût")
k5.metric("💰 Coût LLM",               "0,07 $",help="14 287 offres Gemini 2.0 Flash")
st.divider()


# ════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
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
        bg_pill = T(f"rgba(255,255,255,.04)", f"rgba(0,0,0,.03)")
        with pills[i]:
            st.markdown(f"""
            <div style='background:{bg_pill};border:1px solid {c}44;
                        border-radius:12px;padding:16px;text-align:center;'>
                <div style='font-size:1.6rem;'>{ic}</div>
                <div style='font-size:0.64rem;font-weight:800;text-transform:uppercase;
                            color:{c};margin:6px 0 2px;'>{row.famille}</div>
                <div style='font-size:1.25rem;font-weight:900;color:{c};'>{row.count:,}</div>
                <div style='font-size:0.67rem;color:{MUTED};'>{row.pct} %</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Donuts
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
        # Sources renommées
        src_labels = {
            "Auto-classifié": "⚡ Auto-classifié",
            "LLM-based":      "🤖 LLM-based",
        }
        src_df = (df.groupby("source")["count"].sum().reset_index()
                    .assign(label=lambda x: x["source"].map(src_labels)))
        fig = px.pie(src_df, names="label", values="count",
                     color="label",
                     color_discrete_map={
                         "⚡ Auto-classifié":"#3b82f6",
                         "🤖 LLM-based":     "#6366f1",
                     },
                     hole=0.65, title="Méthode de classification")
        fig.update_traces(
            textposition="outside", textfont_size=11,
            marker=dict(line=dict(color=BG,width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,} offres<br>%{percent}<extra></extra>",
        )
        fig.update_layout(**dark_layout(
            showlegend=True,
            legend=dict(font=dict(size=11,color=MUTED2),bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=50,b=20,l=20,r=120),
            title=dict(font=dict(color=T("#cbd5e1","#334155"),size=13)),
        ))
        pchart(fig, 340)

    st.markdown("---")

    # Top N
    st.markdown(f"### Top {top_n} catégories IT")
    color_src = df_top["source"].map({"Auto-classifié":"#3b82f6","LLM-based":"#6366f1"})
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
        marker=dict(line=dict(width=0)),
        marker_cornerradius=4,
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

    # All 40
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

    # Treemap
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

    # Tableau
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
        def color_func(word, **kw):
            return jitter_hex(FAM_COLORS.get(fam_map.get(word,"Data & IA"),"#6366f1"), 0.07)
        wc = WordCloud(
            width=1400, height=580, background_color=T("#1a1f2e","#f8fafc"),
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
            "GitLab":2100,"GCP":1100,"ArgoCD":700,"Helm":800,
            "Machine Learning":4800,"TensorFlow":2600,"PyTorch":2400,
            "Apache Spark":2000,"Kafka":1800,"Airflow":1600,
            "Databricks":1400,"Power BI":3200,"BigQuery":1100,
            "LLM":1900,"Scikit-learn":1300,"MLflow":700,"dbt":600,
            "Pandas":2000,"NumPy":1600,"Tableau":900,
            "SAP":4000,"ABAP":1700,"S/4HANA":1400,"Pentest":1100,
            "SIEM":850,"ISO 27001":1000,"Salesforce":1200,
            "Scrum":2600,"Agile":3000,"ITIL":900,"SOC":750,
        }
        _d="#6366f1"; _l="#10b981"; _c="#f59e0b"; _f="#3b82f6"; _e="#ec4899"
        color_map = {
            **dict.fromkeys(["Machine Learning","TensorFlow","PyTorch","Apache Spark",
                              "Kafka","Airflow","Databricks","Power BI","BigQuery","LLM",
                              "Scikit-learn","dbt","Pandas","NumPy","Tableau","SQL","MLflow"],_d),
            **dict.fromkeys(["Python","Java","JavaScript","TypeScript","C++","PHP","C#","Go","Kotlin"],_l),
            **dict.fromkeys(["Docker","Kubernetes","Terraform","AWS","Azure","CI/CD",
                              "Jenkins","Ansible","GitLab","GCP","ArgoCD","Helm"],_c),
            **dict.fromkeys(["Spring Boot","React","Angular","Vue.js","Node.js",
                              "Django","FastAPI",".NET"],_f),
            **dict.fromkeys(["SAP","ABAP","S/4HANA","Pentest","SIEM","ISO 27001",
                              "Salesforce","Scrum","Agile","ITIL","SOC"],_e),
        }
        def color_func(word, **kw):
            return jitter_hex(color_map.get(word,"#64748b"), 0.07)
        wc = WordCloud(
            width=1400, height=580, background_color=T("#1a1f2e","#f8fafc"),
            max_words=80, prefer_horizontal=0.70,
            color_func=color_func, margin=10,
            relative_scaling=0.55, min_font_size=10,
        ).generate_from_frequencies(tech_freq)
        return render_wc(wc)

    dark_flag = st.session_state.dark_mode

    if wc_choice == "Catégories IT (par volume)":
        st.info("💡 La **taille** est proportionnelle au nombre d'offres. La **couleur** correspond à la famille.")
        st.image(wc_categories(dark_flag), use_column_width=True)
        leg = st.columns(5)
        for i,(fam,color) in enumerate(FAM_COLORS.items()):
            with leg[i]:
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:6px;font-size:0.73rem;color:{MUTED2};'>"
                    f"<div style='width:12px;height:12px;border-radius:3px;background:{color};'></div>"
                    f"{FAM_ICONS.get(fam,'🔵')} {fam}</div>",
                    unsafe_allow_html=True)
    else:
        st.info("💡 Technologies et mots-clés détectés par les règles d'auto-classification.")
        st.image(wc_tech(dark_flag), use_column_width=True)
        for color,label in [("#6366f1","Data & IA"),("#10b981","Langages"),
                             ("#f59e0b","Cloud & DevOps"),("#3b82f6","Frameworks"),
                             ("#ec4899","ERP / Sécu")]:
            st.markdown(
                f"<span style='display:inline-flex;align-items:center;gap:5px;"
                f"font-size:0.72rem;color:{MUTED2};margin-right:16px;'>"
                f"<span style='width:10px;height:10px;border-radius:3px;"
                f"background:{color};display:inline-block;'></span>{label}</span>",
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
        {"tech":"Agile/Scrum",     "freq":3000,"cat":"ERP / Sécu"},
        {"tech":"Spring Boot",     "freq":3000,"cat":"Frameworks"},
        {"tech":"CI/CD",           "freq":2900,"cat":"Cloud & DevOps"},
        {"tech":"React",           "freq":2800,"cat":"Frameworks"},
        {"tech":"Terraform",       "freq":2700,"cat":"Cloud & DevOps"},
        {"tech":"TensorFlow",      "freq":2600,"cat":"Data & IA"},
    ]).sort_values("freq")
    fig = px.bar(tech_df, x="freq", y="tech", orientation="h",
                 color="cat",
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
         "Le CSV avait des **sauts de ligne** dans les descriptions et des **virgules** dans le texte. "
         "Conversion en Parquet binaire via PyArrow + Snappy. Zéro problème d'encodage.",
         "python","df.to_parquet('jobs.parquet', engine='pyarrow',\n    compression='snappy', index=False)"),
        ("2","☁️ GCS Upload","#6366f1",
         "Upload vers `gs://jobmatching/`. Sert de source BigQuery et de backup du dataset brut.",
         "bash","gsutil cp jobs_for_bigquery.parquet gs://jobmatching/"),
        ("3","⚡ Auto-classification (BigQuery)","#10b981",
         "Règles `REGEXP_CONTAINS` sur `matching_text`. CASE WHEN hiérarchique. "
         "**~52 000 offres en quelques secondes, coût : 0 $.**",
         "sql",
         "CREATE OR REPLACE TABLE jobs_classified AS\nSELECT *,\n  CASE\n"
         "    WHEN REGEXP_CONTAINS(LOWER(matching_text),\n"
         "         r'\\bsap\\b|abap|s/4hana') THEN 'Consultant SAP'\n"
         "    ...\n    ELSE 'Divers IT'\n  END AS job_type\nFROM jobs_raw;"),
        ("4","🤖 LLM-based (Gemini)","#8b5cf6",
         "Les **14 287** offres 'Divers IT' envoyées à Gemini 2.0 Flash. "
         "Prompt numérique (1-42). Temperature=0. Coût : **~0,07 $**.",
         "python",
         "response = model.generate_content(\n    prompt,\n"
         "    generation_config=GenerationConfig(\n"
         "        temperature=0, max_output_tokens=5)\n)"),
        ("5","🔗 Fusion finale","#10b981",
         "LEFT JOIN Auto-classifié + LLM-based sur `offer_id`. "
         "Priorité : Auto > LLM > Fallback. Colonne `source_classif` pour la traçabilité.",
         "sql",
         "SELECT *,\n  CASE\n"
         "    WHEN job_type != 'Divers IT' THEN job_type   -- auto\n"
         "    WHEN gemini IS NOT NULL      THEN gemini     -- LLM\n"
         "    ELSE 'Ingénieur IT Généraliste'              -- fallback\n"
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

    st.markdown("---")
    st.markdown("### 📊 Comparaison des méthodes")
    cmp_df = pd.DataFrame({
        "Méthode":   ["⚡ Auto-classifié","🤖 LLM-based","⚠️ Fallback"],
        "Offres":    [52000, 9500, 1213],
        "Coût":      ["0 $","~0,07 $","0 $"],
        "Vitesse":   ["< 5 sec","~160 min","< 1 sec"],
    })
    fig = px.bar(cmp_df, x="Méthode", y="Offres", color="Méthode",
                 color_discrete_sequence=["#3b82f6","#6366f1","#f59e0b"],
                 text="Offres", title="Offres traitées par méthode",
                 custom_data=["Coût","Vitesse"])
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        marker=dict(line=dict(width=0)), marker_cornerradius=6,
        hovertemplate="<b>%{x}</b><br>Offres : %{y:,}<br>Coût : %{customdata[0]}<br>Vitesse : %{customdata[1]}<extra></extra>",
    )
    fig.update_layout(**dark_layout(
        showlegend=False,
        margin=dict(t=50,b=20,l=20,r=20),
        title=dict(font=dict(color=T("#cbd5e1","#334155"),size=13)),
        xaxis=dict(title="",gridcolor=GRID_COL,zerolinecolor=GRID_COL),
        yaxis=dict(title="Nombre d'offres",gridcolor=GRID_COL,zerolinecolor=GRID_COL),
    ))
    pchart(fig, 340)

    # Tableau comparatif
    st.dataframe(cmp_df, width="stretch", hide_index=True)


# ══════════════════════════════════════════════════════
#  TAB 4 — AUTO-CLASSIFICATION
# ══════════════════════════════════════════════════════
with tab4:

    st.markdown("### ⚡ Auto-classification — Règles BigQuery")

    c1,c2,c3 = st.columns(3)
    c1.metric("Offres traitées",    "66 205")
    c2.metric("Auto-classifiées",   "~52 000","≈ 80 %")
    c3.metric("Résidu LLM-based",   "14 287", "-21,6 %")

    st.markdown("---")

    st.info("""
    **Principe :** `REGEXP_CONTAINS(LOWER(matching_text), pattern)`

    Le champ `matching_text` = **job_title × 2** + **skills × 2** + description + profile_required + experience

    Doubler le titre et les skills leur donne plus de **poids** dans la détection.
    Coût total : **0 $** · Vitesse : **< 5 secondes** sur 66 205 offres.
    """)

    st.markdown("#### 📐 Règles CASE WHEN — exemples")

    rules = [
        ("1","Consultant SAP","#f59e0b",
         [r"\bsap\b","abap","s/4hana","sap hana","sap fi","sap co"],
         "SAP en premier — très spécifique, évite les faux positifs."),
        ("2","Cybersécurité","#ec4899",
         ["cybersécurité","pentest",r"\bsoc\b","siem","iso 27001",r"\brssi\b"],
         "Mots très spécifiques → faible risque de collision."),
        ("3","Data Scientist / IA","#6366f1",
         ["data scientist","machine learning","deep learning","tensorflow","pytorch"],
         "Avant Développeur Python — 'python' seul est trop générique."),
        ("4","Intelligence Artificielle","#818cf8",
         [r"\bai\b",r"\bia\b","intelligence artificielle",r"\bllm\b","generative ai"],
         r"Après Data Scientist — évite que \bai\b capture des offres data classiques."),
        ("5","DevOps / SRE","#10b981",
         [r"\bdevops\b",r"\bsre\b","terraform","kubernetes","ci/cd","docker","ansible"],
         "Docker seul trop générique → combiné avec devops/sre."),
        ("6","Développeur Java","#22c55e",
         [r"\bjava\b","spring boot",r"\bhibernate\b",r"\bmaven\b"],
         r"\bjava\b avec word boundary obligatoire → évite 'javascript'."),
        ("7","Cloud AWS / Azure / GCP","#06b6d4",
         [r"\baws\b",r"\bec2\b",r"\bazure\b",r"\baks\b",r"\bgcp\b","bigquery"],
         "Trois règles séparées pour distinguer les providers."),
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
    st.markdown("#### ⚠️ Word boundaries `\\b` — essentiels")
    wb_df = pd.DataFrame({
        "Pattern":[r"\bsap\b",r"\bsoc\b",r"\bjava\b",r"\bai\b",r"\bdba\b"],
        "✅ Matche":["SAP HANA","SOC analyst","Java developer","AI engineer","DBA Oracle"],
        "❌ Évite":["kidnap, satrap","social","JavaScript","email, paid","sans \\b"],
    })
    st.dataframe(wb_df, width="stretch", hide_index=True)

    st.markdown("---")
    ca2,cl2 = st.columns(2)
    with ca2:
        st.success("""**✅ Avantages Auto-classification**
- Gratuit — 0 $ par offre
- Instantané — < 5 s sur 66 k offres
- Déterministe et traçable
- Maintenable : +1 mot-clé = 1 ligne SQL""")
    with cl2:
        st.error("""**❌ Limites → nécessite LLM-based**
- Contexte ignoré
- Titres ambigus non résolus
- Nouveaux rôles non prévus (MLOps...)
→ 14 287 offres envoyées au LLM""")


# ══════════════════════════════════════════════════════
#  TAB 5 — LLM-BASED
# ══════════════════════════════════════════════════════
with tab5:

    st.markdown("### 🤖 LLM-based vs Non LLM-based")

    # Vue comparative haut niveau
    comp_col1, comp_col2 = st.columns(2)

    with comp_col1:
        st.markdown(f"""
        <div style='background:{SURFACE};border:1px solid #6366f144;
                    border-radius:14px;padding:20px;'>
            <div style='font-size:0.75rem;font-weight:800;text-transform:uppercase;
                        color:#818cf8;margin-bottom:12px;letter-spacing:.08em;'>
                🤖 LLM-BASED (Gemini 2.0 Flash)
            </div>
            <div style='font-size:0.82rem;color:{TEXT};line-height:1.8;'>
                ✅ <strong>Comprend le contexte</strong> complet de l'offre<br>
                ✅ <strong>Titres ambigus</strong> résolus (Ingénieur d'études...)<br>
                ✅ <strong>Multilingue</strong> nativement<br>
                ✅ <strong>NON-IT détectés</strong> automatiquement (cat. 42)<br>
                ✅ <strong>Nouveaux rôles</strong> compris sans re-entraînement<br>
                ⚠️ Coût : ~0,07 $ pour 14 287 offres<br>
                ⚠️ Vitesse : ~94 offres/min
            </div>
        </div>""", unsafe_allow_html=True)

    with comp_col2:
        st.markdown(f"""
        <div style='background:{SURFACE};border:1px solid #3b82f644;
                    border-radius:14px;padding:20px;'>
            <div style='font-size:0.75rem;font-weight:800;text-transform:uppercase;
                        color:#60a5fa;margin-bottom:12px;letter-spacing:.08em;'>
                ⚡ NON LLM-BASED (Auto-classification SQL)
            </div>
            <div style='font-size:0.82rem;color:{TEXT};line-height:1.8;'>
                ✅ <strong>Coût zéro</strong> — 0 $ pour 52 000 offres<br>
                ✅ <strong>Instantané</strong> — < 5 secondes sur tout le dataset<br>
                ✅ <strong>Déterministe</strong> — même entrée = même sortie<br>
                ✅ <strong>Traçable</strong> — chaque règle auditable<br>
                ✅ <strong>Scalable</strong> — BigQuery gère des milliards de lignes<br>
                ❌ Contexte ignoré<br>
                ❌ Titres ambigus non résolus
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Bar comparatif Non LLM vs LLM
    st.markdown("#### 📊 Répartition des offres : Non LLM-based vs LLM-based")
    cmp2 = pd.DataFrame({
        "Méthode":["⚡ Non LLM-based\n(Auto-classifié)","🤖 LLM-based\n(Gemini)","⚠️ Fallback\n(titre seul)"],
        "Offres": [52000, 9500, 1213],
        "Coût $": [0, 0.07, 0],
        "Vitesse":["< 5 sec","~160 min","< 1 sec"],
        "Précision":["Haute (règles explicites)","Très haute (LLM)","Moyenne"],
    })
    fig = px.bar(
        cmp2, x="Méthode", y="Offres", color="Méthode",
        color_discrete_sequence=["#3b82f6","#6366f1","#f59e0b"],
        text="Offres", custom_data=["Coût $","Vitesse","Précision"],
        title="Non LLM-based vs LLM-based — volume d'offres traitées",
    )
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        marker=dict(line=dict(width=0)), marker_cornerradius=6,
        hovertemplate=(
            "<b>%{x}</b><br>Offres : %{y:,}<br>"
            "Coût : %{customdata[0]} $<br>"
            "Vitesse : %{customdata[1]}<br>"
            "Précision : %{customdata[2]}<extra></extra>"
        ),
    )
    fig.update_layout(**dark_layout(
        showlegend=False,
        margin=dict(t=50,b=20,l=20,r=20),
        title=dict(font=dict(color=T("#cbd5e1","#334155"),size=13)),
        xaxis=dict(title="",gridcolor=GRID_COL,zerolinecolor=GRID_COL),
        yaxis=dict(title="Offres",gridcolor=GRID_COL,zerolinecolor=GRID_COL),
    ))
    pchart(fig, 360)

    st.markdown("---")
    st.markdown("#### 🤖 Paramètres Gemini (LLM-based)")

    params = [
        ("Modèle","gemini-2.0-flash","Rapide et économique"),
        ("Temperature","0","100 % déterministe"),
        ("max_output_tokens","5","Juste le numéro '7'"),
        ("Offres traitées","14 287","Résidu Non LLM"),
        ("Vitesse","~94 / min","Avec pause 0,1 s"),
        ("Durée","~160 min","2h40 en continu"),
        ("Coût total","~0,07 $","~600 tokens × 14 287"),
        ("Safety","BLOCK_NONE","Évite blocages tech"),
        ("Pause","0,1 sec","Respecter les quotas"),
    ]
    cols = st.columns(3)
    for i,(lbl,val,hlp) in enumerate(params):
        with cols[i%3]:
            st.metric(lbl, val, help=hlp)

    st.markdown("---")
    st.markdown("#### 📊 Résultats LLM-based sur 14 287 offres")

    gc1,gc2 = st.columns([1,1.2])
    with gc1:
        gem_df = pd.DataFrame({
            "Résultat":["✅ Classifiées IT","🔴 NON-IT détectées","⚠️ Fallback"],
            "Offres":  [9500,3574,1213],
        })
        fig = px.pie(gem_df, names="Résultat", values="Offres",
                     color="Résultat",
                     color_discrete_map={"✅ Classifiées IT":"#10b981",
                                         "🔴 NON-IT détectées":"#ef4444",
                                         "⚠️ Fallback":"#f59e0b"},
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
            ("✅ Classifiées IT",   9500, 66.5,"#10b981"),
            ("🔴 NON-IT détectées",3574, 25.0,"#ef4444"),
            ("⚠️ Fallback",         1213,  8.5,"#f59e0b"),
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
    st.markdown("#### 🎯 Pourquoi LLM-based pour les cas ambigus ?")

    designs = [
        ("Réponse numérique (1-42)","#6366f1",
         "Gemini répond `'3'` → mappe sur la catégorie. Pas d'ambiguïté. "
         "Parsing trivial avec `re.findall(r'\\d{1,2}', response)`."),
        ("Temperature = 0","#10b981",
         "Même offre = même résultat. Essentiel pour la **reproductibilité** du dataset."),
        ("max_output_tokens = 5","#f59e0b",
         "Économie de ~60 % de tokens → coût ~0,07 $ pour 14 287 offres."),
        ("Catégorie 42 = NON-IT","#ec4899",
         "**3 574 NON-IT supplémentaires** détectés que le Non LLM-based avait manqués."),
        ("Texte limité à 300 chars","#3b82f6",
         "`matching_text[:300]` = titre×2 + skills×2. Économie de ~60 % de tokens."),
        ("Safety BLOCK_NONE","#06b6d4",
         "Évite les blocages sur 'pentest', 'exploit', 'injection'."),
    ]
    for title,color,desc in designs:
        with st.expander(f"**{title}**"):
            st.markdown(
                f"<div style='border-left:3px solid {color};padding:12px 16px;"
                f"background:{SURFACE2};border-radius:0 8px 8px 0;'>"
                f"<p style='color:{TEXT};font-size:0.83rem;line-height:1.75;margin:0;'>"
                f"{desc}</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔄 Code — Retry + Fallback vers Non LLM-based")
    st.code("""
def classifier_llm(job_title, texte, retry=0):
    \"\"\"LLM-based : Gemini 2.0 Flash\"\"\"
    if retry > 3:
        # Fallback vers Non LLM-based (regex sur titre)
        return classifier_non_llm(job_title)

    try:
        response = model.generate_content(
            construire_prompt(job_title, texte),
            generation_config=GenerationConfig(
                temperature=0,           # déterministe
                max_output_tokens=5,     # juste "7" ou "34"
            )
        )
        nums = re.findall(r'\\b(\\d{1,2})\\b', response.text.strip())
        if nums and int(nums[0]) in categories_dict:
            return categories_dict[int(nums[0])]
        return classifier_non_llm(job_title)   # fallback

    except Exception as e:
        if "429" in str(e):                    # quota dépassé
            time.sleep(extraire_delai(e) + 10)
            return classifier_llm(job_title, texte, retry + 1)
        return classifier_non_llm(job_title)   # fallback


def classifier_non_llm(job_title):
    \"\"\"Non LLM-based : regex sur job_title seul (fallback)\"\"\"
    titre = str(job_title).lower()
    regles = [
        ("Chef de Projet IT",   [r'chef de projet', r'project manager']),
        ("DevOps / SRE",        [r'devops', r'sre', r'platform engineer']),
        ("Cybersécurité",       [r'security analyst', r'\\biam\\b']),
        ("DBA / Base de données",[r'database admin', r'\\bdba\\b']),
        ("Ingénieur Logiciel",  [r'software engineer', r'software developer']),
    ]
    for categorie, patterns in regles:
        for p in patterns:
            if re.search(p, titre):
                return categorie
    return 'Ingénieur IT Généraliste'
""", language="python")

    st.warning("""
    **⚠️ Reprendre après interruption LLM-based :**
    Charger `gemini_temp.csv`, filtrer les `offer_id` déjà traités,
    reprendre avec `WRITE_APPEND`. Perte max = 500 offres ≈ 5 min.
    """)

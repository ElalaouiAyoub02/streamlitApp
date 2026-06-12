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

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background:#0f1117; }
[data-testid="stSidebar"]          { background:#0d1117; border-right:1px solid #1e293b; }
[data-testid="metric-container"]   {
    background:#1a1f2e; border:1px solid #2a3347; border-radius:12px; padding:16px;
}
[data-testid="metric-container"] label { color:#64748b !important; font-size:0.72rem !important; }
[data-testid="stMetricValue"]          { color:#818cf8 !important; font-size:1.8rem !important; font-weight:900 !important; }
h1 { color:#f1f5f9 !important; }
h2 { color:#e2e8f0 !important; font-size:1.1rem !important; }
h3 { color:#cbd5e1 !important; font-size:0.95rem !important; }
[data-testid="stTabs"] button { color:#64748b; font-weight:600; font-size:0.82rem; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color:#818cf8 !important; border-bottom:2px solid #6366f1 !important;
}
[data-testid="stExpander"] {
    background:#1a1f2e; border:1px solid #2a3347; border-radius:12px;
}
hr { border-color:#1e293b !important; }
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
    "Data & IA":"📊", "Conseil & Mgmt":"💼",
    "Développement":"💻", "Autres IT":"🔐", "Cloud & Infra":"☁️",
}

def dark_layout(**extra):
    """Base layout plotly dark — kwargs fusionnés sans collision."""
    base = dict(
        paper_bgcolor="#1a1f2e",
        plot_bgcolor="#1a1f2e",
        font=dict(color="#94a3b8", family="Segoe UI, system-ui, sans-serif"),
    )
    base.update(extra)
    return base

def pchart(fig, height=400):
    fig.update_layout(height=height)
    st.plotly_chart(fig, width="stretch")

def safe_rgb(r, g, b):
    """
    Clamp r, g, b dans [0, 255] (int) pour PIL.
    Évite ValueError: unknown color specifier 'rgb(x,y,-z)'.
    """
    r = int(np.clip(round(r), 0, 255))
    g = int(np.clip(round(g), 0, 255))
    b = int(np.clip(round(b), 0, 255))
    return f"rgb({r},{g},{b})"

def jitter_hex(hex_color, amount=0.08):
    """
    Applique un jitter aléatoire sur une couleur hex
    et retourne une chaîne rgb() sûre pour PIL/Pillow.
    """
    r, g, b = mcolors.hex2color(hex_color)   # valeurs float [0.0, 1.0]
    r = r * 255 + np.random.uniform(-amount * 255, amount * 255)
    g = g * 255 + np.random.uniform(-amount * 255, amount * 255)
    b = b * 255 + np.random.uniform(-amount * 255, amount * 255)
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
            "SQL","SQL","SQL","SQL","SQL","SQL","SQL","SQL","Gemini","SQL",
            "SQL","SQL","SQL","SQL","SQL","SQL","SQL","SQL","Gemini","SQL",
            "Gemini","SQL","SQL","Gemini","SQL","SQL","SQL","SQL","SQL","SQL",
            "Gemini","Gemini","SQL","SQL","Gemini","Gemini","SQL","Gemini","Gemini","Gemini",
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
    st.markdown("## 🤖 Classification IT")
    st.markdown("**Projet Job Matching · 2026**")
    st.divider()

    st.markdown("### 🔧 Filtres")
    fam_sel = st.selectbox("Famille métier",  ["Toutes"] + sorted(df["famille"].unique()))
    src_sel = st.selectbox("Source classif.", ["Toutes"] + sorted(df["source"].unique()))
    top_n   = st.slider("Top N catégories", 5, 40, 15, 5)

    st.divider()
    st.markdown("### 📊 Résumé")
    st.metric("Offres IT",  f"{TOTAL:,}".replace(",", " "))
    st.metric("Catégories", "40")
    st.metric("Familles",   "5")

    st.divider()
    st.markdown("""
| Étape | % |
|-------|---|
| 🔍 SQL | ~80 % |
| 🤖 Gemini | ~15 % |
| ⚠️ Fallback | ~5 % |
""")
    st.caption("💰 Coût Gemini : ~0,07 $")
    st.caption("⏱️ Durée : ~160 min")
    st.caption("🚀 gemini-2.0-flash")


# ════════════════════════════════════════════════════════════
#  FILTRES APPLIQUÉS
# ════════════════════════════════════════════════════════════
df_f = df.copy()
if fam_sel != "Toutes":
    df_f = df_f[df_f["famille"] == fam_sel]
if src_sel != "Toutes":
    df_f = df_f[df_f["source"] == src_sel]
df_top = df_f.nlargest(top_n, "count")


# ════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════
st.markdown("""
<div style='background:linear-gradient(135deg,#1e1b4b,#1a1f2e);
            border:1px solid #334155;border-radius:16px;padding:28px 32px;margin-bottom:24px;'>
    <div style='font-size:0.72rem;color:#818cf8;text-transform:uppercase;
                letter-spacing:.1em;margin-bottom:8px;'>
        📋 RAPPORT TECHNIQUE · JOB MATCHING IT · 2026
    </div>
    <h1 style='font-size:2rem;font-weight:900;color:#f1f5f9;margin:0 0 8px;'>
        Classification Automatique des Offres IT
    </h1>
    <p style='color:#94a3b8;font-size:0.88rem;margin:0;'>
        Pipeline hybride BigQuery SQL + Google Gemini API · 66 205 offres · 40 catégories
    </p>
</div>
""", unsafe_allow_html=True)

# KPIs
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("📦 Offres analysées",     "66 205", help="Dataset brut")
k2.metric("✅ Offres IT classifiées","50 121", "75,71 %")
k3.metric("🗂️ Catégories IT",        "40",     help="Métiers identifiés")
k4.metric("🔍 Couverture SQL",        "~80 %",  help="Classifiées par regex BigQuery")
k5.metric("💰 Coût Gemini",           "0,07 $", help="14 287 offres Gemini 2.5 Flash")
st.divider()


# ════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribution",
    "☁️ Nuage de mots",
    "⚙️ Pipeline",
    "🔍 SQL",
    "🤖 Gemini",
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
        c = FAM_COLORS.get(row.famille, "#6366f1")
        ic = FAM_ICONS.get(row.famille, "🔵")
        with pills[i]:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,.04);border:1px solid {c}44;
                        border-radius:12px;padding:16px;text-align:center;'>
                <div style='font-size:1.6rem;'>{ic}</div>
                <div style='font-size:0.64rem;font-weight:800;text-transform:uppercase;
                            color:{c};margin:6px 0 2px;'>{row.famille}</div>
                <div style='font-size:1.25rem;font-weight:900;color:{c};'>{row.count:,}</div>
                <div style='font-size:0.67rem;color:#64748b;'>{row.pct} %</div>
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
            marker=dict(line=dict(color="#0f1117", width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,} offres<br>%{percent}<extra></extra>",
        )
        fig.update_layout(**dark_layout(
            showlegend=True,
            legend=dict(font=dict(size=11,color="#94a3b8"),bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=50,b=20,l=20,r=100),
            title=dict(font=dict(color="#cbd5e1",size=13)),
        ))
        fig.add_annotation(text=f"<b>{TOTAL:,}</b><br>offres IT",
                           x=0.5, y=0.5, showarrow=False,
                           font=dict(size=13, color="#e2e8f0"))
        pchart(fig, 340)

    with cb:
        src_df = (df.groupby("source")["count"].sum().reset_index()
                    .assign(pct=lambda x:(x["count"]/TOTAL*100).round(1)))
        fig = px.pie(src_df, names="source", values="count",
                     color="source",
                     color_discrete_map={"SQL":"#3b82f6","Gemini":"#6366f1","Fallback":"#f59e0b"},
                     hole=0.65, title="Sources de classification")
        fig.update_traces(
            textposition="outside", textfont_size=11,
            marker=dict(line=dict(color="#0f1117",width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,} offres<br>%{percent}<extra></extra>",
        )
        fig.update_layout(**dark_layout(
            showlegend=True,
            legend=dict(font=dict(size=11,color="#94a3b8"),bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=50,b=20,l=20,r=100),
            title=dict(font=dict(color="#cbd5e1",size=13)),
        ))
        pchart(fig, 340)

    st.markdown("---")

    # Top N
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
        textfont=dict(size=10,color="#94a3b8"),
        marker=dict(line=dict(width=0)),
        marker_cornerradius=4,
        hovertemplate=(
            "<b>%{y}</b><br>Offres : <b>%{x:,}</b><br>"
            "Part : <b>%{customdata[0]} %</b><br>"
            "Famille : %{customdata[2]}<br>"
            "Source : %{customdata[1]}<extra></extra>"
        ),
    )
    fig.update_layout(**dark_layout(
        showlegend=True,
        legend=dict(title=dict(text="Famille",font=dict(color="#64748b",size=11)),
                    font=dict(color="#94a3b8",size=11),bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=50,b=20,l=210,r=80),
        title=dict(font=dict(color="#cbd5e1",size=13)),
        xaxis=dict(title="Nombre d'offres",gridcolor="#1e293b",zerolinecolor="#1e293b"),
        yaxis=dict(title="",tickfont=dict(size=11),gridcolor="#1e293b"),
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
            "Source : %{customdata[1]}<extra></extra>"
        ),
    )
    fig.update_layout(**dark_layout(
        showlegend=True,
        legend=dict(title=dict(text="Famille",font=dict(color="#64748b",size=11)),
                    font=dict(color="#94a3b8",size=11),bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=50,b=20,l=230,r=40),
        title=dict(font=dict(color="#cbd5e1",size=13)),
        xaxis=dict(title="Nombre d'offres",gridcolor="#1e293b",zerolinecolor="#1e293b"),
        yaxis=dict(title="",tickfont=dict(size=10),gridcolor="#1e293b"),
    ))
    pchart(fig, 860)

    st.markdown("---")

    # Treemap
    st.markdown("### Treemap — Vue proportionnelle")
    fig = px.treemap(
        df, path=["famille","job_type"], values="count",
        color="famille", color_discrete_map=FAM_COLORS,
        custom_data=["pct"],
        title="Répartition hiérarchique : Famille → Catégorie",
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Offres : %{value:,}<br>%{customdata[0]} %<extra></extra>",
        textfont=dict(size=11), marker=dict(cornerradius=4),
    )
    fig.update_layout(**dark_layout(
        margin=dict(t=50,b=10,l=10,r=10),
        title=dict(font=dict(color="#cbd5e1",size=13)),
    ))
    pchart(fig, 480)

    st.markdown("---")

    # Tableau
    st.markdown("### 📋 Tableau détaillé")
    df_show = df_f.sort_values("count", ascending=False).reset_index(drop=True)
    df_show.index += 1
    df_show.columns = ["Catégorie","Offres","Source","Famille","Part (%)"]
    st.dataframe(
        df_show, width="stretch", height=400,
        column_config={
            "Offres":   st.column_config.NumberColumn(format="%d"),
            "Part (%)": st.column_config.ProgressColumn(
                format="%.2f %%", min_value=0, max_value=float(df["pct"].max())),
        },
    )
    st.download_button(
        "⬇️ Télécharger CSV",
        df_f.to_csv(index=False).encode("utf-8"),
        "distribution_it.csv", "text/csv",
    )


# ══════════════════════════════════════════════════════
#  TAB 2 — NUAGE DE MOTS
# ══════════════════════════════════════════════════════
with tab2:

    st.markdown("### ☁️ Nuages de mots")
    wc_choice = st.radio(
        "Choisir le nuage",
        ["Catégories IT (par volume)", "Technologies & mots-clés SQL"],
        horizontal=True,
    )

    # ── helper commun pour rendre un WordCloud en PNG ──────────
    def render_wc(wc_obj):
        """Convertit un objet WordCloud en BytesIO PNG pour st.image."""
        fig, ax = plt.subplots(figsize=(14, 5.8))
        fig.patch.set_facecolor("#1a1f2e")
        ax.set_facecolor("#1a1f2e")
        ax.imshow(wc_obj.to_array(), interpolation="bilinear")
        ax.axis("off")
        plt.tight_layout(pad=0)
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=150,
                    bbox_inches="tight", facecolor="#1a1f2e")
        plt.close(fig)
        buf.seek(0)
        return buf

    # ── WordCloud catégories ───────────────────────────────────
    @st.cache_data
    def wc_categories():
        freq    = dict(zip(df["job_type"], df["count"]))
        fam_map = dict(zip(df["job_type"], df["famille"]))

        def color_func(word, **kw):
            hex_c = FAM_COLORS.get(fam_map.get(word, "Data & IA"), "#6366f1")
            return jitter_hex(hex_c, amount=0.07)

        wc = WordCloud(
            width=1400, height=580,
            background_color="#1a1f2e",
            max_words=60,
            prefer_horizontal=0.75,
            color_func=color_func,
            margin=12,
            relative_scaling=0.6,
            min_font_size=10,
        ).generate_from_frequencies(freq)

        return render_wc(wc)

    # ── WordCloud technologies ─────────────────────────────────
    @st.cache_data
    def wc_tech():
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

        # mapping mot → couleur hex
        _data   = "#6366f1"
        _lang   = "#10b981"
        _cloud  = "#f59e0b"
        _fw     = "#3b82f6"
        _erp    = "#ec4899"

        color_map = {
            **dict.fromkeys(["Machine Learning","TensorFlow","PyTorch","Apache Spark",
                              "Kafka","Airflow","Databricks","Power BI","BigQuery","LLM",
                              "Scikit-learn","dbt","Pandas","NumPy","Tableau","SQL","MLflow"], _data),
            **dict.fromkeys(["Python","Java","JavaScript","TypeScript","C++",
                              "PHP","C#","Go","Kotlin"], _lang),
            **dict.fromkeys(["Docker","Kubernetes","Terraform","AWS","Azure","CI/CD",
                              "Jenkins","Ansible","GitLab","GCP","ArgoCD","Helm"], _cloud),
            **dict.fromkeys(["Spring Boot","React","Angular","Vue.js","Node.js",
                              "Django","FastAPI",".NET"], _fw),
            **dict.fromkeys(["SAP","ABAP","S/4HANA","Pentest","SIEM","ISO 27001",
                              "Salesforce","Scrum","Agile","ITIL","SOC"], _erp),
        }

        def color_func(word, **kw):
            return jitter_hex(color_map.get(word, "#64748b"), amount=0.07)

        wc = WordCloud(
            width=1400, height=580,
            background_color="#1a1f2e",
            max_words=80,
            prefer_horizontal=0.70,
            color_func=color_func,
            margin=10,
            relative_scaling=0.55,
            min_font_size=10,
        ).generate_from_frequencies(tech_freq)

        return render_wc(wc)

    # ── Affichage ──────────────────────────────────────────────
    if wc_choice == "Catégories IT (par volume)":
        st.info("💡 La **taille** est proportionnelle au nombre d'offres. "
                "La **couleur** correspond à la famille métier.")
        st.image(wc_categories(), use_column_width=True)

        leg = st.columns(5)
        for i, (fam, color) in enumerate(FAM_COLORS.items()):
            with leg[i]:
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:6px;"
                    f"font-size:0.73rem;color:#94a3b8;'>"
                    f"<div style='width:12px;height:12px;border-radius:3px;"
                    f"background:{color};flex-shrink:0;'></div>"
                    f"{FAM_ICONS.get(fam,'🔵')} {fam}</div>",
                    unsafe_allow_html=True,
                )
    else:
        st.info("💡 Technologies et mots-clés détectés par les règles SQL regex.")
        st.image(wc_tech(), use_column_width=True)

        tech_leg = [
            ("#6366f1","Data & IA (ML, BI, SQL...)"),
            ("#10b981","Langages (Python, Java, JS...)"),
            ("#f59e0b","Cloud & DevOps (Docker, K8s...)"),
            ("#3b82f6","Frameworks (React, Spring...)"),
            ("#ec4899","ERP / Sécu / Méthodes"),
        ]
        lc = st.columns(len(tech_leg))
        for i, (color, label) in enumerate(tech_leg):
            with lc[i]:
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:6px;"
                    f"font-size:0.72rem;color:#94a3b8;'>"
                    f"<div style='width:12px;height:12px;border-radius:3px;"
                    f"background:{color};flex-shrink:0;'></div>{label}</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # Tech frequency bar
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
        {"tech":"TypeScript",      "freq":2600,"cat":"Langages"},
    ]).sort_values("freq")

    fig = px.bar(
        tech_df, x="freq", y="tech", orientation="h",
        color="cat",
        color_discrete_map={"Data & IA":"#6366f1","Langages":"#10b981",
                            "Cloud & DevOps":"#f59e0b","Frameworks":"#3b82f6",
                            "ERP / Sécu":"#ec4899"},
        title="Fréquence estimée des technologies",
        labels={"freq":"Fréquence","tech":"","cat":"Catégorie"},
    )
    fig.update_traces(
        marker=dict(line=dict(width=0)), marker_cornerradius=4,
        hovertemplate="<b>%{y}</b><br>Fréquence : %{x:,}<extra></extra>",
    )
    fig.update_layout(**dark_layout(
        showlegend=True,
        legend=dict(font=dict(color="#94a3b8",size=11),bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=50,b=20,l=160,r=30),
        title=dict(font=dict(color="#cbd5e1",size=13)),
        xaxis=dict(title="Offres concernées (estimé)",gridcolor="#1e293b",zerolinecolor="#1e293b"),
        yaxis=dict(title="",gridcolor="#1e293b"),
    ))
    pchart(fig, 480)


# ══════════════════════════════════════════════════════
#  TAB 3 — PIPELINE
# ══════════════════════════════════════════════════════
with tab3:

    st.markdown("### ⚡ Pipeline de traitement complet")

    fig = go.Figure(go.Funnel(
        y=["CSV Brut","→ Parquet Nettoyé","GCS Upload","BigQuery Import",
           "SQL Regex (~80 %)","Gemini API (~20 %)","✅ Dataset Final"],
        x=[66205,66205,66205,66205,52000,14287,50121],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=["#334155","#475569","#64748b",
                           "#3b82f6","#6366f1","#8b5cf6","#10b981"]),
        connector=dict(line=dict(color="#1e293b",dash="dot",width=2)),
        hovertemplate="<b>%{y}</b><br>Offres : %{x:,}<extra></extra>",
    ))
    fig.update_layout(**dark_layout(margin=dict(t=30,b=20,l=20,r=20)))
    pchart(fig, 440)

    st.markdown("---")
    st.markdown("### 📐 Étapes détaillées")

    steps = [
        ("1","📄 CSV → Parquet","#3b82f6",
         "Le CSV avait des **sauts de ligne** dans les descriptions, des **virgules** dans le texte "
         "et des **guillemets mal fermés**. Conversion en Parquet binaire via PyArrow + Snappy. "
         "Zéro problème d'encodage.",
         "python",
         "df.to_parquet('jobs.parquet',\n    engine='pyarrow',\n    compression='snappy',\n    index=False)"),
        ("2","☁️ GCS Upload","#6366f1",
         "Upload avec `gsutil cp` vers `gs://jobmatching/`. "
         "Sert de source BigQuery et de backup du dataset brut nettoyé.",
         "bash",
         "gsutil cp jobs_for_bigquery.parquet gs://jobmatching/"),
        ("3","🗄️ BigQuery — SQL","#8b5cf6",
         "Import en table `jobs_raw`. Application de `REGEXP_CONTAINS(LOWER(matching_text), pattern)` "
         "via CASE WHEN hiérarchique. **~52 000 offres en quelques secondes, coût : 0 $.**",
         "sql",
         "CREATE OR REPLACE TABLE jobs_classified AS\nSELECT *,\n  CASE\n"
         "    WHEN REGEXP_CONTAINS(LOWER(matching_text),\n"
         "         r'\\bsap\\b|abap|s/4hana') THEN 'Consultant SAP'\n"
         "    ...\n    ELSE 'Divers IT'\n  END AS job_type\nFROM jobs_raw;"),
        ("4","🤖 Gemini 2.5 Flash","#a855f7",
         "Les **14 287** offres 'Divers IT' envoyées à Gemini. "
         "Prompt numérique (1-42) → réponse = 1 chiffre. Temperature=0. Coût : **~0,07 $**.",
         "python",
         "response = model.generate_content(\n    prompt,\n"
         "    generation_config=GenerationConfig(\n"
         "        temperature=0,\n        max_output_tokens=5,\n    )\n)"),
        ("5","🔗 Fusion finale","#10b981",
         "LEFT JOIN SQL + Gemini sur `offer_id`. Priorité : SQL > Gemini > Fallback. "
         "Colonne `source_classif` pour la traçabilité.",
         "sql",
         "SELECT *,\n  CASE\n    WHEN job_type != 'Divers IT' THEN job_type\n"
         "    WHEN gemini IS NOT NULL   THEN gemini\n"
         "    ELSE 'Ingénieur IT Généraliste'\n  END AS job_type_FINAL\n"
         "FROM jobs_classified\nLEFT JOIN gemini_results USING (offer_id);"),
    ]

    for num, title, color, desc, lang, code in steps:
        with st.expander(f"**Étape {num} — {title}**", expanded=(num=="1")):
            c1, c2 = st.columns([1.2, 1])
            with c1:
                st.markdown(
                    f"<div style='border-left:3px solid {color};padding:12px 16px;"
                    f"background:rgba(0,0,0,.2);border-radius:0 8px 8px 0;'>"
                    f"<p style='color:#cbd5e1;font-size:0.83rem;line-height:1.75;margin:0;'>"
                    f"{desc}</p></div>",
                    unsafe_allow_html=True,
                )
            with c2:
                st.code(code, language=lang)

    st.markdown("---")
    st.markdown("### 📊 Comparaison des sources")
    src2 = pd.DataFrame({
        "Source":["SQL Rules","Gemini API","Fallback titre"],
        "Offres":[52000,9500,1213],
    })
    fig = px.bar(src2, x="Source", y="Offres", color="Source",
                 color_discrete_sequence=["#3b82f6","#6366f1","#f59e0b"],
                 text="Offres", title="Offres traitées par source")
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        marker=dict(line=dict(width=0)), marker_cornerradius=6,
    )
    fig.update_layout(**dark_layout(
        showlegend=False,
        margin=dict(t=50,b=20,l=20,r=20),
        title=dict(font=dict(color="#cbd5e1",size=13)),
        xaxis=dict(title="",gridcolor="#1e293b",zerolinecolor="#1e293b"),
        yaxis=dict(title="Nombre d'offres",gridcolor="#1e293b",zerolinecolor="#1e293b"),
    ))
    pchart(fig, 320)


# ══════════════════════════════════════════════════════
#  TAB 4 — SQL
# ══════════════════════════════════════════════════════
with tab4:

    st.markdown("### 🔍 Classification SQL — Détails techniques")

    c1,c2,c3 = st.columns(3)
    c1.metric("Offres traitées", "66 205")
    c2.metric("Classifiées SQL", "~52 000", "≈ 80 %")
    c3.metric("Résidu Gemini",   "14 287",  "-21,6 %")

    st.markdown("---")
    st.info("""
    **Champ `matching_text`** = job_title×2 + skills×2 + description + profile_required + experience

    Doubler le titre et les skills leur donne plus de **poids** dans la détection regex.
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
         "Avant Développeur Python car 'python' seul est trop générique."),
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
         "Trois règles séparées pour distinguer les providers cloud."),
    ]

    for num, cat, color, kws, note in rules:
        with st.expander(f"Règle {num} — **{cat}**"):
            c1, c2 = st.columns([1, 1.2])
            with c1:
                st.markdown(
                    f"<div style='border-left:3px solid {color};padding:10px 14px;"
                    f"background:rgba(0,0,0,.2);border-radius:0 8px 8px 0;margin-bottom:10px;'>"
                    f"<p style='color:#94a3b8;font-size:0.77rem;line-height:1.65;margin:0;'>"
                    f"💡 {note}</p></div>",
                    unsafe_allow_html=True,
                )
                kw_html = "".join(
                    f"<code style='background:rgba(99,102,241,.15);color:#818cf8;"
                    f"padding:2px 8px;border-radius:5px;font-size:0.71rem;margin:2px;'>{k}</code>"
                    for k in kws
                )
                st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:4px;'>{kw_html}</div>",
                            unsafe_allow_html=True)
            with c2:
                st.code(
                    f"WHEN REGEXP_CONTAINS(LOWER(matching_text),\n"
                    f"     r'{chr(124).join(kws)}')\n"
                    f"THEN '{cat}'",
                    language="sql",
                )

    st.markdown("---")
    st.markdown("#### ⚠️ Word boundaries `\\b` — pourquoi c'est essentiel")
    wb_df = pd.DataFrame({
        "Pattern":[r"\bsap\b",r"\bsoc\b",r"\bjava\b",r"\bai\b",r"\bdba\b"],
        "✅ Matche":["SAP HANA","SOC analyst","Java developer","AI engineer","DBA Oracle"],
        "❌ Évite":["kidnap, satrap","social","JavaScript","email, paid","sans \\b"],
    })
    st.dataframe(wb_df, width="stretch", hide_index=True)

    st.markdown("---")
    ca2, cl2 = st.columns(2)
    with ca2:
        st.success("""**✅ Avantages SQL**
- Gratuit — 0 $ par offre
- Instantané — < 5 s sur 66 k offres
- Déterministe et traçable
- Facile à maintenir et auditer""")
    with cl2:
        st.error("""**❌ Limites SQL**
- Contexte ignoré
- Titres ambigus non résolus
- Nouveaux rôles non prévus (MLOps...)
→ Ces limites justifient Gemini""")


# ══════════════════════════════════════════════════════
#  TAB 5 — GEMINI
# ══════════════════════════════════════════════════════
with tab5:

    st.markdown("### 🤖 Classification Gemini API — Détails techniques")

    params = [
        ("Modèle",           "gemini-2.0-flash","Rapide et économique"),
        ("Temperature",      "0",               "100 % déterministe"),
        ("max_output_tokens","5",               "Juste le numéro '7'"),
        ("Offres traitées",  "14 287",          "Résidu 'Divers IT'"),
        ("Vitesse",          "~94 / min",       "Avec pause 0,1 s"),
        ("Durée totale",     "~160 min",        "2h40 en continu"),
        ("Coût total",       "~0,07 $",         "~600 tokens × 14 287"),
        ("Safety settings",  "BLOCK_NONE",      "Évite blocages techniques"),
        ("Pause",            "0,1 sec",         "Respecter les quotas"),
    ]
    cols = st.columns(3)
    for i,(lbl,val,hlp) in enumerate(params):
        with cols[i%3]:
            st.metric(lbl, val, help=hlp)

    st.markdown("---")
    st.markdown("#### 📊 Résultats sur les 14 287 offres")
    gc1, gc2 = st.columns([1, 1.2])

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
            marker=dict(line=dict(color="#0f1117",width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>",
        )
        fig.update_layout(**dark_layout(
            showlegend=True,
            legend=dict(font=dict(color="#94a3b8",size=11),bgcolor="rgba(0,0,0,0)"),
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
                f"<div style='background:#1a1f2e;border:1px solid #2a3347;"
                f"border-radius:10px;padding:14px;margin-bottom:10px;'>"
                f"<div style='font-size:0.73rem;color:#64748b;margin-bottom:3px;'>{label}</div>"
                f"<div style='font-size:1.35rem;font-weight:900;color:{color};'>{val:,}</div>"
                f"<div style='font-size:0.67rem;color:#475569;margin-bottom:7px;'>{pct} %</div>"
                f"<div style='height:5px;background:#1e293b;border-radius:3px;overflow:hidden;'>"
                f"<div style='width:{pct}%;height:100%;background:{color};border-radius:3px;'>"
                f"</div></div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("#### 🎯 Choix de design du prompt")

    designs = [
        ("Réponse numérique (1-42)","#6366f1",
         "Gemini répond `'3'` au lieu de `'Data Scientist / IA'`. Parsing trivial."),
        ("Temperature = 0","#10b981",
         "Même offre = même résultat à chaque appel. Essentiel pour la reproductibilité."),
        ("max_output_tokens = 5","#f59e0b",
         "Un chiffre ≤ 2 caractères. Économie de ~60 % de tokens → coût réduit de 60 %."),
        ("Catégorie 42 = NON-IT","#ec4899",
         "3 574 NON-IT supplémentaires détectés que le SQL avait manqués."),
        ("Texte limité à 300 chars","#3b82f6",
         "`matching_text[:300]` contient déjà titre×2 + skills×2. Économie de ~60 % de tokens."),
        ("Safety BLOCK_NONE","#06b6d4",
         "Évite les blocages sur des termes comme 'pentest', 'exploit', 'injection'."),
    ]
    for title, color, desc in designs:
        with st.expander(f"**{title}**"):
            st.markdown(
                f"<div style='border-left:3px solid {color};padding:12px 16px;"
                f"background:rgba(0,0,0,.15);border-radius:0 8px 8px 0;'>"
                f"<p style='color:#cbd5e1;font-size:0.83rem;line-height:1.75;margin:0;'>"
                f"{desc}</p></div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("#### 🔄 Code — Retry + Fallback")
    st.code("""
def classifier_gemini(job_title, texte, retry=0):
    if retry > 3:
        return classifier_par_titre(job_title)   # fallback

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
        return classifier_par_titre(job_title)

    except Exception as e:
        if "429" in str(e):
            time.sleep(extraire_delai(e) + 10)
            return classifier_gemini(job_title, texte, retry + 1)
        return classifier_par_titre(job_title)

# Sauvegarde toutes les 500 offres
if (idx + 1) % 500 == 0:
    pd.DataFrame(resultats).to_csv('gemini_temp.csv', index=False)
""", language="python")

    st.warning("""
    **⚠️ Reprendre après interruption :**
    Charger `gemini_temp.csv`, filtrer les `offer_id` déjà traités,
    reprendre avec `WRITE_APPEND`. Perte max = 500 offres ≈ 5 min.
    """)
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static
import folium

st.set_page_config(page_title="Marketing Dashboard – Segmentation & Personalized Pricing", layout="centered")

if "page_landing" not in st.session_state:
    st.session_state.page_landing = True

if st.session_state.page_landing:
    st.markdown("""
        <style>
        .landing {
            text-align: center;
            padding-top: 5rem;
        }
        .landing h1 {
            font-size: 3.5rem;
            font-weight: 800;
            color: #1f77b4;
            animation: fadeInDown 1s ease;
        }
        .landing p {
            font-size: 1.2rem;
            color: #4b5563;
            margin-bottom: 2rem;
            animation: fadeInUp 1.2s ease;
        }
        .landing img {
            width: 200px;
            margin-bottom: 2rem;
        }
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="landing">
            <h1>Bienvenue dans le Dashboard Client</h1>
            <p>Analyse, segmentation et actions marketing<br></p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Entrer dans le dashboard", use_container_width=True):
        st.session_state.page_landing = False
        st.rerun()
    st.stop()



st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f7f9fc;
        color: #2c3e50;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    }

    /* Title and Subheaders */
    h1, h2, h3 {
        color: #1f2937;
        font-weight: 700;
    }

    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    h2 {
        font-size: 1.8rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    /* Buttons */
    button[kind="primary"] {
        background-color: #1f77b4 !important;
        color: white !important;
        border: none;
        border-radius: 0.5rem;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    button[kind="primary"]:hover {
        background-color: #125a8d !important;
        transform: scale(1.03);
    }

    /* Metric boxes */
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        margin: 0.5rem;
    }

    div[data-testid="metric-container"] > label {
        font-size: 1rem;
        color: #6b7280;
    }

    div[data-testid="metric-container"] > div {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
    }

    /* Dataframe */
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        padding: 0.5rem;
    }

    /* Recommandation blocks */
    .element-container:has(h3) {
        background-color: #fefefe;
        border: 1px solid #e0e0e0;
        border-left: 6px solid #1f77b4;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.03);
        transition: all 0.2s ease-in-out;
    }

    .element-container:has(h3):hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }

    /* Pydeck map container */
    iframe[src*="mapbox"] {
        border-radius: 1rem;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }

    /* Multiselect, Selectbox */
    .stMultiSelect, .stSelectbox {
        background-color: white !important;
        border-radius: 0.5rem;
        border: 1px solid #d1d5db;
        padding: 0.4rem;
    }

    /* Tables and Markdown */
    .stMarkdown p {
        font-size: 1rem;
        line-height: 1.6;
        color: #2c3e50;
    }

    .stMarkdown ul {
        padding-left: 1.2rem;
    }

    /* Captions and footer */
    footer, .css-1v0mbdj, .css-h5rgaw {
        text-align: center;
        font-size: 0.85rem;
        color: #9ca3af;
        margin-top: 2rem;
    }

    /* Smooth transitions */
    * {
        transition: all 0.2s ease-in-out;
    }
    

    /* Mobile responsiveness */
    @media screen and (max-width: 768px) {
        h1 { font-size: 2rem; }
        h2 { font-size: 1.5rem; }
        .stMetric { font-size: 1.2rem; }
        div[data-testid="metric-container"] {
            margin: 0.25rem 0;
        }
    }
    
    /* Mobile responsiveness */
@media screen and (max-width: 768px) {
    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    .stMetric { font-size: 1.2rem; }
    div[data-testid="metric-container"] {
        margin: 0.25rem 0;
    }
}

/* Dark mode styles */
@media (prefers-color-scheme: dark) {
    html, body, [class*="css"] {
        background-color: #1e1e1e;
        color: #f0f0f0;
    }

    section[data-testid="stSidebar"] {
        background-color: #2b2b2b;
        border-right: 1px solid #444;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    .stDataFrame {
        background-color: #2b2b2b;
        color: #e5e5e5;
    }

    .element-container:has(h3) {
        background-color: #2c2f33;
        border-color: #555;
    }

    .stMarkdown p {
        color: #f0f0f0;
    } 

    /* Labels */
    div[data-testid="stVerticalBlock"] label {
        color: #b0b0b0 !important;
        font-weight: 600;
    } 
    
        section[data-testid="stSidebar"] label {
        color: #111111 !important;
        font-weight: 600;
    }

    /* Multiselect */
    div[data-baseweb="select"] > div {
        background-color: #222 !important;
        color: #f0f0f0 !important;
        border-radius: 6px;
    }

    div[data-baseweb="select"] input {
        color: #888 !important;
    }

    ul[role="listbox"] {
        background-color: #222 !important;
        color: #f0f0f0 !important;
    }

    div[class*="multiValue"] {
        background-color: #444 !important;
        color: #111111 !important;
        border-radius: 4px;
    }
    

    /* 📊 Metrics : texte clair sur fond sombre */
    div[data-testid="metric-container"] {
        background-color: #2e2e2e;
        color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #444;
    }

    div[data-testid="metric-container"] > label {
        color: #111111 !important;
        font-weight: bold;
    }

    div[data-testid="metric-container"] > div {
        color: #ffffff !important;
        font-size: 1.3rem;
    }
}




}

    </style>
""", unsafe_allow_html=True)





# Données
df = pd.read_csv("data_with_cluster.csv")

region_coords = {
    "Centre": (3.87, 11.52),
    "Littoral": (4.05, 9.70),
    "Nord": (9.75, 13.50),
    "Sud": (2.75, 11.85),
    "Ouest": (5.50, 10.40),
    "Est": (4.25, 14.60),
    "Nord-Ouest": (6.25, 10.25),
    "Sud-Ouest": (4.25, 9.25),
    "Adamaoua": (7.25, 13.55),
    "Extreme-Nord": (11.00, 14.50),
}


df["lat"] = df["region"].map(lambda x: region_coords[x][0])
df["lon"] = df["region"].map(lambda x: region_coords[x][1])

# Menu
page = option_menu(
    menu_title=None,
    options=["Vue d'ensemble", "Analyse par cluster", "Recommandations marketing", "Données détaillées"],
    icons=['bar-chart-line', 'person-lines-fill', ' ', 'table'],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {
            "padding": "0!important",
            "margin": "0",
            "width": "100%",
            "background-color": "#2c2f33",  # gris foncé sobre
            "border-bottom": "2px solid #444"
        },
        "icon": {"color": "#f0f0f0", "font-size": "18px"},  # couleur lisible sur fond sombre
        "nav-link": {
            "font-size": "16px",
            "color": "#f0f0f0",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#3f444e",
        },
        "nav-link-selected": {
            "background-color": "#1f77b4",
            "color": "white",
            "font-weight": "bold"
        }
    }
)



# FILTRES
with st.sidebar:
    st.header("🔎 Filtres")
    selected_clusters = st.multiselect("Cluster(s)", sorted(df["cluster_kpca"].unique()))
    selected_types = st.multiselect("Type de client", sorted(df["customer_type"].unique()))
    selected_regions = st.multiselect("Région", sorted(df["region"].unique()))

filtered_df = df.copy()
if selected_clusters:
    filtered_df = filtered_df[filtered_df["cluster_kpca"].isin(selected_clusters)]
if selected_types:
    filtered_df = filtered_df[filtered_df["customer_type"].isin(selected_types)]
if selected_regions:
    filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]

# PAGE 1 - VUE D'ENSEMBLE
if page == "Vue d'ensemble":
    st.title("📊 Vue d’ensemble des Clients")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de clients", len(filtered_df))
    col2.metric("Recharge mensuelle moyenne", f"{filtered_df['monthly_recharge_xaf'].mean():,.0f} FCFA")
    col3.metric("Data mensuelle moyenne", f"{filtered_df['data_usage_gb'].mean():.2f} Go")

    st.subheader("🗺️ Répartition géographique")
    df_region = filtered_df["region"].value_counts().reset_index()
    df_region.columns = ["region", "nb_clients"]
    df_region["lat"] = df_region["region"].map(lambda x: region_coords[x][0])
    df_region["lon"] = df_region["region"].map(lambda x: region_coords[x][1])



    # Carte centrée sur le Cameroun
    m = folium.Map(location=[4.5, 11.5], zoom_start=6, tiles="CartoDB positron")

    # Ajouter les cercles pour chaque région
    for _, row in df_region.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=row["nb_clients"] / 90,  # Ajuste le facteur si les cercles sont trop gros
            color='crimson',
            fill=True,
            fill_opacity=0.8,
            popup=folium.Popup(
                html=f"<b>Région :</b> {row['region']}<br><b>Clients :</b> {row['nb_clients']}",
                max_width=250
            )
        ).add_to(m)

    # Afficher la carte dans Streamlit
    folium_static(m)



# PAGE 2 - ANALYSE PAR CLUSTER
elif page == "Analyse par cluster":
    st.title("👤 Analyse par Cluster")
    selected_cluster = st.selectbox("Sélectionnez un cluster :", sorted(filtered_df["cluster_kpca"].unique()))
    cluster_df = filtered_df[filtered_df["cluster_kpca"] == selected_cluster]

    st.write(f"📌 Nombre de clients : **{len(cluster_df)}**")
    st.write(f"💳 Recharge mensuelle moyenne : **{cluster_df['monthly_recharge_xaf'].mean():,.0f} FCFA**")
    st.write(f"📅 Ancienneté moyenne : **{cluster_df['tenure_months'].mean():.1f} mois**")
    st.write(f"🌐 Data mensuelle moyenne : **{cluster_df['data_usage_gb'].mean():.2f} Go**")

    st.subheader("📊 Distribution de l'âge")
    fig, ax = plt.subplots()
    sns.histplot(cluster_df["age"], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

# PAGE 3 - RECOMMANDATIONS
elif page == "Recommandations marketing":
    st.title("Recommandations Marketing Stratégiques")
    
    st.markdown("Ces recommandations sont basées sur une analyse comportementale fine des clusters. Elles visent à activer des **leviers marketing concrets** pour maximiser la valeur client.")

    def show_reco(cluster_id, title, description, objectif, actions, color):
        getattr(st, color)(f"### Cluster {cluster_id} – {title}")
        st.markdown(f"**Qui sont-ils ?** {description}")
        st.markdown(f"**🎯 Objectif :** {objectif}")
        st.markdown("**💡 Actions recommandées :**")
        for act in actions:
            st.markdown(f"- {act}")
        if cluster_id != 2: 
            st.markdown("---")

    show_reco(
        3, "Fidélisation + services exclusifs",
        "Clients très fidèles (4+ ans), très rentables (~15 000 FCFA/mois).",
        "Les garder longtemps et les valoriser.",
        [
            "Offres VIP (anniversaire, cashback à la recharge)",
            "Accès anticipé aux nouveaux produits",
            "Ligne prioritaire au service client",
            "Invitations à des événements partenaires"
        ],
        "success"
    )

    show_reco(
        0, "Montée en gamme rapide",
        "Clients récents (1-1.5 an) mais très dépensiers.",
        "Les transformer en clients premium fidèles.",
        [
            "Bonus de fidélité après 3 ou 6 mois",
            "Offres combinées (data + appels illimités de nuit)",
            "Notifications personnalisées (« client premium Silver »)"
        ],
        "warning"
    )
    
    show_reco(
        1, "Réactivation + upsell",
        "Clients anciens, fidèles, mais faibles dépenses.",
        "Les réactiver ou les convertir en postpaid.",
        [
            "Forfaits data adaptés (1 Go/jour pour 1 000 FCFA)",
            "Migration facile vers postpaid",
            "Remises fidélité pour clients >4 ans"
        ],
        "info"
    )

    show_reco(
        2, "Push recharge + bundles simples",
        "Faible consommation, faible fréquence de recharge.",
        "Augmenter fréquence de recharge et valeur client.",
        [
            "SMS flash : « Rechargez 500 FCFA → 150 Mo gratuits »",
            "Bundles petits prix (300 FCFA/jour)",
            "Campagnes USSD simples (*123#)"
        ],
        "info"
    )

    

# PAGE 4 - DONNÉES DÉTAILLÉES
elif page == "Données détaillées":
    st.title("📋 Données détaillées")
    st.dataframe(filtered_df.head(100))

# FOOTER
st.markdown("---")
st.caption("Projet de segmentation client – réalisé avec Streamlit par ALOTSE Christy")

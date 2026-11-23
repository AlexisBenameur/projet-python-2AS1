import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import contextily as cx
import requests
import io

url_ips = "https://data.education.gouv.fr/explore/embed/dataset/fr-en-ips_lycees/table/?disjunctive_rentree_scolaire=&disjunctive_academie=&disjunctive_code_du_departement=&disjunctive_departement=&disjunctive_uai=&disjunctive_nom_de_l_etablissment=&disjunctive_code_insee_de_la_commune=&disjunctive_nom_de_la_commune=&disjunctive_secteur=&disjunctive_type_de_lycee=&disjunctive.rentree_scolaire&disjunctive.academie&disjunctive.code_du_departement&disjunctive.departement&disjunctive.uai&disjunctive.nom_de_l_etablissment&disjunctive.code_insee_de_la_commune&disjunctive.nom_de_la_commune&disjunctive.secteur&disjunctive.type_de_lycee&q=GRENOBLE&sort=-ips_voie_gt"
url_res = "https://data.education.gouv.fr/explore/dataset/fr-en-ips_lycees/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
url_carte = "https://data-interne.ademe.fr/data-fair/api/v1/datasets/geo-contours-departements"

@st.cache_data
def recup_data(url):
    headers = {
        "Accept": "text/csv",
        "User-Agent": "python-requests/2.31.0"
    }
    response = requests.get(url)
    response.raise_for_status()
    
    if response.text.lstrip().startswith("<"):
        st.error("Le serveur a renvoyé du HTML au lieu d'un CSV :")
        st.code(response.text[:600], language="html")
        st.stop()
    return pd.read_csv(io.StringIO(response.text), sep=";")

df_ips = recup_data(url_ips)
df_res = recup_data(url_res)
df_carte = recup_data(url_carte)

df_ips["Code du département"] = int(df_ips["Code du département"])
df_carte = gpd.GeoDataFrame(df_carte, geometry="geometry")

df_ips_agg = df_ips.groupby("Code du département").agg({"IPS": "mean"}).reset_index()
data_carte = df_carte.merge(df_ips_agg, left_on="DDEP_C_COD", right_on="Code du département")

def tracer_ips(data):
    map = data.explore(columns="IPS", cmap="inferno", legend=True, tiles="CartoDB positron", tooltip=["IPS", "DDEP_L_LIB", "DREG_L_LIB"])
    return map






st.set_page_config(page_title="Cartes IPS", page_icon="🌍", layout = "wide")
st.title("Mérite ou Héritage ? Des cartes pour mieux comprendre les inégalités scolaires en France.")

code_css = """
<style>
 .stApp {
   background-color: #0A192F;
   }
.stApp {
   color: #FFFFFF;
   }
.stAPP {
   # padding: 20px; 
    } 
.stApp label p {
    color: #FFFFFF !important; 
    }
    [data-testid="stSidebar"] {
        color: #FFFFFF;
    }
    [data-testid="stSidebar"] {
        background-color: #0A193F;
    }
    [data-testid="stSidebar"] label p {
            color: #FFFFFF !important; 
            font-size: 16px;}
    """

st.markdown(code_css, unsafe_allow_html=True)

with st.sidebar : 
    st.header("Filtres")
    resolution = st.selectbox("Choisissez la resolution de la carte", ["Pays", "Région"])
    if resolution == "Région" : 
        region = st.selectbox("Choisissez la région", data_carte["DREG_L_LIB"].unique())
        data_final = data_carte[data_carte["DREG_L_LIB"]==region]
    else : 
        data_final = data_carte

    if st.button("Afficher la carte"):
        with st.spinner("Génération de la carte en cours...") :
            map = tracer_ips(data_final)
            st.html(map._repr_html_(),height=600)
                   
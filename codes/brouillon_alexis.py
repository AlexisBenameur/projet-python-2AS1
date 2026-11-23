import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import contextily as cx
import requests
import io
from shapely.geometry import shape
import json
import numpy as np
np.float = float
np.long = int
import sys
sys.modules["numba"] = None

st.set_page_config(page_title="Cartes IPS", page_icon="🌍", layout = "wide")

url_ips = "https://data.education.gouv.fr/explore/dataset/fr-en-ips_lycees/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
url_res = "https://data.education.gouv.fr/explore/dataset/fr-en-indicateurs-de-resultat-des-lycees-gt_v2/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
url_carte = "https://data-interne.ademe.fr/data-fair/api/v1/datasets/geo-contours-departements/lines?draft=false&size=10000&finalizedAt=2022-03-02T14:11:30.661Z&page=1&format=csv&sep=;"

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
df_carte = pd.read_csv(url_carte, sep=";")
df_carte["geometry"] = df_carte["geometry"].apply(
    lambda x: shape(json.loads(x)) if isinstance(x, str) else x
)

df_ips["Code du département"] = pd.to_numeric(df_ips["Code du département"], errors="coerce").astype("Int64")
#df_ips["Code du département"] = df_ips["Code du département"].astype(int)
df_carte["DDEP_C_COD"] = pd.to_numeric(df_carte["DDEP_C_COD"], errors="coerce").astype("Int64")
df_ips_agg = df_ips.groupby("Code du département").agg({"IPS voie GT": "mean"}).reset_index()
data_carte = df_carte.merge(df_ips_agg, left_on="DDEP_C_COD", right_on="Code du département")
data_carte = gpd.GeoDataFrame(data_carte, geometry="geometry")
if data_carte.crs is None:
    data_carte = data_carte.set_crs("EPSG:4326")
else:
    data_carte = data_carte.to_crs("EPSG:4326")


def tracer_ips(data):
    map = data.explore(column="IPS voie GT", cmap="inferno", legend=True, 
                       tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                       attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',       
                       tooltip=["IPS voie GT", "DDEP_L_LIB", "DREG_L_LIB"])
    return map







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



resolution = st.selectbox("Choisissez la resolution de la carte", ["Pays", "Région"])
if resolution == "Région" : 
    region = st.selectbox("Choisissez la région", data_carte["DREG_L_LIB"].unique())
    data_final = data_carte[data_carte["DREG_L_LIB"]==region]
else : 
    data_final = data_carte

if st.button("Afficher la carte"):
    with st.spinner("Génération de la carte en cours...") :
        map = tracer_ips(data_final)
        st.components.v1.html(map._repr_html_(),height=600,scrolling=True)
                   
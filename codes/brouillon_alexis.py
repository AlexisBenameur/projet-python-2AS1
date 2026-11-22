import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st

url_ips = "https://data.education.gouv.fr/explore/embed/dataset/fr-en-ips_lycees/table/?disjunctive_rentree_scolaire=&disjunctive_academie=&disjunctive_code_du_departement=&disjunctive_departement=&disjunctive_uai=&disjunctive_nom_de_l_etablissment=&disjunctive_code_insee_de_la_commune=&disjunctive_nom_de_la_commune=&disjunctive_secteur=&disjunctive_type_de_lycee=&disjunctive.rentree_scolaire&disjunctive.academie&disjunctive.code_du_departement&disjunctive.departement&disjunctive.uai&disjunctive.nom_de_l_etablissment&disjunctive.code_insee_de_la_commune&disjunctive.nom_de_la_commune&disjunctive.secteur&disjunctive.type_de_lycee&q=GRENOBLE&sort=-ips_voie_gt"
url_res = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-indicateurs-de-resultat-des-lycees-gt_v2/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true"
url_carte = "https://data-interne.ademe.fr/data-fair/api/v1/datasets/geo-contours-departements"

@st.cache_data
def recup_data(url):
    df = pd.read_csv(url, sep=";")
    return df 

df_ips = recup_data(url_ips)
df_res = recup_data(url_res)
df_carte = recup_data(url_carte)

df_ips["Code du département"] = int(df_ips["Code du département"])
df_carte = gpd.GeoDataFrame(df_carte, geometry="geometry")

df_ips_agg = df_ips.groupby("Code du département").agg({"IPS": "mean"}).reset_index()
data_carte = df_carte.merge(df_ips_agg, left_on="DDEP_C_COD", right_on="Code du département")

def tracer_carte(data):
    






st.set_page_config(page_title="Cartes IPS", page_icon="🌍", layout = "wide")

                   
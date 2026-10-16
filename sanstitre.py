import streamlit as st
import pandas as pd
import plotly.express as px
import math, os
from datetime import datetime

# Configuration de l'application
st.set_page_config(page_title="mgGCAPP — Votre Guide de Construction Simple", page_icon="🏗️", layout="wide")

# 1. EN-TÊTE ET SALUTATION
heure = datetime.now().hour
salut = "Bonjour Monsieur" if 5 <= heure < 18 else "Bonsoir Monsieur"

st.title("🏗️ mgGCAPP — Votre Guide de Chantier Simple & Complet")
st.caption(f"✨ {salut}, bienvenue ! Même sans aucune notion de génie civil, réalisez et comprenez votre devis de A à Z.")

st.divider()

# 2. IDENTIFICATION ET QUESTION IMMÉDIATE (DEMANDÉE)
st.subheader("👤 Commençons par faire connaissance")

col_id1, col_id2 = st.columns(2)
with col_id1:
    nom = st.text_input("Votre Nom & Prénom :", value="Client")
with col_id2:
    tel = st.text_input("Votre Téléphone / WhatsApp :", placeholder="+237...")

# Enregistrement du client
if nom != "Client" and tel:
    fichier_csv = "visiteurs.csv"
    df_nouveau = pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Nom": nom, "Tel": tel}])
    if os.path.exists(fichier_csv):
        df_exist = pd.read_csv(fichier_csv)
        if not ((df_exist['Nom'] == nom) & (df_exist['Tel'] == tel)).any():
            df_nouveau.to_csv(fichier_csv, mode="a", header=False, index=False)
    else:
        df_nouveau.to_csv(fichier_csv, mode="w", header=True, index=False)

st.markdown("---")

# QUESTION IMMÉDIATE APRÈS LES NOMS
st.markdown(f"### 💬 *Que pouvons-nous faire pour vous, {nom} ?*")
besoin_client = st.selectbox(
    "Sélectionnez votre objectif principal :",
    [
        "Estimer toutes les dépenses de mon projet de A à Z (Gros œuvre & Finitions)",
        "Comprendre pas à pas les étapes de construction et le matériel nécessaire",
        "Savoir combien de sacs de ciment et d'ouvriers il me faudra",
        "Obtenir un accompagnement technique sur le terrain avec un expert"
    ]
)

st.info(f"📌 **Objectif sélectionné :** _{besoin_client}_. L'application configure votre simulation sur mesure ci-dessous.")

st.divider()

# 3. EXPLICATION PÉDAGOGIQUE : CE QUE FAIT L'APPLICATION PAS À PAS
with st.expander("🔍 **Comment ça marche ? Ce que l'application fait en détail pour vous :**"):
    st.markdown("""
    1. **Analyse de votre surface :** À partir de la superficie de votre terrain, nous calculons la quantité exacte de béton, de sable, de gravier et de ciment.
    2. **Adaptation des dosages :** Chaque partie de la maison n'a pas besoin de la même solidité (le béton de propreté est léger, les poteaux et dalles demandent un ciment plus fort).
    3. **Recensement de toutes les dépenses :** Du premier coup de pioche (fouilles) jusqu'à la remise des clés (peinture, carrelage, électricité, plomberie).
    4. **Suivi des ressources :** Nous vous indiquons combien d'ouvriers et de techniciens employer à chaque étape.
    """)

st.divider()

# 4. PARAMÈTRES DU PROJET DE CONSTRUCTION
st.subheader("🏠 Paramètres de votre Maison")

c_proj, c_surf = st.columns(2)
with c_proj:
    type_projet = st.selectbox("Type de projet :", ["Plain-pied (RDC)", "R+1", "R+2", "R+2-1"])
with c_surf:
    surf = st.number_input("Superficie au sol (m²) :", min_value=30, max_value=1500, value=100, step=10)

st.markdown("#### Répartition des pièces :")
cp1, cp2, cp3, cp4, cp5 = st.columns(5)
with cp1:
    nb_chambres = st.number_input("Chambres :", min_value=1, max_value=20, value=3)
with cp2:
    nb_salons = st.number_input("Salons :", min_value=1, max_value=5, value=1)
with cp3:
    nb_cuisines = st.number_input("Cuisines :", min_value=1, max_value=5, value=1)
with cp4:
    nb_wc = st.number_input("SDB / WC :", min_value=1, max_value=10, value=2)
with cp5:
    nb_verandas = st.number_input("Vérandas :", min_value=0, max_value=10, value=1)

with st.expander("⚙️ Options de Devise"):
    devise = st.selectbox("Devise d'affichage :", ["FCFA", "EUR (€)", "USD ($)"])

# 5. CALCULS GLOBAUX & BUDGET COMPLET (DU DÉBUT À LA FIN)
niveaux_dict = {"Plain-pied (RDC)": 1, "R+1": 2, "R+2": 3, "R+2-1": 2.5}
niveaux = niveaux_dict[type_projet]
surf_tot = surf * niveaux
perim = 4 * math.sqrt(surf) * 1.3
ratio_cloison = 1.0 + ((nb_chambres + nb_salons + nb_cuisines + nb_wc) * 0.05)
perim_effectif = perim * ratio_cloison

vol_beton = round((surf * 0.12) + (surf_tot * 0.05) + ((niveaux - 1) * surf * 0.15) + (perim_effectif * 0.45 * 0.45), 1)

# Calcul ciment par étape (dosages techniques expliqués simplement)
ciment_proprete = math.ceil((surf * 0.05 * 180) / 50)          # Dosage 180 kg/m³
ciment_fondation = math.ceil((vol_beton * 0.35 * 300) / 50)     # Dosage 300 kg/m³
ciment_elevation = math.ceil((vol_beton * 0.50 * 350) / 50)     # Dosage 350 kg/m³
ciment_toiture = math.ceil((vol_beton * 0.15 * 400) / 50)       # Dosage 400 kg/m³
sacs_ciment_total = ciment_proprete + ciment_fondation + ciment_elevation + ciment_toiture

sable = round(vol_beton * 0.45, 1)
gravier = round(vol_beton * 0.82, 1)
acier_kg = math.ceil(vol_beton * (75 if niveaux <= 2 else 95))
agglos = math.ceil(perim_effectif * 3.0 * niveaux * 9)

is_fcfa = (devise == "FCFA")
pu = {
    "Ciment": 4800 if is_fcfa else 8,
    "Sable": 9000 if is_fcfa else 35,
    "Gravier": 14000 if is_fcfa else 45,
    "Acier": 750 if is_fcfa else 1.6,
    "Agglos": 320 if is_fcfa else 1.2
}

# Tous les coûts du chantier de A à Z (Gros œuvre + Second œuvre complet)
cout_preparation = surf * (3500 if is_fcfa else 6)
cout_fouilles = surf * (6000 if is_fcfa else 10)
cout_fondation = int((ciment_fondation * pu["Ciment"]) + (sable * pu["Sable"] * 0.3) + (gravier * pu["Gravier"] * 0.3))
cout_elevation = int((ciment_elevation * pu["Ciment"]) + (agglos * pu["Agglos"]) + (acier_kg * pu["Acier"] * 0.6))
cout_toiture = int((ciment_toiture * pu["Ciment"]) + (acier_kg * pu["Acier"] * 0.4) + surf * (12000 if is_fcfa else 20))
cout_second_oeuvre = surf * (25000 if is_fcfa else 40) # Électricité, plomberie, cloisons intérieures
cout_finitions = surf * (20000 if is_fcfa else 35)      # Carrelage, peinture, portes et fenêtres

data_planning = [
    {
        "Étape du Chantier": "1. Préparation & Nettoyage",
        "Dosage Ciment": "N/A",
        "Personnel Requis": "2 Manœuvres + 1 Topographe",
        "Nb Personnel": 3,
        "Sacs": 0,
        "Coût Estimé": cout_preparation
    },
    {
        "Étape du Chantier": "2. Fouilles & Béton de Propreté",
        "Dosage Ciment": "180 kg/m³ (Léger)",
        "Personnel Requis": "4 Manœuvres + 1 Chef d'équipe",
        "Nb Personnel": 5,
        "Sacs": ciment_proprete,
        "Coût Estimé": cout_fouilles
    },
    {
        "Étape du Chantier": "3. Fondation (Semelles, Longrines)",
        "Dosage Ciment": "300 kg/m³ (Standard)",
        "Personnel Requis": "2 Maçons + 5 Manœuvres + 1 Technicien",
        "Nb Personnel": 8,
        "Sacs": ciment_fondation,
        "Coût Estimé": cout_fondation
    },
    {
        "Étape du Chantier": "4. Élévation (Murs & Poteaux)",
        "Dosage Ciment": "350 kg/m³ (Solide)",
        "Personnel Requis": "3 Maçons + 6 Manœuvres + 1 Technicien",
        "Nb Personnel": 10,
        "Sacs": ciment_elevation,
        "Coût Estimé": cout_elevation
    },
    {
        "Étape du Chantier": "5. Toiture & Dalle",
        "Dosage Ciment": "400 kg/m³ (Très résistant)",
        "Personnel Requis": "2 Charpentiers + 3 Manœuvres",
        "Nb Personnel": 5,
        "Sacs": ciment_toiture,
        "Coût Estimé": cout_toiture
    },
    {
        "Étape du Chantier": "6. Second Œuvre (Électricité & Plomberie)",
        "Dosage Ciment": "N/A",
        "Personnel Requis": "1 Électricien + 1 Plombier",
        "Nb Personnel": 2,
        "Sacs": 0,
        "Coût Estimé": cout_second_oeuvre
    },
    {
        "Étape du Chantier": "7. Finitions (Carrelage & Peinture)",
        "Dosage Ciment": "N/A",
        "Personnel Requis": "2 Carreleurs + 2 Peintres",
        "Nb Personnel": 4,
        "Sacs": 0,
        "Coût Estimé": cout_finitions
    }
]

df_planning = pd.DataFrame(data_planning)
total_global = int(df_planning["Coût Estimé"].sum())

st.divider()

# 6. ONGLETS DE PRÉSENTATION CLAIRE
tab_suivi, tab_courbes, tab_fin, tab_admin = st.tabs(["📊 Toutes les Dépenses (De A à Z)", "📈 Courbes & Ressources", "🏁 Suivi de Chantier", "📁 Historique"])

with tab_suivi:
    st.subheader("📅 Tableau récapitulatif complet de toutes les dépenses du chantier")
    st.warning("⚠️ **Important :** Ce devis englobe l'ensemble des matériaux nécessaires du début à la fin. La main-d'œuvre du technicien et des ouvriers fait l'objet d'un accord salarial distinct.")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Ciment Total Requis", f"{sacs_ciment_total} sacs")
    m2.metric("Pic d'Ouvriers", "10 personnes max")
    m3.metric("BUDGET TOTAL ESTIMÉ", f"{total_global:,.0f} {devise}".replace(",", " "))

    st.dataframe(df_planning, use_container_width=True)

with tab_courbes:
    st.subheader("📈 Visualisation des Courbes (Ciment & Personnel)")
    
    c_c1, c_c2 = st.columns(2)
    with c_c1:
        fig_ciment = px.line(df_planning, x='Étape du Chantier', y='Sacs', markers=True, 
                             title="Courbe du Taux de Ciment par Étape",
                             color_discrete_sequence=['#D97706'])
        st.plotly_chart(fig_ciment, use_container_width=True)
    with c_c2:
        fig_pers = px.bar(df_planning, x='Étape du Chantier', y='Nb Personnel', text='Nb Personnel',
                          title="Nombre de Personnel Requis par Étape",
                          color='Nb Personnel', color_continuous_scale='Blues')
        st.plotly_chart(fig_pers, use_container_width=True)

with tab_fin:
    st.subheader("🏁 Accompagnement jusqu'à la Remise des Clés")
    st.write("Cochez les étapes au fur和 à mesure que votre chantier avance sur le terrain :")
    
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        e1 = st.checkbox("1. Implantation & Nettoyage")
        e2 = st.checkbox("2. Fouilles & Béton de propreté")
        e3 = st.checkbox("3. Fondation (Semelles & Longrines)")
        e4 = st.checkbox("4. Élévation des murs & Poteaux")
        e5 = st.checkbox("5. Coulage de la dalle / Toiture")
    with c_f2:
        e6 = st.checkbox("6. Portes, Fenêtres & Cloisons")
        e7 = st.checkbox("7. Électricité & Plomberie encastrée")
        e8 = st.checkbox("8. Enduits / Crépi des murs")
        e9 = st.checkbox("9. Carrelage & Peinture finale")
        e10 = st.checkbox("10. Remise des clés définitive 🔑")
        
    progression = sum([e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]) * 10
    st.progress(progression / 100, text=f"Progression globale : {progression}%")
    
    if progression == 100:
        st.balloons()
        st.success("🎉 Félicitations ! Votre maison est achevée avec succès !")

with tab_admin:
    st.subheader("📋 Historique des clients connectés")
    if os.path.exists("visiteurs.csv"):
        df_visiteurs = pd.read_csv("visiteurs.csv")
        st.write(f"Total clients enregistrés : **{len(df_visiteurs)}**")
        st.dataframe(df_visiteurs, use_container_width=True)
    else:
        st.info("Aucun client enregistré pour l'instant.")

# 7. RAPPORT TÉLÉCHARGEABLE
html_pdf = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Devis Complet mgGCAPP - {nom}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; }}
        .info {{ margin: 20px 0; background: #f8fafc; padding: 15px; border-radius: 5px; }}
        .warning {{ background: #fff3cd; color: #856404; padding: 10px; border: 1px solid #ffeeba; border-radius: 5px; margin-bottom: 15px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #1E3A8A; color: white; }}
        .total {{ font-weight: bold; background-color: #f1f5f9; }}
        .footer {{ margin-top: 30px; text-align: center; font-size: 0.9em; color: #555; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>🏗️ mgGCAPP — DEVIS GLOBAL DE CONSTRUCTION (DE A À Z)</h2>
    </div>
    <div class="warning">
        <b>Note importante :</b> La rémunération de la main-d'œuvre du technicien et des ouvriers n'est pas incluse dans ce devis matériaux.
    </div>
    <div class="info">
        <p><b>Client :</b> {nom} | <b>Tél :</b> {tel}</p>
        <p><b>Objectif :</b> {besoin_client}</p>
        <p><b>Projet :</b> {type_projet} ({surf_tot} m²) | <b>Ciment Total :</b> {sacs_ciment_total} sacs</p>
    </div>
    
    <h3>Détail complet des étapes et dépenses</h3>
    <table>
        <tr><th>Étape du Chantier</th><th>Dosage Ciment</th><th>Personnel Requis</th><th>Sacs</th><th>Coût ({devise})</th></tr>
"""

for idx, row in df_planning.iterrows():
    html_pdf += f"<tr><td>{row['Étape du Chantier']}</td><td>{row['Dosage Ciment']}</td><td>{row['Personnel Requis']}</td><td>{row['Sacs']}</td><td>{row['Coût Estimé']:,.0f}</td></tr>".replace(",", " ")

html_pdf += f"""
        <tr class="total">
            <td colspan="4">BUDGET TOTAL ESTIMÉ</td>
            <td>{total_global:,.0f} {devise}</td>
        </tr>
    </table>
    <div class="footer">
        <p><b>Besoin d'un accompagnement sur le terrain ou d'un plan ?</b> Contactez-nous au <b>+237 696 07 31 21</b></p>
        <p>Merci d’avoir utilisé <b>mgGCAPP</b> !</p>
    </div>
</body>
</html>
""".replace(",", " ")

st.divider()
col_dl, col_info = st.columns([1, 2])

with col_dl:
    st.download_button(
        label="📥 TÉLÉCHARGER LE RAPPORT COMPLET (.HTML)",
        data=html_pdf,
        file_name=f"Devis_Complet_{nom}_{type_projet}.html",
        mime="text/html",
        use_container_width=True
    )

with col_info:
    st.info("📐 **Besoin d'un plan de distribution sur mesure ou d'un accompagnement technique sur le terrain ?**\n\nContactez notre équipe au **696073121** (Appel / WhatsApp).")

# 8. REMERCIEMENT FINAL INCONTOURNABLE
st.markdown("---")
st.markdown(f"""
<div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 20px; border-radius: 10px; text-align: center;">
    <h3 style="color: #166534; margin-top: 0;">🙏 Merci infiniment, {nom} !</h3>
    <p style="font-size: 1.1em; color: #14532d;">
        Nous vous remercions chaleureusement d'avoir fait confiance à <b>mgGCAPP</b> pour votre projet.<br>
        Nous vous souhaitons un <b>magnifique succès</b> dans la réalisation de votre construction, du premier coup de pioche jusqu'à la remise des clés ! 🏗️🔑✨
    </p>
    <p style="font-size: 0.95em; color: #166534; margin-bottom: 0;">
        📞 Pour toute assistance, notre équipe est joignable directement au <b>696073121</b>.
    </p>
</div>
""", unsafe_allow_html=True)

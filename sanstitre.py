import streamlit as st
import pandas as pd
import plotly.express as px
import math, os
from datetime import datetime

# Configuration de l'application
st.set_page_config(page_title="mgGCAPP — Accompagnement Chantier BTP", page_icon="🏗️", layout="wide")

# 1. EN-TÊTE ET SALUTATION
heure = datetime.now().hour
salut = "Bonjour Monsieur" if 5 <= heure < 18 else "Bonsoir Monsieur"

st.title("🏗️ mgGCAPP — Votre Compagnon de Chantier de A à Z")
st.caption(f"✨ {salut}, bienvenue ! Pilotez votre projet de la fondation jusqu'à la remise des clés.")

st.divider()

# 2. SECTION AIDE & SUPPORT (HELP)
with st.expander("❓ **Besoin d'aide ou assistance (Aide / Help)**"):
    col_faq, col_contact = st.columns([2, 1], gap="medium")
    
    with col_faq:
        st.markdown("##### 📌 Guide d'accompagnement global")
        st.markdown("""
        - **De A à Z :** L'application vous guide à travers le gros œuvre, les ressources en ciment, le personnel et le second œuvre.
        - **Checklist interactive :** Suivez chaque étape directement sur le terrain pour ne rien oublier jusqu'à la réception des travaux.
        """)
    
    with col_contact:
        st.markdown("##### 📞 Contactez notre expert")
        whatsapp_url = "https://wa.me/237696073121?text=Bonjour,%20j'ai%20besoin%20d'un%20suivi%20de%20chantier%20sur%20mgGCAPP."
        st.markdown(f'''
            <a href="{whatsapp_url}" target="_blank">
                <button style="background-color:#25D366; color:white; border:none; padding:10px 15px; border-radius:5px; cursor:pointer; font-weight:bold; width:100%;">
                    💬 WhatsApp (696073121)
                </button>
            </a>
        ''', unsafe_allow_html=True)

st.divider()

# 3. PARAMÈTRES DU PROJET
st.subheader("📋 Paramètres du Projet de Construction")

col_a, col_b = st.columns([1, 2], gap="large")

with col_a:
    st.markdown("#### 1️⃣ Vos Coordonnées")
    nom = st.text_input("Nom & Prénom :", value="Client")
    tel = st.text_input("Téléphone / WhatsApp :", placeholder="+237...")

    if nom != "Client" and tel:
        fichier_csv = "visiteurs.csv"
        hdr = not os.path.exists(fichier_csv)
        pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Nom": nom, "Tel": tel}]).to_csv(
            fichier_csv, mode="a", header=hdr, index=False
        )

with col_b:
    st.markdown("#### 2️⃣ Ouvrage & Superficie")
    c_proj, c_surf = st.columns(2)
    with c_proj:
        type_projet = st.selectbox("Type de projet :", ["Plain-pied (RDC)", "R+1", "R+2", "R+2-1"])
    with c_surf:
        surf = st.number_input("Superficie au sol (m²) :", min_value=30, max_value=1500, value=100, step=10)

    st.markdown("#### 3️⃣ Répartition des pièces principales")
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

with st.expander("⚙️ Options avancées (Devise & Dosage Béton)"):
    co1, co2 = st.columns(2)
    with co1:
        dosage = st.selectbox("Dosage du Béton :", [300, 350, 400, 450], index=1, format_func=lambda x: f"{x} kg/m³")
    with co2:
        devise = st.selectbox("Devise d'affichage :", ["FCFA", "EUR (€)", "USD ($)"])

# 4. CALCULS GLOBAUX & RESSOURCES (CIMENT & PERSONNEL)
niveaux_dict = {"Plain-pied (RDC)": 1, "R+1": 2, "R+2": 3, "R+2-1": 2.5}
niveaux = niveaux_dict[type_projet]
surf_tot = surf * niveaux
perim = 4 * math.sqrt(surf) * 1.3
ratio_cloison = 1.0 + ((nb_chambres + nb_salons + nb_cuisines + nb_wc) * 0.05)
perim_effectif = perim * ratio_cloison

vol_beton = round((surf * 0.12) + (surf_tot * 0.05) + ((niveaux - 1) * surf * 0.15) + (perim_effectif * 0.45 * 0.45), 1)
sacs_ciment_total = math.ceil((vol_beton * dosage) / 50)
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

ciment_fouilles = round(sacs_ciment_total * 0.05)
ciment_fondation = round(sacs_ciment_total * 0.35)
ciment_elevation = round(sacs_ciment_total * 0.50)
ciment_toiture = sacs_ciment_total - (ciment_fouilles + ciment_fondation + ciment_elevation)

data_planning = [
    {
        "Étape du Chantier": "1. Préparation du terrain",
        "Personnel Requis": "2 Manœuvres + 1 Topographe",
        "Nb Personnel": 3,
        "Sacs de Ciment": 0,
        "Coût Estimé": int(surf * (3500 if is_fcfa else 6))
    },
    {
        "Étape du Chantier": "2. Fouilles & Tranchées",
        "Personnel Requis": "4 Manœuvres + 1 Chef d'équipe",
        "Nb Personnel": 5,
        "Sacs de Ciment": ciment_fouilles,
        "Coût Estimé": int(surf * (6000 if is_fcfa else 10))
    },
    {
        "Étape du Chantier": "3. Fondation (Semelles, Longrines)",
        "Personnel Requis": "2 Maçons + 5 Manœuvres + 1 Technicien",
        "Nb Personnel": 8,
        "Sacs de Ciment": ciment_fondation,
        "Coût Estimé": int((ciment_fondation * pu["Ciment"]) + (sable * pu["Sable"] * 0.3) + (gravier * pu["Gravier"] * 0.3))
    },
    {
        "Étape du Chantier": "4. Élévation (Murs, Poteaux, Dalles)",
        "Personnel Requis": "3 Maçons + 6 Manœuvres + 1 Technicien",
        "Nb Personnel": 10,
        "Sacs de Ciment": ciment_elevation,
        "Coût Estimé": int((ciment_elevation * pu["Ciment"]) + (agglos * pu["Agglos"]) + (acier_kg * pu["Acier"] * 0.6))
    },
    {
        "Étape du Chantier": "5. Toiture & Finitions de structure",
        "Personnel Requis": "2 Charpentiers + 3 Manœuvres",
        "Nb Personnel": 5,
        "Sacs de Ciment": ciment_toiture,
        "Coût Estimé": int((ciment_toiteur = ciment_toiture * pu["Ciment"]) if 'ciment_toiture' in locals() else 0 + (acier_kg * pu["Acier"] * 0.4) + surf * (12000 if is_fcfa else 20))
    }
]

df_planning = pd.DataFrame(data_planning)
total_global = int(df_planning["Coût Estimé"].sum())

st.divider()

# 5. ONGLETS D'ACCOMPAGNEMENT GLOBAL
tab_suivi, tab_courbes, tab_fin, tab_admin = st.tabs(["📊 Planning & Matériaux", "📈 Courbes (Ciment & Personnel)", "🏁 Suivi de Fin de Projet", "📁 Historique"])

with tab_suivi:
    st.subheader("📅 Tableau récapitulatif par étape de construction")
    st.warning("⚠️ **Avertissement :** Les chiffres ci-dessous indiquent les **matériaux et les besoins en personnel**. La main-d'œuvre du technicien et des ouvriers fait l'objet d'un accord salarial distinct.")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Ciment Total Requis", f"{sacs_ciment_total} sacs")
    m2.metric("Pic de Personnel", "10 ouvriers/techniciens")
    m3.metric("BUDGET GLOBAL ESTIMÉ", f"{total_global:,.0f} {devise}".replace(",", " "))

    st.dataframe(df_planning[["Étape du Chantier", "Personnel Requis", "Sacs de Ciment", "Coût Estimé"]], use_container_width=True)

with tab_courbes:
    st.subheader("📈 Courbes d'utilisation du Ciment et du Personnel")
    
    c_c1, c_c2 = st.columns(2)
    with c_c1:
        fig_ciment = px.line(df_planning, x='Étape du Chantier', y='Sacs de Ciment', markers=True, 
                             title="Courbe du Taux de Ciment par Étape (Sacs)",
                             color_discrete_sequence=['#D97706'])
        st.plotly_chart(fig_ciment, use_container_width=True)
    with c_c2:
        fig_pers = px.bar(df_planning, x='Étape du Chantier', y='Nb Personnel', text='Nb Personnel',
                          title="Nombre de Personnel Requis par Étape",
                          color='Nb Personnel', color_continuous_scale='Blues')
        st.plotly_chart(fig_pers, use_container_width=True)

with tab_fin:
    st.subheader("🏁 Accompagnement de la Fondation jusqu'à la Clé")
    st.write("Cochez les étapes franchies pour suivre l'avancement réel de votre chantier sur le terrain :")
    
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        st.markdown("##### 🧱 Gros Œuvre & Structure")
        e1 = st.checkbox("1. Implantation & Nettoyage du terrain")
        e2 = st.checkbox("2. Fouilles & Coulage du béton de propreté")
        e3 = st.checkbox("3. Fondation (Semelles & Longrines)")
        e4 = st.checkbox("4. Élévation des murs & Poteaux")
        e5 = st.checkbox("5. Coulage de la dalle / Pose de la toiture")
    
    with c_f2:
        st.markdown("##### 🎨 Second Œuvre & Finitions")
        e6 = st.checkbox("6. Portes, Fenêtres & Cloisons intérieures")
        e7 = st.checkbox("7. Installation électrique & Plomberie encastrée")
        e8 = st.checkbox("8. Crépi / Enduit des murs intérieurs et extérieurs")
        e9 = st.checkbox("9. Carrelage & Peinture finale")
        e10 = st.checkbox("10. Réception définitive des travaux & Remise des clés 🔑")
        
    progression = sum([e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]) * 10
    st.progress(progression / 100, text=f"Progression globale du chantier : {progression}%")
    
    if progression == 100:
        st.balloons()
        st.success("🎉 Félicitations ! Votre projet de construction est achevé avec succès grâce à mgGCAPP !")

with tab_admin:
    st.subheader("📋 Historique des Visiteurs")
    if os.path.exists("visiteurs.csv"):
        df_visiteurs = pd.read_csv("visiteurs.csv")
        st.write(f"Total prospects enregistrés : **{len(df_visiteurs)}**")
        st.dataframe(df_visiteurs, use_container_width=True)
    else:
        st.info("Aucun visiteur enregistré pour l'instant.")

# 6. RAPPORT HTML TÉLÉCHARGEABLE
html_pdf = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Accompagnement Chantier mgGCAPP</title>
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
        <h2>🏗️ mgGCAPP — RAPPORT D'ACCOMPAGNEMENT DE CHANTIER</h2>
    </div>
    <div class="warning">
        <b>Note importante :</b> La rémunération de la main-d'œuvre du technicien et des ouvriers n'est pas incluse dans ce devis de matériaux.
    </div>
    <div class="info">
        <p><b>Client :</b> {nom} | <b>Tél :</b> {tel}</p>
        <p><b>Projet :</b> {type_projet} ({surf_tot} m²) | <b>Ciment Total :</b> {sacs_ciment_total} sacs</p>
    </div>
    
    <h3>Détail des étapes, ciment et personnel</h3>
    <table>
        <tr><th>Étape du Chantier</th><th>Personnel Requis</th><th>Sacs de Ciment</th><th>Coût Estimé ({devise})</th></tr>
"""

for idx, row in df_planning.iterrows():
    html_pdf += f"<tr><td>{row['Étape du Chantier']}</td><td>{row['Personnel Requis']}</td><td>{row['Sacs de Ciment']}</td><td>{row['Coût Estimé']:,.0f}</td></tr>".replace(",", " ")

html_pdf += f"""
        <tr class="total">
            <td colspan="3">BUDGET GLOBAL ESTIMÉ</td>
            <td>{total_global:,.0f} {devise}</td>
        </tr>
    </table>
    <div class="footer">
        <p><b>Besoin d'un plan de distribution ou d'un suivi personnalisé ?</b> Contactez-nous au <b>+237 696 07 31 21</b></p>
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
        file_name=f"Accompagnement_Chantier_{nom}_{type_projet}.html",
        mime="text/html",
        use_container_width=True
    )

with col_info:
    st.info("📐 **Besoin d'un plan de distribution sur mesure ou d'un accompagnement technique sur le terrain ?**\n\nContactez notre équipe au **696073121** (Appel / WhatsApp).")

# 7. REMERCIEMENT FINAL INCONTOURNABLE
st.markdown("---")
st.markdown(f"""
<div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 20px; border-radius: 10px; text-align: center;">
    <h3 style="color: #166534; margin-top: 0;">🙏 Merci infiniment, {nom} !</h3>
    <p style="font-size: 1.1em; color: #14532d;">
        Nous vous remercions d'avoir choisi <b>mgGCAPP</b> pour vous accompagner dans votre projet de construction.<br>
        Nous vous souhaitons un <b>excellent succès</b> dans la réalisation de votre chantier, de la fondation jusqu'à la remise des clés ! 🏗️🔑✨
    </p>
    <p style="font-size: 0.95em; color: #166534; margin-bottom: 0;">
        📞 Pour tout besoin d'accompagnement ou de suivi, contactez notre équipe au <b>696073121</b>.
    </p>
</div>
""", unsafe_allow_html=True)

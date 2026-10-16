import streamlit as st
import pandas as pd
import math, os
from datetime import datetime

# Configuration de l'application
st.set_page_config(page_title="mgGCAPP — Devis Express BTP", page_icon="🏗️", layout="wide")

# 1. EN-TÊTE ET SALUTATION
heure = datetime.now().hour
salut = "Bonjour Monsieur" if 5 <= heure < 18 else "Bonsoir Monsieur"

st.title("🏗️ mgGCAPP — Devis Express & Analyse BTP")
st.caption(f"✨ {salut}, bienvenue ! Obtenez votre devis et analysez les données de votre projet.")

st.divider()

# 2. SECTION AIDE & SUPPORT (HELP / ASSISTANCE)
with st.expander("❓ **Besoin d'aide ou problème sur le site ? (Aide / Help)**"):
    col_faq, col_contact = st.columns([2, 1], gap="medium")
    
    with col_faq:
        st.markdown("##### 📌 Foire Aux Questions (FAQ)")
        st.markdown("""
        - **Comment sont calculés les matériaux ?** Les quantités sont estimées selon les normes BTP adaptées à la superficie et au nombre de pièces.
        - **Comment télécharger le devis ?** Cliquez sur le bouton de téléchargement en bas pour enregistrer votre document.
        """)
    
    with col_contact:
        st.markdown("##### 📞 Assistance Directe")
        st.write("Une question ou une difficulté technique ?")
        whatsapp_url = "https://wa.me/237696073121?text=Bonjour,%20j'ai%20besoin%20d'aide%20sur%20le%20site%20mgGCAPP."
        st.markdown(f'''
            <a href="{whatsapp_url}" target="_blank">
                <button style="background-color:#25D366; color:white; border:none; padding:10px 15px; border-radius:5px; cursor:pointer; font-weight:bold; width:100%;">
                    💬 Discuter sur WhatsApp (696073121)
                </button>
            </a>
        ''', unsafe_allow_html=True)

st.divider()

# 3. SAISIE ET COLLECTE DES DONNÉES
st.subheader("📋 Vos informations & Détails du projet")

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
    st.markdown("#### 2️⃣ Type d'ouvrage & Superficie")
    c_proj, c_surf = st.columns(2)
    with c_proj:
        type_projet = st.selectbox("Type de projet :", ["Plain-pied (RDC)", "R+1", "R+2", "R+2-1"])
    with c_surf:
        surf = st.number_input("Superficie à construire (m²) :", min_value=30, max_value=1500, value=100, step=10)

    st.markdown("#### 3️⃣ Répartition des pièces")
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

with st.expander("⚙️ Préférences techniques et devises (Optionnel)"):
    co1, co2 = st.columns(2)
    with co1:
        dosage = st.selectbox("Dosage du Béton :", [300, 350, 400, 450], index=1, format_func=lambda x: f"{x} kg/m³")
    with co2:
        devise = st.selectbox("Devise d'affichage :", ["FCFA", "EUR (€)", "USD ($)"])

# 4. CALCULS DU DEVIS
niveaux_dict = {"Plain-pied (RDC)": 1, "R+1": 2, "R+2": 3, "R+2-1": 2.5}
niveaux = niveaux_dict[type_projet]
surf_tot = surf * niveaux
perim = 4 * math.sqrt(surf) * 1.3

ratio_cloison = 1.0 + ((nb_chambres + nb_salons + nb_cuisines + nb_wc) * 0.05)
perim_effectif = perim * ratio_cloison

vol_beton = round((surf * 0.12) + (surf_tot * 0.05) + ((niveaux - 1) * surf * 0.15) + (perim_effectif * 0.45 * 0.45), 1)
sacs_ciment = math.ceil((vol_beton * dosage) / 50)
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

data = [
    {"Matériau": "Ciment CPJ", "Unité": "Sacs 50kg", "Qté": sacs_ciment, "P.U": pu["Ciment"], "Total": int(sacs_ciment * pu["Ciment"])},
    {"Matériau": "Sable propre", "Unité": "m³", "Qté": sable, "P.U": pu["Sable"], "Total": int(round(sable * pu["Sable"]))},
    {"Matériau": "Gravier concassé", "Unité": "m³", "Qté": gravier, "P.U": pu["Gravier"], "Total": int(round(gravier * pu["Gravier"]))},
    {"Matériau": "Aciers HA FeE500", "Unité": "Kg", "Qté": acier_kg, "P.U": pu["Acier"], "Total": int(acier_kg * pu["Acier"])},
    {"Matériau": "Agglos creux", "Unité": "Unités", "Qté": agglos, "P.U": pu["Agglos"], "Total": int(agglos * pu["Agglos"])},
]

df = pd.DataFrame(data)
total_ht = int(df["Total"].sum())

st.divider()

# 5. ONGLETS DEVIS & ANALYSE NATIVE
tab_devis, tab_analyse, tab_admin = st.tabs(["📊 Devis Estimatif", "📈 Analyse des Coûts", "📁 Historique Visiteurs"])

with tab_devis:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Béton Total", f"{vol_beton} m³")
    m2.metric("Ciment Requis", f"{sacs_ciment} sacs")
    m3.metric("Aciers", f"{acier_kg} kg")
    m4.metric("TOTAL ESTIMÉ", f"{total_ht:,.0f} {devise}".replace(",", " "))

    st.dataframe(df, use_container_width=True)

with tab_analyse:
    st.subheader("📊 Visualisation graphique du budget")
    # Graphique en barres natif de Streamlit (rapide et sans bug)
    chart_data = df.set_index("Matériau")["Total"]
    st.bar_chart(chart_data)

with tab_admin:
    st.subheader("📋 Visiteurs enregistrés")
    if os.path.exists("visiteurs.csv"):
        df_visiteurs = pd.read_csv("visiteurs.csv")
        st.write(f"Total des prospects : **{len(df_visiteurs)}**")
        st.dataframe(df_visiteurs, use_container_width=True)
    else:
        st.info("Aucune donnée visiteur pour le moment.")

# 6. TÉLÉCHARGEMENT DU DEVIS HTML
html_pdf = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Devis Estimatif mgGCAPP</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; }}
        .info {{ margin: 20px 0; background: #f8fafc; padding: 15px; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #1E3A8A; color: white; }}
        .total {{ font-weight: bold; background-color: #f1f5f9; }}
        .footer {{ margin-top: 30px; text-align: center; font-size: 0.9em; color: #555; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>🏗️ mgGCAPP — DEVIS ESTIMATIF RAPIDE</h2>
    </div>
    <div class="info">
        <p><b>Client :</b> {nom} | <b>Tél :</b> {tel}</p>
        <p><b>Projet :</b> {type_projet} ({surf_tot} m²) | <b>Dosage Béton :</b> {dosage} kg/m³</p>
        <p><b>Distribution :</b> {nb_chambres} Ch. | {nb_salons} Salon(s) | {nb_cuisines} Cuis. | {nb_wc} WC | {nb_verandas} Véranda(s)</p>
    </div>
    <table>
        <tr>
            <th>Matériau</th>
            <th>Unité</th>
            <th>Quantité</th>
            <th>P.U ({devise})</th>
            <th>Total HT ({devise})</th>
        </tr>
"""

for r in data:
    html_pdf += f"""
        <tr>
            <td>{r['Matériau']}</td>
            <td>{r['Unité']}</td>
            <td>{r['Qté']}</td>
            <td>{r['P.U']:,.0f}</td>
            <td>{r['Total']:,.0f}</td>
        </tr>
    """.replace(",", " ")

html_pdf += f"""
        <tr class="total">
            <td colspan="4">TOTAL GÉNÉRAL ESTIMÉ</td>
            <td>{total_ht:,.0f} {devise}</td>
        </tr>
    </table>
    <div class="footer">
        <p><b>Besoin d'un plan de distribution adapté à vos besoins ?</b> Contactez-nous au <b>+237 696 07 31 21</b></p>
        <p>Merci d’avoir utilisé <b>mgGCAPP</b> !</p>
    </div>
</body>
</html>
""".replace(",", " ")

st.divider()
col_dl, col_info = st.columns([1, 2])

with col_dl:
    st.download_button(
        label="📥 TÉLÉCHARGER LE DEVIS (.HTML / PDF)",
        data=html_pdf,
        file_name=f"Devis_{nom}_{type_projet}.html",
        mime="text/html",
        use_container_width=True
    )

with col_info:
    st.info("📐 **Vous souhaitez un plan de distribution personnalisé pour votre projet ?**\n\nContactez notre équipe au **696073121** (Appel / WhatsApp).")

st.markdown("---")
st.success(f"🤝 **Merci pour votre confiance, {nom} !** Bon succès dans la réalisation de votre projet !")

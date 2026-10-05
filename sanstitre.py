import streamlit as st
import pandas as pd
import math, os
from datetime import datetime

# Page Streamlit simple
st.set_page_config(page_title="mgGCAPP — Devis Express", page_icon="🏗️", layout="centered")

st.title("🏗️ mgGCAPP — Devis Express BTP")
st.caption("Obtenez une estimation rapide des matériaux pour votre construction.")

# 1. COORDONNÉES
st.subheader("1. Vos informations")
nom = st.text_input("Nom & Prénom :", value="Client")
tel = st.text_input("Téléphone / WhatsApp :", placeholder="+237...")

# Sauvegarde simple des visiteurs
if nom != "Client" and tel:
    fichier_csv = "visiteurs.csv"
    hdr = not os.path.exists(fichier_csv)
    pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Nom": nom, "Tel": tel}]).to_csv(
        fichier_csv, mode="a", header=hdr, index=False
    )

# 2. CARACTÉRISTIQUES DU BÂTIMENT
st.subheader("2. Votre projet")
c1, c2 = st.columns(2)
with c1:
    type_projet = st.selectbox("Type d'ouvrage", ["Plain-pied (RDC)", "R+1", "R+2", "R+2-1"])
with c2:
    surf = st.number_input("Superficie au sol (m²)", min_value=20, max_value=2000, value=100, step=10)

# 3. DISTRIBUTION DES PIÈCES
st.subheader("3. Nombre de pièces")
p1, p2, p3 = st.columns(3)
with p1:
    nb_chambres = st.number_input("Chambres", min_value=1, value=3)
    nb_wc = st.number_input("Toilettes / WC", min_value=1, value=2)
with p2:
    nb_salons = st.number_input("Salons", min_value=1, value=1)
    nb_verandas = st.number_input("Vérandas", min_value=0, value=1)
with p3:
    nb_cuisines = st.number_input("Cuisines", min_value=1, value=1)

# Options cachées par défaut pour ne pas alourdir
with st.expander("⚙️ Options avancées (Devise & Dosage)"):
    dosage = st.selectbox("Dosage Ciment", [300, 350, 400], index=1, format_func=lambda x: f"{x} kg/m³")
    devise = st.selectbox("Devise", ["FCFA", "EUR (€)", "USD ($)"])

# 4. CALCULS
niveaux_dict = {"Plain-pied (RDC)": 1, "R+1": 2, "R+2": 3, "R+2-1": 2.5}
niveaux = niveaux_dict[type_projet]
surf_tot = surf * niveaux
perim = 4 * math.sqrt(surf) * 1.3
perim_effectif = perim * (1.0 + ((nb_chambres + nb_salons + nb_cuisines + nb_wc) * 0.05))

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
    {"Matériau": f"Ciment (Dosage {dosage} kg/m³)", "Unité": "Sacs", "Qté": sacs_ciment, "P.U": pu["Ciment"], "Total": int(sacs_ciment * pu["Ciment"])},
    {"Matériau": "Sable propre", "Unité": "m³", "Qté": sable, "P.U": pu["Sable"], "Total": int(round(sable * pu["Sable"]))},
    {"Matériau": "Gravier concassé", "Unité": "m³", "Qté": gravier, "P.U": pu["Gravier"], "Total": int(round(gravier * pu["Gravier"]))},
    {"Matériau": "Aciers HA FeE500", "Unité": "Kg", "Qté": acier_kg, "P.U": pu["Acier"], "Total": int(acier_kg * pu["Acier"])},
    {"Matériau": "Agglos creux", "Unité": "Unités", "Qté": agglos, "P.U": pu["Agglos"], "Total": int(agglos * pu["Agglos"])},
]

df = pd.DataFrame(data)
total_ht = int(df["Total"].sum())

# 5. RÉSULTAT
st.divider()
st.subheader("📊 Résumé du devis")

m1, m2 = st.columns(2)
m1.metric("Béton Estimé", f"{vol_beton} m³")
m2.metric("TOTAL ESTIMÉ", f"{total_ht:,.0f} {devise}".replace(",", " "))

st.table(df[["Matériau", "Unité", "Qté", "Total"]])

# 6. TÉLÉCHARGEMENT SIMPLIFIÉ (FICHIER TXT / REÇU)
texte_devis = f"""==================================
        mgGCAPP — DEVIS ESTIMATIF
==================================
Client : {nom}
Téléphone : {tel}
Projet : {type_projet} ({surf_tot} m²)
Pièces : {nb_chambres} Ch | {nb_salons} Sal | {nb_cuisines} Cuis | {nb_wc} WC | {nb_verandas} Ver

----------------------------------
DÉTAIL DES MATÉRIAUX :
- Ciment : {sacs_ciment} sacs
- Sable : {sable} m³
- Gravier : {gravier} m³
- Acier : {acier_kg} kg
- Agglos : {agglos} unités

==================================
TOTAL ESTIMÉ : {total_ht:,.0f} {devise}
==================================

Besoin d'un plan de distribution sur-mesure ?
Contactez notre architecte au : 696073121 (WhatsApp)
"""

st.download_button(
    label="📥 Télécharger le Devis (Format Fichier Texte)",
    data=texte_devis,
    file_name=f"Devis_{nom}.txt",
    mime="text/plain"
)

# 7. ASSISTANCE & CONTACT
st.divider()
st.info("📐 **Besoin d'un plan de distribution ou d'aide ?** Contactez-nous au **696073121** (Appel / WhatsApp).")

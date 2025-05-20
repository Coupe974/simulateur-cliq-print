import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Titre de l'application
st.title("📸 Simulateur de revenus - Cliq & Print")

st.markdown("""
Ce simulateur te permet d'estimer tes revenus en fonction de ta cadence photo, du prix de vente, et de ton rythme de travail.
""")

# Entrées utilisateur
prix_photo = st.slider("💰 Prix par photo", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
photos_par_heure = st.slider("📷 Photos par heure", min_value=1, max_value=30, value=12)
heures_par_jour = st.slider("⏰ Heures de travail par jour", min_value=1, max_value=12, value=4)
jours_par_semaine = st.slider("📅 Jours de travail par semaine", min_value=1, max_value=7, value=7)
semaines_par_mois = st.slider("🗓️ Semaines par mois", min_value=2.0, max_value=5.0, value=4.33, step=0.1)
taux_ursaff = 0.062
cout_unitaire_photo = 0.30

# Calculs
total_photos_par_jour = photos_par_heure * heures_par_jour
total_photos_par_mois = total_photos_par_jour * jours_par_semaine * semaines_par_mois
ca_brut = total_photos_par_mois * prix_photo
ca_brut_par_jour = total_photos_par_jour * prix_photo
charges_matieres = total_photos_par_mois * cout_unitaire_photo
cotisations_ursaff = ca_brut * taux_ursaff
benefice_net = ca_brut - charges_matieres
benefice_net_net = benefice_net - cotisations_ursaff

# Résultats
st.markdown("## Résultats mensuels estimés")
st.metric("📦 Chiffre d'affaires brut (mois)", f"{ca_brut:.2f} €")
st.metric("📆 Chiffre d'affaires brut (jour)", f"{ca_brut_par_jour:.2f} €")
st.metric("🧾 Nombre total de photos/mois", f"{int(total_photos_par_mois)}")
st.metric("💸 Charges photo (papier/encre)", f"{charges_matieres:.2f} €")
st.metric("📉 URSSAF (6.2%)", f"{cotisations_ursaff:.2f} €")
st.metric("💵 Bénéfice net (avant URSSAF)", f"{benefice_net:.2f} €")
st.metric("✅ Bénéfice net net (dans ta poche)", f"{benefice_net_net:.2f} €")

# Visualisation - Répartition
st.markdown("## Répartition des revenus")
labels = ['Charges (matières)', 'URSSAF', 'Bénéfice net net']
values = [charges_matieres, cotisations_ursaff, benefice_net_net]
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Visualisation - Comparaison par jour
st.markdown("## Simulation journalière sur une semaine")
days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
revenus_journaliers = [ca_brut_par_jour] * 7
benefices_journaliers = [(ca_brut_par_jour - (total_photos_par_jour * cout_unitaire_photo)) * (1 - taux_ursaff)] * 7

fig2, ax2 = plt.subplots()
x = np.arange(len(days))
width = 0.35
ax2.bar(x - width/2, revenus_journaliers, width, label='CA brut/jour')
ax2.bar(x + width/2, benefices_journaliers, width, label='Bénéfice net net/jour')
ax2.set_ylabel('Montants (€)')
ax2.set_title('CA brut et bénéfice net net par jour')
ax2.set_xticks(x)
ax2.set_xticklabels(days)
ax2.legend()
st.pyplot(fig2)

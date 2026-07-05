import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Simulation Lunette Afocale", layout="centered")
st.title("🔭 Modélisation d'une Lunette Astronomique Afocale")
st.write("Ajustez les caractéristiques des lentilles pour observer la formation de l'image et le grossissement.")

# Barre latérale pour les paramètres optiques
st.sidebar.header("Caractéristiques des Lentilles")
f1_prime = st.sidebar.slider("Distance focale Objectif f'1 (cm) :", 10.0, 50.0, 30.0, 1.0)
f2_prime = st.sidebar.slider("Distance focale Oculaire f'2 (cm) :", 2.0, 15.0, 7.5, 0.5)

st.sidebar.header("Faisceau Incident")
theta_deg = st.sidebar.slider("Angle d'incidence θ (degrés) :", 1.0, 10.0, 4.0, 0.5)

# Calculs optiques
theta_rad = np.radians(theta_deg)
# Condition d'afocalité : distance entre lentilles = f'1 + f'2
encombrement = f1_prime + f2_prime

# Position des éléments sur l'axe optique (x)
x_L1 = 0.0
x_F1p_F2 = f1_prime
x_L2 = encombrement

# Taille de l'image intermédiaire A'B' au foyer commun
# tan(theta) ~= theta = A'B' / f'1  => A'B' = f'1 * theta
y_Bprime = - f1_prime * np.tan(theta_rad) # compté négativement vers le bas

# Angle de sortie theta'
# tan(theta') ~= theta' = A'B' / f'2  => theta' = A'B' / f'2
theta_prime_rad = abs(y_Bprime) / f2_prime
theta_prime_deg = np.degrees(theta_prime_rad)

# Calcul du grossissement G
grossissement = f1_prime / f2_prime

# --- TRACÉ DU SCHÉMA OPTIQUE ---
fig, ax = plt.subplots(figsize=(11, 5))

# Axe optique
ax.axhline(0, color='black', linestyle='-', linewidth=1)

# Représentation des lentilles (lignes verticales)
ax.axvline(x_L1, color='#2b6cb0', linewidth=2.5, label="Objectif (L1)")
ax.axvline(x_L2, color='#319795', linewidth=2.5, label="Oculaire (L2)")

# Points remarquables
ax.plot(x_F1p_F2, 0, 'ro', markersize=6)
ax.text(x_F1p_F2, 0.5, "F'_1 = F_2", color='red', fontsize=10, ha='center')
ax.text(x_L1, -1.5, "L1", color='#2b6cb0', fontsize=12, fontweight='bold', ha='center')
ax.text(x_L2, -1.5, "L2", color='#319795', fontsize=12, fontweight='bold', ha='center')

# Trace de l'image intermédiaire A'B'
ax.vlines(x_F1p_F2, 0, y_Bprime, color='purple', linewidth=2, label="Image intermédiaire (A'B')")

# --- TRACÉ DES RAYONS LUMINEUX ---
# 1. Rayon passant par le centre optique de L1 (O1) -> non dévié jusqu'à B' puis vers L2
x_ray1 = [x_L1 - 10, x_L1, x_F1p_F2, x_L2]
y_ray1 = [10 * np.tan(theta_rad), 0, y_Bprime, y_Bprime + f2_prime * np.tan(theta_prime_rad)]
ax.plot(x_ray1, y_ray1, color='orange', linestyle='-', alpha=0.8)

# 2. Rayon incident parallèle à l'axe passant par le haut de L1 (juste pour le visuel du faisceau)
y_top = 3.0
x_ray2 = [x_L1 - 10, x_L1, x_F1p_F2, x_L2]
# Il doit croiser l'axe au foyer F'1 puis passer par B'
# Pour simplifier le tracé complet du faisceau infini, on simule 3 rayons parallèles se croisant en B'
# Rayon parallèle supérieur arrivant en O1 décalé :
ax.plot([x_L1-10, x_L1, x_F1p_F2], [y_top + 10*np.tan(theta_rad), y_top, y_Bprime], color='orange', linestyle='-', alpha=0.5)

# Extension des rayons émergents de L2 (faisceau parallèle vers l'œil)
x_sortie = [x_L2, x_L2 + 15]
y_s1 = [y_ray1[-1], y_ray1[-1] + 15 * np.tan(theta_rad * grossissement)]
ax.plot(x_sortie, y_s1, color='orange', linestyle='-', linewidth=2, label="Rayons émergents (parallèles)")

# Limites et esthétique du graphique
ax.set_title("Marche des rayons dans une lunette afocale", fontsize=12, fontweight='bold')
ax.set_xlabel("Axe optique x (cm)", fontsize=10)
ax.set_xlim(x_L1 - 15, x_L2 + 20)
ax.set_ylim(-6, 6)
ax.grid(True, linestyle=':', alpha=0.5)
ax.get_yaxis().set_visible(False) # On masque l'axe Y gradué non pertinent en optique géométrique
ax.legend(loc="upper left")

st.pyplot(fig)

# --- BILAN PÉDAGOGIQUE ---
st.subheader("📊 Propriétés du système optique :")
col1, col2, col3 = st.columns(3)
col1.metric("Distance L1 - L2 (Afocalité) :", f"{encombrement:.1f} cm")
col2.metric("Angle de sortie θ' :", f"{theta_prime_deg:.1f} °")
col3.metric("Grossissement nominal G :", f"{grossissement:.2f} ×")

st.info(f"💡 **Observation :** L'objet étant à l'infini, l'image intermédiaire se forme dans le plan focal de l'objectif. "
        f"L'oculaire renvoie cette image à l'infini, ce qui permet une observation **sans fatigue oculaire** (l'œil n'a pas besoin d'accommoder).")

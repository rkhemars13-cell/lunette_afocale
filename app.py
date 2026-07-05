import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Simulation Lunette Afocale", layout="centered")
st.title("🔭 Modélisation d'une Lunette Astronomique Afocale")
st.write("Modélisation rigoureuse : tracé exact des rayons conjugués et des prolongements à l'infini.")

# Barre latérale pour les paramètres optiques
st.sidebar.header("Caractéristiques des Lentilles")
f1_prime = st.sidebar.slider("Distance focale Objectif f'1 (cm) :", 15.0, 50.0, 30.0, 1.0)
f2_prime = st.sidebar.slider("Distance focale Oculaire f'2 (cm) :", 3.0, 15.0, 7.5, 0.5)

st.sidebar.header("Faisceau Incident")
theta_deg = st.sidebar.slider("Angle d'incidence θ (degrés) :", 1.0, 8.0, 4.0, 0.5)

# --- CALCULS OPTIQUES RIGOUREUX ---
theta_rad = np.radians(theta_deg)
encombrement = f1_prime + f2_prime

x_L1 = 0.0
x_F1p_F2 = f1_prime
x_L2 = encombrement

# Position de l'image intermédiaire B' (foyer commun)
y_Bprime = - f1_prime * np.tan(theta_rad)

# Angle de sortie réel theta' (Loi des lentilles : tan(theta') = |A'B'| / f'2)
theta_prime_rad = abs(y_Bprime) / f2_prime
theta_prime_deg = np.degrees(theta_prime_rad)
grossissement = f1_prime / f2_prime

# --- TRACÉ DU SCHÉMA OPTIQUE ---
fig, ax = plt.subplots(figsize=(11, 5))

# Axe optique
ax.axhline(0, color='black', linestyle='-', linewidth=1)

# Représentation des lentilles (lignes verticales avec flèches)
ax.axvline(x_L1, color='#2b6cb0', linewidth=2.5)
ax.axvline(x_L2, color='#319795', linewidth=2.5)
ax.text(x_L1, 5.2, "Objective (L1)", color='#2b6cb0', fontsize=10, ha='center', fontweight='bold')
ax.text(x_L2, 5.2, "Oculaire (L2)", color='#319795', fontsize=10, ha='center', fontweight='bold')

# Points remarquables
ax.plot(x_F1p_F2, 0, 'ro', markersize=5)
ax.text(x_F1p_F2, 0.3, "F'_1 = F_2", color='red', fontsize=10, ha='center')
ax.plot(x_L1, 0, 'ko', markersize=4)
ax.text(x_L1, -0.5, "O_1", fontsize=9, ha='right')
ax.plot(x_L2, 0, 'ko', markersize=4)
ax.text(x_L2, -0.5, "O_2", fontsize=9, ha='right')

# Image intermédiaire A'B'
ax.vlines(x_F1p_F2, 0, y_Bprime, color='purple', linewidth=2.5, label="Image intermédiaire (A'B')")

# --- TRACÉ DES RAYONS EXACTS ---

# RAYON 1 : Passe par O1 (non dévié) -> va jusqu'à B' -> puis frappe L2
y_L2_ray1 = y_Bprime + (x_L2 - x_F1p_F2) * (y_Bprime / f1_prime)
# Avant L1
ax.plot([x_L1 - 15, x_L1], [15 * np.tan(theta_rad), 0], color='orange', linestyle='-')
# Entre L1 et L2 (passe par B')
ax.plot([x_L1, x_L2], [0, y_L2_ray1], color='orange', linestyle='-')

# RAYON 2 : Arrive parallèlement au Rayon 1 et frappe L1 en son centre supérieur (y=3)
y_L1_top = 2.5
# Avant L1
ax.plot([x_L1 - 15, x_L1], [y_L1_top + 15 * np.tan(theta_rad), y_L1_top], color='orange', linestyle='-')
# Après L1, ce rayon converge obligatoirement vers B' puis continue vers L2
y_L2_ray2 = y_L1_top + (y_Bprime - y_L1_top) * (x_L2 / f1_prime)
ax.plot([x_L1, x_L2], [y_L1_top, y_L2_ray2], color='orange', linestyle='-')

# --- MARCHE DES RAYONS APRÈS L'OCULAIRE (L2) ---
# Tous les rayons émergents ressortent parallèles entre eux, inclinés de l'angle theta'
x_max = x_L2 + 15

# Rayon issu de O2 : part de B', passe par O2 (le centre de L2 donc NON DÉVIÉ)
# Sa pente est exactement tan(theta') dirigée vers le haut
ax.plot([x_F1p_F2, x_L2], [y_Bprime, 0], color='green', linestyle='-', linewidth=1.5, label="Rayon directeur (par O_2)")
ax.plot([x_L2, x_max], [0, 15 * np.tan(theta_prime_rad)], color='green', linestyle='-')

# Émergence du Rayon 1 (parallèle au rayon de O2)
y_sortie_ray1 = y_L2_ray1 + 15 * np.tan(theta_prime_rad)
ax.plot([x_L2, x_max], [y_L2_ray1, y_sortie_ray1], color='orange', linestyle='-')

# Émergence du Rayon 2 (parallèle au rayon de O2)
y_sortie_ray2 = y_L2_ray2 + 15 * np.tan(theta_prime_rad)
ax.plot([x_L2, x_max], [y_L2_ray2, y_sortie_ray2], color='orange', linestyle='-', label="Rayons réels émergents")

# --- TRACÉ DES POINTILLÉS VERS L'INFINI (IMAGE VIRTUELLE) ---
# On prolonge les rayons émergents vers l'arrière (vers la gauche) pour montrer l'infini à l'œil
x_inf = x_L2 - 10
ax.plot([x_inf, x_L2], [0 - 10 * np.tan(theta_prime_rad), 0], color='green', linestyle=':', alpha=0.7)
ax.plot([x_inf, x_L2], [y_L2_ray1 - 10 * np.tan(theta_prime_rad), y_L2_ray1], color='orange', linestyle=':', alpha=0.7)
ax.plot([x_inf, x_L2], [y_L2_ray2 - 10 * np.tan(theta_prime_rad), y_L2_ray2], color='orange', linestyle=':', alpha=0.7, label="Prolongements (Image à l'infini)")

# Configuration axe et affichage
ax.set_xlim(x_L1 - 15, x_max + 2)
ax.set_ylim(-5.5, 5.5)
ax.grid(True, linestyle=':', alpha=0.4)
ax.get_yaxis().set_visible(False)
ax.legend(loc="lower left", fontsize=9)

st.pyplot(fig)

# --- BILAN PÉDAGOGIQUE ---
st.subheader("📊 Propriétés du système optique :")
col1, col2, col3 = st.columns(3)
col1.metric("Distance L1 - L2 (Afocalité) :", f"{encombrement:.1f} cm")
col2.metric("Angle de sortie θ' :", f"{theta_prime_deg:.1f} °")
col3.metric("Grossissement nominal G :", f"{grossissement:.2f} ×")

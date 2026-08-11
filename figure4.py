# -*- coding: utf-8 -*-
"""
Python code accompanying the paper:

"Efficiency Ratio Map"

This script generates Figure 4.

Author:
 Tri Tran

License:
MIT
"""

import matplotlib.pyplot as plt
import numpy as np

#h(theta, phi)   [Eqs. (5)-(6)]
def hdivider(theta, phi):
    return (1 + phi) * ((1 + theta) / (2 + theta))


def hbridge(theta, phi):
    return (1 + phi) * (((1 + theta) / (2 + theta)) - 0.5)


#efficiency finite differences  [Eq. (4)]
#        E = |dh/dtheta| / |dh/dphi|

H = 1e-10  # finite-difference step

def efficiency(func, theta, phi):
    tinynumber = 1e-10
    d_theta = (func(theta + tinynumber, phi) - func(theta, phi)) / tinynumber
    d_phi = (func(theta, phi + tinynumber) - func(theta, phi)) / tinynumber
    return np.abs(d_theta) / np.abs(d_phi)



# 3. Parameter Grid & Data Generation

thetavalues = np.linspace(0.1, 5.0, 10)
phivalues = np.linspace(0.1, 5.0, 15)

ratio_grid = np.zeros((15, 10))
for i in range(15):
    for j in range(10):
        e_bridge = efficiency(hbridge, thetavalues[j], phivalues[i])
        e_divider = efficiency(hdivider, thetavalues[j], phivalues[i])
        ratio_grid[i, j] = e_bridge / e_divider



# 4. Plotting Setup


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6), dpi=300)

# --- Panel (a): Efficiency Ratio Map ---
pcm = ax1.pcolormesh(thetavalues, phivalues, ratio_grid, cmap='YlGn')
cb = fig.colorbar(pcm, ax=ax1, pad=0.02)
cb.set_label(r'$R_E=E_{\mathrm{bridge}}/E_{\mathrm{div}}$', fontsize=14)
cb.ax.tick_params(labelsize=12)

ax1.set_xlabel(r'$\theta$  (normalized resistance variation)', fontsize=14)
ax1.set_ylabel(r'$\varphi$  (normalized voltage variation)', fontsize=14)
ax1.set_title('(a)  Efficiency-ratio map', fontsize=15, pad=8)
ax1.tick_params(labelsize=12)

# --- Panel (b): RE vs Theta ---
theta_fine = np.linspace(0.1, 5.0, 400)
closed_form_y = 2.0 * (1.0 + theta_fine) / theta_fine

ax2.plot(
    theta_fine,
    closed_form_y,
    '-',
    linewidth=2.4,
    label=r'Closed form  $2|1+\theta|/|\theta|$  (Eq. 9)',
    zorder=1,
)

phi_targets = [0.1, 2.5, 5.0]
markers = ['o', 's', '^']
colors = ['#0e5c46', '#1a9e79', '#b8860b']

for phi_val, marker, color in zip(phi_targets, markers, colors):
    numerical_y = []
    for theta_val in thetavalues:
        ratio = efficiency(hbridge, theta_val, phi_val) / efficiency(
            hdivider, theta_val, phi_val
        )
        numerical_y.append(ratio)

    ax2.plot(
        thetavalues,
        numerical_y,
        marker,
        color=color,
        markersize=8,
        markerfacecolor='white',
        markeredgewidth=2,
        label=rf'Numerical, $\varphi={phi_val}$',
        zorder=3,
    )

ax2.set_xlabel(r'$\theta$  (normalized resistance variation)', fontsize=14)
ax2.set_ylabel(r'$R_E$', fontsize=14)
ax2.set_title(r'(b)  $R_E$ is independent of $\varphi$', fontsize=15, pad=8)
ax2.set_yscale('log')
ax2.grid(True, which='both', linestyle=':', alpha=0.5)
ax2.legend(fontsize=11, framealpha=0.95)
ax2.tick_params(labelsize=12)

plt.tight_layout()
plt.show()

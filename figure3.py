# -*- coding: utf-8 -*-
"""
Python code accompanying the paper:

"Efficiency Analysis of Voltage Divider and Wheatstone Bridge Sensor Circuits"

This script generates Figures 3.

Author:
 Tri Tran

License:
MIT
"""

import matplotlib.pyplot as plt
import numpy as np


# 1. Output Model Functions

def hdivider(theta, phi):
    return (1 + phi) * ((1 + theta) / (2 + theta))


def hbridge(theta, phi):
    return (1 + phi) * (((1 + theta) / (2 + theta)) - 0.5)


# 2. Derivative and Efficiency Functions

#  Voltage Divider
def numerator_voltagedivider(theta, phi):
    tinynumber = 0.0000000001
    numericalderivative = (
        hdivider(theta + tinynumber, phi) - hdivider(theta, phi)
    ) / tinynumber
    return np.abs(numericalderivative)


def denominator_voltagedivider(theta, phi):
    tinynumber = 0.0000000001
    numericalderivative = (
        hdivider(theta, phi + tinynumber) - hdivider(theta, phi)
    ) / tinynumber
    return np.abs(numericalderivative)


def Evoltagedivider(theta, phi):
    quotient = numerator_voltagedivider(theta, phi) / denominator_voltagedivider(
        theta, phi
    )
    return quotient

#  Wheatstone Bridge
def numerator_wheatstonebridge(theta, phi):
    tinynumber = 0.0000000001
    numericalderivative = (
        hbridge(theta + tinynumber, phi) - hbridge(theta, phi)
    ) / tinynumber
    return np.abs(numericalderivative)


def denominator_wheatstonebridge(theta, phi):
    tinynumber = 0.0000000001
    numericalderivative = (
        hbridge(theta, phi + tinynumber) - hbridge(theta, phi)
    ) / tinynumber
    return np.abs(numericalderivative)


def Ewheatstonebridge(theta, phi):
    quotient = numerator_wheatstonebridge(
        theta, phi
    ) / denominator_wheatstonebridge(theta, phi)
    return quotient


# 3. Parameter Grid

grid_divider = np.zeros((10, 15))
grid_bridge = np.zeros((10, 15))

thetavalues = np.linspace(0.1, 5, 10)
phivalues = np.linspace(0.1, 5, 15)

# Populate both efficiency grids in one nested loop
for k in range(0, 10):
    for j in range(0, 15):
        grid_divider[k, j] = Evoltagedivider(thetavalues[k], phivalues[j])
        grid_bridge[k, j] = Ewheatstonebridge(thetavalues[k], phivalues[j])


# 4. Side-by-Side 3D Plotting

A, B = np.meshgrid(thetavalues, phivalues)

Z_divider = grid_divider.T
Z_bridge = grid_bridge.T

# Create a wider figure to hold both 3D plots
fig = plt.figure(figsize=(14, 6))

#  Left Subplot: Voltage Divider
ax1 = fig.add_subplot(121, projection='3d')  # 1 row, 2 columns, 1st plot
surf1 = ax1.plot_surface(A, B, Z_divider, cmap='Blues')
ax1.set_title('Voltage Divider Efficiency')
ax1.set_xlabel('theta')
ax1.set_ylabel('phi')
ax1.set_zlabel('E')
fig.colorbar(surf1, ax=ax1)

#  Right Subplot: Wheatstone Bridge
ax2 = fig.add_subplot(122, projection='3d')  # 1 row, 2 columns, 2nd plot
surf2 = ax2.plot_surface(A, B, Z_bridge, cmap='Blues')
ax2.set_title('Wheatstone Bridge Efficiency')
ax2.set_xlabel('theta')
ax2.set_ylabel('phi')
ax2.set_zlabel('E')
fig.colorbar(surf2, ax=ax2)

plt.tight_layout()
plt.show()

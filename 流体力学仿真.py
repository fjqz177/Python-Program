# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:13:21 2023

@author: masson
"""
import numpy as np
# import matplotlib
from matplotlib import pyplot

plot_every = 100  # Frequency of plotting the results

def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y2 - y1)**2)

Nx = 400  # Number of grid points in x-direction
Ny = 100  # Number of grid points in y-direction
tau = 0.53  # Collision timescale
Nt = 30000  # Number of timesteps
NL = 9  # Number of lattice directions

# Lattice velocity vectors
cxs = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])
cys = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])

# Lattice weights
weights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36]) 

# Initialize the cylinder obstacle
cylinder = np.full((Ny, Nx), False)  # False indicates no obstacle
F = np.ones((Ny, Nx, NL)) + 0.01 * np.random.randn(Ny, Nx, NL)  # Initialize the distribution function F with random noise
F[:, :, 3] = 2.3  # Set the initial velocity in the x-direction for the fluid

# Set the cylinder obstacle
for y in range(0, Ny):
    for x in range(0, Nx):
        if distance(Nx // 4, Ny // 2, x, y) < 13:
           cylinder[y][x] = True

# Main loop
for it in range(Nt):
    print(it)  # Print the current timestep
    F[:,-1,[6,7,8]]=F[:,-2,[6,7,8]]
    F[:,0,[2,3,4]]=F[:,1,[2,3,4]]
    # Shift the distribution function F in each direction
    for i, cx, cy in zip(range(NL), cxs, cys):
        F[:, :, i] = np.roll(F[:, :, i], cx, axis=1)
        F[:, :, i] = np.roll(F[:, :, i], cy, axis=0)
# =============================================================================
# 这部分代码是用来实现在每个时间步骤中将分布函数F在每个方向上进行平移的操作。
# 具体来说，对于每个方向i，使用np.roll函数将F[:, :, i]在x方向上平移cx个单位，
# 在y方向上平移cy个单位。这样可以实现在每个方向上将分布函数从一个网格点移动到相邻的网格点。
# 这是Lattice Boltzmann方法中的一部分，用于模拟流体的运动。    
# =============================================================================
    # Extract the boundary distribution function values
    bndryF = F[cylinder, :]
    bndryF = bndryF[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]
  
    # Compute fluid variables
    rho = np.sum(F, 2)  # Density
    ux = np.sum(F * cxs, 2) / rho  # 沿着速度分量x求和
    uy = np.sum(F * cys, 2) / rho  # 沿着速度分量y求和
      
    # Set the boundary conditions
    F[cylinder, :] = bndryF
    ux[cylinder] = 0
    uy[cylinder] = 0
    
    # Collision
    Feq = np.zeros(F.shape)  # Equilibrium distribution function
    for i, cx, cy, w in zip(range(NL), cxs, cys, weights):
        Feq[:, :, i] = rho * w * (1 + 3 * (cx * ux + cy * uy) + 9 * (cx * ux + cy * uy)**2 / 2 - 3 * (ux**2 + uy**2) / 2)
    F = F + -(1/tau) * (F - Feq)
      
    if it % plot_every == 0:  # Plot the results every 50 timesteps
        dfydx=ux[2:,1:-1]-ux[0:-2,1:-1]
        dfxdy=uy[1:-1,2:]-uy[1:-1,0:-2] 
        curl = dfydx - dfxdy
        vel_mag_squared = ux**2 + uy**2
        pyplot.imshow(vel_mag_squared,cmap="bwr")        
        pyplot.pause(0.03)  # Pause for a short time to display the plots
        pyplot.cla()
        print("Successfully!")
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp
# Torus parameters
c = 3  # outer radius
a = 1  # inner radius

def X_bar(u, v):
	"""Parameterization of the torus in R^3.""" #Calc 3 type sh*t
	x = (c + a * np.cos(v)) * np.cos(u)
	y = (c + a * np.cos(v)) * np.sin(u)
	z = a * np.sin(v)
	return np.array([x, y, z])

def partial_u(u, v):
	"""Partial derivative of X_bar with respect to u."""
	dx_du = -(c + a * np.cos(v)) * np.sin(u)
	dy_du = (c + a * np.cos(v)) * np.cos(u)
	dz_du = 0
	return np.array([dx_du, dy_du, dz_du])

def partial_v(u, v):
	"""Partial derivative of X_bar with respect to v."""
	dx_dv = -a * np.sin(v) * np.cos(u)
	dy_dv = -a * np.sin(v) * np.sin(u)
	dz_dv = a * np.cos(v)
	return np.array([dx_dv, dy_dv, dz_dv])

def metric_tensor(u, v): #This is what seperates calc 3 from diff geometry.
	"""Compute the 2x2 metric tensor at (u, v)."""
	Xu = partial_u(u, v)
	Xv = partial_v(u, v)
	g11 = np.dot(Xu, Xu)
	g12 = np.dot(Xu, Xv)
	g21 = np.dot(Xv, Xu)
	g22 = np.dot(Xv, Xv)
	return np.array([[g11, g12], [g21, g22]])

if __name__ == "__main__":

	# Example: compute metric tensor at u=0, v=0
	u = 0.0
	v = 0.0
	g = metric_tensor(u, v)
	print("Metric tensor at (u=0, v=0):")
	print(g)

	# Plot the torus surface
	u_vals = np.linspace(0, 2 * np.pi, 100)
	v_vals = np.linspace(0, 2 * np.pi, 100)
	U, V = np.meshgrid(u_vals, v_vals)
	X = (c + a * np.cos(V)) * np.cos(U)
	Y = (c + a * np.cos(V)) * np.sin(U)
	Z = a * np.sin(V)

	fig = plt.figure(figsize=(8, 6))
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.8)
	ax.set_title('2-Torus Surface')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	plt.show()


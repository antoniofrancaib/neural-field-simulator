
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from scipy.integrate import solve_ivp

def create_synthetic_data(num_radial_segments=10, num_angular_segments=10, radial_bounds=(0, 1), angular_bounds=(0, 2 * np.pi)):
    # gives me a nodes and triangles toy data, instead of importing a gifti file
    
    theta = np.linspace(angular_bounds[0], angular_bounds[1], num_angular_segments)
    rho = np.linspace(radial_bounds[0], radial_bounds[1], num_radial_segments)

    Theta, Rho = np.meshgrid(theta, rho)
    X = Rho * np.cos(Theta)
    Y = Rho * np.sin(Theta)
    Z = np.zeros_like(X)
    #Z = np.maximum(-Rho**2 + 3, 0)  # Parabolic shape, clipping at 0

    x_flattened = X.flatten()
    y_flattened = Y.flatten()
    z_flattened = Z.flatten()

    nodes = np.column_stack((x_flattened, y_flattened, z_flattened))

    triangles = []
    for i in range(num_radial_segments - 1):
        for j in range(num_angular_segments - 1):
            top_left = i * num_angular_segments + j
            top_right = top_left + 1
            bottom_left = top_left + num_angular_segments
            bottom_right = bottom_left + 1
            
            triangles.append([top_left, top_right, bottom_left])
            triangles.append([bottom_left, top_right, bottom_right])

    triangles = np.array(triangles)
    
    return nodes, triangles

def firing_rate(u, mu=5.5, theta=5.6):
    return 1 / (1 + np.exp(-mu * u + theta)) - 1 / (1 + np.exp(theta))

def initial_condition(r, alpha=20, beta=1/20):
    r_norm = np.linalg.norm(r)
    return alpha / (np.cosh(beta * r_norm)**2)

def synaptic_kernel(r, r_prime, b=0.4, epsilon=1e-3):
    distance = np.linalg.norm(r - r_prime)
    A_x = np.exp(-b * distance) * (b * np.sin(distance) + np.cos(distance))

    if np.abs(A_x) >= epsilon:
        return A_x
    else:
        return 0
        
class Simulator:
    def __init__(self, N, E, M, W=synaptic_kernel, f=firing_rate, R_0=initial_condition):
        self.N = N
        self.E = E
        self.M = M #self.calculate_connectivity_matrix(W) 
        self.initial_activity = R_0
        self.f = f

    def calculate_connectivity_matrix(self, W):
        num_nodes = len(self.N)
        num_elements = len(self.E)  
        M = np.zeros((num_nodes, num_nodes))
        
        def triangle_area(node_indices):
            a, b, c = node_indices
            AB = self.N[b] - self.N[a]
            AC = self.N[c] - self.N[a]
            cross_product = np.cross(AB, AC)
            return np.linalg.norm(cross_product) / 2
        
        delta_j = np.zeros(num_nodes)

        for alpha in range(num_elements):
            for vertex in self.E[alpha]:
                delta_j[vertex] += triangle_area(self.E[alpha]) / 6  

        for i in range(num_nodes):
            for j in range(num_nodes):
                M[i, j] = W(self.N[i], self.N[j]) * delta_j[j]

        return M
        """for tri_indices in self.E:
            area = triangle_area(tri_indices)
            for node_i in range(num_nodes):  
                for node_j in tri_indices:
                    M[node_i, node_j] += W(self.N[node_i], self.N[node_j]) * (area / 6)  """


    def simulate(self, T = 50):
        R_0 = np.array([self.initial_activity(n) for n in self.N])  # Initialize R based on initial conditions

        def dRdt(t, R):
            return -R + self.M @ self.f(R)

        t_span = (0, T)

        sol = solve_ivp(dRdt, t_span, R_0, method='RK45', t_eval=np.linspace(0, T, 5000))

        return sol.t, sol.y

    def plot_activity(self, timestep=-1):
        _, R_t = self.simulate()

        X, Y, Z = self.N[:, 0], self.N[:, 1], self.N[:, 2]
        activities = R_t[:, timestep]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(X, Y, Z, c=activities, cmap='viridis', edgecolor='k', s=50)

        cbar = plt.colorbar(scatter)
        cbar.set_label('Neural Activity', rotation=270, labelpad=15)

        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate')
        plt.title(f'Neural Activity at Time Step {timestep}')
        plt.show()

    def plot_structure(self, print_triangles=False):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        X = self.N[:, 0]
        Y = self.N[:, 1]
        Z = self.N[:, 2]

        ax.scatter(X, Y, Z, c='b', marker='o')  

        if print_triangles:
            for tri in self.E:
                vertices = self.N[tri, :]
                vertice_order = np.append(tri, tri[0])
                ax.plot(self.N[vertice_order, 0], self.N[vertice_order, 1], self.N[vertice_order, 2], 'r-') 

        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate')
        plt.title('3D Plot of Nodes and Triangles')
        plt.show()
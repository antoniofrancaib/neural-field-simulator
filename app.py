from flask import Flask, request, jsonify, send_file
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from common_utils import Simulator
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

DATA_FOLDER = 'data'
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

simulator = None

def initialize_simulator():
    global simulator

    nodes_path = os.path.join(DATA_FOLDER, 'nodes.dat')
    elements_path = os.path.join(DATA_FOLDER, 'elements.dat')
    synaptic_matrix_path = os.path.join(DATA_FOLDER, 'synaptic-matrix.mat')

    logging.debug(f"Loading files: {nodes_path}, {elements_path}, {synaptic_matrix_path}")

    try:
        N = np.loadtxt(nodes_path)
        E = np.loadtxt(elements_path, dtype=int) - 1
        synaptic_matrix = loadmat(synaptic_matrix_path)['W']

        simulator = Simulator(N, E, synaptic_matrix)
        logging.debug("Simulator initialized successfully with default files")
    except Exception as e:
        logging.error(f"Error initializing simulator: {e}")

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/plot', methods=['GET'])
def plot_activity():
    global simulator
    timestep = int(request.args.get('timestep', 0))

    if not simulator:
        return jsonify({"message": "Simulator not initialized"}), 400

    try:
        _, R_t = simulator.simulate()
        X, Y, Z = simulator.N[:, 0], simulator.N[:, 1], simulator.N[:, 2]
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
        
        plot_path = os.path.join(UPLOAD_FOLDER, 'plot.png')
        plt.savefig(plot_path)
        plt.close()

        return jsonify({"url": f"/uploads/plot.png"})
    except Exception as e:
        logging.error(f"Error generating plot: {e}")
        return jsonify({"message": "Error generating plot", "error": str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

if __name__ == '__main__':
    initialize_simulator()
    app.run(debug=True)

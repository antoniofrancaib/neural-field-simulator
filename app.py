from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from common_utils import Simulator
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

simulator = None

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    global simulator

    nodes_file = request.files['nodes']
    elements_file = request.files['elements']
    synaptic_matrix_file = request.files['synaptic_matrix']

    nodes_path = os.path.join(UPLOAD_FOLDER, nodes_file.filename)
    elements_path = os.path.join(UPLOAD_FOLDER, elements_file.filename)
    synaptic_matrix_path = os.path.join(UPLOAD_FOLDER, synaptic_matrix_file.filename)

    nodes_file.save(nodes_path)
    elements_file.save(elements_path)
    synaptic_matrix_file.save(synaptic_matrix_path)

    logging.debug(f"Files uploaded: {nodes_path}, {elements_path}, {synaptic_matrix_path}")

    try:
        N = np.loadtxt(nodes_path)
        E = np.loadtxt(elements_path, dtype=int) - 1
        synaptic_matrix = loadmat(synaptic_matrix_path)['W']

        simulator = Simulator(N, E, synaptic_matrix)
        logging.debug("Simulator initialized successfully")
        return jsonify({"message": "Files uploaded and simulator initialized successfully!"})
    except Exception as e:
        logging.error(f"Error initializing simulator: {e}")
        return jsonify({"message": "Error initializing simulator", "error": str(e)}), 500

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
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

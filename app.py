from flask import Flask, request, jsonify
from flask_cors import CORS
from common_utils import create_synthetic_data, Simulator
import numpy as np

app = Flask(__name__)
CORS(app)  # This is needed for cross-origin requests if your front-end and back-end are served on different ports or domains.

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    connectivity = float(data.get('connectivity', 0.5))

    # Generate synthetic data
    N, E = create_synthetic_data(num_radial_segments=10, num_angular_segments=10)
    M = np.random.rand(len(N), len(N)) * connectivity  # Dummy matrix for connectivity

    # Initialize simulator with synthetic matrices
    simulator = Simulator(N, E, M)
    time, activities = simulator.simulate(T=50)

    # Convert results to a list for JSON serialization
    results = activities.tolist()
    return jsonify({'time': time.tolist(), 'activities': results})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from common_utils import Simulator, create_synthetic_data

app = Flask(__name__)

# Create synthetic data
num_radial_segments = 10
num_angular_segments = 10
radial_bounds = (0, 1)
angular_bounds = (0, 2 * np.pi)
nodes, triangles = create_synthetic_data(num_radial_segments, num_angular_segments, radial_bounds, angular_bounds)
simulator = Simulator(nodes, triangles)

@app.route('/simulate', methods=['GET'])
def simulate():
    timestep = request.args.get('timestep', default=-1, type=int)
    firing_threshold = request.args.get('firing_threshold', default=5, type=float)
    adaptivity = request.args.get('adaptivity', default=5, type=float)
    colormap = request.args.get('colormap', default='viridis', type=str)
    
    # Update simulator parameters if necessary
    simulator.update_parameters(firing_threshold=firing_threshold, adaptivity=adaptivity)

    fig = simulator.plot_activity(timestep, colormap)
    
    # Save figure to a BytesIO object
    img = io.BytesIO()
    FigureCanvas(fig).print_png(img)
    img.seek(0)
    
    # Encode image in base64
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    return jsonify({'image': img_base64})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from scipy.linalg import svd
import json


app = Flask(__name__)

class CrosswellTomography:
    def __init__(self, source_depth, borehole_distance=50, grid_size=20, depth_range=100):
        self.source_depth = source_depth
        self.borehole_distance = borehole_distance
        self.grid_size = grid_size
        self.depth_range = depth_range
        
        # Create receiver positions (uniformly spaced in receiver borehole)
        self.num_receivers = 10
        self.receiver_depths = np.linspace(10, depth_range-10, self.num_receivers)
        
        # Below are the Grid parameters
        self.nx = grid_size  # horizontal cells
        self.ny = grid_size  # vertical cells
        self.dx = borehole_distance / self.nx
        self.dy = depth_range / self.ny
        
        # Create grid cell centers
        self.x_centers = np.linspace(self.dx/2, borehole_distance - self.dx/2, self.nx)
        self.y_centers = np.linspace(self.dy/2, depth_range - self.dy/2, self.ny)
        
        # Source position (at x=0, source borehole)
        self.source_x = 0
        self.source_y = source_depth
        
        # Receiver positions (at x=borehole_distance, receiver borehole)
        self.receiver_x = borehole_distance


    def calculate_ray_paths(self):
        """Calculate ray paths from source to all receivers"""
        num_cells = self.nx * self.ny
        num_rays = self.num_receivers
    
        # Initialize G matrix (ray path matrix)
        G = np.zeros((num_rays, num_cells))
    
        ray_paths = []
    
        for i, receiver_depth in enumerate(self.receiver_depths):
            # Calculate ray path from source to receiver
            ray_x = [self.source_x, self.receiver_x]
            ray_y = [self.source_y, receiver_depth]
        
            ray_paths.append({
                'x': ray_x,
                'y': ray_y,
                'receiver_depth': receiver_depth
            })
        
            # Calculate path length through each cell
            for j in range(self.ny):
                for k in range(self.nx):
                    cell_index = j * self.nx + k
                    
                    # Cell boundaries
                    x_left = k * self.dx
                    x_right = (k + 1) * self.dx
                    y_top = j * self.dy
                    y_bottom = (j + 1) * self.dy
                    
                    # Calculate intersection length
                    length = self.ray_cell_intersection(
                        ray_x, ray_y, x_left, x_right, y_top, y_bottom
                    )
                    
                    G[i, cell_index] = length
    
        return G, ray_paths   
    
    def ray_cell_intersection(self, ray_x, ray_y, x_left, x_right, y_top, y_bottom):
        """Calculate the length of ray passing through a cell"""
        # Simple straight-line ray approximation
        x1, x2 = ray_x
        y1, y2 = ray_y
        
        # Check if ray passes through cell
        if x1 == x2:  # Vertical ray
            if x_left <= x1 <= x_right:
                y_enter = max(min(y1, y2), y_top)
                y_exit = min(max(y1, y2), y_bottom)
                if y_enter < y_exit:
                    return y_exit - y_enter
        else:
            # Calculate ray equation: y = mx + b
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            
            # Find intersection points
            intersections = []
            
            # Left boundary
            if x_left >= min(x1, x2) and x_left <= max(x1, x2):
                y_int = m * x_left + b
                if y_top <= y_int <= y_bottom:
                    intersections.append((x_left, y_int))
            
            # Right boundary
            if x_right >= min(x1, x2) and x_right <= max(x1, x2):
                y_int = m * x_right + b
                if y_top <= y_int <= y_bottom:
                    intersections.append((x_right, y_int))
            
            # Top boundary
            if m != 0:
                x_int = (y_top - b) / m
                if x_left <= x_int <= x_right and min(x1, x2) <= x_int <= max(x1, x2):
                    intersections.append((x_int, y_top))
            
            # Bottom boundary
            if m != 0:
                x_int = (y_bottom - b) / m
                if x_left <= x_int <= x_right and min(x1, x2) <= x_int <= max(x1, x2):
                    intersections.append((x_int, y_bottom))
            
            # Remove duplicates and calculate length
            if len(intersections) >= 2:
                intersections = list(set(intersections))
                if len(intersections) >= 2:
                    x_int1, y_int1 = intersections[0]
                    x_int2, y_int2 = intersections[1]
                    return np.sqrt((x_int2 - x_int1)**2 + (y_int2 - y_int1)**2)
        
        return 0.0
        
    def perform_svd_inversion(self, G, k=None):
        """Perform SVD inversion with truncation"""
        # Perform SVD
        U, s, Vt = svd(G, full_matrices=False)
        
        # Get matrix rank
        rank = np.sum(s > 1e-10)
        
        # Truncate if k is specified
        if k is not None and k < len(s):
            s_truncated = s[:k]
            U_truncated = U[:, :k]
            Vt_truncated = Vt[:k, :]
        else:
            s_truncated = s
            U_truncated = U
            Vt_truncated = Vt
        
        # Create synthetic travel time data (for demonstration)
        np.random.seed(42)  # For reproducible results
        
        # Create a synthetic slowness model
        true_slowness = np.ones(G.shape[1])
        # Add some anomalies
        anomaly_indices = np.random.choice(G.shape[1], size=G.shape[1]//4, replace=False)
        true_slowness[anomaly_indices] += np.random.normal(0, 0.1, len(anomaly_indices))
        
        # Generate synthetic travel times
        travel_times = G @ true_slowness + np.random.normal(0, 0.01, G.shape[0])
        
        # Compute pseudo-inverse using truncated SVD
        s_inv = np.zeros_like(s_truncated)
        s_inv[s_truncated > 1e-10] = 1.0 / s_truncated[s_truncated > 1e-10]
        
        # Reconstruct inverse: G_inv = V * S_inv * U^T
        G_inv = Vt_truncated.T @ np.diag(s_inv) @ U_truncated.T
        
        # Solve for slowness anomalies
        slowness_anomalies = G_inv @ travel_times
        
        return slowness_anomalies, rank, s
    
    def create_visualization_data(self, slowness_anomalies, ray_paths):
        """Create data for visualization"""
        slowness_grid = slowness_anomalies.reshape(self.ny, self.nx)

        borehole_data = {
            'source': {'x': self.source_x, 'y': self.source_y},
            'receivers': [{'x': self.receiver_x, 'y': depth} for depth in self.receiver_depths],
            'boreholes': {
                'source_x': [self.source_x, self.source_x],
                'source_y': [0, self.depth_range],
                'receiver_x': [self.receiver_x, self.receiver_x],
                'receiver_y': [0, self.depth_range]
            }
        }
        return {
            'slowness_grid': slowness_grid.tolist(),
            'x_centers': self.x_centers.tolist(),
            'y_centers': self.y_centers.tolist(),
            'ray_paths': ray_paths,
            'borehole_data': borehole_data
        }
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/invert', methods=['POST'])
def invert():
    try:
        data = request.json
        source_depth = float(data['sourceDepth'])
        k = int(data['k']) if data.get('k') else None
        
        # Create tomography object
        tomo = CrosswellTomography(source_depth)
        
        # Calculate ray paths and G matrix
        G, ray_paths = tomo.calculate_ray_paths()
        
        # Perform SVD inversion
        slowness_anomalies, rank, singular_values = tomo.perform_svd_inversion(G, k)
        
        # Create visualization data
        viz_data = tomo.create_visualization_data(slowness_anomalies, ray_paths)

        return jsonify({
            'success': True,
            'rank': int(rank),
            'singular_values': singular_values.tolist(),
            'slowness_grid': viz_data['slowness_grid'],
            'x_centers': viz_data['x_centers'],
            'y_centers': viz_data['y_centers'],
            'ray_paths': viz_data['ray_paths'],
            'borehole_data': viz_data['borehole_data'],
            'grid_info': {
                'nx': tomo.nx,
                'ny': tomo.ny,
                'dx': tomo.dx,
                'dy': tomo.dy,
                'borehole_distance': tomo.borehole_distance,
                'depth_range': tomo.depth_range
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True)
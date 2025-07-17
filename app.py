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

@app.route('/')
def index():
    return render_template('index.html')  # This looks for templates/index.html

if __name__ == '__main__':
    app.run(debug=True)

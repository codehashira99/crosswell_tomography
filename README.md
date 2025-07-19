An interactive web application for performing SVD-based crosswell seismic tomography inversion. This tool allows users to visualize ray paths between boreholes, analyze singular value decomposition, and reconstruct subsurface slowness models from synthetic travel time data.
🚀 Features

✨ Interactive Web Interface: Real-time parameter adjustment and visualization
🔧 SVD-based Inversion: Singular Value Decomposition with truncation control
📱 Ray Path Visualization: Dynamic display of seismic ray paths between boreholes
🎯 Slowness Model Reconstruction: Heatmap visualization of subsurface properties
📊 Singular Value Analysis: Interactive plots of eigenvalue spectrum
🎛️ Parameter Control: Adjustable source depth and truncation parameters

🛠️ Tech Stack
Backend:

Python 3.7+
Flask - Web framework
NumPy - Numerical computations
SciPy - Scientific computing (SVD operations)
Matplotlib - Plotting backend

Frontend:

HTML5, CSS3, JavaScript
Plotly.js - Interactive data visualization
Responsive CSS Grid layout
Modern ES6+ JavaScript features

Mathematical Libraries:

scipy.linalg - Linear algebra operations
numpy.random - Synthetic data generation

📁 Project Structure
crosswell-tomography/
│
├── app.py                     # Flask application and tomography engine
├── templates/
│   └── index.html            # Main web interface
├── static/
│   └── css/
│       └── index.css         # Styling (if exists)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore rules
🚀 Getting Started
Prerequisites
Make sure you have the following installed:

Python (3.7 or higher)
pip (Python package installer)

Installation

Clone the repository:

bashgit clone https://github.com/yourusername/crosswell-tomography.git
cd crosswell-tomography

Create a virtual environment (recommended):

bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

bashpip install -r requirements.txt

Run the application:

bashpython app.py

Open http://localhost:5000 to view the application in your browser.

📖 Usage
Basic Operation

Select Source Depth: Choose the depth of the seismic source (100m - 1600m)
Set Truncation Parameter: Define the number of singular values to keep (K parameter)
Run Inversion: Click "Run Inversion" to process the tomographic data
Analyze Results: View the reconstructed slowness model and ray path geometry

Understanding the Results

Singular Values Plot: Shows the eigenvalue spectrum for stability analysis
Crosswell Setup: Visualizes borehole positions, source, receivers, and ray paths
Slowness Model: Heatmap of reconstructed subsurface velocity variations
Inversion Info: Matrix rank, grid dimensions, and processing parameters

Advanced Configuration
The application uses default parameters that can be modified in app.py:
python# Grid and geometry parameters
borehole_distance = 50    # Distance between boreholes (m)
grid_size = 20           # Number of grid cells per dimension
depth_range = 100        # Maximum depth (m)
num_receivers = 10       # Number of receivers per borehole
🧮 Mathematical Background
Crosswell Tomography Theory
The application implements linearized seismic tomography using:

Forward Modeling: Ray path calculation through discretized media
Inverse Problem: SVD-based least squares solution
Regularization: Truncated SVD for stable inversion

Key Equations
The forward problem: t = G * s

t: Travel times
G: Ray path matrix (geometry)
s: Slowness model

The inverse solution: s = G⁻¹ * t

Solved using SVD: G = U * Σ * Vᵀ

🎛️ API Endpoints
POST /invert
Performs tomographic inversion with given parameters.
Request Body:
json{
  "sourceDepth": 500,
  "k": 10
}
Response:
json{
  "success": true,
  "rank": 15,
  "singular_values": [1.23, 0.45, ...],
  "slowness_grid": [[1.0, 1.1, ...], ...],
  "ray_paths": [{"x": [0, 50], "y": [500, 300]}, ...],
  "borehole_data": {...},
  "grid_info": {...}
}
🔧 Configuration
Environment Variables
bashFLASK_ENV=development    # For development mode
FLASK_DEBUG=1           # Enable debug mode
Model Parameters
Key parameters in CrosswellTomography class:

source_depth: Source position along borehole
borehole_distance: Separation between wells
grid_size: Resolution of inversion grid
depth_range: Vertical extent of model

🧪 Testing
Currently uses synthetic data for demonstration. To test with real data:

Modify the perform_svd_inversion method
Need to replace synthetic travel time generation
Input real field measurements


🔬 Scientific Background
This implementation is based on established geophysical methods:

Seismic tomography principles
Linear inverse theory
SVD regularization techniques
Crosswell seismic survey geometry

📚 Documentation
Key Classes
CrosswellTomography: Main computational engine

calculate_ray_paths(): Computes ray geometry matrix
ray_cell_intersection(): Calculates path lengths through cells
perform_svd_inversion(): SVD-based inversion algorithm
create_visualization_data(): Prepares results for plotting

Mathematical Methods

Ray Path Calculation: Linear ray approximation between source-receiver pairs
Matrix Construction: G-matrix representing ray path lengths through cells
SVD Decomposition: Singular value analysis for inversion stability
Truncated Inversion: Regularization through eigenvalue cutoff

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
👨‍💻 Author
Your Name


🙏 Acknowledgments

SciPy community for robust linear algebra tools
Plotly.js for interactive visualization capabilities
Flask development team for the lightweight web framework
Geophysics community for tomography algorithm development


📊 Performance Stats

Grid Resolution: Up to 20x20 cells (400 parameters)
Ray Coverage: 10 receiver positions per source
Computation Time: < 1 second for standard grid
Memory Usage: Minimal for typical problem sizes

🏗️ Technical Details
Dependencies
Flask>=2.0.0
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
Browser Compatibility

Chrome 90+
Firefox 88+
Safari 14+
Edge 90+
Chat controls Sonnet 4
# Crosswell Seismic Tomography

An interactive web application for performing SVD-based crosswell seismic tomography inversion. This tool enables geophysicists to visualize ray paths between boreholes, analyze singular value decomposition, and reconstruct subsurface slowness models from travel time data.

## Features

- **Interactive Web Interface** - Real-time parameter adjustment and visualization
- **SVD-based Inversion** - Singular Value Decomposition with truncation control for stable reconstruction
- **Ray Path Visualization** - Dynamic display of seismic ray paths between boreholes
- **Slowness Model Reconstruction** - Heatmap visualization of subsurface velocity properties
- **Singular Value Analysis** - Interactive plots showing eigenvalue spectrum for stability assessment
- **Parameter Control** - Adjustable source depth and truncation parameters

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/codehashira99/crosswell-tomography.git
cd crosswell-tomography
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

### Basic Operation

1. **Select Source Depth** - Choose the seismic source depth (100m - 1600m)
2. **Set Truncation Parameter** - Define the number of singular values to keep (K parameter)
3. **Run Inversion** - Click "Run Inversion" to process the tomographic data
4. **Analyze Results** - View the reconstructed slowness model and ray path geometry

### Understanding the Results

- **Singular Values Plot** - Shows eigenvalue spectrum for inversion stability analysis
- **Crosswell Setup** - Visualizes borehole positions, source locations, receivers, and ray paths
- **Slowness Model** - Color-coded heatmap of reconstructed subsurface velocity variations
- **Inversion Info** - Matrix rank, grid dimensions, and processing parameters

## Technical Details

### Technology Stack

**Backend:**
- Python 3.7+ with Flask web framework
- NumPy for numerical computations
- SciPy for scientific computing and SVD operations
- Matplotlib for plotting backend

**Frontend:**
- HTML5, CSS3, JavaScript
- Plotly.js for interactive data visualization
- Responsive CSS Grid layout

### Project Structure

```
crosswell-tomography/
├── app.py              # Flask application and tomography engine
├── templates/
│   └── index.html      # Main web interface
├── static/
│   └── css/
│       └── index.css   # Styling
├── requirements.txt    # Python dependencies
├── README.md
└── .gitignore
```

### Mathematical Background

The application implements linearized seismic tomography using:

- **Forward Modeling** - Ray path calculation through discretized media
- **Inverse Problem** - SVD-based least squares solution
- **Regularization** - Truncated SVD for stable inversion

#### Key Equations

Forward problem: `t = G × s`
- `t`: Travel times
- `G`: Ray path matrix (geometry)
- `s`: Slowness model

Inverse solution solved using SVD: `G = U × Σ × V^T`

### Configuration

Default parameters (modifiable in `app.py`):

```python
borehole_distance = 50    # Distance between boreholes (m)
grid_size = 20           # Number of grid cells per dimension
depth_range = 100        # Maximum depth (m)
num_receivers = 10       # Number of receivers per borehole
```

## API Reference

### POST /invert

Performs tomographic inversion with given parameters.

**Request Body:**
```json
{
  "sourceDepth": 500,
  "k": 10
}
```

**Response:**
```json
{
  "success": true,
  "rank": 15,
  "singular_values": [1.23, 0.45, ...],
  "slowness_grid": [[1.0, 1.1, ...], ...],
  "ray_paths": [{"x": [0, 50], "y": [500, 300]}, ...],
  "borehole_data": {...},
  "grid_info": {...}
}
```

## Development

### Key Classes

- **CrosswellTomography** - Main computational engine
  - `calculate_ray_paths()` - Computes ray geometry matrix
  - `ray_cell_intersection()` - Calculates path lengths through cells
  - `perform_svd_inversion()` - SVD-based inversion algorithm
  - `create_visualization_data()` - Prepares results for plotting

### Environment Variables

```bash
FLASK_ENV=development    # For development mode
FLASK_DEBUG=1           # Enable debug mode
```

### Performance

- **Grid Resolution:** Up to 20×20 cells (400 parameters)
- **Ray Coverage:** 10 receiver positions per source
- **Computation Time:** < 1 second for standard grid
- **Browser Compatibility:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## Testing

Currently uses synthetic data for demonstration. To implement real data:

1. Modify the `perform_svd_inversion` method
2. Replace synthetic travel time generation with real field measurements
3. Input actual crosswell survey data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- SciPy community for robust linear algebra tools
- Plotly.js for interactive visualization capabilities
- Flask development team for the lightweight web framework
- Geophysics community for tomography algorithm development

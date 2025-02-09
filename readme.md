# NASA IMERG Precipitation Analysis

## Overview
This project analyzes precipitation patterns in Central Italy using NASA's IMERG (Integrated Multi-satellitE Retrievals for GPM) dataset. The analysis covers the period from 2018 to 2023, focusing on the region between 10°E-15°E longitude and 41°N-44°N latitude.

## Features
- Temporal analysis of precipitation patterns
- Spatial distribution visualization
- Statistical analysis of rainfall data
- 3D visualization of precipitation patterns
- Time series analysis and trend detection

## Project Structure
```
.
├── data.py                     # Data processing and CSV generation
├── statistical_analysis.py     # Statistical computations
├── temporal_analysis.py        # Temporal pattern analysis
├── plot/                      # Visualization scripts
│   ├── plot_all.py            # Main plotting script
│   ├── plot_3D_temp_visualization.py
│   ├── plot_map_grid.py
│   └── plot.py
├── requirements.txt           # Python dependencies
└── output/                   # Generated analysis files and plots
```

## Requirements
- Python 3.7+
- Required packages listed in requirements.txt:
  - numpy>=1.21.0
  - pandas>=1.3.0
  - matplotlib>=3.5.0
  - seaborn>=0.11.0
  - scikit-learn>=1.0.0
  - scipy>=1.7.0
  - rasterio>=1.2.0
  - cartopy>=0.20.0
  - plotly>=5.5.0
  - kaleido>=0.2.1

## Installation
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Process the IMERG data:
   ```bash
   python data.py
   ```
2. Run statistical analysis:
   ```bash
   python statistical_analysis.py
   ```
3. Generate visualizations:
   ```bash
   python plot/plot_all.py
   ```

## Output Files
- `precipitation_timeseries.csv`: Processed precipitation data
- `output_analysis/`: Statistical analysis results
- `output_plots/`: Generated visualizations including:
  - Annual statistics plots
  - Multi-day coverage maps
  - 3D precipitation visualization
  - Temporal trend analysis

## Data Source
The data is sourced from NASA's IMERG dataset via the Giovanni portal (https://giovanni.gsfc.nasa.gov/giovanni).


## Author
Riccardo Benedetti
Thomas De Palma
Mattia Pistoia
Supervised by: Karina Chichifoi
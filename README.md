# ABS Super-Capacitor & Power Electronics Calculator

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-brightgreen)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![MATLAB](https://img.shields.io/badge/MATLAB-Optional-orange)](https://www.mathworks.com/products/matlab.html)

A Streamlit-based web dashboard for calculating super-capacitor parameters in Automotive Brake Systems (ABS) and simulating power electronics circuits using Simulink models. The app supports two main modes for super-capacitor analysis and interactive simulations for circuits like 3-Phase Diode Rectifiers and IGBTs.

**Note**: MATLAB/Simulink functionalities are optional and can be commented out for standalone Python execution. For full simulation features, uncomment and install MATLAB.

## Features

- **Super-Capacitor Calculator**:
  - **Current Profile Visualization**: Plot periodic or non-periodic current waveforms.
  - **Mode 1: Find ABS On/Off Time**: Given capacitance, compute charging/discharging times with voltage-time plots.
  - **Mode 2: Find Capacitor Value**: Binary search sweep to find optimal capacitance for target discharge time.
  - PDF Report Generation: Download detailed inputs, results, and notes.

- **Power Electronics Simulations** (MATLAB/Simulink Required):
  - Interactive tabs for 4 circuit models: 3-Phase Diode Rectifier, IGBTs with RC Snubbers, Permanent Magnet Synchronous Machine (PMSM), and RLC Output Filter for Sine Wave.
  - Parameter tuning (e.g., voltage, frequency, load) and real-time plots/tables of simulation outputs.

- **Responsive UI**: Wide layout, tooltips, metrics, expanders, and mobile-friendly design with custom CSS.
- **Real-Time Updates**: Plots and metrics refresh dynamically.

## Screenshots

![Dashboard Overview](screenshots/dashboard.png) <!-- Add actual screenshots if available -->

![Super-Capacitor Mode](screenshots/super_cap.png)

![Simulink Tab](screenshots/simulink_tab.png)

## Installation

1. **Clone or Download**:
   ```
   git clone <your-repo-url>
   cd abs-calculator
   ```

2. **Install Python Dependencies**:
   ```
   pip install streamlit numpy matplotlib pandas reportlab
   ```

3. **Optional: MATLAB/Simulink Setup**:
   - Install MATLAB (R2020a+) with Simulink.
   - Uncomment MATLAB imports and `get_matlab_engine()` function.
   - Update paths in `get_matlab_engine()` to your MATLAB/Simulink files (e.g., `.slx` models in `C:\Users\adars\OneDrive\Desktop\SimulinkModels`).
   - Ensure models like `3-Phase Diode Rectifier.slx` are accessible.

4. **Run the App**:
   ```
   streamlit run main.py
   ```
   - Opens at `http://localhost:8501`.

## Usage

### Super-Capacitor Calculator Tab
1. **Current Profile**: Select "Periodic" or "Non-Periodic", adjust time period/spike, currents. View plot.
2. **Current Source**: Set constant input current (A).
3. **Charging Model**: Choose 14V or 48V.
4. **Mode Selection**:
   - **Find ABS On/Off Time**: Input capacitance → Get times, plots, and PDF.
   - **Find Capacitor Value**: Input target on-time, range/tolerance → Get optimal C, plots, and PDF.

### Simulink Models Tabs
1. Select a model (e.g., 3-Phase Diode Rectifier).
2. Tune parameters (voltage, frequency, load, sim time).
3. Click "Run Simulation" → View plot and data table (requires MATLAB).

**Tips**:
- Use expanders for inputs to keep UI clean.
- Download PDFs for reports with notes/explanations.
- Hover tooltips for parameter help.

## Dependencies

### Required (Python)
- `streamlit` (UI framework)
- `numpy`, `matplotlib` (plots/data)
- `pandas` (tables)
- `reportlab` (PDF generation)

### Optional (MATLAB)
- MATLAB Engine API for Python
- Simulink with listed `.slx` models
- Paths updated in code for your local setup

Install via `pip` for Python deps; MATLAB requires separate license.

## Project Structure

```
abs-calculator/
├── main.py                  # Main Streamlit app
├── screenshots/             # UI screenshots (optional)
├── SimulinkModels/         # Folder for .slx files (e.g., 3-Phase Diode Rectifier.slx)
├── Matlab/                 # MATLAB scripts (e.g., LogTimes.m)
├── README.md               # This file
└── requirements.txt        # Pip dependencies
```

**requirements.txt** (create this file):
```
streamlit
numpy
matplotlib
pandas
reportlab
```

## Known Issues & Troubleshooting

- **MATLAB Errors**: If uncommented, ensure MATLAB path is correct. Models must exist; otherwise, fallback to "No output data".
- **Plots Not Showing**: Ensure Matplotlib backend is set (default works in Streamlit).
- **PDF Generation**: ReportLab requires no extra config; test with sample inputs.
- **Wide Layout Issues**: On mobile, use portrait mode for better visibility.
- **Session State**: Inputs persist across reruns; clear browser cache if stuck.

If running without MATLAB, simulations show warnings but app runs (plots current profile, metrics as static examples).

## Contributing

1. Fork the repo.
2. Create a branch: `git checkout -b feature/new-model`.
3. Commit changes: `git commit -m "Add new Simulink model"`.
4. Push: `git push

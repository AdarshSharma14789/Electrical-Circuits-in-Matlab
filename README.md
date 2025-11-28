# 📘 ABS Super-Capacitor & Power Electronics Calculator

This project is a **Streamlit-based engineering dashboard** that integrates **MATLAB + Python** to simulate and analyze:

- ABS super-capacitor charging/discharging behavior  
- Capacitor sizing based on target ABS ON-time  
- MATLAB model-based computation of voltage waveforms  
- Execution of Simulink power-electronics models  
- Automatic PDF report generation  
- Interactive visualization using charts and dashboards  

---

## 🚀 Features

### ✅ Super-Capacitor Calculator
- Periodic and non-periodic current profiles  
- ABS ON/OFF time calculation for given capacitance  
- Capacitor value estimation for required ABS ON time  
- MATLAB-based simulation backend  
- Automatically generated PDF report  

---

### ✅ Power Electronics Simulation (Simulink)

Run and visualize results for:

- 3-Phase Diode Rectifier  
- IGBTs with RC Snubbers  
- Permanent Magnet Synchronous Machine (PMSM)  
- RLC Output Filter for Sine Wave  

Results are plotted directly inside Streamlit and presented numerically.

---

### ✅ MATLAB Integration

Uses MATLAB Engine for Python:
- Executes `.m` models  
- Accesses workspace variables  
- Runs Simulink models  
- Transfers simulation results into Python  

---

### ✅ Dashboard UI

- Tab-based navigation  
- Interactive input widgets  
- Real-time simulation status  
- Plotting and reporting tools  
- Custom styled interface (CSS)

---

## 📦 Requirements

### Software
- MATLAB R2025b or later  
- Python 3.9+  
- Anaconda (recommended)  
- Streamlit  

---

### Python Libraries

Run:

```bash
pip install streamlit numpy matplotlib pandas reportlab

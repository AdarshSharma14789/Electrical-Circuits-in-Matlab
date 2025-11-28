import matlab.engine

def main():
    eng = matlab.engine.start_matlab()

    eng.addpath(r'C:\Users\adars\OneDrive\Desktop\Matlab', nargout=0)

    model = 'Week_5_day_4_original'
    
    targetDt = 3.0
    C_list = list(range(1, 101))  # Capacitance values from 1 to 100 F
    
    # Set simulation inputs
    TimePeriod = 0.1          # seconds
    SpikeTime = 0.02         # seconds
    periodic = True         # or False
    CurrentSource = 4.0       # Amps
    high_current = 25.0     # Peak current
    low_current = 10.0      # Static current

    # Compute OnTime in Python
    OnTime = (SpikeTime / TimePeriod) * 100 if periodic else 100.0

    # Push variables into MATLAB base workspace
    eng.workspace['modelName'] = model
    eng.workspace['TimePeriod'] = TimePeriod
    eng.workspace['SpikeTime'] = SpikeTime
    eng.workspace['myFlag'] = float(periodic)  # MATLAB expects 1.0 or 0.0
    eng.workspace['low_current'] = low_current
    eng.workspace['high_current'] = high_current
    eng.workspace['CurrentSource'] = CurrentSource
    eng.workspace['OnTime'] = OnTime
    eng.workspace['targetDt'] = targetDt  # Added to match MATLAB function input
    eng.workspace['C_list'] = matlab.double(C_list)  # Ensure C_list is a MATLAB array

    # Call the MATLAB function
    bestC, bestDt, bestErr = eng.capacitor_sweep(
        float(targetDt),
        matlab.double(C_list),
        model,
        nargout=3
    )
    
    print("\n  Sweep complete:")
    print(f"  Closest C_val = {bestC:.1f} F")
    print(f"  Achieved ABS On Time / Capacitor Discharging Time = {bestDt:.4f} s")
    print(f"  Error = ±{bestErr:.4f} s")

    eng.quit()

if __name__ == "__main__":
    main()
# import matlab.engine
# def main():
#     eng = matlab.engine.start_matlab()
    
#     eng.addpath(r'C:\Users\adars\OneDrive\Desktop\Matlab', nargout=0)
    
#     C_val = 22.5
#     model='Week_6_day_4'
    
#     t_rise, deltaT = eng.LogTimes(C_val, model, nargout=2)
#     print(f"\n  Results for C_val = {C_val} F:")
#     print(f"  Capacitor Charging Time / ABS off Time: {t_rise:.4f} s")
#     print(f"  Capacitor DisCharging Time / ABS On time: {deltaT:.4f} s\n")
       
#     eng.quit()

# if __name__ == "__main__":
#     main()
import matlab.engine

def main():
    # Start MATLAB engine and set model path
    eng = matlab.engine.start_matlab()
    eng.addpath(r'C:\Users\adars\OneDrive\Desktop\Matlab', nargout=0)

    # Parameters to send to MATLAB workspace
    model = 'Week_5_day_4_original'
    C_val = 30

    # Set simulation inputs
    TimePeriod     = 0.1          # seconds
    SpikeTime      = 0.02         # seconds
    periodic       = True         # or False
    CurrentSource  = 2.5        # Amps
    high_current   = 25.0         # Peak current
    low_current    = 10.0         # Static current

    # Compute OnTime in Python (optional, can let MATLAB compute as well)
    OnTime = (SpikeTime / TimePeriod) * 100 if periodic else 100.0

    # Push variables into MATLAB base workspace
    eng.workspace['modelName']      = model
    eng.workspace['C_val']          = C_val
    eng.workspace['TimePeriod']     = TimePeriod
    eng.workspace['SpikeTime']      = SpikeTime
    eng.workspace['myFlag']         = float(periodic)  # MATLAB expects 1.0 or 0.0
    eng.workspace['low_current']    = low_current
    eng.workspace['high_current']   = high_current
    eng.workspace['CurrentSource']  = CurrentSource
    eng.workspace['OnTime']         = OnTime

    # Run LogTimes which internally uses Simulink
    t_rise, deltaT = eng.LogTimes(C_val, model, nargout=2)
    
    # Print results
    print(f"\nResults for C_val = {C_val} F")
    print(f"Capacitor Charging Time (ABS Off): {t_rise:.4f} s")
    print(f"Capacitor Discharging Time (ABS On): {deltaT:.4f} s\n")

    eng.quit()

if __name__ == "__main__":
    main()

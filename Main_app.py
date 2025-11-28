import streamlit as st
import matlab.engine
import numpy as np
import matplotlib.pyplot as plt
import math
import textwrap
import io

from textwrap import wrap 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


st.set_page_config(
    page_title="ABS Super-Capacitor Calculator",
    layout="centered",
    initial_sidebar_state="expanded"
)



def generate_pdf_report(mode, inputs, results):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "ABS Super-Capacitor Calculator Report")
    c.drawString(100, 730, f"Date: {st.session_state.get('current_date', 'July 17, 2025')}")
    c.drawString(100, 710, f"Mode: {mode}")
    c.drawString(100, 690, "Inputs:")

    y = 670
    for key, value in inputs.items():
        c.drawString(120, y, f"{key}: {value}")
        y -= 20

    c.drawString(100, y - 20, "Results:")
    y -= 40

    for key, value in results.items():
        if key != "Notes":
            c.drawString(120, y, f"{key}: {value}")
            y -= 20

    # Wrap and add Notes (if exists)
    if "Notes" in results:
        note_lines = textwrap.wrap(results["Notes"], width=90)  # 90 chars per line (adjust if needed)
        c.drawString(120, y, "Notes:")
        y -= 20
        for line in note_lines:
            c.drawString(130, y, line)
            y -= 18  # adjust line spacing

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

st.markdown("""
    <style>
    .stApp {
        background-color: #E4E9FD;
        background-image: linear-gradient(110deg,#83BEEA 50%, #94E6F1 50%);
        min-height: 100vh;
        font-family: 'helvetica neue', Arial, sans-serif;
    }

                                          
    #title {
        background-color: #6495ED;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
    }
                    
    h1 {
        color: #fff;
        margin: 0;
    }
    
    .stExpander {
        background: white;
        border-radius: 5px;
        box-shadow: 5px 5px 15px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
            
    .stExpander:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    }
            
    .stButton > button {
        background-color: #6495ED;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.2s ease, transform 0.1s ease;
    }
    .stButton > button:hover {
        background-color: #87CEFA;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    .stNumberInput input, .stSlider input {
        background: transparent;
        border: none;
        font-size: 18px;
        font-weight: 370;
        color: #00204a;        
        padding: 8px;
    }
    
    .stNumberInput input:focus, .stSlider input:focus {
        outline: none;
        box-shadow: inset 0 -3px 0 0 #A683E3;
    }
    
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    .stMetric {
        background-color: #f0f4ff;
        border: 1px solid #6495ED;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .metric {
        color: #00204a;
        font-weight: 600;
    }
    .plot-container {
        text-align: center;
        background: #ffffff;
        padding: 15px;
        border-radius: 8px;
    }
    .status {
        margin: 10px 0;
        padding: 12px;
        border-radius: 6px;
        font-weight: 500;;
    }
    .status.success {
      background-color: #FFFFFF;
      color: black;
      border: 1px solid black;
    }
    
    .status.error {
      background-color: #FFFFFF;
      color: black;
      border: 1px solid black;
    }
    
    .status.info {
      background-color: #FFFFFF;
      color: black;
      border: 1px solid black;
    }

    .tooltip {
        position: relative;
        display: inline-block;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    .footer {
        text-align: center;
        padding: 10px;
        color: #000;
        font-size: 14px;
        font-weight: 500;
        border-top: 1px dashed #5A9BD4;
        margin-top: 30px;
        cursor: pointer; /* Subtle cursor change to hint interactivity */
    }
    @media (max-width: 768px) {
        .stApp {
            padding: 10px;
        }
        .stExpander {
            margin-bottom: 15px;
        }
        .footer {
            font-size: 12px;
            padding: 10px;
        }
    }
    # .footer {
    #     text-align: center;
    #     padding: 10px;
    #     color: #000;
    #     font-size: 14px;
    #     font-weight: 500;
    #     border-top: 1px dashed #5A9BD4;
    #     margin-top: 30px;
    #     }
    
    # @media (max-width: 768px) {
    #     .stApp {
    #         padding: 10px;
    #     }
    #     .stExpander {
    #         margin-bottom: 15px;
    #     }
    #     .footer {
    #         font-size: 12px;
    #         padding: 10px;
    #     }
    # }
    </style>
""", unsafe_allow_html=True)



@st.cache_resource
def get_matlab_engine():
    eng = matlab.engine.start_matlab()
    eng.addpath(r'C:\Users\adars\OneDrive\Desktop\Matlab', nargout=0)
    return eng





def plot_current_profile(periodic, time_period, spike_time, peak_current, static_current, duration=1.0, sample_rate=10000):
    t = np.linspace(0, duration, int(duration * sample_rate))
    current = np.zeros_like(t)
    if periodic == "Periodic":
        for i in range(len(t)):
            t_mod = t[i] % time_period
            current[i] = peak_current if t_mod <= spike_time else static_current
    else:
        current[:] = static_current
        current[t <= spike_time] = peak_current

    fig, ax = plt.subplots(figsize=(6, 2.5))
    ax.plot(t, current, linewidth=2, color='#4682B4')
    ax.set_title("Current Profile (A)", fontsize=14, pad=10)
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("Current (A)", fontsize=12)
    ax.set_xlim(0, duration)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_facecolor('#f8f9fa')
    fig.tight_layout()
    st.pyplot(fig)




def compute_log_times(C_val: float, model_name: str):
    eng = get_matlab_engine()
    try:
        t_rise, deltaT, t, Vcap = eng.LogTimes(C_val, model_name, nargout=4)
        t = np.array(t).flatten()
        Vcap = np.array(Vcap).flatten()
        mask = t <= 250.0
        return float(t_rise), float(deltaT), t[mask], Vcap[mask]
    except Exception as e:
        st.error(f"MATLAB computation failed: {str(e)}")
        return None, None, None, None

def sweep_for_cap(target_dt: float, c_min: float, c_max: float, tol_dt: float, cap_tol: float, model_name: str):
    status = st.empty()
    status.info(f"Sweeping C from {c_min:.3f}F to {c_max:.3f}F (step {cap_tol}F)…")

    bestC = None
    bestDt = None
    bestErr = float("inf")
    t_data = v_data = None
    best_t_rise = None

    left, right = c_min, c_max

    while (right - left) > cap_tol:
        mid = 0.5 * (left + right)
        c = cap_tol * math.floor(mid / cap_tol)
        if c <= left:
            c = left + cap_tol
        if c >= right:
            c = right - cap_tol

        status.info(f"Testing C = {c:.4f} F; interval = [{left:.4f}, {right:.4f}]")

        t_rise, deltaT, t_arr, v_arr = compute_log_times(c, model_name)
        if t_rise is None:  # Check for MATLAB errors
            break

        err = abs(deltaT - target_dt)
        if err < bestErr:
            bestErr = err
            bestC = c
            bestDt = deltaT
            t_data, v_data = t_arr, v_arr
            best_t_rise = t_rise

        if err <= tol_dt:
            status.success(f"Converged early: C={c:.4f}F ±{cap_tol}F, Δt err {err:.4f}s")
            return bestC, bestDt, bestErr, cap_tol, t_data, v_data, best_t_rise

        if deltaT < target_dt:
            left = c
        else:
            right = c

    status.success(
        f"Sweep done: Best C ≈ {bestC:.4f}F ±{cap_tol:.4f}F, "
        f"Δt={bestDt:.4f}s err ±{bestErr:.4f}s"
    )
    return bestC, bestDt, bestErr, cap_tol, t_data, v_data, best_t_rise

def plot_voltage_time(t_data, v_data, x_lim=(0, 100), figsize=(6, 4), title_size=16, label_size=14, tick_size=12):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(t_data, v_data, linewidth=2, color='#4682B4')
    ax.set_title("Capacitor Voltage vs. Time", fontsize=title_size, pad=10)
    ax.set_xlabel("Time (s)", fontsize=label_size)
    ax.set_ylabel("Vcap (V)", fontsize=label_size)
    ax.set_xlim(x_lim)
    ax.tick_params(labelsize=tick_size)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_facecolor('#f8f9fa')
    fig.tight_layout()
    st.pyplot(fig)


def main():
    st.title("ABS Super-Capacitor Calculator")
    st.markdown("\n\n")
    st.markdown("\n\n")

    with st.container():
        with st.expander("Current Profile"):
            myFlag = st.radio("", ["Periodic", "Non-Periodic"], horizontal=True, key="profile")
            if myFlag == "Periodic":
                time_period_ms = st.number_input(
                    "Time period (ms)",
                    1.0, 100000.0, value=100.0, format="%.3f",
                    help="Total duration of one current cycle (ms)."
                )
                spike_time_ms = st.number_input(
                    "Spike time (ms)",
                    min_value=0.0, max_value=time_period_ms, value=20.0, format="%.3f",
                    help="Duration of the high-current pulse (ms)."
                )
                peak_current = st.number_input(
                    "Peak current (A)",
                    min_value=0.0, value=25.0,
                    help="Maximum current during the spike (Amperes)."
                )
                static_current = st.number_input(
                    "nominal current (A)",
                    min_value=0.0, value=10.0,
                    help="Baseline current outside the spike (Amperes)."
                )
            else:
                spike_time_ms = st.number_input(
                    "Spike time (ms)",
                    min_value=0.0, value=20.0, format="%.3f",
                    help="Duration of the high-current pulse (ms)."
                )
                time_period_ms = 10000.0
                peak_current = st.number_input(
                    "Peak current (A)",
                    min_value=0.0, value=25.0,
                    help="Maximum current during the spike (Amperes)."
                )
                static_current = st.number_input(
                    "Nominal current (A)",
                    min_value=0.0, value=10.0,
                    help="Baseline current outside the spike (Amperes)."
                )

            # Input validation
            if myFlag == "Periodic" and spike_time_ms > time_period_ms:
                st.error("Spike time cannot exceed time period in Periodic mode.")
                return

            time_period = time_period_ms / 1000.0
            spike_time = spike_time_ms / 1000.0

            plot_current_profile(myFlag, time_period, spike_time,
                                peak_current, static_current,
                                duration=1.0, sample_rate=10000)

    with st.container():
        with st.expander("Current Source Input"):
            CurrentSource = st.number_input(
                "Current Source (A)",
                min_value=0.0, value=4.0, format="%.4f",
                help="Constant current supplied to the system (Amperes)."
            )

    with st.container():
        with st.expander("Select Charging Model"):
            model_option = st.radio(
                "Super-Cap Charging Model",
                [ "14V Charging","48V Charging"],
                horizontal=True,
                help="Select the voltage model for the ABS system."
            )
            model_map = {
                "48V Charging": "Week_6_day_4_original",
                "14V Charging": "Week_5_day_4_original"
            }
            model_name = model_map[model_option]

    eng = get_matlab_engine()
    eng.workspace['myFlag'] = bool(myFlag == "Periodic")
    eng.workspace['low_current'] = static_current
    eng.workspace['high_current'] = peak_current
    eng.workspace['TimePeriod'] = time_period
    eng.workspace['SpikeTime'] = spike_time
    eng.workspace['CurrentSource'] = CurrentSource
    if myFlag == "Periodic":
        eng.workspace['OnTime'] = (spike_time / time_period) * 100.0
    else:
        eng.workspace['OnTime'] = 1000.0

    mode = st.radio("Select Mode:", ["Find ABS On/Off Time", "Find Capacitor Value"], horizontal=True)

    if mode.startswith("Find ABS On/Off Time"):
        st.header("Given Capacitance → Get On/Off Time")
        C_val = st.number_input(
            "Capacitance (F)",
            min_value=0.0, value=22.5, format="%.4f",
            help="Capacitance value to compute charging/discharging times (Farads)."
        )
        if C_val <= 0:
            st.error("Capacitance must be positive.")
            return
        if st.button("Compute Times"):
            with st.spinner("Simulating in MATLAB..."):
                t_rise, deltaT, t, Vcap = compute_log_times(C_val, model_name)
            if t_rise is not None:
                st.success("Simulation Complete.")
                graph_limit = t_rise + deltaT
                st.metric("ABS Off Time (Charging)", f"{t_rise:.4f} s")
                st.metric("ABS On Time (Discharging)", f"{deltaT:.4f} s")
                
                plot_current_profile(myFlag, time_period, spike_time, peak_current, static_current, duration= deltaT, sample_rate=10000)

                plot_voltage_time(t, Vcap, x_lim=(0, 5 * graph_limit))
                
                st.markdown("\n\n")
                st.markdown("\n\n")
                st.markdown(
                    f"""<div style='font-size:20px; font-weight:bold;'>
                    The ABS on time signifies that the super‑capacitor will be able to provide the load current for {deltaT:.4f} seconds, 
                    and the ABS off time signifies that the super‑capacitor will be charging for {t_rise:.4f} seconds and ABS will be inactive during this period.
                    </div>""",
                    unsafe_allow_html=True
                )

                st.markdown(
                    """<div style='font-size:20px; font-weight:bold;'>
                    The Super-Capacitor during this period of charging and discharging will vary within 12V and 14.4V as shown in the above graph.
                    </div>""",
                    unsafe_allow_html=True
                )



                # Generate PDF report
                inputs = {
                    "Profile": myFlag,
                    "Time Period (ms)": f"{time_period_ms:.3f}",
                    "Spike Time (ms)": f"{spike_time_ms:.3f}",
                    "Peak Current (A)": f"{peak_current:.2f}",
                    "Static Current (A)": f"{static_current:.2f}",
                    "Current Source (A)": f"{CurrentSource:.4f}",
                    "Capacitance (F)": f"{C_val:.4f}",
                    "Charging Model": model_option
                }

                note=(
                    f"The ABS on time signifies that the super-capacitor will be able to provide the load current for "
                    f"{deltaT:.4f} seconds, and the ABS off time signifies that the super-capacitor will be charging for "
                    f"{t_rise:.4f} seconds (ABS will be inactive during this period).\n"
                    f"The super-capacitor voltage during this period will vary between 12 V and 14.4 V as shown in the graph."
                )
                results = {
                    "ABS Off Time (s)": f"{t_rise:.4f}",
                    "ABS On Time (s)": f"{deltaT:.4f}",
                    "Notes": note
                }
                pdf_buffer = generate_pdf_report(mode, inputs, results)
                st.download_button(
                    label="Download Report",
                    data=pdf_buffer,
                    file_name="abs_calculator_report.pdf",
                    mime="application/pdf"
                )

    else:
        st.header("Target ABS On Time → Find Capacitance")
        target_dt = st.number_input(
            "Target ABS On time (s)",
            min_value=0.0, value=6.0, format="%.4f",
            help="Desired discharge time for the capacitor (seconds)."
        )
        if target_dt <= 0:
            st.error("Target ABS On time must be positive.")
            return
        cap_tol = st.selectbox(
            "Desired Capacitance Accuracy (±F)",
            options=[ 0.5, 1.0, 0.1, 0.05, 0.01],
            help="Precision for the capacitance value (Farads)."
        )
        c_min, c_max = st.slider(
            "Sweep Cap Range (F)",
            min_value=1.0,
            max_value=200.0,
            value=(0.0, 90.0),
            step=cap_tol,
            help="Range of capacitance values to search (Farads)."
        )
        if c_min >= c_max:
            st.error("Minimum capacitance must be less than maximum capacitance.")
            return
        if st.button("Find Best Capacitance"):
            with st.spinner("Running binary‐search sweep in MATLAB..."):
                bestC, bestDt, bestErr, accuracy, bestT, bestV, best_charge_time = sweep_for_cap(
                    target_dt=target_dt,
                    c_min=c_min,
                    c_max=c_max,
                    tol_dt=1e-3,
                    cap_tol=cap_tol,
                    model_name=model_name
                )
            if bestC is not None:
                st.success("Sweep Complete.")
                st.markdown("### **Optimal Result**")
                st.metric("Best Capacitance", f"{bestC:.4f} F ±{accuracy:.4f} F")
                st.metric("ABS Off Time (Charging)", f"{best_charge_time:.4f} s")
                st.metric("Achieved ABS On Time(Discharging)", f"{bestDt:.4f} s")
                st.metric("Absolute Error", f"±{bestErr:.4f} s")
                graph_limit = best_charge_time + bestDt
                plot_current_profile(myFlag, time_period, spike_time, peak_current, static_current, duration=bestDt, sample_rate=10000)

                plot_voltage_time(bestT, bestV, x_lim=(0, 5 * graph_limit))
                
                st.markdown(
                    f"**The minimum super-capacitor value that will achieve an ABS on-time of "
                    f"{bestDt:.4f} s is {bestC:.4f} F within the provided range.**"
                )

                st.markdown(
                    f"**This means that to get ABS operation of {bestDt:.4f} s without interruption, "
                    f"you will need at least {bestC:.4f} F of super-capacitor capacity.**"
                )


                # Generate PDF report
                inputs = {
                    "Profile": myFlag,
                    "Time Period (ms)": f"{time_period_ms:.3f}",
                    "Spike Time (ms)": f"{spike_time_ms:.3f}",
                    "Peak Current (A)": f"{peak_current:.2f}",
                    "Static Current (A)": f"{static_current:.2f}",
                    "Current Source (A)": f"{CurrentSource:.4f}",
                    "Target ABS On Time (s)": f"{target_dt:.4f}",
                    "Capacitance Range (F)": f"{c_min:.2f} to {c_max:.2f}",
                    "Capacitance Accuracy (±F)": f"{cap_tol:.2f}",
                    "Charging Model": model_option
                }
                notes = (
                    f"The minimum super-capacitor value that will achieve an ABS on-time of "
                    f"{bestDt:.4f} s is {bestC:.4f} F within the provided range.\n"
                    f"This means that to get ABS operation of {bestDt:.4f} s without interruption, "
                    f"you will need at least {bestC:.4f} F of super-capacitor capacity, "
                    "with voltage swinging between 12 V and 14.4 V as shown above."
                )

                results = {
                    "Best Capacitance (F)": f"{bestC:.4f} ±{accuracy:.4f}",
                    "Achieved ABS On Time (s)": f"{bestDt:.4f}",
                    "Absolute Error (s)": f"±{bestErr:.4f}",
                    "Notes":notes
                }
                pdf_buffer = generate_pdf_report(mode, inputs, results)
                st.download_button(
                    label="Download Report",
                    data=pdf_buffer,
                    file_name="abs_calculator_report.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("No suitable capacitor found within the given range.")


                # # Footer
    st.markdown(
        '<div class="footer">Made by System Engineering Team</div>',
        unsafe_allow_html=True
    )
    
    # 2) Define the hidden “easter egg” button in Python
    # if st.button("easter_snow", key="easter_key"):
    #     st.snow()

    # # 3) Render the footer plus CSS that positions the invisible button on top of it
    # st.markdown(
    #     """
    #     <style>
    #     /* Footer text styling */
    #     .footer {
    #         position: relative;
    #         display: inline-block;
    #         cursor: pointer;
    #         color: gray;
    #         font-size: 14px;
    #     }
    #     .stButton button {
    #         opacity: 0;
    #         position: absolute;
    #         top: 0; left: 0;
    #         width: 100%; height: 100%;
    #         cursor: pointer;
    #     }
    #     </style>
    #     <div class="footer">
    #     Made by System Engineering Team
    #     <!-- this empty div will pick up the click via the hidden button -->
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
        

if __name__ == "__main__":
    main()


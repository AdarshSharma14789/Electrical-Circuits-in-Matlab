


function [t_rise, deltaT, t, Vcap] = LogTimes(C_val, modelName)

    periodic        = evalin('base', 'periodic');
    static_current  = evalin('base', 'low_current');
    peak_current    = evalin('base', 'high_current');
    TimePeriod      = evalin('base', 'TimePeriod');
    SpikeTime       = evalin('base', 'SpikeTime');
    CurrentSource   = evalin('base', 'CurrentSource');

    % Compute derived value
    OnTime = (SpikeTime / TimePeriod) * 100;

    % Assign them into base again (if Simulink blocks depend on them during sim)
    assignin('base', 'myFlag',       periodic);
    assignin('base', 'low_current',  static_current);
    assignin('base', 'high_current', peak_current);
    assignin('base', 'TimePeriod',   TimePeriod);
    assignin('base', 'SpikeTime',    SpikeTime);
    assignin('base', 'OnTime',       OnTime);
    assignin('base', 'CurrentSource',CurrentSource);
    assignin('base', 'C_val',        C_val);
    assignin('base', 'modelName',modelName);

    % Run Simulink simulation
    simOut = sim(modelName, 'ReturnWorkspaceOutputs','on');

    % Extract output data
    Vcap = simOut.VcapLog.Data;
    t    = simOut.VcapLog.Time;

    riseIdx = find(Vcap >= 14.4 - 1e-6, 1, 'first');
    fallIdx = find(Vcap <= 12 + 1e-6 & t > t(riseIdx), 1, 'first');

    if isempty(riseIdx) || isempty(fallIdx)
        error('For C_val = %.2f F, voltage never crossed thresholds.', C_val);
    end

    t_rise  = t(riseIdx);
    deltaT  = t(fallIdx) - t_rise;
    
end



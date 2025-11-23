function [N, activity, half_lives] = decay_chain(N0, lambda, t)
% DECAY_CHAIN Calculate radioactive decay chain
%
% [N, activity, half_lives] = decay_chain(N0, lambda, t)
%
% Inputs:
%   N0 - Initial number of atoms (vector for chain)
%   lambda - Decay constants (s⁻¹, vector)
%   t - Time (s, scalar or vector)
%
% Outputs:
%   N - Number of atoms at time t
%   activity - Activity A(t) = λN(t) (Bq)
%   half_lives - Half-lives T_1/2 = ln(2)/λ (s)
%
% For decay chain: A → B → C → ...
%   dN_A/dt = -λ_A N_A
%   dN_B/dt = λ_A N_A - λ_B N_B
%   etc.

    % Calculate half-lives
    half_lives = log(2) ./ lambda;
    
    % Initialize output arrays
    if isscalar(t)
        t = [0, t];
    end
    
    N = zeros(length(N0), length(t));
    activity = zeros(length(N0), length(t));
    
    % For each nuclide in chain
    for i = 1:length(N0)
        if i == 1
            % First nuclide: simple exponential decay
            N(i, :) = N0(i) * exp(-lambda(i) * t);
        else
            % Subsequent nuclides: Bateman equations
            % Simplified: N_i(t) = N_{i-1}(0) * λ_{i-1} * [exp(-λ_{i-1}t) - exp(-λ_i t)] / (λ_i - λ_{i-1})
            % Plus decay from previous step
            if lambda(i) ~= lambda(i-1)
                N(i, :) = N0(i-1) * lambda(i-1) * ...
                    (exp(-lambda(i-1) * t) - exp(-lambda(i) * t)) / ...
                    (lambda(i) - lambda(i-1));
            else
                % Special case: equal decay constants
                N(i, :) = N0(i-1) * lambda(i-1) * t .* exp(-lambda(i) * t);
            end
            
            % Add initial amount if present
            if N0(i) > 0
                N(i, :) = N(i, :) + N0(i) * exp(-lambda(i) * t);
            end
        end
        
        % Activity: A = λN
        activity(i, :) = lambda(i) * N(i, :);
    end
    
    % If single time point, return single values
    if length(t) == 2 && t(1) == 0
        N = N(:, end);
        activity = activity(:, end);
    end
end


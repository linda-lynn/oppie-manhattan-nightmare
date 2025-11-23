function [T, probability, kappa] = quantum_tunneling(m, V0, E, width, x)
% QUANTUM_TUNNELING Calculate quantum tunneling probability
%
% [T, probability, kappa] = quantum_tunneling(m, V0, E, width, x)
%
% Inputs:
%   m - Particle mass (kg)
%   V0 - Barrier height (J)
%   E - Particle energy (J)
%   width - Barrier width (m)
%   x - Position vector (m, optional for probability calculation)
%
% Outputs:
%   T - Transmission coefficient
%   probability - Tunneling probability
%   kappa - Decay constant κ = √(2m(V-E))/ℏ
%
% Formula: T = exp(-2κa) for rectangular barrier
%          T = exp(-2∫κ(x)dx) for general barrier

    % Physical constants
    hbar = 1.0545718e-34;  % J·s
    
    % Decay constant
    kappa = sqrt(2 * m * (V0 - E)) / hbar;
    
    % For rectangular barrier
    T = exp(-2 * kappa * width);
    probability = T;
    
    % For general barrier (if x is provided)
    if nargin >= 5 && ~isempty(x)
        % Calculate κ(x) for each position
        % Assuming V(x) varies with position
        % This is a simplified version - can be extended
        kappa_x = sqrt(2 * m * (V0 - E)) / hbar * ones(size(x));
        
        % Integration: T = exp(-2∫κ(x)dx)
        if length(x) > 1
            dx = x(2) - x(1);
            integral_kappa = trapz(x, kappa_x);
            T = exp(-2 * integral_kappa);
            probability = T;
        end
    end
end


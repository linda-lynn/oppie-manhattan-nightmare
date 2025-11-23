function [B, B_per_nucleon, terms] = binding_energy(Z, A)
% BINDING_ENERGY Calculate nuclear binding energy using semi-empirical mass formula
%
% [B, B_per_nucleon, terms] = binding_energy(Z, A)
%
% Inputs:
%   Z - Atomic number (proton number)
%   A - Mass number (nucleon number)
%
% Outputs:
%   B - Total binding energy (MeV)
%   B_per_nucleon - Binding energy per nucleon (MeV)
%   terms - Structure containing individual terms:
%       .volume - Volume term
%       .surface - Surface term
%       .coulomb - Coulomb term
%       .asymmetry - Asymmetry term
%       .pairing - Pairing term
%
% Formula: B = a_v*A - a_s*A^(2/3) - a_c*Z²/A^(1/3) - a_a*(A-2Z)²/A + δ
%
% Coefficients (MeV):
%   a_v = 15.8  (volume)
%   a_s = 18.3  (surface)
%   a_c = 0.714 (Coulomb)
%   a_a = 23.2  (asymmetry)
%   δ = 12/√A for even-even, -12/√A for odd-odd, 0 for odd-A

    % Coefficients
    a_v = 15.8;   % MeV
    a_s = 18.3;   % MeV
    a_c = 0.714;  % MeV
    a_a = 23.2;   % MeV
    
    % Calculate individual terms
    terms.volume = a_v * A;
    terms.surface = -a_s * A^(2/3);
    terms.coulomb = -a_c * Z^2 / A^(1/3);
    terms.asymmetry = -a_a * (A - 2*Z)^2 / A;
    
    % Pairing term
    if mod(A, 2) == 0 && mod(Z, 2) == 0
        % Even-even
        terms.pairing = 12 / sqrt(A);
    elseif mod(A, 2) == 1
        % Odd-A
        terms.pairing = 0;
    else
        % Odd-odd
        terms.pairing = -12 / sqrt(A);
    end
    
    % Total binding energy
    B = terms.volume + terms.surface + terms.coulomb + ...
        terms.asymmetry + terms.pairing;
    
    % Binding energy per nucleon
    B_per_nucleon = B / A;
end


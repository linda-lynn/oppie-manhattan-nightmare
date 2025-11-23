function [M_critical, R_critical, k_eff, factors] = critical_mass(Z, A, density, geometry)
% CRITICAL_MASS Calculate critical mass for fissile material
%
% [M_critical, R_critical, k_eff, factors] = critical_mass(Z, A, density, geometry)
%
% Inputs:
%   Z - Atomic number
%   A - Mass number
%   density - Material density (kg/m³)
%   geometry - 'sphere', 'cylinder', or 'slab'
%
% Outputs:
%   M_critical - Critical mass (kg)
%   R_critical - Critical radius/dimension (m)
%   k_eff - Effective multiplication factor
%   factors - Structure with four-factor formula components:
%       .eta - Neutron reproduction factor
%       .epsilon - Fast fission factor
%       .p - Resonance escape probability
%       .f - Thermal utilization factor
%
% Uses four-factor formula: k_eff = η × ε × p × f

    % Physical constants
    hbar = 1.0545718e-34;  % J·s
    m_n = 1.674927e-27;    % Neutron mass (kg)
    
    % Typical values for U-235 (can be adjusted for other nuclides)
    % Neutron reproduction factor
    nu = 2.43;  % Average neutrons per fission
    sigma_f = 585e-28;  % Fission cross section (m²) at thermal
    sigma_c = 99e-28;   % Capture cross section (m²) at thermal
    factors.eta = nu * sigma_f / (sigma_f + sigma_c);
    
    % Fast fission factor (slight enhancement)
    factors.epsilon = 1.03;
    
    % Resonance escape probability (depends on moderator)
    factors.p = 0.9;
    
    % Thermal utilization factor
    factors.f = 0.8;
    
    % Effective multiplication factor
    k_eff = factors.eta * factors.epsilon * factors.p * factors.f;
    
    % Diffusion coefficient (m)
    D = 0.9e-2;  % Typical value in meters
    
    % Macroscopic cross sections (m⁻¹)
    N = density * 6.022e23 / (A * 1.6605e-27);  % Number density
    Sigma_f = N * sigma_f;
    Sigma_a = N * (sigma_f + sigma_c);
    
    % Material buckling
    B_squared_m = (nu * Sigma_f - Sigma_a) / D;
    
    % Geometric buckling depends on geometry
    switch lower(geometry)
        case 'sphere'
            % For sphere: B²_g = (π/R)²
            R_critical = pi / sqrt(B_squared_m);
            M_critical = (4/3) * pi * R_critical^3 * density;
            
        case 'cylinder'
            % For infinite cylinder: B²_g = (2.405/R)²
            R_critical = 2.405 / sqrt(B_squared_m);
            % Assuming unit height
            M_critical = pi * R_critical^2 * density;
            
        case 'slab'
            % For infinite slab: B²_g = (π/a)² where a is half-thickness
            a_critical = pi / sqrt(B_squared_m);
            R_critical = 2 * a_critical;  % Full thickness
            % Assuming unit area
            M_critical = R_critical * density;
            
        otherwise
            error('Geometry must be ''sphere'', ''cylinder'', or ''slab''');
    end
end


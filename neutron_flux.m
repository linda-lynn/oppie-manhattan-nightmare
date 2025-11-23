function [phi, reaction_rate, flux_profile] = neutron_flux(n, v, Sigma, geometry, dimensions)
% NEUTRON_FLUX Calculate neutron flux and reaction rates
%
% [phi, reaction_rate, flux_profile] = neutron_flux(n, v, Sigma, geometry, dimensions)
%
% Inputs:
%   n - Neutron density (neutrons/m³)
%   v - Neutron velocity (m/s)
%   Sigma - Macroscopic cross section (m⁻¹)
%   geometry - 'point', 'plane', 'sphere', or 'cylinder'
%   dimensions - Geometry-specific dimensions (m)
%
% Outputs:
%   phi - Neutron flux (neutrons/m²/s)
%   reaction_rate - Reaction rate (reactions/m³/s)
%   flux_profile - Spatial flux profile (if applicable)

    % Basic flux calculation: φ = nv
    phi = n * v;
    
    % Reaction rate: R = φΣ
    reaction_rate = phi * Sigma;
    
    % Spatial flux profile (simplified)
    switch lower(geometry)
        case 'point'
            % Point source: φ(r) = S/(4πr²)
            r = dimensions;
            S = phi * 4 * pi * r^2;  % Source strength
            flux_profile.r = r;
            flux_profile.phi = phi;
            
        case 'plane'
            % Plane source: uniform flux
            flux_profile.x = dimensions;
            flux_profile.phi = phi * ones(size(dimensions));
            
        case 'sphere'
            % Spherical: φ(r) = φ₀ * sin(πr/R) / (πr/R)
            R = dimensions;
            r = linspace(0, R, 100);
            phi_0 = phi;
            flux_profile.r = r;
            flux_profile.phi = phi_0 * sin(pi * r / R) ./ (pi * r / R);
            flux_profile.phi(1) = phi_0;  % Handle r=0
            
        case 'cylinder'
            % Cylindrical: φ(r) = φ₀ * J₀(2.405r/R)
            R = dimensions;
            r = linspace(0, R, 100);
            phi_0 = phi;
            % Using Bessel function approximation
            flux_profile.r = r;
            flux_profile.phi = phi_0 * besselj(0, 2.405 * r / R);
            
        otherwise
            flux_profile = struct();
    end
end


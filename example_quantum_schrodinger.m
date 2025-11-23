% quantum_schrodinger_solver.m
% Solves the time-independent Schrödinger equation
% for a particle in a potential well
% 
% Equation: H*psi = E*psi
% Where H = -hbar^2/(2m) * d^2/dx^2 + V(x)
%
% This implements the quantum mechanical wave function solution

function [E, psi] = quantum_schrodinger_solver(V, x, m)
    % Parameters:
    %   V: potential energy function V(x)
    %   x: position vector
    %   m: particle mass
    
    % Physical constants
    hbar = 1.0545718e-34;  % Reduced Planck constant (J·s)
    
    % Hamiltonian operator: H = -hbar^2/(2m) * d^2/dx^2 + V(x)
    % Discretize the second derivative
    dx = x(2) - x(1);
    N = length(x);
    
    % Kinetic energy operator (finite difference)
    T = -hbar^2/(2*m) * (diag(ones(N-1,1),1) - 2*eye(N) + diag(ones(N-1,1),-1)) / dx^2;
    
    % Potential energy operator (diagonal)
    V_matrix = diag(V);
    
    % Total Hamiltonian
    H = T + V_matrix;
    
    % Solve eigenvalue problem: H*psi = E*psi
    [psi, E] = eig(H);
    E = diag(E);
    
    % Normalize wave functions
    for i = 1:length(E)
        psi(:,i) = psi(:,i) / sqrt(trapz(x, abs(psi(:,i)).^2));
    end
end

% Example usage:
% x = linspace(-10, 10, 1000);
% V = 0.5 * x.^2;  % Harmonic oscillator potential
% m = 9.109e-31;   % Electron mass
% [E, psi] = quantum_schrodinger_solver(V, x, m);

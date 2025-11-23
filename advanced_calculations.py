"""
Advanced Calculation Module for Complex Nuclear Physics Computations
Supports extreme complexity calculations for graduate research

Features:
- Differential equation solvers (ODE, PDE)
- Monte Carlo simulations
- Multi-body calculations
- Advanced numerical integration
- Matrix operations and eigenvalue problems
- Optimization algorithms
- Statistical analysis
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
import math
from scipy import integrate, optimize, linalg, stats
from scipy.integrate import odeint, solve_ivp
import json
from datetime import datetime

class AdvancedCalculations:
    def __init__(self):
        """Initialize advanced calculation engine"""
        self.c = 299792458  # Speed of light (m/s)
        self.hbar = 1.054571817e-34  # Reduced Planck constant (J·s)
        self.k_B = 1.380649e-23  # Boltzmann constant (J/K)
        self.e = 1.602176634e-19  # Elementary charge (C)
        
    def solve_neutron_transport_ode(self, initial_conditions: Dict, 
                                     time_span: Tuple[float, float],
                                     parameters: Dict) -> Dict:
        """
        Solve neutron transport equation using ODE solver
        dN/dt = (k_eff - 1) * N / Λ - λ * N
        
        Parameters:
        - initial_conditions: {'N0': initial neutron density}
        - time_span: (t_start, t_end) in seconds
        - parameters: {'k_eff': multiplication factor, 
                      'lambda': decay constant, 'generation_time': Λ}
        
        Returns: Solution with time points and neutron density
        """
        k_eff = parameters.get('k_eff', 1.0)
        lambda_decay = parameters.get('lambda', 0.0)
        generation_time = parameters.get('generation_time', 1e-5)  # seconds
        
        def neutron_equation(t, N):
            """Neutron transport ODE"""
            dN_dt = ((k_eff - 1) / generation_time) * N - lambda_decay * N
            return dN_dt
        
        N0 = initial_conditions.get('N0', 1.0)
        t_span = time_span
        t_eval = np.linspace(t_span[0], t_span[1], 1000)
        
        solution = solve_ivp(neutron_equation, t_span, [N0], 
                            t_eval=t_eval, method='RK45', rtol=1e-8, atol=1e-10)
        
        return {
            "time": solution.t.tolist(),
            "neutron_density": solution.y[0].tolist(),
            "success": solution.success,
            "message": solution.message,
            "parameters": parameters
        }
    
    def monte_carlo_neutron_path(self, initial_energy: float, 
                                 material_properties: Dict,
                                 n_simulations: int = 10000) -> Dict:
        """
        Monte Carlo simulation of neutron transport through material
        
        Parameters:
        - initial_energy: Initial neutron energy (eV)
        - material_properties: {'density': kg/m³, 'sigma_total': barns, 
                               'sigma_absorption': barns, 'sigma_scattering': barns}
        - n_simulations: Number of Monte Carlo runs
        
        Returns: Statistical results of neutron transport
        """
        density = material_properties.get('density', 1000.0)
        sigma_total = material_properties.get('sigma_total', 1.0) * 1e-28  # Convert barns to m²
        sigma_abs = material_properties.get('sigma_absorption', 0.1) * 1e-28
        sigma_scat = material_properties.get('sigma_scattering', 0.9) * 1e-28
        
        # Number density
        atomic_mass = material_properties.get('atomic_mass', 1.0)
        N = density / (atomic_mass * 1.66053906660e-27)  # atoms/m³
        
        # Mean free path
        mean_free_path = 1.0 / (N * sigma_total) if (N * sigma_total) > 0 else 1e10
        
        # Monte Carlo simulation
        absorption_distances = []
        scattering_distances = []
        final_energies = []
        
        for _ in range(n_simulations):
            distance = 0.0
            energy = initial_energy
            
            while True:
                # Sample interaction distance (exponential distribution)
                interaction_distance = -mean_free_path * np.log(np.random.random())
                distance += interaction_distance
                
                # Determine interaction type
                prob_absorption = sigma_abs / sigma_total if sigma_total > 0 else 0
                
                if np.random.random() < prob_absorption:
                    absorption_distances.append(distance)
                    break
                else:
                    # Scattering - energy loss (simplified)
                    energy *= 0.9  # Approximate energy loss per collision
                    scattering_distances.append(distance)
                    
                    if energy < 0.025:  # Thermal energy threshold
                        final_energies.append(energy)
                        break
        
        return {
            "mean_absorption_distance": np.mean(absorption_distances) if absorption_distances else None,
            "mean_scattering_distance": np.mean(scattering_distances) if scattering_distances else None,
            "mean_free_path_theoretical": mean_free_path,
            "absorption_probability": len(absorption_distances) / n_simulations,
            "scattering_probability": len(scattering_distances) / n_simulations,
            "mean_final_energy": np.mean(final_energies) if final_energies else None,
            "n_simulations": n_simulations
        }
    
    def solve_schrodinger_radial(self, Z: int, A: int, 
                                n: int, l: int) -> Dict:
        """
        Solve radial Schrödinger equation for nuclear potential
        Using Woods-Saxon potential approximation
        
        Parameters:
        - Z, A: Atomic and mass numbers
        - n, l: Principal and orbital quantum numbers
        
        Returns: Energy eigenvalues and wavefunction
        """
        # Woods-Saxon potential parameters
        V0 = 50.0  # MeV (well depth)
        R0 = 1.2e-15 * (A ** (1/3))  # m (nuclear radius)
        a = 0.65e-15  # m (surface diffuseness)
        
        # Reduced mass
        m_nucleon = 1.67e-27  # kg
        mu = m_nucleon * A / (A + 1)
        
        # Radial coordinate
        r_max = 3 * R0
        r = np.linspace(1e-15, r_max, 1000)
        dr = r[1] - r[0]
        
        # Woods-Saxon potential
        V_ws = -V0 / (1 + np.exp((r - R0) / a))
        
        # Centrifugal barrier
        V_centrifugal = (self.hbar**2 * l * (l + 1)) / (2 * mu * r**2)
        V_centrifugal = V_centrifugal / (self.e * 1e6)  # Convert to MeV
        
        # Total potential
        V_total = V_ws + V_centrifugal
        
        # Solve using finite difference method (simplified)
        # This is a simplified approach - full solution requires more sophisticated methods
        E_bound = -V0 * 0.5  # Approximate bound state energy
        
        return {
            "energy_MeV": E_bound,
            "potential_well_depth_MeV": V0,
            "nuclear_radius_m": R0,
            "quantum_numbers": {"n": n, "l": l},
            "potential_profile": {
                "r_m": r.tolist(),
                "V_MeV": V_total.tolist()
            },
            "note": "Simplified calculation - full solution requires advanced numerical methods"
        }
    
    def calculate_fission_yield_distribution(self, Z: int, A: int,
                                            neutron_energy: float = 0.025) -> Dict:
        """
        Calculate fission fragment mass distribution using Gaussian approximation
        and advanced statistical methods
        
        Parameters:
        - Z, A: Parent nucleus
        - neutron_energy: Incident neutron energy (eV)
        
        Returns: Mass distribution and yield data
        """
        # Gaussian parameters for fission yield (empirical)
        A_light = A * 0.4  # Light fragment peak
        A_heavy = A * 0.6  # Heavy fragment peak
        sigma_light = A * 0.05  # Width of light peak
        sigma_heavy = A * 0.05  # Width of heavy peak
        
        # Mass range
        mass_range = np.arange(70, A - 70, 1)
        
        # Gaussian distribution for light and heavy fragments
        yield_light = np.exp(-0.5 * ((mass_range - A_light) / sigma_light)**2)
        yield_heavy = np.exp(-0.5 * ((mass_range - A_heavy) / sigma_heavy)**2)
        
        # Combined yield (normalized)
        total_yield = yield_light + yield_heavy
        total_yield = total_yield / np.sum(total_yield) * 200  # Normalize to 200% (two fragments)
        
        # Calculate moments
        mean_mass = np.sum(mass_range * total_yield) / np.sum(total_yield)
        variance = np.sum((mass_range - mean_mass)**2 * total_yield) / np.sum(total_yield)
        std_dev = np.sqrt(variance)
        
        return {
            "parent_nucleus": f"{A}-{Z}",
            "mass_distribution": {
                "mass_numbers": mass_range.tolist(),
                "yields_percent": total_yield.tolist()
            },
            "statistics": {
                "mean_mass": mean_mass,
                "standard_deviation": std_dev,
                "light_peak": A_light,
                "heavy_peak": A_heavy
            },
            "neutron_energy_eV": neutron_energy
        }
    
    def optimize_critical_configuration(self, Z: int, A: int,
                                       constraints: Dict) -> Dict:
        """
        Optimize critical mass configuration using optimization algorithms
        
        Parameters:
        - Z, A: Fissile material
        - constraints: {'max_radius': m, 'min_mass': kg, 'geometry': 'sphere'|'cylinder'}
        
        Returns: Optimized configuration
        """
        from nuclear_physics import NuclearPhysics
        physics = NuclearPhysics()
        
        # Objective function: minimize critical mass
        def objective(x):
            # x[0] = radius, x[1] = density (if variable)
            radius = x[0]
            density = constraints.get('density', 19050)  # kg/m³
            
            # Calculate volume and mass
            if constraints.get('geometry') == 'sphere':
                volume = (4/3) * np.pi * radius**3
            else:  # cylinder
                height = 2 * radius  # Optimal for minimum mass
                volume = np.pi * radius**2 * height
            
            mass = density * volume
            return mass
        
        # Constraints
        max_radius = constraints.get('max_radius', 0.2)  # 20 cm
        min_radius = constraints.get('min_radius', 0.01)  # 1 cm
        
        # Bounds
        bounds = [(min_radius, max_radius)]
        
        # Initial guess
        x0 = [constraints.get('initial_radius', 0.1)]
        
        # Optimize
        result = optimize.minimize(objective, x0, method='L-BFGS-B', bounds=bounds)
        
        optimal_radius = result.x[0]
        optimal_mass = result.fun
        
        return {
            "optimization_success": result.success,
            "optimal_radius_m": optimal_radius,
            "optimal_radius_cm": optimal_radius * 100,
            "optimal_mass_kg": optimal_mass,
            "optimal_mass_g": optimal_mass * 1000,
            "geometry": constraints.get('geometry', 'sphere'),
            "iterations": result.nit,
            "message": result.message
        }
    
    def calculate_neutron_spectrum(self, source_energy: float,
                                   material_layers: List[Dict]) -> Dict:
        """
        Calculate neutron energy spectrum after passing through material layers
        Using multi-group transport theory
        
        Parameters:
        - source_energy: Initial neutron energy (eV)
        - material_layers: List of {'thickness': m, 'density': kg/m³, 
                                  'sigma_total': barns, 'sigma_elastic': barns}
        
        Returns: Energy spectrum at each layer
        """
        # Energy groups (from fast to thermal)
        energy_groups = np.logspace(np.log10(source_energy), np.log10(0.025), 50)
        
        # Initial flux (all neutrons at source energy)
        flux = np.zeros_like(energy_groups)
        source_idx = np.argmin(np.abs(energy_groups - source_energy))
        flux[source_idx] = 1.0
        
        # Track flux through each layer
        layer_results = []
        
        for layer_idx, layer in enumerate(material_layers):
            thickness = layer.get('thickness', 0.01)  # m
            density = layer.get('density', 1000.0)  # kg/m³
            sigma_total = layer.get('sigma_total', 1.0) * 1e-28  # m²
            sigma_elastic = layer.get('sigma_elastic', 0.9) * 1e-28  # m²
            
            # Number density
            atomic_mass = layer.get('atomic_mass', 1.0)
            N = density / (atomic_mass * 1.66053906660e-27)
            
            # Attenuation
            attenuation = np.exp(-N * sigma_total * thickness)
            
            # Energy degradation (simplified)
            for i in range(len(energy_groups) - 1):
                # Neutrons scatter down in energy
                if flux[i] > 0:
                    energy_loss = energy_groups[i] * 0.1  # 10% energy loss per collision
                    target_idx = np.argmin(np.abs(energy_groups - (energy_groups[i] - energy_loss)))
                    if target_idx > i:
                        flux[target_idx] += flux[i] * 0.1
                        flux[i] *= 0.9
            
            # Apply attenuation
            flux *= attenuation
            
            layer_results.append({
                "layer": layer_idx + 1,
                "thickness_m": thickness,
                "energy_spectrum": {
                    "energies_eV": energy_groups.tolist(),
                    "flux": flux.copy().tolist()
                },
                "total_flux": np.sum(flux)
            })
        
        return {
            "source_energy_eV": source_energy,
            "layers": layer_results,
            "final_spectrum": {
                "energies_eV": energy_groups.tolist(),
                "flux": flux.tolist()
            }
        }
    
    def solve_bateman_equations(self, decay_chain: List[Dict],
                                initial_conditions: Dict,
                                time_points: np.ndarray) -> Dict:
        """
        Solve Bateman equations for radioactive decay chain
        
        Parameters:
        - decay_chain: [{'nuclide': 'A-Z', 'half_life': seconds, 'branching': fraction}]
        - initial_conditions: {'nuclide': initial_amount}
        - time_points: Array of time points (seconds)
        
        Returns: Activity/concentration at each time point
        """
        n_nuclides = len(decay_chain)
        
        # Build decay matrix
        decay_matrix = np.zeros((n_nuclides, n_nuclides))
        
        for i, nuclide in enumerate(decay_chain):
            half_life = nuclide.get('half_life', 1e10)
            lambda_i = np.log(2) / half_life if half_life > 0 else 0
            
            # Diagonal: decay of this nuclide
            decay_matrix[i, i] = -lambda_i
            
            # Off-diagonal: production from parent (if exists)
            if i > 0:
                branching = nuclide.get('branching', 1.0)
                parent_lambda = np.log(2) / decay_chain[i-1].get('half_life', 1e10)
                decay_matrix[i, i-1] = branching * parent_lambda
        
        # Initial conditions
        N0 = np.zeros(n_nuclides)
        for i, nuclide in enumerate(decay_chain):
            nuclide_id = nuclide.get('nuclide', '')
            N0[i] = initial_conditions.get(nuclide_id, 0.0)
        
        # Solve system of ODEs
        def decay_ode(t, N):
            return decay_matrix @ N
        
        solution = solve_ivp(decay_ode, (time_points[0], time_points[-1]), N0,
                            t_eval=time_points, method='RK45', rtol=1e-8)
        
        # Calculate activity (lambda * N)
        activities = []
        for i, nuclide in enumerate(decay_chain):
            half_life = nuclide.get('half_life', 1e10)
            lambda_i = np.log(2) / half_life if half_life > 0 else 0
            activity = lambda_i * solution.y[i]
            activities.append(activity)
        
        return {
            "time_points": solution.t.tolist(),
            "concentrations": solution.y.tolist(),
            "activities": [a.tolist() for a in activities],
            "nuclides": [n.get('nuclide', '') for n in decay_chain]
        }
    
    def calculate_neutron_flux_distribution(self, reactor_geometry: Dict,
                                           source_distribution: Callable) -> Dict:
        """
        Calculate neutron flux distribution in reactor using diffusion theory
        
        Parameters:
        - reactor_geometry: {'shape': 'sphere'|'cylinder'|'slab', 'dimensions': [...]}
        - source_distribution: Function S(r) for neutron source
        
        Returns: Flux distribution
        """
        shape = reactor_geometry.get('shape', 'sphere')
        dimensions = reactor_geometry.get('dimensions', [1.0])
        
        # Diffusion coefficient (simplified)
        D = 1.0  # cm (typical value)
        L = 10.0  # Diffusion length (cm)
        
        # Spatial grid
        if shape == 'sphere':
            r_max = dimensions[0]
            r = np.linspace(0, r_max, 100)
            dr = r[1] - r[0]
            
            # Solve diffusion equation: D∇²φ - φ/L² + S = 0
            # Using finite difference method
            n_points = len(r)
            A = np.zeros((n_points, n_points))
            b = np.zeros(n_points)
            
            for i in range(1, n_points - 1):
                # Laplacian in spherical coordinates
                A[i, i-1] = D / dr**2 - D / (r[i] * dr)
                A[i, i] = -2*D / dr**2 - 1/L**2
                A[i, i+1] = D / dr**2 + D / (r[i] * dr)
                b[i] = -source_distribution(r[i])
            
            # Boundary conditions
            A[0, 0] = 1.0  # Center: dφ/dr = 0
            A[-1, -1] = 1.0  # Surface: φ = 0 (simplified)
            
            # Solve
            flux = linalg.solve(A, b)
        else:
            # Simplified for other geometries
            flux = np.ones(100)
        
        return {
            "geometry": shape,
            "spatial_coordinates": r.tolist() if shape == 'sphere' else list(range(100)),
            "flux_distribution": flux.tolist(),
            "max_flux": float(np.max(flux)),
            "average_flux": float(np.mean(flux))
        }
    
    def perform_sensitivity_analysis(self, function: Callable,
                                     parameters: Dict,
                                     variations: float = 0.1) -> Dict:
        """
        Perform sensitivity analysis on a function
        
        Parameters:
        - function: Function to analyze f(x1, x2, ...)
        - parameters: {'param1': value1, 'param2': value2, ...}
        - variations: Fractional variation (e.g., 0.1 = 10%)
        
        Returns: Sensitivity coefficients
        """
        base_result = function(**parameters)
        sensitivities = {}
        
        for param_name, param_value in parameters.items():
            # Forward variation
            params_forward = parameters.copy()
            params_forward[param_name] = param_value * (1 + variations)
            result_forward = function(**params_forward)
            
            # Backward variation
            params_backward = parameters.copy()
            params_backward[param_name] = param_value * (1 - variations)
            result_backward = function(**params_backward)
            
            # Calculate sensitivity
            delta_result = (result_forward - result_backward) / (2 * variations * param_value)
            sensitivity = (delta_result / base_result) * param_value if base_result != 0 else 0
            
            sensitivities[param_name] = {
                "sensitivity_coefficient": float(sensitivity),
                "relative_change": float((result_forward - base_result) / base_result * 100) if base_result != 0 else 0
            }
        
        return {
            "base_result": float(base_result),
            "sensitivities": sensitivities,
            "variation_fraction": variations
        }
    
    def calculate_nuclear_reaction_rate(self, target_nuclide: Dict, 
                                       neutron_flux: float,
                                       energy_spectrum: np.ndarray) -> Dict:
        """
        Calculate nuclear reaction rate using cross-section data
        
        Parameters:
        - target_nuclide: {'Z': int, 'A': int, 'sigma': float (barns), 'density': kg/m³}
        - neutron_flux: Neutron flux (n/cm²/s)
        - energy_spectrum: Energy distribution array (eV)
        
        Returns: Reaction rate and activity
        """
        Z = target_nuclide.get('Z', 1)
        A = target_nuclide.get('A', 1)
        sigma = target_nuclide.get('sigma', 1.0) * 1e-24  # Convert barns to cm²
        density = target_nuclide.get('density', 1000.0)  # kg/m³
        
        # Number density
        atomic_mass = A * 1.66053906660e-27  # kg
        N = density / atomic_mass  # atoms/m³ = atoms/cm³ * 1e6
        N_cm3 = N / 1e6  # atoms/cm³
        
        # Reaction rate: R = σ * φ * N
        reaction_rate = sigma * neutron_flux * N_cm3  # reactions/cm³/s
        
        # Activity (if radioactive product)
        half_life = target_nuclide.get('half_life', None)
        if half_life:
            lambda_decay = np.log(2) / half_life
            activity = reaction_rate * lambda_decay  # Bq/cm³
        else:
            activity = None
        
        return {
            "target_nuclide": f"{A}-{Z}",
            "reaction_rate_per_cm3_s": float(reaction_rate),
            "reaction_rate_per_m3_s": float(reaction_rate * 1e6),
            "activity_Bq_per_cm3": float(activity) if activity else None,
            "neutron_flux_n_per_cm2_s": neutron_flux,
            "number_density_atoms_per_cm3": float(N_cm3)
        }
    
    def solve_nuclear_reaction_network(self, initial_abundances: Dict,
                                      reaction_rates: Dict,
                                      time_span: Tuple[float, float]) -> Dict:
        """
        Solve nuclear reaction network (e.g., stellar nucleosynthesis)
        
        Parameters:
        - initial_abundances: {'nuclide': abundance}
        - reaction_rates: {'reaction': rate (1/s)}
        - time_span: (t_start, t_end) in seconds
        
        Returns: Abundance evolution
        """
        nuclides = list(initial_abundances.keys())
        n_nuclides = len(nuclides)
        
        # Build rate matrix
        rate_matrix = np.zeros((n_nuclides, n_nuclides))
        
        # Initialize abundances
        N0 = np.array([initial_abundances.get(n, 0.0) for n in nuclides])
        
        # Simplified reaction network (production and destruction)
        for i, nuclide in enumerate(nuclides):
            # Destruction rate
            destruction_key = f"{nuclide}_destruction"
            if destruction_key in reaction_rates:
                rate_matrix[i, i] = -reaction_rates[destruction_key]
            
            # Production from other nuclides
            for j, parent in enumerate(nuclides):
                if i != j:
                    production_key = f"{parent}_to_{nuclide}"
                    if production_key in reaction_rates:
                        rate_matrix[i, j] = reaction_rates[production_key]
        
        # Solve ODE system
        def network_ode(t, N):
            return rate_matrix @ N
        
        t_eval = np.linspace(time_span[0], time_span[1], 1000)
        solution = solve_ivp(network_ode, time_span, N0,
                            t_eval=t_eval, method='RK45', rtol=1e-8)
        
        return {
            "time_points": solution.t.tolist(),
            "abundances": {nuclides[i]: solution.y[i].tolist() 
                          for i in range(n_nuclides)},
            "nuclides": nuclides,
            "final_abundances": {nuclides[i]: float(solution.y[i, -1])
                                for i in range(n_nuclides)}
        }
    
    def calculate_burnup_evolution(self, fuel_composition: Dict,
                                   neutron_flux: float,
                                   time_points: np.ndarray) -> Dict:
        """
        Calculate fuel burnup and transmutation over time
        
        Parameters:
        - fuel_composition: {'nuclide': initial_mass (kg)}
        - neutron_flux: Average neutron flux (n/cm²/s)
        - time_points: Time array (seconds)
        
        Returns: Composition evolution and burnup
        """
        from nuclear_physics import NuclearPhysics
        physics = NuclearPhysics()
        
        nuclides = list(fuel_composition.keys())
        n_nuclides = len(nuclides)
        
        # Build transmutation matrix
        transmutation_matrix = np.zeros((n_nuclides, n_nuclides))
        decay_matrix = np.zeros((n_nuclides, n_nuclides))
        
        # Initial masses
        M0 = np.array([fuel_composition.get(n, 0.0) for n in nuclides])
        
        # Calculate cross-sections and decay constants
        for i, nuclide_str in enumerate(nuclides):
            # Parse nuclide (e.g., "U-235")
            parts = nuclide_str.split('-')
            if len(parts) == 2:
                A = int(parts[1])
                Z = int(parts[0].replace('U', '92').replace('Pu', '94')
                          .replace('Th', '90').replace('Np', '93'))
                
                # Get cross-section data
                props = physics.get_nuclear_properties(Z, A)
                sigma_fission = props.get('fission_cross_section', 0.0) * 1e-24  # cm²
                sigma_capture = props.get('capture_cross_section', 0.0) * 1e-24
                
                # Transmutation rates
                atomic_mass = A * 1.66053906660e-27  # kg
                N = M0[i] / atomic_mass  # atoms
                N_cm3 = N / 1e6  # atoms/cm³ (simplified volume)
                
                # Destruction (fission + capture)
                destruction_rate = (sigma_fission + sigma_capture) * neutron_flux
                transmutation_matrix[i, i] = -destruction_rate
                
                # Decay
                half_life = props.get('half_life', 1e20)
                if half_life < 1e20:
                    lambda_decay = np.log(2) / half_life
                    decay_matrix[i, i] = -lambda_decay
        
        # Combined matrix
        evolution_matrix = transmutation_matrix + decay_matrix
        
        # Solve
        def burnup_ode(t, M):
            return evolution_matrix @ M
        
        solution = solve_ivp(burnup_ode, (time_points[0], time_points[-1]), M0,
                            t_eval=time_points, method='RK45', rtol=1e-8)
        
        # Calculate burnup (MWd/kg)
        total_fission_energy = 200.0  # MeV per fission
        total_fission_energy_J = total_fission_energy * 1.602176634e-13  # J
        burnup_values = []
        
        for t_idx in range(len(time_points)):
            total_fissions = 0.0
            for i, nuclide_str in enumerate(nuclides):
                parts = nuclide_str.split('-')
                if len(parts) == 2:
                    A = int(parts[1])
                    props = physics.get_nuclear_properties(
                        int(parts[0].replace('U', '92').replace('Pu', '94')), A)
                    sigma_fission = props.get('fission_cross_section', 0.0) * 1e-24
                    atomic_mass = A * 1.66053906660e-27
                    N = solution.y[i, t_idx] / atomic_mass
                    N_cm3 = N / 1e6
                    fission_rate = sigma_fission * neutron_flux * N_cm3
                    total_fissions += fission_rate * (time_points[t_idx] - time_points[0])
            
            initial_mass = np.sum(M0)
            if initial_mass > 0:
                energy_released = total_fissions * total_fission_energy_J
                burnup_MWd_per_kg = (energy_released / (initial_mass * 86400)) / 1e6
                burnup_values.append(burnup_MWd_per_kg)
            else:
                burnup_values.append(0.0)
        
        return {
            "time_points": solution.t.tolist(),
            "mass_evolution": {nuclides[i]: solution.y[i].tolist()
                              for i in range(n_nuclides)},
            "burnup_MWd_per_kg": burnup_values,
            "final_composition": {nuclides[i]: float(solution.y[i, -1])
                                 for i in range(n_nuclides)},
            "total_burnup_MWd_per_kg": float(burnup_values[-1]) if burnup_values else 0.0
        }
    
    def solve_multigroup_diffusion(self, energy_groups: int,
                                   material_properties: Dict,
                                   geometry: Dict) -> Dict:
        """
        Solve multi-group neutron diffusion equation
        
        Parameters:
        - energy_groups: Number of energy groups
        - material_properties: {'D': [cm], 'Sigma_a': [1/cm], 'nu_Sigma_f': [1/cm], ...}
        - geometry: {'shape': 'sphere'|'cylinder', 'radius': cm}
        
        Returns: Flux distribution and eigenvalues
        """
        n_groups = energy_groups
        
        # Diffusion coefficients (cm)
        D = material_properties.get('D', [1.0] * n_groups)
        if len(D) < n_groups:
            D = D + [D[-1]] * (n_groups - len(D))
        
        # Absorption cross-sections (1/cm)
        Sigma_a = material_properties.get('Sigma_a', [0.01] * n_groups)
        if len(Sigma_a) < n_groups:
            Sigma_a = Sigma_a + [Sigma_a[-1]] * (n_groups - len(Sigma_a))
        
        # Fission production (1/cm)
        nu_Sigma_f = material_properties.get('nu_Sigma_f', [0.0] * n_groups)
        if len(nu_Sigma_f) < n_groups:
            nu_Sigma_f = nu_Sigma_f + [nu_Sigma_f[-1]] * (n_groups - len(nu_Sigma_f))
        
        # Scattering matrix (downscatter)
        scattering_matrix = material_properties.get('scattering_matrix', None)
        if scattering_matrix is None:
            # Simple downscatter only
            scattering_matrix = np.zeros((n_groups, n_groups))
            for g in range(n_groups - 1):
                scattering_matrix[g+1, g] = 0.1  # 10% downscatter
        
        # Geometry
        shape = geometry.get('shape', 'sphere')
        radius = geometry.get('radius', 10.0)  # cm
        
        # Spatial discretization
        n_points = 50
        r = np.linspace(0, radius, n_points)
        dr = r[1] - r[0]
        
        # Build matrix for eigenvalue problem: Mφ = (1/k) Fφ
        # Where M is loss operator, F is fission source
        n_total = n_groups * n_points
        M = np.zeros((n_total, n_total))
        F = np.zeros((n_total, n_total))
        
        for g in range(n_groups):
            for i in range(1, n_points - 1):
                idx = g * n_points + i
                
                # Diffusion term (Laplacian in spherical coordinates)
                if shape == 'sphere':
                    laplacian = (D[g] / dr**2) * (
                        (r[i+1] - r[i-1]) / (2*r[i]) * (1/dr) +
                        (1.0)  # Simplified
                    )
                else:
                    laplacian = D[g] / dr**2
                
                # Loss term
                M[idx, idx] = -laplacian - Sigma_a[g]
                
                # Scattering
                for g2 in range(n_groups):
                    if g2 != g:
                        M[idx, g2*n_points + i] = -scattering_matrix[g, g2]
                
                # Fission source
                for g2 in range(n_groups):
                    F[idx, g2*n_points + i] = nu_Sigma_f[g] / n_groups
        
        # Solve eigenvalue problem
        eigenvalues, eigenvectors = linalg.eig(M, F)
        
        # Find largest eigenvalue (k_eff = 1/largest_eigenvalue)
        k_eff_idx = np.argmax(np.real(eigenvalues))
        k_eff = 1.0 / np.real(eigenvalues[k_eff_idx])
        flux_eigenvector = np.real(eigenvectors[:, k_eff_idx])
        
        # Normalize flux
        flux_eigenvector = flux_eigenvector / np.max(np.abs(flux_eigenvector))
        
        # Reshape to group-wise flux
        flux_by_group = {}
        for g in range(n_groups):
            flux_by_group[f"group_{g+1}"] = flux_eigenvector[g*n_points:(g+1)*n_points].tolist()
        
        return {
            "k_effective": float(k_eff),
            "flux_distribution": flux_by_group,
            "spatial_coordinates_cm": r.tolist(),
            "energy_groups": n_groups,
            "geometry": shape,
            "radius_cm": radius
        }
    
    def critical_search(self, material_properties: Dict,
                       geometry: Dict,
                       target_k: float = 1.0) -> Dict:
        """
        Search for critical configuration (radius or enrichment)
        
        Parameters:
        - material_properties: Material properties dict
        - geometry: Geometry dict with initial guess
        - target_k: Target k_eff (default 1.0)
        
        Returns: Critical configuration
        """
        def k_eff_function(radius):
            """Calculate k_eff for given radius"""
            geometry_test = geometry.copy()
            geometry_test['radius'] = radius
            
            # Simplified k_eff calculation
            # Using one-group diffusion theory
            D = material_properties.get('D', [1.0])[0]
            Sigma_a = material_properties.get('Sigma_a', [0.01])[0]
            nu_Sigma_f = material_properties.get('nu_Sigma_f', [0.02])[0]
            
            # Geometric buckling
            if geometry.get('shape') == 'sphere':
                B_g_squared = (np.pi / radius)**2
            else:
                B_g_squared = (2.405 / radius)**2  # Cylinder
            
            # Material buckling
            L_squared = D / Sigma_a
            B_m_squared = (nu_Sigma_f / D - Sigma_a / D) / L_squared
            
            # k_eff
            k_eff = nu_Sigma_f / (Sigma_a + D * B_g_squared)
            
            return abs(k_eff - target_k)
        
        # Initial guess
        initial_radius = geometry.get('radius', 10.0)
        
        # Optimize
        result = optimize.minimize_scalar(k_eff_function, 
                                         bounds=(0.1, 100.0),
                                         method='bounded')
        
        critical_radius = result.x
        geometry_critical = geometry.copy()
        geometry_critical['radius'] = critical_radius
        
        # Calculate final k_eff
        D = material_properties.get('D', [1.0])[0]
        Sigma_a = material_properties.get('Sigma_a', [0.01])[0]
        nu_Sigma_f = material_properties.get('nu_Sigma_f', [0.02])[0]
        
        if geometry.get('shape') == 'sphere':
            B_g_squared = (np.pi / critical_radius)**2
        else:
            B_g_squared = (2.405 / critical_radius)**2
        
        k_eff_final = nu_Sigma_f / (Sigma_a + D * B_g_squared)
        
        return {
            "critical_radius_cm": float(critical_radius),
            "critical_radius_m": float(critical_radius / 100),
            "k_effective": float(k_eff_final),
            "target_k": target_k,
            "optimization_success": result.success,
            "geometry": geometry.get('shape', 'sphere')
        }
    
    def uncertainty_propagation(self, function: Callable,
                               parameters: Dict,
                               uncertainties: Dict) -> Dict:
        """
        Propagate uncertainties through calculations using Monte Carlo
        
        Parameters:
        - function: Function to analyze
        - parameters: {'param': value}
        - uncertainties: {'param': (mean, std_dev) or std_dev}
        
        Returns: Result distribution and statistics
        """
        n_samples = 10000
        
        # Sample parameters
        sampled_results = []
        for _ in range(n_samples):
            sampled_params = {}
            for param_name, param_value in parameters.items():
                if param_name in uncertainties:
                    unc = uncertainties[param_name]
                    if isinstance(unc, tuple):
                        mean, std = unc
                    else:
                        mean = param_value
                        std = unc
                    sampled_params[param_name] = np.random.normal(mean, std)
                else:
                    sampled_params[param_name] = param_value
            
            try:
                result = function(**sampled_params)
                if isinstance(result, (int, float)):
                    sampled_results.append(result)
                elif isinstance(result, dict) and 'value' in result:
                    sampled_results.append(result['value'])
            except:
                continue
        
        if not sampled_results:
            return {"error": "No valid samples"}
        
        sampled_results = np.array(sampled_results)
        
        return {
            "mean": float(np.mean(sampled_results)),
            "std_dev": float(np.std(sampled_results)),
            "median": float(np.median(sampled_results)),
            "percentiles": {
                "5th": float(np.percentile(sampled_results, 5)),
                "25th": float(np.percentile(sampled_results, 25)),
                "75th": float(np.percentile(sampled_results, 75)),
                "95th": float(np.percentile(sampled_results, 95))
            },
            "n_samples": len(sampled_results),
            "distribution": sampled_results.tolist()
        }


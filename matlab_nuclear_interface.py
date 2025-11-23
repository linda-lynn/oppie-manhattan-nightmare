"""
MATLAB Nuclear Physics Analysis Interface
Integrates MATLAB Engine for Python to perform nuclear physics calculations
"""

import os
import sys
from typing import Dict, List, Optional, Tuple, Any
import numpy as np

try:
    import matlab.engine  # type: ignore
    MATLAB_AVAILABLE = True
except ImportError:
    MATLAB_AVAILABLE = False
    # Note: matlabengine cannot be installed via pip
    # It must be installed from MATLAB installation directory


class MATLABNuclearAnalysis:
    """Interface to MATLAB nuclear physics analysis functions"""
    
    def __init__(self, matlab_path: Optional[str] = None):
        """
        Initialize MATLAB engine
        
        Args:
            matlab_path: Path to MATLAB installation (optional)
        """
        self.engine = None
        self.matlab_available = False
        
        if not MATLAB_AVAILABLE:
            print("MATLAB Engine not installed. Using fallback calculations.")
            return
        
        try:
            # Start MATLAB engine
            if matlab_path:
                self.engine = matlab.engine.start_matlab(matlab_path)
            else:
                self.engine = matlab.engine.start_matlab()
            
            # Add MATLAB analysis directory to path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            matlab_dir = os.path.join(current_dir, 'matlab_nuclear_analysis')
            if os.path.exists(matlab_dir):
                self.engine.addpath(matlab_dir)
            
            self.matlab_available = True
            print("MATLAB engine started successfully.")
            
        except Exception as e:
            print(f"Warning: Could not start MATLAB engine: {e}")
            print("Falling back to Python calculations.")
            self.matlab_available = False
    
    def calculate_binding_energy(self, Z: int, A: int) -> Dict[str, Any]:
        """
        Calculate nuclear binding energy using MATLAB
        
        Args:
            Z: Atomic number
            A: Mass number
            
        Returns:
            Dictionary with binding energy results
        """
        if not self.matlab_available:
            return self._fallback_binding_energy(Z, A)
        
        try:
            # Call MATLAB function
            B, B_per_nucleon, terms = self.engine.binding_energy(
                float(Z), float(A), nargout=3
            )
            
            # Convert MATLAB struct to Python dict
            terms_dict = {
                'volume': float(terms['volume']),
                'surface': float(terms['surface']),
                'coulomb': float(terms['coulomb']),
                'asymmetry': float(terms['asymmetry']),
                'pairing': float(terms['pairing'])
            }
            
            return {
                'binding_energy_MeV': float(B),
                'binding_energy_per_nucleon_MeV': float(B_per_nucleon),
                'terms': terms_dict,
                'atomic_number': Z,
                'mass_number': A,
                'method': 'MATLAB'
            }
            
        except Exception as e:
            print(f"MATLAB binding energy calculation error: {e}")
            return self._fallback_binding_energy(Z, A)
    
    def calculate_critical_mass(self, Z: int, A: int, density: float = 18700.0,
                               geometry: str = 'sphere') -> Dict[str, Any]:
        """
        Calculate critical mass using MATLAB
        
        Args:
            Z: Atomic number
            A: Mass number
            density: Material density (kg/m³)
            geometry: 'sphere', 'cylinder', or 'slab'
            
        Returns:
            Dictionary with critical mass results
        """
        if not self.matlab_available:
            return self._fallback_critical_mass(Z, A, density, geometry)
        
        try:
            # Call MATLAB function
            M_critical, R_critical, k_eff, factors = self.engine.critical_mass(
                float(Z), float(A), float(density), geometry, nargout=4
            )
            
            factors_dict = {
                'eta': float(factors['eta']),
                'epsilon': float(factors['epsilon']),
                'p': float(factors['p']),
                'f': float(factors['f'])
            }
            
            return {
                'critical_mass_kg': float(M_critical),
                'critical_radius_m': float(R_critical),
                'k_eff': float(k_eff),
                'four_factors': factors_dict,
                'geometry': geometry,
                'density_kg_m3': density,
                'method': 'MATLAB'
            }
            
        except Exception as e:
            print(f"MATLAB critical mass calculation error: {e}")
            return self._fallback_critical_mass(Z, A, density, geometry)
    
    def calculate_neutron_flux(self, n: float, v: float, Sigma: float,
                              geometry: str = 'point', dimensions: float = 1.0) -> Dict[str, Any]:
        """
        Calculate neutron flux using MATLAB
        
        Args:
            n: Neutron density (neutrons/m³)
            v: Neutron velocity (m/s)
            Sigma: Macroscopic cross section (m⁻¹)
            geometry: Geometry type
            dimensions: Geometry dimensions (m)
            
        Returns:
            Dictionary with neutron flux results
        """
        if not self.matlab_available:
            return self._fallback_neutron_flux(n, v, Sigma)
        
        try:
            # Call MATLAB function
            phi, reaction_rate, flux_profile = self.engine.neutron_flux(
                float(n), float(v), float(Sigma), geometry, float(dimensions), nargout=3
            )
            
            result = {
                'flux_neutrons_per_m2_s': float(phi),
                'reaction_rate_per_m3_s': float(reaction_rate),
                'method': 'MATLAB'
            }
            
            # Add flux profile if available
            if flux_profile:
                if hasattr(flux_profile, 'r'):
                    result['flux_profile_r'] = np.array(flux_profile['r']).flatten()
                    result['flux_profile_phi'] = np.array(flux_profile['phi']).flatten()
            
            return result
            
        except Exception as e:
            print(f"MATLAB neutron flux calculation error: {e}")
            return self._fallback_neutron_flux(n, v, Sigma)
    
    def calculate_decay_chain(self, N0: List[float], lambda_decay: List[float],
                             t: float) -> Dict[str, Any]:
        """
        Calculate radioactive decay chain using MATLAB
        
        Args:
            N0: Initial number of atoms for each nuclide
            lambda_decay: Decay constants (s⁻¹) for each nuclide
            t: Time (s)
            
        Returns:
            Dictionary with decay chain results
        """
        if not self.matlab_available:
            return self._fallback_decay_chain(N0, lambda_decay, t)
        
        try:
            # Convert to MATLAB arrays
            N0_matlab = matlab.double(N0)
            lambda_matlab = matlab.double(lambda_decay)
            
            # Call MATLAB function
            N, activity, half_lives = self.engine.decay_chain(
                N0_matlab, lambda_matlab, float(t), nargout=3
            )
            
            return {
                'N_atoms': np.array(N).flatten().tolist(),
                'activity_Bq': np.array(activity).flatten().tolist(),
                'half_lives_s': np.array(half_lives).flatten().tolist(),
                'time_s': t,
                'method': 'MATLAB'
            }
            
        except Exception as e:
            print(f"MATLAB decay chain calculation error: {e}")
            return self._fallback_decay_chain(N0, lambda_decay, t)
    
    def calculate_quantum_tunneling(self, m: float, V0: float, E: float,
                                    width: float) -> Dict[str, Any]:
        """
        Calculate quantum tunneling probability using MATLAB
        
        Args:
            m: Particle mass (kg)
            V0: Barrier height (J)
            E: Particle energy (J)
            width: Barrier width (m)
            
        Returns:
            Dictionary with tunneling results
        """
        if not self.matlab_available:
            return self._fallback_quantum_tunneling(m, V0, E, width)
        
        try:
            # Call MATLAB function
            T, probability, kappa = self.engine.quantum_tunneling(
                float(m), float(V0), float(E), float(width), nargout=3
            )
            
            return {
                'transmission_coefficient': float(T),
                'tunneling_probability': float(probability),
                'kappa_m_inv': float(kappa),
                'method': 'MATLAB'
            }
            
        except Exception as e:
            print(f"MATLAB quantum tunneling calculation error: {e}")
            return self._fallback_quantum_tunneling(m, V0, E, width)
    
    # Fallback methods (Python implementations)
    def _fallback_binding_energy(self, Z: int, A: int) -> Dict[str, Any]:
        """Fallback Python implementation"""
        a_v, a_s, a_c, a_a = 15.8, 18.3, 0.714, 23.2
        
        volume = a_v * A
        surface = -a_s * A**(2/3)
        coulomb = -a_c * Z**2 / A**(1/3)
        asymmetry = -a_a * (A - 2*Z)**2 / A
        
        if A % 2 == 0 and Z % 2 == 0:
            pairing = 12 / np.sqrt(A)
        elif A % 2 == 1:
            pairing = 0
        else:
            pairing = -12 / np.sqrt(A)
        
        B = volume + surface + coulomb + asymmetry + pairing
        
        return {
            'binding_energy_MeV': B,
            'binding_energy_per_nucleon_MeV': B / A,
            'terms': {
                'volume': volume,
                'surface': surface,
                'coulomb': coulomb,
                'asymmetry': asymmetry,
                'pairing': pairing
            },
            'method': 'Python_fallback'
        }
    
    def _fallback_critical_mass(self, Z: int, A: int, density: float,
                                geometry: str) -> Dict[str, Any]:
        """Fallback Python implementation"""
        return {'critical_mass_kg': None, 'method': 'Python_fallback'}
    
    def _fallback_neutron_flux(self, n: float, v: float, Sigma: float) -> Dict[str, Any]:
        """Fallback Python implementation"""
        phi = n * v
        return {
            'flux_neutrons_per_m2_s': phi,
            'reaction_rate_per_m3_s': phi * Sigma,
            'method': 'Python_fallback'
        }
    
    def _fallback_decay_chain(self, N0: List[float], lambda_decay: List[float],
                              t: float) -> Dict[str, Any]:
        """Fallback Python implementation"""
        N = [n0 * np.exp(-lam * t) for n0, lam in zip(N0, lambda_decay)]
        activity = [lam * n for lam, n in zip(lambda_decay, N)]
        half_lives = [np.log(2) / lam for lam in lambda_decay]
        
        return {
            'N_atoms': N,
            'activity_Bq': activity,
            'half_lives_s': half_lives,
            'method': 'Python_fallback'
        }
    
    def _fallback_quantum_tunneling(self, m: float, V0: float, E: float,
                                    width: float) -> Dict[str, Any]:
        """Fallback Python implementation"""
        hbar = 1.0545718e-34
        kappa = np.sqrt(2 * m * (V0 - E)) / hbar
        T = np.exp(-2 * kappa * width)
        
        return {
            'transmission_coefficient': T,
            'tunneling_probability': T,
            'kappa_m_inv': kappa,
            'method': 'Python_fallback'
        }
    
    def close(self):
        """Close MATLAB engine"""
        if self.engine:
            self.engine.quit()
            self.engine = None
            self.matlab_available = False


def main():
    """Test MATLAB interface"""
    print("Testing MATLAB Nuclear Physics Analysis Interface")
    print("=" * 60)
    
    matlab_analysis = MATLABNuclearAnalysis()
    
    if matlab_analysis.matlab_available:
        print("\nMATLAB is available. Testing calculations...\n")
        
        # Test binding energy
        print("1. Testing binding energy calculation (U-235):")
        result = matlab_analysis.calculate_binding_energy(92, 235)
        print(f"   Binding energy: {result['binding_energy_MeV']:.2f} MeV")
        print(f"   Per nucleon: {result['binding_energy_per_nucleon_MeV']:.2f} MeV/nucleon")
        print(f"   Method: {result['method']}\n")
        
        # Test critical mass
        print("2. Testing critical mass calculation (U-235 sphere):")
        result = matlab_analysis.calculate_critical_mass(92, 235, 18700, 'sphere')
        if result.get('critical_mass_kg'):
            print(f"   Critical mass: {result['critical_mass_kg']:.2f} kg")
            print(f"   Critical radius: {result['critical_radius_m']*100:.2f} cm")
            print(f"   k_eff: {result['k_eff']:.3f}")
        print(f"   Method: {result['method']}\n")
        
    else:
        print("\nMATLAB not available. Using fallback calculations.\n")
        print("To use MATLAB:")
        print("1. Install MATLAB")
        print("2. Install MATLAB Engine for Python:")
        print("   cd matlabroot/extern/engines/python")
        print("   python setup.py install")
        print("3. Or install via pip: pip install matlabengine")
    
    matlab_analysis.close()
    print("=" * 60)


if __name__ == "__main__":
    main()


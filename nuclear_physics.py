import numpy as np
from typing import Dict, List, Tuple, Optional
import requests
import json
import math
import os

# Try to import advanced calculations (requires scipy)
try:
    from advanced_calculations import AdvancedCalculations
    ADVANCED_CALCULATIONS_AVAILABLE = True
except ImportError:
    ADVANCED_CALCULATIONS_AVAILABLE = False
    AdvancedCalculations = None

# Try to import PyNE (Nuclear Engineering Toolkit)
# Note: pip version of pyne may be limited, full PyNE requires compilation
try:
    import pyne
    PYNE_AVAILABLE = True
    # Try to import specific modules (may not be available in pip version)
    try:
        from pyne import nucname, data, material
        PYNE_FULL_AVAILABLE = True
    except ImportError:
        PYNE_FULL_AVAILABLE = False
        nucname = None
        data = None
        material = None
except ImportError:
    PYNE_AVAILABLE = False
    PYNE_FULL_AVAILABLE = False
    pyne = None
    nucname = None
    data = None
    material = None

# Try to import NPAT (Nuclear Physics Analysis Tools)
try:
    import npat
    from npat import DecayChain, Isotope, Element
    NPAT_AVAILABLE = True
except ImportError:
    NPAT_AVAILABLE = False
    npat = None
    DecayChain = None
    Isotope = None
    Element = None

class NuclearPhysics:
    def __init__(self):
        # Constants
        self.c = 299792458  # Speed of light (m/s)
        self.m_p = 1.007276466621  # Proton mass (u)
        self.m_n = 1.00866491588   # Neutron mass (u)
        self.m_e = 0.000548579909  # Electron mass (u)
        self.u_to_MeV = 931.49410242  # Conversion factor from u to MeV
        
        # Elementary charge
        self.e = 1.602176634e-19  # Elementary charge (C)
        
        # Nuclear binding energy equation coefficients
        self.a_v = 15.8  # Volume term
        self.a_s = 18.3  # Surface term
        self.a_c = 0.714  # Coulomb term
        self.a_a = 23.2  # Asymmetry term
        self.a_p = 12.0  # Pairing term
        
        # KAERI API endpoint (placeholder - replace with actual endpoint)
        self.kaeri_api_url = "https://www.kaeri.re.kr/api/nuclear-data"
        
        # JANIS API endpoint (Java-based Nuclear Data Information System)
        # JANIS typically runs locally or on institutional servers
        self.janis_api_url = "http://localhost:8080/janis/api"  # Default local JANIS
        self.janis_available = False  # Set to True if JANIS is accessible
        
        # IAEA NUCLEUS / Nuclear Data Services API (公开访问)
        # NUCLEUS成员通过NDS访问数据，使用公开API端点
        self.iaea_nds_url = "https://nds.iaea.org/relnsd/v1/data"  # NUCLEUS访问的NDS端点
        self.iaea_livechart_url = "https://www-nds.iaea.org/relnsd/v0/data"
        self.iaea_available = False
        self.data_source_name = "IAEA NUCLEUS/NDS"  # 标识数据源
        
        # Load cross section data
        self.cross_section_data = self._load_cross_section_data()
        
        # Initialize advanced calculations if available
        if ADVANCED_CALCULATIONS_AVAILABLE:
            self.advanced_calc = AdvancedCalculations()
        else:
            self.advanced_calc = None
        
        # Store library availability flags
        self.pyne_available = PYNE_AVAILABLE
        self.pyne_full_available = PYNE_FULL_AVAILABLE if PYNE_AVAILABLE else False
        self.npat_available = NPAT_AVAILABLE
        
    def calculate_nuclear_radius(self, A: int) -> float:
        """
        Calculate nuclear radius using R = r₀ * A^(1/3)
        A: mass number
        Returns: nuclear radius in meters
        """
        r_0 = 1.2e-15  # Nuclear radius parameter (m)
        return r_0 * (A ** (1/3))
    
    def _load_cross_section_data(self) -> Dict:
        """
        Load cross section data from JSON file
        Returns: dictionary containing cross section data
        """
        try:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, "nuclear_physics_sim", "data", "cross_sections.json")
            
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"nuclides": {}, "description": "Cross section data not found"}
        except Exception as e:
            return {"nuclides": {}, "error": str(e)}
    
    def get_cross_section_data(self, Z: int, A: int, neutron_energy: str = "thermal_neutron") -> Optional[Dict]:
        """
        Get cross section data for a specific nuclide
        Z: atomic number
        A: mass number
        neutron_energy: "thermal_neutron" or "fast_neutron"
        Returns: cross section data dictionary or None if not found
        """
        if "nuclides" not in self.cross_section_data:
            return None
        
        # Try to find nuclide by Z and A
        for nuclide_key, nuclide_data in self.cross_section_data["nuclides"].items():
            if nuclide_data.get("atomic_number") == Z and nuclide_data.get("mass_number") == A:
                result = nuclide_data.copy()
                if neutron_energy in nuclide_data:
                    result["requested_energy"] = neutron_energy
                    result["cross_sections"] = nuclide_data[neutron_energy]
                return result
        
        return None
    
    def find_nuclide_by_name(self, name: str) -> Optional[Dict]:
        """
        Find nuclide data by name (e.g., "U-235", "U235", "Uranium-235")
        Returns: nuclide data dictionary or None if not found
        """
        if "nuclides" not in self.cross_section_data:
            return None
        
        # Normalize name (remove spaces, handle different formats)
        name_normalized = name.replace(" ", "").replace("-", "").upper()
        
        for nuclide_key, nuclide_data in self.cross_section_data["nuclides"].items():
            key_normalized = nuclide_key.replace("-", "")
            nuclide_name = nuclide_data.get("name", "").replace(" ", "").replace("-", "").upper()
            
            if (name_normalized == key_normalized or 
                name_normalized in nuclide_name or 
                nuclide_name in name_normalized):
                return nuclide_data
        
        return None
    
    def list_available_nuclides(self) -> List[str]:
        """
        Get list of all available nuclides in the cross section database
        Returns: list of nuclide identifiers (e.g., ["H-1", "U-235", ...])
        """
        if "nuclides" not in self.cross_section_data:
            return []
        return list(self.cross_section_data["nuclides"].keys())
        
    def calculate_binding_energy(self, Z: int, A: int) -> float:
        """
        Calculate nuclear binding energy using the semi-empirical mass formula
        Z: atomic number (protons)
        A: mass number (protons + neutrons)
        Returns: binding energy in MeV
        """
        N = A - Z  # Number of neutrons
        
        # Volume term
        volume_term = self.a_v * A
        
        # Surface term
        surface_term = -self.a_s * (A ** (2/3))
        
        # Coulomb term
        coulomb_term = -self.a_c * (Z * (Z-1)) / (A ** (1/3))
        
        # Asymmetry term
        asymmetry_term = -self.a_a * ((A - 2*Z)**2) / A
        
        # Pairing term
        pairing_term = 0
        if Z % 2 == 0 and N % 2 == 0:  # Even-even
            pairing_term = self.a_p / (A ** (1/2))
        elif Z % 2 == 1 and N % 2 == 1:  # Odd-odd
            pairing_term = -self.a_p / (A ** (1/2))
        
        # Total binding energy
        binding_energy = volume_term + surface_term + coulomb_term + asymmetry_term + pairing_term
        
        return binding_energy
    
    def calculate_mass_defect(self, Z: int, A: int) -> float:
        """
        Calculate mass defect using binding energy
        Returns: mass defect in atomic mass units (u)
        """
        binding_energy = self.calculate_binding_energy(Z, A)
        return binding_energy / self.u_to_MeV
    
    def get_kaeri_data(self, isotope: str) -> Dict:
        """
        Fetch nuclear data from KAERI database
        isotope: string in format "A-Z" (e.g., "235-U")
        Returns: dictionary containing nuclear data
        """
        try:
            # This is a placeholder for actual API integration
            # Replace with actual KAERI API endpoint and authentication
            response = requests.get(f"{self.kaeri_api_url}/{isotope}", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Failed to fetch KAERI data", "status": response.status_code}
        except requests.exceptions.RequestException:
            return {"error": "KAERI database not accessible", "note": "Using local cross section data instead"}
        except Exception as e:
            return {"error": f"Error accessing KAERI data: {str(e)}"}
    
    def get_janis_data(self, Z: int, A: int, data_type: str = "cross_section") -> Dict:
        """
        Fetch nuclear data from JANIS database
        Z: atomic number
        A: mass number
        data_type: "cross_section", "decay", "structure", etc.
        Returns: dictionary containing JANIS nuclear data
        """
        try:
            # JANIS API integration
            # JANIS typically requires local installation or institutional access
            if not self.janis_available:
                # Try to connect to local JANIS
                try:
                    test_response = requests.get(f"{self.janis_api_url}/health", timeout=2)
                    self.janis_available = test_response.status_code == 200
                except:
                    self.janis_available = False
            
            if not self.janis_available:
                return {
                    "error": "JANIS not accessible",
                    "note": "JANIS (Java-based Nuclear Data Information System) is not currently accessible.",
                    "suggestion": "JANIS typically requires local installation or institutional network access.",
                    "alternative": "Using local cross section database instead."
                }
            
            # Query JANIS API
            nuclide_id = f"{A}-{Z}"
            response = requests.get(
                f"{self.janis_api_url}/nuclide/{nuclide_id}/{data_type}",
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "source": "JANIS",
                    "nuclide": f"{A}-{Z}",
                    "data_type": data_type,
                    "data": response.json()
                }
            else:
                return {
                    "error": f"JANIS query failed",
                    "status": response.status_code,
                    "note": "JANIS may require specific query format or authentication"
                }
        except requests.exceptions.RequestException as e:
            return {
                "error": "JANIS connection error",
                "details": str(e),
                "note": "Ensure JANIS is running and accessible"
            }
        except Exception as e:
            return {"error": f"Error accessing JANIS: {str(e)}"}
    
    def get_iaea_nuclide_data(self, Z: int, A: int, data_type: str = "all") -> Dict:
        """
        Fetch nuclide data from IAEA NUCLEUS/NDS (公开API)
        NUCLEUS成员通过此端点访问权威核素数据
        
        Parameters:
        - Z: atomic number
        - A: mass number
        - data_type: "all", "levels", "decay", "structure", "masses"
          Note: "levels" typically returns full data, while others may return record counts
        
        Returns: IAEA NUCLEUS nuclear data
        """
        try:
            # Element symbol mapping
            element_symbols = {
                1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O',
                9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P',
                16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti',
                23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu',
                30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr',
                37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc',
                44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn',
                51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 57: 'La',
                58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd',
                65: 'Tb', 66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu',
                72: 'Hf', 73: 'Ta', 74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt',
                79: 'Au', 80: 'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At',
                86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th', 91: 'Pa', 92: 'U',
                93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk', 98: 'Cf', 99: 'Es',
                100: 'Fm', 101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db',
                106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg',
                112: 'Cn', 113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts', 118: 'Og'
            }
            
            element = element_symbols.get(Z, f"Z{Z}")
            nuclide_id = f"{A}{element}".lower()
            
            # Build API request
            if data_type == "all":
                fields = "levels,decay,structure,masses"
            else:
                fields = data_type
            
            url = f"{self.iaea_nds_url}?fields={fields}&nuclides={nuclide_id}"
            
            # Try to connect
            try:
                test_response = requests.get(f"{self.iaea_nds_url}?fields=masses&nuclides=1h", timeout=5)
                self.iaea_available = test_response.status_code == 200
            except:
                self.iaea_available = False
            
            if not self.iaea_available:
                return {
                    "error": "IAEA NUCLEUS/NDS not accessible",
                    "note": "IAEA NUCLEUS/NDS may require network access. As a NUCLEUS member, you have access to this data.",
                    "alternative": "Using local cross section database instead."
                }
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Parse response - NUCLEUS/NDS通常返回CSV格式
                content_type = response.headers.get('content-type', '').lower()
                raw_data = response.text
                
                # 解析CSV数据（如果返回CSV格式）
                parsed_data = None
                if 'csv' in content_type:
                    # CSV格式，尝试解析
                    lines = [line.strip() for line in raw_data.strip().split('\n') if line.strip()]
                    
                    if len(lines) > 1:
                        # 有数据行，尝试解析为CSV
                        headers = lines[0].split(',') if lines[0] else []
                        data_rows = [line.split(',') for line in lines[1:] if line.strip()]
                        parsed_data = {
                            "format": "CSV",
                            "headers": headers,
                            "rows": data_rows,
                            "row_count": len(data_rows)
                        }
                    elif len(lines) == 1:
                        # 只有一行数据，可能是记录数或其他信息
                        single_value = lines[0]
                        parsed_data = {
                            "format": "CSV",
                            "single_value": single_value,
                            "note": "Response contains single value (possibly record count or identifier)"
                        }
                elif raw_data.strip().startswith(('nuclide', 'mass', 'energy', 'decay', 'Nuclide', 'Mass', 'Energy')):
                    # 可能是CSV但没有正确的content-type
                    lines = [line.strip() for line in raw_data.strip().split('\n') if line.strip()]
                    if len(lines) > 1:
                        headers = lines[0].split(',') if lines[0] else []
                        data_rows = [line.split(',') for line in lines[1:] if line.strip()]
                        parsed_data = {
                            "format": "CSV",
                            "headers": headers,
                            "rows": data_rows,
                            "row_count": len(data_rows)
                        }
                
                # 构建返回数据
                result = {
                    "source": self.data_source_name,
                    "nuclide": f"{A}-{Z}",
                    "nuclide_id": nuclide_id,
                    "data_type": data_type,
                    "raw_data": raw_data,
                    "parsed_data": parsed_data,
                    "content_type": content_type,
                    "status": "success",
                    "url": url
                }
                
                # 如果解析成功，也提供解析后的数据
                if parsed_data:
                    result["data"] = parsed_data
                else:
                    result["data"] = raw_data
                
                return result
            else:
                return {
                    "error": f"IAEA API returned status {response.status_code}",
                    "nuclide": f"{A}-{Z}",
                    "nuclide_id": nuclide_id,
                    "suggestion": "Check nuclide identifier format or try different data_type"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "error": "IAEA NUCLEUS/NDS connection error",
                "details": str(e),
                "note": "As a NUCLEUS member, you should have access. Check network connection or try again later."
            }
        except Exception as e:
            return {"error": f"Error accessing IAEA NUCLEUS/NDS data: {str(e)}"}
    
    def get_iaea_livechart_data(self, Z: int, A: int) -> Dict:
        """
        Get data from IAEA Livechart (interactive nuclide chart)
        """
        try:
            element_symbols = {
                1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O',
                11: 'Na', 13: 'Al', 26: 'Fe', 29: 'Cu', 48: 'Cd', 54: 'Xe',
                64: 'Gd', 82: 'Pb', 90: 'Th', 92: 'U', 94: 'Pu'
            }
            
            element = element_symbols.get(Z, f"Z{Z}")
            nuclide_id = f"{A}{element}".lower()
            
            # Livechart API endpoint
            url = f"{self.iaea_livechart_url}?nuclide={nuclide_id}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    data = response.json()
                else:
                    data = response.text
                    
                return {
                    "source": "IAEA NUCLEUS/Livechart",
                    "nuclide": f"{A}-{Z}",
                    "nuclide_id": nuclide_id,
                    "data": data,
                    "status": "success",
                    "url": url
                }
            else:
                return {"error": f"Livechart API error: {response.status_code}"}
            
        except Exception as e:
            return {"error": f"Error accessing IAEA Livechart: {str(e)}"}
    
    def calculate_fission_energy(self, Z: int, A: int) -> float:
        """
        Calculate approximate energy released in fission
        Returns: energy in MeV
        """
        # Simplified calculation based on binding energy difference
        # This is a rough approximation
        binding_energy_before = self.calculate_binding_energy(Z, A)
        binding_energy_after = 2 * self.calculate_binding_energy(Z//2, A//2)
        return binding_energy_after - binding_energy_before
    
    def get_nuclear_properties(self, Z: int, A: int) -> Dict:
        """
        Get comprehensive nuclear properties for an isotope
        Returns: dictionary of nuclear properties
        """
        binding_energy = self.calculate_binding_energy(Z, A)
        mass_defect = self.calculate_mass_defect(Z, A)
        fission_energy = self.calculate_fission_energy(Z, A)
        
        properties = {
            "atomic_number": Z,
            "mass_number": A,
            "binding_energy_MeV": binding_energy,
            "mass_defect_u": mass_defect,
            "fission_energy_MeV": fission_energy,
            "neutron_number": A - Z,
            "proton_number": Z
        }
        
        # Add cross section data if available
        cross_section = self.get_cross_section_data(Z, A)
        if cross_section:
            properties["cross_section_data"] = cross_section
        
        return properties
    
    def calculate_shell_model_energy(self, Z: int, A: int) -> Dict:
        """
        Calculate shell model energy levels and magic numbers
        Returns: shell model parameters and magic number analysis
        """
        # Magic numbers for protons and neutrons
        magic_protons = [2, 8, 20, 28, 50, 82, 126]
        magic_neutrons = [2, 8, 20, 28, 50, 82, 126, 184]
        
        N = A - Z
        is_proton_magic = Z in magic_protons
        is_neutron_magic = N in magic_neutrons
        
        # Shell model energy levels (simplified)
        # Using harmonic oscillator model
        n_max = int((A/4)**(1/3))  # Approximate principal quantum number
        
        return {
            "proton_magic": is_proton_magic,
            "neutron_magic": is_neutron_magic,
            "doubly_magic": is_proton_magic and is_neutron_magic,
            "shell_stability_factor": 1.0 if (is_proton_magic or is_neutron_magic) else 0.5,
            "principal_quantum_number": n_max,
            "magic_protons": magic_protons,
            "magic_neutrons": magic_neutrons
        }
    
    def calculate_alpha_decay_probability(self, Z: int, A: int, E_alpha: float) -> Dict:
        """
        Calculate alpha decay probability using quantum tunneling
        E_alpha: alpha particle energy in MeV
        Returns: tunneling probability and half-life
        """
        # Gamow factor for alpha decay
        Z_alpha = 2  # Alpha particle charge
        Z_daughter = Z - Z_alpha
        
        # Coulomb barrier height
        R = self.calculate_nuclear_radius(A)
        V_coulomb = 2 * Z_alpha * Z_daughter * self.e**2 / (4 * math.pi * 8.854e-12 * R)
        V_coulomb_MeV = V_coulomb / (self.e * 1e6)
        
        # Gamow factor
        alpha = 7.2973525693e-3  # Fine structure constant
        eta = 2 * alpha * Z_alpha * Z_daughter * math.sqrt(931.494 / E_alpha)
        gamow_factor = math.exp(-2 * math.pi * eta)
        
        # Tunneling probability
        if E_alpha < V_coulomb_MeV:
            tunneling_prob = gamow_factor
        else:
            tunneling_prob = 1.0
        
        # Half-life estimation (simplified)
        frequency_factor = 1e21  # s^-1 (typical nuclear frequency)
        half_life = math.log(2) / (frequency_factor * tunneling_prob)
        
        return {
            "alpha_energy_MeV": E_alpha,
            "coulomb_barrier_MeV": V_coulomb_MeV,
            "gamow_factor": gamow_factor,
            "tunneling_probability": tunneling_prob,
            "half_life_seconds": half_life,
            "half_life_years": half_life / (365.25 * 24 * 3600)
        }
    
    def calculate_cno_cycle_energy(self) -> Dict:
        """
        Calculate CNO cycle energy production
        Returns: CNO cycle parameters and energy release
        """
        # CNO cycle reactions
        reactions = [
            {"reaction": "¹²C + p → ¹³N + γ", "Q_MeV": 1.94},
            {"reaction": "¹³N → ¹³C + e⁺ + νₑ", "Q_MeV": 2.22},
            {"reaction": "¹³C + p → ¹⁴N + γ", "Q_MeV": 7.55},
            {"reaction": "¹⁴N + p → ¹⁵O + γ", "Q_MeV": 7.30},
            {"reaction": "¹⁵O → ¹⁵N + e⁺ + νₑ", "Q_MeV": 2.76},
            {"reaction": "¹⁵N + p → ¹²C + ⁴He", "Q_MeV": 4.96}
        ]
        
        total_energy = sum(r["Q_MeV"] for r in reactions)
        
        return {
            "total_energy_release_MeV": total_energy,
            "reactions": reactions,
            "net_reaction": "4p → ⁴He + 2e⁺ + 2νₑ",
            "efficiency": 0.7  # Typical stellar efficiency
        }
    
    def calculate_triple_alpha_process(self) -> Dict:
        """
        Calculate triple-alpha process for stellar nucleosynthesis
        Returns: triple-alpha process parameters
        """
        # Triple-alpha process
        reactions = [
            {"reaction": "⁴He + ⁴He → ⁸Be", "Q_MeV": -0.092},
            {"reaction": "⁸Be + ⁴He → ¹²C", "Q_MeV": 7.367}
        ]
        
        net_energy = sum(r["Q_MeV"] for r in reactions)
        
        return {
            "net_energy_release_MeV": net_energy,
            "reactions": reactions,
            "net_reaction": "3⁴He → ¹²C",
            "temperature_threshold_K": 1e8,  # Required stellar temperature
            "density_threshold_kg_m3": 1e5   # Required stellar density
        }
    
    def calculate_nuclear_isomer_properties(self, Z: int, A: int, E_excitation: float) -> Dict:
        """
        Calculate nuclear isomer properties and metastable states
        E_excitation: excitation energy in MeV
        Returns: isomer properties and decay characteristics
        """
        # Isomer half-life estimation (simplified)
        # Based on Weisskopf estimates for gamma decay
        
        if E_excitation < 0.1:  # Low-lying states
            half_life = 1e-12  # picoseconds
        elif E_excitation < 1.0:  # Medium energy
            half_life = 1e-9   # nanoseconds
        else:  # High energy
            half_life = 1e-6   # microseconds
        
        # Spin and parity considerations
        spin_factor = 1.0
        if A % 2 == 0:  # Even-A nucleus
            spin_factor = 0.1  # Slower decay for even-A
        
        # Final half-life
        final_half_life = half_life * spin_factor
        
        return {
            "excitation_energy_MeV": E_excitation,
            "isomer_half_life_seconds": final_half_life,
            "isomer_half_life_hours": final_half_life / 3600,
            "spin_parity_factor": spin_factor,
            "isomer_type": "metastable" if final_half_life > 1e-6 else "short-lived"
        }
    
    def calculate_muon_catalyzed_fusion(self) -> Dict:
        """
        Calculate muon-catalyzed fusion parameters
        Returns: muon fusion characteristics
        """
        # Muon properties
        m_muon = 105.6583755e-3  # MeV/c²
        m_electron = 0.510998950  # MeV/c²
        
        # Reduced Bohr radius for muon
        a_0_muon = 5.29177210903e-11  # m (Bohr radius)
        a_0_muon_reduced = a_0_muon * (m_electron / m_muon)
        
        # Fusion rate calculation
        fusion_rate = 1e6  # s⁻¹ (typical muon-catalyzed fusion rate)
        
        return {
            "muon_mass_MeV": m_muon,
            "reduced_bohr_radius_m": a_0_muon_reduced,
            "fusion_rate_s": fusion_rate,
            "catalysis_cycles": 100,  # Average cycles per muon
            "energy_gain_MeV": 17.6,  # D-T fusion energy
            "net_energy_MeV": 17.6 - 5.5  # After muon production cost
        }
    
    def calculate_neutrino_oscillation(self, L: float, E: float) -> Dict:
        """
        Calculate neutrino oscillation parameters
        L: baseline distance in km
        E: neutrino energy in GeV
        Returns: oscillation probabilities
        """
        # Mixing angles (approximate values)
        theta_12 = 33.44  # degrees
        theta_23 = 49.2   # degrees
        theta_13 = 8.57   # degrees
        
        # Mass squared differences (eV²)
        delta_m21_sq = 7.42e-5
        delta_m31_sq = 2.51e-3
        
        # Oscillation probability for electron neutrino
        P_ee = 1 - 0.5 * (math.sin(2*math.radians(theta_13))**2) * \
               (1 - math.cos(1.27 * delta_m31_sq * L / E))
        
        return {
            "baseline_km": L,
            "energy_GeV": E,
            "electron_survival_probability": P_ee,
            "mixing_angles_degrees": {
                "theta_12": theta_12,
                "theta_23": theta_23,
                "theta_13": theta_13
            },
            "mass_squared_differences_eV2": {
                "delta_m21_sq": delta_m21_sq,
                "delta_m31_sq": delta_m31_sq
            }
        }
    
    def calculate_fission_fragmentation(self, Z: int, A: int) -> Dict:
        """
        Calculate fission fragmentation pathways
        Returns: fragmentation analysis and potential energy surface
        """
        # Fission fragment mass distribution (simplified)
        # Based on liquid drop model
        
        A1_most_probable = A * 0.4  # Light fragment
        A2_most_probable = A * 0.6  # Heavy fragment
        
        # Potential energy surface analysis
        deformation_energy = 0.1 * A**(2/3)  # MeV
        coulomb_energy = 0.6 * Z**2 / A**(1/3)  # MeV
        
        # Fission barrier
        fission_barrier = deformation_energy + coulomb_energy
        
        return {
            "parent_nucleus": f"{A}-{Z}",
            "light_fragment_A": A1_most_probable,
            "heavy_fragment_A": A2_most_probable,
            "deformation_energy_MeV": deformation_energy,
            "coulomb_energy_MeV": coulomb_energy,
            "fission_barrier_MeV": fission_barrier,
            "fragmentation_asymmetry": abs(A1_most_probable - A2_most_probable) / A
        }
    
    def calculate_critical_mass(self, Z: int, A: int, density_kg_m3: Optional[float] = None, 
                                geometry: str = "sphere", reflector: bool = False) -> Dict:
        """
        Calculate critical mass and critical radius using E=mc² and neutron diffusion theory
        Based on academic nuclear physics principles for research purposes
        
        Z: atomic number
        A: mass number
        density_kg_m3: material density (if None, uses default values from database)
        geometry: "sphere", "cylinder", or "slab"
        reflector: whether neutron reflector is present
        
        Returns: critical mass analysis including E=mc² energy calculations
        """
        # Get cross section data
        cross_section = self.get_cross_section_data(Z, A, "thermal_neutron")
        
        if not cross_section:
            return {
                "error": "Cross section data not available for critical mass calculation",
                "suggestion": "Critical mass calculations require neutron cross section data"
            }
        
        # Get fission cross section (required for critical mass)
        thermal_xs = cross_section.get("thermal_neutron", {})
        fission_xs = thermal_xs.get("fission", 0)
        
        if fission_xs == 0:
            return {
                "error": "Non-fissile material",
                "note": f"This nuclide does not undergo thermal neutron fission",
                "fission_cross_section": 0
            }
        
        # Default densities (kg/m³) for common fissile materials
        default_densities = {
            (92, 235): 19050,   # U-235 (depleted U density, pure would be higher)
            (92, 238): 19050,   # U-238
            (94, 239): 19840,   # Pu-239
            (90, 232): 11720,   # Th-232
        }
        
        # Use provided density or default
        if density_kg_m3 is None:
            density_kg_m3 = default_densities.get((Z, A), 10000)  # Default fallback
        
        # Neutron data from cross sections
        absorption_xs = thermal_xs.get("absorption", 0)  # barns
        scattering_xs = thermal_xs.get("scattering", 0)  # barns
        capture_xs = thermal_xs.get("capture", absorption_xs - fission_xs)  # barns
        
        # Convert barns to m² (1 barn = 10⁻²⁸ m²)
        sigma_f = fission_xs * 1e-28  # m²
        sigma_a = absorption_xs * 1e-28  # m²
        sigma_s = scattering_xs * 1e-28  # m²
        sigma_t = sigma_a + sigma_s  # total
        
        # Calculate number density (atoms per m³)
        # Using Avogadro's number and atomic mass
        avogadro = 6.02214076e23  # atoms/mol
        atomic_mass_kg = A * 1.66053906660e-27  # kg per atom
        number_density = density_kg_m3 / atomic_mass_kg  # atoms/m³
        
        # Macroscopic cross sections (m⁻¹)
        Sigma_f = number_density * sigma_f  # fission
        Sigma_a = number_density * sigma_a  # absorption
        Sigma_s = number_density * sigma_s  # scattering
        Sigma_t = number_density * sigma_t  # total
        
        # Neutron reproduction factor (η)
        # Average neutrons released per fission
        neutrons_per_fission = self._estimate_neutrons_per_fission(Z, A)
        
        # η = ν * (σ_f / σ_a) where ν is neutrons per fission
        eta = neutrons_per_fission * (sigma_f / sigma_a) if sigma_a > 0 else 0
        
        # Fast fission factor (ε) - typically 1.0-1.3 for thermal reactors
        # For pure fissile material, ε ≈ 1.0 (no fast fission in thermal systems)
        epsilon = 1.0
        
        # Resonance escape probability (p) - simplified calculation
        # For pure fissile material without moderator, p ≈ 1.0
        # More accurately: p = exp(-N_238 * I_res / (N_238 * I_res + ξ * Σ_s))
        # For pure fissile material: p ≈ 1.0
        p = 1.0  # Simplified for pure fissile material
        
        # Thermal utilization (f) - fraction of thermal neutrons absorbed in fuel
        f = 1.0  # For pure fissile material
        
        # Effective multiplication factor (k_eff = k_infinity for infinite medium)
        # For finite geometry, k_eff = k_infinity / (1 + M² * B²)
        # Here we calculate k_infinity first, then adjust for buckling
        k_infinity = eta * epsilon * p * f
        k_eff = k_infinity  # We'll calculate actual k_eff after determining buckling
        
        # For criticality, we need k_eff = 1
        # Buckling (B²) from neutron diffusion equation
        # B² = (k_inf - 1) / M², where M² is migration area
        
        # Migration area (M²) - simplified
        # M² ≈ L² + τ, where L is diffusion length, τ is Fermi age
        diffusion_length = 1.0 / math.sqrt(3 * Sigma_s * Sigma_a) if (Sigma_s * Sigma_a) > 0 else 0.1
        fermi_age = diffusion_length * 0.5  # Simplified
        migration_area = diffusion_length**2 + fermi_age
        
        # Calculate critical buckling
        # For criticality: k_eff = k_infinity / (1 + M² * B²) = 1
        # Therefore: B² = (k_infinity - 1) / M²
        if k_infinity > 1.0 and migration_area > 0:
            # Material is supercritical at infinite size
            # Critical buckling: B² = (k_inf - 1) / M²
            critical_buckling = (k_infinity - 1.0) / migration_area
            # Actual k_eff at criticality = 1.0
            k_eff = 1.0
        elif k_infinity <= 1.0:
            # Material cannot achieve criticality (subcritical)
            # Use a minimal buckling for calculation
            critical_buckling = abs(k_infinity - 1.0) / migration_area if migration_area > 0 else 0.01
            k_eff = k_infinity
        else:
            critical_buckling = 0.01  # Default fallback
            k_eff = k_infinity
        
        # Geometric buckling for different shapes
        if geometry == "sphere":
            # For sphere: B² = (π/R)²
            critical_radius = math.pi / math.sqrt(critical_buckling) if critical_buckling > 0 else 0.1
        elif geometry == "cylinder":
            # For cylinder: B² = (2.405/R)² + (π/H)² (assuming R ≈ H for minimum mass)
            # Simplified: use R = H
            critical_radius = 2.405 / math.sqrt(critical_buckling) if critical_buckling > 0 else 0.1
        else:  # slab
            # For slab: B² = (π/a)² where a is half-thickness
            critical_radius = math.pi / math.sqrt(critical_buckling) if critical_buckling > 0 else 0.1
        
        # Apply reflector effect (reduces critical mass)
        reflector_reduction = 0.7 if reflector else 1.0
        critical_radius *= reflector_reduction
        
        # Calculate critical volume and mass
        if geometry == "sphere":
            critical_volume = (4/3) * math.pi * critical_radius**3
        elif geometry == "cylinder":
            height = 2 * critical_radius  # Assuming R = H for minimum
            critical_volume = math.pi * critical_radius**2 * height
        else:  # slab
            thickness = 2 * critical_radius
            area = 1.0  # Arbitrary unit area
            critical_volume = area * thickness
        
        critical_mass_kg = density_kg_m3 * critical_volume
        
        # Calculate energy using E=mc²
        # First, calculate mass defect from binding energy
        binding_energy = self.calculate_binding_energy(Z, A)
        mass_defect = binding_energy / self.u_to_MeV  # in atomic mass units
        
        # Energy per atom from mass defect
        energy_per_atom_MeV = binding_energy
        
        # Number of atoms in critical mass
        atoms_in_critical_mass = critical_mass_kg / atomic_mass_kg
        
        # Total binding energy in critical mass (E=mc²)
        total_binding_energy_MeV = energy_per_atom_MeV * atoms_in_critical_mass
        total_binding_energy_J = total_binding_energy_MeV * 1.602176634e-13  # J
        
        # Fission energy release (if all atoms fission)
        # Average energy per fission: ~200 MeV
        energy_per_fission_MeV = 200.0
        total_fission_energy_MeV = energy_per_fission_MeV * atoms_in_critical_mass
        total_fission_energy_J = total_fission_energy_MeV * 1.602176634e-13  # J
        total_fission_energy_kt_TNT = total_fission_energy_J / 4.184e12  # kilotons TNT
        
        # E=mc² calculation for complete conversion
        c_m_s = self.c  # m/s
        total_rest_energy_J = critical_mass_kg * c_m_s**2  # E = mc²
        total_rest_energy_MeV = total_rest_energy_J / 1.602176634e-13
        
        return {
            "nuclide": cross_section.get("name", f"Z={Z}, A={A}"),
            "atomic_number": Z,
            "mass_number": A,
            "geometry": geometry,
            "reflector": reflector,
            "density_kg_m3": density_kg_m3,
            "critical_parameters": {
                "critical_mass_kg": critical_mass_kg,
                "critical_mass_g": critical_mass_kg * 1000,
                "critical_radius_m": critical_radius,
                "critical_radius_cm": critical_radius * 100,
                "critical_volume_m3": critical_volume,
                "critical_volume_cm3": critical_volume * 1e6
            },
            "neutron_physics": {
                "neutrons_per_fission": neutrons_per_fission,
                "fission_cross_section_barn": fission_xs,
                "absorption_cross_section_barn": absorption_xs,
                "scattering_cross_section_barn": scattering_xs,
                "eta": eta,
                "k_effective": k_eff,
                "migration_area_m2": migration_area,
                "diffusion_length_m": diffusion_length
            },
            "energy_calculations": {
                "binding_energy_per_atom_MeV": energy_per_atom_MeV,
                "total_binding_energy_MeV": total_binding_energy_MeV,
                "total_binding_energy_J": total_binding_energy_J,
                "energy_per_fission_MeV": energy_per_fission_MeV,
                "total_fission_energy_MeV": total_fission_energy_MeV,
                "total_fission_energy_J": total_fission_energy_J,
                "total_fission_energy_kt_TNT": total_fission_energy_kt_TNT,
                "e_mc2_rest_energy_J": total_rest_energy_J,
                "e_mc2_rest_energy_MeV": total_rest_energy_MeV,
                "mass_defect_per_atom_u": mass_defect
            },
            "academic_note": "These calculations are based on neutron diffusion theory and E=mc² for academic research purposes."
        }
    
    def _estimate_neutrons_per_fission(self, Z: int, A: int) -> float:
        """
        Estimate average number of neutrons released per fission
        Based on empirical data for fissile materials
        """
        # Known values for common fissile materials
        neutron_yield = {
            (92, 235): 2.43,  # U-235 thermal neutrons
            (92, 238): 2.6,   # U-238 fast neutrons
            (94, 239): 2.87,  # Pu-239 thermal neutrons
            (90, 232): 2.4,   # Th-232 fast neutrons
        }
        
        # Return known value or estimate based on mass number
        if (Z, A) in neutron_yield:
            return neutron_yield[(Z, A)]
        
        # Rough estimation: increases with A
        return 2.0 + 0.003 * (A - 200) if A > 200 else 2.0
    
    def analyze_decay_chain_npat(self, Z: int, A: int, time_seconds: float, initial_activity: float = 1.0) -> Optional[Dict]:
        """
        Analyze radioactive decay chain using NPAT
        
        Args:
            Z: Atomic number
            A: Mass number
            time_seconds: Time for decay calculation (seconds)
            initial_activity: Initial activity (Bq, optional)
            
        Returns:
            Dictionary with decay chain analysis or None if NPAT unavailable
            
        Note: NPAT requires database files. Run: npat.download("all", True) to download data.
        """
        if not self.npat_available:
            return None
        
        try:
            # Convert to NPAT format: "238U" (mass number first, no hyphen)
            element_map = {
                1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
                92: "U", 94: "Pu", 90: "Th", 88: "Ra", 86: "Rn", 84: "Po", 82: "Pb"
            }
            
            element_symbol = element_map.get(Z, f"Z{Z}")
            nuclide_str = f"{A}{element_symbol}"  # NPAT format: "238U" (mass first)
            
            # Create decay chain using NPAT
            # DecayChain(parent, units='s', R=None, A0=None, time=None)
            chain = DecayChain(nuclide_str, units='s', A0=initial_activity, time=time_seconds)
            
            result = {
                'nuclide': f"{element_symbol}-{A}",
                'atomic_number': Z,
                'mass_number': A,
                'time_seconds': time_seconds,
                'initial_activity_Bq': initial_activity,
                'source': 'NPAT',
                'method': 'NPAT_decay_chain',
                'npat_format': nuclide_str
            }
            
            # Try to access chain properties
            try:
                if hasattr(chain, 'chain'):
                    result['chain_data'] = "Available via chain.chain"
                if hasattr(chain, 'activity'):
                    result['activity'] = "Available via chain.activity"
            except:
                pass
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if 'decay.db' in error_msg or 'zero size' in error_msg:
                return {
                    'error': 'NPAT database not initialized',
                    'message': 'Run: npat.download("all", True) to download nuclear data',
                    'nuclide': f"{element_map.get(Z, f'Z{Z}')}-{A}",
                    'source': 'NPAT'
                }
            print(f"NPAT decay chain analysis error: {e}")
            return None
    
    def get_nuclide_data_npat(self, Z: int, A: int) -> Optional[Dict]:
        """
        Get nuclide data using NPAT Isotope class
        
        Args:
            Z: Atomic number
            A: Mass number
            
        Returns:
            Dictionary with nuclide data or None if NPAT unavailable
            
        Note: NPAT requires database files. Run: npat.download("all", True) to download data.
        """
        if not self.npat_available:
            return None
        
        try:
            # Create isotope using NPAT
            # NPAT format: "238U" (mass number first, no hyphen)
            element_map = {
                1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
                92: "U", 94: "Pu", 90: "Th", 88: "Ra", 86: "Rn", 84: "Po", 82: "Pb"
            }
            
            element_symbol = element_map.get(Z, f"Z{Z}")
            nuclide_str = f"{A}{element_symbol}"  # NPAT format: "238U" (mass first)
            
            isotope = Isotope(nuclide_str)
            
            result = {
                'nuclide': f"{element_symbol}-{A}",
                'atomic_number': Z,
                'mass_number': A,
                'source': 'NPAT',
                'method': 'NPAT_isotope',
                'npat_format': nuclide_str
            }
            
            # Try to extract isotope properties
            try:
                # Check available attributes and call methods if needed
                if hasattr(isotope, 'half_life'):
                    try:
                        # half_life might be a method or property
                        half_life_val = isotope.half_life() if callable(isotope.half_life) else isotope.half_life
                        result['half_life_seconds'] = half_life_val
                    except Exception as e:
                        try:
                            # Try as property
                            result['half_life_seconds'] = isotope.half_life
                        except:
                            result['half_life_note'] = "Available but requires database"
                if hasattr(isotope, 'decay_mode'):
                    try:
                        decay_mode_val = isotope.decay_mode() if callable(isotope.decay_mode) else isotope.decay_mode
                        result['decay_mode'] = decay_mode_val
                    except:
                        result['decay_mode_note'] = "Available but requires database"
                if hasattr(isotope, 'stable'):
                    try:
                        stable_val = isotope.stable() if callable(isotope.stable) else isotope.stable
                        result['stable'] = stable_val
                    except:
                        # stable is already set above, skip
                        pass
                if hasattr(isotope, 'atomic_mass'):
                    try:
                        mass_val = isotope.atomic_mass() if callable(isotope.atomic_mass) else isotope.atomic_mass
                        result['atomic_mass_u'] = mass_val
                    except:
                        pass
            except Exception as prop_error:
                if 'decay.db' in str(prop_error) or 'zero size' in str(prop_error):
                    result['error'] = 'NPAT database not initialized'
                    result['message'] = 'Run: npat.download("all", True) to download nuclear data'
                else:
                    result['note'] = "NPAT Isotope created, properties may require database"
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if 'decay.db' in error_msg or 'zero size' in error_msg:
                return {
                    'error': 'NPAT database not initialized',
                    'message': 'Run: npat.download("all", True) to download nuclear data',
                    'nuclide': f"{element_map.get(Z, f'Z{Z}')}-{A}",
                    'source': 'NPAT'
                }
            print(f"NPAT nuclide data error: {e}")
            return None
    
    def get_advanced_nuclear_analysis(self, Z: int, A: int) -> Dict:
        """
        Get comprehensive advanced nuclear analysis including frontier topics
        Returns: complete nuclear physics analysis
        """
        # Basic properties
        basic_props = self.get_nuclear_properties(Z, A)
        
        # Advanced analysis
        shell_model = self.calculate_shell_model_energy(Z, A)
        alpha_decay = self.calculate_alpha_decay_probability(Z, A, 5.0)  # 5 MeV alpha
        fission_frag = self.calculate_fission_fragmentation(Z, A)
        
        # Stellar processes
        cno_cycle = self.calculate_cno_cycle_energy()
        triple_alpha = self.calculate_triple_alpha_process()
        
        # Frontier topics
        muon_fusion = self.calculate_muon_catalyzed_fusion()
        neutrino_osc = self.calculate_neutrino_oscillation(295, 1.0)  # 295 km, 1 GeV
        
        return {
            "basic_properties": basic_props,
            "shell_model_analysis": shell_model,
            "alpha_decay_analysis": alpha_decay,
            "fission_fragmentation": fission_frag,
            "stellar_nucleosynthesis": {
                "cno_cycle": cno_cycle,
                "triple_alpha": triple_alpha
            },
            "frontier_physics": {
                "muon_catalyzed_fusion": muon_fusion,
                "neutrino_oscillation": neutrino_osc
            }
        }

# Example usage
if __name__ == "__main__":
    physics = NuclearPhysics()
    
    # Example calculations for U-235
    u235_properties = physics.get_nuclear_properties(92, 235)
    print("U-235 Properties:")
    print(json.dumps(u235_properties, indent=2)) 
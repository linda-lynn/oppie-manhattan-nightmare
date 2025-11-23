"""
Mathematical Data Generator for Training Oppenheimer AI
Generates comprehensive mathematical formulas, derivations, and calculations
for nuclear physics, quantum mechanics, and quantum field theory
"""

import json
import os
from datetime import datetime
from typing import List, Dict

class MathematicalDataGenerator:
    """Generate comprehensive mathematical data for training"""
    
    def __init__(self):
        self.mathematical_data = []
    
    def generate_nuclear_physics_formulas(self) -> List[Dict]:
        """Generate comprehensive nuclear physics mathematical formulas"""
        formulas = []
        
        # Binding Energy Formulas
        formulas.append({
            "title": "Semi-Empirical Mass Formula (Complete)",
            "category": "binding_energy",
            "formula": "B = a_v*A - a_s*A^(2/3) - a_c*Z²/A^(1/3) - a_a*(A-2Z)²/A + δ",
            "derivation": """
            Starting from the liquid drop model:
            
            Volume term: B_v = a_v * A
            Surface term: B_s = -a_s * A^(2/3)
            Coulomb term: B_c = -a_c * Z²/A^(1/3)
            Asymmetry term: B_a = -a_a * (A-2Z)²/A
            Pairing term: B_p = δ
            
            Where:
            - a_v = 15.8 MeV (volume coefficient)
            - a_s = 18.3 MeV (surface coefficient)
            - a_c = 0.714 MeV (Coulomb coefficient)
            - a_a = 23.2 MeV (asymmetry coefficient)
            - δ = 12 MeV/√A for even-even, -12 MeV/√A for odd-odd, 0 for odd-A
            """,
            "example": """
            For U-235 (Z=92, A=235):
            B = 15.8*235 - 18.3*235^(2/3) - 0.714*92²/235^(1/3) - 23.2*(235-184)²/235 + 12/√235
            B = 3713 - 18.3*38.1 - 0.714*8464/6.18 - 23.2*2601/235 + 0.783
            B = 3713 - 697 - 978 - 257 + 0.783
            B = 1782 MeV
            """,
            "domain": "nuclear_structure"
        })
        
        # Critical Mass Formulas
        formulas.append({
            "title": "Four-Factor Formula",
            "category": "criticality",
            "formula": "k_eff = η × ε × p × f",
            "derivation": """
            Neutron multiplication factor:
            
            η (eta) = ν * σ_f / (σ_f + σ_c) = average neutrons per fission / (fission + capture)
            ε (epsilon) = fast fission factor = (total fast fissions) / (thermal fissions)
            p = resonance escape probability = exp(-N*I*ξ*Σ_s/Σ_a)
            f = thermal utilization = Σ_a_fuel / Σ_a_total
            
            Where:
            - ν = average neutrons per fission (~2.4 for U-235)
            - σ_f = fission cross section
            - σ_c = capture cross section
            - N = number density
            - I = resonance integral
            - ξ = average logarithmic energy decrement
            """,
            "example": """
            For U-235 thermal reactor:
            η = 2.4 * 585 / (585 + 99) = 2.06
            ε ≈ 1.03 (slight fast fission)
            p ≈ 0.9 (resonance escape)
            f ≈ 0.8 (thermal utilization)
            
            k_eff = 2.06 × 1.03 × 0.9 × 0.8 = 1.53
            """,
            "domain": "reactor_physics"
        })
        
        # Neutron Diffusion Equation
        formulas.append({
            "title": "Neutron Diffusion Equation",
            "category": "neutron_transport",
            "formula": "D∇²φ - Σ_a φ + (1/k)νΣ_f φ = 0",
            "derivation": """
            Starting from neutron balance:
            
            Rate of change = Production - Absorption - Leakage
            
            ∂φ/∂t = S - Σ_a φ - ∇·J
            
            Where J = -D∇φ (Fick's law)
            
            For steady state (∂φ/∂t = 0) and critical system:
            
            D∇²φ - Σ_a φ + S = 0
            
            With source S = (1/k)νΣ_f φ (fission neutrons):
            
            D∇²φ - Σ_a φ + (1/k)νΣ_f φ = 0
            
            Rearranging:
            ∇²φ + B²φ = 0
            
            Where B² = (νΣ_f/k - Σ_a)/D is the material buckling
            """,
            "example": """
            For spherical geometry with radius R:
            φ(r) = A * sin(Br) / r
            
            Critical condition: B = π/R
            
            Critical radius: R_c = π/B = π√(D/(νΣ_f - Σ_a))
            """,
            "domain": "reactor_physics"
        })
        
        # Cross Section Formulas
        formulas.append({
            "title": "Reaction Cross Section",
            "category": "nuclear_reactions",
            "formula": "σ = (π/k²)(2J+1)/(2s+1)(2I+1) × T_l",
            "derivation": """
            From quantum scattering theory:
            
            Partial wave expansion:
            σ_l = (π/k²)(2l+1) |1 - S_l|²
            
            For nuclear reactions with spin:
            σ = Σ_l σ_l × (2J+1)/(2s+1)(2I+1)
            
            Where:
            - k = √(2mE)/ℏ (wave number)
            - J = total angular momentum
            - s = projectile spin
            - I = target spin
            - T_l = transmission coefficient = 1 - |S_l|²
            - S_l = S-matrix element
            """,
            "example": """
            For neutron capture on U-238 (I=0, s=1/2):
            At resonance E_r = 6.67 eV:
            
            σ_resonance = (π/k²)(2J+1) × Γ_n Γ_γ / [(E - E_r)² + (Γ/2)²]
            
            With Γ_n = 1.3 meV, Γ_γ = 23 meV, Γ = 24.3 meV:
            σ_max = (π/k²)(2J+1) × 4Γ_n Γ_γ / Γ²
            """,
            "domain": "nuclear_reactions"
        })
        
        # Decay Formulas
        formulas.append({
            "title": "Radioactive Decay Law",
            "category": "decay",
            "formula": "N(t) = N₀ e^(-λt)",
            "derivation": """
            From probability theory:
            
            dN/dt = -λN
            
            Solving the differential equation:
            ∫ dN/N = -λ ∫ dt
            ln(N) = -λt + C
            N(t) = N₀ e^(-λt)
            
            Where:
            - λ = decay constant = ln(2)/T_1/2
            - T_1/2 = half-life
            - Activity A(t) = λN(t) = λN₀ e^(-λt)
            """,
            "example": """
            For U-238 (T_1/2 = 4.47×10⁹ years):
            λ = ln(2) / (4.47×10⁹ × 365.25 × 24 × 3600) = 4.92×10⁻¹⁸ s⁻¹
            
            After 1 billion years:
            N(10⁹) = N₀ e^(-4.92×10⁻¹⁸ × 10⁹ × 365.25 × 24 × 3600)
            N(10⁹) = N₀ e^(-0.155) = 0.856 N₀
            """,
            "domain": "decay_processes"
        })
        
        return formulas
    
    def generate_quantum_mechanics_formulas(self) -> List[Dict]:
        """Generate comprehensive quantum mechanics formulas"""
        formulas = []
        
        # Schrödinger Equation
        formulas.append({
            "title": "Time-Dependent Schrödinger Equation",
            "category": "quantum_mechanics",
            "formula": "iℏ ∂ψ/∂t = Ĥψ",
            "derivation": """
            From de Broglie hypothesis: p = ℏk, E = ℏω
            
            Wave function: ψ(x,t) = A exp(i(kx - ωt))
            
            Operators:
            p̂ = -iℏ∇, Ê = iℏ∂/∂t
            
            Energy operator: Ĥ = p̂²/(2m) + V(x) = -ℏ²/(2m)∇² + V(x)
            
            Substituting: iℏ ∂ψ/∂t = Ĥψ
            
            For stationary states: ψ(x,t) = φ(x)e^(-iEt/ℏ)
            
            Time-independent form: Ĥφ = Eφ
            """,
            "example": """
            For hydrogen atom (V(r) = -e²/(4πε₀r)):
            
            Ĥ = -ℏ²/(2m)∇² - e²/(4πε₀r)
            
            Eigenvalues: E_n = -13.6 eV / n²
            
            Ground state (n=1): E₁ = -13.6 eV
            """,
            "domain": "quantum_mechanics"
        })
        
        # Uncertainty Principle
        formulas.append({
            "title": "Heisenberg Uncertainty Principle",
            "category": "quantum_mechanics",
            "formula": "Δx · Δp ≥ ℏ/2",
            "derivation": """
            From commutation relation: [x̂, p̂] = iℏ
            
            For any two operators: ΔA · ΔB ≥ |⟨[A,B]⟩|/2
            
            Therefore: Δx · Δp ≥ ℏ/2
            
            Similarly: ΔE · Δt ≥ ℏ/2
            
            This is fundamental - not a measurement limitation but a property of quantum systems
            """,
            "example": """
            For electron in atom (Δx ≈ 0.1 nm):
            Δp ≥ ℏ/(2Δx) = 1.05×10⁻³⁴ / (2 × 10⁻¹⁰) = 5.25×10⁻²⁵ kg·m/s
            
            Δv = Δp/m = 5.25×10⁻²⁵ / 9.11×10⁻³¹ = 5.76×10⁵ m/s
            """,
            "domain": "quantum_mechanics"
        })
        
        # Quantum Tunneling
        formulas.append({
            "title": "Quantum Tunneling Probability",
            "category": "quantum_mechanics",
            "formula": "T = exp(-2∫_{x1}^{x2} √(2m(V(x)-E))/ℏ dx)",
            "derivation": """
            For potential barrier V(x) > E:
            
            In classically forbidden region, wave function:
            ψ(x) = A exp(-κx) + B exp(κx)
            
            Where κ = √(2m(V-E))/ℏ
            
            Transmission coefficient:
            T = |t|² = exp(-2κa) for rectangular barrier of width a
            
            For general barrier:
            T ≈ exp(-2∫_{x1}^{x2} κ(x) dx)
            """,
            "example": """
            For alpha decay of U-238:
            Barrier height V₀ ≈ 30 MeV, Q-value ≈ 4.27 MeV
            
            κ = √(2m_α(V₀ - Q))/ℏ = √(2 × 6.64×10⁻²⁷ × 25.73×10⁶ × 1.6×10⁻¹⁹) / 1.05×10⁻³⁴
            κ = 1.57×10¹⁵ m⁻¹
            
            For barrier width a ≈ 10⁻¹⁴ m:
            T = exp(-2 × 1.57×10¹⁵ × 10⁻¹⁴) = exp(-31.4) ≈ 2×10⁻¹⁴
            """,
            "domain": "quantum_mechanics"
        })
        
        # Angular Momentum
        formulas.append({
            "title": "Angular Momentum Operators",
            "category": "quantum_mechanics",
            "formula": "[L̂_i, L̂_j] = iℏε_{ijk} L̂_k",
            "derivation": """
            Angular momentum: L = r × p
            
            Quantum operators:
            L̂_x = -iℏ(y∂/∂z - z∂/∂y)
            L̂_y = -iℏ(z∂/∂x - x∂/∂z)
            L̂_z = -iℏ(x∂/∂y - y∂/∂x)
            
            Commutation relations:
            [L̂_x, L̂_y] = iℏL̂_z
            [L̂_y, L̂_z] = iℏL̂_x
            [L̂_z, L̂_x] = iℏL̂_y
            
            General form: [L̂_i, L̂_j] = iℏε_{ijk} L̂_k
            
            Eigenvalues: L² = ℏ²l(l+1), L_z = ℏm
            """,
            "example": """
            For p-orbital (l=1):
            L² = ℏ² × 1 × 2 = 2ℏ²
            L_z = -ℏ, 0, or +ℏ (m = -1, 0, 1)
            """,
            "domain": "quantum_mechanics"
        })
        
        return formulas
    
    def generate_quantum_field_theory_formulas(self) -> List[Dict]:
        """Generate quantum field theory formulas"""
        formulas = []
        
        # QCD Lagrangian
        formulas.append({
            "title": "QCD Lagrangian",
            "category": "quantum_field_theory",
            "formula": "L_QCD = ψ̄(iγ^μD_μ - m)ψ - (1/4)G^a_{μν}G^{aμν}",
            "derivation": """
            Quantum Chromodynamics describes strong interactions:
            
            Covariant derivative: D_μ = ∂_μ + igA^a_μT^a
            
            Field strength tensor:
            G^a_{μν} = ∂_μA^a_ν - ∂_νA^a_μ + gf^{abc}A^b_μA^c_ν
            
            Where:
            - g = strong coupling constant
            - T^a = SU(3) generators (Gell-Mann matrices)
            - f^{abc} = structure constants
            - A^a_μ = gluon fields
            
            The Lagrangian includes:
            1. Quark kinetic and mass terms
            2. Gluon kinetic term
            3. Self-interactions (3-gluon, 4-gluon vertices)
            """,
            "example": """
            At high energies (Q² >> Λ²_QCD):
            α_s(Q²) = 12π / ((33-2n_f)ln(Q²/Λ²_QCD))
            
            Where n_f = number of flavors, Λ_QCD ≈ 200 MeV
            """,
            "domain": "quantum_field_theory"
        })
        
        # Nuclear Force
        formulas.append({
            "title": "Nuclear Force from Pion Exchange",
            "category": "quantum_field_theory",
            "formula": "V(r) = (g²/4π)(e^(-m_πr)/r)",
            "derivation": """
            From Yukawa potential (exchange of massive particle):
            
            V(r) = -g²/(4π) × e^(-mr)/r
            
            For pion exchange (m_π ≈ 140 MeV/c²):
            V(r) = (g²/4π)(e^(-m_πr)/r)
            
            Where g = pion-nucleon coupling constant ≈ 13.5
            
            Range: R = 1/m_π ≈ 1.4 fm
            
            This gives the long-range part of nuclear force
            """,
            "example": """
            At r = 1 fm:
            V(1 fm) = (13.5²/4π) × e^(-140×1.4/197) / 1
            V(1 fm) = 14.5 × e^(-0.995) ≈ 5.4 MeV
            """,
            "domain": "quantum_field_theory"
        })
        
        return formulas
    
    def generate_additional_nuclear_formulas(self) -> List[Dict]:
        """Generate additional nuclear physics formulas"""
        formulas = []
        
        # Fission Energy Release
        formulas.append({
            "title": "Fission Energy Release",
            "category": "fission",
            "formula": "Q_fission = (M_parent - ΣM_products)c²",
            "derivation": """
            From mass-energy equivalence E = mc²:
            
            Q = (m_initial - m_final)c²
            
            For fission: U-235 + n → fragments + neutrons
            
            Q = [m(U-235) + m(n) - Σm(fragments) - Σm(neutrons)]c²
            
            Typical: Q ≈ 200 MeV per fission
            
            Energy distribution:
            - Kinetic energy of fragments: ~165 MeV
            - Neutron kinetic energy: ~5 MeV
            - Prompt gamma rays: ~7 MeV
            - Beta decay: ~7 MeV
            - Neutrino energy: ~12 MeV (not recoverable)
            """,
            "example": """
            For U-235 fission:
            m(U-235) = 235.0439299 u
            m(n) = 1.0086649 u
            m(Ba-141) = 140.914411 u
            m(Kr-92) = 91.926156 u
            m(3n) = 3.0259947 u
            
            Q = (236.0525948 - 234.8665617) × 931.494 MeV/u
            Q = 1.1860331 × 931.494 = 1105 MeV
            
            But actual Q ≈ 200 MeV (difference due to excited states)
            """,
            "domain": "nuclear_reactions"
        })
        
        # Neutron Flux
        formulas.append({
            "title": "Neutron Flux",
            "category": "neutron_physics",
            "formula": "φ = nv",
            "derivation": """
            Neutron flux: φ = neutron density × velocity
            
            Reaction rate: R = φΣ = nvΣ
            
            Where:
            - n = neutron density (neutrons/cm³)
            - v = neutron velocity (cm/s)
            - Σ = macroscopic cross section (cm⁻¹)
            - φ = flux (neutrons/cm²/s)
            
            For thermal neutrons (E = 0.025 eV):
            v = √(2E/m) = √(2 × 0.025 × 1.6×10⁻¹⁹ / 1.67×10⁻²⁷)
            v = 2.2×10⁵ cm/s
            """,
            "example": """
            In reactor core:
            n = 10¹⁴ neutrons/cm³
            v = 2.2×10⁵ cm/s (thermal)
            
            φ = 10¹⁴ × 2.2×10⁵ = 2.2×10¹⁹ neutrons/cm²/s
            
            For U-235 (σ_f = 585 barns):
            Σ_f = N × σ_f = 0.048 × 10²⁴ × 585×10⁻²⁴ = 28.08 cm⁻¹
            
            Fission rate: R = φΣ_f = 2.2×10¹⁹ × 28.08 = 6.18×10²⁰ fissions/cm³/s
            """,
            "domain": "reactor_physics"
        })
        
        # Beta Decay
        formulas.append({
            "title": "Beta Decay Energy Spectrum",
            "category": "decay",
            "formula": "N(E) dE = (G²|M|²/2π³ℏ⁷c³) p_e E_e (E₀ - E_e)² F(Z,E_e) dE",
            "derivation": """
            From Fermi's Golden Rule:
            
            Transition rate: λ = (2π/ℏ)|M|² ρ(E)
            
            For beta decay: n → p + e⁻ + ν̄
            
            Phase space factor:
            ρ(E) ∝ p_e E_e (E₀ - E_e)²
            
            With Fermi function F(Z,E_e) for Coulomb correction:
            
            N(E) dE = (G²|M|²/2π³ℏ⁷c³) p_e E_e (E₀ - E_e)² F(Z,E_e) dE
            
            Where:
            - G = Fermi coupling constant
            - |M|² = nuclear matrix element
            - E₀ = maximum beta energy (Q-value)
            - p_e = electron momentum
            """,
            "example": """
            For C-14 beta decay (Q = 156 keV):
            Maximum energy: E_max = 156 keV
            
            Average energy: ⟨E⟩ ≈ E_max/3 = 52 keV
            
            Half-life: T_1/2 = 5730 years
            """,
            "domain": "decay_processes"
        })
        
        # Scattering Cross Section
        formulas.append({
            "title": "Differential Scattering Cross Section",
            "category": "scattering",
            "formula": "dσ/dΩ = |f(θ)|²",
            "derivation": """
            Scattering amplitude:
            f(θ) = (1/2ik) Σ_l (2l+1)(e^(2iδ_l) - 1)P_l(cos θ)
            
            Differential cross section:
            dσ/dΩ = |f(θ)|²
            
            Total cross section (optical theorem):
            σ_total = (4π/k) Im[f(0)] = (4π/k²) Σ_l (2l+1) sin²(δ_l)
            
            Elastic cross section:
            σ_elastic = (4π/k²) Σ_l (2l+1) |e^(2iδ_l) - 1|²/4
            
            Inelastic cross section:
            σ_inelastic = (π/k²) Σ_l (2l+1)(1 - |S_l|²)
            """,
            "example": """
            For s-wave scattering (l=0):
            f(θ) = (e^(2iδ₀) - 1)/(2ik) = sin(δ₀)e^(iδ₀)/k
            
            dσ/dΩ = sin²(δ₀)/k² (isotropic)
            
            σ_total = 4π sin²(δ₀)/k²
            """,
            "domain": "nuclear_reactions"
        })
        
        return formulas
    
    def generate_additional_quantum_formulas(self) -> List[Dict]:
        """Generate additional quantum mechanics formulas"""
        formulas = []
        
        # Path Integral
        formulas.append({
            "title": "Path Integral Formulation",
            "category": "quantum_mechanics",
            "formula": "K(x',t';x,t) = ∫D[x(t)] exp(iS[x(t)]/ℏ)",
            "derivation": """
            Feynman's path integral:
            
            Propagator: K(x',t';x,t) = ⟨x'|e^(-iĤ(t'-t)/ℏ)|x⟩
            
            Discretizing time: t₀, t₁, ..., t_N
            
            K = lim_{N→∞} ∫...∫ dx₁...dx_{N-1} Π_{i=0}^{N-1} ⟨x_{i+1}|e^(-iĤε/ℏ)|x_i⟩
            
            Where ε = (t'-t)/N
            
            In the limit: K = ∫D[x(t)] exp(iS/ℏ)
            
            Action: S = ∫_{t}^{t'} L(x, ẋ, t) dt
            
            This gives quantum amplitude as sum over all paths
            """,
            "example": """
            For free particle (L = mẋ²/2):
            K(x',t';x,t) = √(m/2πiℏ(t'-t)) exp(im(x'-x)²/2ℏ(t'-t))
            """,
            "domain": "quantum_mechanics"
        })
        
        # Density Matrix
        formulas.append({
            "title": "Density Matrix",
            "category": "quantum_mechanics",
            "formula": "ρ = Σ_i p_i |ψ_i⟩⟨ψ_i|",
            "derivation": """
            For mixed state (statistical ensemble):
            
            Density operator: ρ = Σ_i p_i |ψ_i⟩⟨ψ_i|
            
            Where p_i = probability of state |ψ_i⟩
            
            Properties:
            - Tr(ρ) = 1 (normalization)
            - ρ = ρ† (Hermitian)
            - Tr(ρ²) ≤ 1 (equality for pure states)
            
            Expectation value: ⟨A⟩ = Tr(ρA)
            
            Time evolution: iℏ dρ/dt = [Ĥ, ρ]
            """,
            "example": """
            For thermal equilibrium:
            ρ = exp(-Ĥ/kT) / Tr(exp(-Ĥ/kT))
            
            This is the canonical ensemble density matrix
            """,
            "domain": "quantum_mechanics"
        })
        
        # Perturbation Theory
        formulas.append({
            "title": "Time-Dependent Perturbation Theory",
            "category": "quantum_mechanics",
            "formula": "c_f(t) = -(i/ℏ)∫₀ᵗ ⟨f|H'(t')|i⟩ e^(iω_fi t') dt'",
            "derivation": """
            For perturbation H'(t):
            
            Wave function: |ψ(t)⟩ = Σ_n c_n(t) e^(-iE_n t/ℏ)|n⟩
            
            Substituting into Schrödinger equation:
            
            iℏ dc_f/dt = Σ_n ⟨f|H'|n⟩ c_n e^(iω_fn t)
            
            First order (c_n ≈ δ_ni):
            c_f(t) = -(i/ℏ)∫₀ᵗ ⟨f|H'(t')|i⟩ e^(iω_fi t') dt'
            
            Transition probability: P_{i→f} = |c_f(t)|²
            
            Where ω_fi = (E_f - E_i)/ℏ
            """,
            "example": """
            For constant perturbation H'(t) = H':
            c_f(t) = -(i/ℏ)⟨f|H'|i⟩ ∫₀ᵗ e^(iω_fi t') dt'
            c_f(t) = -(i/ℏ)⟨f|H'|i⟩ (e^(iω_fi t) - 1)/(iω_fi)
            
            P_{i→f} = |⟨f|H'|i⟩|² sin²(ω_fi t/2)/(ℏ²ω_fi²)
            """,
            "domain": "quantum_mechanics"
        })
        
        return formulas
    
    def generate_advanced_calculations(self) -> List[Dict]:
        """Generate advanced mathematical calculations with step-by-step solutions"""
        calculations = []
        
        # Binding Energy Calculation
        calculations.append({
            "title": "Complete Binding Energy Calculation for Fe-56",
            "category": "binding_energy",
            "formula": "B = a_v*A - a_s*A^(2/3) - a_c*Z²/A^(1/3) - a_a*(A-2Z)²/A + δ",
            "derivation": "",
            "example": """
            For Fe-56 (Z=26, A=56, even-even):
            
            Step 1: Calculate each term
            Volume term: B_v = a_v × A = 15.8 × 56 = 884.8 MeV
            
            Surface term: B_s = -a_s × A^(2/3) = -18.3 × 56^(2/3)
            56^(2/3) = (56^(1/3))² = (3.8259)² = 14.637
            B_s = -18.3 × 14.637 = -267.86 MeV
            
            Coulomb term: B_c = -a_c × Z²/A^(1/3) = -0.714 × 26²/56^(1/3)
            56^(1/3) = 3.8259
            B_c = -0.714 × 676/3.8259 = -0.714 × 176.7 = -126.16 MeV
            
            Asymmetry term: B_a = -a_a × (A-2Z)²/A = -23.2 × (56-52)²/56
            B_a = -23.2 × 16/56 = -23.2 × 0.2857 = -6.63 MeV
            
            Pairing term: δ = 12/√A = 12/√56 = 12/7.483 = 1.60 MeV (even-even)
            
            Step 2: Sum all terms
            B = 884.8 - 267.86 - 126.16 - 6.63 + 1.60
            B = 485.75 MeV
            
            Step 3: Binding energy per nucleon
            B/A = 485.75/56 = 8.67 MeV/nucleon
            
            This matches the experimental value closely!
            """,
            "domain": "nuclear_structure"
        })
        
        # Critical Mass Calculation
        calculations.append({
            "title": "Critical Mass Calculation for U-235",
            "category": "criticality",
            "formula": "M_critical = (4π/3)ρR_c³",
            "derivation": "",
            "example": """
            For U-235 sphere:
            
            Step 1: Calculate material buckling
            B²_m = (νΣ_f - Σ_a)/D
            
            Given:
            - ν = 2.43 (average neutrons per fission)
            - Σ_f = 0.366 cm⁻¹ (macroscopic fission cross section)
            - Σ_a = 0.153 cm⁻¹ (macroscopic absorption cross section)
            - D = 0.9 cm (diffusion coefficient)
            
            B²_m = (2.43 × 0.366 - 0.153)/0.9
            B²_m = (0.889 - 0.153)/0.9 = 0.736/0.9 = 0.818 cm⁻²
            
            Step 2: Calculate critical radius
            For sphere: B²_g = (π/R)² (geometric buckling)
            
            At criticality: B²_m = B²_g
            R_c = π/√B²_m = π/√0.818 = 3.1416/0.904 = 3.47 cm
            
            Step 3: Calculate critical mass
            Density: ρ = 18.7 g/cm³
            M_critical = (4π/3) × 18.7 × (3.47)³
            M_critical = (4π/3) × 18.7 × 41.75
            M_critical = 3267 g = 3.27 kg
            
            With reflector: M_critical ≈ 15-20 kg
            """,
            "domain": "reactor_physics"
        })
        
        # Quantum Tunneling Calculation
        calculations.append({
            "title": "Alpha Decay Tunneling Probability",
            "category": "quantum_mechanics",
            "formula": "T = exp(-2∫√(2m(V-E))/ℏ dx)",
            "derivation": "",
            "example": """
            For U-238 alpha decay:
            
            Step 1: Parameters
            Q-value: Q = 4.27 MeV
            Barrier height: V₀ ≈ 30 MeV (Coulomb barrier)
            Alpha particle mass: m_α = 6.64×10⁻²⁷ kg
            
            Step 2: Calculate κ
            κ = √(2m(V₀ - Q))/ℏ
            κ = √(2 × 6.64×10⁻²⁷ × (30-4.27)×10⁶ × 1.6×10⁻¹⁹) / 1.05×10⁻³⁴
            κ = √(2 × 6.64×10⁻²⁷ × 25.73×10⁶ × 1.6×10⁻¹⁹) / 1.05×10⁻³⁴
            κ = √(5.47×10⁻³⁸) / 1.05×10⁻³⁴
            κ = 2.34×10⁻¹⁹ / 1.05×10⁻³⁴ = 2.23×10¹⁵ m⁻¹
            
            Step 3: Estimate barrier width
            Nuclear radius: R₁ = 1.2 × 238^(1/3) = 7.4 fm
            Turning point: R₂ = 2Ze²/(4πε₀Q) = 2×92×1.44/(4.27) = 62 fm
            Width: a = R₂ - R₁ ≈ 55 fm = 55×10⁻¹⁵ m
            
            Step 4: Calculate transmission
            T = exp(-2κa) = exp(-2 × 2.23×10¹⁵ × 55×10⁻¹⁵)
            T = exp(-245.3) = 2.2×10⁻¹⁰⁷
            
            Step 5: Decay constant
            Attempt frequency: f ≈ 10²¹ s⁻¹
            λ = f × T = 10²¹ × 2.2×10⁻¹⁰⁷ = 2.2×10⁻⁸⁶ s⁻¹
            
            Half-life: T_1/2 = ln(2)/λ = 0.693/2.2×10⁻⁸⁶ = 3.15×10⁸⁵ s ≈ 10¹⁸ years
            
            (Actual T_1/2 = 4.47×10⁹ years - Gamow factor improves this)
            """,
            "domain": "quantum_mechanics"
        })
        
        return calculations
    
    def generate_all_mathematical_data(self) -> List[Dict]:
        """Generate all mathematical data"""
        all_data = []
        
        # Add nuclear physics formulas
        nuclear_formulas = self.generate_nuclear_physics_formulas()
        all_data.extend(nuclear_formulas)
        
        # Add quantum mechanics formulas
        quantum_formulas = self.generate_quantum_mechanics_formulas()
        all_data.extend(quantum_formulas)
        
        # Add quantum field theory formulas
        qft_formulas = self.generate_quantum_field_theory_formulas()
        all_data.extend(qft_formulas)
        
        # Add additional nuclear physics formulas
        additional_nuclear = self.generate_additional_nuclear_formulas()
        all_data.extend(additional_nuclear)
        
        # Add additional quantum mechanics formulas
        additional_quantum = self.generate_additional_quantum_formulas()
        all_data.extend(additional_quantum)
        
        # Add advanced calculations
        advanced_calc = self.generate_advanced_calculations()
        all_data.extend(advanced_calc)
        
        # Format for knowledge base
        formatted_data = []
        for item in all_data:
            formatted_data.append({
                "source": "mathematical_generator",
                "title": item["title"],
                "content": f"{item['formula']}\n\nDerivation:\n{item['derivation']}\n\nExample:\n{item['example']}",
                "formulas": [item["formula"]],
                "category": item["category"],
                "domain": item["domain"],
                "keywords": [item["category"], item["domain"], "mathematics", "formula", "derivation"],
                "publication_date": datetime.now().isoformat(),
                "imported_at": datetime.now().isoformat()
            })
        
        return formatted_data
    
    def save_to_file(self, output_file: str = "mathematical_data.json"):
        """Save generated mathematical data to file"""
        data = self.generate_all_mathematical_data()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Generated {len(data)} mathematical formulas and saved to {output_file}")
        return data


def main():
    """Generate and save mathematical data"""
    generator = MathematicalDataGenerator()
    data = generator.save_to_file()
    
    print(f"\nGenerated mathematical data categories:")
    categories = {}
    for item in data:
        cat = item.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in categories.items():
        print(f"  {cat}: {count} formulas")


if __name__ == "__main__":
    main()


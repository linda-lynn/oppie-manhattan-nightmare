# Oppenheimer AI - Nuclear Physics Research Environment

A comprehensive nuclear physics simulation and AI research environment featuring J. Robert Oppenheimer AI assistant for undergraduate nuclear physics studies.

## 🔬 Features

### Nuclear Physics Calculations
- **Binding Energy**: Semi-empirical mass formula (Weizsäcker formula)
- **Critical Mass**: Fissile material criticality calculations
- **Decay Constants**: Radioactive decay and half-life calculations
- **Fission/Fusion Energy**: Energy release calculations
- **Neutron Scattering**: Elastic and inelastic scattering cross-sections
- **Reactor Kinetics**: Point kinetics equations and reactor dynamics
- **Cross-sections**: Energy-dependent neutron cross-sections

### AI Assistant Features
- **Oppenheimer AI**: J. Robert Oppenheimer personality simulation
- **Time-aware responses**: AI mood changes based on time of day
- **Academic rigor**: Professional nuclear physics discussions
- **Research support**: Comprehensive theoretical analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Ollama with Mistral model
- Required Python packages (see Installation)

### Installation

1. **Clone/Download the project**
   ```bash
   cd /Users/amy/oppenheimer_env
   ```

2. **Install Python dependencies**
   ```bash
   /opt/homebrew/bin/python3 -m pip install ollama requests numpy pytz --break-system-packages
   ```

3. **Start Ollama service**
   ```bash
   ollama serve
   ```

4. **Launch the application**
   ```bash
   /opt/homebrew/bin/python3 oppenheimer_gui.py
   ```

### Access
- **Login Code**: `Joanna3225@`
- **Interface**: KAERI Research Portal style

## 📚 Nuclear Physics Equations

### Binding Energy (Weizsäcker Formula)
```
B(A,Z) = a_v*A - a_s*A^(2/3) - a_c*Z*(Z-1)/A^(1/3) - a_a*(A-2Z)²/A + a_p*δ(A,Z)/A^(1/2)
```

### Critical Mass
```
M_c = (4/3)π * R_c³ * ρ
where R_c = π√(D/(k_inf-1))
```

### Neutron Scattering Cross-sections
- **Elastic**: σ_elastic = πR²(1 + 1/√E)
- **Inelastic**: σ_inelastic = πR²(E-E_th)/E
- **Total**: σ_total = σ_elastic + σ_inelastic

### Reactor Kinetics
```
dn/dt = (ρ-β)/Λ * n + ΣλᵢCᵢ
dCᵢ/dt = βᵢ/Λ * n - λᵢCᵢ
```

## 🎯 Usage Examples

### Nuclear Properties Calculation
```python
physics = NuclearPhysics()
properties = physics.get_comprehensive_nuclear_properties(92, 235)
# Returns: binding energy, mass defect, critical mass, etc.
```

### Neutron Scattering Analysis
```python
# Calculate scattering cross-sections
sigma_elastic = physics.calculate_elastic_scattering_cross_section(238, 1e6)
sigma_inelastic = physics.calculate_inelastic_scattering_cross_section(238, 1e6)

# Scattering kinematics
kinematics = physics.calculate_scattering_kinematics(1e6, 238, math.pi/4)
```

### Reactor Analysis
```python
# Reactor kinetics
kinetics = physics.calculate_reactor_kinetics(0.001, 0.0065, 1e-4)

# Neutron flux
flux = physics.calculate_neutron_flux(1000, 50)  # 1000 MW, 50 m³
```

## 🔧 Technical Details

### Dependencies
- `ollama`: AI model interface
- `requests`: API communication
- `numpy`: Numerical calculations
- `pytz`: Timezone handling
- `tkinter`: GUI framework (built-in)

### File Structure
```
oppenheimer_env/
├── nuclear_physics.py      # Core physics calculations
├── oppenheimer_gui.py      # GUI interface
├── oppenheimer_agent.py    # AI agent (standalone)
└── README.md              # This file
```

### AI Model Configuration
- **Model**: Mistral (via Ollama)
- **Personality**: J. Robert Oppenheimer
- **Context**: Nuclear physics research
- **Time awareness**: Los Alamos timezone

## 📖 Academic Applications

### Undergraduate Nuclear Physics
- **Course Support**: Nuclear reactions, reactor physics
- **Homework**: Cross-section calculations, decay analysis
- **Research**: Critical mass studies, neutron transport
- **Projects**: Reactor design, safety analysis

### Research Capabilities
- **Theoretical Analysis**: Binding energy calculations
- **Experimental Design**: Cross-section measurements
- **Safety Studies**: Criticality analysis
- **Educational**: Interactive learning with AI mentor

## 🎓 Educational Value

### Learning Objectives
- Master nuclear physics equations
- Understand reactor physics principles
- Learn neutron transport theory
- Develop critical thinking skills

### AI Mentorship
- **Academic Guidance**: Professional nuclear physics discussions
- **Problem Solving**: Step-by-step equation derivations
- **Research Support**: Theoretical analysis and calculations
- **Time Context**: Realistic research environment simulation

## 🔒 Security & Access

### Research Environment
- **Access Control**: Secure login system
- **Academic Integrity**: Original calculations and analysis
- **Data Privacy**: Local processing, no external data sharing
- **Research Ethics**: Proper academic standards

## 🚀 Advanced Features

### Future Enhancements
- [ ] Monte Carlo neutron transport
- [ ] Reactor core design tools
- [ ] Nuclear data visualization
- [ ] Advanced AI model integration
- [ ] Multi-language support

## 📞 Support

### Troubleshooting
1. **Ollama not running**: `ollama serve`
2. **Module errors**: Check Python path and dependencies
3. **GUI issues**: Verify tkinter installation
4. **AI responses**: Ensure Mistral model is loaded

### Academic Use
- **Citation**: Proper attribution for academic work
- **Originality**: All calculations are original implementations
- **Verification**: Cross-check with standard references
- **Learning**: Use as educational tool, not for direct assignment submission

## 📄 License

Academic Research Use - Nuclear Physics Education
© 2024 Oppenheimer AI Research Environment

---

**Note**: This is an educational tool for nuclear physics studies. All calculations should be verified against standard references and used responsibly in academic contexts.

# Advanced Complex Calculations Module

## Installation

To enable extreme complex calculations, install scipy:

```bash
pip install scipy
```

## Available Calculations

### 1. **Neutron Transport ODE Solver**
- Solves: dN/dt = (k_eff - 1)N/Λ - λN
- Uses RK45 (Runge-Kutta) method
- High precision numerical integration

### 2. **Monte Carlo Neutron Transport**
- Simulates individual neutron paths
- Statistical sampling (10,000+ simulations)
- Calculates absorption/scattering probabilities
- Mean free path calculations

### 3. **Fission Yield Distribution**
- Gaussian approximation for fragment masses
- Statistical analysis of yield curves
- Light/heavy fragment peaks

### 4. **Critical Mass Optimization**
- L-BFGS-B optimization algorithm
- Minimizes critical mass under constraints
- Handles geometry constraints

### 5. **Neutron Energy Spectrum**
- Multi-group transport theory
- Energy degradation through materials
- Layer-by-layer analysis

### 6. **Bateman Equations Solver**
- Radioactive decay chain calculations
- System of ODEs solution
- Activity calculations over time

### 7. **Neutron Flux Distribution**
- Diffusion equation solver
- Finite difference method
- Spatial distribution in reactors

### 8. **Sensitivity Analysis**
- Parameter sensitivity coefficients
- Forward/backward variations
- Statistical impact analysis

## Usage

1. Click "Advanced Calc" button in GUI
2. Select calculation type
3. System uses current Z/A values or defaults
4. Results displayed with full methodology

## Technical Details

- **Numerical Methods**: ODE solvers, Monte Carlo, optimization
- **Precision**: High-precision floating point (64-bit)
- **Performance**: Optimized for complex calculations
- **Scalability**: Handles large parameter spaces

## For 6-Year Research

These calculations support:
- PhD-level research complexity
- Publication-quality results
- Reproducible numerical methods
- Advanced statistical analysis






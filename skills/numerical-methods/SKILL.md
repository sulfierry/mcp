---
name: Numerical Methods
description: Numerical computing and scientific computation. ODE/PDE solvers, linear algebra, interpolation, quadrature, root finding, finite differences, spectral methods, and stability analysis using SciPy, NumPy, and JAX.
---

# Numerical Methods

Expert in numerical analysis and scientific computing. Covers the full spectrum of computational mathematics from root finding to PDE discretization.

## Core Competencies

### Linear Algebra (Dense & Sparse)
- **Direct solvers**: LU, Cholesky, QR factorization via `scipy.linalg`
- **Iterative solvers**: CG, GMRES, BiCGSTAB via `scipy.sparse.linalg`
- **Eigenvalue problems**: `eigh`, `eigs`, Lanczos, Arnoldi iterations
- **Sparse formats**: CSR, CSC, COO — construction, conversion, and efficient operations
- **Conditioning**: Condition number estimation, preconditioning strategies (ILU, AMG)

```python
import numpy as np
from scipy import linalg, sparse
from scipy.sparse.linalg import spsolve, eigsh, LinearOperator

# Dense SVD
U, s, Vt = linalg.svd(A, full_matrices=False)

# Sparse eigenvalue problem (shift-invert for interior eigenvalues)
eigenvalues, eigenvectors = eigsh(A_sparse, k=10, sigma=0.0, which='LM')

# Preconditioned iterative solve
M = sparse.linalg.spilu(A_sparse)
M_operator = LinearOperator(A_sparse.shape, M.solve)
x, info = sparse.linalg.gmres(A_sparse, b, M=M_operator, atol=1e-10)
```

### ODE Solvers
- **Initial Value Problems (IVP)**: `solve_ivp` with RK45, RK23, DOP853, Radau, BDF, LSODA
- **Stiff systems**: Implicit methods (Radau, BDF) with Jacobian support
- **Boundary Value Problems (BVP)**: `solve_bvp` with collocation
- **Delay Differential Equations**: via `ddeint` or custom stepping
- **Event detection**: Zero-crossing detection for hybrid systems

```python
from scipy.integrate import solve_ivp

def lorenz(t, y, sigma=10, rho=28, beta=8/3):
    x, y_coord, z = y
    return [sigma*(y_coord - x), x*(rho - z) - y_coord, x*y_coord - beta*z]

sol = solve_ivp(lorenz, [0, 50], [1, 1, 1],
                method='RK45', dense_output=True,
                rtol=1e-10, atol=1e-12,
                max_step=0.01)

# Stiff system with analytical Jacobian
sol_stiff = solve_ivp(stiff_rhs, t_span, y0,
                      method='Radau', jac=jacobian,
                      rtol=1e-8, atol=1e-10)
```

### PDE Discretization
- **Finite Differences (FD)**: 2nd/4th-order central, upwind, Crank-Nicolson
- **Finite Elements (FEM)**: Weak formulation, mesh generation, assembly
- **Spectral Methods**: Chebyshev/Fourier collocation, Galerkin projection
- **Method of Lines**: Semi-discretize space → integrate with ODE solver
- **Libraries**: FEniCS/FEniCSx, Firedrake, Dedalus (spectral)

```python
import numpy as np

# 2D Poisson with 5-point stencil (Method of Lines)
def laplacian_2d(u, dx, dy):
    """5-point Laplacian on uniform grid."""
    lap = np.zeros_like(u)
    lap[1:-1,1:-1] = (
        (u[2:,1:-1] - 2*u[1:-1,1:-1] + u[:-2,1:-1]) / dx**2 +
        (u[1:-1,2:] - 2*u[1:-1,1:-1] + u[1:-1,:-2]) / dy**2
    )
    return lap

# Spectral differentiation (Chebyshev)
def cheb_diff_matrix(N):
    """Chebyshev differentiation matrix."""
    x = np.cos(np.pi * np.arange(N+1) / N)
    c = np.ones(N+1); c[0] = 2; c[N] = 2
    c *= (-1)**np.arange(N+1)
    X = np.tile(x, (N+1, 1))
    dX = X - X.T
    D = np.outer(c, 1/c) / (dX + np.eye(N+1))
    D -= np.diag(D.sum(axis=1))
    return D, x
```

### Interpolation & Approximation
- **Polynomial**: Lagrange, Newton, barycentric via `scipy.interpolate`
- **Splines**: Cubic, B-splines, NURBS, tension splines
- **Radial Basis Functions (RBF)**: Multiquadric, Gaussian, thin-plate
- **Scattered data**: `griddata`, `RBFInterpolator`, `CloughTocher2DInterpolator`
- **Rational approximation**: Padé, AAA algorithm

```python
from scipy.interpolate import (
    CubicSpline, BSpline, make_interp_spline,
    RBFInterpolator, griddata
)

# Cubic spline with boundary conditions
cs = CubicSpline(x, y, bc_type='natural')
y_fine = cs(x_fine)
y_deriv = cs(x_fine, 1)  # first derivative

# RBF interpolation for scattered data
rbf = RBFInterpolator(points, values, kernel='thin_plate_spline', smoothing=0.1)
result = rbf(query_points)
```

### Numerical Integration (Quadrature)
- **1D**: `quad` (adaptive Gauss-Kronrod), `fixed_quad`, `romberg`
- **Multi-dimensional**: `dblquad`, `tplquad`, `nquad`
- **Monte Carlo**: Importance sampling, stratified, quasi-Monte Carlo (Sobol, Halton)
- **Oscillatory integrals**: Filon, Levin, steepest descent
- **Gauss quadrature**: Legendre, Laguerre, Hermite nodes/weights

```python
from scipy.integrate import quad, dblquad
from scipy.stats import qmc

# Adaptive quadrature with error estimate
result, error = quad(lambda x: np.exp(-x**2), -np.inf, np.inf)

# Quasi-Monte Carlo integration (high dimension)
sampler = qmc.Sobol(d=10, scramble=True)
points = sampler.random_base2(m=16)  # 2^16 points
estimate = np.mean(f(points)) * volume
```

### Root Finding & Optimization
- **Scalar**: `brentq`, `ridder`, `newton` (with derivatives)
- **Multivariate**: `fsolve`, `root` (hybr, lm, krylov)
- **Minimization**: `minimize` (Nelder-Mead, BFGS, L-BFGS-B, trust-constr)
- **Global**: `differential_evolution`, `dual_annealing`, `shgo`, `basinhopping`
- **Constrained**: SLSQP, trust-constr with bounds and linear/nonlinear constraints

```python
from scipy.optimize import root, minimize, differential_evolution

# Newton-Krylov for large nonlinear systems
sol = root(F, x0, method='krylov', options={'fatol': 1e-12})

# Constrained minimization
bounds = [(0, None)] * n  # non-negative
constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
result = minimize(objective, x0, method='SLSQP',
                  bounds=bounds, constraints=constraints)
```

### FFT & Spectral Analysis
- **FFT**: `scipy.fft.fft`, `rfft`, `fft2`, `fftn` — real/complex, multidimensional
- **Convolution**: `fftconvolve`, overlap-add for long signals
- **Power spectral density**: Welch, periodogram, multitaper
- **Filtering**: Butterworth, Chebyshev, FIR design via `scipy.signal`

### Stability & Error Analysis
- **Floating-point**: IEEE 754, catastrophic cancellation, Kahan summation
- **Conditioning**: Forward/backward error, condition number analysis
- **Convergence**: Richardson extrapolation, order verification
- **A-stability**: Absolute stability regions for time integrators
- **Grid convergence**: GCI (Grid Convergence Index), manufactured solutions

### JAX for Differentiable Numerics
- **Autodiff through solvers**: `jax.grad` of ODE solutions, implicit differentiation
- **JIT compilation**: `jax.jit` for tight numerical loops
- **Vectorization**: `jax.vmap` for parameter sweeps
- **GPU acceleration**: Same code on CPU/GPU/TPU

```python
import jax
import jax.numpy as jnp
from jax import jit, vmap, grad

@jit
def rk4_step(f, t, y, dt):
    k1 = f(t, y)
    k2 = f(t + dt/2, y + dt/2 * k1)
    k3 = f(t + dt/2, y + dt/2 * k2)
    k4 = f(t + dt, y + dt * k3)
    return y + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# Gradient of solution w.r.t. parameters
def solve_and_loss(params):
    y = integrate(f_param(params), y0, t_span)
    return jnp.sum((y - y_obs)**2)

grad_loss = grad(solve_and_loss)
```

## Decision Framework

| Problem | Method | Library |
|---------|--------|---------|
| Dense linear system (n < 10K) | LU / Cholesky | `scipy.linalg` |
| Sparse linear system | CG / GMRES + preconditioner | `scipy.sparse.linalg` |
| Non-stiff ODE | RK45 / DOP853 | `scipy.integrate.solve_ivp` |
| Stiff ODE | Radau / BDF | `scipy.integrate.solve_ivp` |
| Elliptic PDE | FEM (FEniCS) or spectral | FEniCSx / Dedalus |
| Parabolic PDE | Method of Lines + BDF | SciPy + FD/FEM |
| Hyperbolic PDE | WENO / DG | Custom / Clawpack |
| Smooth interpolation | Cubic splines | `scipy.interpolate` |
| Scattered data | RBF | `scipy.interpolate.RBFInterpolator` |
| High-dim integration | Quasi-Monte Carlo | `scipy.stats.qmc` |
| Global optimization | Differential evolution | `scipy.optimize` |
| Differentiable numerics | Autodiff solvers | JAX / Diffrax |

## Best Practices

1. **Always check conditioning** before solving linear systems
2. **Use appropriate tolerances**: `rtol` for relative, `atol` for absolute
3. **Verify convergence order** with manufactured solutions
4. **Profile before optimizing**: `%timeit`, `line_profiler`
5. **Prefer vectorized NumPy** over Python loops
6. **Use sparse formats** when fill ratio < 10%
7. **Monitor energy/mass conservation** in physical simulations
8. **Document numerical parameters**: grid size, time step, tolerances

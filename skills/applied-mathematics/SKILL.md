---
name: Applied Mathematics
description: Pure and applied mathematics for engineering and science. Calculus, real/complex analysis, abstract algebra, topology, probability theory, information theory, dynamical systems, and mathematical proof techniques.
---

# Applied Mathematics

Expert in mathematical reasoning, proof construction, and applied mathematical frameworks for engineering and scientific computing.

## Core Domains

### Calculus & Analysis
- **Real Analysis**: Limits, continuity, uniform convergence, measure theory, Lebesgue integration
- **Complex Analysis**: Cauchy integral theorem, residues, conformal mapping, analytic continuation
- **Functional Analysis**: Banach/Hilbert spaces, operator theory, spectral theory, distributions
- **Variational Calculus**: Euler-Lagrange equations, Hamiltonian mechanics, optimal control

```python
import sympy as sp

x, t, lambda_ = sp.symbols('x t lambda')

# Euler-Lagrange equation from Lagrangian
y = sp.Function('y')
L = sp.Rational(1, 2) * y(x).diff(x)**2 - sp.Rational(1, 2) * y(x)**2
EL = sp.euler_equations(L, y(x), x)
print("Euler-Lagrange:", EL)  # y'' + y = 0

# Residue computation
f = 1 / (sp.sin(x) * x**2)
res = sp.residue(f, x, 0)
print("Residue at 0:", res)
```

### Linear Algebra (Theoretical)
- **Vector spaces**: Basis, dimension, dual spaces, quotient spaces
- **Spectral theory**: Eigendecomposition, SVD, Jordan normal form
- **Matrix analysis**: Norms, positive definiteness, matrix exponential
- **Tensor algebra**: Multilinear maps, Einstein notation, tensor decomposition
- **Numerical linear algebra**: Conditioning, backward stability, Krylov methods

```python
import numpy as np
from scipy.linalg import expm, logm, sqrtm

# Matrix exponential (exact for matrix ODE: dy/dt = Ay)
A = np.array([[0, 1], [-1, 0]])  # rotation
exp_A = expm(A * t_val)  # solution: y(t) = exp(At) @ y0

# Tensor decomposition (CP/Tucker)
# For higher-order data analysis
import tensorly
from tensorly.decomposition import tucker
core, factors = tucker(tensor, rank=[3, 3, 3])
```

### Probability & Stochastic Processes
- **Measure-theoretic probability**: σ-algebras, conditional expectation, martingales
- **Stochastic processes**: Brownian motion, Poisson processes, Markov chains
- **Stochastic calculus**: Itô integral, Itô's lemma, SDE discretization (Euler-Maruyama)
- **Random matrix theory**: Wigner semicircle, Marchenko-Pastur, Tracy-Widom
- **Bayesian inference**: Conjugate priors, MCMC theory, variational inference

```python
import numpy as np

def euler_maruyama(f, g, y0, t_span, dt, n_paths=1000):
    """Solve SDE: dY = f(Y)dt + g(Y)dW via Euler-Maruyama."""
    t = np.arange(t_span[0], t_span[1], dt)
    n = len(t)
    Y = np.zeros((n_paths, n))
    Y[:, 0] = y0
    sqrt_dt = np.sqrt(dt)
    for i in range(n - 1):
        dW = np.random.randn(n_paths) * sqrt_dt
        Y[:, i+1] = Y[:, i] + f(Y[:, i]) * dt + g(Y[:, i]) * dW
    return t, Y

# Geometric Brownian Motion (Black-Scholes)
mu, sigma, S0 = 0.05, 0.2, 100
t, paths = euler_maruyama(
    f=lambda S: mu * S,
    g=lambda S: sigma * S,
    y0=S0, t_span=(0, 1), dt=0.001
)
```

### Dynamical Systems & Chaos
- **Phase portrait analysis**: Fixed points, stability classification, bifurcation
- **Lyapunov exponents**: Maximal Lyapunov exponent, Lyapunov spectrum
- **Bifurcation theory**: Saddle-node, Hopf, period-doubling, codimension-2
- **Ergodic theory**: Invariant measures, mixing, Poincaré recurrence
- **Control theory**: Controllability, observability, LQR, Kalman filter

```python
import numpy as np
from scipy.integrate import solve_ivp

def lyapunov_exponent(f, jac, y0, T, dt=0.01):
    """Compute maximal Lyapunov exponent via QR method."""
    n = len(y0)
    Q = np.eye(n)
    lyap = np.zeros(n)
    t = 0
    y = np.array(y0, dtype=float)
    n_steps = int(T / dt)
    
    for _ in range(n_steps):
        # Integrate state
        y = y + f(0, y) * dt  # Euler (use RK4 for production)
        # Integrate tangent linear
        J = jac(0, y)
        Q = Q + J @ Q * dt
        # QR reorthogonalize periodically
        Q, R = np.linalg.qr(Q)
        lyap += np.log(np.abs(np.diag(R)))
        t += dt
    
    return lyap / T
```

### Information Theory
- **Entropy**: Shannon, Rényi, differential entropy, maximum entropy principle
- **Mutual information**: KL divergence, Jensen-Shannon, f-divergences
- **Rate-distortion theory**: Lossy compression bounds
- **Coding theory**: Hamming, Reed-Solomon, LDPC, turbo codes
- **Applications**: Feature selection, ICA, information bottleneck

```python
from scipy.stats import entropy
from scipy.special import rel_entr
import numpy as np

# KL divergence (discrete)
p = np.array([0.4, 0.3, 0.2, 0.1])
q = np.array([0.25, 0.25, 0.25, 0.25])
kl_div = np.sum(rel_entr(p, q))

# Mutual information estimation (k-NN, continuous)
from sklearn.feature_selection import mutual_info_regression
mi = mutual_info_regression(X, y, n_neighbors=5)
```

### Abstract Algebra & Number Theory
- **Group theory**: Symmetry groups, group actions, Burnside's lemma
- **Ring theory**: Ideals, polynomial rings, Gröbner bases
- **Number theory**: Primality testing, modular arithmetic, elliptic curves
- **Combinatorics**: Generating functions, Pólya enumeration, graph theory
- **Coding applications**: Error correction, cryptography foundations

```python
import sympy as sp
from sympy import isprime, nextprime, factorint, mod_inverse
from sympy.combinatorics import PermutationGroup, Permutation

# Gröbner basis computation
x, y, z = sp.symbols('x y z')
I = [x**2 + y - 1, x + y**2 - 1]
gb = sp.groebner(I, x, y, order='lex')
print("Gröbner basis:", gb)

# Elliptic curve arithmetic
from sympy import EllipticCurve
E = EllipticCurve(0, 7)  # y² = x³ + 7
```

### Graph Theory & Combinatorial Optimization
- **Graph algorithms**: Shortest path, max flow, matching, coloring
- **Spectral graph theory**: Graph Laplacian, Cheeger inequality, spectral clustering
- **Network analysis**: Centrality, community detection, random graphs
- **Combinatorial optimization**: TSP, knapsack, scheduling, branch-and-bound

```python
import networkx as nx
import numpy as np

G = nx.karate_club_graph()

# Spectral analysis
L = nx.normalized_laplacian_matrix(G).toarray()
eigenvalues = np.sort(np.linalg.eigvalsh(L))
algebraic_connectivity = eigenvalues[1]  # Fiedler value

# Community detection via spectral clustering
from sklearn.cluster import SpectralClustering
sc = SpectralClustering(n_clusters=2, affinity='precomputed')
labels = sc.fit_predict(nx.to_numpy_array(G))
```

### Differential Geometry & Topology
- **Manifolds**: Charts, tangent spaces, differential forms
- **Riemannian geometry**: Metric tensors, geodesics, curvature
- **Topological data analysis (TDA)**: Persistent homology, Betti numbers, Vietoris-Rips
- **Applications**: Shape analysis, dimensionality reduction (UMAP), physics

```python
# Persistent homology with ripser
from ripser import ripser
from persim import plot_diagrams
import numpy as np

# Point cloud on a torus
theta = np.random.uniform(0, 2*np.pi, 200)
phi = np.random.uniform(0, 2*np.pi, 200)
R, r = 3, 1
X = np.column_stack([
    (R + r*np.cos(phi)) * np.cos(theta),
    (R + r*np.cos(phi)) * np.sin(theta),
    r * np.sin(phi)
])

diagrams = ripser(X, maxdim=2)['dgms']
plot_diagrams(diagrams, show=True)
# Expect: 1 H0 component, 2 H1 loops, 1 H2 void
```

## Mathematical Proof Patterns

### Proof Techniques
1. **Direct proof**: Assume hypothesis → derive conclusion
2. **Contradiction**: Assume negation → derive contradiction
3. **Induction**: Base case + inductive step (strong/structural variants)
4. **Contrapositive**: Prove ¬Q → ¬P instead of P → Q
5. **Construction**: Exhibit explicit example satisfying claim
6. **Pigeonhole**: n+1 objects in n boxes → some box has ≥2

### LaTeX Integration
```latex
\begin{theorem}[Convergence of Newton's Method]
Let $f \in C^2[a,b]$ with simple root $x^*$. If $x_0$ is sufficiently 
close to $x^*$ and $f'(x^*) \neq 0$, then Newton's method converges 
quadratically:
\[
|x_{n+1} - x^*| \leq C |x_n - x^*|^2, \quad 
C = \frac{\|f''\|_\infty}{2|f'(x^*)|}
\]
\end{theorem}
```

## Decision Framework

| Problem Domain | Key Tools | Libraries |
|---|---|---|
| Symbolic math | CAS, simplification | SymPy, Mathematica |
| Numerical linear algebra | LU, QR, SVD, iterative | NumPy, SciPy, PETSc |
| ODEs/SDEs | RK, BDF, Euler-Maruyama | SciPy, Diffrax, DifferentialEquations.jl |
| PDEs | FEM, spectral, FD | FEniCSx, Dedalus, Firedrake |
| Graph theory | Spectral, flow, matching | NetworkX, igraph, graph-tool |
| Topology (TDA) | Persistent homology | Ripser, GUDHI, giotto-tda |
| Optimization | Convex, nonlinear, MILP | CVXPY, SciPy, Gurobi, PuLP |
| Probability/Stats | MCMC, variational | PyMC, Stan, NumPyro |
| Tensor computation | Decomposition, contraction | TensorLy, opt_einsum, JAX |

## Best Practices

1. **State assumptions clearly**: Domain, smoothness, boundedness
2. **Check dimensions**: Physical units and tensor ranks must be consistent
3. **Verify edge cases**: Empty sets, degenerate matrices, boundary conditions
4. **Use exact arithmetic** (SymPy) for symbolic derivation, float for numerics
5. **Convergence tests**: Always verify with known analytical solutions
6. **Cite theorems**: Reference standard results (e.g., Lax-Milgram, Banach fixed-point)

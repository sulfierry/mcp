---
name: Finite Element Methods
description: Finite Element Method (FEM) for engineering and science. Weak formulations, mesh generation, element types, assembly, solvers, error estimation, and production FEM with FEniCSx, Firedrake, and deal.II.
---

# Finite Element Methods

Expert in Finite Element Analysis (FEA) for structural mechanics, heat transfer, fluid dynamics, and electromagnetics.

## Core Competencies

### Mathematical Foundation
- **Weak (variational) formulation**: Multiply by test function, integrate by parts
- **Galerkin method**: Approximate solution in finite-dimensional subspace
- **Sobolev spaces**: H¹, H(div), H(curl) — function space selection
- **Lax-Milgram theorem**: Existence and uniqueness for coercive bilinear forms
- **Céa's lemma**: Best approximation property of Galerkin solutions

```
Strong form:  -∇·(κ∇u) = f  in Ω,  u = g on ∂Ω_D,  κ∇u·n = h on ∂Ω_N

Weak form:    Find u ∈ V_g such that
              a(u,v) = L(v)  ∀v ∈ V_0
              where a(u,v) = ∫_Ω κ∇u·∇v dx
                    L(v) = ∫_Ω fv dx + ∫_{∂Ω_N} hv ds
```

### Element Types & Function Spaces
| Element | Continuity | Degree | Use Case |
|---------|-----------|--------|----------|
| Lagrange (CG) | C⁰ | 1-5 | Standard elliptic/parabolic |
| Discontinuous Galerkin (DG) | None | 0-5 | Advection-dominated, sharp fronts |
| Raviart-Thomas (RT) | H(div) | 1-3 | Mixed Poisson, Darcy flow |
| Nédélec | H(curl) | 1-3 | Maxwell's equations |
| Taylor-Hood (P2/P1) | C⁰ | 2/1 | Stokes/Navier-Stokes |
| Mini (P1+bubble/P1) | C⁰ | 1 | Stokes (inf-sup stable) |
| Crouzeix-Raviart | Nonconforming | 1 | Stokes, elasticity |

### FEniCSx (DOLFINx) — Production FEM
```python
import dolfinx
from dolfinx import fem, mesh, io
from dolfinx.fem.petsc import LinearProblem
import ufl
from mpi4py import MPI
import numpy as np

# Create mesh
domain = mesh.create_unit_square(MPI.COMM_WORLD, 64, 64, mesh.CellType.triangle)
V = fem.functionspace(domain, ("Lagrange", 2))

# Define variational problem
u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)
f = fem.Constant(domain, -6.0)

a = ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = f * v * ufl.dx

# Boundary conditions
def boundary_D(x):
    return np.isclose(x[0], 0) | np.isclose(x[0], 1)

u_D = fem.Function(V)
u_D.interpolate(lambda x: 1 + x[0]**2 + 2*x[1]**2)
bc = fem.dirichletbc(u_D, fem.locate_dofs_geometrical(V, boundary_D))

# Solve
problem = LinearProblem(a, L, bcs=[bc], petsc_options={"ksp_type": "preonly", "pc_type": "lu"})
uh = problem.solve()

# Export to ParaView
with io.XDMFFile(domain.comm, "solution.xdmf", "w") as xdmf:
    xdmf.write_mesh(domain)
    xdmf.write_function(uh)
```

### Nonlinear Problems (Newton)
```python
import dolfinx
from dolfinx import fem, mesh
from dolfinx.fem.petsc import NonlinearProblem
from dolfinx.nls.petsc import NewtonSolver
import ufl
from mpi4py import MPI

domain = mesh.create_unit_square(MPI.COMM_WORLD, 32, 32)
V = fem.functionspace(domain, ("Lagrange", 1))

u = fem.Function(V)
v = ufl.TestFunction(V)

# Nonlinear residual: -Δu + u³ = f
F = ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx + u**3 * v * ufl.dx - f * v * ufl.dx

problem = NonlinearProblem(F, u, bcs=[bc])
solver = NewtonSolver(MPI.COMM_WORLD, problem)
solver.convergence_criterion = "incremental"
solver.rtol = 1e-8
solver.max_it = 50
solver.solve(u)
```

### Time-Dependent Problems
```python
# Heat equation: ∂u/∂t - κΔu = f (implicit Euler)
dt = 0.01
u_n = fem.Function(V)  # solution at previous time step
u_n.interpolate(initial_condition)

a = u * v * ufl.dx + dt * kappa * ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = u_n * v * ufl.dx + dt * f * v * ufl.dx

for t_step in range(num_steps):
    problem = LinearProblem(a, L, bcs=[bc])
    uh = problem.solve()
    u_n.x.array[:] = uh.x.array[:]
```

### Mesh Generation
- **Gmsh**: Complex geometries, CAD import, structured/unstructured
- **Built-in**: `mesh.create_unit_square`, `create_box`, `create_interval`
- **Adaptive mesh refinement (AMR)**: Error indicators → mark → refine

```python
import gmsh

gmsh.initialize()
gmsh.model.occ.addDisk(0, 0, 0, 1, 1)  # unit disk
gmsh.model.occ.synchronize()
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 0.05)
gmsh.model.mesh.generate(2)

# Import into DOLFINx
from dolfinx.io import gmshio
domain, cell_tags, facet_tags = gmshio.model_to_mesh(
    gmsh.model, MPI.COMM_WORLD, 0, gdim=2
)
gmsh.finalize()
```

### Error Estimation & Adaptivity
- **A priori**: ‖u - uₕ‖ ≤ C h^{p+1} |u|_{H^{p+1}} (smooth solutions)
- **A posteriori**: Residual-based, recovery-based (ZZ), goal-oriented
- **Convergence rates**: h-refinement (mesh), p-refinement (degree), hp-refinement

### Applications

| Domain | Equation | Elements | Key Issues |
|--------|----------|----------|------------|
| Heat transfer | Poisson/diffusion | CG Lagrange | Conductivity jumps |
| Structural mechanics | Linear elasticity | CG (vector) | Locking, mixed methods |
| Fluid dynamics | Navier-Stokes | Taylor-Hood P2/P1 | Inf-sup, stabilization |
| Electromagnetics | Maxwell | Nédélec edge | Curl-conforming spaces |
| Porous media | Darcy flow | RT + DG | Mass conservation |
| Acoustics | Helmholtz | CG high-order | Pollution effect |

## Best Practices

1. **Verify with manufactured solutions** before applying to real problems
2. **Check inf-sup stability** for mixed formulations (Stokes, Darcy)
3. **Use appropriate solvers**: Direct (LU) for small, iterative (CG/GMRES + AMG) for large
4. **Monitor mesh quality**: Aspect ratio, skewness, minimum angle
5. **Dimensional analysis**: Non-dimensionalize before discretization
6. **Convergence study**: Plot error vs h on log-log, verify expected slope
7. **Parallel scaling**: Use `mpi4py` + PETSc for HPC deployments

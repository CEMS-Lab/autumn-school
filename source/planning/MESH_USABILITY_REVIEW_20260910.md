# Mesh workflow: teaching usability review

Issue: [#5](https://github.com/CEMS-Lab/autumn-school/issues/5). Date: 10 September 2026.

## Finding

The current first practical's mesh code cell combines coordinate/connectivity
construction, NPZ save/reload, equality/index validation and FEMMesh creation.
These are useful implementation details, but their combined presentation makes
the first mesh appear harder to create than the public interface requires.

The installed public snapshot supports loading a compatible Gmsh file directly:

```python
import torch
from phast import FEMMesh

mesh = FEMMesh("specimen.msh", device="cpu", dtype=torch.float64)
```

This example assumes a valid existing file. The API was source-inspected in
`vendor/PhAST/src/phast/core/mesh.py`; a new imported teaching case still requires
execution and validation. The snapshot also includes Gmsh-backed geometry
generators, including `miehe_tension` and `square_plate`.

## Reference teaching patterns

- [FEniCSx membrane tutorial](https://jsdokken.com/dolfinx-tutorial/chapter1/membrane_code.html):
  separate geometry creation, physical tags, mesh generation and solver import.
- [JAX-FEM quickstart](https://deepmodeling.github.io/jax-fem/guide/Quickstart.html):
  create a rectangular mesh using a short helper, construct the solver mesh,
  and explain boundary conditions in the next section.
- [Gmsh manual](https://gmsh.info/doc/texinfo/gmsh.html): use named physical
  groups and the standard mesh generation/export workflow.

These public sources were inspected for their teaching sequence. No third-party
notebooks or figures were copied into the course.

## Next implementation checklist

- [ ] Keep the current tested rectangular case and its exact node/connectivity
      arrays while shortening the visible mesh cell to parameters, generation
      or import, and inspection. Use a clearly identified course helper.
- [ ] Move NPZ round-trip, index checks and source provenance into the helper
      or an optional implementation section. Keep the checks active.
- [ ] Separate initial damage, material/loading and mesh plotting into short
      adjacent cells with defined quantities and physical boundary names.
- [ ] Add a standard Gmsh → `.msh` → `FEMMesh` activity and a pre-generated mesh
      fallback. Check Colab installation and setup separately from simulation.
- [ ] Test named physical groups, area, element count and initial damage seed.
      The current reader takes the first supported 2D cell block, so use a
      single surface block initially and validate multipart imports separately.
- [ ] Regenerate study/solution/HTML variants, rerun the full changed practical
      under 300 seconds, and inspect the same fields and response plots.

## Physical and derivative conventions to preserve

The current calculation uses a continuous 4 × 2 rectangle with a centreline
damage seed held at d = 1. The Miehe generator creates a geometric V-notch in a
square; substituting it changes the physical problem. An unstructured mesh
needs an embedded/tagged seed line to supply the required initial nodes.

`identify_boundaries()` detects axis-aligned extrema; physical names provide a
more general geometry interface. `from_tensors()` detaches coordinates, so
manual coordinate construction does not establish geometry differentiability.

This is a diagnostic and implementation plan. The published practical retains
its tested calculation until the revised workflow passes the checks above.

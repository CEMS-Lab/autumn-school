# Additional fracture notebooks

The primary classroom route starts at
`../classroom/01_simulate_fracture.ipynb`: one short dynamic B3 plate
calculation, followed by the gradient and learning practicals.

`01_dynamic_plate_crossing.ipynb` is the standalone form of the same B3
lesson. Its final local candidate ran all nine code cells, figures, a
40-frame GIF and a results table in 27.33 seconds under the 120-second
whole-process gate. The portable inputs are in
`../../configs/day2_forward/b3_classroom/`; the inspected implementation is
`../day2_helpers/dynamic_practical.py`.

`reference_quasistatic_diffuse_damage_20260911.ipynb` preserves the preceding
executed two-load quasistatic practical exactly. It is an archival reference,
outside the three-notebook classroom execution route. Its SHA256 is
`9dfc9b355eeced35126a114051e4a4c44c73b879e35a5e609de5fcf4b2b8a148`.
The former configuration, result arrays and helper remain available unchanged.

The classroom generator's `build_simulation` function authors the current
dynamic practical; `build_quasistatic_reference` preserves the previous
authoring function. P1-R01 and P1-A01 continue to identify the propagation
example and geometry-to-damage animation. The prior P1 register contained
those two IDs.

Fresh classroom execution and output/variant generation follow intentional
source changes. Authenticated Colab timing and spatial mesh refinement are
separate checks from these local runtime and residual measurements.

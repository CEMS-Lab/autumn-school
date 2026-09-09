# Self-contained inverse notebook: draft review

Related course issues: #11 and #13. Actual fracture-inverse work remains #7.

This topic branch preserves the existing published course and its main
navigation. It adds an isolated inverse teaching extension for review.
No private paper source, solver modifications or private fracture arrays are
included. The notebook contains original explanations, all numerical/plotting
code, 20 worked answers and eight freshly executed plot outputs.

## Current verification

- The expanded seven-example notebook passed all 26 HPC checks.
- All 16 code cells executed; all eight plots have native cell outputs.
- Whole-notebook time was 8.56 seconds including kernel startup, excluding
  queue wait, installation and HTML rendering. The public receipt records hashes.
- Independent source-primitive checks also passed, retained privately;
  those are not whole-trajectory gradient verification.
- The extended HTML passed 20 offline desktop/mobile page checks.
- Full fracture recovery, GNN training and probabilistic fracture inference
  are outside the executed teaching-example scope.

## Before integration

1. Review the new history lesson and public execution receipt.
2. Keep the hard-forward/sigmoid-backward rule labelled as a surrogate.
3. Preserve the private failure log from the earlier pre-execution quota issue.
4. Integrate with the main curriculum through the publication owner.

The draft has not been pushed or merged. Published v0.1.0/v0.1.1 are unchanged.
The standalone preview reuses the published book's MathJax/static assets;
these are not duplicated in this source subtree.

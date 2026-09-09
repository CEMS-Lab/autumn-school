# Self-contained inverse notebook: draft review

Related course issues: #11 and #13. Actual fracture-inverse work remains #7.

This topic branch preserves the existing published course and its main
navigation. It adds an isolated inverse teaching extension for review.
No private paper source, solver modifications or private fracture arrays are
included. The notebook contains original explanations, all numerical/plotting
code, worked answers and seven hash-verified retained plots.

## Current verification

- The six original teaching calculations previously passed 15 HPC checks.
- Every code cell in the assembled notebook parses.
- The reading notebook labels its figures as retained outputs. It does not
  claim the entire notebook has been executed from top to bottom.
- A fresh whole-notebook CPU execution is queued on HPC.
- The extended HTML has passed offline desktop/mobile checks.
- Full fracture recovery, GNN training and probabilistic fracture inference
  are outside the executed six-example scope.

## Before integration

1. Retrieve the fresh executed notebook and execution receipt; verify hashes.
2. Preserve any failed execution and address genuine numerical/rendering errors.
3. Require all 15 checks, all seven native plot outputs and a whole-notebook
   runtime below 300 seconds, excluding dependency installation and queue wait.
4. Replace the retained-output reading copy only with the verified notebook.
5. Review the plots, complete derivations, solution text and public provenance.
6. Integrate with the main curriculum through the publication owner.

The draft has not been pushed or merged. The main v0.1.0 course is unchanged.
The standalone preview reuses the published book's MathJax/static assets;
these are not duplicated in this source subtree.

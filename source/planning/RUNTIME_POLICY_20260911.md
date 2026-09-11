# Classroom runtime policy: two-minute student runs

## Decision and scope

The maintainer's 11 September instruction sets a strict **whole-notebook
runtime below 120 seconds** for student calculations on laptops and Google
Colab. This supersedes the earlier 300-second computational budget. The three
classroom practicals and any extension offered as a live student run use this
budget. Historical numerical receipts remain unchanged and retain their
original measured times and conditions.

Runtime includes every cell in the selected activity, solver work, training,
validation, tables, figures and animation rendering. A complete execution is
measured from launching the notebook worker through its exit. Runtime after
setup and the setup cell time may also be reported for interpretation.

## Execution and acceptance gates

| Item | Current requirement |
| --- | --- |
| Complete student run | Less than 120 seconds |
| Local design target | At most 60 seconds, leaving headroom for slower hosts |
| Individual cell timeout | 110 seconds |
| Notebook worker timeout | 115 seconds |
| Worker termination | Two-second graceful stop, then a two-second forced-stop grace period |
| Numerical checks | Retain the relevant residual, admissibility, derivative or reload checks |
| Course examples | Reduce workload and mesh size while retaining an interpretable result |

`scripts/run_classroom.py`, `scripts/run_course.py` and
`scripts/execute_visual_review.py` enforce the worker and cell caps. A worker
that exceeds the complete-run threshold receives
`timed_out` status even if its process returns a successful exit code. Receipts
record `under_120_seconds`, the 120-second acceptance limit and both timeout
settings. The legacy `under_300_seconds` field supports old report consumers;
current acceptance uses the 120-second field and measured duration.

`scripts/check_classroom_curation.py` and
`source/book/scripts/build_classroom_pages.py` require passing executions below
120 seconds before validating or preparing the classroom edition. Older
receipts can be assessed using their recorded whole-process times without
changing the original evidence. Changed computation still requires a fresh
execution and matching source/helper hashes.

## Colab rehearsal and installation

The engineering target applies to a **pre-provisioned runtime** with the course
dependencies available. Downloading the course and installing dependencies in
a cold Colab session are measured separately because network and package-server
latency vary. The student-facing setup instructions should make both timings
visible and offer retained outputs while setup completes.

Fresh authenticated Colab receipts are required before describing an activity
as Colab-certified under two minutes. Record the notebook revision, dependency
versions, CPU/GPU identity, setup time, complete execution time, numerical checks
and rendered output review. Local timing and hard timeout guards establish local
execution evidence and resource bounds; Colab timing is established by the
Colab rehearsal itself.

Larger research demonstrations can be included as recorded videos with their
original runtime and source identified. Keep these exhibits distinct from the
timed student-computation route.

## Ownership and follow-up

- Runtime gate implementation: the three runners, the classroom checker and the
  classroom page builder listed above.
- Notebook contributors: reduce the selected problem, retain scientific
  checks, and supply fresh complete-run receipts with visual outputs.
- Course integration: update the top-level plans and linked runtime issue
  [#10](https://github.com/CEMS-Lab/autumn-school/issues/10), then rehearse the
  published revision in fresh Colab before completing its acceptance checklist.

The policy change is independent of publication. New results and notebook
editions require the usual source, numerical and rendered-deliverable checks.

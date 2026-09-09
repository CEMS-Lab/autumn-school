# Delivery and validation record

The learner-facing notebook and HTML contain the teaching material. This note
records delivery status separately from the lesson.

The latest local run used a fresh Python kernel on an arm64 macOS CPU, with
PyTorch 2.8.0, NumPy 2.2.6 and Matplotlib 3.10.8 already installed. The dependency
check took 0.000987375 seconds and used the installed packages. Whole-process
execution took 6.935439083 seconds; excluding the dependency check, the measured
runtime was 6.934451708 seconds. The automated run enabled the scientific watchdog.
All numerical assertions passed. The revised gradient-plot legend was regenerated
by this run. Every numerical array and check value matches the retained previous
execution exactly. Source, execution and rendering hashes are in the JSON receipt.

Colab was opened in the course browser on 9 September 2026. Google sign-in was
required to start a runtime. The Colab rehearsal awaits that sign-in step; the
timings above describe the local CPU execution.

To complete that rehearsal, sign in to Colab, upload the downloadable notebook,
select a CPU runtime, run the separate dependency setup, and time a complete
Run all with the optional watchdog enabled. Record installation and computation
separately, retain the executed notebook and check its figures and assertions.

The machine-readable record is `evidence/differentiability_step_by_step.json`
in the course repository. The HTML structural report is alongside this note.

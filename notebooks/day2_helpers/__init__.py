"""Small, course-owned helpers used by the UKACM day-two notebooks.

The package intentionally keeps the public PhAST forward calculation separate
from the compact inverse and learning toys.  See each notebook for the
scientific scope of the corresponding exercise.
"""

from .course_tools import (
    EXPECTED_PHAST_REVISION,
    TinyDamageMLP,
    ToyDamageAdapter,
    ToyHelmholtzProblem,
    assets_dir,
    course_root,
    import_public_phast,
    load_forward_config,
    make_toy_checkpoint,
    run_notched_tension,
)

__all__ = [
    "EXPECTED_PHAST_REVISION",
    "TinyDamageMLP",
    "ToyDamageAdapter",
    "ToyHelmholtzProblem",
    "assets_dir",
    "course_root",
    "import_public_phast",
    "load_forward_config",
    "make_toy_checkpoint",
    "run_notched_tension",
]

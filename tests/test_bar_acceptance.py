"""Analytic acceptance of the existing single-force PhAST bar lesson.

Units are N, mm and MPa. This fixed-topology test uses one homogeneous elastic
bar and a synthetic tip observation. It checks first-order differentiation.
"""
import json
from time import perf_counter

import pytest

from scripts.teaching_preflight import verify_phast_environment


@pytest.fixture(scope="module")
def bar():
    identity = verify_phast_environment()
    import phast
    import torch

    old_threads = torch.get_num_threads()
    torch.set_num_threads(1)
    mesh = phast.line_mesh(length=100.0, n_elements=10)

    def forward(E):
        return phast.solve_bar(mesh, young_modulus=E, area=10.0,
                               end_force=4000.0, left_displacement=0.0)

    print("\nPHAST_ENVIRONMENT=" + json.dumps(identity, sort_keys=True))
    try:
        with torch.sparse.check_sparse_tensor_invariants():
            yield torch, mesh, forward
    finally:
        torch.set_num_threads(old_threads)


def test_forward_displacement_reaction_and_residual(bar):
    torch, mesh, forward = bar
    result = forward(torch.tensor(210000.0, dtype=torch.float64))
    expected_u = 4000.0 * mesh.nodes / (210000.0 * 10.0)
    assert result.displacement.dtype == torch.float64
    assert result.displacement.device.type == "cpu"
    torch.testing.assert_close(result.displacement, expected_u, rtol=1e-10, atol=1e-12)
    assert result.reaction.item() == pytest.approx(-4000.0, rel=0, abs=1e-6)
    assert result.free_residual.abs().max().item() < 1e-6
    torch.testing.assert_close(result.stress, torch.full_like(result.stress, 400.0))
    print("\nBAR_FORWARD=" + json.dumps({
        "tip_mm": result.displacement[-1].item(),
        "reaction_N": result.reaction.item(),
        "max_free_residual_N": result.free_residual.abs().max().item(),
    }))


def test_tip_and_loss_derivatives(bar):
    torch, _, forward = bar
    E = torch.tensor(100000.0, dtype=torch.float64, requires_grad=True)
    tip = forward(E).displacement[-1]
    # Independent analytic observation; the load remains 4000 N.
    observed = 4000.0 * 100.0 / (210000.0 * 10.0)
    loss = ((tip-observed)/observed).square()
    dy = torch.autograd.grad(tip, E, retain_graph=True)[0]
    dloss = torch.autograd.grad(loss, E)[0]
    expected_dy = -4000.0 * 100.0 / (10.0 * E.detach().square())
    expected_dloss = 2 * (tip.detach()-observed) / observed**2 * expected_dy
    torch.testing.assert_close(dy, expected_dy, rtol=1e-12, atol=0)
    torch.testing.assert_close(dloss, expected_dloss, rtol=1e-12, atol=0)
    print("\nBAR_DERIVATIVES=" + json.dumps({
        "tip_mm_per_MPa": dy.item(), "loss_per_MPa": dloss.item(),
    }))


def test_single_force_modulus_recovery(bar):
    torch, _, forward = bar
    reference = forward(torch.tensor(210000.0, dtype=torch.float64))
    observed = reference.displacement[-1].detach()
    log_E = torch.nn.Parameter(torch.log(torch.tensor(100000.0, dtype=torch.float64)))
    optimiser = torch.optim.SGD([log_E], lr=0.1, momentum=0.5)
    history, consecutive = [], 0
    start = perf_counter()
    for update in range(81):
        optimiser.zero_grad(set_to_none=True)
        E = log_E.exp()
        prediction = forward(E).displacement[-1]
        loss = ((prediction-observed)/observed).square()
        assert bool(torch.isfinite(loss))
        history.append([update, E.item(), prediction.item(), loss.item()])
        consecutive = consecutive + 1 if loss.item() < 1e-8 else 0
        if consecutive >= 5 or update == 80:
            break
        loss.backward()
        assert log_E.grad is not None and bool(torch.isfinite(log_E.grad))
        optimiser.step()
    elapsed = perf_counter() - start
    assert consecutive >= 5, "Recovery did not meet the stated displacement tolerance."
    assert abs(history[-1][1]/210000.0-1) < 2e-4
    assert abs(history[-1][2]/observed.item()-1) < 1e-4
    recovered = forward(torch.tensor(history[-1][1], dtype=torch.float64))
    torch.testing.assert_close(recovered.displacement, reference.displacement, rtol=1e-4, atol=1e-12)
    print("\nBAR_RECOVERY=" + json.dumps({
        "modulus_GPa": history[-1][1]/1000, "updates": history[-1][0],
        "recovery_forward_evaluations": len(history), "loop_seconds": elapsed,
        "relative_modulus_error": abs(history[-1][1]/210000.0-1),
        "history_columns": ["update", "E_MPa", "tip_mm", "normalised_loss"],
        "history": history,
    }))

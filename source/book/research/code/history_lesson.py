"""Small history-rule diagnostics; execute numerical work on HPC."""

def history_rules():
    import numpy as np
    import torch

    class HardForwardSigmoidBackward(torch.autograd.Function):
        @staticmethod
        def forward(ctx, a, b, scale):
            ctx.save_for_backward(a, b)
            ctx.scale = scale
            return torch.maximum(a, b)

        @staticmethod
        def backward(ctx, upstream):
            a, b = ctx.saved_tensors
            return (upstream * torch.sigmoid(ctx.scale * (a-b)),
                    upstream * torch.sigmoid(ctx.scale * (b-a)), None)

    def custom(a, b, scale=10.0):
        return HardForwardSigmoidBackward.apply(a, b, scale)

    x = torch.linspace(.6, 1.4, 401, dtype=torch.float64, requires_grad=True)
    a = torch.ones_like(x)
    hard = torch.maximum(a, x)
    smooth = torch.logaddexp(10*a, 10*x) / 10
    proxy = custom(a, x)
    gh = torch.autograd.grad(hard.sum(), x, retain_graph=True)[0]
    gs = torch.autograd.grad(smooth.sum(), x, retain_graph=True)[0]
    gp = torch.autograd.grad(proxy.sum(), x)[0]
    tie_a = torch.tensor(1., dtype=torch.float64, requires_grad=True)
    tie_b = torch.tensor(1., dtype=torch.float64, requires_grad=True)
    ties = torch.autograd.grad(torch.maximum(tie_a, tie_b), (tie_a, tie_b))
    theta = torch.tensor(1., dtype=torch.float64, requires_grad=True)
    old_route = torch.autograd.grad(torch.maximum(2*theta, theta), theta)[0]
    b = torch.tensor(.99, dtype=torch.float64, requires_grad=True)
    one = torch.ones_like(b)
    surrogate = torch.autograd.grad(custom(one, b), b)[0].item()
    eps = 1e-6
    hard_fd = (max(1., .99+eps)-max(1., .99-eps))/(2*eps)
    smooth_fd = (np.logaddexp(10., 10*(.99+eps))-
                 np.logaddexp(10., 10*(.99-eps)))/(20*eps)
    values = [.2, .8, .4, 1.2, .7]
    routes = {}
    for label in ('hard', 'surrogate'):
        energies = torch.tensor(values, dtype=torch.float64, requires_grad=True)
        hist = torch.zeros((), dtype=torch.float64)
        for energy in energies:
            hist = torch.maximum(hist, energy) if label == 'hard' else custom(hist, energy, 4.)
        routes[label] = torch.autograd.grad(hist, energies)[0].tolist()
    repeated = [1.]
    for _ in range(40):
        repeated.append(float(np.logaddexp(10*repeated[-1], 10.)/10))
    expected = 1 + np.log(np.arange(41)+1)/10
    reference = .006
    energy_gap = .001
    weight = torch.sigmoid(torch.tensor(6*energy_gap/reference)).item()
    converted_weight = torch.sigmoid(torch.tensor(6*(energy_gap*1e6)/(reference*1e6))).item()
    saturated = torch.sigmoid(torch.tensor(-1e3, dtype=torch.float64)).item()
    checks = {
        'history_custom_forward_exact': torch.equal(hard, proxy),
        'history_hard_tie_halves': all(t.item() == .5 for t in ties),
        'history_old_route_retained': old_route.item() == 2.,
        'history_hard_losing_branch_zero': hard_fd == 0.,
        'history_surrogate_mismatch_preserved': abs(surrogate-hard_fd) > .4,
        'history_smooth_sibling_fd': abs(surrogate-smooth_fd) < 1e-8,
        'history_smooth_bias_bound': bool(torch.all(smooth-hard <= np.log(2)/10+1e-14)),
        'history_repeat_bias_formula': bool(np.allclose(repeated, expected, rtol=0, atol=1e-14)),
        'history_exact_peak_route': routes['hard'] == [0., 0., 0., 1., 0.],
        'history_unit_invariance': abs(weight-converted_weight) < 1e-14,
        'history_sigmoid_saturation_retained': saturated == 0.,
    }
    result = {
        'x': x.detach().tolist(), 'hard': hard.detach().tolist(),
        'smooth': smooth.detach().tolist(), 'hard_gradient': gh.tolist(),
        'smooth_gradient': gs.tolist(), 'surrogate_gradient': gp.tolist(),
        'energies': values, 'routes': routes, 'repeat_smooth': repeated,
        'hard_fd': hard_fd, 'surrogate': surrogate, 'smooth_fd': smooth_fd,
        'scope': 'dimensionless history primitives; not a fracture recovery',
    }
    return result, {k: bool(v) for k, v in checks.items()}


def plot_history_rules(result):
    import matplotlib.pyplot as plt
    import numpy as np
    fig, axes = plt.subplots(2, 2, figsize=(10.4, 7.7), layout='constrained')
    blue, orange, green = '#0072B2', '#D55E00', '#009E73'
    ax = axes[0, 0]
    ax.plot(result['x'], result['hard'], color=blue, label='hard / custom forward')
    ax.plot(result['x'], result['smooth'], color=orange, label='smooth forward')
    ax.set(title='(a) History value', xlabel='current energy', ylabel='new history')
    ax.legend(loc='upper left', frameon=False)
    ax = axes[0, 1]
    ax.plot(result['x'], result['hard_gradient'], color=blue, label='hard branch rule')
    ax.plot(result['x'], result['surrogate_gradient'], color=orange,
            label='sigmoid reverse weight')
    ax.set(title='(b) Local reverse rule', xlabel='current energy', ylabel='current-energy weight')
    ax.legend(loc='upper left', frameon=False)
    ax = axes[1, 0]
    steps = np.arange(1, 6)
    ax.bar(steps-.16, result['routes']['hard'], width=.3, color=blue, label='exact hard history')
    ax.bar(steps+.16, result['routes']['surrogate'], width=.3, color=green, label='surrogate history')
    ax.set(title='(c) Which earlier energy receives sensitivity?',
           xlabel='loading step', ylabel='final-history sensitivity', xticks=steps)
    ax.legend(loc='upper left', frameon=False)
    ax = axes[1, 1]
    ax.plot(np.arange(41), np.ones(41), color=blue, label='hard / custom forward')
    ax.plot(np.arange(41), result['repeat_smooth'], color=orange, label='smooth forward')
    ax.set(title='(d) Constant input, repeated updates', xlabel='history update', ylabel='stored history')
    ax.legend(loc='upper left', frameon=False)
    for ax in axes.flat:
        ax.grid(alpha=.18)
        ax.spines[['top', 'right']].set_visible(False)
    return fig

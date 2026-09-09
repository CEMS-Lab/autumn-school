# Why a fracture solver needs a memory-aware derivative

**A diffuse crack can still contain a sharp mathematical decision.** At each
material point, the solver asks: *is the current crack-driving energy larger
than anything this point has experienced before?* This short lesson follows
that decision through loading, unloading and backpropagation.

## Watch the switch

Press play. Blue is the current tensile energy; orange is its remembered
maximum. On unloading, the blue curve falls while the orange history stays.
The lower panels show the history update and its reverse weight at that step.

```{figure} visuals/history_switch.png
:width: 100%
:name: fig-history-switch
:alt: Loading history, a maximum function with a kink, and hard versus sigmoid reverse weights at a repeated maximum.

A dimensionless example at one material point. The orange marker is the
current state; the green marker is its surrogate reverse weight. The open
blue marker at a tie denotes the half-weight convention. It does not imply
a unique classical derivative there.
```

```{raw} html
<video data-visual-film="history_switch.mp4" data-poster="fig-history-switch" controls preload="none" playsinline aria-label="Nine loading steps showing history memory and reverse sensitivity" style="display:block;width:100%;aspect-ratio:11.6/7.8;background:#fff"></video>
```

{download}`Play or download the 18-second animation <visuals/history_switch.mp4>`.
Each frame is one history update; playback is slowed for reading.
The open blue point marks the half-weight convention at equality; the green
curve shows the surrogate reverse weight. Energy values are dimensionless.

## 1. Remember the largest energy

$$H_{n+1}=\max(H_n,\psi^+_{n+1}).$$

Here $H_n$ stores the previous maximum and $\psi^+$ is the current tensile
driving energy. The maximum is **continuous, with a kink at equality**.
Its current-energy partial is zero below the old maximum and one above it.
At the tie, a classical partial derivative is generally undefined.

## 2. Carry the memory backwards

Sensitivity means how much a quantity changes when an input changes slightly.
For any inverse parameter $\theta$, such as a particle coordinate,

$$
\frac{\mathrm dH_{n+1}}{\mathrm d\theta}
=w_H\frac{\mathrm dH_n}{\mathrm d\theta}
+w_\psi\frac{\mathrm d\psi^+_{n+1}}{\mathrm d\theta}.
$$

For the hard branch rule, $(w_H,w_\psi)=(1,0)$ during unloading and $(0,1)$
at a new maximum. **Unloading does not erase sensitivity:** the derivative
can still pass through the earlier history. At equality, the implementation
can assign half to each input as a convention.

## 3. What our custom PhAST rule does

PhAST offers several history choices. Its **hard-forward, sigmoid-backward**
option keeps the maximum in the forward calculation and uses

$$
\begin{aligned}
w_\psi&=\sigma\!\left(k\frac{\psi^+-H_n}{E_{\rm ref}}\right),\\
w_H&=1-w_\psi,\\
\sigma(s)&=\frac{1}{1+e^{-s}}.
\end{aligned}
$$

in reverse. The operator saves its inputs and applies these weights to the
incoming sensitivity. This is a compact vector--Jacobian product; it does
not require storing a full Jacobian matrix. The research option uses a fixed
reference energy $E_{\rm ref}$; a dimensional-scale variant also exists.
The animation uses dimensionless energies and $k=12$ to make the transition
visible, rather than a production fracture setting.

Near a switch, this is a **surrogate derivative of the hard forward map**.
A separate smooth-forward option changes the history value itself.
Neither choice guarantees a smooth derivative across competing crack paths.
Damage bounds and equilibrium solves also need their own consistent
backward rules. Our detailed chapter explains those dependencies and tests.

**Take away:** phase-field regularisation spreads a crack in space.
History differentiation carries its memory through time. These solve
different parts of the problem.

[Read the complete source-grounded explanation](03_history.md), or inspect
the {download}`Matplotlib source <code/history_animation.py>`,
{download}`tested teaching primitive <code/history_lesson.py>`,
{download}`plotted arrays <visuals/history_animation_arrays.npz>`, and
{download}`HPC checks and receipt <visuals/history_manifest.json>`.
The receipt retains the example where a hard-map finite difference is zero
and the surrogate weight is approximately $0.475$.

```{raw} html
<script>
document.querySelectorAll('video[data-visual-film]').forEach(video => {
  const name = video.dataset.visualFilm;
  const link = Array.from(document.querySelectorAll('a[href]')).find(a => a.getAttribute('href').endsWith('/' + name));
  if (link) video.src = link.href;
  const poster = document.querySelector('#' + video.dataset.poster + ' img');
  if (poster) {
    video.poster = poster.src;
    document.getElementById(video.dataset.poster).style.display = 'none';
  }
});
</script>
```

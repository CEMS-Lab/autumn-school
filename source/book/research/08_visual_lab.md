---
myst:
  all_links_external: false
---

# Watch the particle, the crack and the loss

A loss landscape assigns a height to each candidate parameter pair. Here the
horizontal coordinates are the unknown particle centre $(c_x,c_y)$ and the
height is the loss. The plate is a physical domain; the landscape is a
parameter domain. We connect the two views without confusing them.

This visual laboratory has three evidence levels: a newly computed geometry
toy, a retained 25-point FEM scan, and a retained fracture-inverse trajectory.
Each uses its own stated observations and loss. Videos start only when you
press play; their controls provide pause, seeking and fullscreen viewing.

## 1. Begin with something we can see directly

Imagine observing a soft-edged image of a circular inclusion in a 40 mm plate.
The radius is fixed at 3 mm; only its centre is unknown. This teaching example
assumes that the geometry image is measured directly. A real fracture inverse
problem observes the response of the specimen instead.

At pixel centres $\mathbf x_p$, define

$$
s_p(\mathbf c)=\frac{1}{1+\exp[(\|\mathbf x_p-\mathbf c\|-r)/\epsilon]},
\qquad
L_{\rm geom}(\mathbf c)=\frac{1}{N}\sum_p
[s_p(\mathbf c)-s_p(\mathbf c^*)]^2.
$$

We use an $80\times80$ pixel grid, $\epsilon=1.5$ mm and reference centre
$(28,23)$ mm. This explicitly smooth image makes a compact differentiable
example. It is not a stiffness field or a solution of the fracture equations.

```{figure} visuals/geometry_observation.png
:width: 100%
:name: fig-visual-geometry
:alt: Three plate images show the reference circular indicator, the offset initial indicator, and their signed residual.

The initial centre is $(34,33)$ mm. Both indicator images use the same colour
scale. The residual changes sign where the reference and trial images differ.
No crack or displacement calculation is involved in this example.
```

**Predict:** should moving the candidate circle towards the reference reduce
the mismatch? What happens to the information available far from the circle?

## 2. Lift the same loss into a landscape

```{figure} visuals/geometry_loss.png
:width: 100%
:name: fig-visual-landscape
:alt: A three-dimensional geometry-loss surface and its top-down map show the computed descent trajectory into a low-loss region.

The surface is calculated at 5,265 centre locations on a $65\times81$ grid.
The map and surface display the same untransformed loss. Orange marks a
computed descent using analytic gradients and a sufficient-decrease line
search. Surface tessellation is a rendering choice, not additional physics.
```

The algorithm does not need this entire map. At each iterate it evaluates its
current loss and gradient, proposes a direction and tests a step. We compute
the complete map afterwards to help interpret its movement. In the companion
code, an independent central-difference check tests the analytic derivative at
one stated point.

```{raw} html
<video data-visual-film="geometry_descent.mp4" data-poster="fig-visual-landscape" controls preload="none" playsinline aria-label="Geometry image and loss-surface descent animation" style="display:block;width:100%;aspect-ratio:14/6;background:#fff"></video>
```

{download}`Download the geometry descent animation <visuals/geometry_descent.mp4>`.
The two panels advance together. Each displayed state is a computed iterate;
the status line identifies its update number.

:::{admonition} What should I notice?
:class: dropdown

The candidate geometry changes on the plate while its centre moves across
parameter space. Far from overlap, the mismatch changes slowly, so a gradient
can be small even when the position error is large. Near the reference, the
loss is more informative. A line search tests whether a proposed update
actually reduces the objective.
:::

## 3. Inspect a real, sampled fracture loss

For the retained PhAST scan, each of 25 candidate centres was evaluated by a
forward fracture calculation. The observation is the damage field at step
1454. Its recorded loss is

$$
L_{\rm single}(\mathbf c)=
\frac{\sum_i[d_i(\mathbf c)-d_i^{\rm obs}]^2}
{\max(\sum_i d_i^{\rm obs},10^{-12})}.
$$

This is the archived damage-mass normalization. It differs from both the
geometry-image MSE above and the four-frame objective in the next section.

```{figure} visuals/fem_sampled_loss.png
:width: 100%
:name: fig-visual-fem-landscape
:alt: A coarse three-dimensional FEM loss surface and a five-by-five sample map mark every evaluated particle centre.

Exactly 25 retained FEM values are shown. Facets join adjacent samples;
the top-down view shows their individual values. The reference centre lies at
$(28,23)$ mm. This is a local same-basin scan, not an exhaustive global map.
No optimizer path from a different objective is superposed.
```

This surface is coarser than the geometry toy because each height requires a
fracture solve. A dense grid would cost additional solves; plotting a smooth
interpolant would not supply the missing evidence. The retained grid is useful
for comparing nearby candidates without claiming the shape between samples.

## 4. Watch a recorded particle recovery

The next case recovers two centre coordinates with radius and material
contrasts fixed. The synthetic reference centre is $(28,23)$ mm and the initial
centre is $(34,33.392)$ mm, approximately 12 mm away. The recorded calculation
uses four damage observations selected from observed damage-mass increments:
steps 1018, 1163, 1309 and 1454.

$$
L_{\rm time}(\mathbf c)=
\frac{\sum_{t\in\mathcal T}\sum_i[d_i(t;\mathbf c)-d_i^{\rm obs}(t)]^2}
{\max(\sum_{t\in\mathcal T}\sum_i d_i^{\rm obs}(t),10^{-12})}.
$$

```{figure} visuals/fem_recovery.png
:width: 100%
:name: fig-visual-recovery
:alt: Five panels compare reference damage, predicted damage, signed error, particle centre updates and the complete objective history.

Final recorded state after 20 inverse updates. The centre is approximately
$(28.080,23.034)$ mm, with a 0.087 mm centre error. The damage panels show the
last fitting frame, step 1454. Full damage values are retained; no threshold
removes diffuse damage. Particle circles and trajectories are shown separately
on a geometry plate. The signed-error scale is fixed over the entire animation.
```

```{raw} html
<video data-visual-film="fem_recovery.mp4" data-poster="fig-visual-recovery" controls preload="none" playsinline aria-label="Five-panel recorded FEM inverse recovery animation" style="display:block;width:100%;aspect-ratio:14/9;background:#fff"></video>
```

{download}`Download the recorded recovery animation <visuals/fem_recovery.mp4>`.
Each frame is a saved inverse iterate, not interpolated particle motion. The
underlying FEM damage arrays and recorded loss history are checked together
before rendering. This verifies their consistency, rather than re-verifying
the complete historical solver or its derivative.

The fixed normalized step of 0.75 mm brings the particle close to its target,
then overshoots on updates 17 and 19. The plotted history preserves those
oscillations. The reference is used to assess the result; the optimizer follows
the damage objective. The four displayed observations are fitting data, so
their agreement is not independent validation.

:::{admonition} Why does the last part of the curve oscillate?
:class: dropdown

A fixed travel distance can exceed the remaining distance to a low-loss
region. After crossing it, the gradient points back. A smaller step or an
adaptive step strategy could be tested, but this animation shows the original
recorded schedule, including its increases in loss.
:::

## 5. Separate physical time from inverse updates

```{figure} visuals/fem_time.png
:width: 100%
:name: fig-visual-time
:alt: Four reference damage fields show successive retained physical observation steps with one shared colour scale.

Four saved reference observations. Here geometry stays fixed while physical
time advances. In the inverse animation above, the observation step stays
fixed while the candidate geometry changes between forward replays.
```

```{raw} html
<video data-visual-film="fem_time.mp4" data-poster="fig-visual-time" controls preload="none" playsinline aria-label="Reference and recovered-geometry crack evolution at four retained steps" style="display:block;width:100%;aspect-ratio:10/5.3;background:#fff"></video>
```

{download}`Download the four-frame crack evolution <visuals/fem_time.mp4>`.
Playback advances through the four stored steps without synthesizing
intermediate fracture states. The screen duration is for reading; it is not
the physical time scale of the experiment.

:::{admonition} Check your interpretation
:class: dropdown

In a forward movie, the crack evolves under one specified geometry. In an
inverse movie, the geometry changes and the forward problem is solved again.
The changing particle centre represents an updated estimate, not a particle
physically translating inside the plate during fracture.
:::

## Inspect or reproduce the visuals

The {download}`Matplotlib source <code/particle_visuals.py>` computes the
geometry toy and renders the retained FEM arrays. The
{download}`artifact manifest <visuals/manifest.json>` records the input hashes,
checks, plotting versions and output hashes. Download the
{download}`geometry arrays <visuals/geometry_arrays.npz>`,
{download}`retained FEM arrays <visuals/fem_arrays.npz>` and
{download}`25-point loss grid <visuals/sampled_landscape.npz>` for inspection.
These compressed data contain the exact plotted values. The
{download}`original numerical input bundle <visuals/retained_inputs.zip>`
contains the files expected by the renderer. Extract it, then run:

```bash
python particle_visuals.py --inputs inputs --output regenerated_visuals
```

NumPy, Matplotlib and an FFmpeg executable with H.264 support are needed.
Use a new output directory to preserve earlier receipts. Research execution
for this project uses HPC. The private source-lineage map accompanies the
integration handoff; the downloadable bundle contains numerical data only.

Vector figures:
{download}`geometry observations <visuals/geometry_observation.pdf>`,
{download}`geometry landscape <visuals/geometry_loss.pdf>`,
{download}`FEM loss samples <visuals/fem_sampled_loss.pdf>`,
{download}`inverse recovery <visuals/fem_recovery.pdf>`, and
{download}`physical observation frames <visuals/fem_time.pdf>`.

Numerical generation and rendering for this laboratory run on HPC. The two
FEM examples reuse archived data. Their agreement and source-file hashes are
not a new source-locked rerun of the historical fracture calculation. All
materials form the optional inverse extension of the autumn-school book.

```{raw} html
<script>
document.querySelectorAll('video[data-visual-film]').forEach(video => {
  const name = video.dataset.visualFilm;
  const link = Array.from(document.querySelectorAll('a[href]')).find(a => a.getAttribute('href').endsWith('/' + name));
  if (link) video.src = link.href;
  const poster = document.querySelector('#' + video.dataset.poster + ' img');
  if (poster) video.poster = poster.src;
});
</script>
```

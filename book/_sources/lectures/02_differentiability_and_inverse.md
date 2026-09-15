# Lecture 2: Differentiability and inverse recovery

The forward problem predicts a mechanical response from known inputs. The inverse
problem estimates an unknown input from an observed response. Begin with the small
elastic bar, then connect the same operations to the particle-position exhibits.

## 1. State the experiment

A uniform bar has length $L=100\,\mathrm{mm}$ and area $A=10\,\mathrm{mm}^2$.
Its left end is fixed and a tensile force $F=4000\,\mathrm{N}$ acts at the right.
The unknown is the uniform Young’s modulus $E$. The observation is the tip
displacement $y_{\mathrm{obs}}$. Geometry, area and force are known independently.
This example uses linear elasticity; damage evolution belongs to the later
fracture applications.

## 2. Build and solve the forward problem with PhAST

The continuum equation and its finite-element form are

$$
\begin{aligned}
\frac{\mathrm{d}}{\mathrm{d}x}\left(EA\frac{\mathrm{d}u}{\mathrm{d}x}\right)&=0,\\
u(0)&=0,\qquad EA u'(L)=F,\\
\mathbf K_{ff}(E)\mathbf u_f&=\mathbf f_f.
\end{aligned}
$$

The subscript $f$ denotes unconstrained degrees of freedom. Ten line elements
give eleven nodes. Reuse this forward function throughout recovery:

```python
mesh = phast.line_mesh(length=100.0, n_elements=10)

def forward(E):
    return phast.solve_bar(mesh, young_modulus=E,
                           area=10.0, end_force=4000.0)
```

For this uniform bar, $u(x)=Fx/(EA)$ supplies an analytical comparison.
The notebook creates a synthetic observation with $E_{\mathrm{ref}}=210\,\mathrm{GPa}$,
giving $y_{\mathrm{obs}}\approx0.190476\,\mathrm{mm}$. Inspect nodal displacement,
reaction and the free-degree residual before beginning recovery.

## 3. Differentiate a scalar mismatch

At a trial modulus, predict $y(E)=u(L;E)$ and define

$$
\begin{aligned}
\mathcal L(E)&=\left(\frac{y(E)-y_{\mathrm{obs}}}{y_{\mathrm{obs}}}\right)^2,\\[0.5em]
\frac{\mathrm{d}\mathcal L}{\mathrm{d}E}
&=\frac{2(y-y_{\mathrm{obs}})}{y_{\mathrm{obs}}^2}\frac{\mathrm{d}y}{\mathrm{d}E},\\[0.5em]
\frac{\mathrm{d}y}{\mathrm{d}E}&=-\frac{FL}{AE^2}.
\end{aligned}
$$

The computational sequence is $E\rightarrow\mathbf u\rightarrow y\rightarrow\mathcal L$.
`loss.backward()` applies the chain rule through the recorded calculation,
including the PhAST solve. At the initial $E=100\,\mathrm{GPa}$ the bar extends
too much: increasing $E$ locally reduces the loss. One backward pass gives a
gradient at the evaluated state. Plotting the loss over a range of modulus
values requires a separate forward calculation at each value.

## 4. Let the optimiser choose the next modulus

Use $q=\log(E/E_{\mathrm{scale}})$ with $E_{\mathrm{scale}}=1\,\mathrm{MPa}$,
so $E=E_{\mathrm{scale}}\exp(q)$ remains positive. The code stores modulus
values in MPa. The Day 3 notebook uses SGD with momentum:

```python
log_E = torch.nn.Parameter(torch.log(torch.tensor(100000.)))
optimiser = torch.optim.SGD([log_E], lr=0.1, momentum=0.5)
optimiser.zero_grad()
y = forward(log_E.exp()).displacement[-1]
loss = ((y - observed) / observed)**2
loss.backward()
optimiser.step()
```

Repeat prediction, loss, backward and update until the relative tip mismatch
is below $10^{-4}$ for five consecutive evaluations, with at most 80 updates.
The force stays fixed. Momentum can produce overshoot and oscillation.
The lecture’s plain-SGD example and the notebook’s momentum example have
different histories: use the notebook’s printed result beside its own plots.

## 5. Interpret and check the result

{doc}`Lab 2 <../classroom/02_gradients_and_recovery>` contains geometry,
mesh, boundary conditions, displacement fields, a computational graph, modulus
and loss histories, and an animated recovery. Compare the recovered field with
the observed tip and analytical extension. Synthetic, noise-free data test this
implementation; experimental identification adds measurement and model uncertainty.

Finite differences and Taylor remainders are optional derivative checks:

$$
\begin{aligned}
\mathcal L'(E)&\approx\frac{\mathcal L(E+h)-\mathcal L(E-h)}{2h},\\[0.5em]
R(h)&=|\mathcal L(E+h)-\mathcal L(E)-h\mathcal L'(E)|.
\end{aligned}
$$

The first compares the gradient with nearby solves. For a smooth function and
a correct derivative, the second decreases as $h^2$ until numerical error
dominates. These checks assess a local derivative separately from the inverse loop.
The {doc}`reference derivation <../05_differentiation_and_inverse>` gives details.

## 6. Extend the same chain rule to fracture

For observations $\mathbf y(\boldsymbol\theta)$ and a symmetric positive-semidefinite
weighting matrix $\mathbf W$,

$$
\begin{aligned}
\mathcal L&=\tfrac12(\mathbf y-\mathbf y_{\mathrm{obs}})^T
\mathbf W(\mathbf y-\mathbf y_{\mathrm{obs}}),\\[0.5em]
\nabla_{\boldsymbol\theta}\mathcal L
&=\mathbf J^T\mathbf W(\mathbf y-\mathbf y_{\mathrm{obs}}),\\[0.5em]
\mathbf J&=\frac{\partial\mathbf y}{\partial\boldsymbol\theta}.
\end{aligned}
$$

This vector–Jacobian product combines the sensitivity of each observation into
a gradient of the scalar loss. For an implicitly solved equilibrium equation,
write the force residual as $\mathbf R(\mathbf u,\boldsymbol\theta)=0$.
If the residual is differentiable and its displacement Jacobian is invertible,
differentiating this equation locally gives

$$
\mathbf R_{\mathbf u}\frac{\partial\mathbf u}{\partial\boldsymbol\theta}
=-\mathbf R_{\boldsymbol\theta}.
$$

For evolving fracture, sensitivities also pass through earlier states, history
and damage updates. Shared parameters contribute at each use. Particle-position
recovery replaces $E$ with inclusion coordinates and the tip measurement with
selected field observations. Assess sensitivity, initialisation, active
constraints and non-uniqueness for that problem. The
{doc}`inverse visual laboratory <../research/08_visual_lab>`
provides additional reading; these larger studies are separate from the bar practical.

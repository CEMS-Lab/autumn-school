"""Original LaTeX-style equation assets and the actual teaching BC schematic.

No simulation is performed. Equations are SVG paths with PNG fallbacks;
the LaTeX strings below remain the editable source.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / 'assets'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'mathtext.fontset': 'stix', 'svg.fonttype': 'path',
                     'font.family': 'DejaVu Sans', 'font.size': 22})
EQUATIONS = {
 'damage_convention': r'd=0:\ \mathrm{intact}\qquad\qquad d=1:\ \mathrm{fully\ damaged}',
 'state_zero': r'\mathrm{Initial\ state}\quad z_0',
 'state_one': r'\mathrm{Updated\ state}\quad z_1',
 'state_final': r'\mathrm{Final\ state}\quad z_N',
 'diffusion_glossary': r'q:\ \mathrm{scalar}\qquad\alpha:\ \mathrm{diffusivity}\qquad\Delta t,\Delta x:\ \mathrm{fixed\ step\ sizes}',
 'energy': r'\Pi(u,d)=\int_\Omega g(d)\,\psi_0(\varepsilon(u))\,\mathrm{d}x + G_c\,\Gamma_\ell(d)-W_{\mathrm{ext}}(u)',
 'crack_cost': r'\Gamma_\ell(d)=\frac{1}{2}\int_\Omega\left(\frac{d^2}{\ell}+\ell\,|\nabla d|^2\right)\mathrm{d}x',
 'degradation': r'g(d)=(1-\eta)(1-d)^2+\eta',
 'local_gradient': r"g'(d)=-2(1-\eta)(1-d)",
 'state_step': r'z_{n+1}=S_n(z_n,p),\qquad J=\frac{1}{2}\|Cz_N-y_\star\|^2',
 'diffusion': r'q_i^{n+1}=q_i^n+\frac{\alpha\,\Delta t}{\Delta x^2}\left(q_{i-1}^n-2q_i^n+q_{i+1}^n\right)',
 'adjoint': r'\lambda_N=C^{\mathsf{T}}(Cz_N-y_\star),\qquad\lambda_n=A_n^{\mathsf{T}}\lambda_{n+1}',
 'jacobians': r'A_n=\frac{\partial S_n}{\partial z_n},\qquad B_n=\frac{\partial S_n}{\partial p}',
 'gradient_sum': r'\frac{\mathrm{d}J}{\mathrm{d}p}=\sum_{n=0}^{N-1}B_n^{\mathsf{T}}\lambda_{n+1}',
 'finite_difference': r'\frac{\mathrm{d}J}{\mathrm{d}p}\approx\frac{J(p+h)-J(p-h)}{2h}',
 'implicit': r'R(z,p)=0,\quad R_z^{\mathsf{T}}\lambda=\nabla_z J,\quad\nabla_p J_{\mathrm{total}}=\nabla_p J-R_p^{\mathsf{T}}\lambda',
 'hybrid': r'z_{n+1}=S\!\left(z_n,\,f_\theta(\xi_n)\right)',
 'loading': r'u_y^{\mathrm{top}}=+0.02\,\lambda,\qquad u_y^{\mathrm{bottom}}=-0.02\,\lambda',
}
for name, equation in EQUATIONS.items():
    fig = plt.figure(figsize=(18, 1.7))
    fig.text(.01, .43, '$' + equation + '$', fontsize=38, va='center', color='#17191C')
    for ext in ['svg', 'png']:
        fig.savefig(OUT / f'{name}.{ext}', transparent=True, bbox_inches='tight', pad_inches=.08, dpi=220)
    plt.close(fig)
(OUT / 'equations.json').write_text(json.dumps(EQUATIONS, indent=2))

# Illustrative coarse mesh, with the boundary constraints of the actual quick lab.
fig, ax = plt.subplots(figsize=(11, 5))
for x in np.linspace(0, 4, 25): ax.plot([x,x], [0,2], color='#CFD8E3', lw=.6)
for y in np.linspace(0, 2, 13): ax.plot([0,4], [y,y], color='#CFD8E3', lw=.6)
for x in np.linspace(0, 4, 25)[:-1]:
    for y in np.linspace(0, 2, 13)[:-1]:
        ax.plot([x,x+1/6], [y,y+1/6], color='#CFD8E3', lw=.6)
ax.plot([0,4,4,0,0],[0,0,2,2,0], color='#245A81',lw=2)
ax.plot([0,.8],[1,1],color='#B85C20',lw=5)
ax.annotate(r'Locked $d=1$', xy=(.5,1), xytext=(.1,1.6),
            arrowprops={'arrowstyle':'->','color':'#B85C20'}, color='#B85C20',fontsize=17)
ax.text(2,2.25,r'$u_y=+0.02\lambda$',ha='center',color='#245A81',fontsize=19)
ax.text(2,-.33,r'$u_y=-0.02\lambda$',ha='center',color='#245A81',fontsize=19)
ax.text(4.12,1,r'$u_x=0$'+'\non all four\nouter edges',va='center',fontsize=16)
ax.set(xlim=(-.1,5.15),ylim=(-.5,2.55),aspect='equal')
ax.axis('off')
for ext in ['svg','png']:
    fig.savefig(OUT / f'teaching_bcs.{ext}',bbox_inches='tight',pad_inches=.1,dpi=200)
plt.close(fig)

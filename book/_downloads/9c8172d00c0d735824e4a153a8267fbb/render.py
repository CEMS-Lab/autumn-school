"""Render retained HPC arrays. Does not execute the numerical experiments."""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.lines import Line2D
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/teaching_results.json'
d=json.loads(DATA.read_text())
assert d['receipt']['execution']=='HPC only'
assert d['receipt']['source_sha256']==hashlib.sha256((ROOT/'code/lab.py').read_bytes()).hexdigest()
OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':12,
                     'axes.titlesize':13,'axes.labelsize':12,'legend.fontsize':10,'figure.dpi':130})
BLUE='#0072B2';ORANGE='#D55E00';GREEN='#009E73'
def save(fig,name):
    for suffix in ('png','pdf'):fig.savefig(OUT/f'{name}.{suffix}',dpi=240,bbox_inches='tight',pad_inches=.12)
    plt.close(fig)
g=d['geometry'];fig,ax=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
for eps,y,c in zip(g['epsilon'],g['indicators'],[BLUE,ORANGE,GREEN]):ax[0].plot(g['x'],y,color=c,label=f'$\\varepsilon={eps:g}$ mm')
ax[0].set(xlabel='$x-c_x$ (mm)',ylabel='Indicator $s$',title='(a) Fixed radius: 2 mm');ax[0].legend()
ax[1].plot(g['distance'],g['energy'],color=BLUE);ax[1].set(xlabel='Centre distance $q$ (mm)',ylabel='Penalty (mm$^2$)',title='(b) Overlap energy')
ax[2].plot(g['distance'],g['derivative'],color=ORANGE);ax[2].set(xlabel='Centre distance $q$ (mm)',ylabel='$dP/dq$ (mm)',title='(c) Radial derivative')
save(fig,'geometry')
q=d['quadrature'];fig,ax=plt.subplots(1,2,figsize=(9,3.8),layout='constrained')
for r,y,c in zip(q,[1,0],[BLUE,ORANGE]):ax[0].plot(r['x'],np.full(len(r['x']),y),'|',ms=13,color=c,label=r['name'].replace('_',' '))
ax[0].set(xlabel='$x$',yticks=[],title='(a) Two sampling patterns');ax[0].legend(loc='center')
x=np.arange(3)
for i,r in enumerate(q):ax[1].bar(x+(i-.5)*.35,[r['nodal_mse'],r['lumped_mse'],r['consistent_mse']],width=.35,label=r['name'].replace('_',' '),color=[BLUE,ORANGE][i])
ax[1].axhline(1/3,color='black',ls='--',lw=1,label='Exact integral: 1/3');ax[1].set(xticks=x,xticklabels=['Nodal','Lumped','Consistent'],ylim=(0,.54),ylabel='Mean squared residual',title='(b) Same residual $r(x)=x$');ax[1].legend(fontsize=9,loc='upper right')
save(fig,'quadrature')
v=d['derivatives'];fig,ax=plt.subplots(figsize=(6.8,3.8),layout='constrained')
ax.loglog(v['h'],np.maximum(v['relative_error'],1e-16),'o-',color=BLUE,ms=4)
ax.set(xlabel='Log-stiffness perturbation $h$',ylabel='Relative FD discrepancy',title='Two-degree-of-freedom equilibrium');ax.grid(alpha=.2,which='major');save(fig,'derivatives')
fig,ax=plt.subplots(1,2,figsize=(9,3.8),layout='constrained')
for name,c in [('gradient',BLUE),('scaled',ORANGE)]:
    p=np.array(d['conditioning'][name]);label={'gradient':'Gradient descent','scaled':'Scaled descent'}[name]
    ax[0].plot(p[:,0],p[:,1],'.-',ms=3,color=c,label=label)
    ax[1].semilogy(np.arange(21),p[:21,2],color=c,label=label)
ax[0].set(xlabel='$p_1$',ylabel='$p_2$',title='(a) Recorded parameter paths');ax[1].set(xlabel='Update',ylabel='Objective',title='(b) First 20 updates');ax[0].legend();ax[1].legend();save(fig,'conditioning')
o=d['observations'];xx,yy=np.meshgrid(np.linspace(-.6,2.3,160),np.linspace(-.6,2.3,160))
fig,ax=plt.subplots(1,2,figsize=(9,4.5),layout='constrained')
for a,(name,r) in zip(ax,o['models'].items()):
    J=np.array(r['J']);target=np.array(r['y']);res=np.einsum('ij,jkl->ikl',J,np.array([xx,yy]))-target[:,None,None]
    levels=a.contour(xx,yy,.5*np.sum(res**2,axis=0),levels=[.005,.05,.2,.8,2],colors='.72',linewidths=.8)
    for path,c in zip(r['paths'],[BLUE,ORANGE]):
        p=np.array(path);a.plot(p[:,0],p[:,1],'.-',ms=3,color=c)
        a.plot(p[0,0],p[0,1],'s',color=c,ms=5)
    a.plot(*o['truth'],'*',ms=10,color='black');a.set(xlabel='$p_1$',ylabel='$p_2$',aspect='equal',title=name.replace('_',' ').capitalize())
fig.legend(handles=[Line2D([],[],color=BLUE,label='Start: (0, 0)'),
                    Line2D([],[],color=ORANGE,label='Start: (1.5, 0)'),
                    Line2D([],[],color='.4',marker='s',ls='',label='Initial estimate'),
                    Line2D([],[],color='black',marker='*',ls='',label='Reference')],
           loc='outside lower center',ncol=4,frameon=False)
save(fig,'observations')
fig,ax=plt.subplots(figsize=(6.8,4.5),layout='constrained')
for (name,r),c in zip(o['models'].items(),[BLUE,ORANGE]):
    cov=np.array(r['posterior_covariance']);eig,V=np.linalg.eigh(cov);i=np.argmax(eig);angle=np.degrees(np.arctan2(V[1,i],V[0,i]))
    width,height=2*np.sqrt(5.991464547*np.array([eig[i],eig[1-i]]))
    ax.add_patch(Ellipse(r['posterior_mean'],width,height,angle=angle,fill=False,color=c,lw=2,label=name.replace('_',' ')))
    ax.plot(*r['posterior_mean'],'o',color=c,ms=4)
ax.plot(*o['truth'],'*',color='black',ms=10,label='Reference parameters')
ax.set(xlim=(-1.5,3),ylim=(-1,3.5),aspect='equal',xlabel='$p_1$',ylabel='$p_2$',title='Exact linear-Gaussian posterior: 95% contours');ax.legend(loc='upper right');save(fig,'uncertainty')
h=d['hybrid'];fig,ax=plt.subplots(1,2,figsize=(9,3.8),layout='constrained')
for name,c,style in [('reference','black','-'),('prediction',ORANGE,'--'),('corrected',BLUE,':')]:ax[0].plot(h['x'],h[name],color=c,ls=style,label=name)
for key,c in [('zero_residuals',ORANGE),('warm_residuals',BLUE)]:ax[1].semilogy(np.arange(len(h[key])),np.maximum(h[key],1e-16),'o-',color=c,label=key.split('_')[0]+' start',ms=4)
ax[0].set(xlabel='Normalised position',ylabel='Displacement (nondimensional)',title='(a) Predict and correct');ax[1].set(xlabel='CG iteration',xticks=range(max(len(h['zero_residuals']),len(h['warm_residuals']))),ylabel='Relative residual',title='(b) Same equation, two starts');ax[0].legend();ax[1].legend();save(fig,'hybrid')
receipt=d['receipt']
rows='\n'.join(f'| {k.replace("_"," ")} | {"Pass" if v else "Fail"} |' for k,v in receipt['checks'].items())
text=f'''# Retained computations and reproducibility

The six numerical teaching experiments were executed on HPC. The figures in
this extension are generated from their retained arrays, not from a new local
execution. These checks concern the stated teaching models.

## Result card

- Checks passed: {sum(receipt['checks'].values())} / {len(receipt['checks'])}.
- Measured experiment-loop time: {receipt['seconds']:.3f} seconds, excluding Python
  startup, package imports, queue wait and figure rendering.
- Python {receipt['python']}; PyTorch {receipt['torch']}; NumPy {receipt['numpy']}.
- AD log-stiffness derivative: {v['ad']:.4f}.
- Implicit derivative: {v['implicit']:.4f}.
- Best sampled FD relative discrepancy: {min(v['relative_error']):.3g}.

| Check | Outcome |
|---|---|
{rows}

The coincidence check intentionally records a zero separating gradient. A
passing test here means that this behaviour was reproduced, not that coincident
particles can be separated by that gradient.

## Reproduce and inspect

Download the {{download}}`experiment script <code/lab.py>` and
{{download}}`retained arrays and checks <data/teaching_results.json>`.
The {{download}}`figure renderer <code/render.py>` only reads retained results.
The {{download}}`workflow source <tex/inverse_workflow.tex>` uses LaTeX/TikZ.
The {{download}}`rendering receipt <data/rendering_receipt.json>` records
input, generator and figure hashes with the plotting-library version.

```bash
python lab.py --output teaching_results.json
```

NumPy and PyTorch are required. Research executions for this project use HPC.
The script exits unsuccessfully if any declared teaching check fails. The
source SHA-256 stored in the result file is checked by the renderer.

## What this evidence establishes

The tests verify geometry behaviour, quadrature, a smooth linear-solve
derivative, simple optimisation and observation models, and a corrected linear
prediction. Verifying an entire fracture trajectory additionally requires its
specific source, observation rule, history updates and forward/adjoint checks.
The application chapter sets out those separate experiments.
'''
(ROOT/'07_results.md').write_text(text)
render_receipt={
    'scope':'Local authoring/rendering only; numerical arrays were retained from HPC.',
    'matplotlib':matplotlib.__version__,
    'numpy':np.__version__,
    'data_sha256':hashlib.sha256(DATA.read_bytes()).hexdigest(),
    'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'workflow_tex_sha256':hashlib.sha256((ROOT/'tex/inverse_workflow.tex').read_bytes()).hexdigest(),
    'figure_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted(OUT.iterdir()) if p.suffix in ('.png','.pdf')}
}
(ROOT/'data/rendering_receipt.json').write_text(json.dumps(render_receipt,indent=2)+'\n')
print('Rendered seven figures and the result chapter from verified HPC data.')

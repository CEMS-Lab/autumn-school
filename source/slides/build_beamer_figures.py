"""Original scientific illustrations for the PhAST course. No solver is run here.

Run: python build_beamer_figures.py
Requires NumPy and Matplotlib. Writes vector PDFs, PNG previews and plot data.
Analytic curves and conceptual damage bands are not fracture simulation results.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent / 'latex_figures'
OUT.mkdir(exist_ok=True)
NAVY, TEAL, RUST, GREY = '#20364D', '#087F82', '#BD5435', '#67737D'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14,
    'axes.labelsize': 16, 'xtick.labelsize': 12, 'ytick.labelsize': 12,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.edgecolor': GREY, 'axes.labelcolor': 'black', 'text.color': 'black',
    'xtick.color': GREY, 'ytick.color': GREY, 'lines.linewidth': 2.5,
    'pdf.fonttype': 42, 'ps.fonttype': 42, 'savefig.facecolor': 'white'})
DATA = {'scope': 'Analytic teaching curves; no fracture solve', 'eta': 1e-6}

def save(fig, name):
    fig.savefig(OUT / (name + '.pdf'), bbox_inches='tight', pad_inches=.08)
    fig.savefig(OUT / (name + '.png'), dpi=180, bbox_inches='tight', pad_inches=.08)
    plt.close(fig)

def axes():
    fig, ax = plt.subplots(figsize=(7.5, 4.1))
    ax.grid(axis='y', color='#DDE3E6', lw=.7)
    ax.set_axisbelow(True)
    return fig, ax

d = np.linspace(0, 1, 401)
eta = DATA['eta']
quad = (1 - eta) * (1 - d)**2 + eta
cubic = (1 - eta) * (1 - 3*d*d + 2*d**3) + eta
rational = (1 - eta) * (1-d)**2 / ((1-d)**2 + 2*d*(1+d)) + eta
DATA['degradation'] = {'d': d.tolist(), 'quadratic': quad.tolist(),
    'cubic_illustration': cubic.tolist(), 'rational_a2_illustration': rational.tolist()}
fig, ax = axes()
for values, colour, style, label in [(quad,NAVY,'-','Quadratic baseline'),
        (cubic,TEAL,'--','Cubic illustration'),(rational,RUST,'-.','Rational illustration')]:
    ax.plot(d, values, color=colour, ls=style, label=label)
ax.set(xlabel=r'Damage $d$', ylabel=r'Degradation $g(d)$', xlim=(0,1), ylim=(0,1.04))
ax.set_xticks([0,.25,.5,.75,1]); ax.set_yticks(np.linspace(0,1,6))
ax.legend(frameon=False, fontsize=12, loc='upper right')
save(fig, 'degradation')

fig, ax = axes()
derivative = -2*(1-eta)*(1-d)
ax.plot(d, derivative, color=NAVY)
ax.scatter([.25],[-1.5*(1-eta)],s=48,color=TEAL,zorder=4)
ax.annotate(r"$g'(0.25)\approx-1.5$",(.25,-1.5*(1-eta)),xytext=(.40,-1.67),
    arrowprops={'arrowstyle':'-','color':TEAL},color=TEAL,fontsize=14)
ax.set(xlabel=r'Damage $d$',ylabel=r"Derivative $g'(d)$",xlim=(0,1),ylim=(-2.05,.05))
ax.set_yticks([-2,-1.5,-1,-.5,0]); save(fig,'degradation_derivative')
DATA['derivative'] = {'d':d.tolist(),'gprime':derivative.tolist()}

x = np.linspace(-4,4,801)
at2, at1 = np.exp(-abs(x)), np.maximum(1-abs(x)/2,0)**2
fig, ax = axes()
ax.plot(x,at2,color=NAVY,label='AT2: exponential tail')
ax.plot(x,at1,color=TEAL,ls='--',label='AT1: compact support')
ax.set(xlabel=r'Position $x/\ell$',ylabel=r'Damage $d$',xlim=(-4,4),ylim=(0,1.04))
ax.legend(frameon=False,fontsize=12,loc='upper left'); save(fig,'damage_profiles')
DATA['profiles'] = {'x_over_ell':x.tolist(),'AT1':at1.tolist(),'AT2':at2.tolist()}

cmap = LinearSegmentedColormap.from_list('original_damage', ['#FFFFFF','#AED8D5',TEAL,NAVY])
def crack(ax, mode='diffuse', stage='propagation', mesh=False, loads=True):
    ax.set(xlim=(-.10,1.10),ylim=(-.15,.95),aspect='equal')
    ax.axis('off')
    pts=np.array([[0,.39],[.24,.39],[.43,.41],[.62,.47],[.83,.52]])
    if stage=='initiation': pts=pts[:2]
    if mesh:
        for xx in np.linspace(0,1,13): ax.plot([xx,xx],[0,.8],color='#CCD6DC',lw=.45,zorder=1)
        for yy in np.linspace(0,.8,11): ax.plot([0,1],[yy,yy],color='#CCD6DC',lw=.45,zorder=1)
    ax.add_patch(Rectangle((0,0),1,.8,fill=False,ec=NAVY,lw=1.4,zorder=4))
    if mode=='diffuse':
        gx,gy=np.meshgrid(np.linspace(0,1,360),np.linspace(0,.8,288))
        dist=np.full_like(gx,np.inf)
        branches=[pts]
        if stage=='branching': branches.append(np.array([[.43,.41],[.62,.29],[.81,.19]]))
        for branch in branches:
            for a,b in zip(branch[:-1],branch[1:]):
                v=b-a;t=np.clip(((gx-a[0])*v[0]+(gy-a[1])*v[1])/(v@v),0,1)
                dist=np.minimum(dist,np.hypot(gx-a[0]-t*v[0],gy-a[1]-t*v[1]))
        ax.imshow(np.exp(-dist/.023),extent=[0,1,0,.8],origin='lower',cmap=cmap,
                  vmin=0,vmax=1,zorder=2,interpolation='bilinear')
    elif mode=='cohesive':
        ax.plot([0,1],[.4,.4],color=TEAL,lw=2)
        for xx in np.linspace(.15,.9,6):
            ax.annotate('',(xx,.50),(xx,.42),arrowprops={'arrowstyle':'->','color':TEAL,'lw':1})
            ax.annotate('',(xx,.30),(xx,.38),arrowprops={'arrowstyle':'->','color':TEAL,'lw':1})
    else: ax.plot(pts[:,0],pts[:,1],color=NAVY,lw=2.5,zorder=5)
    if loads:
        for xx in [.25,.5,.75]:
            ax.annotate('',(xx,.93),(xx,.82),arrowprops={'arrowstyle':'->','color':TEAL,'lw':1.4})
            ax.annotate('',(xx,-.13),(xx,-.02),arrowprops={'arrowstyle':'->','color':TEAL,'lw':1.4})

fig,ax=plt.subplots(figsize=(4.5,4.2));crack(ax,stage='branching');save(fig,'title_specimen')
fig,axs=plt.subplots(1,3,figsize=(11.5,3.4))
for ax,mode,title in zip(axs,['sharp','cohesive','diffuse'],['Sharp discontinuity','Cohesive interface','Diffuse phase field']):
    crack(ax,mode=mode,mesh=mode=='sharp');ax.set_title(title,fontsize=16,pad=3)
fig.subplots_adjust(wspace=.24); save(fig,'representations')
fig,axs=plt.subplots(1,3,figsize=(11.5,3.4))
for ax,stage in zip(axs,['initiation','propagation','branching']):
    crack(ax,stage=stage);ax.set_title(stage.capitalize(),fontsize=16,pad=3)
fig.subplots_adjust(wspace=.24);save(fig,'evolution_schematic')

fig,axs=plt.subplots(1,2,figsize=(10.8,3.35))
for ax,n,title in zip(axs,[4,16],['Coarse sampling','Finer sampling']):
    gx,gy=np.meshgrid(np.linspace(0,2,360),np.linspace(0,1,180))
    ax.imshow(np.exp(-abs(gy-.5)/.055),extent=[0,2,0,1],origin='lower',cmap=cmap,vmin=0,vmax=1)
    for xx in np.linspace(0,2,2*n+1):ax.plot([xx,xx],[0,1],color=GREY,lw=.6,alpha=.8)
    for yy in np.linspace(0,1,n+1):ax.plot([0,2],[yy,yy],color=GREY,lw=.6,alpha=.8)
    ax.set_title(title,fontsize=16);ax.set(xlim=(0,2),ylim=(0,1),aspect='equal');ax.axis('off')
fig.subplots_adjust(wspace=.20);save(fig,'mesh_resolution')

fig,ax=plt.subplots(figsize=(6.1,3.6));ax.axis('off');ax.set(xlim=(-.8,4.3),ylim=(-.5,2.5),aspect='equal')
for xx in np.linspace(0,4,17):ax.plot([xx,xx],[0,2],color='#CCD6DC',lw=.5)
for yy in np.linspace(0,2,9):ax.plot([0,4],[yy,yy],color='#CCD6DC',lw=.5)
for xx in np.linspace(0,3.75,16):
    for yy in np.linspace(0,1.75,8):ax.plot([xx,xx+.25],[yy,yy+.25],color='#CCD6DC',lw=.4)
ax.add_patch(Rectangle((0,0),4,2,fill=False,ec=NAVY,lw=1.5))
ax.plot([0,.8],[1,1],color=NAVY,lw=3)
ax.text(2,2.25,r'$u_y=+\bar u/2$',ha='center',fontsize=15,color=TEAL)
ax.text(2,-.35,r'$u_y=-\bar u/2$; one $u_x$ anchor',ha='center',fontsize=13,color=TEAL)
ax.text(-.10,1,'$d=1$',ha='right',va='center',fontsize=13)
save(fig,'geometry_mesh')

fig,ax=plt.subplots(figsize=(9.5,2.6));ax.axis('off')
layers=[3,5,5,1]; xp=[.06,.36,.66,.94]
for k,n in enumerate(layers):
    yp=np.linspace(.24,.77,n) if n>1 else [.505]
    if k<len(layers)-1:
        yn=np.linspace(.24,.77,layers[k+1]) if layers[k+1]>1 else [.505]
        for a in yp:
            for b in yn:ax.plot([xp[k],xp[k+1]],[a,b],color='#CDDBDF',lw=.6,zorder=1)
    ax.scatter(np.full(n,xp[k]),yp,s=120,fc='white',ec=TEAL if k<3 else NAVY,lw=1.6,zorder=2)
for xx,label in zip(xp,['features','hidden layer','hidden layer','target']):ax.text(xx,.09,label,ha='center',fontsize=14)
ax.set(xlim=(-.04,1.03),ylim=(0,1));save(fig,'mlp')

# Replot a frozen course-owned, actually executed PhAST record. This is not a solve.
if (OUT/'forward_fields.npz').is_file():
    import matplotlib.tri as mtri
    fields=np.load(OUT/'forward_fields.npz')
    summary=json.loads((OUT/'forward_summary.json').read_text())
    nodes=fields['nodes']; triangles=mtri.Triangulation(nodes[:,0],nodes[:,1],fields['elements'])
    fig,axs=plt.subplots(1,3,figsize=(11.5,3.0),layout='constrained')
    for ax,key,title in zip(axs,['seeded_damage','first_damage','final_damage'],
            ['Locked precrack','First increment','Final increment']):
        im=ax.tripcolor(triangles,fields[key],shading='gouraud',cmap=cmap,vmin=0,vmax=1,rasterized=True)
        ax.set(xlabel=r'$x$',ylabel=r'$y$',aspect='equal',xlim=(0,4),ylim=(0,2))
        ax.set_title(title,fontsize=15);ax.set_xticks([0,2,4]);ax.set_yticks([0,1,2])
    fig.colorbar(im,ax=axs,shrink=.74,label=r'Damage $d$',ticks=[0,.5,1])
    save(fig,'phast_evolution')
    fig,axs=plt.subplots(1,2,figsize=(8.7,3.5),layout='constrained')
    for ax,key,title in zip(axs,['first_damage','final_damage'],['First increment','Final increment']):
        im=ax.tripcolor(triangles,fields[key],shading='gouraud',cmap='viridis',vmin=0,vmax=1,rasterized=True)
        ax.set(xlabel=r'$x$',ylabel=r'$y$',aspect='equal',xlim=(0,4),ylim=(0,2))
        ax.set_title(title,fontsize=17);ax.set_xticks([0,2,4]);ax.set_yticks([0,1,2])
    fig.colorbar(im,ax=axs,shrink=.64,label=r'Damage $d$',ticks=[0,.5,1])
    save(fig,'phast_comparison')
    tr=summary['trace']; load=np.array([r['load_factor'] for r in tr])
    fig,axs=plt.subplots(1,2,figsize=(10.4,3.65),layout='constrained')
    axs[0].plot(load,[r['reaction_top_y'] for r in tr],color=NAVY)
    axs[0].set(xlabel='Load factor',ylabel='Top vertical reaction')
    axs[1].semilogy(load,[r['stagger_residual'] for r in tr],color=TEAL)
    axs[1].axhline(1e-5,color=GREY,ls='--',lw=1.2,label=r'stated tolerance $10^{-5}$')
    axs[1].set(xlabel='Load factor',ylabel='Recorded stagger residual')
    axs[1].legend(frameon=False,fontsize=10)
    for ax in axs:ax.grid(axis='y',color='#DDE3E6',lw=.7)
    save(fig,'phast_response')

if (OUT/'toy_heldout_arrays.npz').is_file():
    heldout=np.load(OUT/'toy_heldout_arrays.npz')
    fig,axs=plt.subplots(1,2,figsize=(8.8,4.4),layout='constrained')
    for ax,key,title in zip(axs,['reference','prediction'],['Reference solution','Reloaded MLP']):
        im=ax.imshow(heldout[key],origin='lower',extent=[0,1,0,1],cmap='viridis',vmin=0,vmax=1,interpolation='nearest')
        ax.set(xlabel=r'$x/L$',ylabel=r'$y/H$',aspect='equal')
        ax.set_title(title,fontsize=17);ax.set_xticks([0,.5,1]);ax.set_yticks([0,.5,1])
    fig.colorbar(im,ax=axs,shrink=.8,label='Toy field',ticks=[0,.5,1])
    save(fig,'toy_reference_prediction')

(OUT/'analytic_plot_data.json').write_text(json.dumps(DATA,indent=2)+'\n')
print('Wrote original vector figures and analytic_plot_data.json to',OUT)

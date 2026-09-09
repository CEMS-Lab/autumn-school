"""Original CPU teaching experiments. Execute on HPC; render results separately.

These are analytic and small linear-algebra models, not fracture simulations.
Requires NumPy and PyTorch. Outputs contain arrays, checks and source hashes.
"""
import argparse
import hashlib
import json
import platform
import time
from pathlib import Path
import numpy as np
import torch

torch.set_default_dtype(torch.float64)


def geometry():
    distances = torch.linspace(0, 7, 281, requires_grad=True)
    energy = torch.relu(4-distances).square()/2
    derivative = torch.autograd.grad(energy.sum(), distances)[0]
    p = torch.zeros((2, 2), requires_grad=True)
    radius = torch.tensor([2., 2.])
    penalty = torch.relu(radius.sum()-torch.linalg.vector_norm(p[0]-p[1])).square()/2
    g = torch.autograd.grad(penalty, p)[0]
    x = np.linspace(-5, 5, 401)
    epsilon = [.15, .4, 1.]
    indicators = [1/(1+np.exp((np.abs(x)-2)/eps)) for eps in epsilon]
    return {'distance': distances.detach().tolist(), 'energy': energy.detach().tolist(),
            'derivative': derivative.tolist(), 'coincident_gradient': g.tolist(),
            'x': x.tolist(), 'epsilon': epsilon, 'indicators': [a.tolist() for a in indicators]}, {
            'overlap_gradient_finite': bool(torch.isfinite(g).all()),
            'coincident_centres_have_zero_separating_gradient': bool((g==0).all()),
            'separated_energy_zero': float(energy[-1].detach()) == 0,
            'tangent_energy_zero': float(torch.relu(torch.tensor(4.)-4)**2)==0}


def quadrature():
    records=[]
    for name,x in [('uniform',np.linspace(0,1,41)),('left_refined',np.r_[np.linspace(0,.25,31),np.linspace(.25,1,11)[1:]])]:
        h=np.diff(x)
        lump=np.zeros_like(x)
        lump[:-1]+=h/2
        lump[1:]+=h/2
        consistent=float(np.sum(h*(x[:-1]**2+x[:-1]*x[1:]+x[1:]**2)/3))
        records.append({'name':name,'x':x.tolist(),'residual':x.tolist(),
                        'nodal_mse':float(np.mean(x*x)), 'lumped_mse':float(np.dot(lump,x*x)),
                        'consistent_mse':consistent,'exact_integral':1/3})
    return records, {'consistent_integral_exact_on_both_meshes':all(abs(r['consistent_mse']-1/3)<1e-14 for r in records),
                     'nodal_average_changes_with_sampling':abs(records[0]['nodal_mse']-records[1]['nodal_mse'])>.05}


def solve_loss(theta):
    A=torch.stack([torch.stack([theta.exp()+1.,theta.new_tensor(-1.)]),torch.stack([theta.new_tensor(-1.),theta.new_tensor(2.)])])
    b=theta.new_tensor([1.,.2])
    u=torch.linalg.solve(A,b)
    y=theta.new_tensor([.2,.3])
    return .5*((u-y)**2).sum(), A, u, y


def derivatives():
    theta=torch.tensor(.3,requires_grad=True)
    loss,A,u,y=solve_loss(theta)
    ad=torch.autograd.grad(loss,theta)[0]
    adjoint=torch.linalg.solve(A.detach().T,(u-y).detach())
    implicit=-adjoint[0]*theta.detach().exp()*u.detach()[0]
    hs=np.logspace(-1,-9,17)
    fds=[]
    for h in hs:
        with torch.no_grad():
            fds.append(float((solve_loss(theta+h)[0]-solve_loss(theta-h)[0])/(2*h)))
    relative=[abs(x-float(ad))/max(abs(x),abs(float(ad)),1e-30) for x in fds]
    return {'theta':float(theta.detach()),'ad':float(ad),'implicit':float(implicit), 'h':hs.tolist(),'fd':fds,'relative_error':relative}, {
        'ad_matches_implicit':bool(torch.allclose(ad,implicit,rtol=1e-12,atol=1e-14)),
        'fd_has_accurate_intermediate_steps':min(relative)<1e-7}


def conditioning():
    matrix=np.diag([1.,100.])
    paths={}
    for name,preconditioner,step in [('gradient',np.eye(2),.015),('scaled',np.diag([1.,.01]),.8)]:
        p=np.array([2.,2.]); rows=[]
        for _ in range(81):
            rows.append([*p,.5*float(p@matrix@p)])
            p=p-step*preconditioner@matrix@p
        paths[name]=rows
    return paths, {'scaled_quadratic_objective_smaller':paths['scaled'][-1][2]<paths['gradient'][-1][2],
                   'both_quadratic_objectives_decrease':all(np.all(np.diff(np.array(r)[:,2])<=1e-12) for r in paths.values())}


def observations():
    # A two-variable linearized observation model, not an actual inclusion solver.
    truth=np.array([.7,1.1]); records={}
    for name,J in [('one_observation',np.array([[1.,1.]])),('two_observations',np.array([[1.,1.],[1.,-1.]]))]:
        y=J@truth
        paths=[]
        for start in ([0.,0.],[1.5,0.]):
            p=np.array(start); rows=[]
            for _ in range(51):
                residual=J@p-y
                rows.append([*p,.5*float(residual@residual)])
                p-=.2*J.T@residual
            paths.append(rows)
        covariance=np.linalg.inv(np.eye(2)+(J.T@J)/.1**2)
        mean=covariance@J.T@y/.1**2
        records[name]={'J':J.tolist(),'y':y.tolist(),'paths':paths,
                        'posterior_mean':mean.tolist(),'posterior_covariance':covariance.tolist(),
                        'singular_values':np.linalg.svd(J,compute_uv=False).tolist()}
    return {'truth':truth.tolist(),'models':records,'noise_std':.1,'prior_mean':[0.,0.],'prior_covariance':np.eye(2).tolist()}, {
        'one_observation_has_null_direction':bool(np.allclose(np.array([[1.,1.]])@np.array([1.,-1.]),0)),
        'two_observations_recover_both_unknowns':all(np.linalg.norm(np.array(p[-1][:2])-truth)<1e-9 for p in records['two_observations']['paths']),
        'additional_observation_reduces_posterior_determinant':np.linalg.det(records['two_observations']['posterior_covariance'])<np.linalg.det(records['one_observation']['posterior_covariance'])}


def hybrid():
    # Learn a reduced-basis initial guess; enforce the exact fixed linear system.
    n=24
    A=2*np.eye(n)-np.eye(n,k=1)-np.eye(n,k=-1)
    A+=.05*np.eye(n)
    x=np.arange(1,n+1)/(n+1)
    train=np.array([np.sin(np.pi*x), np.sin(2*np.pi*x)]).T
    targets=np.linalg.solve(A,train)
    B=targets@np.linalg.pinv(train)
    b=np.sin(np.pi*x)+.2*np.sin(3*np.pi*x)
    reference=np.linalg.solve(A,b)
    def cg(initial):
        u=initial.copy(); r=b-A@u; p=r.copy(); rows=[float(np.linalg.norm(r)/np.linalg.norm(b))]
        for _ in range(n*2):
            if rows[-1]<1e-11:break
            Ap=A@p; rr=r@r; alpha=rr/(p@Ap)
            u+=alpha*p; rnew=r-alpha*Ap
            p=rnew+(rnew@rnew)/rr*p; r=rnew
            rows.append(float(np.linalg.norm(b-A@u)/np.linalg.norm(b)))
        return u,rows
    zero,rz=cg(np.zeros(n)); warm,rw=cg(B@b)
    return {'x':x.tolist(),'prediction':(B@b).tolist(),'reference':reference.tolist(),'corrected':warm.tolist(),
            'zero_residuals':rz,'warm_residuals':rw,'scope':'Learned linear initial guess on a fixed 1D system; no wall-time speedup claim'}, {
        'corrected_solution_matches_direct_solve':bool(np.allclose(warm,reference,atol=1e-9)),
        'zero_start_also_matches_direct_solve':bool(np.allclose(zero,reference,atol=1e-9))}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(); start=time.perf_counter(); output={};checks={}
    for name,fn in [('geometry',geometry),('quadrature',quadrature),('derivatives',derivatives),('conditioning',conditioning),('observations',observations),('hybrid',hybrid)]:
        output[name],values=fn(); checks.update({key: bool(value) for key,value in values.items()})
    output['receipt']={'checks':checks,'all_checks_passed':all(checks.values()),'seconds':time.perf_counter()-start,
        'execution':'HPC only' if __import__('os').environ.get('SLURM_JOB_ID') else 'unverified execution environment',
        'python':platform.python_version(),'torch':torch.__version__,'numpy':np.__version__,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Analytic and small linear-algebra teaching experiments; not full fracture recovery.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output['receipt'],indent=2))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()

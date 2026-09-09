"use strict";
(() => {
  const byId = id => document.getElementById(id);
  const teal = "#087f83", orange = "#c16a31", ink = "#173248", muted = "#596b78";
  const clamp = (x,a,b) => Math.max(a,Math.min(b,x));
  const fixed = (x,n=3) => (Math.abs(x)<0.5*Math.pow(10,-n)?0:x).toFixed(n);
  const state = window.courseState = {};
  const text = (x,y,s,extra="") => '<text x="'+x+'" y="'+y+'" '+extra+'>'+s+'</text>';
  const line = (x1,y1,x2,y2,color="#dce5e9",width=1,extra="") => '<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="'+color+'" stroke-width="'+width+'" '+extra+'/>';
  function chart(svgId, fn, bounds, options={}) {
    const el=byId(svgId), [w,h]=el.getAttribute("viewBox").split(" ").slice(2).map(Number);
    const m={l:49,r:20,t:27,b:46};
    const sx=x=>m.l+(x-bounds.x0)/(bounds.x1-bounds.x0)*(w-m.l-m.r);
    const sy=y=>h-m.b-(y-bounds.y0)/(bounds.y1-bounds.y0)*(h-m.t-m.b);
    let out="";
    for(let i=0;i<=4;i++){
      const y=bounds.y0+(bounds.y1-bounds.y0)*i/4, py=sy(y);
      out+=line(m.l,py,w-m.r,py)+text(m.l-9,py+4,fixed(y,options.yDigits??2),'text-anchor="end"');
      const x=bounds.x0+(bounds.x1-bounds.x0)*i/4, px=sx(x);
      out+=line(px,h-m.b,px,h-m.b+5,muted)+text(px,h-m.b+22,fixed(x,options.xDigits??2),'text-anchor="middle"');
    }
    out+=line(m.l,m.t,m.l,h-m.b,muted)+line(m.l,h-m.b,w-m.r,h-m.b,muted);
    if(options.title)out+=text(m.l,15,options.title,'style="fill:'+ink+';font-weight:600"');
    if(options.xlabel)out+=text((m.l+w-m.r)/2,h-4,options.xlabel,'text-anchor="middle"');
    let d="";
    for(let i=0;i<=220;i++){const x=bounds.x0+(bounds.x1-bounds.x0)*i/220;d+=(i?"L":"M")+sx(x).toFixed(2)+","+sy(fn(x)).toFixed(2);}
    out+='<path d="'+d+'" fill="none" stroke="'+(options.color||teal)+'" stroke-width="3"/>';
    if(options.marker!==undefined){
      const x=options.marker,y=fn(x);
      out+=line(sx(x),sy(bounds.y0),sx(x),sy(y),orange,1,'stroke-dasharray="4 4"');
      out+='<circle cx="'+sx(x)+'" cy="'+sy(y)+'" r="5" fill="'+orange+'" stroke="white" stroke-width="2"/>';
    }
    el.innerHTML=out;
  }

  const descriptions={
    sharp:"<b>Sharp crack.</b> The crack is represented as a geometric discontinuity. A fitted-mesh approach aligns element boundaries with the crack, and propagation can require geometry and mesh updates.",
    xfem:"<b>XFEM.</b> Enriched approximation functions represent displacement jumps and near-tip behaviour without requiring the mesh to conform to every crack segment. Enrichment and crack-tracking choices remain part of the method.",
    cohesive:"<b>Cohesive zone.</b> A traction–separation law describes forces transmitted across a separating interface. Interface placement and the softening law influence the predicted crack path and process zone.",
    phase:"<b>Phase field.</b> A continuous damage field regularises the crack over a finite width. Its evolution changes the elastic energy and can describe changes in crack topology without explicit geometric tracking."
  };
  function representation(){
    const mode=document.querySelector('input[name="representation"]:checked').value;
    let out='<rect x="45" y="25" width="700" height="175" rx="3" fill="#f1f6f7" stroke="#aec6cf"/>';
    if(mode==="xfem"){
      for(let x=45;x<=745;x+=70)out+=line(x,25,x,200,"#b5cbd2");
      for(let y=25;y<=200;y+=35)out+=line(45,y,745,y,"#b5cbd2");
      for(let x=45;x<745;x+=70)for(let y=25;y<200;y+=35)out+=line(x,y,x+70,y+35,"#d1e0e5");
      for(let x=115;x<=395;x+=70)out+='<circle cx="'+x+'" cy="95" r="10" fill="#d7ede7" stroke="'+teal+'"/><circle cx="'+x+'" cy="130" r="10" fill="#d7ede7" stroke="'+teal+'"/>';
    }
    const path="M45 112L230 112L315 94L405 112L460 88";
    if(mode==="phase"){
      out+='<path d="'+path+'" fill="none" stroke="#bddcd5" stroke-width="49" stroke-linecap="round"/><path d="'+path+'" fill="none" stroke="#6db6ad" stroke-width="28" stroke-linecap="round"/><path d="'+path+'" fill="none" stroke="'+teal+'" stroke-width="9" stroke-linecap="round"/>';
      out+=text(545,69,"d = 0 · intact")+text(545,94,"0 &lt; d &lt; 1 · transition")+text(545,119,"d ≈ 1 · crack centre");
    }else{
      out+='<path d="'+path+'" fill="none" stroke="white" stroke-width="13"/><path d="'+path+'" fill="none" stroke="'+ink+'" stroke-width="3"/>';
      if(mode==="cohesive"){
        for(let x=315;x<455;x+=17)out+=line(x,98,x,121,orange,2);
        out+=text(518,81,"Tractions decrease")+text(518,102,"as separation grows.");
      }else if(mode==="xfem"){
        out+=text(518,81,"Enriched degrees")+text(518,102,"of freedom near the crack.");
      }else{
        out+=text(518,81,"Displacement jumps")+text(518,102,"across the crack surfaces.");
      }
    }
    out+=text(45,226,"Notched body under tension · schematic")+line(180,24,180,4,teal,2)+line(180,200,180,219,teal,2);
    byId("crack-view").innerHTML=out;
    byId("representation-text").innerHTML=descriptions[mode];
    state.representation=mode;
  }
  document.querySelectorAll('input[name="representation"]').forEach(el=>el.addEventListener("change",representation));representation();

  const energy={
    elastic:"<b>Stored elastic energy.</b> Displacement u determines the small strain ε(u). The split energies ψ⁺ and ψ⁻ distinguish the degraded and undegraded contributions. Reducing g(d) lowers the selected stiffness as damage develops.",
    fracture:"<b>Regularised fracture energy.</b> Gc is the critical energy release rate. The local term w(d)/ℓ penalises damage, while ℓ|∇d|² penalises spatial gradients. Together with c₀ they approximate the energetic cost of a crack surface.",
    work:"<b>External work.</b> Applied forces and prescribed motion supply energy. The potential energy subtracts the work of conservative external loads; prescribed displacement conditions also restrict the admissible displacement field."
  };
  document.querySelectorAll("[data-energy]").forEach(btn=>btn.addEventListener("click",()=>{
    document.querySelectorAll("[data-energy]").forEach(b=>b.classList.toggle("selected",b===btn));
    byId("energy-explanation").innerHTML=energy[btn.dataset.energy];
    state.energyTerm=btn.dataset.energy;
  }));byId("energy-explanation").innerHTML=energy.elastic;state.energyTerm="elastic";

  function profile(){
    const ell=Number(byId("length-scale").value),model=byId("profile-model").value;
    const fn=x=>model==="AT2"?Math.exp(-Math.abs(x)/ell):Math.pow(Math.max(1-Math.abs(x)/(2*ell),0),2);
    byId("length-value").textContent=fixed(ell,2)+" mm";
    chart("profile-chart",fn,{x0:-4,x1:4,y0:0,y1:1},{xlabel:"Distance normal to crack, x (mm)",title:"Damage d(x)",xDigits:0});
    let out="";
    for(let i=0;i<350;i++){
      const x=-4+8*(i+.5)/350,d=fn(x);
      const col="rgb("+Math.round(243-235*d)+","+Math.round(248-121*d)+","+Math.round(249-118*d)+")";
      out+='<rect x="'+(49+i*731/350)+'" y="3" width="'+(731/350+.2)+'" height="38" fill="'+col+'"/>';
    }
    out+=text(49,66,"Same profile as a damage band")+text(780,66,"intact — damaged centre — intact",'text-anchor="end"');
    byId("profile-band").innerHTML=out;
    byId("profile-equation").innerHTML=model==="AT2"
      ? "<b>AT2:</b> d(x) = exp(−|x|/ℓ). The damage decays continuously and does not have a finite zero-damage boundary. Increasing ℓ widens the profile."
      : "<b>AT1:</b> d(x) = max(1 − |x|/(2ℓ), 0)². The profile reaches zero at |x| = 2ℓ; its total support width is "+fixed(4*ell,2)+" mm.";
    state.profile={model,ell,centre:fn(0),at2ell:fn(2*ell)};
  }
  byId("profile-model").addEventListener("change",profile);byId("length-scale").addEventListener("input",profile);profile();

  const eta=1e-6;
  function law(name,d){
    const q=1-d;
    if(name==="cubic")return {g:(1-eta)*(3*q*q-2*q*q*q)+eta,dg:(1-eta)*(-6*q+6*q*q)};
    if(name==="rational"){
      const a=2,N=q*q,D=N+a*d*(1+d),Np=-2*q,Dp=Np+a*(1+2*d);
      return {g:(1-eta)*N/D+eta,dg:(1-eta)*(Np*D-N*Dp)/(D*D)};
    }
    return {g:(1-eta)*q*q+eta,dg:-2*(1-eta)*q};
  }
  function degradation(){
    const name=byId("degradation-law").value,d=Number(byId("damage-value").value),v=law(name,d);
    byId("damage-output").textContent=fixed(d,2);
    chart("g-chart",x=>law(name,x).g,{x0:0,x1:1,y0:0,y1:1},{title:"Stiffness factor g(d)",xlabel:"Damage d",marker:d});
    chart("dg-chart",x=>law(name,x).dg,{x0:0,x1:1,y0:-2.25,y1:0},{title:"Slope g′(d)",xlabel:"Damage d",marker:d,color:orange,yDigits:2});
    const formula=name==="quadratic"?"g = (1 − η)q² + η":name==="cubic"?"g = (1 − η)(3q² − 2q³) + η":"g = (1 − η)q² / [q² + 2d(1 + d)] + η";
    byId("degradation-readout").innerHTML="<b>"+formula+"</b>, q = 1 − d. At d = "+fixed(d,2)+": g = "+fixed(v.g,4)+", g′ = "+fixed(v.dg,4)+". The same damage variable can produce different stiffness and driving-force contributions under different laws.";
    state.degradation={law:name,d,...v};
  }
  byId("degradation-law").addEventListener("change",degradation);byId("damage-value").addEventListener("input",degradation);degradation();

  const stages=[
    "<b>Apply the next load increment.</b> Retain the previous converged displacement, damage and history. A load increment is not the same as an inner nonlinear iteration.",
    "<b>Solve mechanics at fixed damage.</b> The current damage field determines the degraded stiffness. Apply the mechanical boundary conditions and solve for displacement.",
    "<b>Update the chosen damage-driving field.</b> A common history formulation uses H = max(H previous, ψ⁺). Its use and derivative treatment are explicit modelling and numerical choices.",
    "<b>Solve the damage subproblem.</b> Use the current displacement or history. Enforce the chosen bounds and irreversibility treatment and retain convergence diagnostics.",
    "<b>Check the coupled update.</b> Inspect the configured residual or change criteria. If not converged, repeat mechanics and damage at the same load; otherwise accept the increment and advance."
  ];
  let stage=0,iteration=1,increment=1;
  function staggered(){
    document.querySelectorAll("[data-step]").forEach(el=>el.classList.toggle("current",Number(el.dataset.step)===stage));
    byId("staggered-readout").innerHTML=stages[stage]+"<br><span>Illustrative load increment "+increment+" · inner iteration "+iteration+".</span>";
    state.staggered={stage,iteration,increment};
  }
  byId("step-algorithm").addEventListener("click",()=>{
    if(stage===4){if(byId("repeat-iteration").checked){stage=1;iteration++;}else{stage=0;increment++;iteration=1;}}else stage++;
    staggered();
  });
  byId("reset-algorithm").addEventListener("click",()=>{stage=0;iteration=1;increment=1;staggered();});staggered();

  function operator(){
    const a=Number(byId("operator-value").value),v=[0,1,a,0.2],K=[[1,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,1]];
    const assembled=K.map(row=>row.reduce((s,x,j)=>s+x*v[j],0)), mf=[0,0,0,0];
    for(let i=0;i<3;i++){const f=v[i]-v[i+1];mf[i]+=f;mf[i+1]-=f;}
    const error=Math.max(...mf.map((x,i)=>Math.abs(x-assembled[i])));
    byId("operator-output").textContent=fixed(a,1);
    byId("assembled-result").textContent="Kv = ["+assembled.map(x=>fixed(x,2)).join(", ")+"]";
    byId("matrixfree-result").textContent="Kv = ["+mf.map(x=>fixed(x,2)).join(", ")+"]";
    byId("operator-check").innerHTML="<b>Same action, different construction.</b> v = ["+v.map(x=>fixed(x,1)).join(", ")+"]. Maximum absolute difference = "+error.toExponential(1)+". This identity does not establish which route is faster for a particular fracture problem.";
    state.operator={v,assembled,matrixfree:mf,error};
  }
  byId("operator-value").addEventListener("input",operator);operator();

  let reverse=false;
  function ad(){
    const d=Number(byId("ad-damage").value),g=(1-d)**2,y=2*g,L=.5*(y-1)**2,dg=-2*(1-d),dL=(y-1)*2*dg;
    byId("ad-damage-value").textContent=fixed(d,2);byId("ad-input").textContent=fixed(d,3);
    byId("ad-g").textContent=fixed(g,3);byId("ad-y").textContent=fixed(y,3);byId("ad-loss").textContent=fixed(L,4);
    byId("ad-graph").classList.toggle("reverse",reverse);
    byId("ad-direction").textContent=reverse?"Show forward pass":"Show reverse pass";
    byId("ad-direction").setAttribute("aria-pressed",String(reverse));
    byId("ad-readout").innerHTML=reverse
      ? "<b>Reverse pass:</b> ∂L/∂y = "+fixed(y-1)+", ∂y/∂g = 2, ∂g/∂d = "+fixed(dg)+". Therefore ∂L/∂d = (y − 1) × 2 × [−2(1 − d)] = <b>"+fixed(dL,4)+"</b>."
      : "<b>Forward pass:</b> start with d, compute g, form the prediction y, and compare it with the target y* = 1. The resulting loss is "+fixed(L,4)+". Select the reverse pass to see the chain rule.";
    state.autograd={d,g,y,L,dL,reverse};
  }
  byId("ad-damage").addEventListener("input",ad);byId("ad-direction").addEventListener("click",()=>{reverse=!reverse;ad();});ad();

  function proposal(){
    const prediction=Number(byId("proposal-value").value),tol=Number(byId("assessment-tolerance").value),projected=clamp(prediction,.25,1),residual=Math.abs(projected-.6),accepted=residual<=tol;
    byId("proposal-output").textContent=fixed(prediction,2);byId("predicted-node").textContent="d̂ = "+fixed(prediction,2);
    byId("residual-node").textContent="|r| = "+fixed(residual,3)+"; tolerance "+fixed(tol,2);
    byId("decision-text").textContent=accepted?"Accept projected candidate":"Reference correction to d = 0.60";
    byId("decision-node").classList.toggle("current",accepted);
    byId("proposal-readout").innerHTML="<b>Projected value: "+fixed(projected,2)+".</b> "+(accepted?"The scalar residual meets the selected tolerance, so this illustrative candidate is accepted.":"Bounds and irreversibility are satisfied, but the scalar residual fails the selected tolerance. Correct using the reference equation.")+" Final d = "+fixed(accepted?projected:.6,2)+".";
    state.proposal={prediction,projected,residual,tol,accepted,final:accepted?projected:.6};
  }
  byId("proposal-value").addEventListener("input",proposal);byId("assessment-tolerance").addEventListener("change",proposal);proposal();
  const navLinks=[...document.querySelectorAll(".sidebar nav a")];
  const navSections=navLinks.map(a=>document.querySelector(a.hash));
  let navQueued=false;
  function updateNavigation(){
    navQueued=false;
    let current=0;
    navSections.forEach((el,i)=>{if(el&&el.getBoundingClientRect().top<=window.innerHeight*.3)current=i;});
    navLinks.forEach((a,i)=>{
      a.classList.toggle("active",i===current);
      if(i===current)a.setAttribute("aria-current","location");else a.removeAttribute("aria-current");
    });
  }
  function queueNavigation(){if(!navQueued){navQueued=true;requestAnimationFrame(updateNavigation);}}
  window.addEventListener("scroll",queueNavigation,{passive:true});
  window.addEventListener("resize",queueNavigation);
  updateNavigation();
})();

/** Extend the user's Keynote export without modifying the source document.
 * Created by Allamaprabhu Ani for CEMS-Lab, UKACM Autumn School 2026.
 * Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.
 * Run from the private build folder after linking bundled node_modules.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {FileBlob, PresentationFile} from '@oai/artifact-tool';

const root = process.env.COURSE_ROOT;
if (!root || !path.isAbsolute(root)) throw new Error('Set COURSE_ROOT to the course worktree.');
const build = path.join(root,'.build/intro-lecture-20260909');
const src = process.env.SOURCE_PPTX || path.join(build,'source/keynote-original.pptx');
const assets = path.join(root,'source/slides/intro-lecture/assets');
const figures = path.join(root,'source/slides/latex_figures');
const skill = process.env.PRESENTATION_SKILL_DIR;
const runtimePython = process.env.RUNTIME_PYTHON;
if (!path.isAbsolute(skill ?? '') || !path.isAbsolute(runtimePython ?? '')) {
  throw new Error('Set PRESENTATION_SKILL_DIR and RUNTIME_PYTHON to the configured authoring runtime.');
}
const {finalizePresentation} = await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')));
const lectureNotes = JSON.parse(await fs.readFile(path.join(root,'source/slides/intro-lecture/lecture_notes.json'),'utf8'));
const output = path.join(root,'output/intro-lecture-20260909');
const p = await PresentationFile.importPptx(await FileBlob.load(src));
const snapshot = await p.inspect({kind:'slide,textbox,shape',maxChars:40000});
const entries = snapshot.ndjson.split('\n').filter(Boolean).map(JSON.parse);
const originals = entries.filter(e=>e.kind==='slide');
const C={ink:'#17191C',muted:'#525D67',title:'#B91862',blue:'#245A81',orange:'#B85C20',paper:'#FFFAFC'};
const FF='Helvetica Neue';
const manifest=[];
const creditedSlides=new WeakSet();

function style(shape,copy,x,y,w,h,size=54,colour=C.ink,bold=false) {
  shape.position={left:x,top:y,width:w,height:h};
  shape.text=copy;
  shape.text.style={typeface:FF,fontSize:size,color:colour,bold,autoFit:'none',
    verticalAlignment:'top',alignment:'left',wrap:'square',
    insets:{left:0,right:0,top:0,bottom:0}};
  return shape;
}
function text(sl,copy,x,y,w,h,size=54,colour=C.ink,bold=false) {
  return style(sl.shapes.add({geometry:'textbox',name:copy.slice(0,70),
    fill:'none',line:{fill:'none',width:0}}),copy,x,y,w,h,size,colour,bold);
}
function title(sl,copy,existing) {
  return existing ? style(existing,copy,128,100,2304,220,88,C.title,true)
                  : text(sl,copy,128,100,2304,220,88,C.title,true);
}
function footer(sl,n,scope='') {
  if(!creditedSlides.has(sl)) {
    text(sl,'CEMS-Lab · UKACM Autumn School 2026',128,1352,1500,38,24,C.muted);
    text(sl,String(n).padStart(2,'0'),2330,1344,105,45,30,C.muted);
    creditedSlides.add(sl);
  }
  if(scope) text(sl,scope,128,1250,2240,75,30,C.muted);
}
function note(sl,titleText,notes,source='') {
  sl.speakerNotes.textFrame.setText(notes+(source?'\n\nSources and provenance:\n'+source:'')+
    '\n\nCourse material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.');
  manifest.push({slide:manifest.length+1,title:titleText,notes,source});
}
function fresh(t) {
  const sl=p.slides.add({layoutId:'/ppt/slideLayouts/slideLayout17.xml'});
  sl.background.fill=C.paper; title(sl,t); footer(sl,manifest.length+1); return sl;
}
async function pic(sl,file,x,y,w,h,alt) {
  return sl.images.add({blob:new Uint8Array(await fs.readFile(file)),
    contentType:file.endsWith('.svg')?'image/svg+xml':'image/png',fit:'contain',
    position:{left:x,top:y,width:w,height:h},alt});
}
// High-resolution PNG is used for native Keynote/PDF compatibility. The
// corresponding LaTeX source and vector SVG remain editable source assets.
async function eq(sl,name,x,y,w,h) { return pic(sl,path.join(assets,name+'.png'),x,y,w,h,
  'Equation: '+JSON.parse(await fs.readFile(path.join(assets,'equations.json'),'utf8'))[name]); }
function box(sl,label,x,y,w=480,h=126,colour=C.blue){
  const sh=sl.shapes.add({geometry:'rect',name:label,position:{left:x,top:y,width:w,height:h},
     fill:'#FFFFFF',line:{fill:colour,width:2}});
  sh.text=label; sh.text.style={typeface:FF,fontSize:48,color:colour,alignment:'center',
    verticalAlignment:'middle',autoFit:'none',insets:{left:14,right:14,top:10,bottom:10}};
  return sh;
}
function arrow(sl,a,b,colour=C.blue,from='right',to='left') {
  sl.shapes.connect(a,b,{kind:'straight',fromSide:from,toSide:to,
    line:{fill:colour,width:3},tail:{type:'triangle',width:'sm',length:'sm'}});
}
function row(sl,y,label,description) {
  text(sl,label,128,y,710,100,58,C.blue,true);
  text(sl,description,920,y,1490,155,54,C.ink);
}

// Retain all four source slides and their title shapes; remove dense bodies.
for(let i=0;i<4;i++){
 const e=originals[i], sl=p.resolve(e.id);
 const shapeEntries=entries.filter(v=>v.slide===i+1 && ['shape','textbox'].includes(v.kind));
 const heading=shapeEntries.find(v=>v.placeholder==='title');
 for(const sh of shapeEntries) if(sh.id!==heading?.id) p.resolve(sh.id).delete();
 sl.background.fill=C.paper;
 sl._courseTitle=heading ? p.resolve(heading.id) : undefined;
}
{
 const sl=p.resolve(originals[0].id);
 sl.background.fill='linear(145deg, #FF9C8D 0%, #F7B6A4 100%)';
 style(sl._courseTitle,'Numerical methods\nand deep learning',128,270,2270,445,136,C.ink,true);
 text(sl,'Phase-field fracture and differentiable simulation',136,860,2160,130,58,C.ink);
 text(sl,'Presented by\nSathiskumar A. Ponnusami',136,1090,2100,142,47,C.ink);
 text(sl,'Queen Mary University of London · CEMS-Lab\nPrepared for the UKACM Autumn School 2026',136,1270,2250,110,31,C.ink);
 note(sl,'Numerical methods and deep learning',lectureNotes['Numerical methods and deep learning'],'User-created Physics Constrained Differentiable Solver Key Points.key, exported 9 September 2026.');
}
{
 const sl=p.resolve(originals[1].id);title(sl,'What learning can contribute',sl._courseTitle);
 row(sl,410,'Approximation','Represent a complex relation between inputs and physical responses.');
 row(sl,675,'Repeated queries','Amortise a training investment across many suitable predictions.');
 row(sl,940,'A learned component','Propose a material response or a correction inside a numerical method.');
 footer(sl,2,'Compare data generation, training, prediction and correction costs separately.');
 note(sl,'What learning can contribute',lectureNotes['What learning can contribute'],'Course source/book/06_learning_adapter.md; Physics-Based Deep Learning, https://physicsbaseddeeplearning.org/diffphys.html');
}
{
 const sl=p.resolve(originals[2].id);title(sl,'What a prediction must satisfy',sl._courseTitle);
 row(sl,410,'Physical conditions','Boundary conditions, balance laws and admissible material states.');
 row(sl,675,'Numerical accuracy','Discretisation error, solver tolerance and the chosen observation.');
 row(sl,940,'Use beyond training','Unseen loads, geometries and material parameters require evaluation.');
 footer(sl,3,'Assess prediction accuracy and physical consistency separately.');
 note(sl,'What a prediction must satisfy',lectureNotes['What a prediction must satisfy'],'Course source/book/06_learning_adapter.md.');
}
{
 const sl=p.resolve(originals[3].id);title(sl,'Coupling a network and a solver',sl._courseTitle);
 text(sl,'Prediction with a learned component',128,380,2260,85,53,C.ink,true);
 const a=box(sl,'Physical state',128,510), b=box(sl,'Learned proposal',858,510), c=box(sl,'Solver + checks',1588,510,710);
 arrow(sl,a,b);arrow(sl,b,c);
 text(sl,'Training through the numerical response',128,820,2260,90,53,C.ink,true);
 const d=box(sl,'Model weights',128,950), e=box(sl,'Differentiable solve',858,950,600),f=box(sl,'Observation loss',1708,950,590);
 arrow(sl,d,e);arrow(sl,e,f);
 text(sl,'Backward sensitivity: loss → solve → model weights',128,1130,2260,80,44,C.orange);
 footer(sl,4,'Blue: forward evaluation. Orange: backward sensitivity. Each interface has a contract.');
 note(sl,'Coupling a network and a solver',lectureNotes['Coupling a network and a solver'],'Original diagram; course source/book/06_learning_adapter.md; https://physicsbaseddeeplearning.org/diffphys.html');
}
{
 const sl=fresh('The six-hour learning sequence');
 text(sl,'Lecture questions',128,350,850,90,56,C.blue,true);text(sl,'Practical evidence',1200,350,1160,90,56,C.orange,true);
 for(const [y,l,r] of [[525,'1. Fracture and numerical solution','1. A small PhAST forward calculation'],[765,'2. Differentiation through a solve','2. A checked sensitivity and recovery'],[1005,'3. Learning inside numerical methods','3. Train, reload and assess a proposal']]){
  text(sl,l,128,y,980,150,50);text(sl,r,1200,y,1160,150,50);
 }
 footer(sl,5,'Three lecture hours, followed by three practical hours.');
 note(sl,'The six-hour learning sequence',lectureNotes['The six-hour learning sequence'],'COURSE_PLAN.md; TEACHING_SCHEDULE.md; MVP_DELIVERY.md.');
}
{
 const sl=fresh('A crack represented by a damage field');
 await eq(sl,'damage_convention',128,335,1740,120);
 await eq(sl,'energy',128,520,2260,185);
 await eq(sl,'crack_cost',128,795,1780,185);
 text(sl,'Stored elastic energy',128,1090,690,85,47,C.blue);
 text(sl,'Regularised crack cost',890,1090,690,85,47,C.orange);
 text(sl,'External work',1750,1090,620,85,47,C.muted);
 footer(sl,6,'Illustrative isotropic AT2 energy; tension/compression splits are a separate modelling choice.');
 note(sl,'A crack represented by a damage field',lectureNotes['A crack represented by a damage field'],'Course source/book/02_phase_field_energy.md; Miehe et al. (2010), https://doi.org/10.1002/nme.2861; Bourdin et al. (2000), https://doi.org/10.1016/S0022-5096(99)00028-9.');
}
{
 const sl=fresh('How damage changes stiffness');
 await pic(sl,path.join(figures,'degradation.png'),128,360,1295,755,'Analytic degradation functions: quadratic baseline, cubic and rational illustrations.');
 await eq(sl,'degradation',1510,470,875,180);
 await eq(sl,'local_gradient',1510,730,875,170);
 text(sl,'Predict the sign of the derivative.\nWhat changes near complete damage?',1510,990,875,170,46);
 footer(sl,7,'Quadratic baseline with illustrative cubic and rational alternatives.');
 note(sl,'How damage changes stiffness',lectureNotes['How damage changes stiffness'],'Original course figure build_beamer_figures.py and latex_figures/analytic_plot_data.json; public PhAST quadratic law pinned f6324f899f0701769810be117f27f1208f7a582e.');
}
{
 const sl=fresh('The staggered solution');
 text(sl,'At a fixed load increment, update one coupled field at a time.',128,355,2230,125,56);
 const a=box(sl,'Mechanics',128,655,560,155),b=box(sl,'Driving energy',980,655,560,155),c=box(sl,'Damage',1832,655,560,155);
 arrow(sl,a,b);arrow(sl,b,c);
 text(sl,'Hold damage fixed',128,890,560,95,43,C.blue);
 text(sl,'Update the history',980,890,660,95,43,C.blue);
 text(sl,'Enforce admissibility',1800,890,640,95,43,C.blue);
 text(sl,'Repeat with the updated damage until the chosen convergence checks pass.',128,1090,2240,145,50,C.orange);
 footer(sl,8,'Load increment, staggered iteration and physical time are different indices.');
 note(sl,'The staggered solution',lectureNotes['The staggered solution'],'Course source/book/03_staggered_solution.md; vendor/PhAST/src/phast/solvers/staggered.py.');
}
{
 const sl=fresh('Finite elements as tensor operations');
 const labels=['Gather nodal values','Element kernels','Quadrature reduction','Scatter contributions'];
 const nodes=labels.map((v,i)=>box(sl,v,128+i*598,500,495,200));
 for(let i=0;i<3;i++)arrow(sl,nodes[i],nodes[i+1]);
 text(sl,'Element, quadrature and component axes express the numerical structure.',128,860,2270,150,58);
 text(sl,'The same operations can expose derivatives when the computational path supports them.',128,1080,2250,140,51,C.blue);
 footer(sl,9,'Differentiability depends on the operations along the computational path.');
 note(sl,'Finite elements as tensor operations',lectureNotes['Finite elements as tensor operations'],'Course source/book/04_fem_to_tensors.md; public PhAST source pin f6324f899f0701769810be117f27f1208f7a582e.');
}
{
 const sl=fresh('From an input to a final observation');
 await eq(sl,'state_step',128,370,2200,175);
 const a=box(sl,'',128,720,540),b=box(sl,'',926,720,540),c=box(sl,'',1724,720,620);
 await eq(sl,'state_zero',146,737,504,85);await eq(sl,'state_one',944,737,504,85);await eq(sl,'state_final',1742,737,584,85);
 arrow(sl,a,b);arrow(sl,b,c);
 text(sl,'Input: a material parameter, a load parameter or model weights',128,1010,2260,90,52,C.blue);
 text(sl,'Observation: a fixed map from the final state to the measured quantities',128,1140,2260,90,49);
 footer(sl,10,'Differentiate the final scalar loss with respect to a defined input.');
 note(sl,'From an input to a final observation',lectureNotes['From an input to a final observation'],'Course source/book/05a_backpropagation_step_by_step.md; https://physicsbaseddeeplearning.org/diffphys.html.');
}
{
 const sl=fresh('The backward pass through time steps');
 await eq(sl,'jacobians',128,345,1660,150);
 await eq(sl,'adjoint',128,605,2270,180);
 await eq(sl,'gradient_sum',128,930,1100,195);
 text(sl,'Each use of the same parameter\ncontributes to the final gradient.',1330,930,1010,180,54,C.orange);
 footer(sl,11,'Fixed initial state and observation map; parameter dependence enters through the updates.');
 note(sl,'The backward pass through time steps',lectureNotes['The backward pass through time steps'],'Original course derivation source/book/05a_backpropagation_step_by_step.md; PyTorch autograd documentation; https://physicsbaseddeeplearning.org/diffphys.html.');
}
{
 const sl=fresh('Implicit differentiation of a solved equation');
 await eq(sl,'implicit',128,425,2290,230);
 row(sl,820,'Forward calculation','Find a converged state satisfying the residual equation.');
 row(sl,1050,'Backward calculation','Solve the transposed sensitivity system, then form the parameter derivative.');
 footer(sl,12,'Requires a differentiable residual and a locally nonsingular state Jacobian.');
 note(sl,'Implicit differentiation of a solved equation',lectureNotes['Implicit differentiation of a solved equation'],'Course source/book/05_differentiation_and_inverse.md; Ceyron adjoint_linear_system_example.py, commit a2e50a9df4bb6e938901b33fd957c06ac06b5224, pedagogical reference only.');
}
{
 const sl=fresh('Check the derivative before using it');
 await eq(sl,'finite_difference',128,370,1850,180);
 row(sl,725,'Automatic differentiation','Differentiate the implemented computation.');
 row(sl,925,'Independent check','Use an analytical expression or a hand-written adjoint.');
 row(sl,1120,'Finite differences','Compare several spacings at the same physical state.');
 note(sl,'Check the derivative before using it',lectureNotes['Check the derivative before using it'],'Course notebooks/02_degradation_autograd.ipynb; new diffusion draft; https://docs.pytorch.org/docs/stable/notes/autograd.html.');
}
{
 const sl=fresh('A small time-stepping notebook');
 await eq(sl,'diffusion',128,380,2220,185);
 await eq(sl,'diffusion_glossary',128,670,2250,140);
 text(sl,'Plot a forward trajectory.\nDifferentiate a terminal observation.\nCompare AD, manual reverse mode and finite differences.\nRecover a synthetic parameter.',128,905,2280,305,53);
 footer(sl,14,'One-dimensional diffusion provides a compact example of time-step differentiation.');
 note(sl,'A small time-stepping notebook',lectureNotes['A small time-stepping notebook'],'notebooks/drafts/06_differentiability_step_by_step.ipynb; original code. Cell sequencing inspired by Felix Köhler, hybridization-in-jax/first_data_assimilation.ipynb at61ee2629f5800d92fba64492a0f81efe3a6a7c39; no code copied.');
}
{
 const sl=fresh('A mesh, a prescribed notch and boundary values');
 await pic(sl,path.join(assets,'teaching_bcs.png'),128,375,1620,750,'Illustrative coarse mesh. Locked nodal damage notch; top and bottom vertical displacement; horizontal displacement fixed on all outer edges.');
 text(sl,'Represent the notch by\nprescribing fully damaged\nnodes on the intact mesh.',1830,455,600,300,50,C.orange);
 text(sl,'Inspect every boundary set\nand displacement component\nbefore solving.',1830,920,600,200,48);
 footer(sl,15,'Diagram uses a coarse mesh; the actual quick run has 8,385 nodes and 16,384 triangles.');
 note(sl,'A mesh, a prescribed notch and boundary values',lectureNotes['A mesh, a prescribed notch and boundary values'],'Original BC schematic based on notebooks/day2_helpers/course_tools.py and public symmetric_tension_bcs; no new fracture solve.');
}
{
 const sl=fresh('Read the field as well as the response');
 await pic(sl,path.join(figures,'phast_evolution.png'),128,480,2304,600,'Retained PhAST fields: seeded precrack, first increment and final increment; common damage colour scale.');
 text(sl,'Separate the prescribed seed, its diffuse profile and subsequent damage change.',128,1110,2260,120,51);
 footer(sl,16,'Quasistatic AT2 response: initial damage, diffuse regularisation and loading-induced change.');
 note(sl,'Read the field as well as the response',lectureNotes['Read the field as well as the response'],'source/slides/latex_figures/forward_fields.npz; forward_summary.json; evidence/notebook_runtime.json; evidence/package_rehearsal.json.');
}
{
 const sl=fresh('Keep a reproducible numerical experiment');
 row(sl,405,'Input specification','Geometry, connectivity, materials, boundary values and loading.');
 row(sl,650,'Numerical specification','Algorithm, precision, tolerances and failure conditions.');
 row(sl,895,'Saved evidence','Field arrays, response history, configuration and source revision.');
 text(sl,'Reload the saved data into fresh variables, then reproduce a plot.',128,1155,2260,100,54,C.orange);
 note(sl,'Keep a reproducible numerical experiment',lectureNotes['Keep a reproducible numerical experiment'],'source/planning/PRACTICAL_SEQUENCE_AUDIT_20260909.md; notebooks/day2_helpers/course_tools.py.');
}
{
 const sl=fresh('The practical learning cycle');
 text(sl,'Predict',128,405,680,100,74,C.blue,true);
 text(sl,'What should change, and in which direction?',960,410,1430,140,58);
 text(sl,'Compute',128,695,680,100,74,C.blue,true);
 text(sl,'Run one short, inspectable calculation.',960,700,1430,140,58);
 text(sl,'Explain',128,985,680,100,74,C.orange,true);
 text(sl,'Use a field, a response and an independent check.',960,990,1430,150,58);
 footer(sl,18,'Companion book, executable notebooks and worked solutions: CEMS-Lab autumn-school.');
 note(sl,'The practical learning cycle',lectureNotes['The practical learning cycle'],'Ceyron notebook references: source/planning/CEYRON_NOTEBOOK_DESIGN.md; D2L and Physics-Based Deep Learning supplied by the user as pedagogical references.');
}
await fs.mkdir(output,{recursive:true});
await fs.writeFile(path.join(build,'slide_manifest.json'),JSON.stringify(manifest,null,2));
await fs.writeFile(path.join(root,'source/slides/intro-lecture/speaker_notes.md'),manifest.map(m=>`## ${m.slide}. ${m.title}\n\n${m.notes}\n\n${m.source}\n`).join('\n'));
const candidatePath=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidatePath);
execFileSync(runtimePython,
 [path.join(root,'source/slides/intro-lecture/normalise_template_media.py'),candidatePath]);
execFileSync(runtimePython,
 [path.join(root,'source/slides/intro-lecture/stamp_metadata.py'),candidatePath]);
const sha=crypto.createHash('sha256').update(await fs.readFile(src)).digest('hex');
const result=await finalizePresentation({workspaceDir:root,candidatePath,
 finalPath:path.join(output,'phast_lecture_introduction_v7.pptx'),
 pythonExecutable:runtimePython,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','24384000,13716000','--validate-bullet-geometry','--validate-heading-fit'],
 explicitTotalSlideCount:18,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
 fontPolicy:{basis:'reference',families:[FF],referencePath:src,referenceSha256:sha},
 verifyArtifactToolImport:true,receiptPath:path.join(build,'presentation-v7.validation.json')});
console.log(JSON.stringify(result,null,2));

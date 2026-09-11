import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation, PresentationFile, FileBlob} from '@oai/artifact-tool';
import {finalizePresentation} from '/Users/allamaprabhuani/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations/container_tools/artifact_tool_utils.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../..');
const workspace = path.join(repo, 'reviews/master-lecture-20260912');
const draft = path.join(workspace, 'draft');
const output = path.join(workspace, 'output');
const skill = '/Users/allamaprabhuani/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations';
const python = '/Users/allamaprabhuani/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const assets = path.join(here, 'assets');
await fs.mkdir(draft, {recursive: true});
await fs.mkdir(output, {recursive: true});

const ink = '#17232D', blue = '#245A81', orange = '#C96824', teal = '#007E87', muted = '#576572', pale = '#EDF4F7';
const deck = Presentation.create({slideSize: {width: 1280, height: 720}});
const boxes = [];
function text(slide, name, value, x, y, w, h, size = 28, color = ink, bold = false, font = 'Arial', align = 'left') {
  const box = slide.shapes.add({name, geometry: 'textbox', position: {left: x, top: y, width: w, height: h}, fill: 'none', line: {fill: 'none', width: 0}});
  box.text = value;
  box.text.style = {typeface: font, fontSize: size, color, bold, autoFit: 'none', wrap: 'word', alignment: align, verticalAlignment: 'top', insets: {top: 0, bottom: 0, left: 0, right: 0}};
  boxes.push({slide: deck.slides.items.length, name, x, y, w, h, size, value});
  return box;
}
function rule(slide, y = 132) {
  slide.shapes.add({geometry: 'rect', position: {left: 72, top: y, width: 1136, height: 3}, fill: {color: orange}, line: {fill: 'none', width: 0}});
}
async function image(slide, file, x, y, w, h, alt) {
  const suffix = path.extname(file).toLowerCase();
  const contentType = suffix === '.jpg' || suffix === '.jpeg' ? 'image/jpeg' : 'image/png';
  slide.images.add({blob: new Uint8Array(await fs.readFile(file)), contentType, fit: 'contain', position: {left: x, top: y, width: w, height: h}, alt});
}
async function standard(title, subtitle, notes) {
  const s = deck.slides.add(); s.background.fill = '#FFFFFF';
  text(s, 'Title', title, 72, 34, 1040, 92, 38, ink, true);
  if (subtitle) text(s, 'Subtitle', subtitle, 72, 132, 1020, 50, 20, muted);
  rule(s, 186);
  await image(s, path.join(repo, 'source/slides/phast-overview/assets/logo.png'), 1144, 38, 64, 64, 'PhAST logo');
  text(s, 'Footer', 'CEMS-Lab · UKACM Autumn School 2026', 72, 677, 1000, 22, 16, muted);
  text(s, 'Page', String(deck.slides.items.length), 1168, 677, 40, 22, 16, muted, false, 'Arial', 'right');
  s.speakerNotes.textFrame.setText('Presented by Sathiskumar A. Ponnusami, Queen Mary University of London. Prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami, CEMS-Lab.\n\n' + notes);
  return s;
}
async function divider(number, title, sentence, background, notes) {
  const s = deck.slides.add(); s.background.fill = '#FFFFFF';
  await image(s, background, 580, 0, 700, 720, 'Computed PhAST visual used as a section backdrop.');
  s.shapes.add({geometry: 'rect', position: {left: 0, top: 0, width: 650, height: 720}, fill: {color: '#FFFFFF', transparency: 4}, line: {fill: 'none', width: 0}});
  text(s, 'Section', `SECTION ${number}`, 74, 123, 350, 34, 20, orange, true);
  text(s, 'Title', title, 72, 183, 528, 128, 48, ink, true);
  text(s, 'Sentence', sentence, 72, 350, 485, 96, 28, muted);
  text(s, 'Footer', 'CEMS-Lab · UKACM Autumn School 2026', 72, 677, 1000, 22, 16, muted);
  text(s, 'Page', String(deck.slides.items.length), 1168, 677, 40, 22, 16, muted, false, 'Arial', 'right');
  s.speakerNotes.textFrame.setText('Presented by Sathiskumar A. Ponnusami, Queen Mary University of London. Prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami, CEMS-Lab.\n\n' + notes);
  return s;
}

let s = await standard('Phase-field fracture and differentiable simulation with PhAST', 'UKACM Autumn School 2026 · six-hour lecture and notebook sequence', 'Opening slide. Introduce the course as an applied route from fracture modelling to differentiable simulation and machine-learning interfaces.');
text(s, 'Presented by', 'Presented by\nSathiskumar A. Ponnusami', 74, 203, 590, 84, 30, blue, true);
text(s, 'Affiliation', 'Queen Mary University of London · CEMS-Lab', 74, 304, 640, 39, 24, muted);
text(s, 'Prepared by', 'Prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami', 74, 565, 770, 31, 20, muted);
await image(s, path.join(repo, 'assets/propagation_review/plate_crossing_poster.png'), 680, 178, 520, 330, 'Dynamic phase-field crack propagation in the compact plate demonstrator.');
text(s, 'Caption', 'Computed phase-field fracture trajectory', 760, 525, 365, 24, 18, orange, true, 'Arial', 'center');

s = await standard('One master deck, three connected sections', 'The extended scaffold and specialist modules remain available as insertable teaching resources.', 'Explain that this deck is the standard presentation entry point. The 90-slide outline provides the long-form delivery structure; short specialist decks provide selectable inserts.');
const lanes = [
  ['01', 'Phase-field fracture', 'Energy, degradation, discretisation, and a compact dynamic run.'],
  ['02', 'Differentiability', 'Forward evaluation, local sensitivities, reverse accumulation, and recovery.'],
  ['03', 'Learning interfaces', 'Train, save, reload, audit, and couple a learned component.'],
];
for (let i = 0; i < lanes.length; i++) {
  const x = 82 + i * 377;
  s.shapes.add({geometry: 'rect', position: {left: x, top: 205, width: 334, height: 280}, fill: {color: i === 1 ? '#FFF4E9' : pale}, line: {color: i === 1 ? orange : '#C7D8E2', width: 1}});
  text(s, 'Number', lanes[i][0], x + 25, 230, 285, 42, 32, i === 1 ? orange : blue, true);
  text(s, 'Lane title', lanes[i][1], x + 25, 286, 280, 62, 28, ink, true);
  text(s, 'Lane description', lanes[i][2], x + 25, 367, 275, 85, 20, muted);
}

await divider('01', 'Phase-field fracture and the PhAST workflow', 'Represent fracture by a smooth damage field, then resolve coupled mechanics and damage.', path.join(repo, 'assets/propagation_review/plate_crossing_poster.png'), 'Section divider. Ask students to predict where damage will extend before showing the next slide.');

s = await standard('A compact dynamic plate produces a visible fracture trajectory', 'The visual shows a computed diffuse damage field; the bright core is highlighted without reinterpreting it as a sharp crack.', 'Walk left-to-right through the four snapshots. Damage is d=0 in intact material and d=1 in fully damaged material. The high-damage core is a display aid defined by d greater than or equal to 0.95.');
await image(s, path.join(assets, 'b3_damage_snapshots.png'), 72, 205, 1136, 342, 'Four snapshots of the dynamic phase-field plate run.');
text(s, 'Caption', 'Damage field:  d = 0 intact  ·  d = 1 fractured  ·  high-damage core shown at d ≥ 0.95', 104, 570, 1072, 31, 20, orange, true, 'Arial', 'center');

s = await standard('Fields, boundary conditions, and energy checks stay connected', 'Notebook 01 gives each setup action an immediately visible outcome.', 'Use the left panel to introduce geometry, notch, mesh, and boundary condition labels. Use the right panel to explain that results are interpreted using both fields and energy histories.');
await image(s, path.join(assets, 'b3_mesh_boundary_conditions.png'), 72, 205, 544, 329, 'Mesh and boundary condition plot for the compact dynamic fracture plate.');
await image(s, path.join(assets, 'b3_energy_history.png'), 664, 205, 544, 329, 'Energy history for the compact dynamic fracture plate.');

await divider('02', 'Differentiability, sensitivities, and inverse questions', 'A scalar objective can send information back through tensor operations to the parameters that shaped the response.', path.join(assets, 'autodiff_forward_reverse.png'), 'Section divider. Emphasise that the section begins with a small damaged-bar example before returning to the solver-scale setting.');

s = await standard('From a measured force mismatch to input gradients', 'The toy damaged bar keeps the chain rule visible before students encounter solver-scale tensors.', 'Read the forward path first: prescribed displacement and damage determine force and loss. Then read the reverse path: the scalar loss sends derivatives back to the shared inputs. This is the same computational principle used by PyTorch autograd in the solver.');
await image(s, path.join(assets, 'autodiff_forward_reverse.png'), 72, 205, 1136, 400, 'Forward and reverse computation graph for the local damaged-bar force mismatch.');

s = await standard('Local derivatives retain physical interpretation', 'At fixed damage, displacement raises force; at fixed displacement, damage lowers the retained stiffness and force.', 'Use this plot to interpret derivative signs before discussing numerical gradient checks and inverse recovery. The illustrated points are dimensionless teaching values, not a calibration result.');
await image(s, path.join(assets, 'autodiff_force_sensitivities.png'), 72, 205, 1136, 400, 'Force sensitivities to displacement and damage in the damaged-bar teaching example.');

await divider('03', 'Learning interfaces and hybrid simulation', 'A learned model can be inserted at a defined interface, trained against data, and audited against a physics-based reference.', path.join(assets, 'learning_interface.png'), 'Section divider. State that a learned component is an explicit proposal inside an auditable workflow, not a replacement for the problem definition.');

s = await standard('A learning workflow has a clear hand-off and a clear check', 'Notebook 03 trains a toy field predictor, reloads it, then evaluates the prediction against a reference.', 'Use this as the bridge to model modularity. The notebook can be extended from the small MLP to an RBF model, GNN, GNO, or CNN provided the input-output interface and verification remain explicit.');
await image(s, path.join(assets, 'training_history.png'), 72, 222, 515, 286, 'Recorded training and validation history from the classroom learning notebook.');
await image(s, path.join(assets, 'heldout_field.png'), 630, 222, 578, 286, 'Held-out field comparison from the classroom learning notebook.');
text(s, 'Learning caption', 'Training history', 72, 538, 515, 25, 20, orange, true, 'Arial', 'center');
text(s, 'Field caption', 'Held-out reference, reloaded MLP, compatible baseline, and error', 630, 538, 578, 25, 18, orange, true, 'Arial', 'center');

s = await standard('Dynamic branching is a recorded reference exhibit', 'A separate PhAST example illustrates branching; it is retained as a media insert rather than presented as a classroom runtime target.', 'This slide distinguishes the two-minute classroom B3 run from the higher-complexity B7 branching reference. The B7 media originates from the pinned public PhAST example recorded in the asset source record.');
await image(s, path.join(repo, 'source/slides/phast-overview/assets/branching.png'), 108, 205, 1064, 370, 'Recorded dynamic crack branching exhibit from the public PhAST B7 example.');
text(s, 'Caption', 'Reference exhibit: dynamic crack branching · use MP4/GIF during delivery when supported', 122, 594, 1036, 28, 20, orange, true, 'Arial', 'center');

s = await standard('Continue from a working course site and three short notebooks', 'The web edition carries the course narrative; notebooks provide the reproducible practical route.', 'Closing slide. Invite students to use the live book, download the notebooks, and open an issue or discussion after the school. The QR code points to the public PhAST repository.');
text(s, 'Takeaways', '• Phase field provides a regularised fracture representation.\n• Tensor operations enable differentiation through a simulation workflow.\n• Verified interfaces let learning components enter the workflow responsibly.', 72, 194, 738, 260, 28, ink);
await image(s, path.join(repo, 'source/slides/phast-overview/assets/repository_qr.png'), 892, 192, 215, 215, 'QR code for the PhAST repository.');
text(s, 'URL', 'cems-lab.github.io/autumn-school', 828, 449, 344, 32, 21, blue, true, 'Arial', 'center');

const candidate = path.join(draft, 'candidate.pptx');
const final = path.join(output, 'PhAST_UKACM_Autumn_School_2026_Master_v4.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidate);
await finalizePresentation({workspaceDir: workspace, candidatePath: candidate, finalPath: final, pythonExecutable: python,
  integrityValidatorPath: path.join(skill, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skill, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-bullet-geometry', '--validate-heading-fit'],
  explicitTotalSlideCount: 12, fontPolicy: {basis: 'design', families: ['Arial']}, verifyArtifactToolImport: true,
  receiptPath: path.join(draft, 'validation-v4.json')});
await fs.writeFile(path.join(draft, 'shape_boxes.json'), JSON.stringify(boxes, null, 2));
const checked = await PresentationFile.importPptx(await FileBlob.load(final));
const preview = path.join(workspace, 'preview'); await fs.mkdir(preview, {recursive: true});
for (let i = 0; i < checked.slides.items.length; i++) {
  const png = await checked.export({slide: checked.slides.items[i], format: 'png', scale: 1});
  await fs.writeFile(path.join(preview, `slide-${i + 1}.png`), new Uint8Array(await png.arrayBuffer()));
}
console.log(final);

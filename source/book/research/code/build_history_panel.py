"""Export retained FEM fields and a self-contained interactive teaching panel on HPC."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as tri

parser=argparse.ArgumentParser()
parser.add_argument("--inputs",type=Path,required=True)
parser.add_argument("--template",type=Path,required=True)
parser.add_argument("--output",type=Path,required=True)
a=parser.parse_args()
a.output.mkdir(parents=True,exist_ok=False)
start=time.monotonic()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
nodes=np.load(a.inputs/"mesh_nodes.npy",allow_pickle=False)
elements=np.load(a.inputs/"mesh_elements.npy",allow_pickle=False)
archive=np.load(a.inputs/"truth_damage_snapshots.npz",allow_pickle=False)
steps=archive["snapshot_steps"].astype(int)
fields=archive["snapshots"]
particle=json.loads((a.inputs/"particle_params.json").read_text())
target=np.load(a.inputs/"blind_temporal_target_snapshots.npy",allow_pickle=False)
target_steps=np.load(a.inputs/"blind_temporal_iter_pred_steps.npy",allow_pickle=False)
assert fields.shape==(len(steps),len(nodes))
assert np.isfinite(fields).all() and fields.min()>=-1e-8 and fields.max()<=1+1e-8
matches=[np.max(np.abs(fields[np.where(steps==step)[0][0]]-target[k]))
         for k,step in enumerate(target_steps)]
assert max(matches)<1e-12, matches
conversion=float(np.max(np.abs(fields-fields.astype(np.float32).astype(float))))
assert conversion<3.1e-8
mesh=tri.Triangulation(nodes[:,0],nodes[:,1],elements)
pictures={}
for name,cmap in [("plate","Greys"),("damage","inferno")]:
    pictures[name]=[]
    for field in fields:
        fig=plt.figure(figsize=(4,4),dpi=144,facecolor="white")
        ax=fig.add_axes([0,0,1,1])
        ax.tripcolor(mesh,field,shading="gouraud",cmap=cmap,vmin=0,vmax=1,rasterized=True)
        ax.set(xlim=(0,40),ylim=(0,40),aspect="equal")
        ax.axis("off")
        stream=io.BytesIO()
        fig.savefig(stream,format="png",dpi=144,facecolor="white")
        plt.close(fig)
        pictures[name].append("data:image/png;base64,"+base64.b64encode(stream.getvalue()).decode())
def pack(x):
    return base64.b64encode(np.asarray(x,dtype="<f4").tobytes()).decode()
luts={}
for name,cmap in [("plate","Greys"),("damage","inferno")]:
    luts[name]=[matplotlib.colors.to_hex(c) for c in plt.get_cmap(cmap)(np.linspace(0,1,64))]
payload={"steps":steps.tolist(),"nodeCount":len(nodes),"nodes":pack(nodes[:,:2]),
         "damage":pack(fields),"pictures":pictures,"luts":luts,
         "width":40,"height":40,"sourceKind":"Retained PhAST FEM damage; no new forward solve",
         "energyHistoryAvailable":False,"float32MaximumError":conversion,
         "maximumSelectedFrameDifference":float(max(matches)),
         "minimumRecordedDamageIncrement":float(np.diff(fields,axis=0).min()),
         "particle":{"center":particle["truth_center"],"radius":particle["radius_mm"]}}
template=a.template.read_text()
assert template.count("__PAYLOAD__")==1
output=template.replace("__PAYLOAD__",json.dumps(payload,separators=(",",":")))
(a.output/"history_plate.html").write_text(output)
np.savez_compressed(a.output/"history_plate_arrays.npz",nodes=nodes,elements=elements,
                    steps=steps,damage=fields)
receipt={"scope":payload["sourceKind"],"job":os.environ.get("SLURM_JOB_ID"),
         "frames":len(steps),"nodes":len(nodes),"elements":len(elements),
         "selected_frame_difference":float(max(matches)),
         "float32_maximum_error":conversion,
         "minimum_recorded_damage_increment":payload["minimumRecordedDamageIncrement"],
         "energy_and_history_fields_retained":False,
         "rendering":"Full d in [0,1]; linear FEM colour interpolation; no masking or artificial crack line",
         "source_hashes":{Path(__file__).name:sha(Path(__file__)),a.template.name:sha(a.template)},
         "input_hashes":{p.name:sha(p) for p in sorted(a.inputs.iterdir())},
         "outputs":{p.name:sha(p) for p in sorted(a.output.iterdir())},
         "seconds":time.monotonic()-start,"numpy":np.__version__,"matplotlib":matplotlib.__version__}
(a.output/"history_plate_manifest.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))

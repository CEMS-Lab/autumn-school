"""Build an offline gallery/player from already rendered course animations.

Reuse local MP4 assets and validate their encoding and complete decoding.
"""
from pathlib import Path
import hashlib
import html
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "animations"
ITEMS = [
    {
        "id": "phase-field",
        "title": "A sharp crack and its diffuse representation",
        "video": "mechanics/phase_field_band.mp4",
        "poster": "mechanics/phase_field_band_poster.png",
        "slot": "L1: energy and regularisation",
        "description": "An isolated analytic AT2 profile connects the damage field to the regularisation length. Increasing the length spreads the band.",
        "question": "If the regularisation length decreases, what must change in the mesh to resolve the damage band?",
        "answer": "The mesh must be refined relative to the length scale and its adequacy checked. The animation varies the regularisation length of an analytic isolated AT2 profile.",
        "steps": ["A sharp crack marks a discontinuity.", "A continuous damage field represents that crack.", "The isolated AT2 profile decays away from the crack.", "The regularisation length sets the width of the diffuse damage band."],
        "limit": "Analytic isolated AT2 damage profile, with a fixed crack centre and varied regularisation length."
    },
    {
        "id": "partitioned-step",
        "title": "Explicit mechanics and implicit damage",
        "video": "mechanics/explicit_implicit_step.mp4",
        "poster": "mechanics/explicit_implicit_step_poster.png",
        "slot": "L1: numerical solution",
        "description": "One partitioned physical time step uses accepted damage for explicit mechanics, updates the driving quantity, and solves damage implicitly.",
        "question": "Which stability requirement governs the explicit mechanics update?",
        "answer": "Choose the mechanics timestep according to its explicit stability requirements. Accept the state after the stated checks pass; on failure, stop or reduce the timestep and restart from the accepted state.",
        "steps": ["Begin at an accepted time level.", "Update mechanics with lagged damage.", "Evaluate the tensile driving/history quantity.", "Solve the implicit damage problem with irreversibility.", "Check residuals, bounds and energy; accept or stop/reduce the timestep."],
        "limit": "Dynamic splitting schematic. The PhAST classroom notebook uses quasistatic mechanics."
    },
    {
        "id": "reverse-mode",
        "title": "Backpropagation through several updates",
        "video": "learning/reverse_accumulation.mp4",
        "poster": "learning/reverse_accumulation.png",
        "slot": "L2: the chain rule",
        "description": "States move forward through two update maps. Adjoint sensitivities move backward and each use of the shared parameter contributes to its gradient.",
        "question": "Why does the parameter gradient contain a contribution from each update?",
        "answer": "The same parameter enters both maps. The chain rule adds both paths to the loss. Here the initial state is fixed and the loss depends on the final state. Parameter-dependent initial states or explicit parameter dependence in the loss contribute additional terms.",
        "steps": ["Specify a fixed initial state and a shared parameter.", "Evaluate two differentiable update maps and a scalar final loss.", "Propagate the final-state adjoint backward.", "Sum the parameter contribution from every update.", "An optimiser chooses a separate update using the resulting gradient."],
        "limit": "Computational-graph schematic. Assumes differentiable maps, fixed initial state and a final-state-only loss."
    },
    {
        "id": "learned-proposal",
        "title": "A learned proposal and a checked correction",
        "video": "learning/checked_learned_proposal.mp4",
        "poster": "learning/checked_learned_proposal.png",
        "slot": "L3 / P3: hybrid methods",
        "description": "A compatible Radius-GNO or GNN produces a proposed damage field. Acceptance depends on declared bounds, residuals and constraints.",
        "question": "When can a corrected proposal be accepted?",
        "answer": "Accept the corrected state when it passes the declared checks. If correction fails, stop and report nonconvergence. Assess interface compatibility, field quality and complete computational cost for the chosen architecture.",
        "steps": ["Declare mesh/graph, feature ordering, units and normalisation.", "Evaluate a compatible model and obtain a proposal.", "Check bounds, irreversibility and the declared residual/constraint tolerance.", "Accept a qualified state or use reference correction.", "Recheck the correction and accept or report failure; include all overhead in any speed comparison."],
        "limit": "Interface schematic for a compatible learned proposal, declared numerical checks and reference correction."
    }
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def markdown_cell(text, name):
    return {"cell_type": "markdown", "id": name, "metadata": {}, "source": text.splitlines(keepends=True)}

def code_cell(text, name):
    return {"cell_type": "code", "id": name, "execution_count": None, "metadata": {}, "outputs": [], "source": text.splitlines(keepends=True)}

def main():
    records, sections = [], []
    cells = [markdown_cell(
        "# Phase-field fracture: animated explanations\n\n"
        "Four short original Manim clips support the lecture and practicals. "
        "Run the player cells in the complete animation kit or repository. "
        "The player cells display the supplied local videos. "
        "Try each question before revealing its worked answer. "
        "MP4 playback depends on the notebook front end; use index.html or the poster if necessary.",
        "introduction")]
    cells.append(code_cell(
        "from pathlib import Path\nfrom IPython.display import Video, display\n\n"
        "candidates = [Path.cwd(), Path.cwd() / 'assets' / 'animations']\n"
        "animation_root = next((p for p in candidates if (p / 'mechanics' / 'phase_field_band.mp4').is_file()), None)\n"
        "if animation_root is None:\n"
        "    raise FileNotFoundError('Open this notebook in the complete animation-kit folder or course repository root, including the MP4 files.')\n"
        "print('Ready: local animation files found for playback.')",
        "setup"))
    for item in ITEMS:
        video, poster = OUT / item["video"], OUT / item["poster"]
        if not video.is_file() or not poster.is_file():
            raise FileNotFoundError(str(video if not video.is_file() else poster))
        probe = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate",
            "-of", "json", str(video)
        ]))
        stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
        duration = float(probe["format"]["duration"])
        assert duration < 35 and stream["width"] == 1280 and stream["height"] == 720
        assert stream["codec_name"] == "h264" and stream["pix_fmt"] == "yuv420p"
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=True)
        records.append({**item, "duration_seconds": duration, "stream": stream,
                        "video_sha256": digest(video), "poster_sha256": digest(poster)})
        esc = html.escape
        steps = "".join("<li>" + esc(s) + "</li>" for s in item["steps"])
        caption_file = Path(item["video"]).with_suffix(".vtt")
        track = (
            f'<track kind="captions" src="{caption_file.as_posix()}" srclang="en" label="English">'
            if (OUT / caption_file).is_file() else ""
        )
        sections.append(f"""
<section id="{item['id']}">
  <p class="placement">{esc(item['slot'])} · {duration:g} seconds</p>
  <h2>{esc(item['title'])}</h2>
  <p>{esc(item['description'])}</p>
  <figure>
    <video controls playsinline preload="metadata" poster="{item['poster']}"
      aria-label="{esc(item['title'])}" aria-describedby="{item['id']}-caption">
      <source src="{item['video']}" type="video/mp4">
      {track}
      Use the MP4 download or still frame below for alternative playback and reading.
    </video>
    <img class="print-poster" src="{item['poster']}" alt="{esc(item['title'])}. {esc(item['limit'])}">
    <figcaption id="{item['id']}-caption">{esc(item['limit'])}</figcaption>
  </figure>
  <p class="downloads"><a href="{item['video']}" download>Download MP4</a>
    <a href="{item['poster']}" download>Download still frame</a></p>
  <p><strong>Question.</strong> {esc(item['question'])}</p>
  <details><summary>Worked answer</summary><p>{esc(item['answer'])}</p></details>
  <details><summary>Text description of the animation</summary><ol>{steps}</ol></details>
</section>""")
        cells.append(markdown_cell(
            "## " + item["title"] + "\n\n" + item["description"] + "\n\n"
            "**Scope:** " + item["limit"] + "\n\n**Question:** " + item["question"],
            item["id"] + "-question"))
        cells.append(code_cell(
            "display(Video(str(animation_root / " + repr(item["video"]) + "), embed=True, width=960, html_attributes='controls playsinline'))",
            item["id"] + "-player"))
        cells.append(markdown_cell(
            "<details><summary>Worked answer</summary>\n\n" + item["answer"] +
            "\n\n</details>\n\n**Animation description**\n\n" +
            "\n".join(str(n + 1) + ". " + s for n, s in enumerate(item["steps"])),
            item["id"] + "-answer"))
    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Phase-field fracture: animated explanations</title>
<style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;color:#17212a;background:#fff;font:18px/1.6 Arial,sans-serif}
main{max-width:1040px;margin:auto;padding:36px 24px 60px}h1{font-size:clamp(28px,4vw,42px);line-height:1.16;margin:0 0 18px}
h2{font-size:clamp(23px,3vw,31px);line-height:1.2;margin:6px 0 12px}p{max-width:82ch}a{color:#245a81;text-underline-offset:3px}
nav{display:flex;flex-wrap:wrap;gap:8px 20px;margin:24px 0}section{padding:32px 0;border-top:1px solid #d8e0e5}
.placement,figcaption{color:#4f5b63;font-size:16px}figure{margin:20px 0 10px}video{display:block;width:100%;aspect-ratio:16/9;background:white}
figcaption{padding-top:10px}.print-poster{display:none}.downloads{display:flex;gap:24px;flex-wrap:wrap}details{margin:16px 0}summary{cursor:pointer;color:#245a81}
:focus-visible{outline:3px solid #087f82;outline-offset:4px}footer{border-top:1px solid #d8e0e5;padding-top:24px;font-size:16px}
@media(max-width:480px){main{padding:22px 16px}body{font-size:17px}}
@media print{video{display:none}.print-poster{display:block;width:100%}details{display:block}section{break-inside:avoid}nav,.downloads{display:none}}
</style></head><body><main>
<header><h1>Phase-field fracture: animated explanations</h1>
<p>Four short animations connect fracture representation, numerical updates, sensitivities and learned proposals.
Pause at each stage and explain the quantities before continuing.</p>
<p>On a small screen, use fullscreen playback to read mathematical labels.</p>
<p>All clips are silent, original teaching diagrams of an analytic profile and computational algorithms.</p>
<p><a href="animation_gallery.ipynb" download>Download the player notebook with questions and worked answers</a></p>
<nav aria-label="Animation topics">"""
    page += "".join(f'<a href="#{i["id"]}">{html.escape(i["title"])}</a>' for i in ITEMS)
    page += "</nav></header>" + "".join(sections)
    page += """<footer><p>For PowerPoint or Keynote, insert a local MP4 as a video and choose click-to-play.
Keep its scope caption on the slide. Use the PNG still for print or unsupported playback.
Rehearse playback in your presentation software before teaching.</p>
<p>The complete animation kit includes editable Manim source, rebuild instructions and mathematical teaching notes.
The clips use the course's original academic diagram style.</p></footer></main></body></html>"""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(page)
    notebook = {"cells": cells, "metadata": {"kernelspec": {
        "display_name": "Python 3", "language": "python", "name": "python3"
    }, "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
    (OUT / "animation_gallery.ipynb").write_text(json.dumps(notebook, indent=2) + "\n")
    manifest = {"kind": "Original Manim teaching diagrams and local media metadata",
                "videos": records,
                "gallery_sha256": digest(OUT / "index.html"),
                "player_notebook_sha256": digest(OUT / "animation_gallery.ipynb")}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"videos": len(records), "seconds": [r["duration_seconds"] for r in records],
                      "codec_and_decode_checks": "passed", "gallery": str(OUT / "index.html")}, indent=2))

if __name__ == "__main__":
    main()

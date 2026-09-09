/* Progressive enhancement: answers remain ordinary visible text without JS. */
(() => {
  function enhance() {
    document.querySelectorAll(".admonition.dropdown").forEach(panel => {
      if (panel.dataset.solutionEnhanced) return;
      const title = panel.querySelector(":scope > .admonition-title");
      if (!title) return;
      panel.dataset.solutionEnhanced = "true";
      const details = document.createElement("details");
      details.className = "worked-answer";
      const summary = document.createElement("summary");
      summary.textContent = title.textContent;
      details.append(summary);
      title.remove();
      while (panel.firstChild) details.append(panel.firstChild);
      panel.append(details);
    });
    const panels = [...document.querySelectorAll(".worked-answer")];
    if (!panels.length || document.querySelector(".answer-controls")) return;
    const controls = document.createElement("div");
    controls.className = "answer-controls";
    controls.setAttribute("aria-label", "Worked answers");
    for (const [label, open] of [["Show all hints and solutions", true], ["Hide answers", false]]) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = label;
      button.addEventListener("click", () => panels.forEach(panel => {panel.open = open;}));
      controls.append(button);
    }
    panels[0].closest(".admonition").before(controls);
    // Printing must include full solutions, including when collapsed on screen.
    let openBeforePrint = [];
    window.addEventListener("beforeprint", () => {
      openBeforePrint = panels.map(panel => panel.open);
      panels.forEach(panel => {panel.open = true;});
    });
    window.addEventListener("afterprint", () => panels.forEach((panel, index) => {
      panel.open = openBeforePrint[index];
    }));
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", enhance);
  else enhance();
})();

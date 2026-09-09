// Answers remain readable without JavaScript and expand for printing.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".cell_output img").forEach(img => {
    if (img.closest("a")) return;
    const link = document.createElement("a");
    link.href = img.currentSrc || img.src;
    link.title = "Open figure at full resolution";
    link.setAttribute("aria-label", "Open figure at full resolution");
    img.replaceWith(link);
    link.append(img);
  });
  document.querySelectorAll(".admonition.dropdown").forEach(panel => {
    const title = panel.querySelector(":scope > .admonition-title");
    if (!title) return;
    const details = document.createElement("details");
    details.className = "worked-answer";
    const summary = document.createElement("summary");
    summary.textContent = title.textContent;
    title.remove();
    details.append(summary);
    while (panel.firstChild) details.append(panel.firstChild);
    panel.append(details);
  });
  let previous = [];
  const panels = [...document.querySelectorAll(".worked-answer")];
  window.addEventListener("beforeprint", () => {
    previous = panels.map(panel => panel.open);
    panels.forEach(panel => { panel.open = true; });
  });
  window.addEventListener("afterprint", () => panels.forEach((panel, i) => {
    panel.open = previous[i];
  }));
});

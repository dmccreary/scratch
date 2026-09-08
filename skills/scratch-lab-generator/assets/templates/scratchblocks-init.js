/* Render <pre class="blocks"> elements as Scratch 3 block diagrams.
 *
 * Installed by the scratch-lab-generator skill. Re-runs on every page load,
 * including MkDocs Material's instant navigation, which swaps page content
 * without a full reload.
 */
(function () {
  function render() {
    if (typeof scratchblocks === "undefined") return;
    document.querySelectorAll("pre.blocks:not([data-rendered])").forEach(function (el) {
      el.setAttribute("data-rendered", "true");
    });
    scratchblocks.renderMatching("pre.blocks", {
      style: "scratch3",
      languages: ["en"],
      scale: 0.8
    });
    scratchblocks.renderMatching("code.b", {
      style: "scratch3",
      inline: true,
      scale: 0.7
    });
  }

  // MkDocs Material instant navigation
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(render);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();

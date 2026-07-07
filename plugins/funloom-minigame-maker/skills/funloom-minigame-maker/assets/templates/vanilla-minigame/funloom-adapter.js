(function () {
  const allowedResults = new Set(window.FUNLOOM_ALLOWED_RESULTS || ["success", "failure"]);
  let completed = false;

  window.completeFunloomMinigame = function completeFunloomMinigame(result) {
    if (completed) return;
    if (!allowedResults.has(result)) return;
    completed = true;
    parent.postMessage({
      type: "funloom:minigame:complete",
      result
    }, "*");
  };
})();

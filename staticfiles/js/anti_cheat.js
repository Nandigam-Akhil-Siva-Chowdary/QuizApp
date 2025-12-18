(function () {
  const attemptId = window.ATTEMPT_ID;

  function warn(type) {
    if (!attemptId) return;

    fetch(window.WARN_VIOLATION_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.CSRF_TOKEN,
      },
      body: JSON.stringify({ type, attempt_id: attemptId }),
    }).catch(() => {});
  }

  /* ---------------------------
     COPY / RIGHT CLICK BLOCK
  ---------------------------- */

  document.addEventListener("copy", function (e) {
    e.preventDefault();
    alert("Copying is not allowed during the quiz.");
    warn("copy_attempt");
  });

  document.addEventListener("cut", function (e) {
    e.preventDefault();
    warn("cut_attempt");
  });

  document.addEventListener("contextmenu", function (e) {
    e.preventDefault();
    warn("right_click");
  });

  /* ---------------------------
     KEYBOARD SHORTCUT BLOCK
  ---------------------------- */

  document.addEventListener("keydown", function (e) {
    if (
      e.ctrlKey &&
      ["c", "x", "v", "u", "s", "p"].includes(e.key.toLowerCase())
    ) {
      e.preventDefault();
      warn("keyboard_shortcut");
    }

    // F12
    if (e.key === "F12") {
      e.preventDefault();
      warn("devtools_detected");
    }
  });

  /* ---------------------------
     TAB SWITCH / VISIBILITY
  ---------------------------- */

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
      warn("tab_switch");
      alert(
        "You switched tabs or minimized the window. This counts as a warning."
      );
    }
  });

  /* ---------------------------
     TEXT SELECTION BLOCK
  ---------------------------- */

  document.addEventListener("selectstart", function (e) {
    e.preventDefault();
  });
})();
(function () {
  const fullscreenBtn = document.getElementById("enter-fullscreen-btn");
  const attemptId = window.ATTEMPT_ID;

  function requestFullscreen() {
    const el = document.documentElement;

    if (el.requestFullscreen) {
      el.requestFullscreen();
    } else if (el.webkitRequestFullscreen) {
      el.webkitRequestFullscreen();
    } else if (el.msRequestFullscreen) {
      el.msRequestFullscreen();
    }
  }

  function isFullscreen() {
    return (
      document.fullscreenElement ||
      document.webkitFullscreenElement ||
      document.msFullscreenElement
    );
  }

  function reportFullscreenExit() {
    if (!attemptId) return;

    fetch(window.WARN_VIOLATION_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.CSRF_TOKEN,
      },
      body: JSON.stringify({
        type: "fullscreen_exit",
        attempt_id: attemptId,
      }),
    }).catch(() => {});
  }

  document.addEventListener("fullscreenchange", () => {
    if (!isFullscreen()) {
      reportFullscreenExit();
      alert(
        "You exited fullscreen mode. This counts as a warning. Returning to quiz..."
      );
    }
  });

  if (fullscreenBtn) {
    fullscreenBtn.addEventListener("click", () => {
      requestFullscreen();
    });
  } else {
    // Enforce fullscreen on page load if no button is present
    requestFullscreen();
  }
})();
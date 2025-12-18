(function () {
  const fullscreenBtn = document.getElementById("enter-fullscreen-btn");
  const attemptId = window.ATTEMPT_ID;
  const warningsAllowed = window.WARNINGS_ALLOWED || 2;
  let violationCount = 0;
  let isChecking = false;

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
    if (!attemptId || isChecking) return;
    isChecking = true;

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
    })
    .then(response => response.json())
    .then(data => {
      if (!data.success) {
        isChecking = false;
        return;
      }

      const fullscreenViolations = data.fullscreen_violations || 0;
      const warningsAllowed = data.warnings_allowed || 2;
      const isDisqualified = data.is_disqualified || false;

      if (isDisqualified) {
        // Disqualified - exit quiz
        alert(
          "You have exceeded the allowed warnings. " +
          "You have been exited from the quiz and your attempt has been used."
        );
        window.location.href = window.QUIZ_HOME_URL || '/';
        return;
      }

      if (fullscreenViolations <= warningsAllowed) {
        // Show warning
        const warningsRemaining = warningsAllowed - fullscreenViolations;
        alert(
          `Warning ${fullscreenViolations}/${warningsAllowed + 1}: You exited fullscreen mode. ` +
          `You have ${warningsRemaining} warning(s) remaining. ` +
          `Please return to fullscreen mode immediately.`
        );
        // Force back to fullscreen
        setTimeout(() => {
          requestFullscreen();
          isChecking = false;
        }, 100);
      } else {
        // Exceeded warnings - should be disqualified by server
        alert(
          "You have exceeded the allowed warnings. " +
          "You have been exited from the quiz and your attempt has been used."
        );
        window.location.href = window.QUIZ_HOME_URL || '/';
      }
    })
    .catch(() => {
      isChecking = false;
    });
  }

  // Monitor fullscreen changes
  document.addEventListener("fullscreenchange", () => {
    if (!isFullscreen()) {
      reportFullscreenExit();
    } else {
      isChecking = false;
    }
  });

  document.addEventListener("webkitfullscreenchange", () => {
    if (!isFullscreen()) {
      reportFullscreenExit();
    } else {
      isChecking = false;
    }
  });

  document.addEventListener("msfullscreenchange", () => {
    if (!isFullscreen()) {
      reportFullscreenExit();
    } else {
      isChecking = false;
    }
  });

  // Enforce fullscreen on page load
  if (fullscreenBtn) {
    fullscreenBtn.addEventListener("click", () => {
      requestFullscreen();
    });
  } else {
    // Auto-request fullscreen on page load
    setTimeout(() => {
      if (!isFullscreen()) {
        requestFullscreen();
      }
    }, 500);
  }

  // Check fullscreen periodically
  setInterval(() => {
    if (!isFullscreen() && !isChecking) {
      reportFullscreenExit();
    }
  }, 1000);
})();
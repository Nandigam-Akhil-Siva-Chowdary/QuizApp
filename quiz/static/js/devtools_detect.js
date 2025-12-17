(function () {
    let devtoolsDetected = false;
    const attemptId = window.ATTEMPT_ID;
  
    function warnDevtools() {
      if (!attemptId) return;

      fetch(window.WARN_VIOLATION_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": window.CSRF_TOKEN,
        },
        body: JSON.stringify({
          type: "devtools_detected",
          attempt_id: attemptId,
        }),
      });
  
      alert(
        "Developer tools usage detected. This is a violation and has been recorded."
      );
    }
  
    /* ---------------------------------
       METHOD 1: WINDOW SIZE DIFFERENCE
       (Detect docked DevTools)
    ---------------------------------- */
  
    setInterval(() => {
      const widthDiff = window.outerWidth - window.innerWidth;
      const heightDiff = window.outerHeight - window.innerHeight;
  
      if (widthDiff > 160 || heightDiff > 160) {
        if (!devtoolsDetected) {
          devtoolsDetected = true;
          warnDevtools();
        }
      }
    }, 1000);
  
    /* ---------------------------------
       METHOD 2: DEBUGGER PAUSE CHECK
       (Detect debugger opening)
    ---------------------------------- */
  
    setInterval(() => {
      const start = performance.now();
      debugger;
      const end = performance.now();
  
      if (end - start > 120) {
        if (!devtoolsDetected) {
          devtoolsDetected = true;
          warnDevtools();
        }
      }
    }, 2000);
  })();
  
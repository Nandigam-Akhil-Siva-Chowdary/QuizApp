(function () {
  const submitBtn = document.getElementById("submit-quiz-btn");
  const attemptId = window.ATTEMPT_ID;

  if (!submitBtn) return;

  let submitted = false;

  function submitQuiz() {
    if (submitted) return;
    submitted = true;

    submitBtn.disabled = true;
    submitBtn.innerText = "Submitting...";

    fetch(window.SUBMIT_QUIZ_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": window.CSRF_TOKEN,
      },
      body: new URLSearchParams({
        attempt_id: attemptId || "",
      }),
    })
      .then((response) => {
        if (response.ok || response.redirected) {
          // Submission successful - redirect to result or home
          if (response.redirected) {
            window.location.href = response.url;
          } else {
            window.location.href = window.SUBMIT_REDIRECT_URL || window.QUIZ_HOME_URL;
          }
        } else {
          throw new Error("Submission failed");
        }
      })
      .catch(() => {
        alert("Submission failed. Please try again.");
        submitted = false;
        submitBtn.disabled = false;
        submitBtn.innerText = "Submit";
      });
  }

  submitBtn.addEventListener("click", function () {
    const confirmSubmit = confirm(
      "Are you sure you want to submit the quiz? You cannot attempt again."
    );

    if (confirmSubmit) {
      submitQuiz();
    }
  });

  // Prevent accidental page unload
  window.addEventListener("beforeunload", function (e) {
    if (!submitted) {
      e.preventDefault();
      e.returnValue = "";
    }
  });
})();
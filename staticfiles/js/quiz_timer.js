(function () {
    let remainingSeconds = window.QUIZ_REMAINING_SECONDS;
    const timerElement = document.getElementById("quiz-timer");
    const attemptId = window.ATTEMPT_ID;
  
    function formatTime(seconds) {
      const m = Math.floor(seconds / 60);
      const s = seconds % 60;
      return `${m.toString().padStart(2, "0")}:${s
        .toString()
        .padStart(2, "0")}`;
    }
  
    function tick() {
      if (remainingSeconds <= 0) {
        autoSubmitQuiz();
        return;
      }
  
      timerElement.innerText = formatTime(remainingSeconds);
      remainingSeconds--;
    }
  
    function autoSubmitQuiz() {
      fetch(window.AUTO_SUBMIT_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": window.CSRF_TOKEN,
        },
        body: new URLSearchParams({
          attempt_id: attemptId || "",
        }),
      }).finally(() => {
        window.location.href = window.SUBMIT_REDIRECT_URL;
      });
    }
  
    setInterval(tick, 1000);
  })();
  
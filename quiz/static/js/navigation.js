(function () {
  let currentQuestionIndex = 0;
  const attemptId = window.ATTEMPT_ID;

  const questions = document.querySelectorAll(".quiz-question");
  const navButtons = document.querySelectorAll(".question-nav-btn");
  const answerInputs = document.querySelectorAll(".answer-input");

  function updateNavStatus(index, status) {
    const btn = navButtons[index];
    if (!btn) return;

    btn.classList.remove(
      "bg-gray-400",
      "bg-yellow-400",
      "bg-green-500",
      "bg-purple-500",
      "bg-orange-400"
    );

    // Status color mapping
    switch (status) {
      case "visited":
        btn.classList.add("bg-yellow-400");
        break;
      case "answered":
        btn.classList.add("bg-green-500");
        break;
      case "review":
        btn.classList.add("bg-purple-500");
        break;
      case "not_answered":
        btn.classList.add("bg-orange-400");
        break;
      default:
        btn.classList.add("bg-gray-400");
    }
  }

  function showQuestion(index) {
    questions.forEach((q, i) => {
      q.classList.toggle("hidden", i !== index);
    });

    updateNavStatus(index, "visited");
    currentQuestionIndex = index;
  }

  function hasAnswer(index) {
    const inputs = questions[index].querySelectorAll(
      "input[type=radio], input[type=checkbox]"
    );
    return Array.from(inputs).some((i) => i.checked);
  }

  function saveAnswer(questionId) {
    const questionEl = Array.from(questions).find(
      (q) => q.dataset.questionId === questionId
    );
    if (!questionEl || !attemptId) return;

    const inputs = questionEl.querySelectorAll(
      "input[type=radio], input[type=checkbox]"
    );
    const selected = Array.from(inputs)
      .filter((i) => i.checked)
      .map((i) => i.value);

    fetch(window.SAVE_ANSWER_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.CSRF_TOKEN,
      },
      body: JSON.stringify({
        attempt_id: attemptId,
        question_id: questionId,
        selected_option_ids: selected,
        marked_for_review: false,
      }),
    }).catch(() => {});
  }

  /* -----------------------------
     NAV BUTTON CLICK
  ------------------------------ */
  navButtons.forEach((btn, index) => {
    btn.addEventListener("click", () => {
      if (hasAnswer(currentQuestionIndex)) {
        updateNavStatus(currentQuestionIndex, "answered");
      } else {
        updateNavStatus(currentQuestionIndex, "not_answered");
      }
      showQuestion(index);
    });
  });

  /* -----------------------------
     PREV / NEXT BUTTONS
  ------------------------------ */
  document.getElementById("prev-btn")?.addEventListener("click", () => {
    if (currentQuestionIndex > 0) {
      showQuestion(currentQuestionIndex - 1);
    }
  });

  document.getElementById("next-btn")?.addEventListener("click", () => {
    if (currentQuestionIndex < questions.length - 1) {
      showQuestion(currentQuestionIndex + 1);
    }
  });

  /* -----------------------------
     MARK FOR REVIEW
  ------------------------------ */
  document.getElementById("mark-review-btn")?.addEventListener("click", () => {
    const questionEl = questions[currentQuestionIndex];
    const questionId = questionEl?.dataset?.questionId;
    if (!questionId || !attemptId) return;

    updateNavStatus(currentQuestionIndex, "review");
    fetch(window.MARK_REVIEW_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.CSRF_TOKEN,
      },
      body: JSON.stringify({
        attempt_id: attemptId,
        question_id: questionId,
        is_marked_for_review: true,
      }),
    }).catch(() => {});
  });

  /* -----------------------------
     ANSWER CHANGE HANDLER
  ------------------------------ */
  answerInputs.forEach((input) => {
    input.addEventListener("change", () => {
      const questionId = input.dataset.questionId;
      saveAnswer(questionId);
      updateNavStatus(currentQuestionIndex, "answered");
    });
  });

  /* -----------------------------
     INITIAL LOAD
  ------------------------------ */
  if (questions.length > 0) {
    showQuestion(0);
  }
})();
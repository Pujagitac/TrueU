
document.addEventListener("DOMContentLoaded", () => {

    // ---------------- Motivation ----------------
    const motivations = [
        "Believe in yourself.","You are stronger than you think.","Every day is a new beginning.",
        "Small steps count.","Keep moving forward.","You are capable of amazing things.","Your effort matters.",
        "Stay positive.","Believe in your dreams.","Make today count.","Embrace challenges.","Stay curious.",
        "Take time to breathe.","Focus on what matters.","You can achieve greatness.","Be kind to yourself.",
        "Celebrate small wins.","Never stop learning.","Progress, not perfection.","You are enough.","Trust the process.",
        "Keep shining.","Your actions matter.","Stay motivated.","One step at a time.","Positivity attracts positivity.",
        "Your mind is powerful.","Face today with courage.","Your potential is limitless.","Gratitude brings happiness.",
        "Believe in your journey.","Stay patient.","You are unique.","Take time for self-care.","Good things are coming.",
        "Keep your head up.","Stay focused.","Your dreams are valid.","You are resilient.","Find joy in the small things.",
        "Stay true to yourself.","You can do it.","Confidence is key.","Embrace positivity.","Your hard work pays off.",
        "Keep your spirit high.","Motivation fuels success.","You are worthy."
    ];

    const motivationOutput = document.querySelector("#motivation-output");
    if (motivationOutput) {
        const day = new Date().getDate();
        const index = day % motivations.length;
        motivationOutput.textContent = motivations[index];
    }

// ---------------- Predictions ----------------
    let predictionResults = [];

    fetch('http://127.0.0.1:5000/predictions')
        .then(res => res.json())
        .then(json => {
            predictionResults = json;
            console.log("Loaded predictions:", predictionResults);
        })
        .catch(err => console.error("Error loading predictions:", err));

    // ---------------- Random Prediction Click ----------------
    const predictSphere = document.querySelector("#predict-sphere");
    const predictionOutputBox = document.querySelector("#prediction-output");

    if (predictSphere && predictionOutputBox) {
        predictSphere.addEventListener("click", () => {
            if (predictionResults.length === 0) {
                predictionOutputBox.textContent = "No predictions loaded yet.";
                return;
            }

            const rand = Math.floor(Math.random() * predictionResults.length);
            const chosen = predictionResults[rand];

            predictionOutputBox.textContent = `${chosen.predictions} — Spirit: ${chosen.spirit}`;
        });
    }
});

//-------------find clue game

document.addEventListener("DOMContentLoaded", () => {
    let wordsClues = [];
    let currentWord = null;

    const clueDisplay = document.querySelector("#clue-display");
    const wordDisplay = document.querySelector("#word-display");
    const newClueBtn = document.querySelector("#new-clue-btn");
    const revealBtn = document.querySelector("#reveal-word-btn");

    // Load words from Flask
    fetch("/moodspace")
        .then(res => res.json())
        .then(json => wordsClues = json)
        .catch(err => console.error("Error loading Mood Space words:", err));

    newClueBtn.addEventListener("click", () => {
        if (wordsClues.length === 0) return;

        const randIndex = Math.floor(Math.random() * wordsClues.length);
        currentWord = wordsClues[randIndex];

        clueDisplay.textContent = "Clue: " + currentWord.clue;
        wordDisplay.style.display = "none";
        revealBtn.style.display = "inline-block";
    });

    revealBtn.addEventListener("click", () => {
        if (!currentWord) return;
        wordDisplay.textContent = "Word: " + currentWord.word;
        wordDisplay.style.display = "block";
    });
});





// MOOD SELECTION FOR DIARY ENTRY
document.addEventListener('DOMContentLoaded', () => {

  const moodButtons = document.querySelectorAll('.mood-buttons button');
  const moodInput = document.getElementById('moodName');

  if (moodButtons && moodInput) {
    moodButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        moodInput.value = btn.dataset.mood;

        // Reset borders
        moodButtons.forEach(b => b.style.border = 'none');

        // Highlight selected
        btn.style.border = '2px solid #1d4064';
      });
    });
  }

  // Mood selection
  const moodInputs = document.querySelectorAll('.mood-input');

  moodInputs.forEach(input => {
    input.addEventListener('change', () => {

      const form = input.closest('form');
      if (form) {
        form.submit();
      }

    });
  });

}); 

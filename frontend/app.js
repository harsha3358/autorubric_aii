let radar, ring;

// Theme toggle
function toggleTheme() {
  if (document.body.classList.contains("dark")) {
    document.body.classList.remove("dark");
    document.body.classList.add("light");
    localStorage.setItem("theme", "light");
  } else {
    document.body.classList.remove("light");
    document.body.classList.add("dark");
    localStorage.setItem("theme", "dark");
  }
}

// Load saved theme
window.onload = () => {
  const theme = localStorage.getItem("theme");
  if (theme === "dark") {
    document.body.classList.remove("light");
    document.body.classList.add("dark");
  }
};

// Reveal animation
function revealSections() {
  document.querySelectorAll(".reveal").forEach((el, i) => {
    setTimeout(() => el.classList.add("show"), i * 200);
  });
}

// Typing effect
function typeText(el, text) {
  el.innerHTML = "";
  let i = 0;
  function type() {
    if (i < text.length) {
      el.innerHTML += text.charAt(i);
      i++;
      setTimeout(type, 10);
    }
  }
  type();
}

// Score ring
function drawRing(score) {
  if (ring) ring.destroy();

  ring = new Chart(document.getElementById("scoreRing"), {
    type: "doughnut",
    data: {
      datasets: [{
        data: [score, 100 - score]
      }]
    },
    options: {
      cutout: "80%",
      plugins: { legend: { display: false } }
    }
  });

  document.getElementById("scoreText").innerText = score + "%";
}

// Reasoning logic
function generateReasoning(score) {
  if (score > 80)
    return ["Strong clarity", "Well structured", "Good coverage"];
  if (score > 50)
    return ["Basic idea present", "Needs depth", "Limited explanation"];
  return ["Weak answer", "Missing key concepts", "Needs improvement"];
}

// Main function
async function runEvaluation() {
  const prompt = document.getElementById("prompt").value;
  const answer = document.getElementById("answer").value;

  const loading = document.getElementById("loading");
  const result = document.getElementById("result");

  loading.classList.remove("hidden");
  result.classList.add("hidden");

  try {
    const res = await fetch("http://127.0.0.1:8000/evaluate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ prompt, answer })
    });

    const data = await res.json();

    loading.classList.add("hidden");
    result.classList.remove("hidden");

    revealSections();

    drawRing(data.score);

    typeText(document.getElementById("feedback"), data.feedback);

    document.getElementById("rubric").innerText = data.rubric;

    // Radar chart
    if (radar) radar.destroy();

    radar = new Chart(document.getElementById("radarChart"), {
      type: "radar",
      data: {
        labels: ["Clarity", "Depth", "Relevance"],
        datasets: [{
          label: "Metrics",
          data: [data.score * 0.9, data.score * 0.8, data.score]
        }]
      }
    });

    // Reasoning
    const list = document.getElementById("reasoning");
    list.innerHTML = "";

    generateReasoning(data.score).forEach(r => {
      const li = document.createElement("li");
      li.textContent = "• " + r;
      list.appendChild(li);
    });

  } catch (err) {
    console.error(err);
    loading.innerHTML = "❌ Connection issue";
  }
}
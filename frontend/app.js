let radar, ring;

const API_URL = "https://autorubric-aii.onrender.com/evaluate";

// Theme toggle
function toggleTheme() {
  const isDark = document.documentElement.classList.contains("dark");
  if (isDark) {
    document.documentElement.classList.remove("dark");
    localStorage.setItem("theme", "light");
  } else {
    document.documentElement.classList.add("dark");
    localStorage.setItem("theme", "dark");
  }
}

// Load theme
window.onload = () => {
  const theme = localStorage.getItem("theme");
  if (theme === "dark" || (!theme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
    document.documentElement.classList.add("dark");
  }
};

// Reveal animation
function revealSections() {
  document.querySelectorAll(".reveal").forEach((el, i) => {
    setTimeout(() => el.classList.add("show"), i * 150);
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
      setTimeout(type, 8);
    }
  }
  type();
}

// Score ring
function drawRing(score) {
  if (ring) ring.destroy();

  // Determine color based on score
  let color = '#22c55e'; // green (brand)
  if (score < 50) color = '#ef4444'; // red
  else if (score < 80) color = '#f59e0b'; // amber

  ring = new Chart(document.getElementById("scoreRing"), {
    type: "doughnut",
    data: {
      datasets: [{
        data: [score, 100 - score],
        backgroundColor: [color, 'rgba(150, 150, 150, 0.1)'],
        borderWidth: 0,
        hoverBackgroundColor: [color, 'rgba(150, 150, 150, 0.1)']
      }]
    },
    options: {
      cutout: "75%",
      responsive: true,
      maintainAspectRatio: true,
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      animation: { animateScale: true, animateRotate: true }
    }
  });

  const scoreTextEl = document.getElementById("scoreText");
  scoreTextEl.innerText = score + "%";
  scoreTextEl.style.color = color;
}

// Reasoning
function generateReasoning(score) {
  if (score >= 80)
    return ["Strong clarity and articulation", "Well-structured response", "Covers all key aspects comprehensively"];
  if (score >= 50)
    return ["Basic understanding is present", "Needs more depth in explanation", "Structure could be improved"];
  return ["Insufficient explanation", "Missing fundamental concepts", "Lacks clarity and cohesion"];
}

// Main function
async function runEvaluation() {
  const prompt = document.getElementById("prompt").value;
  const answer = document.getElementById("answer").value;

  if (!prompt.trim() || !answer.trim()) {
    alert("Please enter both an assignment prompt and a student answer.");
    return;
  }

  const emptyState = document.getElementById("emptyState");
  const loadingState = document.getElementById("loadingState");
  const resultsState = document.getElementById("resultsState");
  const evaluateBtn = document.getElementById("evaluateBtn");

  // Show loading state
  if(emptyState) emptyState.classList.add("hidden");
  resultsState.classList.add("hidden");
  resultsState.classList.remove("flex");
  loadingState.classList.remove("hidden");
  loadingState.classList.add("flex");
  
  // Disable button
  evaluateBtn.disabled = true;
  evaluateBtn.classList.add("opacity-75", "cursor-not-allowed");
  evaluateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

  // Reset animations
  document.querySelectorAll(".reveal").forEach(el => el.classList.remove("show"));

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ prompt, answer })
    });

    const data = await res.json();

    // Hide loading, show results
    loadingState.classList.add("hidden");
    loadingState.classList.remove("flex");
    resultsState.classList.remove("hidden");
    resultsState.classList.add("flex");

    drawRing(data.score || 0);

    typeText(document.getElementById("feedback"), data.feedback || "No feedback provided.");

    // Parse Markdown Rubric
    const rubricHtml = marked.parse(data.rubric || "No rubric available.");
    document.getElementById("rubric").innerHTML = rubricHtml;

    // Radar chart
    if (radar) radar.destroy();

    const isDark = document.documentElement.classList.contains("dark");
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
    const textColor = isDark ? '#94a3b8' : '#64748b';

    radar = new Chart(document.getElementById("radarChart"), {
      type: "radar",
      data: {
        labels: ["Clarity", "Depth", "Relevance"],
        datasets: [{
          label: "Score Breakdown",
          data: [Math.min(100, (data.score || 0) * 1.1), Math.max(0, (data.score || 0) * 0.8), (data.score || 0)],
          backgroundColor: "rgba(34, 197, 94, 0.2)",
          borderColor: "#22c55e",
          pointBackgroundColor: "#22c55e",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "#22c55e",
          borderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          r: {
            angleLines: { color: gridColor },
            grid: { color: gridColor },
            pointLabels: { color: textColor, font: { family: 'Inter', size: 12 } },
            ticks: { display: false, max: 100, min: 0 }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });

    // Reasoning
    const list = document.getElementById("reasoning");
    list.innerHTML = "";

    generateReasoning(data.score || 0).forEach(r => {
      const li = document.createElement("li");
      li.className = "flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300";
      
      const icon = document.createElement("i");
      icon.className = "fas fa-check-circle text-brand-500 mt-1";
      if (data.score < 50) icon.className = "fas fa-exclamation-circle text-red-500 mt-1";
      else if (data.score < 80) icon.className = "fas fa-info-circle text-amber-500 mt-1";
      
      const span = document.createElement("span");
      span.textContent = r;
      
      li.appendChild(icon);
      li.appendChild(span);
      list.appendChild(li);
    });

    // Trigger reveal animations
    setTimeout(revealSections, 100);

  } catch (err) {
    loadingState.classList.add("hidden");
    loadingState.classList.remove("flex");
    resultsState.classList.remove("hidden");
    resultsState.classList.add("flex");

    drawRing(0);
    document.getElementById("feedback").innerText = "Unable to connect to the backend service. Please check your network or try again later.";
    document.getElementById("rubric").innerHTML = "<p class='text-red-500 font-medium'>No data available due to connection failure.</p>";
    document.getElementById("reasoning").innerHTML = "<li class='text-red-500 flex items-center gap-2'><i class='fas fa-times-circle'></i> Connection failure</li>";
    
    setTimeout(revealSections, 100);
  } finally {
    // Re-enable button
    evaluateBtn.disabled = false;
    evaluateBtn.classList.remove("opacity-75", "cursor-not-allowed");
    evaluateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Evaluation';
  }
}
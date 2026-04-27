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

    // Extract actual metrics from backend "reasoning" array
    // Format is "MetricName Score: 80%"
    const metrics = {};
    if (data.reasoning && Array.isArray(data.reasoning)) {
      data.reasoning.forEach(r => {
        const parts = r.split(" Score: ");
        if (parts.length === 2) {
          const name = parts[0];
          const val = parseFloat(parts[1].replace("%", ""));
          metrics[name] = val;
        }
      });
    } else {
      metrics["Relevance"] = data.score || 0;
      metrics["Clarity"] = data.score || 0;
      metrics["Depth"] = data.score || 0;
      metrics["Structure"] = data.score || 0;
    }

    // Radar chart
    if (radar) radar.destroy();

    const isDark = document.documentElement.classList.contains("dark");
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
    const textColor = isDark ? '#94a3b8' : '#64748b';

    radar = new Chart(document.getElementById("radarChart"), {
      type: "radar",
      data: {
        labels: ["Relevance", "Clarity", "Depth", "Structure"],
        datasets: [{
          label: "Score Breakdown",
          data: [metrics["Relevance"], metrics["Clarity"], metrics["Depth"], metrics["Structure"]],
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

    // Detailed Breakdown Progress Bars
    const breakdownContainer = document.getElementById("detailedBreakdown");
    if(breakdownContainer) {
      breakdownContainer.innerHTML = "";
      
      const criteriaKeys = ["Relevance", "Clarity", "Depth", "Structure"];
      criteriaKeys.forEach(key => {
        const val = metrics[key];
        let barColor = "bg-brand-500";
        if (val < 50) barColor = "bg-red-500";
        else if (val < 80) barColor = "bg-amber-500";

        const barHtml = `
          <div>
            <div class="flex justify-between items-center mb-1">
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">${key}</span>
              <span class="text-sm font-semibold text-gray-900 dark:text-white">${val}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
              <div class="${barColor} h-2 rounded-full transition-all duration-1000 ease-out" style="width: 0%" data-width="${val}%"></div>
            </div>
          </div>
        `;
        breakdownContainer.innerHTML += barHtml;
      });

      // Animate progress bars
      setTimeout(() => {
        breakdownContainer.querySelectorAll('[data-width]').forEach(el => {
          el.style.width = el.getAttribute('data-width');
        });
      }, 300);
    }

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
    if(document.getElementById("detailedBreakdown")) {
        document.getElementById("detailedBreakdown").innerHTML = "<p class='text-red-500 text-sm flex items-center gap-2'><i class='fas fa-times-circle'></i> Connection failure</p>";
    }
    
    setTimeout(revealSections, 100);
  } finally {
    // Re-enable button
    evaluateBtn.disabled = false;
    evaluateBtn.classList.remove("opacity-75", "cursor-not-allowed");
    evaluateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Evaluation';
  }
}
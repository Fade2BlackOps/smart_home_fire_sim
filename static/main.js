// static/main.js (Polling Version)

let chart = null;

function createChart(labels, datasets) {
  const ctx = document.getElementById("tempsChart").getContext("2d");
  if (chart) {
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  } else {
    chart = new Chart(ctx, {
      type: "line",
      data: { labels: labels, datasets: datasets },
      options: {
        responsive: true,
        animation: false, // Disable animation for smoother live updates
        plugins: {
          legend: { position: "bottom", labels: { color: "#cfeff1" } },
        },
        scales: {
          x: { ticks: { color: "#9aa4b2" } },
          y: { ticks: { color: "#9aa4b2" } }
        }
      }
    });
  }
}

function buildDatasets(latestBlocks) {
  if (!latestBlocks || latestBlocks.length === 0) return {labels:[], datasets:[]};
  
  // Safety check: ensure first block has temps
  const firstValid = latestBlocks.find(b => b.data && b.data.temps);
  if (!firstValid) return {labels:[], datasets:[]};

  const sensorCount = firstValid.data.temps.length;
  const labels = latestBlocks.map(b => `t=${b.data.time}`);
  
  const datasets = [];
  for (let i = 0; i < sensorCount; i++) {
    const data = latestBlocks.map(b => (b.data && b.data.temps ? b.data.temps[i] : null));
    datasets.push({
      label: `Sensor ${i}`,
      data,
      fill: false,
      borderColor: `hsl(${i * 40}, 70%, 50%)`, // Auto-color sensors
      tension: 0.2,
      pointRadius: 2
    });
  }
  return { labels, datasets };
}

async function fetchData() {
  try {
    const response = await fetch('/api/updates');
    const payload = await response.json();
    
    const blocks = payload.blocks || [];
    const latest = payload.latest || {};

    document.getElementById("status-text").innerText = "Connected (Polling)";

    // Update latest info
    document.getElementById("latest-time").innerText = latest.time ?? "--";
    document.getElementById("latest-decision").innerText = latest.decision ?? "--";
    document.getElementById("latest-votes").innerText = latest.votes ? latest.votes.join(", ") : "--";

    // Update table
    const tbody = document.querySelector("#ledger-table tbody");
    tbody.innerHTML = "";
    blocks.slice().reverse().forEach(b => {
      const tr = document.createElement("tr");
      const d = b.data || {};
      tr.innerHTML = `<td>${b.index}</td><td>${d.time}</td><td>${d.decision}</td><td>${d.votes}</td>`;
      tbody.appendChild(tr);
    });

    // Update Chart
    const built = buildDatasets(blocks);
    if (built.datasets.length > 0) {
        createChart(built.labels, built.datasets);
    }

  } catch (err) {
    console.error(err);
    document.getElementById("status-text").innerText = "Disconnected";
  }
}

// Poll every 1000ms (1 second)
setInterval(fetchData, 1000);
fetchData(); // Initial call
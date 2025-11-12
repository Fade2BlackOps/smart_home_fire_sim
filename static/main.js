// static/main.js
const socket = io("/dashboard");

let chart = null;
const sensorCount = 9; // fallback; your simulation may change this. Chart adapts dynamically.

function createChart(labels, datasets) {
  const ctx = document.getElementById("tempsChart").getContext("2d");
  if (chart) {
    chart.destroy();
  }
  chart = new Chart(ctx, {
    type: "line",
    data: { labels: labels, datasets: datasets },
    options: {
      responsive: true,
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

function buildDatasets(latestBlocks) {
  if (!latestBlocks || latestBlocks.length === 0) return {labels:[], datasets:[]};
  // assume temps arrays are same length = sensor count
  const sensors = latestBlocks[0].temps.length;
  const labels = latestBlocks.map(b => `t=${b.time}`);
  const datasets = [];
  for (let i = 0; i < sensors; i++) {
    const data = latestBlocks.map(b => (b.temps ? b.temps[i] : null));
    datasets.push({
      label: `Sensor ${i}`,
      data,
      fill: false,
      tension: 0.2,
      pointRadius: 2
    });
  }
  return { labels, datasets };
}

socket.on("connect", () => {
  document.getElementById("status-text").innerText = "Connected";
});

socket.on("ledger_update", (payload) => {
  const blocks = payload.blocks || [];
  const latest = payload.latest || null;

  // Update latest info panel
  if (latest) {
    document.getElementById("latest-time").innerText = latest.time ?? "--";
    document.getElementById("latest-decision").innerText = latest.decision ?? "--";
    document.getElementById("latest-votes").innerText = latest.votes ? latest.votes.join(", ") : "--";
  }

  // Update ledger table
  const tbody = document.querySelector("#ledger-table tbody");
  tbody.innerHTML = "";
  blocks.slice().reverse().forEach(b => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${b.index ?? "--"}</td><td>${b.time ?? "--"}</td><td>${b.decision ?? "--"}</td><td>${b.votes ? b.votes.map(v=>v?"1":"0").join("") : "--"}</td>`;
    tbody.appendChild(tr);
  });

  // Update chart
  const built = buildDatasets(blocks);
  createChart(built.labels, built.datasets);
});

socket.on("ledger_error", (err) => {
  document.getElementById("status-text").innerText = "Error: " + (err.error || "unknown");
});

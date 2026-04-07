// frontend/static/js/app.js
'use strict';

// ── State ──────────────────────────────────────────────────────────────────
let currentResult = null;

// ── DOM helpers ────────────────────────────────────────────────────────────
const $  = id => document.getElementById(id);
const el = (tag, attrs = {}, ...children) => {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === 'html') e.innerHTML = v;
    else if (k === 'cls') e.className = v;
    else e.setAttribute(k, v);
  });
  children.forEach(c => c && e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c));
  return e;
};

// ── Upload zone ────────────────────────────────────────────────────────────
const uploadZone = $('upload-zone');
const fileInput  = $('file-input');

uploadZone.addEventListener('dragover',  e => { e.preventDefault(); uploadZone.classList.add('drag-over'); });
uploadZone.addEventListener('dragleave', ()  => uploadZone.classList.remove('drag-over'));
uploadZone.addEventListener('drop', e => {
  e.preventDefault(); uploadZone.classList.remove('drag-over');
  const f = e.dataTransfer.files[0];
  if (f) setFile(f);
});
uploadZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', e => { if (e.target.files[0]) setFile(e.target.files[0]); });

function setFile(file) {
  const label = $('file-label');
  label.textContent = `📎 ${file.name}`;
  label.style.display = 'block';
  uploadZone.dataset.file = 'yes';
}

// ── Form submission ────────────────────────────────────────────────────────
$('analyze-btn').addEventListener('click', submitForm);

async function submitForm() {
  const btn    = $('analyze-btn');
  const errEl  = $('error-msg');
  const text   = $('report-text').value.trim();
  const hasFile = fileInput.files.length > 0;

  errEl.style.display = 'none';

  if (!text && !hasFile) {
    errEl.style.display = 'flex';
    errEl.textContent   = '⚠ Please paste report text or upload a file before analyzing.';
    return;
  }

  btn.disabled   = true;
  btn.innerHTML  = '<div class="spinner"></div><span>Analyzing report…</span>';
  $('results').style.display = 'none';

  const form = new FormData();
  form.append('age',    $('patient-age').value    || 35);
  form.append('gender', $('patient-gender').value || 'male');
  if (text)    form.append('text', text);
  if (hasFile) form.append('file', fileInput.files[0]);

  try {
    const res  = await fetch('/api/analyze', { method: 'POST', body: form });
    const data = await res.json();

    if (!res.ok || data.error) throw new Error(data.error || 'Analysis failed');

    currentResult = data.result;
    renderResults(currentResult);
  } catch (err) {
    errEl.textContent   = `⚠ ${err.message}`;
    errEl.style.display = 'flex';
  } finally {
    btn.disabled  = false;
    btn.innerHTML = '<span>Analyze Again</span>';
  }
}

// ── Render Results ─────────────────────────────────────────────────────────
function renderResults(r) {
  const wrap = $('results');
  wrap.innerHTML = '';

  wrap.appendChild(buildScoreCard(r));
  wrap.appendChild(buildParamsCard(r.parameters || []));
  wrap.appendChild(buildChartsSection(r.parameters || []));
  wrap.appendChild(buildInsightsCard(r));
  wrap.appendChild(buildRecsCard(r.recommendations || []));
  wrap.appendChild(buildDisclaimer());

  wrap.style.display = 'block';
  wrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Score Card ─────────────────────────────────────────────────────────────
function buildScoreCard(r) {
  const score  = r.health_score  || 0;
  const status = r.health_status || 'Unknown';

  const colorMap = { 'Good': '#2d6a4f', 'Moderate': '#b7700d', 'Needs Attention': '#c1392b' };
  const badgeCls = { 'Good': 'status-good', 'Moderate': 'status-moderate', 'Needs Attention': 'status-attention' };
  const color    = colorMap[status] || '#888';
  const circ     = 2 * Math.PI * 42;
  const offset   = circ - (score / 100) * circ;

  const card = el('div', { cls: 'card score-card' });
  card.innerHTML = `
    <div class="card-label">Overall Health Assessment</div>
    <div class="score-section">
      <div class="ring-wrap">
        <svg width="110" height="110" viewBox="0 0 110 110">
          <circle cx="55" cy="55" r="42" fill="none" stroke="#e8e4dc" stroke-width="9"/>
          <circle cx="55" cy="55" r="42" fill="none" stroke="${color}" stroke-width="9"
            stroke-dasharray="${circ.toFixed(1)}" stroke-dashoffset="${offset.toFixed(1)}"
            stroke-linecap="round" style="transition:stroke-dashoffset 1.1s ease;"/>
        </svg>
        <div class="ring-label">
          <span class="ring-num">${score}</span>
          <span class="ring-sub">/ 100</span>
        </div>
      </div>
      <div class="score-meta">
        <h3>Health Score</h3>
        <p>${r.patientSummary || ''}</p>
        <span class="status-badge ${badgeCls[status] || ''}">${status}</span>
        <div style="margin-top:6px;font-size:12px;color:var(--muted);">
          Report type: <strong>${r.report_type || 'General'}</strong>
        </div>
      </div>
    </div>`;
  return card;
}

// ── Parameters Card ────────────────────────────────────────────────────────
function buildParamsCard(params) {
  const card = el('div', { cls: 'card' });
  card.innerHTML = `<div class="card-label">Parameter Analysis</div>`;

  const wrap = el('div', { cls: 'params-wrap' });
  const tbl  = el('table', { cls: 'params-table' });
  tbl.innerHTML = `
    <thead><tr>
      <th>Parameter</th>
      <th>Your Value</th>
      <th>Normal Range</th>
      <th>Status</th>
      <th>What it means</th>
    </tr></thead>`;

  const tbody = el('tbody');
  params.forEach(p => {
    const s   = (p.status || 'Unknown').toLowerCase();
    const row = el('tr');
    row.innerHTML = `
      <td><span class="status-dot dot-${s}"></span>${p.name || ''}</td>
      <td style="font-weight:500;">${p.value_raw || '—'}</td>
      <td style="color:var(--muted);font-size:12px;">${p.normal_range || '—'}</td>
      <td><span class="tag tag-${s}">${p.status || 'Unknown'}</span></td>
      <td style="color:var(--muted);font-size:12px;max-width:220px;">${p.plain_explanation || ''}</td>`;
    tbody.appendChild(row);
  });

  tbl.appendChild(tbody);
  wrap.appendChild(tbl);
  card.appendChild(wrap);
  return card;
}

// ── Charts ─────────────────────────────────────────────────────────────────
function buildChartsSection(params) {
  const grid = el('div', { cls: 'chart-grid' });

  // Bar chart
  const barBox = el('div', { cls: 'chart-box' });
  barBox.innerHTML = '<div class="chart-title">Parameter Values</div>';
  const barCanvas = el('canvas', { id: 'barChart', style: 'max-height:260px;' });
  barBox.appendChild(barCanvas);
  grid.appendChild(barBox);

  // Pie chart
  const pieBox = el('div', { cls: 'chart-box' });
  pieBox.innerHTML = '<div class="chart-title">Status Distribution</div>';
  const pieCanvas = el('canvas', { id: 'pieChart', style: 'max-height:260px;' });
  pieBox.appendChild(pieCanvas);
  grid.appendChild(pieBox);

  // Render after DOM insertion
  requestAnimationFrame(() => {
    renderBarChart(params);
    renderPieChart(params);
  });

  return grid;
}

function renderBarChart(params) {
  const numeric = params.filter(p => p.value_numeric != null);
  if (!numeric.length) return;

  const colorMap = { Normal: '#2d6a4f', High: '#c1392b', Low: '#b7700d', Borderline: '#d4580a', Unknown: '#a09b94' };

  new Chart($('barChart'), {
    type: 'bar',
    data: {
      labels: numeric.map(p => p.name),
      datasets: [{
        label: 'Value',
        data:  numeric.map(p => p.value_numeric),
        backgroundColor: numeric.map(p => colorMap[p.status] || '#888'),
        borderRadius: 4,
        borderSkipped: false,
      }],
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: '#f0ede8' } },
        y: { grid: { display: false }, ticks: { font: { size: 11 } } },
      },
    },
  });
}

function renderPieChart(params) {
  const counts = {};
  params.forEach(p => { const s = p.status || 'Unknown'; counts[s] = (counts[s] || 0) + 1; });

  const colorMap = { Normal: '#2d6a4f', High: '#c1392b', Low: '#b7700d', Borderline: '#d4580a', Unknown: '#a09b94' };
  const labels   = Object.keys(counts);

  new Chart($('pieChart'), {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data:            labels.map(l => counts[l]),
        backgroundColor: labels.map(l => colorMap[l] || '#888'),
        borderWidth: 2,
        borderColor: '#fff',
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 12 }, padding: 14 } },
      },
      cutout: '55%',
    },
  });
}

// ── Insights Card ──────────────────────────────────────────────────────────
function buildInsightsCard(r) {
  const card = el('div', { cls: 'card' });
  card.innerHTML = '<div class="card-label">Key Insights</div>';

  (r.insights || []).forEach(i => {
    const d = el('div', { cls: `insight-block insight-${i.type || 'info'}` });
    d.textContent = i.text;
    card.appendChild(d);
  });

  if (r.consult_doctor) {
    const d = el('div', { cls: 'insight-block insight-danger' });
    d.innerHTML = '🩺 <strong>Medical consultation recommended.</strong> Some values in this report require professional evaluation. Please consult a qualified healthcare provider.';
    card.appendChild(d);
  }

  return card;
}

// ── Recommendations Card ───────────────────────────────────────────────────
function buildRecsCard(recs) {
  const card = el('div', { cls: 'card' });
  card.innerHTML = '<div class="card-label">Personalized Recommendations</div>';

  recs.forEach(r => {
    const row = el('div', { cls: 'rec-item' });
    row.innerHTML = `
      <div class="rec-icon">${r.icon || '💡'}</div>
      <div class="rec-text">${r.text}</div>`;
    card.appendChild(row);
  });

  return card;
}

// ── Disclaimer ─────────────────────────────────────────────────────────────
function buildDisclaimer() {
  const d = el('div', { cls: 'disclaimer' });
  d.innerHTML = '<span style="font-size:16px;flex-shrink:0;">ℹ</span><span><strong>Educational purpose only.</strong> This AI analysis is not a medical diagnosis. Always consult a qualified healthcare professional for advice, diagnosis, or treatment decisions.</span>';
  return d;
}

// ── Export JSON ────────────────────────────────────────────────────────────
$('export-btn') && $('export-btn').addEventListener('click', () => {
  if (!currentResult) return;
  const blob = new Blob([JSON.stringify(currentResult, null, 2)], { type: 'application/json' });
  const a = el('a', { href: URL.createObjectURL(blob), download: 'mediscan_report.json' });
  a.click();
  URL.revokeObjectURL(a.href);
});

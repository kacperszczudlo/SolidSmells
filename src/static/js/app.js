const $ = (id) => document.getElementById(id);

$("analyze").addEventListener("click", async () => {
  const code = $("code").value.trim();
  const mode = $("mode").value;
  if (!code) return showError("Wklej kod do analizy.");

  toggleLoading(true);
  hideError();

  try {
    const res = await fetch("/api/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, mode }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Błąd serwera");
    render(data);
  } catch (e) {
    showError(e.message);
  } finally {
    toggleLoading(false);
  }
});

function render(data) {
  $("verdict").textContent = data.verdict;
  $("score").innerHTML = scoreHTML(data.score);
  $("issues").innerHTML = (data.issues || []).map(issueHTML).join("");
  $("missing-tests").innerHTML = (data.missing_tests || [])
    .map((t) => `<li>${escape(t)}</li>`)
    .join("");
  $("refactor").textContent = data.refactor_suggestion || "Brak sugestii.";
  $("results").hidden = false;
}

const ICONS = { critical: "🔴", warning: "🟡", nit: "🟢" };

function issueHTML(i) {
  return `<li class="issue issue--${i.severity}">
    <header>${ICONS[i.severity]} <strong>${escape(i.category)}</strong>
      <small>${escape(i.location)}</small></header>
    <p><strong>Problem:</strong> ${escape(i.problem)}</p>
    <p><strong>Dlaczego boli:</strong> ${escape(i.why_it_hurts)}</p>
    <p><strong>Fix:</strong> ${escape(i.fix)}</p>
  </li>`;
}

function scoreHTML(s) {
  return ["solid", "testability", "readability"]
    .map((k) => `<span class="badge">${k.toUpperCase()}: ${s[k]}/5</span>`)
    .join(" ") + ` <span class="badge">COVERAGE: ${s.coverage_estimate}%</span>`;
}

function escape(s) {
  return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

function toggleLoading(b) {
  $("loading").hidden = !b;
  $("analyze").disabled = b;
}

function showError(msg) {
  $("error").textContent = msg;
  $("error").hidden = false;
}

function hideError() {
  $("error").hidden = true;
}

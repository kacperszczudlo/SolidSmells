const $ = (id) => document.getElementById(id);

const EXAMPLES = {
  "god-class": `class ReportGod:
    def __init__(self, data):
        self.data = data
    def load(self, path):
        self.data = open(path).read()
    def parse(self):
        return self.data.split(",")
    def validate(self):
        return len(self.data) > 0
    def export_pdf(self): pass
    def export_csv(self): pass
    def send_email(self): pass
`,
  "long-method": `def calculate_invoice(items, tax, discount, shipping, currency):
    total = 0
    for i in items:
        total += i * 1.23 * 0.97 + 42
    if discount > 0:
        total = total - discount * 1.15
    total += shipping * 3.14
    if currency == "EUR":
        total *= 4.32
    return total
`,
  "switch-type": `def area(shape, a, b=None):
    if shape == "circle":
        return 3.14 * a * a
    elif shape == "rect":
        return a * b
    elif shape == "triangle":
        return a * b / 2
    else:
        raise ValueError("unknown")
`,
};

$("analyze").addEventListener("click", analyze);

document.querySelectorAll("[data-example]").forEach((btn) => {
  btn.addEventListener("click", () => {
    const key = btn.getAttribute("data-example");
    $("code").value = EXAMPLES[key] || "";
    hideError();
    $("results").hidden = true;
  });
});

async function analyze() {
  const code = $("code").value.trim();
  const mode = $("mode").value;
  if (!code) {
    showError("Wklej kod do analizy.");
    return;
  }

  toggleLoading(true);
  hideError();
  $("results").hidden = true;

  try {
    const res = await fetch("/api/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, mode }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || `Błąd serwera (${res.status})`);
    }
    render(data);
  } catch (e) {
    showError(e.message);
  } finally {
    toggleLoading(false);
  }
}

function render(data) {
  $("verdict").textContent = data.verdict;
  $("score").innerHTML = scoreHTML(data.score);
  $("issues").innerHTML =
    (data.issues || []).map(issueHTML).join("") ||
    '<li class="issue issue--nit">Brak zgłoszonych problemów.</li>';
  $("missing-tests").innerHTML = (data.missing_tests || [])
    .map((t) => `<li>${escape(t)}</li>`)
    .join("") || "<li>—</li>";
  $("refactor").textContent = data.refactor_suggestion || "Brak sugestii.";
  $("results").hidden = false;
}

const ICONS = { critical: "🔴", warning: "🟡", nit: "🟢" };

function issueHTML(i) {
  return `<li class="issue issue--${i.severity}">
    <header>${ICONS[i.severity] || ""} <strong>${escape(i.category)}</strong>
      <small>${escape(i.location)}</small></header>
    <p><strong>Problem:</strong> ${escape(i.problem)}</p>
    <p><strong>Dlaczego boli:</strong> ${escape(i.why_it_hurts)}</p>
    <p><strong>Fix:</strong> ${escape(i.fix)}</p>
  </li>`;
}

function scoreHTML(s) {
  if (!s) return "";
  const keys = ["solid", "testability", "readability"];
  return (
    keys
      .map((k) => `<span class="badge">${k.toUpperCase()}: ${s[k]}/5</span>`)
      .join(" ") +
    ` <span class="badge">COVERAGE: ${s.coverage_estimate}%</span>`
  );
}

function escape(s) {
  return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

function toggleLoading(on) {
  $("loading").hidden = !on;
  $("analyze").disabled = on;
}

function showError(msg) {
  $("error").textContent = msg;
  $("error").hidden = false;
}

function hideError() {
  $("error").hidden = true;
}

const API = "https://me-api-playground-zrps.onrender.com";

let allProjects = [];
let activeSkill = null;

// ── Wake-up ping with retry ──────────────────────────────────────────────────
async function wakeServer() {
  const banner = document.getElementById("wake-banner");
  const msg = document.getElementById("wake-msg");
  const maxAttempts = 10;

  for (let i = 1; i <= maxAttempts; i++) {
    try {
      const res = await fetch(`${API}/health`, { signal: AbortSignal.timeout(4000) });
      if (res.ok) {
        msg.textContent = "Server is ready.";
        setTimeout(() => banner.classList.add("hidden"), 800);
        return true;
      }
    } catch (_) {}
    msg.textContent = `Waking up server... attempt ${i}/${maxAttempts}`;
    await sleep(2000);
  }
  msg.textContent = "Server may be slow — data will load when ready.";
  return false;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── Typed name effect ────────────────────────────────────────────────────────
function typeName(text) {
  const el = document.getElementById("hero-name");
  el.classList.remove("skeleton-line");
  el.style.width = ""; el.style.height = "";
  el.textContent = "";
  let i = 0;
  const interval = setInterval(() => {
    el.textContent += text[i++];
    if (i >= text.length) clearInterval(interval);
  }, 60);
}

// ── Profile ──────────────────────────────────────────────────────────────────
async function loadProfile() {
  try {
    const res = await fetch(`${API}/profile`);
    const data = await res.json();

    typeName(data.name);

    const edu = document.getElementById("hero-edu");
    edu.classList.remove("skeleton-line");
    edu.style.width = ""; edu.style.height = "";
    edu.textContent = data.education;

    const emailBtn = document.getElementById("hero-email");
    emailBtn.classList.remove("skeleton-btn");
    emailBtn.textContent = `✉ ${data.email}`;
    emailBtn.href = `mailto:${data.email}`;
  } catch (e) {
    document.getElementById("hero-name").textContent = "Portfolio";
  }
}

// ── Skills ───────────────────────────────────────────────────────────────────
async function loadSkills() {
  try {
    const res = await fetch(`${API}/skills`);
    const skills = await res.json();
    const wrap = document.getElementById("skills-wrap");
    wrap.innerHTML = "";

    skills.forEach(skill => {
      const tag = document.createElement("button");
      tag.className = "skill-tag";
      tag.textContent = skill;
      tag.addEventListener("click", () => toggleSkillFilter(skill, tag));
      wrap.appendChild(tag);
    });
  } catch (e) {
    document.getElementById("skills-wrap").innerHTML =
      '<p style="color:var(--muted);font-size:13px">Could not load skills.</p>';
  }
}

function toggleSkillFilter(skill, tagEl) {
  const allTags = document.querySelectorAll(".skill-tag");
  if (activeSkill === skill) {
    activeSkill = null;
    allTags.forEach(t => t.classList.remove("active"));
    clearSearch();
    renderProjects(allProjects);
    setFilterLabel(null);
  } else {
    activeSkill = skill;
    allTags.forEach(t => t.classList.remove("active"));
    tagEl.classList.add("active");
    fetchProjectsBySkill(skill);
  }
}

// ── Projects ─────────────────────────────────────────────────────────────────
async function loadProjects() {
  try {
    const res = await fetch(`${API}/projects`);
    allProjects = await res.json();
    renderProjects(allProjects);
  } catch (e) {
    document.getElementById("projects-grid").innerHTML =
      '<p style="color:var(--muted);font-size:13px">Could not load projects.</p>';
  }
}

async function fetchProjectsBySkill(skill) {
  showProjectSkeletons();
  try {
    const res = await fetch(`${API}/projects/${encodeURIComponent(skill)}`);
    const data = await res.json();
    renderProjects(data);
    setFilterLabel(`Showing projects tagged: ${skill}`);
  } catch (e) {
    renderProjects([]);
  }
}

function renderProjects(projects) {
  const grid = document.getElementById("projects-grid");
  const noResults = document.getElementById("no-results");
  grid.innerHTML = "";

  if (!projects.length) {
    noResults.classList.remove("hidden");
    return;
  }
  noResults.classList.add("hidden");

  projects.forEach((p, i) => {
    const title = p.title ?? p[0];
    const desc = p.description ?? p[1];
    const link = p.link ?? p[2];

    const card = document.createElement("div");
    card.className = "card";
    card.style.animationDelay = `${i * 60}ms`;
    card.innerHTML = `
      <h3>${escHtml(title)}</h3>
      <p>${escHtml(desc)}</p>
      <a href="${escHtml(link)}" target="_blank" rel="noopener">View Project ↗</a>
    `;
    grid.appendChild(card);
  });
}

function showProjectSkeletons() {
  const grid = document.getElementById("projects-grid");
  grid.innerHTML = `
    <div class="card-skeleton"></div>
    <div class="card-skeleton"></div>
    <div class="card-skeleton"></div>
  `;
  document.getElementById("no-results").classList.add("hidden");
}

function setFilterLabel(text) {
  const el = document.getElementById("filter-label");
  if (text) {
    el.textContent = text;
    el.classList.remove("hidden");
  } else {
    el.classList.add("hidden");
  }
}

// ── Search ────────────────────────────────────────────────────────────────────
document.getElementById("search-btn").addEventListener("click", doSearch);
document.getElementById("search-input").addEventListener("keydown", e => {
  if (e.key === "Enter") doSearch();
});
document.getElementById("clear-btn").addEventListener("click", () => {
  clearSearch();
  renderProjects(allProjects);
  setFilterLabel(null);
});

async function doSearch() {
  const q = document.getElementById("search-input").value.trim();
  if (!q) return;

  activeSkill = null;
  document.querySelectorAll(".skill-tag").forEach(t => t.classList.remove("active"));

  showProjectSkeletons();
  document.getElementById("clear-btn").classList.remove("hidden");

  try {
    const res = await fetch(`${API}/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    renderProjects(data);
    setFilterLabel(`Search results for: "${q}"`);
  } catch (e) {
    renderProjects([]);
  }
}

function clearSearch() {
  document.getElementById("search-input").value = "";
  document.getElementById("clear-btn").classList.add("hidden");
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Boot ──────────────────────────────────────────────────────────────────────
(async () => {
  await wakeServer();
  await Promise.all([loadProfile(), loadSkills(), loadProjects()]);
})();

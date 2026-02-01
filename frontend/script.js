const API = "https://me-api-playground-zrps.onrender.com";

let PROJECTS = []

async function loadProfile() {
  const res = await fetch(`${API}/profile`);
  const data = await res.json();

  document.getElementById("name").innerText = data.name;
  document.getElementById("email").innerText = data.email;
  document.getElementById("education").innerText = data.education;
}

async function loadSkills() {
  const res = await fetch(`${API}/skills`);
  const data = await res.json();

  const ul = document.getElementById("skills");
  ul.innerHTML = "";
  data.forEach(skill => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.setAttribute('href', `?skill=${skill}`)
    a.textContent = skill;
     a.addEventListener("click", (e) => {
      e.preventDefault();
      history.pushState(null, "", `?skill=${skill}`);
      filterSkills()
    });
    li.appendChild(a)
    ul.appendChild(li);
  });
}


function handleRouteChange() {
  const params = new URLSearchParams(window.location.search);
  const skill = params.get("skill");

  if (skill) {
    filterSkills(); 
  } else {
    loadProjects();
  }
}

async function filterSkills() {
 const params = new URLSearchParams(window.location.search);
  const skill = params.get('skill');

  if (!skill) return;

  const res = await fetch(`${API}/projects/${skill}`);
  const data = await res.json();

  PROJECTS = data; 
  renderProjects(); 
}

async function loadProjects() {
 console.log('load projects');

  const res = await fetch(`${API}/projects`);
  const data = await res.json();

  PROJECTS = data;   // overwrite instead of reset + refill
  renderProjects();
}

function renderProjects() {
  const div = document.getElementById("projects");
  div.innerHTML = "";
  PROJECTS.forEach(p => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${p[0]}</h3>
      <p>${p[1]}</p>
      <a href="${p[2]}" target="_blank">View</a>
    `;
    div.appendChild(card);
  });
}

window.addEventListener("popstate", () => {
  handleRouteChange();
})

loadProfile();
loadSkills();
loadProjects();

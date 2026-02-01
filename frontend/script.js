const API = "http://127.0.0.1:5000";

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
    li.innerText = skill;
    ul.appendChild(li);
  });
}

async function loadProjects() {
  const res = await fetch(`${API}/projects`);
  const data = await res.json();

  const div = document.getElementById("projects");
  div.innerHTML = "";
  data.forEach(p => {
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

loadProfile();
loadSkills();
loadProjects();

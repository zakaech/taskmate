const listEl = document.getElementById("task-list");
const statsEl = document.getElementById("stats");
const errorEl = document.getElementById("error");
const form = document.getElementById("task-form");

const PRIORITY_LABELS = { low: "basse", medium: "moyenne", high: "haute" };

// ---------- Appels à l'API ----------
async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (response.status === 204) return null;
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Erreur serveur");
  return data;
}

function buildQuery() {
  const params = new URLSearchParams();
  const category = document.getElementById("filter-category").value.trim();
  const priority = document.getElementById("filter-priority").value;
  const done = document.getElementById("filter-done").value;
  if (category) params.set("category", category);
  if (priority) params.set("priority", priority);
  if (done) params.set("done", done);
  if (document.getElementById("sort-due").checked) params.set("sort", "due_date");
  const query = params.toString();
  return query ? `/tasks?${query}` : "/tasks";
}

// ---------- Affichage ----------
async function loadTasks() {
  const tasks = await api(buildQuery());
  listEl.innerHTML = "";
  tasks.forEach((task) => listEl.appendChild(renderTask(task)));
  loadStats();
}

async function loadStats() {
  const s = await api("/tasks/stats");
  statsEl.textContent =
    `${s.total} tâche(s) : ${s.done} terminée(s), ${s.remaining} restante(s)`;
}

function renderTask(task) {
  const li = document.createElement("li");
  li.className = `task ${task.priority}${task.done ? " done" : ""}`;

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = task.done;
  checkbox.addEventListener("change", () => updateTask(task.id, { done: checkbox.checked }));

  const info = document.createElement("div");
  info.className = "task-info";
  const title = document.createElement("div");
  title.className = "task-title";
  title.textContent = task.title;
  const meta = document.createElement("div");
  meta.className = "task-meta";
  meta.textContent =
    `${task.category} · priorité ${PRIORITY_LABELS[task.priority]}` +
    (task.due_date ? ` · pour le ${task.due_date}` : "");
  info.append(title, meta);

  const editBtn = document.createElement("button");
  editBtn.className = "secondary";
  editBtn.textContent = "Modifier";
  editBtn.addEventListener("click", () => {
    const newTitle = prompt("Nouveau titre :", task.title);
    if (newTitle !== null) updateTask(task.id, { title: newTitle });
  });

  const deleteBtn = document.createElement("button");
  deleteBtn.className = "danger";
  deleteBtn.textContent = "Supprimer";
  deleteBtn.addEventListener("click", () => deleteTask(task.id));

  li.append(checkbox, info, editBtn, deleteBtn);
  return li;
}

// ---------- Actions ----------
async function updateTask(id, changes) {
  try {
    await api(`/tasks/${id}`, { method: "PUT", body: JSON.stringify(changes) });
    loadTasks();
  } catch (err) {
    alert(err.message);
  }
}

async function deleteTask(id) {
  if (!confirm("Supprimer cette tâche ?")) return;
  await api(`/tasks/${id}`, { method: "DELETE" });
  loadTasks();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorEl.textContent = "";
  const body = {
    title: document.getElementById("title").value,
    category: document.getElementById("category").value,
    priority: document.getElementById("priority").value,
    due_date: document.getElementById("due_date").value,
  };
  try {
    await api("/tasks", { method: "POST", body: JSON.stringify(body) });
    form.reset();
    loadTasks();
  } catch (err) {
    errorEl.textContent = err.message;
  }
});

["filter-category", "filter-priority", "filter-done", "sort-due"].forEach((id) =>
  document.getElementById(id).addEventListener("input", loadTasks)
);

loadTasks();
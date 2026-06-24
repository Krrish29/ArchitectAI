export const getProjects = () => {
  return JSON.parse(localStorage.getItem("projects")) || [];
};

export const saveProject = (project) => {
  const projects = getProjects();

  localStorage.setItem(
    "projects",
    JSON.stringify([project, ...projects])
  );
};

export const deleteProject = (id) => {
  const projects = getProjects().filter(
    (project) => project.id !== id
  );

  localStorage.setItem(
    "projects",
    JSON.stringify(projects)
  );
};
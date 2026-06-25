export const getProjects = () => {
  return JSON.parse(
    localStorage.getItem("projects")
  ) || [];
};

export const saveProject = (project) => {
  const projects = getProjects();

  localStorage.setItem(
    "projects",
    JSON.stringify([project, ...projects])
  );
};

export const deleteProject = (id) => {
  const updatedProjects = getProjects().filter(
    (project) => project.id !== id
  );

  localStorage.setItem(
    "projects",
    JSON.stringify(updatedProjects)
  );

  return updatedProjects;
};

export const renameProject = (
  id,
  newTitle
) => {
  const updatedProjects = getProjects().map(
    (project) =>
      project.id === id
        ? {
            ...project,
            title: newTitle,
          }
        : project
  );

  localStorage.setItem(
    "projects",
    JSON.stringify(updatedProjects)
  );

  return updatedProjects;
};

export const togglePinProject = (id) => {
  const updatedProjects = getProjects()
    .map((project) =>
      project.id === id
        ? {
            ...project,
            pinned: !project.pinned,
          }
        : project
    )
    .sort((a, b) => {
      if (
        (b.pinned || false) !==
        (a.pinned || false)
      ) {
        return (b.pinned || false) - (a.pinned || false);
      }

      return 0;
    });

  localStorage.setItem(
    "projects",
    JSON.stringify(updatedProjects)
  );

  return updatedProjects;
};
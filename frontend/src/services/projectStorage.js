export const getProjects = () => {
  return (
    JSON.parse(
      localStorage.getItem("projects")
    ) || []
  );
};

export const saveProjects = (
  projects
) => {
  localStorage.setItem(
    "projects",
    JSON.stringify(projects)
  );
};

export const saveProject = (
  project
) => {
  const projects = getProjects();

  saveProjects([
    project,
    ...projects,
  ]);
};

export const deleteProject = (
  id
) => {
  const updatedProjects =
    getProjects().filter(
      (project) =>
        project.id !== id
    );

  saveProjects(updatedProjects);

  return updatedProjects;
};

export const renameProject = (
  id,
  newTitle
) => {
  const updatedProjects =
    getProjects().map(
      (project) =>
        project.id === id
          ? {
              ...project,
              title: newTitle,
            }
          : project
    );

  saveProjects(updatedProjects);

  return updatedProjects;
};

export const togglePinProject = (
  id
) => {
  const updatedProjects =
    getProjects()
      .map((project) =>
        project.id === id
          ? {
              ...project,
              pinned:
                !project.pinned,
            }
          : project
      )
      .sort((a, b) => {
        if (
          (b.pinned ||
            false) !==
          (a.pinned || false)
        ) {
          return (
            (b.pinned ||
              false) -
            (a.pinned ||
              false)
          );
        }

        return 0;
      });

  saveProjects(updatedProjects);

  return updatedProjects;
};

/* ---------------------------------- */
/* NEW */
/* ---------------------------------- */

export const updateProjectBlueprint =
  (
    id,
    blueprint
  ) => {
    const updatedProjects =
      getProjects().map(
        (project) =>
          project.id === id
            ? {
                ...project,
                blueprint,
              }
            : project
      );

    saveProjects(updatedProjects);

    return updatedProjects;
  };

export const updateBlueprintSection =
  (
    id,
    section,
    data
  ) => {
    const updatedProjects =
      getProjects().map(
        (project) => {
          if (
            project.id !== id
          )
            return project;

          return {
            ...project,
            blueprint: {
              ...project.blueprint,
              [section]: data,
            },
          };
        }
      );

    saveProjects(updatedProjects);

    return updatedProjects;
  };
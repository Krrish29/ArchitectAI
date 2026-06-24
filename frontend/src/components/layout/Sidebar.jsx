import useBlueprint from "../../hooks/useBlueprint";

function Sidebar() {
  const {
    projects,
    setBlueprint,
    setSelectedProject,
    setTimeline,
    setMessages,
  } = useBlueprint();

  const handleProjectClick = (project) => {
    setSelectedProject(project);
    setBlueprint(project.blueprint);

    setTimeline({
      supervisor: "completed",
      requirement: "completed",
      architecture: "completed",
      planner: "completed",
    });

    // Only show the original user prompt
    setMessages([
      {
        role: "user",
        content: project.idea,
      },
    ]);
  };

  const handleNewProject = () => {
    setSelectedProject(null);
    setBlueprint(null);

    setTimeline({
      supervisor: "pending",
      requirement: "pending",
      architecture: "pending",
      planner: "pending",
    });

    setMessages([]);
  };

  return (
    <aside className="w-[260px] bg-[#171717] border-r border-[#2F2F2F] flex flex-col">
      {/* Logo */}
      <div className="p-4 border-b border-[#2F2F2F]">
        <h1 className="text-xl font-semibold text-white">
          ArchitectAI
        </h1>

        <p className="text-xs text-[#8E8EA0] mt-1">
          AI Software Architect
        </p>
      </div>

      {/* New Chat */}
      <div className="p-3">
        <button
          onClick={handleNewProject}
          className="
            w-full
            rounded-xl
            border
            border-[#3F3F46]
            px-4
            py-3
            text-white
            text-sm
            font-medium
            hover:bg-[#2A2A2A]
            transition
          "
        >
          + New Chat
        </button>
      </div>

      {/* Projects */}
      <div className="flex-1 overflow-y-auto px-2 pb-4">
        <p className="px-3 py-2 text-xs uppercase tracking-wider text-[#8E8EA0]">
          Recent Projects
        </p>

        {projects.length === 0 ? (
          <div className="px-3 py-3 text-sm text-[#8E8EA0]">
            No projects yet
          </div>
        ) : (
          projects.map((project) => (
            <button
              key={project.id}
              onClick={() =>
                handleProjectClick(project)
              }
              className="
                w-full
                text-left
                px-3
                py-3
                rounded-lg
                text-sm
                text-[#ECECEC]
                hover:bg-[#2A2A2A]
                transition
                truncate
                mb-1
              "
            >
              {project.title}
            </button>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-[#2F2F2F] p-4">
        <p className="text-xs text-[#8E8EA0]">
          ArchitectAI v1
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;
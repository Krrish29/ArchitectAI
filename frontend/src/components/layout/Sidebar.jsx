import { useState } from "react";

import useBlueprint from "../../hooks/useBlueprint";

import SidebarMenu from "../common/SidebarMenu";
import DeleteProjectModal from "../modal/DeleteProjectModal";

function Sidebar() {
  const {
    projects,
    selectedProject,

    setBlueprint,
    setSelectedProject,

    setTimeline,
    setMessages,

    removeProject,
  } = useBlueprint();

  const [deleteProject, setDeleteProject] =
    useState(null);

  const handleProjectClick = (project) => {
    setSelectedProject(project);

    setBlueprint(project.blueprint);

    const newTimeline = {
      supervisor: "completed",
    };

    project.blueprint?.selected_agents?.forEach(
      (agent) => {
        newTimeline[agent] =
          "completed";
      }
    );

    setTimeline(newTimeline);

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
      database: "pending",
      api: "pending",
      planner: "pending",
    });

    setMessages([]);
  };

  const openDeleteModal = (
    project
  ) => {
    setDeleteProject(project);
  };

  return (
    <>
      <aside
        className="
          relative
          w-72
          bg-[#171717]
          border-r
          border-[#262626]
          flex
          flex-col
          overflow-visible
        "
      >
        {/* Header */}

        <div className="px-5 py-5 border-b border-[#262626]">
          <h1 className="text-2xl font-semibold text-white">
            ArchitectAI
          </h1>

          <p className="text-sm text-[#8E8EA0] mt-1">
            AI Software Architect
          </p>
        </div>

        {/* New Blueprint */}

        <div className="p-4">
          <button
            onClick={handleNewProject}
            className="
              w-full
              rounded-xl
              border
              border-[#3A3A3A]
              bg-[#1E1E1E]
              px-4
              py-3
              text-sm
              font-medium
              text-white
              transition-all
              hover:bg-[#2A2A2A]
              hover:border-[#4A4A4A]
            "
          >
            + New Blueprint
          </button>
        </div>

        {/* Projects */}

        <div className="flex-1 overflow-y-auto overflow-x-visible px-3 pb-4">
          <p
            className="
              px-3
              pb-3
              text-xs
              uppercase
              tracking-widest
              text-[#8E8EA0]
            "
          >
            Recent Projects
          </p>

          {projects.length === 0 ? (
            <div className="px-3 py-3 text-sm text-[#8E8EA0]">
              No projects yet
            </div>
          ) : (
            <div className="space-y-1">
              {projects.map((project) => {
                const isSelected =
                  selectedProject?.id ===
                  project.id;

                return (
                  <div
                    key={project.id}
                    className={`
                      group
                      flex
                      items-center
                      justify-between
                      rounded-xl
                      transition-all
                      ${
                        isSelected
                          ? "bg-[#2A2A2A]"
                          : "hover:bg-[#222222]"
                      }
                    `}
                  >
                    <button
                      onClick={() =>
                        handleProjectClick(
                          project
                        )
                      }
                      className={`
                        flex-1
                        text-left
                        px-3
                        py-3
                        truncate
                        text-sm
                        ${
                          isSelected
                            ? "text-white"
                            : "text-[#ECECEC]"
                        }
                      `}
                    >
                      {project.pinned && (
                        <span className="mr-2">
                          📌
                        </span>
                      )}

                      {project.title}
                    </button>

                    <div className="pr-2">
                      <SidebarMenu
                        pinned={
                          project.pinned
                        }
                        onPin={() => {}}
                        onRename={() => {}}
                        onDelete={() =>
                          openDeleteModal(
                            project
                          )
                        }
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer */}

        <div className="border-t border-[#262626] px-5 py-4">
          <p className="text-xs text-[#8E8EA0]">
            ArchitectAI v1.0
          </p>
        </div>
      </aside>

      {deleteProject && (
        <DeleteProjectModal
          project={deleteProject}
          onCancel={() =>
            setDeleteProject(null)
          }
onDelete={() => {
  removeProject(
    deleteProject.id,
    selectedProject?.id === deleteProject.id
  );

  setDeleteProject(null);
}}
        />
      )}
    </>
  );
}

export default Sidebar;
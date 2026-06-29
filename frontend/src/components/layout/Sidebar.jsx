import { useEffect, useRef, useState } from "react";

import { Pin } from "lucide-react";

import useBlueprint from "../../hooks/useBlueprint";

import SidebarMenu from "../common/SidebarMenu";
import DeleteProjectModal from "../modal/DeleteProjectModal";

function Sidebar() {
  const {
    projects,
    selectedProject,

    setBlueprint,
    setSelectedProject,
    setNewChat,

    setTimeline,
    setMessages,

    resetChat,
    removeProject,
    updateProjectTitle,
    toggleProjectPin,
  } = useBlueprint();

  const [deleteProject, setDeleteProject] =
    useState(null);

  const [editingId, setEditingId] =
    useState(null);

  const [editingTitle, setEditingTitle] =
    useState("");

  const inputRef = useRef(null);

  useEffect(() => {
    if (editingId && inputRef.current) {
      inputRef.current.focus();

      inputRef.current.select();
    }
  }, [editingId]);

  const pinnedProjects =
    projects.filter(
      (project) => project.pinned
    );

  const recentProjects =
    projects.filter(
      (project) => !project.pinned
    );

  const buildInitialTimeline = (executionPlan = []) => {
    const visibleAgents = Array.isArray(executionPlan)
      ? executionPlan.filter(Boolean)
      : [];

    return {
      supervisor: "pending",
      ...Object.fromEntries(visibleAgents.map((agent) => [agent, "pending"])),
    };
  };

  const buildTimelineFromEvents = (events, executionPlan = []) => {
    const initialTimeline = buildInitialTimeline(executionPlan);

    if (!Array.isArray(events)) {
      return initialTimeline;
    }

    return events.reduce((timelineState, event) => {
      if (event?.type === "agent" && event.agent) {
        const shouldDisplay =
          event.agent === "supervisor" ||
          (Array.isArray(executionPlan) && executionPlan.includes(event.agent));

        if (!shouldDisplay) {
          return timelineState;
        }

        return {
          ...timelineState,
          [event.agent]: event.status,
        };
      }

      return timelineState;
    }, initialTimeline);
  };

  const handleProjectClick = (
    project
  ) => {
    setSelectedProject(project);
    setNewChat(false);

    setBlueprint(project.blueprint);

    const newTimeline = buildTimelineFromEvents(
      project.events,
      project.blueprint?.execution_plan || []
    );

    if (!project.events?.length) {
      Object.keys(newTimeline).forEach((key) => {
        if (key !== "supervisor") {
          newTimeline[key] = "completed";
        }
      });
    }

    setTimeline(newTimeline);

    setMessages([
      {
        role: "user",
        content: project.idea,
      },
    ]);
  };

  const handleNewProject = () => {
    resetChat();
    setSelectedProject(null);
    setNewChat(true);
    setBlueprint(null);
    setMessages([]);
    setTimeline({
      supervisor: "pending",
    });

    setTimeout(() => {
      const promptBox = document.querySelector("textarea[placeholder='Describe the software you want to build...']");
      if (promptBox) {
        promptBox.focus();
      }
    }, 0);
  };

  const openDeleteModal = (
    project
  ) => {
    setDeleteProject(project);
  };

  const startRename = (
    project
  ) => {
    setEditingId(project.id);

    setEditingTitle(project.title);
  };

  const saveRename = () => {
    if (!editingId) return;

    const title =
      editingTitle.trim();

    if (title.length) {
      updateProjectTitle(
        editingId,
        title
      );
    }

    setEditingId(null);

    setEditingTitle("");
  };

  const cancelRename = () => {
    setEditingId(null);

    setEditingTitle("");
  };

  const renderProject = (project) => {
  const isSelected =
    selectedProject?.id === project.id;

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
      {editingId === project.id ? (
        <input
          ref={inputRef}
          value={editingTitle}
          onChange={(e) =>
            setEditingTitle(
              e.target.value
            )
          }
          onBlur={saveRename}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              saveRename();
            }

            if (e.key === "Escape") {
              cancelRename();
            }
          }}
          className="
            flex-1
            bg-transparent
            px-3
            py-3
            text-sm
            text-white
            outline-none
          "
        />
      ) : (
<button
  onClick={() =>
    handleProjectClick(project)
  }
  className={`
    flex-1
    flex
    items-center
    gap-2
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
    <Pin
      size={14}
      strokeWidth={2}
      className="text-white shrink-0"
    />
  )}

  <span className="truncate">
    {project.title}
  </span>
</button>
      )}

      <div className="pr-2">
        <SidebarMenu
          pinned={project.pinned}
          onRename={() =>
            startRename(project)
          }
          onPin={() =>
            toggleProjectPin(
              project.id
            )
          }
          onDelete={() =>
            openDeleteModal(project)
          }
        />
      </div>
    </div>
  );
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
            hover:bg-[#2A2A2A]
            transition-all
          "
        >
          + New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-3 pb-4">
        {pinnedProjects.length > 0 && (
          <>
            <p className="px-3 pb-2 text-xs uppercase tracking-widest text-[#8E8EA0]">
              Pinned
            </p>

            <div className="space-y-1 mb-6">
              {pinnedProjects.map(renderProject)}
            </div>
          </>
        )}

        <p className="px-3 pb-2 text-xs uppercase tracking-widest text-[#8E8EA0]">
          Recent Projects
        </p>

        {recentProjects.length === 0 ? (
          <div className="px-3 py-3 text-sm text-[#8E8EA0]">
            No recent projects
          </div>
        ) : (
          <div className="space-y-1">
            {recentProjects.map(renderProject)}
          </div>
        )}
      </div>

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
            selectedProject?.id ===
              deleteProject.id
          );

          setDeleteProject(null);
        }}
      />
    )}
  </>
);
}

export default Sidebar;
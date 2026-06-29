import {
  createContext,
  useEffect,
  useState,
} from "react";

import {
  getProjects,
  deleteProject,
  renameProject,
  togglePinProject,
  updateBlueprintSection,
} from "../services/projectStorage";

export const BlueprintContext =
  createContext();

export const BlueprintProvider = ({
  children,
}) => {
  // ------------------------
  // Chat
  // ------------------------

  const [messages, setMessages] =
    useState([]);

  // ------------------------
  // Generation
  // ------------------------

  const [loading, setLoading] =
    useState(false);

  const [blueprint, setBlueprint] =
    useState(null);

  // ------------------------
  // Sidebar
  // ------------------------

  const [sidebarOpen, setSidebarOpen] =
    useState(true);

  // ------------------------
  // Streaming
  // ------------------------

  const [
    currentAgent,
    setCurrentAgent,
  ] = useState(null);

  // ------------------------
  // Timeline
  // ------------------------

  const [timeline, setTimeline] =
    useState({
      supervisor: "pending",
    });

  // ------------------------
  // Projects
  // ------------------------

  const [projects, setProjects] =
    useState([]);

  const [
    selectedProject,
    setSelectedProject,
  ] = useState(null);
  const [newChat, setNewChat] = useState(true);

  useEffect(() => {
    setProjects(getProjects());
  }, []);

  const resetChat = () => {
    setSelectedProject(null);
    setNewChat(true);
    setBlueprint(null);
    setMessages([]);
    setTimeline({
      supervisor: "pending",
    });
    setLoading(false);
    setCurrentAgent(null);
  };

  // ------------------------
  // Remove Project
  // ------------------------

  const removeProject = (id) => {
    const updatedProjects =
      deleteProject(id);

    setProjects(updatedProjects);

    if (
      selectedProject?.id === id
    ) {
      setSelectedProject(null);

      setBlueprint(null);

      setMessages([]);

      setTimeline({
        supervisor: "pending",
      });
    }
  };

  // ------------------------
  // Rename Project
  // ------------------------

  const updateProjectTitle = (
    id,
    title
  ) => {
    const updatedProjects =
      renameProject(id, title);

    setProjects(updatedProjects);

    if (
      selectedProject?.id === id
    ) {
      setSelectedProject({
        ...selectedProject,
        title,
      });
    }
  };

  // ------------------------
  // Pin Project
  // ------------------------

  const toggleProjectPin = (
    id
  ) => {
    const updatedProjects =
      togglePinProject(id);

    setProjects(updatedProjects);

    if (
      selectedProject?.id === id
    ) {
      const updated =
        updatedProjects.find(
          (project) =>
            project.id === id
        );

      setSelectedProject(updated);
    }
  };

  // ------------------------
  // Update Blueprint Section
  // ------------------------

  const updateProjectSection = (
    section,
    data
  ) => {
    if (!selectedProject) return;

    const updatedProjects =
      updateBlueprintSection(
        selectedProject.id,
        section,
        data
      );

    setProjects(updatedProjects);

    const updatedProject =
      updatedProjects.find(
        (project) =>
          project.id ===
          selectedProject.id
      );

    setSelectedProject(
      updatedProject
    );

    setBlueprint(
      updatedProject.blueprint
    );
  };

  return (
    <BlueprintContext.Provider
      value={{
        // Chat
        messages,
        setMessages,

        // Generation
        loading,
        setLoading,

        blueprint,
        setBlueprint,

        // Timeline
        timeline,
        setTimeline,

        // Streaming
        currentAgent,
        setCurrentAgent,

        // Sidebar
        sidebarOpen,
        setSidebarOpen,

        // Projects
        projects,
        setProjects,

        selectedProject,
        setSelectedProject,
        newChat,
        setNewChat,

        // Actions
        resetChat,
        removeProject,
        updateProjectTitle,
        toggleProjectPin,
        updateProjectSection,
      }}
    >
      {children}
    </BlueprintContext.Provider>
  );
}

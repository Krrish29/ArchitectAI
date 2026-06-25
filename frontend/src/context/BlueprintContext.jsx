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
} from "../services/projectStorage";

export const BlueprintContext =
  createContext();

export const BlueprintProvider = ({
  children,
}) => {
  // Chat
  const [messages, setMessages] =
    useState([]);

  // Generation
  const [loading, setLoading] =
    useState(false);

  const [blueprint, setBlueprint] =
    useState(null);

  // Sidebar
  const [sidebarOpen, setSidebarOpen] =
    useState(true);

  // Streaming
  const [
    currentAgent,
    setCurrentAgent,
  ] = useState(null);

  // Timeline
  const [timeline, setTimeline] =
    useState({
      supervisor: "pending",
      requirement: "pending",
      architecture: "pending",
      database: "pending",
      api: "pending",
      planner: "pending",
    });

  // Projects
  const [projects, setProjects] =
    useState([]);

  const [
    selectedProject,
    setSelectedProject,
  ] = useState(null);

  useEffect(() => {
    setProjects(getProjects());
  }, []);

  // ------------------------
  // Project Actions
  // ------------------------
const removeProject = (
  id,
  clearWorkspace = false
) => {
  
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
        requirement: "pending",
        architecture: "pending",
        database: "pending",
        api: "pending",
        planner: "pending",
      });
    }
  };

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
          (p) => p.id === id
        );

      setSelectedProject(updated);
    }
  };

  return (
    <BlueprintContext.Provider
      value={{
        messages,
        setMessages,

        loading,
        setLoading,

        blueprint,
        setBlueprint,

        timeline,
        setTimeline,

        currentAgent,
        setCurrentAgent,

        sidebarOpen,
        setSidebarOpen,

        projects,
        setProjects,

        selectedProject,
        setSelectedProject,

        removeProject,
        updateProjectTitle,
        toggleProjectPin,
      }}
    >
      {children}
    </BlueprintContext.Provider>
  );
};
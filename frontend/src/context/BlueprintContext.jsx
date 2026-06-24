import {
  createContext,
  useEffect,
  useState,
} from "react";
import { getProjects } from "../services/projectStorage";

export const BlueprintContext = createContext();

export const BlueprintProvider = ({
  children,
}) => {
  // Chat
  const [messages, setMessages] = useState([]);

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
      }}
    >
      {children}
    </BlueprintContext.Provider>
  );
};
import { generateBlueprint } from "../services/api";
import { saveProject } from "../services/projectStorage";
import Workspace from "../components/layout/Workspace";
import useBlueprint from "../hooks/useBlueprint";

function Dashboard() {
  const {
    messages,
    setMessages,
    loading,
    setLoading,
    blueprint,
    setBlueprint,
    timeline,
    setTimeline,
    projects,
    setProjects,
    setSelectedProject,
  } = useBlueprint();

  const handleGenerate = async (idea) => {
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: idea,
      },
    ]);

    setLoading(true);
    setBlueprint(null);

    setTimeline({
      supervisor: "running",
    });

    try {
      const data = await generateBlueprint(idea);

      // 🔍 DEBUG — check browser console
      console.log("=== FULL API RESPONSE ===", data);
      console.log("requirements:", data?.requirements);
      console.log("architecture:", data?.architecture);
      console.log("database:", data?.database);
      console.log("api:", data?.api);
      console.log("plan:", data?.plan);

      setBlueprint(data);

      const project = {
        id: Date.now(),
        title: idea,
        idea,
        blueprint: data,
        createdAt: new Date().toISOString(),
      };

      saveProject(project);

      setProjects((prev) => [project, ...prev]);

      setSelectedProject(project);

      const timelineState = {
        supervisor: "completed",
      };

      if (data.selected_agents) {
        data.selected_agents.forEach((agent) => {
          timelineState[agent] = "completed";
        });
      }

      setTimeline(timelineState);
    } catch (error) {
      console.error("Generation failed:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong while generating the blueprint.",
        },
      ]);

      setTimeline({
        supervisor: "failed",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Workspace
      onGenerate={handleGenerate}
      loading={loading}
      blueprint={blueprint}
      messages={messages}
      timeline={timeline}
    />
  );
}

export default Dashboard;
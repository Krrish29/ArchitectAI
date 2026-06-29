import {
  generateBlueprint,
  generateBlueprintStream,
} from "../services/api";
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
    setTimeline(buildInitialTimeline());

    const source = generateBlueprintStream(
      idea,
      (event) => {
        setTimeline((prev) => ({
          ...prev,
          [event.agent]: event.status,
        }));
      },
      (payload) => {
        const result = payload?.result || null;
        const timelineState = buildTimelineFromEvents(
          payload?.events || [],
          result?.execution_plan || []
        );

        setBlueprint(result);

        const project = {
          id: Date.now(),
          title: idea,
          idea,
          blueprint: result,
          events: payload?.events || [],
          createdAt: new Date().toISOString(),
        };

        saveProject(project);

        setProjects((prev) => [project, ...prev]);
        setSelectedProject(project);
        setTimeline(timelineState);
        setLoading(false);
      },
      (message) => {
        console.error("Generation failed:", message);

        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: "Something went wrong while generating the blueprint.",
          },
        ]);

        setLoading(false);
      }
    );

    source.onerror = () => {
      source.close();
      setLoading(false);
    };
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
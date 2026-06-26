import { Map } from "lucide-react";

import CardHeader from "./CardHeader";
import BlueprintCard from "./BlueprintCard";

const PLACEHOLDER_TASK = "Implementation details TBD";

function RoadmapCard({ roadmap }) {
  if (!roadmap) return null;

  const normalizeTasks = (tasks) => {
    if (!tasks) return [];
    if (Array.isArray(tasks)) return tasks;
    return [tasks];
  };

  const phases = Array.isArray(roadmap.phases) ? roadmap.phases : [];

  const handleCopy = async () => {
    const text = phases
      .map((phase, index) => {
        const title =
          typeof phase === "string"
            ? phase
            : phase?.phase_name || phase?.name || `Phase ${index + 1}`;

        const tasks = normalizeTasks(phase?.tasks).map((task) =>
          typeof task === "string"
            ? task
            : task?.task || task?.name || task?.title || task?.description || JSON.stringify(task)
        );

        return `${index + 1}. ${title}\n` + tasks.map((t) => `   - ${t}`).join("\n");
      })
      .join("\n\n");

    await navigator.clipboard.writeText(`Implementation Roadmap\n\n${text}`);
  };

  const renderTask = (task, index) => {
    const text =
      typeof task === "string"
        ? task
        : task?.task ||
          task?.name ||
          task?.title ||
          task?.description ||
          JSON.stringify(task);

    const isPlaceholder = text === PLACEHOLDER_TASK;

    return (
      <div
        key={index}
        className="flex items-start gap-3 text-[15px] leading-7"
      >
        <span
          className={`mt-1 ${isPlaceholder ? "text-[#5A5A5A]" : "text-green-400"}`}
        >
          {isPlaceholder ? "•" : "✓"}
        </span>
        <span className={isPlaceholder ? "text-[#8E8EA0] italic" : "text-[#ECECEC]"}>
          {text}
        </span>
      </div>
    );
  };

  return (
    <div className="mt-10">
      <CardHeader
        title="Implementation Roadmap"
        icon={Map}
        showEditControls={false}
        onCopy={handleCopy}
      />

      <BlueprintCard>
        <div className="space-y-8">
          {phases.map((phase, index) => {
            const phaseTitle =
              typeof phase === "string"
                ? phase
                : phase?.phase_name || phase?.name || `Phase ${index + 1}`;

            const tasks = normalizeTasks(phase?.tasks);
            const isLast = index === phases.length - 1;

            return (
              <div key={index} className="relative">
                {!isLast && (
                  <div className="absolute left-4 top-9 bottom-[-32px] w-px bg-[#2F2F2F]" />
                )}

                <div className="flex items-center gap-3 mb-4">
                  <div className="h-8 w-8 rounded-full bg-[#2A2A2A] border border-[#3A3A3A] flex items-center justify-center text-sm text-white font-medium shrink-0 relative z-10">
                    {index + 1}
                  </div>

                  <h3 className="text-lg font-medium text-white">
                    {phaseTitle}
                  </h3>
                </div>

                <div className="ml-11 space-y-2.5">
                  {tasks.length > 0 ? (
                    tasks.map(renderTask)
                  ) : (
                    <div className="text-[#5A5A5A] text-sm italic">
                      No tasks available
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </BlueprintCard>
    </div>
  );
}

export default RoadmapCard;
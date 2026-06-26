import {
  Bot,
  Boxes,
  Database,
  Network,
  ClipboardList,
  CalendarCheck,
  LoaderCircle,
  Check,
  Circle,
  CircleAlert,
} from "lucide-react";

function AgentTimeline({ timeline }) {
  if (!timeline || Object.keys(timeline).length === 0) {
    return null;
  }

  const agentMap = {
    requirement: {
      name: "Requirement Agent",
      icon: ClipboardList,
    },
    architecture: {
      name: "Architecture Agent",
      icon: Boxes,
    },
    database: {
      name: "Database Agent",
      icon: Database,
    },
    api: {
      name: "API Agent",
      icon: Network,
    },
    planner: {
      name: "Planner Agent",
      icon: CalendarCheck,
    },
  };

  const agents = [
    {
      name: "Supervisor Agent",
      icon: Bot,
      status: timeline.supervisor,
    },

    ...Object.entries(timeline)
      .filter(
        ([key]) => key !== "supervisor"
      )
      .map(([key, status]) => ({
        name:
          agentMap[key]?.name ??
          `${key} Agent`,
        icon:
          agentMap[key]?.icon ??
          Bot,
        status,
      })),
  ];

  const Status = ({ status }) => {
    switch (status) {
      case "running":
        return (
          <div className="flex items-center gap-2 text-blue-400">
            <LoaderCircle
              size={16}
              className="animate-spin"
            />

            <span className="text-sm">
              Running...
            </span>
          </div>
        );

      case "completed":
        return (
          <div className="flex items-center gap-2 text-green-400">
            <Check size={16} />

            <span className="text-sm">
              Completed
            </span>
          </div>
        );

      case "failed":
        return (
          <div className="flex items-center gap-2 text-red-400">
            <CircleAlert size={16} />

            <span className="text-sm">
              Failed
            </span>
          </div>
        );

      default:
        return (
          <div className="flex items-center gap-2 text-[#8E8EA0]">
            <Circle size={12} />

            <span className="text-sm">
              Waiting
            </span>
          </div>
        );
    }
  };

  return (
    <div className="max-w-4xl mt-8">
      {/* Header */}

      <div className="flex items-center gap-3 mb-8">
        <div
          className="
            h-10
            w-10
            rounded-full
            bg-[#2A2A2A]
            border
            border-[#333]
            flex
            items-center
            justify-center
          "
        >
          <Bot
            size={18}
            className="text-white"
          />
        </div>

        <div>
          <h2 className="text-white font-semibold">
            ArchitectAI
          </h2>

          <p className="text-[#8E8EA0] text-sm">
            Building your software architecture...
          </p>
        </div>
      </div>

      {/* Timeline */}

      <div className="space-y-3">
        {agents.map((agent) => {
          const Icon = agent.icon;

          return (
            <div
              key={agent.name}
              className="
                flex
                items-center
                justify-between
                rounded-xl
                px-4
                py-4
                bg-[#222222]
                border
                border-[#303030]
                hover:border-[#404040]
                transition-all
              "
            >
              <div className="flex items-center gap-3">
                <Icon
                  size={18}
                  className="text-white"
                />

                <span className="text-white">
                  {agent.name}
                </span>
              </div>

              <Status
                status={agent.status}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default AgentTimeline;
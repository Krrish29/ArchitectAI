function AgentTimeline({ timeline }) {
  if (!timeline || Object.keys(timeline).length === 0) {
    return null;
  }

  const agentMap = {
    requirement: "📋 Requirement Agent",
    architecture: "🏗 Architecture Agent",
    database: "🗄 Database Agent",
    api: "🔌 API Agent",
    planner: "🗺 Planner Agent",
  };

  const agents = [
    {
      name: "🧠 Supervisor Agent",
      status: timeline.supervisor,
    },

    ...Object.entries(timeline)
      .filter(
        ([key, status]) =>
          key !== "supervisor" &&
          status !== undefined
      )
      .map(([key, status]) => ({
        name: agentMap[key] || `🤖 ${key} Agent`,
        status,
      })),
  ];

  const getStatus = (status) => {
    switch (status) {
      case "running":
        return (
          <div className="flex items-center gap-2 text-yellow-400">
            <div className="flex gap-1">
              <span className="h-2 w-2 rounded-full bg-yellow-400 animate-bounce"></span>
              <span
                className="h-2 w-2 rounded-full bg-yellow-400 animate-bounce"
                style={{ animationDelay: "0.15s" }}
              ></span>
              <span
                className="h-2 w-2 rounded-full bg-yellow-400 animate-bounce"
                style={{ animationDelay: "0.3s" }}
              ></span>
            </div>

            <span>Thinking...</span>
          </div>
        );

      case "completed":
        return (
          <span className="text-green-400">
            ✓ Completed
          </span>
        );

      case "failed":
        return (
          <span className="text-red-400">
            ✕ Failed
          </span>
        );

      default:
        return (
          <span className="text-[#8E8EA0]">
            Waiting...
          </span>
        );
    }
  };

  return (
    <div className="max-w-4xl mt-8">
      {/* Assistant Header */}
      <div className="flex items-center gap-3 mb-8">
        <div
          className="
            h-10
            w-10
            rounded-full
            bg-[#303030]
            flex
            items-center
            justify-center
            text-lg
          "
        >
          🏗
        </div>

        <div>
          <h2 className="text-white font-semibold">
            ArchitectAI
          </h2>

          <p className="text-[#8E8EA0] text-sm">
            Analyzing your idea and generating a software blueprint...
          </p>
        </div>
      </div>

      {/* Agent Timeline */}
      <div className="space-y-3">
        {agents.map((agent) => (
          <div
            key={agent.name}
            className="
              flex
              items-center
              justify-between
              rounded-xl
              px-4
              py-4
              bg-[#2A2A2A]
              border
              border-[#3A3A3A]
            "
          >
            <span className="text-white">
              {agent.name}
            </span>

            {getStatus(agent.status)}
          </div>
        ))}
      </div>
    </div>
  );
}

export default AgentTimeline;
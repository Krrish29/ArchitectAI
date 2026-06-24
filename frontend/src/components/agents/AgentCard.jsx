function AgentCard({
  name,
  status,
}) {
  const config = {
    completed: {
      icon: "✓",
      text: "Completed",
      color: "text-green-400",
    },

    running: {
      icon: "●",
      text: "Thinking...",
      color:
        "text-yellow-400 animate-pulse",
    },

    pending: {
      icon: "○",
      text: "Waiting...",
      color: "text-[#8E8EA0]",
    },

    failed: {
      icon: "✕",
      text: "Failed",
      color: "text-red-400",
    },
  };

  const current =
    config[status] ??
    config.pending;

  return (
    <div
      className="
        flex
        items-center
        justify-between
        py-2
      "
    >
      <span className="text-white">
        {name}
      </span>

      <span className={current.color}>
        {current.icon} {current.text}
      </span>
    </div>
  );
}

export default AgentCard;
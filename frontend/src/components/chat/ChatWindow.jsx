import MessageBubble from "./MessageBubble";
import AgentTimeline from "../agents/AgentTimeline";

import RequirementCard from "../blueprint/RequirementCard";
import ArchitectureCard from "../blueprint/ArchitectureCard";
import DatabaseCard from "../blueprint/DatabaseCard";
import ApiCard from "../blueprint/ApiCard";
import RoadmapCard from "../blueprint/RoadmapCard";

function ChatWindow({
  messages = [],
  timeline,
  blueprint,
}) {
  // Empty State
  if (messages.length === 0) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center px-8">
          <h1 className="text-5xl font-semibold text-white mb-4">
            ArchitectAI
          </h1>

          <p className="text-[#B4B4B4] text-lg">
            What are we building today?
          </p>
        </div>
      </div>
    );
  }

  console.log("BLUEPRINT:", blueprint);

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <div className="space-y-8">
        {/* User Messages */}
        {messages.map((message, index) => (
          <MessageBubble
            key={index}
            sender={message.role}
            message={message.content}
          />
        ))}

        {/* Agent Execution Timeline */}
        <AgentTimeline timeline={timeline} />

        {/* Generated Blueprint */}
        {blueprint && (
          <div className="space-y-10">
            <RequirementCard
              requirements={blueprint.requirements}
            />

            <ArchitectureCard
              architecture={blueprint.architecture}
            />

            <DatabaseCard
              database={blueprint.database}
            />

            <ApiCard
              api={blueprint.api}
            />

            <RoadmapCard
              roadmap={blueprint.plan}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatWindow;
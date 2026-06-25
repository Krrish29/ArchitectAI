import {
  useEffect,
  useRef,
} from "react";

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
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [
    messages,
    timeline,
    blueprint,
  ]);

  // Empty State
  if (messages.length === 0) {
    return (
      <div className="h-full flex items-center justify-center px-8">
        <div className="max-w-2xl text-center">
          <h1 className="text-6xl font-semibold text-white mb-4">
            ArchitectAI
          </h1>

          <p className="text-[#A1A1AA] text-xl mb-10">
            Your AI Software Architect
          </p>

          <div className="grid grid-cols-2 gap-4 text-left">
            <div className="rounded-2xl border border-[#262626] bg-[#1E1E1E] p-5">
              <h3 className="text-white font-medium mb-2">
                🏗 Architecture Design
              </h3>

              <p className="text-sm text-[#8E8EA0]">
                Generate system designs and
                tech stacks.
              </p>
            </div>

            <div className="rounded-2xl border border-[#262626] bg-[#1E1E1E] p-5">
              <h3 className="text-white font-medium mb-2">
                🗄 Database Design
              </h3>

              <p className="text-sm text-[#8E8EA0]">
                Generate entities,
                relationships and indexes.
              </p>
            </div>

            <div className="rounded-2xl border border-[#262626] bg-[#1E1E1E] p-5">
              <h3 className="text-white font-medium mb-2">
                🔌 REST APIs
              </h3>

              <p className="text-sm text-[#8E8EA0]">
                Generate endpoints and
                request/response schemas.
              </p>
            </div>

            <div className="rounded-2xl border border-[#262626] bg-[#1E1E1E] p-5">
              <h3 className="text-white font-medium mb-2">
                🗺 Roadmaps
              </h3>

              <p className="text-sm text-[#8E8EA0]">
                Build implementation plans
                and phases.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-8 py-10">
      <div className="space-y-10">
        {messages.map(
          (message, index) => (
            <MessageBubble
              key={index}
              sender={message.role}
              message={message.content}
            />
          )
        )}

        <AgentTimeline
          timeline={timeline}
        />

        {blueprint && (
          <div className="space-y-14">
            <RequirementCard
              requirements={
                blueprint.requirements
              }
            />

            <ArchitectureCard
              architecture={
                blueprint.architecture
              }
            />

            <DatabaseCard
              database={
                blueprint.database
              }
            />

            <ApiCard
              api={blueprint.api}
            />

            <RoadmapCard
              roadmap={blueprint.plan}
            />
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}

export default ChatWindow;
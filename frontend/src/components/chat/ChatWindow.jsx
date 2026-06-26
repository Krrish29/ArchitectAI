import { useEffect, useRef } from "react";
import { Building2, Database, Webhook, Map } from "lucide-react";

import MessageBubble from "./MessageBubble";
import AgentTimeline from "../agents/AgentTimeline";

import RequirementCard from "../blueprint/RequirementCard";
import ArchitectureCard from "../blueprint/ArchitectureCard";
import DatabaseCard from "../blueprint/DatabaseCard";
import ApiCard from "../blueprint/ApiCard";
import RoadmapCard from "../blueprint/RoadmapCard";

const EMPTY_STATE_CARDS = [
  {
    icon: Building2,
    title: "Architecture Design",
    description: "Generate system designs and tech stacks.",
  },
  {
    icon: Database,
    title: "Database Design",
    description: "Generate entities, relationships and indexes.",
  },
  {
    icon: Webhook,
    title: "REST APIs",
    description: "Generate endpoints and request/response schemas.",
  },
  {
    icon: Map,
    title: "Roadmaps",
    description: "Build implementation plans and phases.",
  },
];

function ChatWindow({
  messages = [],
  timeline,
  blueprint,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, timeline, blueprint]);

  if (messages.length === 0) {
    return (
      <div className="h-full flex items-center justify-center px-8">
        <div className="max-w-2xl text-center">
          <h1 className="text-5xl font-semibold text-white mb-3 tracking-tight">
            ArchitectAI
          </h1>

          <p className="text-[#A1A1AA] text-lg mb-10">
            Your AI Software Architect
          </p>

          <div className="grid grid-cols-2 gap-4 text-left">
            {EMPTY_STATE_CARDS.map(({ icon: Icon, title, description }) => (
              <div
                key={title}
                className="rounded-2xl border border-[#2F2F2F] bg-[#1E1E1E] p-5"
              >
                <div className="flex items-center gap-2.5 mb-2">
                  <Icon size={18} className="text-[#8E8EA0]" strokeWidth={1.75} />
                  <h3 className="text-white font-medium">{title}</h3>
                </div>
                <p className="text-sm text-[#8E8EA0]">{description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-8 py-10">
      <div className="space-y-10">
        {messages.map((message, index) => (
          <MessageBubble
            key={index}
            sender={message.role}
            message={message.content}
          />
        ))}

        <AgentTimeline timeline={timeline} />

        {blueprint && (
          <div className="space-y-10">
            <RequirementCard requirements={blueprint.requirements} />
            <ArchitectureCard architecture={blueprint.architecture} />
            <DatabaseCard database={blueprint.database} />
            <ApiCard api={blueprint.api} />
            <RoadmapCard roadmap={blueprint.plan} />
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}

export default ChatWindow;
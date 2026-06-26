import { Building2 } from "lucide-react";

import CardHeader from "./CardHeader";
import BlueprintCard from "./BlueprintCard";

const SECTIONS = [
  { key: "frontend", label: "Frontend" },
  { key: "backend", label: "Backend" },
  { key: "database", label: "Database" },
  { key: "devops", label: "DevOps" },
  { key: "infrastructure", label: "Infrastructure" },
];

function ArchitectureCard({ architecture }) {
  if (!architecture) return null;

  const itemText = (item) => {
    if (!item) return "";
    return typeof item === "string"
      ? item
      : item.name || item.tech || item.title || JSON.stringify(item);
  };

  const handleCopy = async () => {
    const lines = SECTIONS.filter(({ key }) => architecture[key]?.length > 0).map(
      ({ key, label }) =>
        `${label}\n` + architecture[key].map((item) => `  - ${itemText(item)}`).join("\n")
    );
    await navigator.clipboard.writeText(`Architecture\n\n${lines.join("\n\n")}`);
  };

  const renderItem = (item, index) => {
    if (!item) return null;

    return (
      <div
        key={index}
        className="flex items-center gap-3 text-[#ECECEC] text-[15px]"
      >
        <span className="h-1.5 w-1.5 rounded-full bg-[#5A5A5A] shrink-0" />
        <span>{itemText(item)}</span>
      </div>
    );
  };

  return (
    <div className="mt-10">
      <CardHeader
        title="Architecture"
        icon={Building2}
        showEditControls={false}
        onCopy={handleCopy}
      />

      <BlueprintCard>
        <div className="space-y-6">
          {architecture.architecture_type && (
            <div>
              <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-2">
                Type
              </h3>
              <p className="text-[#ECECEC] text-[15px]">{architecture.architecture_type}</p>
            </div>
          )}

          {SECTIONS.map(({ key, label }) =>
            architecture[key]?.length > 0 ? (
              <div key={key}>
                <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-3">
                  {label}
                </h3>
                <div className="space-y-2">{architecture[key].map(renderItem)}</div>
              </div>
            ) : null
          )}

          {architecture.additional_features?.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-3">
                Additional Features
              </h3>
              <div className="space-y-3">
                {architecture.additional_features.map((feature, index) => (
                  <div key={index} className="border-l-2 border-[#2F2F2F] pl-4">
                    <p className="text-[#ECECEC] text-[15px] font-medium">
                      {feature?.name || `Feature ${index + 1}`}
                    </p>
                    {feature?.details && (
                      <p className="text-[#8E8EA0] text-sm mt-1">{feature.details}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </BlueprintCard>
    </div>
  );
}

export default ArchitectureCard;
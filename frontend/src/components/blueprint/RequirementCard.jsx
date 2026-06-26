import { useEffect, useState } from "react";

import { ClipboardList } from "lucide-react";

import useBlueprint from "../../hooks/useBlueprint";

import CardHeader from "./CardHeader";
import BlueprintCard from "./BlueprintCard";

function RequirementCard({ requirements }) {
  if (!requirements) return null;

  const { updateProjectSection } = useBlueprint();

  const [editing, setEditing] = useState(false);

  const [features, setFeatures] = useState(requirements.features);

  const [originalFeatures, setOriginalFeatures] = useState(
    requirements.features
  );

  useEffect(() => {
    setFeatures(requirements.features);
    setOriginalFeatures(requirements.features);
  }, [requirements]);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(
      "Requirements\n\n• " + features.join("\n• ")
    );
  };

  const handleEdit = () => {
    setEditing(true);
  };

  const handleSave = () => {
    const updatedRequirements = {
      ...requirements,
      features,
    };

    updateProjectSection("requirements", updatedRequirements);

    setOriginalFeatures(features);

    setEditing(false);
  };

  const handleCancel = () => {
    setFeatures(originalFeatures);

    setEditing(false);
  };

  return (
    <div className="mt-10">
      <CardHeader
        title="Requirements"
        icon={ClipboardList}
        editing={editing}
        onCopy={handleCopy}
        onEdit={handleEdit}
        onSave={handleSave}
        onCancel={handleCancel}
        onRegenerate={() => {}}
      />

      <BlueprintCard>
        <div className="space-y-4">
          {features.map((feature, index) => (
            <div key={index} className="flex items-start gap-3">
              <div className="mt-[9px] h-1.5 w-1.5 rounded-full bg-[#5A5A5A] shrink-0" />

              {editing ? (
                <input
                  value={feature}
                  onChange={(e) => {
                    const updated = [...features];

                    updated[index] = e.target.value;

                    setFeatures(updated);
                  }}
                  className="
                    w-full
                    bg-transparent
                    border-b
                    border-[#3A3A3A]
                    outline-none
                    text-white
                    py-1
                  "
                />
              ) : (
                <p className="text-[#ECECEC] text-[15px] leading-7">
                  {feature}
                </p>
              )}
            </div>
          ))}
        </div>
      </BlueprintCard>
    </div>
  );
}

export default RequirementCard;
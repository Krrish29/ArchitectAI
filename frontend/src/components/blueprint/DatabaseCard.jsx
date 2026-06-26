import { Database as DatabaseIcon } from "lucide-react";

import CardHeader from "./CardHeader";
import BlueprintCard from "./BlueprintCard";

function DatabaseCard({ database }) {
  if (!database) return null;

  const itemText = (item) => {
    if (!item) return "";
    return typeof item === "string"
      ? item
      : item.name
      ? `${item.name}${item.type ? ` (${item.type})` : ""}${
          item.description ? ` — ${item.description}` : ""
        }`
      : JSON.stringify(item);
  };

  const handleCopy = async () => {
    const sections = [
      database.database && `Database: ${database.database}`,
      database.entities?.length > 0 &&
        `Entities\n` + database.entities.map((e) => `  - ${itemText(e)}`).join("\n"),
      database.relationships?.length > 0 &&
        `Relationships\n` + database.relationships.map((r) => `  - ${itemText(r)}`).join("\n"),
      database.indexes?.length > 0 &&
        `Indexes\n` + database.indexes.map((i) => `  - ${itemText(i)}`).join("\n"),
    ].filter(Boolean);

    await navigator.clipboard.writeText(`Database Design\n\n${sections.join("\n\n")}`);
  };

  const renderItem = (item, index) => (
    <div
      key={index}
      className="flex items-center gap-3 text-[#ECECEC] text-[15px]"
    >
      <span className="h-1.5 w-1.5 rounded-full bg-[#5A5A5A] shrink-0" />
      <span>{itemText(item)}</span>
    </div>
  );

  return (
    <div className="mt-10">
      <CardHeader
        title="Database Design"
        icon={DatabaseIcon}
        showEditControls={false}
        onCopy={handleCopy}
      />

      <BlueprintCard>
        <div className="space-y-6">
          {database.database && (
            <div>
              <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-2">
                Database
              </h3>
              <p className="text-[#ECECEC] text-[15px]">{database.database}</p>
            </div>
          )}

          {database.entities?.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-3">
                Entities
              </h3>
              <div className="space-y-2">{database.entities.map(renderItem)}</div>
            </div>
          )}

          {database.relationships?.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-3">
                Relationships
              </h3>
              <div className="space-y-2">{database.relationships.map(renderItem)}</div>
            </div>
          )}

          {database.indexes?.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-3">
                Indexes
              </h3>
              <div className="space-y-2">{database.indexes.map(renderItem)}</div>
            </div>
          )}
        </div>
      </BlueprintCard>
    </div>
  );
}

export default DatabaseCard;
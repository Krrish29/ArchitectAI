import { Webhook } from "lucide-react";

import CardHeader from "./CardHeader";
import BlueprintCard from "./BlueprintCard";

const METHOD_COLORS = {
  GET: "text-green-400",
  POST: "text-blue-400",
  PUT: "text-yellow-400",
  PATCH: "text-orange-400",
  DELETE: "text-red-400",
};

function ApiCard({ api }) {
  if (!api) return null;

  const stringifyBlock = (value) =>
    typeof value === "string" ? value : JSON.stringify(value, null, 2);

  const handleCopy = async () => {
    const lines = [
      api.base_url && `Base URL: ${api.base_url}`,
      api.endpoints?.length > 0 &&
        "Endpoints\n" +
          api.endpoints
            .map((e) => `  ${e.method} ${e.path}${e.description ? ` — ${e.description}` : ""}`)
            .join("\n"),
    ].filter(Boolean);

    await navigator.clipboard.writeText(`REST APIs\n\n${lines.join("\n\n")}`);
  };

  return (
    <div className="mt-10">
      <CardHeader
        title="REST APIs"
        icon={Webhook}
        showEditControls={false}
        onCopy={handleCopy}
      />

      <BlueprintCard>
        <div className="space-y-6">
          {/* Base URL */}
          {api.base_url && (
            <div>
              <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-2">
                Base URL
              </h3>
              <p className="font-mono text-[#ECECEC] text-sm">{api.base_url}</p>
            </div>
          )}

          {/* Endpoints */}
          <div>
            <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-3">
              Endpoints
            </h3>
            <div className="space-y-3">
              {api.endpoints?.map((endpoint, index) => (
                <div
                  key={index}
                  className="border border-[#2F2F2F] rounded-xl p-4 space-y-2 bg-[#171717]"
                >
                  {/* Method + Path */}
                  <div className="flex items-center gap-3">
                    <span
                      className={`font-mono font-bold text-sm ${
                        METHOD_COLORS[endpoint.method] || "text-white"
                      }`}
                    >
                      {endpoint.method}
                    </span>
                    <span className="font-mono text-white text-sm">
                      {endpoint.path}
                    </span>
                  </div>

                  {/* Description */}
                  {endpoint.description && (
                    <p className="text-[#8E8EA0] text-sm">{endpoint.description}</p>
                  )}

                  {/* Request Body */}
                  {endpoint.request_body && (
                    <div>
                      <p className="text-xs text-[#5A5A5A] mb-1">Request Body</p>
                      <pre className="text-xs text-[#ECECEC] bg-[#0D0D0D] rounded p-3 overflow-auto">
                        {stringifyBlock(endpoint.request_body)}
                      </pre>
                    </div>
                  )}

                  {/* Response */}
                  {endpoint.response && (
                    <div>
                      <p className="text-xs text-[#5A5A5A] mb-1">Response</p>
                      <pre className="text-xs text-[#ECECEC] bg-[#0D0D0D] rounded p-3 overflow-auto">
                        {stringifyBlock(endpoint.response)}
                      </pre>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Request Schemas */}
          {api.request_schemas?.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-3">
                Request Schemas
              </h3>
              <div className="space-y-2">
                {api.request_schemas.map((schema, index) => (
                  <pre
                    key={index}
                    className="text-xs text-[#ECECEC] bg-[#0D0D0D] rounded p-3 overflow-auto"
                  >
                    {stringifyBlock(schema)}
                  </pre>
                ))}
              </div>
            </div>
          )}

          {/* Response Schemas */}
          {api.response_schemas?.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-[#8E8EA0] uppercase tracking-wide mb-3">
                Response Schemas
              </h3>
              <div className="space-y-2">
                {api.response_schemas.map((schema, index) => (
                  <pre
                    key={index}
                    className="text-xs text-[#ECECEC] bg-[#0D0D0D] rounded p-3 overflow-auto"
                  >
                    {stringifyBlock(schema)}
                  </pre>
                ))}
              </div>
            </div>
          )}
        </div>
      </BlueprintCard>
    </div>
  );
}

export default ApiCard;
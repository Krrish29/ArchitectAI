function ApiCard({ api }) {
  if (!api) return null;

  return (
    <div className="mt-10">
      <h2 className="text-2xl font-semibold text-white mb-6">
        🔌 REST APIs
      </h2>

      <div className="rounded-3xl border border-[#30363D] bg-[#111827] p-6 space-y-6">
        <div>
          <h3 className="text-lg font-medium text-white mb-3">
            Endpoints
          </h3>

          <div className="space-y-2">
            {api.endpoints?.map(
              (endpoint, index) => (
                <div
                  key={index}
                  className="text-[#ECECEC]"
                >
                  • {endpoint}
                </div>
              )
            )}
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium text-white mb-3">
            Request Schemas
          </h3>

          <div className="space-y-2">
            {api.request_schemas?.map(
              (schema, index) => (
                <div
                  key={index}
                  className="text-[#ECECEC]"
                >
                  • {schema}
                </div>
              )
            )}
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium text-white mb-3">
            Response Schemas
          </h3>

          <div className="space-y-2">
            {api.response_schemas?.map(
              (schema, index) => (
                <div
                  key={index}
                  className="text-[#ECECEC]"
                >
                  • {schema}
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ApiCard;
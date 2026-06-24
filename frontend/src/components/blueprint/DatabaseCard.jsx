function DatabaseCard({ database }) {
  if (!database) return null;

  return (
    <div className="mt-10">
      <h2 className="text-2xl font-semibold text-white mb-6">
        🗄️ Database Design
      </h2>

      <div className="rounded-3xl border border-[#30363D] bg-[#111827] p-6 space-y-6">
        <div>
          <h3 className="text-lg font-medium text-white mb-2">
            Database
          </h3>

          <p className="text-[#ECECEC]">
            {database.database}
          </p>
        </div>

        <div>
          <h3 className="text-lg font-medium text-white mb-3">
            Entities
          </h3>

          <div className="space-y-2">
            {database.entities?.map((entity, index) => (
              <div
                key={index}
                className="text-[#ECECEC]"
              >
                • {entity}
              </div>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium text-white mb-3">
            Relationships
          </h3>

          <div className="space-y-2">
            {database.relationships?.map(
              (relation, index) => (
                <div
                  key={index}
                  className="text-[#ECECEC]"
                >
                  • {relation}
                </div>
              )
            )}
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium text-white mb-3">
            Indexes
          </h3>

          <div className="space-y-2">
            {database.indexes?.map(
              (indexName, index) => (
                <div
                  key={index}
                  className="text-[#ECECEC]"
                >
                  • {indexName}
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DatabaseCard;
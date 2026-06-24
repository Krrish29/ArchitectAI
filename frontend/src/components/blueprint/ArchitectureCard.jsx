function ArchitectureCard({ architecture }) {
  if (!architecture) return null;

  return (
    <div className="mt-12">
      <h2 className="text-2xl font-semibold text-white mb-8">
        🏗 Architecture
      </h2>

      <div className="space-y-8">
        {/* Frontend */}
        <div>
          <h3 className="text-lg font-medium text-white mb-3">
            Frontend
          </h3>

          <div className="space-y-2">
            {architecture.frontend?.map(
              (item, index) => (
                <div
                  key={index}
                  className="
                    flex
                    items-center
                    gap-3
                    text-[#ECECEC]
                    text-[15px]
                  "
                >
                  <span className="text-[#8E8EA0]">
                    └
                  </span>

                  <span>{item}</span>
                </div>
              )
            )}
          </div>
        </div>

        {/* Backend */}
        <div>
          <h3 className="text-lg font-medium text-white mb-3">
            Backend
          </h3>

          <div className="space-y-2">
            {architecture.backend?.map(
              (item, index) => (
                <div
                  key={index}
                  className="
                    flex
                    items-center
                    gap-3
                    text-[#ECECEC]
                    text-[15px]
                  "
                >
                  <span className="text-[#8E8EA0]">
                    └
                  </span>

                  <span>{item}</span>
                </div>
              )
            )}
          </div>
        </div>

        {/* Database */}
        <div>
          <h3 className="text-lg font-medium text-white mb-3">
            Database
          </h3>

          <div className="space-y-2">
            {architecture.database?.map(
              (item, index) => (
                <div
                  key={index}
                  className="
                    flex
                    items-center
                    gap-3
                    text-[#ECECEC]
                    text-[15px]
                  "
                >
                  <span className="text-[#8E8EA0]">
                    └
                  </span>

                  <span>{item}</span>
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ArchitectureCard;
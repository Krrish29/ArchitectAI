function RoadmapCard({ roadmap }) {
  if (!roadmap) return null;

  return (
    <div className="mt-12">
      <h2 className="text-2xl font-semibold text-white mb-8">
        🗺 Implementation Roadmap
      </h2>

      <div className="space-y-10">
        {roadmap.phases?.map((phase, index) => (
          <div key={index}>
            {/* Phase Heading */}
            <div className="flex items-center gap-3 mb-4">
              <div
                className="
                  h-8
                  w-8
                  rounded-full
                  bg-[#303030]
                  flex
                  items-center
                  justify-center
                  text-sm
                  text-white
                  font-medium
                "
              >
                {index + 1}
              </div>

              <h3 className="text-xl font-medium text-white">
                {phase.phase_name}
              </h3>
            </div>

            {/* Tasks */}
            <div className="ml-11 space-y-3">
              {phase.tasks?.map((task, taskIndex) => (
                <div
                  key={taskIndex}
                  className="
                    flex
                    items-start
                    gap-3
                    text-[#ECECEC]
                    text-[15px]
                    leading-7
                  "
                >
                  <span className="text-green-400 mt-1">
                    ✓
                  </span>

                  <span>{task}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RoadmapCard;
function RequirementCard({
  requirements,
}) {
  if (!requirements) return null;

  return (
    <div className="mt-10">
      <h2 className="text-2xl font-semibold text-white mb-6">
        📋 Requirements
      </h2>

      <div className="space-y-3">
        {requirements.features?.map(
          (feature, index) => (
            <div
              key={index}
              className="
                text-[#ECECEC]
                text-[15px]
                leading-7
              "
            >
              • {feature}
            </div>
          )
        )}
      </div>
    </div>
  );
}

export default RequirementCard;
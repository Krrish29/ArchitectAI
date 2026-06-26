function BlueprintCard({ children }) {
  return (
    <div
      className="
        rounded-2xl
        border
        border-[#2F2F2F]
        bg-[#1E1E1E]
        p-6
      "
    >
      {children}
    </div>
  );
}

export default BlueprintCard;
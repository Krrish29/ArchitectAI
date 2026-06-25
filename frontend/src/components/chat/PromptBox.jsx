import { useRef, useState } from "react";
import { ArrowUp, Plus } from "lucide-react";

function PromptBox({
  onGenerate,
  loading = false,
}) {
  const [idea, setIdea] = useState("");
  const textareaRef = useRef(null);

  const handleSubmit = () => {
    if (!idea.trim() || loading) return;

    onGenerate(idea);

    setIdea("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "24px";
    }
  };

  const handleChange = (e) => {
    setIdea(e.target.value);

    const textarea = textareaRef.current;

    textarea.style.height = "24px";
    textarea.style.height =
      textarea.scrollHeight + "px";
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div
        className="
          rounded-[28px]
          border
          border-[#303030]
          bg-[#1E1E1E]
          px-4
          py-3
          flex
          items-end
          gap-3
          transition-all
          duration-200
          focus-within:border-[#4A4A4A]
          shadow-[0_0_40px_rgba(0,0,0,0.35)]
        "
      >
        {/* Left Button */}
        <button
          className="
            h-9
            w-9
            rounded-full
            flex
            items-center
            justify-center
            text-[#A1A1AA]
            hover:bg-[#2B2B2B]
            hover:text-white
            transition-all
            duration-150
          "
        >
          <Plus
            size={18}
            strokeWidth={2}
          />
        </button>

        {/* Prompt */}
        <textarea
          ref={textareaRef}
          rows={1}
          value={idea}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Describe the software you want to build..."
          className="
            flex-1
            bg-transparent
            text-white
            placeholder:text-[#8E8EA0]
            resize-none
            outline-none
            text-[15px]
            leading-7
            max-h-48
            overflow-y-auto
          "
        />

        {/* Send */}
        <button
          onClick={handleSubmit}
          disabled={!idea.trim() || loading}
          className="
            h-10
            w-10
            rounded-full
            bg-white
            text-black
            flex
            items-center
            justify-center
            transition-all
            duration-150
            hover:scale-105
            disabled:opacity-40
            disabled:cursor-not-allowed
          "
        >
          <ArrowUp
            size={18}
            strokeWidth={2.5}
          />
        </button>
      </div>
    </div>
  );
}

export default PromptBox;
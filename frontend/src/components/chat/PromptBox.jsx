import { useRef, useState } from "react";
import { HiArrowUp } from "react-icons/hi2";

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
          bg-[#2F2F2F]
          rounded-[28px]
          border
          border-[#444]
          px-5
          py-4
          flex
          items-end
          gap-4
        "
      >
        <textarea
          ref={textareaRef}
          rows={1}
          value={idea}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Message ArchitectAI..."
          className="
            flex-1
            bg-transparent
            text-white
            placeholder:text-[#8E8EA0]
            resize-none
            outline-none
            text-[16px]
            max-h-48
            overflow-y-auto
          "
        />

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
            transition
            disabled:opacity-40
            disabled:cursor-not-allowed
          "
        >
          <HiArrowUp size={20} />
        </button>
      </div>
    </div>
  );
}

export default PromptBox;
import {
  ChevronDown,
  EllipsisVertical,
} from "lucide-react";

function Header() {
  return (
    <header
      className="
        h-14
        bg-[#171717]
        border-b
        border-[#262626]
        px-6
        flex
        items-center
        justify-between
        shrink-0
      "
    >
      <div className="flex items-center gap-2 text-white text-[17px] font-semibold">
        <span>ArchitectAI</span>
        <ChevronDown
          size={16}
          strokeWidth={2}
          className="text-[#A1A1AA]"
        />
      </div>

      <button
        className="
          h-9
          w-9
          rounded-xl
          flex
          items-center
          justify-center
          text-[#A1A1AA]
          hover:bg-[#262626]
          hover:text-white
          transition-all
          duration-150
        "
      >
        <EllipsisVertical
          size={18}
          strokeWidth={2}
        />
      </button>
    </header>
  );
}

export default Header;
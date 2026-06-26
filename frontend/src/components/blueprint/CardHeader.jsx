import {
  Copy,
  Pencil,
  RotateCw,
  Save,
  X,
} from "lucide-react";

function CardHeader({
  title,
  icon: Icon,
  editing = false,
  showEditControls = true,

  onCopy,
  onEdit,
  onSave,
  onCancel,
  onRegenerate,
}) {
  return (
    <div className="flex items-center justify-between mb-6">
      <div className="flex items-center gap-2.5">
        {Icon && (
          <Icon size={20} className="text-[#8E8EA0]" strokeWidth={1.75} />
        )}
        <h2 className="text-2xl font-semibold text-white">
          {title}
        </h2>
      </div>

      <div className="flex items-center gap-2">
        {/* Copy */}

        <button
          onClick={onCopy}
          className="
            h-9
            w-9
            rounded-lg
            flex
            items-center
            justify-center
            text-[#A1A1AA]
            hover:bg-[#2A2A2A]
            hover:text-white
            transition
          "
          title="Copy"
        >
          <Copy size={18} />
        </button>

        {!showEditControls ? null : !editing ? (
          <>
            {/* Edit */}

            <button
              onClick={onEdit}
              className="
                h-9
                w-9
                rounded-lg
                flex
                items-center
                justify-center
                text-[#A1A1AA]
                hover:bg-[#2A2A2A]
                hover:text-white
                transition
              "
              title="Edit"
            >
              <Pencil size={18} />
            </button>

            {/* Regenerate */}

            <button
              onClick={onRegenerate}
              className="
                h-9
                w-9
                rounded-lg
                flex
                items-center
                justify-center
                text-[#A1A1AA]
                hover:bg-[#2A2A2A]
                hover:text-white
                transition
              "
              title="Regenerate"
            >
              <RotateCw size={18} />
            </button>
          </>
        ) : (
          <>
            {/* Save */}

            <button
              onClick={onSave}
              className="
                h-9
                w-9
                rounded-lg
                flex
                items-center
                justify-center
                text-green-400
                hover:bg-green-500/10
                transition
              "
              title="Save"
            >
              <Save size={18} />
            </button>

            {/* Cancel */}

            <button
              onClick={onCancel}
              className="
                h-9
                w-9
                rounded-lg
                flex
                items-center
                justify-center
                text-red-400
                hover:bg-red-500/10
                transition
              "
              title="Cancel"
            >
              <X size={18} />
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default CardHeader;
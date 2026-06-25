import { useEffect } from "react";
import { createPortal } from "react-dom";
import { Trash2 } from "lucide-react";

function DeleteProjectModal({
  project,
  onCancel,
  onDelete,
}) {
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape") {
        onCancel();
      }
    };

    document.addEventListener("keydown", handleEsc);

    return () =>
      document.removeEventListener(
        "keydown",
        handleEsc
      );
  }, [onCancel]);

  return createPortal(
    <div className="fixed inset-0 z-[99999] flex items-center justify-center">
      {/* Backdrop */}
      <div
        onClick={onCancel}
        className="absolute inset-0 bg-black/55 backdrop-blur-sm"
      />

      {/* Modal */}
      <div
        className="
          relative
          w-[380px]
          rounded-xl
          border
          border-[#3A3A3A]
          bg-[#202123]
          shadow-[0_20px_80px_rgba(0,0,0,0.6)]
          overflow-hidden
          animate-[fadeIn_.18s_ease]
        "
      >
        {/* Header */}
        <div className="flex items-center gap-3 px-5 py-4 border-b border-[#303030]">
          <div
            className="
              h-10
              w-10
              rounded-lg
              bg-red-500/10
              flex
              items-center
              justify-center
            "
          >
            <Trash2
              size={18}
              className="text-red-400"
            />
          </div>

          <div>
            <h2 className="text-base font-semibold text-white">
              Delete Project
            </h2>

            <p className="text-sm text-[#8E8EA0]">
              This action cannot be undone.
            </p>
          </div>
        </div>

        {/* Body */}
        <div className="px-5 py-5">
          <p className="text-[15px] leading-7 text-[#ECECEC]">
            Are you sure you want to delete{" "}
            <span className="font-semibold text-white">
              "{project.title}"
            </span>
            ?
          </p>

          <p className="mt-4 text-sm leading-6 text-[#8E8EA0]">
            The project, generated blueprint,
            architecture, APIs and roadmap will be
            permanently removed.
          </p>
        </div>

        {/* Footer */}
        <div className="flex justify-end gap-3 px-5 py-4 border-t border-[#303030]">
          <button
            onClick={onCancel}
            className="
              rounded-lg
              border
              border-[#3A3A3A]
              px-4
              py-2
              text-white
              hover:bg-[#2B2B2B]
              transition-all
            "
          >
            Cancel
          </button>

          <button
            onClick={onDelete}
            className="
              rounded-lg
              bg-[#EF4444]
              px-4
              py-2
              text-white
              hover:bg-[#DC2626]
              transition-all
            "
          >
            Delete
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
}

export default DeleteProjectModal;
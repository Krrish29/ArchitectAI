import {
  useEffect,
  useRef,
  useState,
} from "react";

import { createPortal } from "react-dom";

import {
  MoreHorizontal,
  Pencil,
  Trash2,
  Pin,
  PinOff,
} from "lucide-react";

function SidebarMenu({
  onRename,
  onDelete,
  onPin,
  pinned = false,
}) {
  const [open, setOpen] = useState(false);

  const buttonRef = useRef(null);
  const dropdownRef = useRef(null);

  const [position, setPosition] =
    useState({
      top: 0,
      left: 0,
    });

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target) &&
        buttonRef.current &&
        !buttonRef.current.contains(e.target)
      ) {
        setOpen(false);
      }
    };

    const handleEsc = (e) => {
      if (e.key === "Escape") {
        setOpen(false);
      }
    };

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    document.addEventListener(
      "keydown",
      handleEsc
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );

      document.removeEventListener(
        "keydown",
        handleEsc
      );
    };
  }, []);

  const toggleMenu = () => {
    if (!buttonRef.current) return;

    const rect =
      buttonRef.current.getBoundingClientRect();

    setPosition({
      top: rect.top,
      left: rect.right + 8,
    });

    setOpen((prev) => !prev);
  };

  return (
    <>
      {/* Three Dots */}
      <button
        ref={buttonRef}
        onClick={toggleMenu}
        className="
          opacity-0
          group-hover:opacity-100
          hover:opacity-100
          transition-opacity
          duration-150

          h-8
          w-8

          rounded-lg

          flex
          items-center
          justify-center

          text-[#8E8EA0]

          hover:bg-[#303030]
          hover:text-white
        "
      >
        <MoreHorizontal
          size={18}
          strokeWidth={2}
        />
      </button>

      {open &&
        createPortal(
          <div
            ref={dropdownRef}
            style={{
              position: "fixed",
              top: position.top,
              left: position.left,
            }}
            className="
              z-[9999]

              w-56

              rounded-2xl

              border
              border-[#303030]

              bg-[#202123]

              shadow-2xl

              overflow-hidden

              animate-[fadeIn_.15s_ease]
            "
          >
            {/* Rename */}

            <button
              onClick={() => {
                setOpen(false);
                onRename();
              }}
              className="
                w-full

                flex
                items-center
                gap-3

                px-4
                py-3

                text-sm
                text-white

                hover:bg-[#2D2D2D]

                transition
              "
            >
              <Pencil
                size={18}
                strokeWidth={2}
              />

              Rename
            </button>

            <div className="mx-2 border-t border-[#333]" />

            {/* Pin */}

            <button
              onClick={() => {
                setOpen(false);
                onPin();
              }}
              className="
                w-full

                flex
                items-center
                gap-3

                px-4
                py-3

                text-sm
                text-white

                hover:bg-[#2D2D2D]

                transition
              "
            >
              {pinned ? (
                <PinOff
                  size={18}
                  strokeWidth={2}
                />
              ) : (
                <Pin
                  size={18}
                  strokeWidth={2}
                />
              )}

              {pinned
                ? "Unpin Chat"
                : "Pin Chat"}
            </button>

            <div className="mx-2 border-t border-[#333]" />

            {/* Delete */}

            <button
              onClick={() => {
                setOpen(false);
                onDelete();
              }}
              className="
                w-full

                flex
                items-center
                gap-3

                px-4
                py-3

                text-sm

                text-red-400

                hover:bg-[#2D2D2D]

                transition
              "
            >
              <Trash2
                size={18}
                strokeWidth={2}
              />

              Delete
            </button>
          </div>,
          document.body
        )}
    </>
  );
}

export default SidebarMenu;
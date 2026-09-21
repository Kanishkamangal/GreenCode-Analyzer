import { FaArrowRight } from "react-icons/fa";

export default function OrbitArrow({ className = "" }) {
  return (
    <div
      className={`
        absolute
        ${className}
        flex
        items-center
        justify-center
        w-10
        h-10
      `}
    >
      <FaArrowRight
        className="
          text-[#166534]
          text-2xl
          drop-shadow-[0_0_6px_rgba(22,101,52,0.25)]
        "
      />
    </div>
  );
}
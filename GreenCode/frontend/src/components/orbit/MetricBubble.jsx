import {
  FaMicrochip,
  FaMemory,
  FaBolt,
  FaClock,
} from "react-icons/fa";

export default function MetricBubble({
  icon = "cpu",
  title,
  value,
  unit,
  className = "",
}) {
  const icons = {
    cpu: <FaMicrochip size={20} />,
    memory: <FaMemory size={20} />,
    energy: <FaBolt size={20} />,
    time: <FaClock size={20} />,
  };

  return (
    <div
      className={`
        absolute
        ${className}
        group

        w-[126px]
        h-[126px]
        rounded-full

        bg-[#FFFFFF]

        border
        border-[#D5E6D8]

        shadow-[0_8px_30px_rgba(15,23,42,0.07)]

        flex
        flex-col
        items-center
        justify-center
        text-center

        transition-all
        duration-300

        hover:scale-105
        hover:border-[#16A34A]
        hover:shadow-[0_12px_35px_rgba(11,107,43,0.14)]
      `}
    >

      {/* =================================================
          ICON
      ================================================= */}

      <div
        className="
          text-[#0B6B2B]
          mb-2
          transition-colors
          duration-300
          group-hover:text-[#16A34A]
        "
      >
        {icons[icon]}
      </div>


      {/* =================================================
          TITLE
      ================================================= */}

      <p
        className="
          text-[12px]
          text-[#6B7280]
          font-medium
        "
      >
        {title}
      </p>


      {/* =================================================
          VALUE
      ================================================= */}

      <h2
        className="
          text-[25px]
          font-bold
          text-[#0F172A]
          leading-none
          mt-1
        "
      >
        {value}
      </h2>


      {/* =================================================
          UNIT
      ================================================= */}

      <span
        className="
          text-[11px]
          text-[#0B6B2B]
          mt-1
          tracking-wider
          uppercase
          font-semibold
        "
      >
        {unit}
      </span>

    </div>
  );
}
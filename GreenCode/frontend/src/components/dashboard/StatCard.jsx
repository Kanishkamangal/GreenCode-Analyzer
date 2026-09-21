export default function StatCard({
  title,
  value,
  unit,
  description,
  icon,
}) {
  return (
    <div
      className="
        group
        relative
        overflow-hidden
        rounded-2xl
        border
        border-[#DDE8DF]
        bg-white
        p-6
        transition-all
        duration-300
        hover:-translate-y-1
        hover:border-[#3F6B4B]
        hover:shadow-[0_12px_30px_rgba(63,107,75,0.12)]
      "
    >
      {/* Background Glow */}

      <div
        className="
          absolute
          -top-16
          -right-16
          w-40
          h-40
          rounded-full
          bg-[#3F6B4B]/5
          blur-3xl
          group-hover:bg-[#3F6B4B]/10
          transition-all
          duration-500
        "
      />

      <div className="relative">

        {/* Header */}

        <div className="flex items-center justify-between">

          <p
            className="
              text-xs
              uppercase
              tracking-[0.18em]
              text-[#7A867D]
              font-semibold
            "
          >
            {title}
          </p>

          <span className="text-[#3F6B4B] text-xl">
            {icon}
          </span>

        </div>

        {/* Value */}

        <div className="mt-6 flex items-end gap-2">

          <span className="text-4xl font-bold text-[#1E2A22]">
            {value}
          </span>

          {unit && (
            <span className="mb-1 text-sm text-[#6C7A70]">
              {unit}
            </span>
          )}

        </div>

        {/* Description */}

        <p className="mt-4 text-sm leading-6 text-[#6C7A70]">
          {description}
        </p>

      </div>
    </div>
  );
}
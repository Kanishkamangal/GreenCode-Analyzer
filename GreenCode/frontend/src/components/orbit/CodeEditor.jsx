import { FaRegCopy } from "react-icons/fa";

export default function CodeEditor() {
  return (
    <div
      className="
        w-[520px]
        overflow-hidden
        rounded-2xl
        bg-[#FFFFFF]
        border
        border-[#D5E6D8]
        shadow-[0_18px_50px_rgba(15,23,42,0.08)]
        editorGlow
      "
    >

      {/* =================================================
          HEADER
      ================================================= */}

      <div
        className="
          flex
          items-center
          justify-between
          px-5
          py-4
          border-b
          border-[#D5E6D8]
          bg-[#FFFFFF]
        "
      >

        {/* ================= WINDOW CONTROLS ================= */}

        <div className="flex gap-2">

          <div className="w-3 h-3 rounded-full bg-red-400" />

          <div className="w-3 h-3 rounded-full bg-yellow-400" />

          <div className="w-3 h-3 rounded-full bg-[#16A34A]" />

        </div>


        {/* ================= FILE NAME ================= */}

        <h2
          className="
            text-[#0F172A]
            text-[20px]
            font-semibold
          "
        >
          hello.py
        </h2>


        {/* ================= COPY ICON ================= */}

        <FaRegCopy
          className="
            text-[#6B7280]
            hover:text-[#0B6B2B]
            cursor-pointer
            transition-colors
            duration-300
          "
          size={20}
        />

      </div>


      {/* =================================================
          CODE
      ================================================= */}

      <div
        className="
          px-6
          py-7
          font-mono
          text-[18px]
          leading-10
          bg-[#FFFFFF]
        "
      >

        {/* ================= LINE 1 ================= */}

        <div>

          <span className="text-[#9CA3AF] mr-5">
            1
          </span>

          {/* Code Comment */}

          <span className="text-[#15803D]">
            # Simple Program
          </span>

        </div>


        {/* ================= LINE 2 ================= */}

        <div>

          <span className="text-[#9CA3AF] mr-5">
            2
          </span>

          {/* Keyword */}

          <span className="text-[#2563EB]">
            print
          </span>

          {/* Parenthesis */}

          <span className="text-[#0F172A]">
            (
          </span>

          {/* String */}

          <span className="text-[#EA580C]">
            "Hello, GreenCode!"
          </span>

          {/* Parenthesis */}

          <span className="text-[#0F172A]">
            )
          </span>

        </div>


        {/* ================= LINE 3 ================= */}

        <div>

          <span className="text-[#9CA3AF] mr-5">
            3
          </span>

        </div>

      </div>

    </div>
  );
}
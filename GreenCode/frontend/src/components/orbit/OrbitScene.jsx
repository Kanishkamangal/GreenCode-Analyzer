import OrbitRing from "./OrbitRing";
import MetricBubble from "./MetricBubble";

import CodeEditor from "./CodeEditor";

export default function OrbitScene() {
  return (
    <div
      className="
        relative
        w-[680px]
        h-[680px]
        flex
        items-center
        justify-center
      "
    >

      {/* =================================================
          BACKGROUND GLOW
      ================================================= */}

      <div
        className="
          absolute
          w-[680px]
          h-[680px]
          rounded-full
          bg-[#EAF6EC]
          blur-3xl
          opacity-80
        "
      />


      {/* =================================================
          SVG ORBIT RINGS
      ================================================= */}

      <OrbitRing />


      {/* =================================================
          ROTATING METRIC LAYER
      ================================================= */}

      <div
        className="
          absolute
          w-[480px]
          h-[480px]
          animate-[spin_18s_linear_infinite]
        "
      >

        {/* ================= TOP ================= */}

        <MetricBubble
          icon="cpu"
          title="CPU Usage"
          value="45"
          unit="%"
          className="
            absolute
            left-1/2
            -translate-x-1/2
            -top-16
            animate-[spin_18s_linear_infinite_reverse]
          "
        />


        {/* ================= RIGHT ================= */}

        <MetricBubble
          icon="memory"
          title="Memory"
          value="64"
          unit="MB"
          className="
            absolute
            top-1/2
            -translate-y-1/2
            -right-16
            animate-[spin_18s_linear_infinite_reverse]
          "
        />


        {/* ================= BOTTOM ================= */}

        <MetricBubble
          icon="time"
          title="Execution"
          value="1.24"
          unit="s"
          className="
            absolute
            left-1/2
            -translate-x-1/2
            -bottom-16
            animate-[spin_18s_linear_infinite_reverse]
          "
        />


        {/* ================= LEFT ================= */}

        <MetricBubble
          icon="energy"
          title="Energy"
          value="12"
          unit="Wh"
          className="
            absolute
            top-1/2
            -translate-y-1/2
            -left-16
            animate-[spin_18s_linear_infinite_reverse]
          "
        />

      </div>


      {/* =================================================
          FIXED CODE EDITOR
      ================================================= */}

      <div
        className="
          absolute
          z-20
        "
      >
        <CodeEditor />
      </div>

    </div>
  );
}
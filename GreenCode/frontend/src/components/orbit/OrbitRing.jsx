export default function OrbitRing() {
  return (
    <svg
      width="700"
      height="700"
      viewBox="0 0 700 700"
      className="absolute"
      fill="none"
    >
      <defs>

        {/* =================================================
            SOFT GREEN GLOW
        ================================================= */}

        <filter
          id="ringGlow"
          x="-50%"
          y="-50%"
          width="200%"
          height="200%"
        >
          <feGaussianBlur
            stdDeviation="2.5"
            result="blur"
          />

          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>


        {/* =================================================
            GREEN GRADIENT
        ================================================= */}

        <linearGradient
          id="ringGradient"
          x1="0%"
          y1="0%"
          x2="100%"
          y2="100%"
        >
          <stop
            offset="0%"
            stopColor="#16A34A"
          />

          <stop
            offset="100%"
            stopColor="#0B6B2B"
          />
        </linearGradient>

      </defs>


      {/* =================================================
          OUTER DOTTED RING
      ================================================= */}

      <circle
        cx="350"
        cy="350"
        r="300"
        stroke="#0B6B2B"
        strokeOpacity="0.08"
        strokeWidth="1.5"
        strokeDasharray="4 10"
      />


      {/* =================================================
          MIDDLE DOTTED RING
      ================================================= */}

      <circle
        cx="350"
        cy="350"
        r="270"
        stroke="#0B6B2B"
        strokeOpacity="0.12"
        strokeWidth="1.5"
        strokeDasharray="4 10"
      />


      {/* =================================================
          MAIN ORBIT
      ================================================= */}

      <circle
        cx="350"
        cy="350"
        r="240"
        stroke="url(#ringGradient)"
        strokeWidth="3"
        fill="transparent"
        filter="url(#ringGlow)"
      />


      {/* =================================================
          INNER RING
      ================================================= */}

      <circle
        cx="350"
        cy="350"
        r="210"
        stroke="#0B6B2B"
        strokeOpacity="0.18"
        strokeWidth="1.5"
        strokeDasharray="6 10"
      />

    </svg>
  );
}
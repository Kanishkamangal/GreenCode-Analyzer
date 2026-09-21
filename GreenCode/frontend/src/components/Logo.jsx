export default function Logo() {
  return (
    <div className="flex items-center gap-4">

      {/* =================================================
          LOGO ICON
      ================================================= */}

      <svg
        width="64"
        height="64"
        viewBox="0 0 80 80"
        fill="none"
      >
        <defs>

          {/* Natural Green Gradient */}

          <radialGradient
            id="greenGlow"
            cx="50%"
            cy="50%"
            r="70%"
          >
            <stop
              offset="0%"
              stopColor="#16A34A"
            />

            <stop
              offset="100%"
              stopColor="#0B6B2B"
            />
          </radialGradient>


          {/* Soft Green Glow */}

          <filter id="glow">
            <feGaussianBlur
              stdDeviation="2"
              result="blur"
            />

            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

        </defs>


        {/* =================================================
            OUTER CIRCLE
        ================================================= */}

        <circle
          cx="40"
          cy="40"
          r="34"
          stroke="url(#greenGlow)"
          strokeWidth="3"
          fill="transparent"
          filter="url(#glow)"
        />


        {/* =================================================
            LEAF
        ================================================= */}

        <path
          d="
            M31 23
            C42 20 50 25 52 34
            C45 36 36 33 31 23
          "
          fill="#16A34A"
        />


        {/* =================================================
            STEM
        ================================================= */}

        <path
          d="M40 28 L34 41"
          stroke="#0B6B2B"
          strokeWidth="2"
        />


        {/* =================================================
            LEFT CODE BRACKET
        ================================================= */}

        <path
          d="M28 50 L21 44 L28 38"
          stroke="#0B6B2B"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />


        {/* =================================================
            RIGHT CODE BRACKET
        ================================================= */}

        <path
          d="M52 50 L59 44 L52 38"
          stroke="#0B6B2B"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />


        {/* =================================================
            CODE SLASH
        ================================================= */}

        <path
          d="M45 33 L35 55"
          stroke="#0B6B2B"
          strokeWidth="3"
          strokeLinecap="round"
        />

      </svg>


      {/* =================================================
          BRAND TEXT
      ================================================= */}

      <div>

        <h1 className="leading-none font-extrabold text-[46px]">

          <span className="text-[#0B6B2B]">
            Green
          </span>

          <span className="text-[#0F172A]">
            Code
          </span>

        </h1>


        <p
          className="
            tracking-[12px]
            text-[#6B7280]
            text-sm
            mt-2
          "
        >
          ANALYZER
        </p>

      </div>

    </div>
  );
}
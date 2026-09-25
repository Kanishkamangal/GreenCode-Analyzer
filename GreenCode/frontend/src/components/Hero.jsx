import { useEffect, useRef, useState } from "react";
import OrbitScene from "./orbit/OrbitScene";
import { Link } from "react-router-dom";

export default function Hero() {
  const [typed, setTyped] = useState("");
  const code = "benchmark.run(code)";

  const heroRef = useRef(null);

  // Typing sequence for the hero visualization.
  useEffect(() => {
    let i = 0;
    const timer = setInterval(() => {
      i += 1;
      setTyped(code.slice(0, i));
      if (i >= code.length) clearInterval(timer);
    }, 48);

    return () => {
      clearInterval(timer);
    };
  }, []);

  // Subtle pointer parallax for the orbit visualization.
  useEffect(() => {
    const node = heroRef.current;
    if (!node || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const handleMove = (event) => {
      const rect = node.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      node.style.setProperty("--hero-x", `${x * 14}px`);
      node.style.setProperty("--hero-y", `${y * 10}px`);
    };

    const reset = () => {
      node.style.setProperty("--hero-x", "0px");
      node.style.setProperty("--hero-y", "0px");
    };

    node.addEventListener("pointermove", handleMove);
    node.addEventListener("pointerleave", reset);

    return () => {
      node.removeEventListener("pointermove", handleMove);
      node.removeEventListener("pointerleave", reset);
    };
  }, []);

  return (
    <section
      id="home"
      ref={heroRef}
      className="
        relative isolate overflow-hidden
        max-w-[1700px] mx-auto
        min-h-[calc(100vh-96px)]
        flex items-center justify-between
        px-6 sm:px-10
        py-16 lg:py-10
      "
    >
      {/* Technical background */}
      <div className="pointer-events-none absolute inset-0 -z-20 opacity-70 [background-image:linear-gradient(rgba(15,23,42,0.045)_1px,transparent_1px),linear-gradient(90deg,rgba(15,23,42,0.045)_1px,transparent_1px)] [background-size:42px_42px]" />
      <div className="pointer-events-none absolute left-1/2 top-1/2 -z-10 h-[620px] w-[620px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#EAF6EC]/80 blur-3xl" />
      <div className="pointer-events-none absolute left-0 top-1/2 -z-10 h-px w-full bg-gradient-to-r from-transparent via-[#16A34A]/20 to-transparent" />

      {/* LEFT — cinematic entrance */}
      <div className="w-full lg:w-[46%] max-w-2xl">
        <div className="gc-hero-reveal gc-hero-delay-1">
          <p className="mb-5 flex items-center gap-3 text-xs font-bold uppercase tracking-[0.28em] text-[#0B6B2B]">
            <span className="h-2 w-2 rounded-full bg-[#16A34A] shadow-[0_0_0_5px_rgba(22,163,74,0.10)]" />
            Performance analysis engine
          </p>
        </div>

        <h1 className="gc-hero-reveal gc-hero-delay-2 text-[clamp(48px,5vw,68px)] font-black leading-[1.03] tracking-[-0.035em] text-[#0F172A]">
          Measure. Compare.
          <br />
          <span className="text-[#0B6B2B]">Optimize.</span>
        </h1>

        <div className="gc-hero-line gc-hero-delay-3" />

        <p className="gc-hero-reveal gc-hero-delay-4 max-w-xl text-[18px] sm:text-[21px] leading-8 sm:leading-9 text-[#526174]">
          GreenCode Analyzer helps developers benchmark programs across
          multiple programming languages by analysing execution time, CPU
          utilisation, memory usage and estimated energy consumption through
          an intuitive visual dashboard.
        </p>

        <div className="gc-hero-reveal gc-hero-delay-5 mt-10 flex flex-wrap items-center gap-5">
          <Link
            to="/dashboard"
            className="
              group inline-flex items-center justify-center
              rounded-xl bg-[#0B6B2B] px-9 py-4
              text-lg font-bold text-white
              shadow-[0_12px_30px_rgba(11,107,43,0.16)]
              transition-all duration-300
              hover:-translate-y-1 hover:bg-[#16A34A]
              hover:shadow-[0_18px_38px_rgba(11,107,43,0.22)]
            "
          >
            Get Started
            <span className="ml-3 transition-transform duration-300 group-hover:translate-x-1">→</span>
          </Link>

          <span className="text-xs font-semibold uppercase tracking-[0.18em] text-[#94A3B8]">
            Code → Measure → Improve
          </span>
        </div>
      </div>

      {/* RIGHT — moving benchmark visual */}
      <div
        className="
          relative hidden lg:flex w-[54%]
          justify-center -translate-x-8
          transition-transform duration-300
        "
        style={{
          transform: "translate3d(var(--hero-x), var(--hero-y), 0)",
        }}
      >
        <div className="absolute h-[540px] w-[540px] rounded-full bg-[#EAF6EC] blur-3xl" />

        <div className="relative flex min-h-[600px] w-full items-center justify-center">
          {/* Orbit */}
          <div className="gc-orbit-entrance relative z-10">
            <OrbitScene />
          </div>

        </div>
      </div>

      <style>{`
        @keyframes gcHeroRise {
          0% { opacity: 0; transform: translate3d(0, 34px, 0); filter: blur(9px); }
          100% { opacity: 1; transform: translate3d(0, 0, 0); filter: blur(0); }
        }

        @keyframes gcHeroLine {
          0% { transform: scaleX(0); transform-origin: left; opacity: 0; }
          100% { transform: scaleX(1); transform-origin: left; opacity: 1; }
        }

        @keyframes gcOrbitIn {
          0% { opacity: 0; transform: scale(.82) rotate(-8deg); filter: blur(12px); }
          100% { opacity: 1; transform: scale(1) rotate(0); filter: blur(0); }
        }

        .gc-hero-reveal {
          opacity: 0;
          animation: gcHeroRise .85s cubic-bezier(.22,1,.36,1) forwards;
        }

        .gc-hero-delay-1 { animation-delay: .05s; }
        .gc-hero-delay-2 { animation-delay: .18s; }
        .gc-hero-delay-3 { animation-delay: .38s; }
        .gc-hero-delay-4 { animation-delay: .48s; }
        .gc-hero-delay-5 { animation-delay: .65s; }

        .gc-hero-line {
          width: 112px;
          height: 4px;
          margin: 28px 0 34px;
          border-radius: 999px;
          background: #16A34A;
          opacity: 0;
          animation: gcHeroLine .7s .38s cubic-bezier(.22,1,.36,1) forwards;
        }

        .gc-orbit-entrance {
          opacity: 0;
          animation: gcOrbitIn 1.15s .25s cubic-bezier(.22,1,.36,1) forwards;
        }

        @media (prefers-reduced-motion: reduce) {
          .gc-hero-reveal,
          .gc-hero-line,
          .gc-orbit-entrance {
            animation: none !important;
            opacity: 1 !important;
            transform: none !important;
            filter: none !important;
          }
        }
      `}</style>
    </section>
  );
}
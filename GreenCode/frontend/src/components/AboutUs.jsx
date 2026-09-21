import React from "react";

const AboutUs = () => {
  const languages = [
    "Python",
    "C",
    "C++",
    "Java",
    "JavaScript",
    "Go",
    "Rust",
    "C#",
    "Kotlin",
    "PHP",
  ];

  const languageIcons = {
    Python: "https://cdn.simpleicons.org/python/3776AB",
    C: "https://cdn.simpleicons.org/c/A8B9CC",
    "C++": "https://cdn.simpleicons.org/cplusplus/00599C",
    Java: "https://cdn.simpleicons.org/openjdk/ED8B00",
    JavaScript: "https://cdn.simpleicons.org/javascript/F7DF1E",
    Go: "https://cdn.simpleicons.org/go/00ADD8",
    Rust: "https://cdn.simpleicons.org/rust/000000",
    "C#": "https://cdn.simpleicons.org/csharp/512BD4",
    Kotlin: "https://cdn.simpleicons.org/kotlin/7F52FF",
    PHP: "https://cdn.simpleicons.org/php/777BB4",
  };

  const metrics = [
    {
      number: "01",
      title: "Execution Time",
      text: "Time taken by a program to complete its task.",
    },
    {
      number: "02",
      title: "CPU Usage",
      text: "Processing power consumed during execution.",
    },
    {
      number: "03",
      title: "Memory Usage",
      text: "Memory required while the program runs.",
    },
    {
      number: "04",
      title: "Energy Consumption",
      text: "Estimated energy consumed during execution.",
    },
  ];

  const audiences = [
    {
      title: "Developers",
      text: "Optimize and write more efficient code.",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" className="w-6 h-6">
          <path strokeLinecap="round" strokeLinejoin="round" d="m8 9-3 3 3 3" />
          <path strokeLinecap="round" strokeLinejoin="round" d="m16 9 3 3-3 3" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M14 5 10 19" />
        </svg>
      ),
    },
    {
      title: "Students",
      text: "Learn and compare programming languages.",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" className="w-6 h-6">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 10.5 12 5l9 5.5-9 5-9-5Z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M6 12.5V16c0 1.5 2.7 3 6 3s6-1.5 6-3v-3.5" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 10.5V16" />
        </svg>
      ),
    },
    {
      title: "Researchers",
      text: "Analyze performance and resource patterns.",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" className="w-6 h-6">
          <circle cx="11" cy="11" r="6.5" />
          <path strokeLinecap="round" d="m16 16 4.5 4.5" />
          <path strokeLinecap="round" d="M8.5 11h5" />
          <path strokeLinecap="round" d="M11 8.5v5" />
        </svg>
      ),
    },
    {
      title: "Organizations",
      text: "Make informed technology decisions.",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" className="w-6 h-6">
          <path strokeLinecap="round" strokeLinejoin="round" d="M4 20V9l8-5 8 5v11" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M8 20v-5h8v5" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01" />
        </svg>
      ),
    },
  ];

  const approach = [
    {
      number: "01",
      title: "Measure",
      text: "Capture execution time, CPU, memory and energy.",
    },
    {
      number: "02",
      title: "Compare",
      text: "Evaluate equivalent programs across languages.",
    },
    {
      number: "03",
      title: "Optimize",
      text: "Choose smarter approaches for efficient software.",
    },
  ];

  return (
    <section
      id="about"
      className="relative overflow-hidden bg-[#F9FAFA] text-[#0F172A] py-24 md:py-28"
    >
      {/* =====================================================
          BACKGROUND EFFECTS
      ===================================================== */}

      <div className="absolute top-[-180px] left-1/2 -translate-x-1/2 w-[700px] h-[500px] bg-[#EAF6EC] blur-[140px] rounded-full pointer-events-none" />

      <div className="absolute bottom-[-250px] right-[-150px] w-[500px] h-[500px] bg-[#DFF0E1] blur-[130px] rounded-full pointer-events-none" />

      <div className="absolute inset-0 opacity-[0.45] pointer-events-none [background-image:linear-gradient(rgba(11,107,43,0.035)_1px,transparent_1px),linear-gradient(90deg,rgba(11,107,43,0.035)_1px,transparent_1px)] [background-size:70px_70px]" />

      {/* =====================================================
          MAIN CONTAINER
      ===================================================== */}

      <div className="relative max-w-6xl mx-auto px-6">
        {/* =====================================================
            ABOUT INTRO
        ===================================================== */}

        <div className="relative min-h-[420px] flex items-center">
          {/* LEFT CONTENT */}
          <div className="relative z-10 max-w-3xl">
            <div className="inline-flex items-center gap-3 px-4 py-2 rounded-full border border-[#D5E6D8] bg-[#EAF6EC] text-xs tracking-[0.2em] text-[#526174] uppercase mb-7">
              <span className="w-2 h-2 rounded-full bg-[#16A34A] shadow-[0_0_10px_rgba(22,163,74,0.3)] animate-pulse" />
              Live Analysis
            </div>

            <h2 className="text-5xl sm:text-6xl md:text-7xl font-semibold tracking-[-0.04em] leading-[0.95] text-[#0F172A]">
              About{" "}
              <span className="text-[#0B6B2B] drop-shadow-[0_0_15px_rgba(11,107,43,0.10)]">
                GreenCode
              </span>
            </h2>

            <div className="mt-7 w-20 h-[3px] rounded-full bg-[#16A34A]" />

            <div className="mt-8">
              <p className="text-2xl md:text-3xl font-medium text-[#0F172A]">
                Write smarter.
                <span className="text-[#0B6B2B]"> Run greener.</span>
              </p>
            </div>

            <p className="mt-5 max-w-2xl text-[#526174] text-base md:text-lg leading-8">
              GreenCode Analyzer benchmarks and compares programs across 10 programming languages,
              helping developers understand performance, resource usage and energy efficiency.
            </p>
          </div>

          {/* =================================================
              FLOATING METRICS
          ================================================= */}

          {/* ENERGY */}
          <div className="hidden lg:block absolute right-5 top-8 w-44 p-5 rounded-2xl border border-[#D5E6D8] bg-[#FFFFFF] shadow-[0_15px_40px_rgba(15,23,42,0.07)] animate-[floatOne_5s_ease-in-out_infinite]">
            <div className="flex items-center justify-between">
              <span className="text-xs text-[#6B7280] uppercase tracking-widest">Energy</span>
              <span className="text-[#0B6B2B] text-xs font-medium">↓ 18%</span>
            </div>
            <p className="mt-3 text-2xl font-semibold text-[#0F172A]">
              0.42<span className="text-sm text-[#6B7280] ml-1">J</span>
            </p>
            <div className="mt-4 h-1 rounded-full bg-[#EAF6EC] overflow-hidden">
              <div className="h-full w-[38%] bg-[#16A34A] rounded-full" />
            </div>
          </div>

          {/* CPU */}
          <div className="hidden lg:block absolute right-[-35px] top-[210px] w-44 p-5 rounded-2xl border border-[#D5E6D8] bg-[#FFFFFF] shadow-[0_15px_40px_rgba(15,23,42,0.07)] animate-[floatTwo_6s_ease-in-out_infinite]">
            <span className="text-xs text-[#6B7280] uppercase tracking-widest">CPU Usage</span>
            <p className="mt-3 text-2xl font-semibold text-[#0F172A]">
              12.4<span className="text-sm text-[#6B7280] ml-1">%</span>
            </p>
            <div className="mt-4 flex gap-1 items-end h-8">
              {[35, 55, 40, 70, 48, 65, 52, 80].map((height, index) => (
                <div
                  key={index}
                  className="flex-1 bg-[#16A34A] rounded-sm animate-pulse"
                  style={{
                    height: `${height}%`,
                    animationDelay: `${index * 120}ms`,
                  }}
                />
              ))}
            </div>
          </div>

          {/* MEMORY */}
          <div className="hidden lg:block absolute right-20 bottom-5 w-44 p-5 rounded-2xl border border-[#D5E6D8] bg-[#FFFFFF] shadow-[0_15px_40px_rgba(15,23,42,0.07)] animate-[floatThree_5.5s_ease-in-out_infinite]">
            <span className="text-xs text-[#6B7280] uppercase tracking-widest">Memory</span>
            <p className="mt-3 text-2xl font-semibold text-[#0F172A]">
              38.7<span className="text-sm text-[#6B7280] ml-1">MB</span>
            </p>
            <p className="mt-2 text-xs text-[#0B6B2B]">Resource monitored</p>
          </div>

          {/* EXECUTION TIME */}
          <div className="hidden lg:block absolute right-[235px] bottom-[55px] w-44 p-5 rounded-2xl border border-[#D5E6D8] bg-[#FFFFFF] shadow-[0_15px_40px_rgba(15,23,42,0.07)] animate-[floatFour_6.5s_ease-in-out_infinite]">
            <div className="flex items-center justify-between">
              <span className="text-xs text-[#6B7280] uppercase tracking-widest">Time</span>
              <span className="text-[#0B6B2B] text-xs font-medium">Fast</span>
            </div>
            <p className="mt-3 text-2xl font-semibold text-[#0F172A]">
              532<span className="text-sm text-[#6B7280] ml-1">ms</span>
            </p>
            <div className="mt-4 h-1 rounded-full bg-[#EAF6EC] overflow-hidden">
              <div className="h-full w-[62%] bg-[#16A34A] rounded-full" />
            </div>
          </div>
        </div>

        {/* =====================================================
            10 LANGUAGES — TREE ORBIT
        ===================================================== */}

        <div className="mt-20">
          <div className="text-center">
            <p className="text-xs tracking-[0.3em] text-[#0B6B2B] uppercase">
              Run Benchmark
            </p>

            <h3 className="mt-2 text-2xl md:text-3xl font-medium text-[#0F172A]">
              10 Languages. One Comparison.
            </h3>

            <p className="mt-3 max-w-xl mx-auto text-sm md:text-base text-[#6B7280]">
              Run equivalent programs across multiple languages and compare their performance and efficiency.
            </p>
          </div>

          {/* =================================================
              TREE + LANGUAGE ORBIT
          ================================================= */}

          <div className="gc-benchmark-scene relative mx-auto mt-4 h-[560px] w-full max-w-[1000px] overflow-hidden">
            {/* Atmospheric glow */}
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-[500px] w-[500px] rounded-full bg-[#DDF5E2] opacity-70 blur-[100px] pointer-events-none" />

            {/* Orbit rings */}
            <div className="gc-orbit-ring gc-orbit-ring-outer" />
            <div className="gc-orbit-ring gc-orbit-ring-middle" />
            <div className="gc-orbit-ring gc-orbit-ring-inner" />

            {/* Orbit dots */}
            <span className="gc-orbit-dot gc-orbit-dot-1" />
            <span className="gc-orbit-dot gc-orbit-dot-2" />
            <span className="gc-orbit-dot gc-orbit-dot-3" />
            <span className="gc-orbit-dot gc-orbit-dot-4" />
            <span className="gc-orbit-dot gc-orbit-dot-5" />
            <span className="gc-orbit-dot gc-orbit-dot-6" />
            <span className="gc-orbit-dot gc-orbit-dot-7" />
            <span className="gc-orbit-dot gc-orbit-dot-8" />

            {/* =================================================
                LANGUAGE ORBIT
            ================================================= */}

            <div className="gc-language-orbit">
              {languages.map((language, index) => (
                <div
                  key={language}
                  className="gc-language-node"
                  style={{
                    "--delay": `${-(32 / languages.length) * index}s`,
                  }}
                >
                  <div className="gc-language-card">
                    <div className="gc-language-icon">
                      <img src={languageIcons[language]} alt={language} />
                    </div>
                    <span>{language}</span>
                  </div>
                </div>
              ))}
            </div>

            {/* =================================================
                PROFESSIONAL TREE
            ================================================= */}

            <div className="gc-tree-wrapper">
              <div className="gc-tree-aura" />

              <img
                src="/greencode-tree.png"
                alt="GreenCode ecosystem tree"
                className="gc-professional-tree"
              />
            </div>
          </div>
        </div>

        {/* =====================================================
            WHO IS IT FOR
        ===================================================== */}

        <div className="mt-20">
          <div className="text-center">
            <p className="text-xs tracking-[0.3em] text-[#0B6B2B] uppercase">Built For</p>

            <h3 className="mt-2 text-2xl md:text-3xl font-medium text-[#0F172A]">
              Who Is It For?
            </h3>

            <div className="w-12 h-[2px] bg-[#16A34A] mx-auto mt-4" />
          </div>

          <div className="mt-8 grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {audiences.map((item) => (
              <div
                key={item.title}
                className="group text-center p-7 rounded-2xl border border-[#D5E6D8] bg-[#FFFFFF] shadow-sm transition-all duration-500 hover:-translate-y-2 hover:border-[#16A34A] hover:shadow-[0_15px_35px_rgba(11,107,43,0.08)]"
              >
                <div className="mx-auto w-12 h-12 rounded-xl border border-[#D5E6D8] bg-[#EAF6EC] flex items-center justify-center text-[#0B6B2B] group-hover:bg-[#DFF0E1] group-hover:border-[#16A34A] transition">
                  {item.icon}
                </div>

                <h4 className="mt-5 text-lg font-medium text-[#0F172A]">{item.title}</h4>

                <p className="mt-3 text-sm text-[#6B7280] leading-6">{item.text}</p>
              </div>
            ))}
          </div>
        </div>

        {/* =====================================================
            MEASURE → COMPARE → OPTIMIZE
        ===================================================== */}

        <div className="mt-20">
          <div className="text-center mb-10">
            <p className="text-xs tracking-[0.3em] text-[#0B6B2B] uppercase">Our Approach</p>

            <h3 className="mt-3 text-2xl md:text-3xl font-medium text-[#0F172A]">
              From code to insight.
            </h3>
          </div>

          <div className="relative">
            {/* CONNECTING LINE */}
            <div className="hidden md:block absolute top-7 left-[16%] right-[16%] h-px bg-gradient-to-r from-transparent via-[#16A34A]/30 to-transparent" />

            <div className="grid md:grid-cols-3 gap-8">
              {approach.map((item) => (
                <div key={item.number} className="relative text-center">
                  <div className="relative z-10 mx-auto w-14 h-14 rounded-full border border-[#D5E6D8] bg-[#FFFFFF] flex items-center justify-center text-[#0B6B2B] font-mono text-sm shadow-sm">
                    {item.number}
                  </div>

                  <h4 className="mt-5 text-xl font-medium text-[#0F172A]">{item.title}</h4>

                  <p className="mt-3 max-w-xs mx-auto text-sm text-[#6B7280] leading-6">
                    {item.text}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* =====================================================
            MISSION
        ===================================================== */}

        <div className="relative mt-20 rounded-3xl border border-[#D5E6D8] bg-[#FFFFFF] px-8 md:px-20 py-12 md:py-14 text-center overflow-hidden shadow-[0_15px_40px_rgba(15,23,42,0.06)]">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-72 h-32 bg-[#EAF6EC] blur-[80px] pointer-events-none" />

          <div className="relative">
            <p className="text-[#0B6B2B] text-sm tracking-[0.3em] uppercase font-semibold">
              Our Mission
            </p>

            <h3 className="mt-5 text-2xl md:text-4xl font-medium leading-tight text-[#0F172A]">
              Make software performance
              <br className="hidden md:block" />
              measurable, comparable, and greener.
            </h3>

            <p className="mt-5 max-w-2xl mx-auto text-[#526174] leading-7">
              Better software isn't only about what it does — it's also about the resources it takes to do it.
            </p>
          </div>
        </div>

        {/* =====================================================
            FINAL TAGLINE
        ===================================================== */}

        <div className="mt-10 text-center">
          <div className="flex flex-wrap items-center justify-center gap-4 md:gap-7 text-xs md:text-sm tracking-[0.3em] text-[#6B7280]">
            <span className="hover:text-[#0B6B2B] transition">MEASURE</span>
            <span className="text-[#16A34A]">•</span>
            <span className="hover:text-[#0B6B2B] transition">COMPARE</span>
            <span className="text-[#16A34A]">•</span>
            <span className="hover:text-[#0B6B2B] transition">OPTIMIZE</span>
          </div>

          <p className="mt-4 text-sm text-[#6B7280] tracking-[0.2em]">
            For a <span className="text-[#0B6B2B] font-semibold">greener</span> future.
          </p>
        </div>
      </div>

      {/* =====================================================
          ANIMATION KEYFRAMES
      ===================================================== */}

      <style>{`
        /* =====================================================
           FLOATING METRICS
        ===================================================== */

        @keyframes floatOne {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-14px); }
        }

        @keyframes floatTwo {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(12px); }
        }

        @keyframes floatThree {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
        }

        @keyframes floatFour {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(14px); }
        }

        /* =====================================================
           ORBIT RINGS
        ===================================================== */

        .gc-orbit-ring {
          position: absolute;
          left: 50%;
          top: 51%;
          transform: translate(-50%, -50%);
          border-radius: 50%;
          pointer-events: none;
          border: 1.5px dashed rgba(22,163,74,.20);
          z-index: 10;
        }

        .gc-orbit-ring-outer {
          width: 820px;
          height: 360px;
          animation: none;
        }

        .gc-orbit-ring-middle {
          width: 700px;
          height: 300px;
          border-color: rgba(22,163,74,.15);
          animation: none;
        }

        .gc-orbit-ring-inner {
          width: 570px;
          height: 240px;
          border-color: rgba(22,163,74,.10);
          animation: none;
        }

        /* =====================================================
           ORBIT DOTS
        ===================================================== */

        .gc-orbit-dot {
          position: absolute;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #55C878;
          box-shadow: 0 0 12px rgba(85,200,120,.45);
          animation: gcDotPulse 2.5s ease-in-out infinite;
          z-index: 15;
        }

        .gc-orbit-dot-1 { left: 17%; top: 48%; }
        .gc-orbit-dot-2 { left: 26%; top: 27%; }
        .gc-orbit-dot-3 { left: 39%; top: 16%; }
        .gc-orbit-dot-4 { left: 62%; top: 16%; }
        .gc-orbit-dot-5 { right: 20%; top: 34%; }
        .gc-orbit-dot-6 { right: 16%; top: 61%; }
        .gc-orbit-dot-7 { left: 39%; bottom: 17%; }
        .gc-orbit-dot-8 { left: 61%; bottom: 16%; }

        @keyframes gcDotPulse {
          0%, 100% {
            transform: scale(1);
            opacity: .65;
          }
          50% {
            transform: scale(1.5);
            opacity: 1;
          }
        }

        /* =====================================================
           LANGUAGE ORBIT
        ===================================================== */

        .gc-language-orbit {
          position: absolute;
          left: 50%;
          top: 51%;
          width: 820px;
          height: 360px;
          transform: translate(-50%, -50%);
          /* The oval itself is completely fixed. Only the language cards move. */
          animation: none;
          z-index: 30;
          pointer-events: none;
        }

        .gc-language-node {
          position: absolute;
          left: 50%;
          top: 50%;
          width: 78px;
          height: 86px;
          margin-left: -39px;
          margin-top: -43px;
          z-index: 30;
          offset-path: ellipse(410px 180px at 0 0);
          offset-distance: 0%;
          offset-rotate: 0deg;
          animation: gcLanguageEllipseOrbit 32s linear infinite;
          animation-delay: var(--delay);
          pointer-events: auto;
        }

        .gc-language-card {
          width: 78px;
          min-height: 86px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 4px;
          transform: translate(-50%, -50%);
          border: 1px solid rgba(22,163,74,.12);
          border-radius: 50%;
          background: radial-gradient(circle at 35% 25%, rgba(255,255,255,.99), rgba(248,253,249,.94));
          box-shadow:
            0 10px 28px rgba(15,23,42,.075),
            0 0 0 5px rgba(255,255,255,.55);
          backdrop-filter: blur(10px);
          transition: transform .3s ease, box-shadow .3s ease;
        }

        .gc-language-card:hover {
          transform: translate(-50%, -50%) scale(1.12);
          box-shadow:
            0 15px 35px rgba(22,163,74,.15),
            0 0 0 7px rgba(255,255,255,.8);
        }

        .gc-language-icon {
          width: 39px;
          height: 39px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          background: rgba(255,255,255,.92);
        }

        .gc-language-icon img {
          width: 30px;
          height: 30px;
          object-fit: contain;
        }

        .gc-language-card span {
          font-size: 9px;
          font-weight: 700;
          color: #243047;
          white-space: nowrap;
        }

        @keyframes gcLanguageEllipseOrbit {
          from {
            offset-distance: 0%;
          }
          to {
            offset-distance: 100%;
          }
        }

        /* =====================================================
           PROFESSIONAL TREE
        ===================================================== */

        /* =====================================================
          PROFESSIONAL TREE — SUBTLE WIND
        ===================================================== */

        .gc-tree-wrapper {
          position: absolute;

          left: 50%;
          top: 52%;

          width: 500px;

          transform: translate(-50%, -50%);

          z-index: 20;

          pointer-events: none;
        }

        .gc-tree-aura {
          position: absolute;

          left: 50%;
          top: 50%;

          width: 430px;
          height: 430px;

          transform: translate(-50%, -50%);

          border-radius: 50%;

          background:
            radial-gradient(
              circle,
              rgba(120, 220, 120, 0.20) 0%,
              rgba(120, 220, 120, 0.10) 35%,
              rgba(120, 220, 120, 0) 72%
            );

          filter: blur(25px);

          animation: gcTreeAura 6s ease-in-out infinite;
        }

        .gc-professional-tree {
          position: relative;

          display: block;

          width: 500px;
          height: auto;

          object-fit: contain;

          transform-origin: center bottom;

          filter:
            drop-shadow(
              0 20px 30px
              rgba(22, 101, 52, 0.16)
            );

          animation:
            gcProfessionalTreeSway
            6s
            ease-in-out
            infinite;
        }


        /* Gentle natural wind */

        @keyframes gcProfessionalTreeSway {

          0%,
          100% {
            transform:
              rotate(-0.7deg)
              translateX(-1px);
          }

          25% {
            transform:
              rotate(0.25deg)
              translateX(1px);
          }

          50% {
            transform:
              rotate(0.8deg)
              translateX(3px);
          }

          75% {
            transform:
              rotate(0.15deg)
              translateX(1px);
          }

        }


        /* Soft breathing glow */

        @keyframes gcTreeAura {

          0%,
          100% {
            opacity: 0.60;
            transform: translate(-50%, -50%) scale(0.96);
          }

          50% {
            opacity: 0.85;
            transform: translate(-50%, -50%) scale(1.04);
          }

        }

        /* =====================================================
           RESPONSIVE
        ===================================================== */

        @media (max-width: 1100px) {
          .gc-tree-wrapper,
          .gc-professional-tree {
            width: 470px;
          }
        }

        @media (max-width: 900px) {
          .gc-benchmark-scene {
            transform: scale(.82);
            transform-origin: top center;
            margin-bottom: -90px;
          }
        }

        @media (max-width: 640px) {
          .gc-benchmark-scene {
            transform: scale(.62);
            transform-origin: top center;
            margin-bottom: -190px;
            height: 560px;
          }

          .gc-tree-wrapper,
          .gc-professional-tree {
            width: 500px;
          }

          .gc-language-card {
            width: 70px;
            min-height: 78px;
          }

          .gc-language-icon {
            width: 34px;
            height: 34px;
          }

          .gc-language-icon img {
            width: 27px;
            height: 27px;
          }
        }

        /* =====================================================
           REDUCED MOTION
        ===================================================== */

        @media (prefers-reduced-motion: reduce) {
          .gc-language-node,
          .gc-professional-tree,
          .gc-tree-aura,
          .gc-orbit-dot,
          .gc-orbit-ring {
            animation: none !important;
          }
        }
      `}</style>
    </section>
  );
};

export default AboutUs;

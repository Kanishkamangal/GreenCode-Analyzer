import React, { useState } from "react";
import { Link } from "react-router-dom";

export default function Compare() {

  const [benchmark, setBenchmark] = useState("Hello World");

  const [selectedLanguages, setSelectedLanguages] = useState([
    "C++",
    "C",
    "Java",
    "Python",
  ]);

  const [isComparing, setIsComparing] = useState(false);
  const [showResults, setShowResults] = useState(false);


  /* =========================================================
      LANGUAGE DATA
  ========================================================= */

  const languages = [
    {
      name: "C",
      short: "C",
      description: "Low-level & efficient",
    },
    {
      name: "C++",
      short: "C++",
      description: "High performance",
    },
    {
      name: "Java",
      short: "Java",
      description: "Managed runtime",
    },
    {
      name: "Python",
      short: "Py",
      description: "High-level & flexible",
    },
    {
      name: "JavaScript",
      short: "JS",
      description: "Web & runtime",
    },
    {
      name: "Go",
      short: "Go",
      description: "Fast & lightweight",
    },
    {
      name: "Rust",
      short: "Rs",
      description: "Memory safe",
    },
    {
      name: "C#",
      short: "C#",
      description: "Managed & powerful",
    },
    {
      name: "Kotlin",
      short: "Kt",
      description: "Modern JVM",
    },
    {
      name: "PHP",
      short: "PHP",
      description: "Web scripting",
    },
  ];


  /* =========================================================
      DEMO RESULTS
  ========================================================= */

  const results = [
    {
      language: "C++",
      time: 0.31,
      cpu: 8.5,
      memory: 14.2,
      energy: 0.19,
      score: 94,
    },

    {
      language: "C",
      time: 0.32,
      cpu: 8.2,
      memory: 12.1,
      energy: 0.18,
      score: 92,
    },

    {
      language: "Rust",
      time: 0.34,
      cpu: 9.1,
      memory: 13.8,
      energy: 0.21,
      score: 89,
    },

    {
      language: "Java",
      time: 0.51,
      cpu: 14.2,
      memory: 38.4,
      energy: 0.42,
      score: 76,
    },

    {
      language: "Python",
      time: 1.84,
      cpu: 21.5,
      memory: 42.1,
      energy: 0.63,
      score: 61,
    },
  ];


  /* =========================================================
      TOGGLE LANGUAGE
  ========================================================= */

  const toggleLanguage = (language) => {

    setShowResults(false);

    if (selectedLanguages.includes(language)) {

      setSelectedLanguages(
        selectedLanguages.filter(
          (item) => item !== language
        )
      );

      return;
    }

    if (selectedLanguages.length >= 5) {
      return;
    }

    setSelectedLanguages([
      ...selectedLanguages,
      language,
    ]);
  };


  /* =========================================================
      COMPARE
  ========================================================= */

  const handleCompare = () => {

    if (selectedLanguages.length < 2) {
      return;
    }

    setIsComparing(true);
    setShowResults(false);

    setTimeout(() => {

      setIsComparing(false);
      setShowResults(true);

    }, 1800);
  };


  /* =========================================================
      RESET
  ========================================================= */

  const handleReset = () => {

    setSelectedLanguages([
      "C++",
      "C",
      "Java",
      "Python",
    ]);

    setShowResults(false);
    setIsComparing(false);

  };


  /* =========================================================
      FILTER RESULTS
  ========================================================= */

  const comparisonResults = results.filter(
    (item) =>
      selectedLanguages.includes(item.language)
  );


  const winner =
    comparisonResults.length > 0
      ? [...comparisonResults].sort(
          (a, b) => b.score - a.score
        )[0]
      : null;


  return (

    <main
      className="
        relative
        min-h-screen
        bg-[#05090a]
        text-white
        px-6
        py-12
        md:px-10
        md:py-16
        overflow-hidden
      "
    >

      {/* =====================================================
          BACKGROUND
      ===================================================== */}

      <div
        className="
          absolute
          top-[-180px]
          left-1/2
          -translate-x-1/2
          w-[700px]
          h-[450px]
          bg-[#9DFF00]/[0.045]
          blur-[140px]
          rounded-full
          pointer-events-none
        "
      />

      <div
        className="
          absolute
          bottom-[-250px]
          right-[-150px]
          w-[500px]
          h-[500px]
          bg-[#9DFF00]/[0.025]
          blur-[130px]
          rounded-full
          pointer-events-none
        "
      />

      <div
        className="
          absolute
          inset-0
          opacity-[0.025]
          pointer-events-none
          [background-image:linear-gradient(rgba(255,255,255,0.5)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.5)_1px,transparent_1px)]
          [background-size:70px_70px]
        "
      />


      {/* =====================================================
          CONTENT
      ===================================================== */}

      <div className="relative max-w-7xl mx-auto">


        {/* =====================================================
            TOP BAR
        ===================================================== */}

        <div
          className="
            flex
            items-center
            justify-between
            mb-12
          "
        >

          <Link
            to="/benchmark"
            className="
              text-sm
              text-gray-500
              hover:text-[#9DFF00]
              transition
            "
          >
            ← Back to Benchmark
          </Link>


          <div
            className="
              hidden
              md:flex
              items-center
              gap-3
              text-xs
              text-gray-600
              font-mono
            "
          >

            <span
              className="
                w-2
                h-2
                rounded-full
                bg-[#9DFF00]
                shadow-[0_0_10px_rgba(157,255,0,0.7)]
              "
            />

            GREENCODE ANALYZER

          </div>

        </div>


        {/* =====================================================
            HEADER
        ===================================================== */}

        <div className="mb-10">

          <div
            className="
              inline-flex
              items-center
              gap-3
              px-4
              py-2
              rounded-full
              border
              border-[#9DFF00]/20
              bg-[#9DFF00]/[0.04]
              text-xs
              tracking-[0.2em]
              text-gray-400
              uppercase
            "
          >

            <span
              className="
                w-2
                h-2
                rounded-full
                bg-[#9DFF00]
                shadow-[0_0_12px_rgba(157,255,0,0.8)]
              "
            />

            Comparison Lab

          </div>


          <h1
            className="
              mt-6
              text-4xl
              md:text-6xl
              font-semibold
              tracking-[-0.04em]
            "
          >

            Compare.
            <span
              className="
                text-[#9DFF00]
                ml-3
              "
            >
              Discover.
            </span>

          </h1>


          <p
            className="
              mt-5
              max-w-2xl
              text-gray-500
              text-base
              md:text-lg
              leading-7
            "
          >

            Compare equivalent programs across programming
            languages and discover which implementations
            use resources more efficiently.

          </p>

        </div>


        {/* =====================================================
            BENCHMARK SELECTOR
        ===================================================== */}

        <div
          className="
            rounded-2xl
            border
            border-white/10
            bg-[#090e10]/80
            backdrop-blur-xl
            p-5
            md:p-6
          "
        >

          <div
            className="
              flex
              flex-col
              md:flex-row
              md:items-center
              justify-between
              gap-5
            "
          >

            <div>

              <label
                className="
                  block
                  mb-3
                  text-xs
                  uppercase
                  tracking-[0.2em]
                  text-gray-500
                "
              >
                Benchmark Task
              </label>


              <div className="relative">

                <select
                  value={benchmark}
                  onChange={(e) => {
                    setBenchmark(e.target.value);
                    setShowResults(false);
                  }}
                  className="
                    appearance-none
                    min-w-[280px]
                    rounded-xl
                    border
                    border-white/10
                    bg-[#05090a]
                    px-5
                    py-4
                    pr-12
                    text-white
                    outline-none
                    cursor-pointer
                    focus:border-[#9DFF00]/50
                    transition
                  "
                >

                  <option>Hello World</option>
                  <option>Loop / Iteration</option>
                  <option>Fibonacci</option>
                  <option>Prime Number</option>
                  <option>Array Processing</option>
                  <option>Sorting</option>
                  <option>Matrix Multiplication</option>

                </select>


                <span
                  className="
                    absolute
                    right-5
                    top-1/2
                    -translate-y-1/2
                    text-gray-500
                    pointer-events-none
                  "
                >
                  ↓
                </span>

              </div>

            </div>


            <div className="text-sm text-gray-600">

              Select up to{" "}
              <span className="text-gray-400">
                5 languages
              </span>

            </div>

          </div>

        </div>


        {/* =====================================================
            LANGUAGE SELECTION
        ===================================================== */}

        <section className="mt-10">

          <div
            className="
              flex
              items-end
              justify-between
              mb-5
            "
          >

            <div>

              <p
                className="
                  text-xs
                  uppercase
                  tracking-[0.2em]
                  text-[#9DFF00]
                "
              >
                Step 01
              </p>


              <h2 className="mt-2 text-2xl font-medium">
                Select languages
              </h2>

            </div>


            <span
              className="
                text-xs
                text-gray-600
                font-mono
              "
            >
              {selectedLanguages.length}/5 selected
            </span>

          </div>


          <div
            className="
              grid
              grid-cols-2
              sm:grid-cols-3
              lg:grid-cols-5
              gap-3
            "
          >

            {languages.map((language) => {

              const selected =
                selectedLanguages.includes(
                  language.name
                );


              const disabled =
                !selected &&
                selectedLanguages.length >= 5;


              return (

                <button
                  key={language.name}
                  onClick={() =>
                    toggleLanguage(language.name)
                  }
                  disabled={disabled}
                  className={`
                    group
                    relative
                    text-left
                    p-5
                    rounded-2xl
                    border
                    transition-all
                    duration-300
                    ${
                      selected
                        ? `
                          border-[#9DFF00]/50
                          bg-[#9DFF00]/[0.055]
                          shadow-[0_0_30px_rgba(157,255,0,0.045)]
                        `
                        : `
                          border-white/10
                          bg-[#090e10]
                          hover:border-white/20
                          hover:-translate-y-0.5
                        `
                    }
                    ${
                      disabled
                        ? "opacity-35 cursor-not-allowed"
                        : "cursor-pointer"
                    }
                  `}
                >

                  {/* CHECK */}

                  <div
                    className={`
                      absolute
                      top-4
                      right-4
                      w-5
                      h-5
                      rounded-full
                      flex
                      items-center
                      justify-center
                      text-[10px]
                      transition
                      ${
                        selected
                          ? `
                            bg-[#9DFF00]
                            text-black
                          `
                          : `
                            border
                            border-white/10
                            text-transparent
                          `
                      }
                    `}
                  >
                    ✓
                  </div>


                  {/* LANGUAGE SYMBOL */}

                  <div
                    className={`
                      w-11
                      h-11
                      rounded-xl
                      flex
                      items-center
                      justify-center
                      font-mono
                      text-sm
                      font-semibold
                      transition
                      ${
                        selected
                          ? `
                            bg-[#9DFF00]
                            text-black
                          `
                          : `
                            bg-white/[0.035]
                            text-gray-400
                            group-hover:text-white
                          `
                      }
                    `}
                  >
                    {language.short}
                  </div>


                  <h3 className="mt-5 font-medium">
                    {language.name}
                  </h3>


                  <p className="mt-1 text-xs text-gray-600">
                    {language.description}
                  </p>

                </button>

              );

            })}

          </div>

        </section>


        {/* =====================================================
            COMPARE ACTION
        ===================================================== */}

        <div
          className="
            mt-8
            flex
            flex-col
            sm:flex-row
            justify-end
            gap-3
          "
        >

          <button
            onClick={handleReset}
            className="
              px-6
              py-3.5
              rounded-xl
              border
              border-white/10
              text-gray-400
              hover:text-white
              hover:border-white/20
              transition
            "
          >
            Reset
          </button>


          <button
            onClick={handleCompare}
            disabled={
              isComparing ||
              selectedLanguages.length < 2
            }
            className="
              min-w-[210px]
              px-7
              py-3.5
              rounded-xl
              bg-[#9DFF00]
              text-black
              font-semibold
              hover:-translate-y-0.5
              hover:shadow-[0_0_30px_rgba(157,255,0,0.25)]
              transition-all
              disabled:opacity-40
              disabled:cursor-not-allowed
            "
          >

            {isComparing ? (

              <span className="flex items-center justify-center gap-3">

                <span
                  className="
                    w-4
                    h-4
                    border-2
                    border-black/30
                    border-t-black
                    rounded-full
                    animate-spin
                  "
                />

                Comparing...

              </span>

            ) : (

              "Compare Results →"

            )}

          </button>

        </div>


        {/* =====================================================
            LOADING STATE
        ===================================================== */}

        {isComparing && (

          <div
            className="
              mt-10
              rounded-2xl
              border
              border-white/10
              bg-[#090e10]
              p-8
              text-center
            "
          >

            <div
              className="
                mx-auto
                w-12
                h-12
                rounded-full
                border-2
                border-[#9DFF00]/20
                border-t-[#9DFF00]
                animate-spin
              "
            />

            <p className="mt-5 text-gray-300">
              Analysing selected implementations...
            </p>

            <p className="mt-2 text-xs text-gray-600 font-mono">
              Normalising benchmark results
            </p>

          </div>

        )}


        {/* =====================================================
            RESULTS
        ===================================================== */}

        {showResults && (

          <section
            className="
              mt-16
              animate-[fadeIn_.6s_ease-out]
            "
          >

            {/* HEADER */}

            <div
              className="
                flex
                flex-col
                md:flex-row
                md:items-end
                justify-between
                gap-6
                mb-8
              "
            >

              <div>

                <p
                  className="
                    text-[#9DFF00]
                    text-xs
                    uppercase
                    tracking-[0.25em]
                  "
                >
                  Step 02
                </p>


                <h2
                  className="
                    mt-3
                    text-3xl
                    md:text-4xl
                    font-semibold
                  "
                >
                  Comparison results
                </h2>


                <p className="mt-3 text-gray-500">
                  {benchmark} • {selectedLanguages.length} languages
                </p>

              </div>


              {/* WINNER */}

              {winner && (

                <div
                  className="
                    flex
                    items-center
                    gap-4
                    px-5
                    py-4
                    rounded-2xl
                    border
                    border-[#9DFF00]/20
                    bg-[#9DFF00]/[0.04]
                  "
                >

                  <div
                    className="
                      w-11
                      h-11
                      rounded-xl
                      bg-[#9DFF00]
                      text-black
                      flex
                      items-center
                      justify-center
                      text-lg
                    "
                  >
                    ♛
                  </div>


                  <div>

                    <p className="text-xs text-gray-600">
                      Most efficient
                    </p>

                    <p className="mt-1 text-[#9DFF00] font-medium">
                      {winner.language}
                    </p>

                  </div>

                </div>

              )}

            </div>


            {/* =================================================
                QUICK STATS
            ================================================= */}

            <div
              className="
                grid
                grid-cols-2
                lg:grid-cols-4
                gap-4
              "
            >

              <QuickStat
                title="Best Time"
                value={
                  `${Math.min(
                    ...comparisonResults.map(
                      (item) => item.time
                    )
                  )} ms`
                }
                label="Fastest execution"
              />


              <QuickStat
                title="Lowest CPU"
                value={
                  `${Math.min(
                    ...comparisonResults.map(
                      (item) => item.cpu
                    )
                  )}%`
                }
                label="Lowest utilisation"
              />


              <QuickStat
                title="Lowest Memory"
                value={
                  `${Math.min(
                    ...comparisonResults.map(
                      (item) => item.memory
                    )
                  )} MB`
                }
                label="Lowest RAM usage"
              />


              <QuickStat
                title="Lowest Energy"
                value={
                  `${Math.min(
                    ...comparisonResults.map(
                      (item) => item.energy
                    )
                  )} J`
                }
                label="Lowest energy use"
              />

            </div>


            {/* =================================================
                TABLE
            ================================================= */}

            <div
              className="
                mt-5
                rounded-2xl
                border
                border-white/10
                bg-[#090e10]
                overflow-hidden
              "
            >

              <div className="px-6 py-5 border-b border-white/5">

                <p
                  className="
                    text-xs
                    uppercase
                    tracking-[0.2em]
                    text-gray-500
                  "
                >
                  Detailed comparison
                </p>

              </div>


              <div className="overflow-x-auto">

                <table className="w-full min-w-[800px]">

                  <thead>

                    <tr className="border-b border-white/5">

                      <th className="text-left px-6 py-5 text-xs font-normal text-gray-600">
                        Language
                      </th>

                      <th className="text-right px-6 py-5 text-xs font-normal text-gray-600">
                        Execution Time
                      </th>

                      <th className="text-right px-6 py-5 text-xs font-normal text-gray-600">
                        CPU
                      </th>

                      <th className="text-right px-6 py-5 text-xs font-normal text-gray-600">
                        Memory
                      </th>

                      <th className="text-right px-6 py-5 text-xs font-normal text-gray-600">
                        Energy
                      </th>

                      <th className="text-right px-6 py-5 text-xs font-normal text-gray-600">
                        Green Score
                      </th>

                    </tr>

                  </thead>


                  <tbody>

                    {[...comparisonResults]
                      .sort(
                        (a, b) =>
                          b.score - a.score
                      )
                      .map((item, index) => {

                        const isWinner =
                          item.language ===
                          winner?.language;


                        return (

                          <tr
                            key={item.language}
                            className={`
                              border-b
                              border-white/5
                              last:border-b-0
                              transition
                              ${
                                isWinner
                                  ? "bg-[#9DFF00]/[0.025]"
                                  : "hover:bg-white/[0.015]"
                              }
                            `}
                          >

                            {/* LANGUAGE */}

                            <td className="px-6 py-5">

                              <div className="flex items-center gap-4">

                                <span
                                  className={`
                                    w-7
                                    h-7
                                    rounded-lg
                                    flex
                                    items-center
                                    justify-center
                                    text-xs
                                    font-mono
                                    ${
                                      index === 0
                                        ? `
                                          bg-[#9DFF00]
                                          text-black
                                        `
                                        : `
                                          bg-white/[0.04]
                                          text-gray-500
                                        `
                                    }
                                  `}
                                >
                                  {index + 1}
                                </span>


                                <div>

                                  <p
                                    className={`
                                      font-medium
                                      ${
                                        isWinner
                                          ? "text-[#9DFF00]"
                                          : "text-white"
                                      }
                                    `}
                                  >
                                    {item.language}
                                  </p>


                                  {isWinner && (

                                    <span
                                      className="
                                        text-[10px]
                                        uppercase
                                        tracking-widest
                                        text-[#9DFF00]/60
                                      "
                                    >
                                      Best performer
                                    </span>

                                  )}

                                </div>

                              </div>

                            </td>


                            {/* TIME */}

                            <td
                              className="
                                px-6
                                py-5
                                text-right
                                font-mono
                                text-sm
                              "
                            >
                              {item.time} ms
                            </td>


                            {/* CPU */}

                            <td
                              className="
                                px-6
                                py-5
                                text-right
                                font-mono
                                text-sm
                                text-gray-400
                              "
                            >
                              {item.cpu}%
                            </td>


                            {/* MEMORY */}

                            <td
                              className="
                                px-6
                                py-5
                                text-right
                                font-mono
                                text-sm
                                text-gray-400
                              "
                            >
                              {item.memory} MB
                            </td>


                            {/* ENERGY */}

                            <td
                              className="
                                px-6
                                py-5
                                text-right
                                font-mono
                                text-sm
                                text-gray-400
                              "
                            >
                              {item.energy} J
                            </td>


                            {/* SCORE */}

                            <td className="px-6 py-5">

                              <div
                                className="
                                  flex
                                  items-center
                                  justify-end
                                  gap-3
                                "
                              >

                                <div
                                  className="
                                    w-20
                                    h-1.5
                                    rounded-full
                                    bg-white/5
                                    overflow-hidden
                                  "
                                >

                                  <div
                                    className="
                                      h-full
                                      rounded-full
                                      bg-[#9DFF00]
                                    "
                                    style={{
                                      width:
                                        `${item.score}%`,
                                    }}
                                  />

                                </div>


                                <span
                                  className={`
                                    min-w-[30px]
                                    text-right
                                    font-mono
                                    text-sm
                                    ${
                                      isWinner
                                        ? "text-[#9DFF00]"
                                        : "text-gray-400"
                                    }
                                  `}
                                >
                                  {item.score}
                                </span>

                              </div>

                            </td>

                          </tr>

                        );

                      })}

                  </tbody>

                </table>

              </div>

            </div>


            {/* =================================================
                VISUAL COMPARISON
            ================================================= */}

            <div className="mt-5">

              <div
                className="
                  rounded-2xl
                  border
                  border-white/10
                  bg-[#090e10]
                  p-6
                  md:p-8
                "
              >

                <div>

                  <p
                    className="
                      text-xs
                      uppercase
                      tracking-[0.2em]
                      text-gray-500
                    "
                  >
                    Resource comparison
                  </p>


                  <h3 className="mt-3 text-xl font-medium">
                    Energy consumption
                  </h3>


                  <p className="mt-2 text-sm text-gray-600">
                    Lower consumption indicates a more
                    energy-efficient implementation.
                  </p>

                </div>


                <div className="mt-8 space-y-6">

                  {[...comparisonResults]
                    .sort(
                      (a, b) =>
                        a.energy - b.energy
                    )
                    .map((item) => {

                      const maxEnergy =
                        Math.max(
                          ...comparisonResults.map(
                            (result) =>
                              result.energy
                          )
                        );


                      const width =
                        (item.energy /
                          maxEnergy) *
                        100;


                      return (

                        <div key={item.language}>

                          <div
                            className="
                              flex
                              justify-between
                              items-center
                              mb-2
                            "
                          >

                            <span className="text-sm text-gray-400">
                              {item.language}
                            </span>


                            <span
                              className="
                                text-xs
                                text-gray-600
                                font-mono
                              "
                            >
                              {item.energy} J
                            </span>

                          </div>


                          <div
                            className="
                              h-2
                              rounded-full
                              bg-white/5
                              overflow-hidden
                            "
                          >

                            <div
                              className="
                                h-full
                                rounded-full
                                bg-[#9DFF00]
                                transition-all
                                duration-1000
                              "
                              style={{
                                width:
                                  `${width}%`,
                              }}
                            />

                          </div>

                        </div>

                      );

                    })}

                </div>

              </div>

            </div>


            {/* =================================================
                RANKING
            ================================================= */}

            <div className="mt-5">

              <div
                className="
                  rounded-2xl
                  border
                  border-[#9DFF00]/15
                  bg-[#0a0f0b]
                  p-6
                  md:p-8
                "
              >

                <div
                  className="
                    flex
                    flex-col
                    md:flex-row
                    md:items-end
                    justify-between
                    gap-4
                  "
                >

                  <div>

                    <p
                      className="
                        text-xs
                        uppercase
                        tracking-[0.2em]
                        text-[#9DFF00]
                      "
                    >
                      Final ranking
                    </p>


                    <h3 className="mt-3 text-2xl font-medium">
                      Efficiency leaderboard
                    </h3>

                  </div>


                  <p className="text-sm text-gray-600">
                    Higher Green Score = better
                  </p>

                </div>


                <div className="mt-8 grid md:grid-cols-3 gap-4">

                  {[...comparisonResults]
                    .sort(
                      (a, b) =>
                        b.score - a.score
                    )
                    .slice(0, 3)
                    .map((item, index) => (

                      <RankingCard
                        key={item.language}
                        rank={index + 1}
                        language={item.language}
                        score={item.score}
                      />

                    ))}

                </div>

              </div>

            </div>


            {/* =================================================
                ACTIONS
            ================================================= */}

            <div
              className="
                mt-8
                flex
                flex-col
                sm:flex-row
                justify-end
                gap-3
              "
            >

              <button
                className="
                  px-6
                  py-3.5
                  rounded-xl
                  border
                  border-white/10
                  text-gray-400
                  hover:text-white
                  hover:border-white/20
                  transition
                "
              >
                Download Report
              </button>


              <Link
                to="/benchmark"
                className="
                  px-7
                  py-3.5
                  rounded-xl
                  bg-[#9DFF00]
                  text-black
                  font-medium
                  text-center
                  hover:-translate-y-0.5
                  hover:shadow-[0_0_25px_rgba(157,255,0,0.25)]
                  transition-all
                "
              >
                New Benchmark →
              </Link>

            </div>

          </section>

        )}


        {/* =====================================================
            EMPTY STATE
        ===================================================== */}

        {!showResults && !isComparing && (

          <div
            className="
              mt-12
              py-16
              text-center
              border
              border-white/5
              rounded-2xl
              bg-white/[0.01]
            "
          >

            <div
              className="
                mx-auto
                w-14
                h-14
                rounded-2xl
                border
                border-white/10
                bg-white/[0.025]
                flex
                items-center
                justify-center
                text-gray-600
                text-xl
              "
            >
              ≋
            </div>


            <h3 className="mt-5 text-lg text-gray-400">
              Ready to compare
            </h3>


            <p className="mt-2 text-sm text-gray-600">
              Select at least two languages and run the comparison.
            </p>

          </div>

        )}

      </div>

    </main>

  );
}


/* =============================================================
    QUICK STAT
============================================================= */

function QuickStat({
  title,
  value,
  label
}) {

  return (

    <div
      className="
        rounded-2xl
        border
        border-white/10
        bg-[#090e10]
        p-5
      "
    >

      <p className="text-xs text-gray-600">
        {title}
      </p>


      <p
        className="
          mt-3
          text-2xl
          font-semibold
          text-[#9DFF00]
          font-mono
        "
      >
        {value}
      </p>


      <p className="mt-2 text-xs text-gray-700">
        {label}
      </p>

    </div>

  );

}


/* =============================================================
    RANKING CARD
============================================================= */

function RankingCard({
  rank,
  language,
  score
}) {

  const rankSymbol =
    rank === 1
      ? "🥇"
      : rank === 2
        ? "🥈"
        : "🥉";


  return (

    <div
      className={`
        rounded-2xl
        p-6
        border
        ${
          rank === 1
            ? `
              border-[#9DFF00]/30
              bg-[#9DFF00]/[0.055]
            `
            : `
              border-white/10
              bg-white/[0.015]
            `
        }
      `}
    >

      <div className="flex items-center justify-between">

        <span className="text-2xl">
          {rankSymbol}
        </span>


        <span
          className="
            text-xs
            text-gray-600
            font-mono
          "
        >
          #{rank}
        </span>

      </div>


      <h4
        className={`
          mt-7
          text-xl
          font-medium
          ${
            rank === 1
              ? "text-[#9DFF00]"
              : "text-white"
          }
        `}
      >
        {language}
      </h4>


      <div className="mt-4 flex items-end gap-2">

        <span className="text-4xl font-semibold">
          {score}
        </span>

        <span className="mb-1 text-sm text-gray-600">
          / 100
        </span>

      </div>


      <div
        className="
          mt-5
          h-1.5
          rounded-full
          bg-white/5
          overflow-hidden
        "
      >

        <div
          className="
            h-full
            rounded-full
            bg-[#9DFF00]
          "
          style={{
            width: `${score}%`,
          }}
        />

      </div>

    </div>

  );

}
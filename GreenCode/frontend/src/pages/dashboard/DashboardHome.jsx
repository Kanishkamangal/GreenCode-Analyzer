import { Link } from "react-router-dom";

export default function DashboardHome() {
  return (
    <div className="min-h-screen bg-[#F9FAFA] text-[#0F172A]">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5 mb-10">

        <div>
          <p className="text-[#0B6B2B] text-xs uppercase tracking-[0.25em] font-semibold">
            GreenCode Analyzer
          </p>

          <h1 className="mt-3 text-3xl md:text-4xl font-semibold text-[#0F172A]">
            Dashboard
          </h1>

          <p className="mt-2 text-[#526174]">
            Overview of your benchmarking activity and performance.
          </p>
        </div>

        <Link
          to="/dashboard/benchmark"
          replace
          className="
            inline-flex
            items-center
            justify-center
            px-6
            py-3
            rounded-xl
            bg-[#0B6B2B]
            text-white
            font-semibold
            hover:bg-[#095923]
            hover:-translate-y-0.5
            hover:shadow-[0_8px_24px_rgba(11,107,43,0.18)]
            transition-all
          "
        >
          Run Benchmark →
        </Link>

      </div>


      {/* =====================================================
          STAT CARDS
      ===================================================== */}

      <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-5">

        <StatCard
          number="24"
          label="Total Benchmarks"
          description="Completed analyses"
        />

        <StatCard
          number="532 ms"
          label="Avg. Execution Time"
          description="Across benchmarks"
        />

        <StatCard
          number="256 MB"
          label="Avg. Memory Usage"
          description="Peak memory average"
        />

        <StatCard
          number="12.45 J"
          label="Avg. Energy Consumption"
          description="Estimated energy usage"
        />

      </div>


      {/* =====================================================
          RECENT BENCHMARKS
      ===================================================== */}

      <section
        className="
          mt-7
          rounded-2xl
          border
          border-[#E3EAE4]
          bg-white
          overflow-hidden
          shadow-[0_4px_20px_rgba(15,23,42,0.04)]
        "
      >

        <div
          className="
            px-6
            py-5
            border-b
            border-[#E3EAE4]
            flex
            items-center
            justify-between
          "
        >

          <div>

            <p className="text-xs uppercase tracking-[0.2em] text-[#6B7280]">
              Activity
            </p>

            <h2 className="mt-2 text-xl font-semibold text-[#0F172A]">
              Recent Benchmarks
            </h2>

          </div>

          <Link
            to="/dashboard/history"
            replace
            className="
              text-sm
              font-medium
              text-[#0B6B2B]
              hover:text-[#166534]
              hover:underline
              transition
            "
          >
            View all →
          </Link>

        </div>


        {/* TABLE */}

        <div className="overflow-x-auto">

          <table className="w-full text-sm">

            <thead>

              <tr className="text-left bg-[#EAF6EC] border-b border-[#E3EAE4]">

                <th className="px-6 py-4 font-semibold text-[#526174]">
                  Benchmark
                </th>

                <th className="px-6 py-4 font-semibold text-[#526174]">
                  Languages
                </th>

                <th className="px-6 py-4 font-semibold text-[#526174]">
                  Date
                </th>

                <th className="px-6 py-4 font-semibold text-[#526174]">
                  Status
                </th>

                <th className="px-6 py-4 font-semibold text-[#526174]">
                  Action
                </th>

              </tr>

            </thead>


            <tbody>

              <BenchmarkRow
                benchmark="Matrix Multiplication"
                languages="C, C++, Python"
                date="13-05-2026"
              />

              <BenchmarkRow
                benchmark="Sorting (Quick Sort)"
                languages="C, Java, Python"
                date="13-05-2026"
              />

              <BenchmarkRow
                benchmark="Fibonacci Series"
                languages="C, Rust, Go"
                date="11-05-2026"
              />

              <BenchmarkRow
                benchmark="Prime Numbers"
                languages="C++, Java, Python"
                date="11-05-2026"
              />

            </tbody>

          </table>

        </div>

      </section>


      {/* =====================================================
          QUICK ACTIONS
      ===================================================== */}

      <section className="mt-7 grid md:grid-cols-2 gap-5">

        <QuickAction
          title="Run a new benchmark"
          description="Compare code performance across programming languages."
          link="/dashboard/benchmark"
          button="Start Benchmark"
        />

        <QuickAction
          title="View benchmark history"
          description="Review your previous benchmark executions and results."
          link="/dashboard/history"
          button="Open History"
        />

      </section>

    </div>
  );
}


/* =========================================================
   STAT CARD
========================================================= */

function StatCard({
  number,
  label,
  description
}) {

  return (
    <div
      className="
        rounded-2xl
        border
        border-[#E3EAE4]
        bg-white
        p-6
        shadow-[0_4px_20px_rgba(15,23,42,0.04)]
        hover:-translate-y-0.5
        hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)]
        transition-all
      "
    >

      <div
        className="
          w-10
          h-1
          rounded-full
          bg-[#16A34A]
          mb-5
        "
      />

      <p className="text-[#526174] text-sm">
        {label}
      </p>

      <h2 className="mt-4 text-3xl font-semibold text-[#0F172A]">
        {number}
      </h2>

      <p className="mt-2 text-xs text-[#6B7280]">
        {description}
      </p>

    </div>
  );
}


/* =========================================================
   BENCHMARK ROW
========================================================= */

function BenchmarkRow({
  benchmark,
  languages,
  date
}) {

  return (
    <tr
      className="
        border-b
        border-[#E3EAE4]
        last:border-b-0
        hover:bg-[#F7FBF8]
        transition
      "
    >

      <td className="px-6 py-4 font-medium text-[#0F172A]">
        {benchmark}
      </td>

      <td className="px-6 py-4 text-[#526174]">
        {languages}
      </td>

      <td className="px-6 py-4 text-[#6B7280]">
        {date}
      </td>

      <td className="px-6 py-4">

        <span
          className="
            inline-flex
            items-center
            px-2.5
            py-1
            rounded-full
            bg-[#DFF0E1]
            text-[#0B6B2B]
            text-xs
            font-semibold
          "
        >
          Completed
        </span>

      </td>

      <td className="px-6 py-4">

        <Link
          to="/dashboard/history"
          replace
          className="
            text-[#0B6B2B]
            hover:text-[#166534]
            font-medium
            transition
          "
        >
          View
        </Link>

      </td>

    </tr>
  );
}


/* =========================================================
   QUICK ACTION
========================================================= */

function QuickAction({
  title,
  description,
  link,
  button
}) {

  return (
    <div
      className="
        rounded-2xl
        border
        border-[#E3EAE4]
        bg-white
        p-6
        shadow-[0_4px_20px_rgba(15,23,42,0.04)]
        hover:-translate-y-0.5
        hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)]
        transition-all
      "
    >

      <div
        className="
          w-10
          h-10
          rounded-xl
          bg-[#DFF0E1]
          flex
          items-center
          justify-center
          mb-4
        "
      >
        <span className="text-[#0B6B2B] text-lg">
          →
        </span>
      </div>

      <h3 className="text-lg font-semibold text-[#0F172A]">
        {title}
      </h3>

      <p className="mt-2 text-sm text-[#526174]">
        {description}
      </p>

      <Link
        to={link}
        replace
        className="
          inline-flex
          items-center
          mt-5
          text-sm
          font-semibold
          text-[#0B6B2B]
          hover:text-[#166534]
          transition
        "
      >
        {button} →
      </Link>

    </div>
  );
}
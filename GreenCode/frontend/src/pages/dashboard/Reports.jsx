import { useEffect, useMemo, useState } from "react";
import api from "../../services/api";

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  const [reportSearch, setReportSearch] = useState("");
  const [selectedBenchmark, setSelectedBenchmark] = useState("all");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [reportSort, setReportSort] = useState("latest");
  const [reportView, setReportView] = useState("list");

  const [comparisons, setComparisons] = useState([]);
  const [comparisonLoading, setComparisonLoading] = useState(true);

  const [selectedComparison, setSelectedComparison] = useState(null);
  const [comparisonDetailLoading, setComparisonDetailLoading] =
    useState(false);

  // Temporary user ID until authentication is connected.
  const userId = 1;
  
  const [reportFormat, setReportFormat] = useState("all");
  

  /* =====================================================
     FETCH REPORT DATA
  ===================================================== */

  useEffect(() => {
    const fetchReports = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get(
          `/history/user/${userId}`
        );

        setReports(response.data.items || []);
      } catch (err) {
        console.error(
          "Failed to fetch reports:",
          err
        );

        setError(
          "Unable to load reports."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, []);








  useEffect(() => {
    const fetchComparisons = async () => {
      try {
        setComparisonLoading(true);

        const response = await api.get(
          `/comparisons/user/${userId}`
        );

        const items = response.data.items || [];

        // Only completed comparisons with at least
        // one benchmark result are shown as reports.
        const completedComparisons = items.filter(
          (item) =>
            item.results &&
            item.results.length > 0
        );

        setComparisons(completedComparisons);
      } catch (err) {
        console.error(
          "Failed to fetch comparison reports:",
          err
        );
      } finally {
        setComparisonLoading(false);
      }
    };

    fetchComparisons();
  }, []);

  /* =====================================================
     DATE FORMAT
  ===================================================== */

  const formatDate = (value) => {
    if (!value) {
      return "—";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
      return value;
    }

    return date.toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  /* =====================================================
     REPORT NAME
  ===================================================== */

  const getReportName = (report) => {
    const benchmark =
      report.benchmark_name || "Benchmark";

    const language =
      report.language || "Program";

    return `${benchmark}_${language}_Report`;
  };

  /* =====================================================
     DOWNLOAD REPORT
  ===================================================== */

  const handleDownload = async (
    analysisId,
    format
  ) => {
    try {
      const response = await api.get(
        `/reports/analysis/${analysisId}/${format}`,
        {
          responseType: "blob",
        }
      );

      const blob = new Blob(
        [response.data]
      );

      const url =
        window.URL.createObjectURL(blob);

      const link =
        document.createElement("a");

      link.href = url;

      link.download =
        `GreenCodeAnalyzer_Analysis_${analysisId}.${format}`;

      document.body.appendChild(link);

      link.click();

      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(
        `Failed to download ${format} report:`,
        err
      );

      alert(
        `Unable to download ${format.toUpperCase()} report.`
      );
    }
  };









  // const handleComparisonDownload = async (comparisonId, format) => {
  //   try {
  //     const response = await api.get(
  //       `/reports/comparison/${comparisonId}/${format}`,
  //       {
  //         responseType: "blob",
  //       }
  //     );

  //     const blob = new Blob([response.data]);

  //     const url = window.URL.createObjectURL(blob);

  //     const link = document.createElement("a");

  //     link.href = url;

  //     link.download =
  //       `GreenCodeAnalyzer_Comparison_${comparisonId}.${format}`;

  //     document.body.appendChild(link);

  //     link.click();

  //     link.remove();

  //     window.URL.revokeObjectURL(url);

  //   } catch (err) {
  //     console.error(
  //       `Failed to download comparison ${format} report:`,
  //       err
  //     );

  //     alert(
  //       `Unable to download comparison ${format.toUpperCase()} report.`
  //     );
  //   }
  // };

      /* =====================================================
      DOWNLOAD COMPARISON REPORT
    ===================================================== */

    const handleComparisonDownload = async (comparisonId, format) => {
      try {
        const response = await api.get(
          `/reports/comparison/${comparisonId}/${format}`,
          {
            responseType: "blob",
          }
        );

        const blob = new Blob([response.data]);

        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;

        link.download = `GreenCodeAnalyzer_Comparison_${comparisonId}.${format}`;

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);
      } catch (err) {
        console.error(
          `Failed to download comparison ${format} report:`,
          err
        );

        alert(
          `Unable to download comparison ${format.toUpperCase()} report.`
        );
      }
    };


  const handleViewComparison = async (comparisonId) => {
    try {
      setComparisonDetailLoading(true);
      setSelectedComparison({
        loading: true,
      });

      const response = await api.get(
        `/comparisons/${comparisonId}`
      );

      setSelectedComparison(response.data);
    } catch (err) {
      console.error(
        "Failed to fetch comparison:",
        err
      );

      setSelectedComparison(null);
      alert("Unable to load comparison details.");
    } finally {
      setComparisonDetailLoading(false);
    }
  };

  const closeComparison = () => {
    setSelectedComparison(null);
  };

  /* =====================================================
     LATEST REPORT
  ===================================================== */

  const latestReport = useMemo(() => {
    if (!reports.length) {
      return null;
    }

    return [...reports].sort(
      (a, b) =>
        new Date(b.created_at) -
        new Date(a.created_at)
    )[0];
  }, [reports]);





  const filteredReports = useMemo(() => {
    let result = [...reports];

    // SEARCH
    if (reportSearch.trim()) {
      const query = reportSearch.toLowerCase();

      result = result.filter((report) => {
        const reportName = getReportName(report).toLowerCase();
        const benchmark = (report.benchmark_name || "").toLowerCase();
        const language = (report.language || "").toLowerCase();

        return (
          reportName.includes(query) ||
          benchmark.includes(query) ||
          language.includes(query)
        );
      });
    }

    // BENCHMARK FILTER
    if (selectedBenchmark !== "all") {
      result = result.filter(
        (report) =>
          report.benchmark_name === selectedBenchmark
      );
    }

    // DATE FILTER
    if (startDate) {
      result = result.filter(
        (report) =>
          new Date(report.created_at) >=
          new Date(`${startDate}T00:00:00`)
      );
    }

    if (endDate) {
      result = result.filter(
        (report) =>
          new Date(report.created_at) <=
          new Date(`${endDate}T23:59:59`)
      );
    }

    // SORT
    // SORT
    result.sort((a, b) => {
      const dateA = new Date(a.created_at);
      const dateB = new Date(b.created_at);

      if (reportSort === "latest") {
        return dateB - dateA;
      }

      if (reportSort === "oldest") {
        return dateA - dateB;
      }

      if (reportSort === "nameAsc") {
        return getReportName(a).localeCompare(
          getReportName(b)
        );
      }

      if (reportSort === "nameDesc") {
        return getReportName(b).localeCompare(
          getReportName(a)
        );
      }

      // File-size sorting is intentionally disabled
      // until real generated file-size metadata exists.
      if (
        reportSort === "sizeDesc" ||
        reportSort === "sizeAsc"
      ) {
        return 0;
      }

      return 0;
    });

    return result;
  }, [
    reports,
    reportSearch,
    selectedBenchmark,
    startDate,
    endDate,
    reportSort,
  ]);



  const benchmarkOptions = useMemo(() => {
    return [
      ...new Set(
        reports
          .map((report) => report.benchmark_name)
          .filter(Boolean)
      ),
    ].sort();
  }, [reports]);

  /* =====================================================
     UI
  ===================================================== */

  return (
    <div className="min-h-screen bg-[#F9FAFA] text-[#0F172A] px-6 py-8 md:px-10">

      {/* HEADER */}

      



      {/* PAGE HEADER */}

      <div className="mb-7 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 -mt-20">

        {/* LEFT — PAGE TITLE */}

        <div className="min-w-0">

          <div className="text-[11px] font-bold tracking-[0.22em] text-[#0B6B2B]">
            REPORTS
          </div>

          <h1 className="mt-2 text-[32px] leading-[1.1] font-bold tracking-[-0.02em] text-[#0F172A]">
            Benchmark Reports
          </h1>

          <p className="mt-2 text-[13px] leading-5 text-[#526174]">
            Access, view, and download detailed reports from your benchmark runs.
          </p>

        </div>


        {/* RIGHT — GENERATED PROMOTIONAL IMAGE */}

        <div className="w-full lg:w-[600px] shrink-0">
          <img
            src="/codetoimpact.png"
            alt="From code to impact — detailed benchmark insights"
            className="block w-full h-[200px] object-contain"
          />
        </div>

      </div>

      {/* ERROR */}

      {error && (
        <div className="mb-6 rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">
          {error}
        </div>
      )}


        {/* QUICK STATS */}

     <div className="grid grid-cols-0 md:grid-cols-1 xl:grid-cols-4 gap-3 -translate-y-5 -mt-3">

        {/* TOTAL REPORTS */}
        <div className="rounded-2xl border border-[#E3EAE4] bg-white p-5 shadow-[0_4px_20px_rgba(15,23,42,0.04)] hover:-translate-y-0.5 hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)] transition-all">

          <div className="flex items-center justify-between">

            <div>
              <p className="text-[#526174] text-sm font-medium">
                Total Reports
              </p>

              <h2 className="mt-2 text-3xl font-bold text-[#0F172A]">
                {reports.length}
              </h2>
            </div>

            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#EAF6EC]">
              <svg
                width="21"
                height="21"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#16803C"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <path d="M14 2v6h6" />
                <path d="M8 13h8" />
                <path d="M8 17h5" />
              </svg>
            </div>

          </div>

          <p className="mt-4 text-[11px] text-[#94A3B8]">
            Generated benchmark reports
          </p>

        </div>


        {/* BENCHMARKS ANALYZED */}
        <div className="rounded-2xl border border-[#E3EAE4] bg-white p-5 shadow-[0_4px_20px_rgba(15,23,42,0.04)] hover:-translate-y-0.5 hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)] transition-all">

          <div className="flex items-center justify-between">

            <div>
              <p className="text-[#526174] text-sm font-medium">
                Benchmarks Analyzed
              </p>

              <h2 className="mt-2 text-3xl font-bold text-[#0F172A]">
                {
                  new Set(
                    reports
                      .map((report) => report.benchmark_name)
                      .filter(Boolean)
                  ).size
                }
              </h2>
            </div>

            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#EAF6EC]">
              <svg
                width="21"
                height="21"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#16803C"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M20 4C12 4 6 8 5 15c-.4 3 1.8 5 4.5 5C16 20 20 13 20 4Z" />
                <path d="M5 20c2-5 6-8 11-10" />
              </svg>
            </div>

          </div>

          <p className="mt-4 text-[11px] text-[#94A3B8]">
            Distinct benchmark workloads
          </p>

        </div>


        {/* TOTAL EXECUTIONS */}
        <div className="rounded-2xl border border-[#E3EAE4] bg-white p-5 shadow-[0_4px_20px_rgba(15,23,42,0.04)] hover:-translate-y-0.5 hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)] transition-all">

          <div className="flex items-center justify-between">

            <div>
              <p className="text-[#526174] text-sm font-medium">
                Total Executions
              </p>

              <h2 className="mt-2 text-3xl font-bold text-[#0F172A]">
                {reports.length}
              </h2>
            </div>

            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#EAF6EC]">
              <svg
                width="21"
                height="21"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#16803C"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="9" />
                <path d="M12 7v5l3 2" />
              </svg>
            </div>

          </div>

          <p className="mt-4 text-[11px] text-[#94A3B8]">
            Benchmark executions recorded
          </p>

        </div>


        {/* ENERGY MEASURED */}
        <div className="rounded-2xl border border-[#E3EAE4] bg-white p-5 shadow-[0_4px_20px_rgba(15,23,42,0.04)] hover:-translate-y-0.5 hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)] transition-all">

          <div className="flex items-center justify-between">

            <div>
              <p className="text-[#526174] text-sm font-medium">
                Energy Measured
              </p>

              <h2 className="mt-2 text-2xl font-bold text-[#0F172A]">
                {(() => {
                  const energyValues = reports
                    .map((report) => report.energy_consumption)
                    .filter(
                      (value) =>
                        value !== null &&
                        value !== undefined &&
                        Number.isFinite(Number(value))
                    );

                  if (!energyValues.length) {
                    return "Unavailable";
                  }

                  const totalJoules = energyValues.reduce(
                    (sum, value) => sum + Number(value),
                    0
                  );

                  const totalKwh = totalJoules / 3600000;

                  return `${totalJoules.toFixed(2)} J`;
                })()}
              </h2>
            </div>

            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#EAF6EC]">
              <svg
                width="21"
                height="21"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#16803C"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M12 3a9 9 0 1 0 9 9h-9V3Z" />
                <path d="M14 3a9 9 0 0 1 7 7h-7V3Z" />
              </svg>
            </div>

          </div>

          <p className="mt-4 text-[11px] text-[#94A3B8]">
            Total measured execution energy
          </p>

        </div>

      </div>

      {/* REPORT FILTER BAR */}
      <div className="mb-5 flex flex-col gap-3 xl:flex-row xl:items-center">

        {/* SEARCH */}
        <div className="relative flex-1">

          <svg
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[#64748B]"
            width="17"
            height="17"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="11" cy="11" r="7" />
            <path d="m20 20-3.5-3.5" />
          </svg>

          <input
            type="text"
            value={reportSearch}
            onChange={(e) =>
              setReportSearch(e.target.value)
            }
            placeholder="Search reports, benchmarks or keywords..."
            className="h-11 w-full rounded-xl border border-[#DCE5DE] bg-white pl-10 pr-4 text-[12px] text-[#334155] outline-none transition placeholder:text-[#94A3B8] focus:border-[#8BBF9A] focus:ring-2 focus:ring-[#EAF6EC]"
          />

        </div>


        {/* ALL BENCHMARKS */}
        <div className="relative">

          <select
            value={selectedBenchmark}
            onChange={(e) =>
              setSelectedBenchmark(e.target.value)
            }
            className="h-11 min-w-[190px] appearance-none rounded-xl border border-[#DCE5DE] bg-white px-4 pr-9 text-[12px] font-medium text-[#475569] outline-none transition focus:border-[#8BBF9A] focus:ring-2 focus:ring-[#EAF6EC]"
          >

            <option value="all">
              All Benchmarks
            </option>

            {benchmarkOptions.map((benchmark) => (
              <option
                key={benchmark}
                value={benchmark}
              >
                {benchmark}
              </option>
            ))}

          </select>

          {/* Dropdown arrow */}
          <svg
            className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-[#64748B]"
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="m6 9 6 6 6-6" />
          </svg>

        </div>


        {/* DATE RANGE */}
        <div className="flex items-center gap-2">

          {/* FROM DATE */}
          <div className="relative">

            <input
              type="date"
              value={startDate}
              onChange={(e) =>
                setStartDate(e.target.value)
              }
              className="h-11 rounded-xl border border-[#DCE5DE] bg-white px-3 text-[12px] text-[#475569] outline-none transition focus:border-[#8BBF9A] focus:ring-2 focus:ring-[#EAF6EC]"
            />

          </div>

          <span className="text-[11px] text-[#94A3B8]">
            to
          </span>

          {/* TO DATE */}
          <div className="relative">

            <input
              type="date"
              value={endDate}
              onChange={(e) =>
                setEndDate(e.target.value)
              }
              className="h-11 rounded-xl border border-[#DCE5DE] bg-white px-3 text-[12px] text-[#475569] outline-none transition focus:border-[#8BBF9A] focus:ring-2 focus:ring-[#EAF6EC]"
            />

          </div>

        </div>


        {/* CLEAR FILTERS */}
        {(reportSearch ||
          selectedBenchmark !== "all" ||
          startDate ||
          endDate) && (

          <button
            type="button"
            onClick={() => {
              setReportSearch("");
              setSelectedBenchmark("all");
              setStartDate("");
              setEndDate("");
            }}
            className="h-11 rounded-xl border border-[#DCE5DE] bg-white px-4 text-[12px] font-medium text-[#64748B] transition hover:border-[#B8D4BE] hover:bg-[#F7FAF8] hover:text-[#166534]"
          >
            Clear
          </button>

        )}

      </div>






      


    {/* GENERATED REPORTS */}

    <section className="rounded-2xl border border-[#DDE7DF] bg-white shadow-[0_2px_12px_rgba(15,23,42,0.04)] overflow-hidden">

      {/* HEADER */}

      <div className="px-5 py-5 border-b border-[#E2EAE4]">

        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">

          {/* TITLE */}

          <div className="flex items-start gap-3">

            {/* REPORT ICON */}

            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#EAF6EC] border border-[#D5E9D9]">

              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#16753A"
                strokeWidth="1.8"
              >
                <path
                  d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                />
                <path d="M14 2v6h6" />
                <path d="M8 13h8" />
                <path d="M8 17h6" />
              </svg>

            </div>

            <div>

              <h2 className="text-[17px] font-bold text-[#0F172A]">
                Generated Reports
              </h2>

              <p className="mt-1 text-[12px] text-[#526174]">
                Download and explore detailed performance reports from your benchmark runs.
              </p>

            </div>

          </div>


          {/* SORT */}

          {/* SORT + VIEW CONTROLS */}

        <div className="flex items-center gap-2">

          <span className="text-[12px] text-[#64748B]">
            Sort by
          </span>

          {/* SORT DROPDOWN */}
          <select
            value={reportSort}
            onChange={(e) => setReportSort(e.target.value)}
            className="h-9 rounded-lg border border-[#DCE5DE] bg-white px-3 text-[12px] font-medium text-[#334155] outline-none transition focus:border-[#198754] focus:ring-2 focus:ring-[#EAF6EC]"
          >
            <option value="latest">
              Latest First
            </option>

            <option value="oldest">
              Oldest First
            </option>

            <option value="nameAsc">
              Name A-Z
            </option>

            <option value="nameDesc">
              Name Z-A
            </option>

            <option value="sizeDesc" disabled>
              Largest File
            </option>

            <option value="sizeAsc" disabled>
              Smallest File
            </option>
          </select>

          {/* LIST / GRID TOGGLE */}
          <div className="ml-1 flex items-center rounded-lg border border-[#DCE5DE] bg-white p-0.5">

            {/* LIST VIEW */}
            <button
              type="button"
              onClick={() => setReportView("list")}
              title="List view"
              className={`flex h-8 w-8 items-center justify-center rounded-md transition ${
                reportView === "list"
                  ? "bg-[#EAF6EC] text-[#16803C]"
                  : "text-[#64748B] hover:bg-[#F7FAF8]"
              }`}
            >
              <svg
                width="17"
                height="17"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M8 6h13" />
                <path d="M8 12h13" />
                <path d="M8 18h13" />
                <path d="M3 6h.01" />
                <path d="M3 12h.01" />
                <path d="M3 18h.01" />
              </svg>
            </button>

            {/* GRID VIEW */}
            <button
              type="button"
              onClick={() => setReportView("grid")}
              title="Grid view"
              className={`flex h-8 w-8 items-center justify-center rounded-md transition ${
                reportView === "grid"
                  ? "bg-[#EAF6EC] text-[#16803C]"
                  : "text-[#64748B] hover:bg-[#F7FAF8]"
              }`}
            >
              <svg
                width="17"
                height="17"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <rect x="4" y="4" width="6" height="6" />
                <rect x="14" y="4" width="6" height="6" />
                <rect x="4" y="14" width="6" height="6" />
                <rect x="14" y="14" width="6" height="6" />
              </svg>
            </button>

          </div>

        </div>

        </div>




      </div>


      {/* TABLE */}

      {reportView === "list" ? (

      <div className="overflow-x-auto">

        <table className="w-full min-w-[900px] border-collapse">

          {/* TABLE HEADER */}

          <thead>

            <tr className="bg-[#EAF6EC] border-b border-[#DCE8DF]">

              <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                Report Name
              </th>

              <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                Benchmark
              </th>

              <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                Generated On
              </th>

              <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                Format
              </th>

              <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                Actions
              </th>

            </tr>

          </thead>


          {/* TABLE BODY */}

          <tbody>

            {filteredReports.map((report, index) => (

              <tr
                key={report.analysis_id}
                className="border-b border-[#E7ECE9] last:border-b-0 hover:bg-[#FAFCFB] transition"
              >

                {/* REPORT NAME */}

                <td className="px-5 py-4">

                  <div className="flex items-center gap-3">

                    {/* FILE ICON */}

                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#EAF6EC]">

                      <svg
                        width="17"
                        height="17"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="#17833F"
                        strokeWidth="1.8"
                      >
                        <path
                          d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                        />
                        <path d="M14 2v6h6" />
                        <path d="M8 13h8" />
                        <path d="M8 17h6" />
                      </svg>

                    </div>


                    <div>

                      <div className="text-[12px] font-semibold text-[#0F172A]">
                        {getReportName(report)}
                      </div>

                      <div className="mt-0.5 text-[10px] text-[#94A3B8]">
                        Analysis #{report.analysis_id}
                      </div>

                    </div>

                  </div>

                </td>


                {/* BENCHMARK */}

                <td className="px-5 py-4">

                  <div className="text-[12px] font-medium text-[#475569]">
                    {report.benchmark_name}
                  </div>

                  {report.category && (
                    <div className="mt-1 text-[10px] text-[#94A3B8]">
                      {report.category}
                    </div>
                  )}

                </td>


                {/* GENERATED ON */}

                <td className="px-5 py-4">

                  <div className="text-[12px] font-medium text-[#475569]">
                    {new Date(report.created_at).toLocaleDateString("en-GB")}
                  </div>

                  <div className="mt-0.5 text-[10px] text-[#94A3B8]">
                    {new Date(report.created_at).toLocaleTimeString(
                      "en-IN",
                      {
                        hour: "2-digit",
                        minute: "2-digit",
                      }
                    )}
                  </div>

                </td>


                {/* FORMAT */}

                <td className="px-5 py-4">

                  <div className="flex items-center gap-2 flex-wrap">

                    {/* PDF */}

                    <span className="inline-flex items-center rounded-md bg-[#FDECEC] px-2.5 py-1 text-[10px] font-bold text-[#D84A4A]">
                      PDF
                    </span>

                    {/* XLSX */}

                    <span className="inline-flex items-center rounded-md bg-[#EAF7ED] px-2.5 py-1 text-[10px] font-bold text-[#29934A]">
                      Excel
                    </span>

                    {/* CSV */}

                    <span className="inline-flex items-center rounded-md bg-[#EAF2FC] px-2.5 py-1 text-[10px] font-bold text-[#4185C5]">
                      CSV
                    </span>

                  </div>

                </td>


                {/* ACTIONS */}

                <td className="px-5 py-4">

                  <div className="flex items-center gap-2">

                    {/* DOWNLOAD PDF */}

                    <button
                      type="button"
                      onClick={() =>
                        handleDownload(report.analysis_id, "pdf")
                      }
                      className="inline-flex items-center gap-1.5 rounded-lg border border-[#CFE3D4] bg-white px-3 py-2 text-[11px] font-semibold text-[#16753A] hover:bg-[#F2FAF4] transition"
                    >

                      <svg
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                      >
                        <path d="M12 3v12" />
                        <path d="m7 10 5 5 5-5" />
                        <path d="M5 21h14" />
                      </svg>

                      PDF

                    </button>


                    {/* XLSX */}

                    <button
                      type="button"
                      onClick={() =>
                        handleDownload(report.analysis_id, "xlsx")
                      }
                      className="inline-flex items-center gap-1.5 rounded-lg border border-[#CFE3D4] bg-white px-3 py-2 text-[11px] font-semibold text-[#16753A] hover:bg-[#F2FAF4] transition"
                    >
                      XLSX
                    </button>


                    {/* CSV */}

                    <button
                      type="button"
                      onClick={() =>
                        handleDownload(report.analysis_id, "csv")
                      }
                      className="inline-flex items-center gap-1.5 rounded-lg border border-[#CFE3D4] bg-white px-3 py-2 text-[11px] font-semibold text-[#16753A] hover:bg-[#F2FAF4] transition"
                    >
                      CSV
                    </button>

                  </div>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>
    
   ) : (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {filteredReports.map((report) => (
          <div
            key={report.analysis_id}
            className="
              group
              rounded-2xl
              border border-[#DCE9DF]
              bg-white
              p-5
              shadow-sm
              transition-all
              duration-200
              hover:-translate-y-1
              hover:border-[#9BC7A8]
              hover:shadow-md
            "
          >
            {/* CARD HEADER */}
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-3 min-w-0">
                {/* FILE ICON */}
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#EAF6EC]">
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="#17833F"
                    strokeWidth="1.8"
                  >
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <path d="M14 2v6h6" />
                    <path d="M8 13h8" />
                    <path d="M8 17h6" />
                  </svg>
                </div>

                <div className="min-w-0">
                  <h3 className="truncate text-[13px] font-bold text-[#0F172A]">
                    {getReportName(report)}
                  </h3>

                  <p className="mt-1 text-[10px] text-[#94A3B8]">
                    Analysis #{report.analysis_id}
                  </p>
                </div>
              </div>

              {/* LANGUAGE */}
              <span className="shrink-0 rounded-full bg-[#EEF8F0] px-2.5 py-1 text-[10px] font-semibold text-[#267A3F]">
                {report.language || "Unknown"}
              </span>
            </div>

            {/* BENCHMARK + CATEGORY */}
            <div className="mt-4 flex items-center gap-2 flex-wrap">
              <span className="text-[11px] font-semibold text-[#475569]">
                {report.benchmark_name}
              </span>

              {report.category && (
                <>
                  <span className="text-[#CBD5E1]">•</span>

                  <span className="text-[10px] text-[#94A3B8]">
                    {report.category}
                  </span>
                </>
              )}
            </div>

            {/* DATE */}
            <div className="mt-2 text-[10px] text-[#94A3B8]">
              Generated{" "}
              {new Date(report.created_at).toLocaleDateString("en-GB")}
              {" · "}
              {new Date(report.created_at).toLocaleTimeString("en-IN", {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </div>

            {/* METRICS */}
            <div className="mt-5 grid grid-cols-2 gap-3">
              {/* EXECUTION TIME */}
              <div className="rounded-xl bg-[#F8FAF9] p-3">
                <div className="text-[9px] font-semibold uppercase tracking-wide text-[#94A3B8]">
                  Execution Time
                </div>

                <div className="mt-1 text-[13px] font-bold text-[#1E293B]">
                  {report.execution_time != null
                    ? `${report.execution_time.toFixed(2)} ms`
                    : "—"}
                </div>
              </div>

              {/* ENERGY */}
              <div className="rounded-xl bg-[#F8FAF9] p-3">
                <div className="text-[9px] font-semibold uppercase tracking-wide text-[#94A3B8]">
                  Energy
                </div>

                <div className="mt-1 text-[13px] font-bold text-[#1E293B]">
                  {report.energy_consumption != null
                    ? `${report.energy_consumption.toFixed(3)} J`
                    : "—"}
                </div>
              </div>

              {/* MEMORY */}
              <div className="rounded-xl bg-[#F8FAF9] p-3">
                <div className="text-[9px] font-semibold uppercase tracking-wide text-[#94A3B8]">
                  Memory
                </div>

                <div className="mt-1 text-[13px] font-bold text-[#1E293B]">
                  {report.memory_usage != null
                    ? `${report.memory_usage.toFixed(2)} MB`
                    : "—"}
                </div>
              </div>

              {/* GREEN SCORE */}
              <div className="rounded-xl bg-[#F8FAF9] p-3">
                <div className="text-[9px] font-semibold uppercase tracking-wide text-[#94A3B8]">
                  Green Score
                </div>

                <div className="mt-1 text-[13px] font-bold text-[#1E293B]">
                  {report.green_score != null
                    ? `${report.green_score.toFixed(1)} / 100`
                    : "Not available"}
                </div>
              </div>
            </div>

            {/* OUTPUT VERIFIED */}
            <div className="mt-4">
              {report.output_verified ? (
                <span className="inline-flex items-center gap-1.5 rounded-full bg-[#EAF7ED] px-2.5 py-1 text-[10px] font-semibold text-[#267A3F]">
                  <span className="h-1.5 w-1.5 rounded-full bg-[#29934A]" />
                  Output Verified
                </span>
              ) : (
                <span className="inline-flex items-center gap-1.5 rounded-full bg-[#F8EEEE] px-2.5 py-1 text-[10px] font-semibold text-[#B54747]">
                  <span className="h-1.5 w-1.5 rounded-full bg-[#D84A4A]" />
                  Output Not Verified
                </span>
              )}
            </div>

            {/* ACTIONS */}
            <div className="mt-5 flex items-center justify-between gap-3 border-t border-[#EEF2EF] pt-4">
              {/* VIEW REPORT */}
              <button
                type="button"
                onClick={() => handleViewReport(report)}
                className="
                  rounded-lg
                  bg-[#17833F]
                  px-3.5
                  py-2
                  text-[11px]
                  font-semibold
                  text-white
                  transition
                  hover:bg-[#126B34]
                "
              >
                View Report
              </button>

              {/* DOWNLOADS */}
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() =>
                    handleDownload(report.analysis_id, "pdf")
                  }
                  className="
                    rounded-lg
                    border border-[#CFE3D4]
                    bg-white
                    px-2.5
                    py-2
                    text-[10px]
                    font-semibold
                    text-[#16753A]
                    transition
                    hover:bg-[#F2FAF4]
                  "
                >
                  PDF
                </button>

                <button
                  type="button"
                  onClick={() =>
                    handleDownload(report.analysis_id, "xlsx")
                  }
                  className="
                    rounded-lg
                    border border-[#CFE3D4]
                    bg-white
                    px-2.5
                    py-2
                    text-[10px]
                    font-semibold
                    text-[#16753A]
                    transition
                    hover:bg-[#F2FAF4]
                  "
                >
                  XLSX
                </button>

                <button
                  type="button"
                  onClick={() =>
                    handleDownload(report.analysis_id, "csv")
                  }
                  className="
                    rounded-lg
                    border border-[#CFE3D4]
                    bg-white
                    px-2.5
                    py-2
                    text-[10px]
                    font-semibold
                    text-[#16753A]
                    transition
                    hover:bg-[#F2FAF4]
                  "
                >
                  CSV
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    )}


      {/* EMPTY SEARCH RESULT */}

      {filteredReports.length === 0 && !loading && (

        <div className="px-6 py-12 text-center">

          <div className="mx-auto flex h-11 w-11 items-center justify-center rounded-full bg-[#EAF6EC]">

            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#17833F"
              strokeWidth="1.8"
            >
              <circle cx="11" cy="11" r="7" />
              <path d="m20 20-3.5-3.5" />
            </svg>

          </div>

          <p className="mt-3 text-sm font-semibold text-[#334155]">
            No reports found
          </p>

          <p className="mt-1 text-xs text-[#94A3B8]">
            Try searching with a different report, benchmark, or language.
          </p>

        </div>

      )}

    </section>






      {/* =====================================================
          COMPARISON REPORTS
      ===================================================== */}

      <section className="mt-7 rounded-2xl border border-[#E3EAE4] bg-white overflow-hidden shadow-[0_4px_20px_rgba(15,23,42,0.04)]">

        {/* SECTION HEADER */}

        <div className="px-6 py-5 border-b border-[#E3EAE4]">
          <div className="flex items-center justify-between gap-4">

            <div>
              <h2 className="text-xl font-semibold text-[#0F172A]">
                Comparison Reports
              </h2>

              <p className="mt-1 text-sm text-[#526174]">
                Compare measured performance across different language
                implementations of the same benchmark.
              </p>
            </div>

            <div className="hidden md:flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EAF6EC] text-[#0B6B2B] text-sm font-medium">
              {comparisons.length}{" "}
              {comparisons.length === 1
                ? "Comparison"
                : "Comparisons"}
            </div>

          </div>
        </div>


        {/* CONTENT */}

        <div className="p-6">

          {comparisonLoading ? (

            <div className="py-12 text-center text-[#6B7280]">
              Loading comparison reports...
            </div>

          ) : comparisons.length > 0 ? (

            <div className="space-y-4">

              {comparisons.map((item) => {

                const comparison = item.comparison;
                const benchmark = item.benchmark;
                const results = item.results || [];

                const benchmarkName =
                  benchmark?.bench_name ||
                  comparison?.custom_benchmark_name ||
                  "Comparison";

                const category =
                  benchmark?.category ||
                  comparison?.custom_category ||
                  "—";

                const inputSize =
                  results[0]?.analysis?.input_size;

                return (
                  <div
                    key={comparison.comparison_id}
                    className="rounded-2xl border border-[#E3EAE4] bg-[#FBFDFC] p-5 hover:border-[#BFD7C2] hover:shadow-[0_6px_24px_rgba(15,23,42,0.05)] transition-all duration-200"
                  >

                    {/* TOP ROW */}

                    <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5">

                      <div className="min-w-0">

                        <div className="flex flex-wrap items-center gap-3">

                          <h3 className="text-lg font-semibold text-[#0F172A]">
                            {benchmarkName}
                          </h3>

                          <span className="px-2.5 py-1 rounded-full bg-[#EAF6EC] text-[#0B6B2B] text-xs font-semibold">
                            Comparison #{comparison.comparison_id}
                          </span>

                        </div>

                        <p className="mt-2 text-sm text-[#526174]">
                          {category}
                        </p>

                      </div>


                      {/* VIEW BUTTON */}

                        <button
                            onClick={() =>
                              handleViewComparison(
                                comparison.comparison_id
                              )
                            }
                            className="
                              px-4 py-2.5
                              rounded-lg
                              bg-[#0B6B2B]
                              text-white
                              text-sm
                              font-semibold
                              hover:bg-[#095A24]
                              transition-all
                              duration-200
                            "
                          >
                            View Comparison →
                          </button>

                          <button
                            onClick={() =>
                              handleComparisonDownload(
                                comparison.comparison_id,
                                "pdf"
                              )
                            }
                            className="
                              px-3 py-2.5
                              rounded-lg
                              border border-[#BFD7C2]
                              bg-white
                              text-[#0B6B2B]
                              text-sm
                              font-medium
                              hover:bg-[#EAF6EC]
                              transition-all
                              duration-200
                            "
                          >
                            PDF
                          </button>

                          <button
                            onClick={() =>
                              handleComparisonDownload(
                                comparison.comparison_id,
                                "xlsx"
                              )
                            }
                            className="
                              px-3 py-2.5
                              rounded-lg
                              border border-[#BFD7C2]
                              bg-white
                              text-[#0B6B2B]
                              text-sm
                              font-medium
                              hover:bg-[#EAF6EC]
                              transition-all
                              duration-200
                            "
                          >
                            XLSX
                          </button>

                          <button
                            onClick={() =>
                              handleComparisonDownload(
                                comparison.comparison_id,
                                "csv"
                              )
                            }
                            className="
                              px-3 py-2.5
                              rounded-lg
                              border border-[#BFD7C2]
                              bg-white
                              text-[#0B6B2B]
                              text-sm
                              font-medium
                              hover:bg-[#EAF6EC]
                              transition-all
                              duration-200
                            "
                          >
                            CSV
                          </button>

                    </div>


                    {/* METADATA */}

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-5">

                      <div className="rounded-xl border border-[#E3EAE4] bg-white px-4 py-3">
                        <p className="text-xs text-[#6B7280]">
                          Benchmark Size
                        </p>

                        <p className="mt-1 text-sm font-semibold text-[#0F172A] capitalize">
                          {comparison?.bench_size || "—"}
                        </p>
                      </div>


                      <div className="rounded-xl border border-[#E3EAE4] bg-white px-4 py-3">
                        <p className="text-xs text-[#6B7280]">
                          Input Size
                        </p>

                        <p className="mt-1 text-sm font-semibold text-[#0F172A]">
                          {inputSize != null
                            ? inputSize.toLocaleString()
                            : "—"}
                        </p>
                      </div>


                      <div className="rounded-xl border border-[#E3EAE4] bg-white px-4 py-3">
                        <p className="text-xs text-[#6B7280]">
                          Implementations
                        </p>

                        <p className="mt-1 text-sm font-semibold text-[#0F172A]">
                          {results.length}
                        </p>
                      </div>


                      <div className="rounded-xl border border-[#E3EAE4] bg-white px-4 py-3">
                        <p className="text-xs text-[#6B7280]">
                          Created
                        </p>

                        <p className="mt-1 text-sm font-semibold text-[#0F172A]">
                          {formatDate(comparison?.created_at)}
                        </p>
                      </div>

                    </div>


                    {/* IMPLEMENTATIONS */}

                    <div className="mt-5">

                      <p className="mb-3 text-xs uppercase tracking-[0.15em] font-semibold text-[#6B7280]">
                        Implementations
                      </p>

                      <div className="flex flex-wrap gap-3">

                        {results.map((result) => {

                          const analysis = result.analysis;
                          const language = result.language;

                          return (
                            <div
                              key={analysis.analysis_id}
                              className="flex items-center gap-3 px-4 py-3 rounded-xl border border-[#E3EAE4] bg-white"
                            >

                              <div className="w-8 h-8 rounded-lg bg-[#EAF6EC] flex items-center justify-center text-[#0B6B2B] text-xs font-bold">
                                {language?.lang_name
                                  ?.slice(0, 2)
                                  ?.toUpperCase() || "??"}
                              </div>

                              <div>
                                <p className="text-sm font-semibold text-[#0F172A]">
                                  {language?.lang_name || "Unknown"}
                                </p>

                                <p className="text-xs text-[#6B7280]">
                                  {analysis?.execution_time != null
                                    ? `${analysis.execution_time.toFixed(2)} ms`
                                    : "—"}
                                </p>
                              </div>

                            </div>
                          );

                        })}

                      </div>

                    </div>

                  </div>
                );

              })}

            </div>

          ) : (

            <div className="py-12 text-center">

              <div className="mx-auto w-12 h-12 rounded-xl bg-[#EAF6EC] flex items-center justify-center text-[#0B6B2B] text-xl">
                ⇄
              </div>

              <h3 className="mt-4 text-base font-semibold text-[#0F172A]">
                No comparison reports yet
              </h3>

              <p className="mt-1 text-sm text-[#6B7280]">
                Completed comparison runs will appear here.
              </p>

            </div>

          )}

        </div>

      </section>

      {/* INFO CARD */}

      <section className="mt-7 rounded-2xl border border-[#C6E3CB] bg-[#EAF6EC] p-6">

        <div className="flex items-start gap-4">

          <div className="w-10 h-10 shrink-0 rounded-xl bg-[#DFF0E1] flex items-center justify-center">

            <span className="text-[#0B6B2B] font-bold">
              ✓
            </span>

          </div>

          <div>

            <h3 className="text-base font-semibold text-[#0F172A]">
              Report Information
            </h3>

            <p className="mt-1 text-sm leading-6 text-[#526174]">
              Reports contain benchmark performance metrics including
              execution time, CPU usage, memory consumption, energy
              consumption, and overall efficiency scores.
            </p>

          </div>

        </div>

      </section>

















     {/* =====================================================
          COMPARISON DETAIL MODAL
      ===================================================== */}

      {selectedComparison && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4 py-6"
          onClick={closeComparison}
        >

          <div
            className="w-full max-w-6xl max-h-[90vh] overflow-y-auto rounded-2xl bg-white shadow-2xl"
            onClick={(event) => event.stopPropagation()}
          >

            {/* MODAL HEADER */}

            <div className="sticky top-0 z-10 bg-white border-b border-[#E3EAE4] px-6 py-5">

              <div className="flex items-start justify-between gap-5">

                <div>

                  <p className="text-xs uppercase tracking-[0.2em] font-semibold text-[#0B6B2B]">
                    Comparison Report
                  </p>

                  <h2 className="mt-2 text-2xl font-bold text-[#0F172A]">
                    {selectedComparison.benchmark?.bench_name ||
                      selectedComparison.comparison?.custom_benchmark_name ||
                      "Comparison"}
                  </h2>

                  <p className="mt-1 text-sm text-[#526174]">
                    Comparison #{selectedComparison.comparison?.comparison_id}
                  </p>

                </div>


                <div className="flex items-center gap-2 shrink-0">

                    <button
                      onClick={() =>
                        handleComparisonDownload(
                          selectedComparison.comparison?.comparison_id,
                          "pdf"
                        )
                      }
                      className="
                        px-3 py-2
                        rounded-lg
                        border border-[#BFD7C2]
                        bg-white
                        text-[#0B6B2B]
                        text-sm
                        font-medium
                        hover:bg-[#EAF6EC]
                        transition-all
                      "
                    >
                      PDF
                    </button>

                    <button
                      onClick={() =>
                        handleComparisonDownload(
                          selectedComparison.comparison?.comparison_id,
                          "xlsx"
                        )
                      }
                      className="
                        px-3 py-2
                        rounded-lg
                        border border-[#BFD7C2]
                        bg-white
                        text-[#0B6B2B]
                        text-sm
                        font-medium
                        hover:bg-[#EAF6EC]
                        transition-all
                      "
                    >
                      XLSX
                    </button>

                    <button
                      onClick={() =>
                        handleComparisonDownload(
                          selectedComparison.comparison?.comparison_id,
                          "csv"
                        )
                      }
                      className="
                        px-3 py-2
                        rounded-lg
                        border border-[#BFD7C2]
                        bg-white
                        text-[#0B6B2B]
                        text-sm
                        font-medium
                        hover:bg-[#EAF6EC]
                        transition-all
                      "
                    >
                      CSV
                    </button>

                    <button
                      onClick={closeComparison}
                      className="
                        w-9 h-9
                        rounded-lg
                        border border-[#E3EAE4]
                        text-[#526174]
                        hover:bg-[#F7FBF8]
                        hover:text-[#0F172A]
                        transition-all
                      "
                    >
                      ✕
                    </button>

                  </div>

              </div>

            </div>


            {/* MODAL CONTENT */}

            <div className="p-6">

              {comparisonDetailLoading ? (

                <div className="py-20 text-center text-[#6B7280]">
                  Loading comparison...
                </div>

              ) : (

                <>

                  {/* METADATA */}

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-7">

                    <div className="rounded-xl border border-[#E3EAE4] p-4">
                      <p className="text-xs text-[#6B7280]">
                        Category
                      </p>
                      <p className="mt-1 font-semibold text-[#0F172A]">
                        {selectedComparison.benchmark?.category ||
                          selectedComparison.comparison?.custom_category ||
                          "—"}
                      </p>
                    </div>

                    <div className="rounded-xl border border-[#E3EAE4] p-4">
                      <p className="text-xs text-[#6B7280]">
                        Benchmark Size
                      </p>
                      <p className="mt-1 font-semibold text-[#0F172A] capitalize">
                        {selectedComparison.comparison?.bench_size || "—"}
                      </p>
                    </div>

                    <div className="rounded-xl border border-[#E3EAE4] p-4">
                      <p className="text-xs text-[#6B7280]">
                        Input Size
                      </p>
                      <p className="mt-1 font-semibold text-[#0F172A]">
                        {selectedComparison.results?.[0]?.analysis?.input_size
                          ? selectedComparison.results[0].analysis.input_size.toLocaleString()
                          : "—"}
                      </p>
                    </div>

                    <div className="rounded-xl border border-[#E3EAE4] p-4">
                      <p className="text-xs text-[#6B7280]">
                        Implementations
                      </p>
                      <p className="mt-1 font-semibold text-[#0F172A]">
                        {selectedComparison.results?.length || 0}
                      </p>
                    </div>

                  </div>


                  {/* COMPARISON TABLE */}

                  <div className="rounded-2xl border border-[#E3EAE4] overflow-hidden">

                    <div className="overflow-x-auto">

                      <table className="w-full text-sm">

                        <thead className="bg-[#EAF6EC]">

                          <tr className="border-b border-[#E3EAE4]">

                            <th className="px-5 py-4 text-left font-semibold text-[#526174]">
                              Metric
                            </th>

                            {selectedComparison.results?.map(
                              (result) => (
                                <th
                                  key={result.analysis.analysis_id}
                                  className="px-5 py-4 text-left font-semibold text-[#0F172A]"
                                >
                                  {result.language.lang_name}
                                </th>
                              )
                            )}

                          </tr>

                        </thead>

                        <tbody>

                          {/* EXECUTION TIME */}

                          <tr className="border-b border-[#E3EAE4]">
                            <td className="px-5 py-4 font-medium text-[#526174]">
                              Execution Time
                            </td>

                            {selectedComparison.results?.map(
                              (result) => (
                                <td
                                  key={result.analysis.analysis_id}
                                  className="px-5 py-4 font-semibold text-[#0F172A]"
                                >
                                  {result.analysis.execution_time?.toFixed(2)} ms
                                </td>
                              )
                            )}

                          </tr>


                          {/* CPU */}

                          <tr className="border-b border-[#E3EAE4]">
                            <td className="px-5 py-4 font-medium text-[#526174]">
                              CPU Usage
                            </td>

                            {selectedComparison.results?.map(
                              (result) => (
                                <td
                                  key={result.analysis.analysis_id}
                                  className="px-5 py-4 font-semibold text-[#0F172A]"
                                >
                                  {result.analysis.cpu_usage?.toFixed(2)}%
                                </td>
                              )
                            )}

                          </tr>


                          {/* MEMORY */}

                          <tr className="border-b border-[#E3EAE4]">
                            <td className="px-5 py-4 font-medium text-[#526174]">
                              Memory Usage
                            </td>

                            {selectedComparison.results?.map(
                              (result) => (
                                <td
                                  key={result.analysis.analysis_id}
                                  className="px-5 py-4 font-semibold text-[#0F172A]"
                                >
                                  {result.analysis.memory_usage?.toFixed(2)} MB
                                </td>
                              )
                            )}

                          </tr>


                          {/* ENERGY */}

                          <tr className="border-b border-[#E3EAE4]">
                            <td className="px-5 py-4 font-medium text-[#526174]">
                              Energy Consumption
                            </td>

                            {selectedComparison.results?.map(
                              (result) => (
                                <td
                                  key={result.analysis.analysis_id}
                                  className="px-5 py-4 font-semibold text-[#0F172A]"
                                >
                                  {result.analysis.energy_consumption != null
                                    ? `${result.analysis.energy_consumption.toFixed(2)} J`
                                    : "—"}
                                </td>
                              )
                            )}

                          </tr>


                          {/* GREEN SCORE */}

                          <tr className="border-b border-[#E3EAE4]">
                            <td className="px-5 py-4 font-medium text-[#526174]">
                              Green Score
                            </td>

                            {selectedComparison.results?.map(
                              (result) => (
                                <td
                                  key={result.analysis.analysis_id}
                                  className="px-5 py-4 font-semibold text-[#0B6B2B]"
                                >
                                  {result.analysis.green_score != null
                                    ? `${result.analysis.green_score}/100`
                                    : "—"}
                                </td>
                              )
                            )}

                          </tr>


                          {/* VALIDATION */}

                          <tr>
                            <td className="px-5 py-4 font-medium text-[#526174]">
                              Output Verified
                            </td>

                            {selectedComparison.results?.map(
                              (result) => (
                                <td
                                  key={result.analysis.analysis_id}
                                  className="px-5 py-4 font-semibold"
                                >
                                  {result.analysis.output_verified
                                    ? "✓ Verified"
                                    : "Not Verified"}
                                </td>
                              )
                            )}

                          </tr>

                        </tbody>

                      </table>

                    </div>

                  </div>


                  {/* REPORT NOTE */}

                  <div className="mt-6 rounded-xl border border-[#C6E3CB] bg-[#EAF6EC] px-5 py-4">

                    <p className="text-sm leading-6 text-[#526174]">
                      This comparison presents the measured benchmark
                      metrics for the implementations included in this
                      comparison run. Values are displayed as recorded
                      during execution.
                    </p>

                  </div>

                </>

              )}

            </div>

          </div>

        </div>
      )}
    </div>
  );
}
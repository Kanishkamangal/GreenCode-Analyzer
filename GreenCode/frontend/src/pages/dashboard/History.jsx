import { useEffect, useMemo, useState } from "react";
import api from "../../services/api";

/*
 * GreenCode Analyzer — Execution History
 *
 * History is intentionally an execution log:
 * - browse/filter/sort previous benchmark executions
 * - inspect one execution with "View"
 * - no duplicate PDF/XLSX/CSV actions here; exports belong to Reports
 */

const PAGE_SIZE = 10;

const iconPaths = {
  search: (
    <>
      <circle cx="11" cy="11" r="6.5" />
      <path d="m16 16 4.5 4.5" />
    </>
  ),
  calendar: (
    <>
      <rect x="3" y="4.5" width="18" height="17" rx="3" />
      <path d="M7 2.5v4M17 2.5v4M3 9h18" />
    </>
  ),
  chevronDown: <path d="m7 10 5 5 5-5" />,
  chevronLeft: <path d="m14.5 7-5 5 5 5" />,
  chevronRight: <path d="m9.5 7 5 5-5 5" />,
  eye: (
    <>
      <path d="M2.5 12s3.4-5.5 9.5-5.5 9.5 5.5 9.5 5.5-3.4 5.5-9.5 5.5S2.5 12 2.5 12Z" />
      <circle cx="12" cy="12" r="2.4" />
    </>
  ),
  more: (
    <>
      <circle cx="12" cy="5" r="1" fill="currentColor" stroke="none" />
      <circle cx="12" cy="12" r="1" fill="currentColor" stroke="none" />
      <circle cx="12" cy="19" r="1" fill="currentColor" stroke="none" />
    </>
  ),
  play: <path d="m9 6 9 6-9 6V6Z" fill="currentColor" stroke="none" />,
  layers: (
    <>
      <path d="m12 3 8 4-8 4-8-4 8-4Z" />
      <path d="m4 12 8 4 8-4" />
      <path d="m4 17 8 4 8-4" />
    </>
  ),
  code: (
    <>
      <path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14" />
    </>
  ),
  check: <path d="m5 12 4.2 4.2L19 6.5" />,
  x: (
    <>
      <path d="m6 6 12 12M18 6 6 18" />
    </>
  ),
  clock: (
    <>
      <circle cx="12" cy="12" r="8.5" />
      <path d="M12 7v5l3.5 2" />
    </>
  ),
  memory: (
    <>
      <rect x="6" y="6" width="12" height="12" rx="2" />
      <path d="M9 2.5v3M15 2.5v3M9 18.5v3M15 18.5v3M2.5 9h3M2.5 15h3M18.5 9h3M18.5 15h3" />
    </>
  ),
  bolt: <path d="M13.2 2.8 5.5 13h5.6l-1 8.2L18.5 11h-5.7l.4-8.2Z" />,
  leaf: (
    <>
      <path d="M19.5 3.5C11 3.6 5.5 7 5.2 13.1c-.2 3.7 2.1 6.2 5.5 6.2 6.1 0 8.7-6 8.8-15.8Z" />
      <path d="M4 20c2.2-4 5.6-6.6 10.7-8.8" />
    </>
  ),
  close: (
    <>
      <path d="m6 6 12 12M18 6 6 18" />
    </>
  ),
};

function Icon({ name, size = 18, strokeWidth = 1.8, className = "" }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      {iconPaths[name]}
    </svg>
  );
}

function getBenchmarkVisual(name = "", category = "") {
  const value = `${name} ${category}`.toLowerCase();

  if (value.includes("matrix")) {
    return {
      icon: "matrix",
      bg: "bg-[#E6EEFF]",
      text: "text-[#315FD1]",
      border: "border-[#C9D8FF]",
    };
  }

  if (
    value.includes("file") ||
    value.includes("processing") ||
    value.includes("io")
  ) {
    return {
      icon: "file",
      bg: "bg-[#FFF0E8]",
      text: "text-[#D86A2A]",
      border: "border-[#FFD7C3]",
    };
  }

  if (
    value.includes("sort") ||
    value.includes("heap") ||
    value.includes("merge") ||
    value.includes("quick")
  ) {
    return {
      icon: "sort",
      bg: "bg-[#FFF3D9]",
      text: "text-[#A96C00]",
      border: "border-[#F3DEAE]",
    };
  }

  if (
    value.includes("fibonacci") ||
    value.includes("sequence") ||
    value.includes("dynamic programming")
  ) {
    return {
      icon: "sigma",
      bg: "bg-[#F0EAFE]",
      text: "text-[#7652C9]",
      border: "border-[#DDD0FA]",
    };
  }

  if (
    value.includes("graph") ||
    value.includes("bfs") ||
    value.includes("dfs") ||
    value.includes("dijkstra")
  ) {
    return {
      icon: "graph",
      bg: "bg-[#E7F7E9]",
      text: "text-[#238144]",
      border: "border-[#C9E9CF]",
    };
  }

  if (
    value.includes("string") ||
    value.includes("pattern") ||
    value.includes("matching")
  ) {
    return {
      icon: "string",
      bg: "bg-[#E8F4FF]",
      text: "text-[#2778B9]",
      border: "border-[#C8E2F7]",
    };
  }

  if (
    value.includes("image") ||
    value.includes("vision") ||
    value.includes("pixel")
  ) {
    return {
      icon: "image",
      bg: "bg-[#EAF0FF]",
      text: "text-[#4969C5]",
      border: "border-[#D2DCFF]",
    };
  }

  if (
    value.includes("prime") ||
    value.includes("number") ||
    value.includes("math")
  ) {
    return {
      icon: "number",
      bg: "bg-[#FFF0DD]",
      text: "text-[#D76A19]",
      border: "border-[#FFD7AE]",
    };
  }

  if (
    value.includes("json") ||
    value.includes("parse") ||
    value.includes("database") ||
    value.includes("sql")
  ) {
    return {
      icon: "database",
      bg: "bg-[#EAF5FF]",
      text: "text-[#3E76A8]",
      border: "border-[#CFE3F3]",
    };
  }

  return {
    icon: "code",
    bg: "bg-[#E9F6EC]",
    text: "text-[#237B3D]",
    border: "border-[#CBE6D1]",
  };
}

function BenchmarkGlyph({ type, size = 20 }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round",
    strokeLinejoin: "round",
    "aria-hidden": true,
  };

  if (type === "matrix") {
    return (
      <svg {...common}>
        <rect x="4" y="4" width="16" height="16" rx="2" />
        <path d="M9.3 4v16M14.7 4v16M4 9.3h16M4 14.7h16" />
      </svg>
    );
  }

  if (type === "file") {
    return (
      <svg {...common}>
        <path d="M7 3.5h7l4 4V20a.5.5 0 0 1-.5.5h-10A.5.5 0 0 1 7 20V3.5Z" />
        <path d="M14 3.5V8h4M9.5 12h5M9.5 15h5" />
      </svg>
    );
  }

  if (type === "sort") {
    return (
      <svg {...common}>
        <path d="M8 5v14M8 5 5 8M8 5l3 3M16 19V5M16 19l-3-3M16 19l3-3" />
      </svg>
    );
  }

  if (type === "sigma") {
    return (
      <svg {...common}>
        <path d="M18.5 5H7l6.3 7L7 19h11.5" />
      </svg>
    );
  }

  if (type === "graph") {
    return (
      <svg {...common}>
        <circle cx="6" cy="6" r="2" />
        <circle cx="18" cy="7" r="2" />
        <circle cx="9" cy="18" r="2" />
        <circle cx="18" cy="17" r="2" />
        <path d="m7.7 7.1 8.6-1.2M7.2 7.6l.9 8.3M10.8 17.2l5.3-1.1M17.2 8.8l.7 6.1" />
      </svg>
    );
  }

  if (type === "string") {
    return (
      <svg {...common}>
        <path d="M5 7h14M5 12h10M5 17h7" />
        <path d="M18 14.5v5M15.5 17h5" />
      </svg>
    );
  }

  if (type === "image") {
    return (
      <svg {...common}>
        <rect x="4" y="4" width="16" height="16" rx="2" />
        <circle cx="9" cy="9" r="1.5" />
        <path d="m5.5 18 5-5 3.5 3 2-2 2.5 2.5" />
      </svg>
    );
  }

  if (type === "number") {
    return (
      <svg {...common}>
        <circle cx="12" cy="12" r="8.5" />
        <path d="M9 8.5h5M9 12h5M9 15.5h5" />
        <path d="M12 7v10" />
      </svg>
    );
  }

  if (type === "database") {
    return (
      <svg {...common}>
        <ellipse cx="12" cy="6.5" rx="7" ry="3" />
        <path d="M5 6.5v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5" />
        <path d="M5 11.5v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5" />
      </svg>
    );
  }

  return (
    <svg {...common}>
      <path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14" />
    </svg>
  );
}

function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function formatTime(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatNumber(value, decimals = 2) {
  if (value === null || value === undefined || value === "") return "—";
  const number = Number(value);
  if (!Number.isFinite(number)) return "—";
  return number.toLocaleString("en-IN", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

function formatInputSize(value) {
  if (value === null || value === undefined || value === "") return "—";
  const number = Number(value);
  if (!Number.isFinite(number)) return String(value);
  return number.toLocaleString("en-IN");
}

function formatAnalysisType(value) {
  if (!value) return "—";
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function getScoreNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function getScoreTone(score) {
  if (score === null) {
    return {
      wrapper: "bg-[#F4F6F4] border-[#E4E9E5]",
      text: "text-[#69746D]",
    };
  }

  if (score >= 75) {
    return {
      wrapper: "bg-[#DDF4E1] border-[#C3E8CA]",
      text: "text-[#147334]",
    };
  }

  if (score >= 60) {
    return {
      wrapper: "bg-[#FFF4D6] border-[#F3E3AC]",
      text: "text-[#A56A00]",
    };
  }

  return {
    wrapper: "bg-[#FFF0EE] border-[#F5D1CB]",
    text: "text-[#C4473B]",
  };
}

function StatCard({ icon, title, value, subtitle, iconClass = "" }) {
  return (
    <div className="min-w-0 rounded-2xl border border-[#E2EAE4] bg-white px-5 py-4 shadow-[0_5px_18px_rgba(15,23,42,0.035)]">
      <div className="flex items-center gap-4">
        <div
          className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-[#E7F5EA] text-[#0B6B2B] ${iconClass}`}
        >
          <Icon name={icon} size={22} strokeWidth={1.9} />
        </div>

        <div className="min-w-0">
          <p className="text-xs font-medium text-[#66736B]">{title}</p>
          <p className="mt-0.5 text-[25px] font-bold leading-tight tracking-[-0.02em] text-[#101A15]">
            {value}
          </p>
          <p className="mt-1 truncate text-[11px] text-[#78847D]">
            {subtitle}
          </p>
        </div>
      </div>
    </div>
  );
}

function FilterSelect({ value, onChange, children, ariaLabel }) {
  return (
    <div className="relative min-w-[145px]">
      <select
        value={value}
        onChange={onChange}
        aria-label={ariaLabel}
        className="h-11 w-full appearance-none rounded-xl border border-[#DFE8E1] bg-white px-4 pr-10 text-sm font-medium text-[#1D2922] outline-none transition focus:border-[#0B6B2B] focus:ring-2 focus:ring-[#0B6B2B]/10"
      >
        {children}
      </select>
      <Icon
        name="chevronDown"
        size={16}
        className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-[#66736B]"
      />
    </div>
  );
}

function DateFilter({ value, onChange, placeholder }) {
  return (
    <div className="relative min-w-[142px]">
      <input
        type="date"
        value={value}
        onChange={onChange}
        aria-label={placeholder}
        className="h-11 w-full rounded-xl border border-[#DFE8E1] bg-white px-4 pr-10 text-sm font-medium text-[#34433A] outline-none transition focus:border-[#0B6B2B] focus:ring-2 focus:ring-[#0B6B2B]/10"
      />
      {!value && (
        <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 bg-white pr-1 text-sm text-[#8B968F]">
          {placeholder}
        </span>
      )}
      <Icon
        name="calendar"
        size={16}
        className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-[#6F7C74]"
      />
    </div>
  );
}

function ScoreBadge({ score, greenest = false }) {
  const numericScore = getScoreNumber(score);
  const tone = getScoreTone(numericScore);

  if (numericScore === null) {
    return (
      <span className="inline-flex min-w-[58px] items-center justify-center rounded-lg border bg-[#F4F6F4] px-2.5 py-1.5 text-xs font-semibold text-[#69746D]">
        —
      </span>
    );
  }

  return (
    <div className="flex flex-wrap items-center gap-1.5">
      <span
        className={`inline-flex min-w-[58px] items-center justify-center rounded-lg border px-2.5 py-1.5 text-xs font-bold ${tone.wrapper} ${tone.text}`}
      >
        {numericScore.toFixed(1)}
      </span>
      {greenest && (
        <span className="inline-flex items-center gap-1 rounded-full border border-[#B8E2C1] bg-[#E6F7E9] px-2 py-1 text-[10px] font-bold uppercase tracking-[0.05em] text-[#16743A]">
          <Icon name="leaf" size={11} strokeWidth={2} />
          Greenest
        </span>
      )}
    </div>
  );
}

function StatusBadge({ verified }) {
  return verified ? (
    <span className="inline-flex items-center gap-1.5 rounded-lg border border-[#D3E9D7] bg-[#EFF9F1] px-2.5 py-1.5 text-xs font-semibold text-[#237A3E]">
      <span className="flex h-4 w-4 items-center justify-center rounded-full bg-[#2F9B50] text-white">
        <Icon name="check" size={10} strokeWidth={2.5} />
      </span>
      Verified
    </span>
  ) : (
    <span className="inline-flex items-center gap-1.5 rounded-lg border border-[#F1D3CE] bg-[#FFF3F1] px-2.5 py-1.5 text-xs font-semibold text-[#C4473B]">
      <span className="flex h-4 w-4 items-center justify-center rounded-full bg-[#E55B4F] text-white">
        <Icon name="x" size={10} strokeWidth={2.5} />
      </span>
      Not Verified
    </span>
  );
}

function DetailCard({ label, value }) {
  return (
    <div className="rounded-xl border border-[#E4EBE5] bg-[#F9FBF9] p-4">
      <p className="text-[11px] font-medium uppercase tracking-[0.08em] text-[#77827B]">
        {label}
      </p>
      <p className="mt-1.5 break-words text-sm font-semibold text-[#142019]">
        {value}
      </p>
    </div>
  );
}

function MetricCard({ icon, label, value }) {
  return (
    <div className="rounded-xl border border-[#E4EBE5] bg-white p-4 shadow-[0_3px_12px_rgba(15,23,42,0.025)]">
      <div className="flex items-center gap-2 text-[#557064]">
        <Icon name={icon} size={16} />
        <p className="text-xs font-medium">{label}</p>
      </div>
      <p className="mt-2 text-lg font-bold text-[#132019]">{value}</p>
    </div>
  );
}

export default function History() {
  const [search, setSearch] = useState("");
  const [history, setHistory] = useState([]);

  const [benchmarkFilter, setBenchmarkFilter] = useState("all");
  const [languageFilter, setLanguageFilter] = useState("all");
  const [typeFilter, setTypeFilter] = useState("all");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [sortBy, setSortBy] = useState("latest");

  const [currentPage, setCurrentPage] = useState(1);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState("");

  // Temporary user ID until authentication/user context is connected.
  const userId = 1;

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get(`/history/user/${userId}`);
        setHistory(response.data.items || []);
      } catch (err) {
        console.error("Failed to fetch benchmark history:", err);
        setError("Unable to load benchmark history.");
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const benchmarkOptions = useMemo(() => {
    return [...new Set(history.map((item) => item.benchmark_name).filter(Boolean))].sort(
      (a, b) => a.localeCompare(b)
    );
  }, [history]);

  const languageOptions = useMemo(() => {
    return [...new Set(history.map((item) => item.language).filter(Boolean))].sort(
      (a, b) => a.localeCompare(b)
    );
  }, [history]);

  const typeOptions = useMemo(() => {
    return [...new Set(history.map((item) => item.analysis_type).filter(Boolean))].sort(
      (a, b) => a.localeCompare(b)
    );
  }, [history]);

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();

    const result = history.filter((item) => {
      const matchesQuery =
        !query ||
        [
          item.benchmark_name,
          item.category,
          item.language,
          item.analysis_type,
          item.workload_type,
          item.created_at,
        ]
          .filter(Boolean)
          .some((value) => String(value).toLowerCase().includes(query));

      const matchesBenchmark =
        benchmarkFilter === "all" || item.benchmark_name === benchmarkFilter;

      const matchesLanguage =
        languageFilter === "all" || item.language === languageFilter;

      const matchesType =
        typeFilter === "all" || item.analysis_type === typeFilter;

      const createdAt = item.created_at ? new Date(item.created_at) : null;
      const validDate = createdAt && !Number.isNaN(createdAt.getTime());

      const matchesStart =
        !startDate ||
        (validDate && createdAt >= new Date(`${startDate}T00:00:00`));

      const matchesEnd =
        !endDate ||
        (validDate && createdAt <= new Date(`${endDate}T23:59:59.999`));

      return (
        matchesQuery &&
        matchesBenchmark &&
        matchesLanguage &&
        matchesType &&
        matchesStart &&
        matchesEnd
      );
    });

    result.sort((a, b) => {
      if (sortBy === "oldest") {
        return new Date(a.created_at || 0) - new Date(b.created_at || 0);
      }

      if (sortBy === "name-asc") {
        return String(a.benchmark_name || "").localeCompare(
          String(b.benchmark_name || "")
        );
      }

      if (sortBy === "name-desc") {
        return String(b.benchmark_name || "").localeCompare(
          String(a.benchmark_name || "")
        );
      }

      if (sortBy === "score-desc") {
        return (
          (getScoreNumber(b.green_score) ?? -Infinity) -
          (getScoreNumber(a.green_score) ?? -Infinity)
        );
      }

      return new Date(b.created_at || 0) - new Date(a.created_at || 0);
    });

    return result;
  }, [
    history,
    search,
    benchmarkFilter,
    languageFilter,
    typeFilter,
    startDate,
    endDate,
    sortBy,
  ]);

  useEffect(() => {
    setCurrentPage(1);
  }, [
    search,
    benchmarkFilter,
    languageFilter,
    typeFilter,
    startDate,
    endDate,
    sortBy,
  ]);

  const greenestScore = useMemo(() => {
    const scores = filtered
      .map((item) => getScoreNumber(item.green_score))
      .filter((score) => score !== null);

    return scores.length ? Math.max(...scores) : null;
  }, [filtered]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));

  const visibleRows = useMemo(() => {
    const start = (currentPage - 1) * PAGE_SIZE;
    return filtered.slice(start, start + PAGE_SIZE);
  }, [filtered, currentPage]);

  const totalExecutions = history.length;

  const benchmarkCount = useMemo(
    () =>
      new Set(
        history.map((item) => item.benchmark_name).filter(Boolean)
      ).size,
    [history]
  );

  const languageCount = useMemo(
    () =>
      new Set(history.map((item) => item.language).filter(Boolean)).size,
    [history]
  );

  const verifiedCount = useMemo(
    () => history.filter((item) => item.output_verified === true).length,
    [history]
  );

  const verifiedPercentage = totalExecutions
    ? ((verifiedCount / totalExecutions) * 100).toFixed(1)
    : "0.0";

  const clearFilters = () => {
    setSearch("");
    setBenchmarkFilter("all");
    setLanguageFilter("all");
    setTypeFilter("all");
    setStartDate("");
    setEndDate("");
    setSortBy("latest");
    setCurrentPage(1);
  };

  const handleView = async (analysisId) => {
    try {
      setDetailLoading(true);
      setDetailError("");
      setSelectedAnalysis(null);

      const response = await api.get(`/history/${analysisId}`);
      setSelectedAnalysis(response.data);
    } catch (err) {
      console.error("Failed to fetch analysis details:", err);
      setDetailError("Unable to load analysis details.");
    } finally {
      setDetailLoading(false);
    }
  };

  const handleCloseDetails = () => {
    setSelectedAnalysis(null);
    setDetailError("");
  };

  useEffect(() => {
    const onKeyDown = (event) => {
      if (event.key === "Escape" && selectedAnalysis) {
        handleCloseDetails();
      }
    };

    if (selectedAnalysis) {
      window.addEventListener("keydown", onKeyDown);
    }

    return () => window.removeEventListener("keydown", onKeyDown);
  }, [selectedAnalysis]);

  return (
    <div className="min-h-screen bg-[#F9FAFA] text-[#0F172A] px-6 py-8 md:px-10">
        {/* PAGE HEADER — same placement and dimensions as Reports */}
        <div className="mb-7 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 -mt-20">
          <div className="min-w-0">
            <div className="text-[11px] font-bold tracking-[0.22em] text-[#0B6B2B]">
              HISTORY
            </div>

            <h1 className="mt-2 text-[32px] leading-[1.1] font-bold tracking-[-0.02em] text-[#0F172A]">
              Execution History
            </h1>

            <p className="mt-2 text-[13px] leading-5 text-[#526174]">
              Track and review your past benchmark executions.
            </p>
          </div>

          {/* Same right-side banner placement as Reports */}
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

        {/* QUICK STATS — same sizing/layout as Reports */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3 -translate-y-5 -mt-3">

          {/* TOTAL EXECUTIONS */}
          <div className="rounded-2xl border border-[#E3EAE4] bg-white p-5 shadow-[0_4px_20px_rgba(15,23,42,0.04)] hover:-translate-y-0.5 hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)] transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[#526174] text-sm font-medium">
                  Total Executions
                </p>
                <h2 className="mt-2 text-3xl font-bold text-[#0F172A]">
                  {totalExecutions.toLocaleString("en-IN")}
                </h2>
              </div>

              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#EAF6EC] text-[#16803C]">
                <Icon name="play" size={21} strokeWidth={1.8} />
              </div>
            </div>

            <p className="mt-4 text-[11px] text-[#94A3B8]">
              All benchmark executions
            </p>
          </div>

          {/* BENCHMARKS RUN */}
          <div className="rounded-2xl border border-[#E3EAE4] bg-white p-5 shadow-[0_4px_20px_rgba(15,23,42,0.04)] hover:-translate-y-0.5 hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)] transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[#526174] text-sm font-medium">
                  Benchmarks Run
                </p>
                <h2 className="mt-2 text-3xl font-bold text-[#0F172A]">
                  {benchmarkCount.toLocaleString("en-IN")}
                </h2>
              </div>

              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#EAF6EC] text-[#16803C]">
                <Icon name="layers" size={21} strokeWidth={1.8} />
              </div>
            </div>

            <p className="mt-4 text-[11px] text-[#94A3B8]">
              Distinct benchmark workloads
            </p>
          </div>

          {/* LANGUAGES USED */}
          <div className="rounded-2xl border border-[#E3EAE4] bg-white p-5 shadow-[0_4px_20px_rgba(15,23,42,0.04)] hover:-translate-y-0.5 hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)] transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[#526174] text-sm font-medium">
                  Languages Used
                </p>
                <h2 className="mt-2 text-3xl font-bold text-[#0F172A]">
                  {languageCount.toLocaleString("en-IN")}
                </h2>
              </div>

              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#EAF6EC] text-[#16803C]">
                <Icon name="code" size={21} strokeWidth={1.8} />
              </div>
            </div>

            <p className="mt-4 truncate text-[11px] text-[#94A3B8]">
              {languageCount
                ? `${languageOptions.slice(0, 4).join(", ")}${languageCount > 4 ? " + more" : ""}`
                : "No executions yet"}
            </p>
          </div>

          {/* VERIFIED RUNS */}
          <div className="rounded-2xl border border-[#E3EAE4] bg-white p-5 shadow-[0_4px_20px_rgba(15,23,42,0.04)] hover:-translate-y-0.5 hover:shadow-[0_8px_28px_rgba(15,23,42,0.07)] transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[#526174] text-sm font-medium">
                  Verified Runs
                </p>
                <h2 className="mt-2 text-3xl font-bold text-[#0F172A]">
                  {verifiedCount.toLocaleString("en-IN")}
                </h2>
              </div>

              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#EAF6EC] text-[#16803C]">
                <Icon name="check" size={21} strokeWidth={1.9} />
              </div>
            </div>

            <p className="mt-4 text-[11px] text-[#94A3B8]">
              {verifiedPercentage}% output verified
            </p>
          </div>
        </div>

        {/* =====================================================
            FILTER BAR
        ====================================================== */}
        <div className="mb-5 rounded-2xl border border-[#E1E9E3] bg-white p-3 shadow-[0_4px_18px_rgba(15,23,42,0.03)]">
          <div className="flex flex-col gap-2.5 xl:flex-row xl:items-center">
            <div className="relative min-w-0 flex-1">
              <Icon
                name="search"
                size={18}
                className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-[#4C7A5C]"
              />
              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search by benchmark, language or keywords..."
                className="h-11 w-full rounded-xl border border-[#DFE8E1] bg-white pl-11 pr-4 text-sm text-[#152119] outline-none transition placeholder:text-[#8B968F] focus:border-[#0B6B2B] focus:ring-2 focus:ring-[#0B6B2B]/10"
              />
            </div>

            <FilterSelect
              value={benchmarkFilter}
              onChange={(event) => setBenchmarkFilter(event.target.value)}
              ariaLabel="Filter by benchmark"
            >
              <option value="all">All Benchmarks</option>
              {benchmarkOptions.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </FilterSelect>

            <FilterSelect
              value={languageFilter}
              onChange={(event) => setLanguageFilter(event.target.value)}
              ariaLabel="Filter by language"
            >
              <option value="all">All Languages</option>
              {languageOptions.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </FilterSelect>

            <FilterSelect
              value={typeFilter}
              onChange={(event) => setTypeFilter(event.target.value)}
              ariaLabel="Filter by analysis type"
            >
              <option value="all">All Types</option>
              {typeOptions.map((type) => (
                <option key={type} value={type}>
                  {formatAnalysisType(type)}
                </option>
              ))}
            </FilterSelect>

            <DateFilter
              value={startDate}
              onChange={(event) => setStartDate(event.target.value)}
              placeholder="From Date"
            />

            <DateFilter
              value={endDate}
              onChange={(event) => setEndDate(event.target.value)}
              placeholder="To Date"
            />

            <button
              type="button"
              onClick={clearFilters}
              className="h-11 shrink-0 rounded-xl bg-[#0B6B2B] px-5 text-sm font-semibold text-white shadow-sm transition hover:bg-[#095A24] focus:outline-none focus:ring-2 focus:ring-[#0B6B2B]/20"
            >
              Clear
            </button>
          </div>
        </div>

        {/* =====================================================
            HISTORY TABLE
        ====================================================== */}
        <div className="rounded-2xl border border-[#DDE7DF] bg-white shadow-[0_2px_12px_rgba(15,23,42,0.04)] overflow-hidden">
          <div className="px-5 py-5 border-b border-[#E2EAE4]">
            <div>
              <h2 className="text-[17px] font-bold text-[#0F172A]">
                Execution History
              </h2>
              <p className="mt-1 text-[12px] text-[#526174]">
                {filtered.length === history.length
                  ? `${history.length.toLocaleString("en-IN")} executions recorded`
                  : `${filtered.length.toLocaleString("en-IN")} executions match your filters`}
              </p>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-[#78847D]">Sort by</span>
              <div className="relative">
                <select
                  value={sortBy}
                  onChange={(event) => setSortBy(event.target.value)}
                  className="h-9 appearance-none rounded-lg border border-[#DFE8E1] bg-white px-3 pr-8 text-xs font-semibold text-[#304037] outline-none focus:border-[#0B6B2B]"
                  aria-label="Sort execution history"
                >
                  <option value="latest">Latest First</option>
                  <option value="oldest">Oldest First</option>
                  <option value="name-asc">Name A-Z</option>
                  <option value="name-desc">Name Z-A</option>
                  <option value="score-desc">Highest Green Score</option>
                </select>
                <Icon
                  name="chevronDown"
                  size={14}
                  className="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 text-[#65736A]"
                />
              </div>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full min-w-[1100px] border-collapse text-sm">
              <thead className="bg-[#EAF6EC]">
                <tr className="border-b border-[#DDE9DF] text-[#315143]">
                  <th className="w-12 px-5 py-3.5 text-center text-[11px] font-bold text-[#526174]">
                    #
                  </th>
                  <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                    Benchmark
                  </th>
                  <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                    Language
                  </th>
                  <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                    Input Size
                  </th>
                  <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                    Execution Time
                  </th>
                  <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                    Memory Usage
                  </th>
                  <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                    Energy (J)
                  </th>
                  <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                    Green Score
                  </th>
                  <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                    Status
                  </th>
                  <th className="px-5 py-3.5 text-left text-[11px] font-bold text-[#526174]">
                    Executed On
                  </th>
                  <th className="px-5 py-3.5 text-center text-[11px] font-bold text-[#526174]">
                    Actions
                  </th>
                </tr>
              </thead>

              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={11} className="py-20 text-center">
                      <div className="flex flex-col items-center justify-center gap-3 text-[#748078]">
                        <div className="h-8 w-8 animate-spin rounded-full border-2 border-[#D6E8DA] border-t-[#0B6B2B]" />
                        <span className="text-sm font-medium">
                          Loading benchmark history...
                        </span>
                      </div>
                    </td>
                  </tr>
                ) : visibleRows.length > 0 ? (
                  visibleRows.map((item, index) => {
                    const visual = getBenchmarkVisual(
                      item.benchmark_name,
                      item.category
                    );

                    const absoluteIndex =
                      (currentPage - 1) * PAGE_SIZE + index + 1;

                    const isGreenest =
                      greenestScore !== null &&
                      getScoreNumber(item.green_score) === greenestScore;

                    return (
                      <tr
                        key={item.analysis_id}
                        className="border-b border-[#E7ECE8] last:border-b-0 hover:bg-[#F8FCF9] transition-colors"
                      >
                        <td className="px-5 py-4 text-center text-xs font-semibold text-[#88928C]">
                          {absoluteIndex}
                        </td>

                        <td className="px-5 py-4">
                          <div className="flex min-w-[220px] items-center gap-3">
                            <div
                              className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border ${visual.bg} ${visual.text} ${visual.border}`}
                            >
                              <BenchmarkGlyph type={visual.icon} size={19} />
                            </div>

                            <div className="min-w-0">
                              <p className="truncate text-[13px] font-bold text-[#152119]">
                                {item.benchmark_name || "Custom Benchmark"}
                              </p>
                              <p className="mt-0.5 truncate text-[11px] text-[#7A867F]">
                                {item.category || "Custom"}
                              </p>
                            </div>
                          </div>
                        </td>

                        <td className="px-5 py-4">
                          <span className="inline-flex rounded-lg border border-[#DDE7E0] bg-[#F8FAF8] px-2.5 py-1.5 text-xs font-semibold text-[#405047]">
                            {item.language || "—"}
                          </span>
                        </td>

                        <td className="px-5 py-4 text-xs font-medium text-[#45534B]">
                          {formatInputSize(item.input_size)}
                        </td>

                        <td className="px-5 py-4 text-xs font-semibold text-[#34443A]">
                          {item.execution_time !== null &&
                          item.execution_time !== undefined
                            ? `${formatNumber(item.execution_time)} ms`
                            : "—"}
                        </td>

                        <td className="px-5 py-4 text-xs font-medium text-[#4C5B52]">
                          {item.memory_usage !== null &&
                          item.memory_usage !== undefined
                            ? `${formatNumber(item.memory_usage)} MB`
                            : "—"}
                        </td>

                        <td className="px-5 py-4 text-xs font-semibold text-[#34443A]">
                          {item.energy_consumption !== null &&
                          item.energy_consumption !== undefined
                            ? formatNumber(item.energy_consumption, 2)
                            : "—"}
                        </td>

                        <td className="px-5 py-4">
                          <ScoreBadge
                            score={item.green_score}
                            greenest={isGreenest}
                          />
                        </td>

                        <td className="px-5 py-4">
                          <StatusBadge verified={item.output_verified === true} />
                        </td>

                        <td className="px-5 py-4">
                          <div className="whitespace-nowrap">
                            <p className="text-xs font-semibold text-[#425047]">
                              {formatDate(item.created_at)}
                            </p>
                            <p className="mt-0.5 text-[11px] text-[#8A958F]">
                              {formatTime(item.created_at)}
                            </p>
                          </div>
                        </td>

                        <td className="px-5 py-4">
                          <div className="flex items-center justify-center gap-1.5">
                            <button
                              type="button"
                              onClick={() => handleView(item.analysis_id)}
                              className="inline-flex items-center gap-1.5 rounded-lg border border-[#BFD7C5] bg-white px-3 py-1.5 text-xs font-semibold text-[#176D36] transition hover:border-[#0B6B2B] hover:bg-[#0B6B2B] hover:text-white focus:outline-none focus:ring-2 focus:ring-[#0B6B2B]/15"
                              aria-label={`View ${item.benchmark_name || "benchmark"} execution`}
                            >
                              <Icon name="eye" size={15} strokeWidth={1.9} />
                              View
                            </button>

                            <button
                              type="button"
                              onClick={() => handleView(item.analysis_id)}
                              className="flex h-8 w-8 items-center justify-center rounded-lg text-[#78847D] transition hover:bg-[#EFF6F0] hover:text-[#0B6B2B]"
                              aria-label={`More actions for analysis ${item.analysis_id}`}
                              title="View execution details"
                            >
                              <Icon name="more" size={17} strokeWidth={1.7} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td colSpan={11} className="py-20 text-center">
                      <div className="mx-auto flex max-w-sm flex-col items-center">
                        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[#EAF6EC] text-[#238144]">
                          <Icon name="search" size={24} />
                        </div>
                        <p className="mt-4 text-sm font-bold text-[#26342C]">
                          {search ||
                          benchmarkFilter !== "all" ||
                          languageFilter !== "all" ||
                          typeFilter !== "all" ||
                          startDate ||
                          endDate
                            ? "No executions match these filters."
                            : "No benchmark history available."}
                        </p>
                        <p className="mt-1 text-xs text-[#7A867F]">
                          {history.length
                            ? "Try clearing a filter or changing your search."
                            : "Run a benchmark to start building your execution history."}
                        </p>
                        {(search ||
                          benchmarkFilter !== "all" ||
                          languageFilter !== "all" ||
                          typeFilter !== "all" ||
                          startDate ||
                          endDate) && (
                          <button
                            type="button"
                            onClick={clearFilters}
                            className="mt-4 rounded-lg bg-[#0B6B2B] px-4 py-2 text-xs font-semibold text-white hover:bg-[#095A24]"
                          >
                            Clear Filters
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* =====================================================
              PAGINATION
          ====================================================== */}
          {!loading && filtered.length > 0 && (
            <div className="flex flex-col gap-3 border-t border-[#E4EBE5] px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-xs text-[#748078]">
                Showing{" "}
                <span className="font-semibold text-[#445149]">
                  {(currentPage - 1) * PAGE_SIZE + 1}
                </span>{" "}
                to{" "}
                <span className="font-semibold text-[#445149]">
                  {Math.min(currentPage * PAGE_SIZE, filtered.length)}
                </span>{" "}
                of{" "}
                <span className="font-semibold text-[#445149]">
                  {filtered.length}
                </span>{" "}
                executions
              </p>

              <div className="flex items-center gap-1.5">
                <button
                  type="button"
                  disabled={currentPage === 1}
                  onClick={() => setCurrentPage((page) => Math.max(1, page - 1))}
                  className="flex h-8 w-8 items-center justify-center rounded-lg border border-[#DCE6DF] bg-white text-[#647169] transition hover:bg-[#F2F8F3] disabled:cursor-not-allowed disabled:opacity-40"
                  aria-label="Previous page"
                >
                  <Icon name="chevronLeft" size={15} />
                </button>

                {Array.from({ length: totalPages }, (_, index) => index + 1)
                  .slice(
                    Math.max(0, currentPage - 3),
                    Math.min(totalPages, currentPage + 2)
                  )
                  .map((page) => (
                    <button
                      type="button"
                      key={page}
                      onClick={() => setCurrentPage(page)}
                      className={`flex h-8 min-w-8 items-center justify-center rounded-lg border px-2 text-xs font-semibold transition ${
                        page === currentPage
                          ? "border-[#0B6B2B] bg-[#0B6B2B] text-white"
                          : "border-[#DCE6DF] bg-white text-[#59665E] hover:bg-[#F2F8F3]"
                      }`}
                    >
                      {page}
                    </button>
                  ))}

                <button
                  type="button"
                  disabled={currentPage === totalPages}
                  onClick={() =>
                    setCurrentPage((page) => Math.min(totalPages, page + 1))
                  }
                  className="flex h-8 w-8 items-center justify-center rounded-lg border border-[#DCE6DF] bg-white text-[#647169] transition hover:bg-[#F2F8F3] disabled:cursor-not-allowed disabled:opacity-40"
                  aria-label="Next page"
                >
                  <Icon name="chevronRight" size={15} />
                </button>
              </div>
            </div>
          )}
        </div>
  
      {/* =====================================================
          DETAIL LOADING
      ====================================================== */}
      {detailLoading && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center bg-[#102016]/35 px-4 backdrop-blur-sm">
          <div className="flex items-center gap-3 rounded-2xl border border-[#DDE7DF] bg-white px-6 py-5 text-sm font-semibold text-[#4D5A52] shadow-[0_20px_60px_rgba(15,23,42,0.18)]">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-[#D8E9DC] border-t-[#0B6B2B]" />
            Loading execution details...
          </div>
        </div>
      )}

      {/* =====================================================
          DETAIL ERROR
      ====================================================== */}
      {detailError && (
        <div className="fixed bottom-6 right-6 z-[80] max-w-sm rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm font-medium text-red-700 shadow-xl">
          <div className="flex items-start gap-3">
            <Icon name="x" size={18} className="mt-0.5 shrink-0" />
            <span>{detailError}</span>
            <button
              type="button"
              onClick={() => setDetailError("")}
              className="ml-2 text-red-500 hover:text-red-800"
              aria-label="Dismiss error"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* =====================================================
          EXECUTION DETAIL MODAL
      ====================================================== */}
      {selectedAnalysis && (
        <div
          className="fixed inset-0 z-[60] flex items-center justify-center bg-[#102016]/45 px-4 py-7 backdrop-blur-sm"
          onClick={handleCloseDetails}
        >
          <div
            className="max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-3xl border border-[#DCE7DF] bg-white shadow-[0_25px_80px_rgba(15,23,42,0.22)]"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="sticky top-0 z-10 flex items-start justify-between gap-5 border-b border-[#E4EBE5] bg-white/95 px-6 py-5 backdrop-blur sm:px-7">
              <div className="flex min-w-0 items-center gap-4">
                {(() => {
                  const visual = getBenchmarkVisual(
                    selectedAnalysis.benchmark_name,
                    selectedAnalysis.category
                  );

                  return (
                    <div
                      className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border ${visual.bg} ${visual.text} ${visual.border}`}
                    >
                      <BenchmarkGlyph type={visual.icon} size={24} />
                    </div>
                  );
                })()}

                <div className="min-w-0">
                  <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#0B6B2B]">
                    Execution Details
                  </p>
                  <h2 className="mt-1 truncate text-xl font-bold text-[#111C16] sm:text-2xl">
                    {selectedAnalysis.benchmark_name || "Custom Benchmark"}
                  </h2>
                  <p className="mt-0.5 text-xs text-[#6E7A72]">
                    {selectedAnalysis.language || "Unknown language"} · Analysis #
                    {selectedAnalysis.analysis_id}
                  </p>
                </div>
              </div>

              <button
                type="button"
                onClick={handleCloseDetails}
                className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-[#68756D] transition hover:bg-[#F1F5F2] hover:text-[#17231C]"
                aria-label="Close execution details"
              >
                <Icon name="close" size={19} />
              </button>
            </div>

            <div className="p-6 sm:p-7">
              <div className="mb-6">
                <div className="mb-3 flex items-center justify-between gap-3">
                  <h3 className="text-sm font-bold text-[#243229]">
                    Benchmark Information
                  </h3>
                  <StatusBadge
                    verified={selectedAnalysis.output_verified === true}
                  />
                </div>

                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                  <DetailCard
                    label="Category"
                    value={selectedAnalysis.category || "Not available"}
                  />
                  <DetailCard
                    label="Analysis Type"
                    value={formatAnalysisType(selectedAnalysis.analysis_type)}
                  />
                  <DetailCard
                    label="Input Size"
                    value={formatInputSize(selectedAnalysis.input_size)}
                  />
                  <DetailCard
                    label="Benchmark Size"
                    value={selectedAnalysis.bench_size || "Not available"}
                  />
                </div>
              </div>

              <div className="mb-6">
                <h3 className="mb-3 text-sm font-bold text-[#243229]">
                  Performance Metrics
                </h3>

                <div className="grid gap-3 sm:grid-cols-3">
                  <MetricCard
                    icon="clock"
                    label="Execution Time"
                    value={
                      selectedAnalysis.execution_time !== null &&
                      selectedAnalysis.execution_time !== undefined
                        ? `${formatNumber(
                            selectedAnalysis.execution_time
                          )} ms`
                        : "Not available"
                    }
                  />

                  <MetricCard
                    icon="code"
                    label="CPU Usage"
                    value={
                      selectedAnalysis.cpu_usage !== null &&
                      selectedAnalysis.cpu_usage !== undefined
                        ? `${formatNumber(selectedAnalysis.cpu_usage)} %`
                        : "Not available"
                    }
                  />

                  <MetricCard
                    icon="memory"
                    label="Memory Usage"
                    value={
                      selectedAnalysis.memory_usage !== null &&
                      selectedAnalysis.memory_usage !== undefined
                        ? `${formatNumber(selectedAnalysis.memory_usage)} MB`
                        : "Not available"
                    }
                  />
                </div>
              </div>

              <div className="mb-6">
                <h3 className="mb-3 text-sm font-bold text-[#243229]">
                  Sustainability Metrics
                </h3>

                <div className="grid gap-3 sm:grid-cols-3">
                  <MetricCard
                    icon="bolt"
                    label="Energy Consumption"
                    value={
                      selectedAnalysis.energy_consumption !== null &&
                      selectedAnalysis.energy_consumption !== undefined
                        ? `${formatNumber(
                            selectedAnalysis.energy_consumption,
                            4
                          )} J`
                        : "Not available"
                    }
                  />

                  <MetricCard
                    icon="leaf"
                    label="Green Score"
                    value={
                      selectedAnalysis.green_score !== null &&
                      selectedAnalysis.green_score !== undefined
                        ? `${formatNumber(selectedAnalysis.green_score)} / 100`
                        : "Not available"
                    }
                  />

                  <MetricCard
                    icon="leaf"
                    label="Green Score Label"
                    value={selectedAnalysis.green_score_label || "Not available"}
                  />
                </div>
              </div>

              <div className="rounded-2xl border border-[#DDE8DF] bg-[#F7FBF8] p-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p className="text-sm font-bold text-[#243229]">
                      Execution Validation
                    </p>
                    <p className="mt-1 text-xs text-[#758179]">
                      Stored result from this benchmark execution.
                    </p>
                  </div>

                  <StatusBadge
                    verified={selectedAnalysis.output_verified === true}
                  />
                </div>

                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  <DetailCard
                    label="Executed On"
                    value={`${formatDate(
                      selectedAnalysis.created_at
                    )} ${formatTime(selectedAnalysis.created_at)}`}
                  />
                  <DetailCard
                    label="Workload Type"
                    value={selectedAnalysis.workload_type || "Not available"}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>

  );
  
}
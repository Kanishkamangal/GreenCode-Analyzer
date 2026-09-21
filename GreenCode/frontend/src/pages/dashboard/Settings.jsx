import { useState } from "react";

export default function Settings() {
  const [notifications, setNotifications] = useState(true);
  const [autoReport, setAutoReport] = useState(true);
  const [saveHistory, setSaveHistory] = useState(true);

  return (
    <div className="min-h-screen bg-[#F9FAFA] text-[#0F172A] px-6 py-8 md:px-10">

      {/* =================================================
          HEADER
      ================================================= */}

      <div className="mb-8">

        <p className="
          text-[#0B6B2B]
          text-xs
          uppercase
          tracking-[0.25em]
          font-semibold
        ">
          Preferences
        </p>

        <h1 className="
          mt-3
          text-3xl
          md:text-4xl
          font-semibold
          text-[#0F172A]
        ">
          Settings
        </h1>

        <p className="mt-2 text-[#526174]">
          Manage your GreenCode Analyzer workspace preferences.
        </p>

      </div>


      {/* =================================================
          GENERAL
      ================================================= */}

      <SettingsSection
        title="General"
        description="Basic workspace preferences."
      >

        <SettingRow
          title="Workspace"
          description="GreenCode Analyzer"
        >

          <span
            className="
              inline-flex
              items-center
              px-3
              py-1.5
              rounded-lg
              bg-[#DFF0E1]
              text-[#0B6B2B]
              text-sm
              font-medium
            "
          >
            Active
          </span>

        </SettingRow>


        <SettingRow
          title="Theme"
          description="Current application appearance."
        >

          <span
            className="
              px-3
              py-1.5
              rounded-lg
              bg-[#EAF6EC]
              border
              border-[#C6E3CB]
              text-sm
              text-[#0B6B2B]
              font-medium
            "
          >
            Light
          </span>

        </SettingRow>

      </SettingsSection>


      {/* =================================================
          BENCHMARK
      ================================================= */}

      <SettingsSection
        title="Benchmark Preferences"
        description="Control how benchmark results are handled."
      >

        <SettingRow
          title="Save Benchmark History"
          description="Keep completed benchmark runs in your history."
        >

          <Toggle
            enabled={saveHistory}
            setEnabled={setSaveHistory}
          />

        </SettingRow>


        <SettingRow
          title="Generate Reports Automatically"
          description="Create a report after a successful benchmark."
        >

          <Toggle
            enabled={autoReport}
            setEnabled={setAutoReport}
          />

        </SettingRow>

      </SettingsSection>


      {/* =================================================
          NOTIFICATIONS
      ================================================= */}

      <SettingsSection
        title="Notifications"
        description="Manage application notifications."
      >

        <SettingRow
          title="Benchmark Notifications"
          description="Show notifications when benchmark execution is complete."
        >

          <Toggle
            enabled={notifications}
            setEnabled={setNotifications}
          />

        </SettingRow>

      </SettingsSection>


      {/* =================================================
          SAVE
      ================================================= */}

      <div className="flex justify-end mt-6">

        <button
          className="
            px-7
            py-3.5
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
          Save Changes
        </button>

      </div>

    </div>
  );
}


/* =========================================================
   SETTINGS SECTION
========================================================= */

function SettingsSection({
  title,
  description,
  children,
}) {
  return (
    <section
      className="
        mb-6
        rounded-2xl
        border
        border-[#E3EAE4]
        bg-white
        overflow-hidden
        shadow-[0_4px_20px_rgba(15,23,42,0.04)]
      "
    >

      {/* SECTION HEADER */}

      <div className="
        px-6
        py-5
        border-b
        border-[#E3EAE4]
        bg-[#FFFFFF]
      ">

        <h2 className="
          text-lg
          font-semibold
          text-[#0F172A]
        ">
          {title}
        </h2>

        <p className="
          mt-1
          text-sm
          text-[#6B7280]
        ">
          {description}
        </p>

      </div>


      {/* SECTION CONTENT */}

      <div className="divide-y divide-[#E3EAE4]">
        {children}
      </div>

    </section>
  );
}


/* =========================================================
   SETTING ROW
========================================================= */

function SettingRow({
  title,
  description,
  children,
}) {
  return (
    <div
      className="
        px-6
        py-5
        flex
        items-center
        justify-between
        gap-6
        hover:bg-[#F7FBF8]
        transition
      "
    >

      <div>

        <h3 className="
          text-sm
          font-medium
          text-[#0F172A]
        ">
          {title}
        </h3>

        <p className="
          mt-1
          text-xs
          text-[#6B7280]
        ">
          {description}
        </p>

      </div>

      {children}

    </div>
  );
}


/* =========================================================
   TOGGLE
========================================================= */

function Toggle({
  enabled,
  setEnabled,
}) {
  return (
    <button
      type="button"
      onClick={() => setEnabled(!enabled)}
      aria-pressed={enabled}
      className={`
        relative
        w-12
        h-6
        rounded-full
        transition-all
        duration-200
        focus:outline-none
        focus:ring-2
        focus:ring-[#0B6B2B]/20
        ${
          enabled
            ? "bg-[#0B6B2B]"
            : "bg-[#D1D5DB]"
        }
      `}
    >

      <span
        className={`
          absolute
          top-1
          w-4
          h-4
          rounded-full
          bg-white
          shadow-sm
          transition-all
          duration-200
          ${
            enabled
              ? "left-7"
              : "left-1"
          }
        `}
      />

    </button>
  );
}
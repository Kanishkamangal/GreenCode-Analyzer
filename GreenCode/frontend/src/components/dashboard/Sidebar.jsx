import {
  NavLink,
  Link,
} from "react-router-dom";

import {
  FiHome,
  FiPlay,
  FiClock,
  FiFileText,
  FiSettings,
  FiChevronLeft,
  FiChevronRight,
  FiArrowLeft,
} from "react-icons/fi";

export default function Sidebar({
  collapsed,
  setCollapsed,
}) {

  const menuItems = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: FiHome,
      exact: true,
    },
    {
      name: "Run Benchmark",
      path: "/dashboard/benchmark",
      icon: FiPlay,
    },
    {
      name: "Benchmark History",
      path: "/dashboard/history",
      icon: FiClock,
    },
    {
      name: "Reports",
      path: "/dashboard/reports",
      icon: FiFileText,
    },
    {
      name: "Settings",
      path: "/dashboard/settings",
      icon: FiSettings,
    },
  ];

  return (
    <aside
      className={`
        fixed
        left-0
        top-20
        z-50
        h-[calc(100vh-80px)]

        ${collapsed ? "w-[88px]" : "w-[270px]"}

        bg-[#D4E8D5]

        border-r
        border-[#C4DCC7]

        transition-all
        duration-300

        flex
        flex-col

        overflow-hidden

        shadow-[10px_0_35px_rgba(0,0,0,0.04)]
      `}
    >

      {/* =====================================================
          NAVIGATION
      ===================================================== */}

      <nav
        className="
          flex-1
          p-4
          pt-6
          space-y-2
          overflow-y-auto
        "
      >

        {menuItems.map((item) => {

          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              replace
              end={item.exact}
              title={collapsed ? item.name : undefined}

              className={({ isActive }) => `

                group
                relative

                flex
                items-center

                ${collapsed ? "justify-center" : "gap-4"}

                px-4
                py-3.5

                rounded-xl

                transition-all
                duration-200

                ${
                  isActive
                    ? `
                      bg-[#3F6B4B]
                      text-white
                      shadow-[0_8px_20px_rgba(63,107,75,.18)]
                    `
                    : `
                      text-[#526174]
                      hover:bg-[#C5DEC9]
                      hover:text-[#1E2A22]
                    `
                }

              `}
            >

              <Icon
                size={20}
                className="shrink-0"
              />

              {!collapsed && (
                <span
                  className="
                    text-sm
                    font-medium
                    whitespace-nowrap
                  "
                >
                  {item.name}
                </span>
              )}

              {/* COLLAPSED TOOLTIP */}

              {collapsed && (
                <span
                  className="
                    pointer-events-none
                    absolute
                    left-[78px]
                    z-50

                    px-3
                    py-2

                    rounded-lg

                    bg-[#1E2A22]
                    text-white

                    text-xs
                    whitespace-nowrap

                    opacity-0
                    translate-x-[-4px]

                    group-hover:opacity-100
                    group-hover:translate-x-0

                    transition-all
                    duration-200
                  "
                >
                  {item.name}
                </span>
              )}

            </NavLink>
          );

        })}

      </nav>


      {/* =====================================================
          SIDEBAR FOOTER
      ===================================================== */}

      <div
        className={`
          border-t
          border-[#C4DCC7]

          ${collapsed ? "p-3" : "p-4"}

          space-y-2
        `}
      >

        {/* =====================================================
            ECO BRANDING
            ===================================================== */}

        {!collapsed && (
          <div
            className="
              relative
              flex
              flex-col
              items-center
              mb-4
            "
          >

            {/* PLANT */}

          <div
            className="
              relative
              z-10
              h-[62px]
              w-full
              flex
              justify-center
              items-end
              pointer-events-none
            "
          >
            <img
              src="/plant.png"
              alt=""
              className="
                w-[100px]
                h-[110px]
                object-contain
                object-bottom
                animate-plant-sway
                origin-bottom
              "
            />
          </div>


            {/* BRANDING CARD */}

                      {/* BRANDING CARD */}

            <div
              className="
                relative
                z-0

                w-full
                min-h-[82px]

                -mt-[10px]

                rounded-[10px]

                bg-[#DDF0E0]

                px-2
                py-3

                flex
                flex-col
                items-center
                justify-center

                text-center
              "
            >
              <div
                className="
                  text-[15px]
                  leading-[1.15]
                  font-bold
                  text-[#155C38]
                "
              >
                Code Smarter
                <br />
                for a Greener Planet
              </div>

              <div
                className="
                  mt-1.5

                  text-[10px]
                  leading-tight
                  font-medium

                  text-[#4D765D]

                  whitespace-nowrap
                "
              >
                Measure. Optimize. Impact.
              </div>
            </div>

          </div>
        )}


        {/* =====================================================
            BACK TO HOME
        ===================================================== */}

        <Link
          to="/"
          title="Back to Home"

          className={`
            group
            relative

            w-full
            h-11

            rounded-xl

            flex
            items-center

            transition

            ${
              collapsed
                ? "justify-center"
                : "gap-3 px-4"
            }

            text-[#526174]

            hover:bg-[#C5DEC9]
            hover:text-[#1E2A22]
          `}
        >

          <FiArrowLeft size={18} />

          {!collapsed && (
            <span
              className="
                text-sm
                font-medium
              "
            >
              Back to Home
            </span>
          )}

          {collapsed && (
            <span
              className="
                pointer-events-none
                absolute
                left-[78px]

                px-3
                py-2

                rounded-lg

                bg-[#1E2A22]
                text-white

                text-xs
                whitespace-nowrap

                opacity-0
                translate-x-[-4px]

                group-hover:opacity-100
                group-hover:translate-x-0

                transition-all
              "
            >
              Back to Home
            </span>
          )}

        </Link>


        {/* =====================================================
            COLLAPSE BUTTON
        ===================================================== */}

        <button
          onClick={() => setCollapsed(!collapsed)}

          className="
            w-full
            h-11

            rounded-xl

            border
            border-[#BFD7C2]

            text-[#526174]

            hover:bg-[#C5DEC9]
            hover:text-[#1E2A22]
            hover:border-[#3F6B4B]

            transition

            flex
            items-center
            justify-center
          "
        >

          {collapsed ? (
            <FiChevronRight size={18} />
          ) : (
            <FiChevronLeft size={18} />
          )}

        </button>

      </div>

    </aside>
  );
}
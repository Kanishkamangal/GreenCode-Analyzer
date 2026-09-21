import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import {
  FiUser,
  FiEdit3,
  FiMessageSquare,
  FiHelpCircle,
  FiLogOut,
  FiChevronDown,
} from "react-icons/fi";

export default function DashboardNavbar() {
  const [profileOpen, setProfileOpen] = useState(false);

  const dropdownRef = useRef(null);
  const navigate = useNavigate();
  const storedUser = JSON.parse(
  localStorage.getItem("user") || "{}"
);

const userName =
  storedUser?.name ||
  storedUser?.user_name ||
  storedUser?.full_name ||
  "User";
  /* =====================================================
     CLOSE DROPDOWN WHEN CLICKING OUTSIDE
  ===================================================== */

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target)
      ) {
        setProfileOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
    };
  }, []);

  /* =====================================================
     MENU ACTION
  ===================================================== */

  const handleMenuClick = (path) => {
    setProfileOpen(false);
    navigate(path);
  };

  /* =====================================================
     LOGOUT
  ===================================================== */

  const handleLogout = () => {
    setProfileOpen(false);

    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("user");

    navigate("/");
  };

  return (
    <header
      className="
        fixed
        top-0
        left-0
        right-0
        z-[60]
        h-20
        bg-[#E6F2E6]
        border-b
        border-[#CFE3D2]
        shadow-[0_4px_20px_rgba(22,101,52,0.06)]
      "
    >
      <div
        className="
          h-full
          flex
          items-center
          justify-between
          px-6
          md:px-8
        "
      >

        {/* =================================================
            LEFT — LOGO
        ================================================= */}

        <button
          onClick={() => navigate("/dashboard")}
          className="
            flex
            items-center
            gap-3
            group
            outline-none
          "
        >

          {/* Logo */}

          <div
            className="
              w-10
              h-10
              rounded-xl
              bg-[#3F6B4B]
              text-white
              flex
              items-center
              justify-center
              font-bold
              text-lg
              shadow-[0_5px_15px_rgba(63,107,75,0.18)]
              group-hover:scale-105
              transition-transform
            "
          >
            G
          </div>

          {/* Brand */}

          <div className="text-left">

            <h1
              className="
                text-lg
                md:text-xl
                font-bold
                text-[#1E2A22]
                leading-tight
              "
            >
              GreenCode
            </h1>

            <p
              className="
                text-[10px]
                md:text-xs
                text-[#526174]
                tracking-[0.18em]
                uppercase
                leading-tight
              "
            >
              Analyzer
            </p>

          </div>

        </button>


        {/* =================================================
            RIGHT — PROFILE
        ================================================= */}

        <div
          ref={dropdownRef}
          className="relative"
        >

          {/* PROFILE BUTTON */}

          <button
            onClick={() => setProfileOpen(!profileOpen)}
            className="
              flex
              items-center
              gap-3
              px-3
              py-2
              rounded-xl
              hover:bg-[#D7EBD9]
              transition-all
              outline-none
            "
          >

            {/* PROFILE ICON */}

            <div
              className="
                w-10
                h-10
                rounded-full
                bg-[#3F6B4B]
                text-white
                flex
                items-center
                justify-center
                shadow-[0_4px_12px_rgba(63,107,75,0.15)]
              "
            >
              <FiUser size={19} />
            </div>

            {/* PROFILE TEXT */}

            <div className="hidden sm:block text-left">

              <p
                className="
                  text-sm
                  font-semibold
                  text-[#1E2A22]
                  leading-tight
                "
              >
                {userName}
              </p>

              <p
                className="
                  text-xs
                  text-[#526174]
                  mt-0.5
                "
              >
                Account
              </p>

            </div>

            <FiChevronDown
              size={16}
              className={`
                text-[#526174]
                transition-transform
                duration-200
                ${profileOpen ? "rotate-180" : ""}
              `}
            />

          </button>


          {/* =================================================
              PROFILE DROPDOWN
          ================================================= */}

          {profileOpen && (

            <div
              className="
                absolute
                right-0
                top-[58px]
                w-56
                bg-white
                border
                border-[#D7E5DA]
                rounded-2xl
                shadow-[0_15px_40px_rgba(30,42,34,0.14)]
                overflow-hidden
                py-2
                animate-[fadeIn_.15s_ease-out]
              "
            >

              {/* PROFILE HEADER */}

              <div
                className="
                  px-4
                  py-3
                  border-b
                  border-[#E6EEE8]
                "
              >

                <p
                  className="
                    text-sm
                    font-semibold
                    text-[#1E2A22]
                  "
                >
                  {userName}
                </p>

                <p
                  className="
                    text-xs
                    text-[#6C7A70]
                    mt-1
                  "
                >
                  Manage your account
                </p>

              </div>


              {/* EDIT PROFILE */}

              <button
                onClick={() => handleMenuClick("/dashboard/settings")}
                className="
                  w-full
                  flex
                  items-center
                  gap-3
                  px-4
                  py-3
                  text-sm
                  text-[#526174]
                  hover:bg-[#EEF5EF]
                  hover:text-[#1E2A22]
                  transition
                "
              >

                <FiEdit3 size={17} />

                <span>
                  Edit Profile
                </span>

              </button>


              {/* SEND FEEDBACK */}

              <button
                onClick={() => handleMenuClick("/dashboard/feedback")}
                className="
                  w-full
                  flex
                  items-center
                  gap-3
                  px-4
                  py-3
                  text-sm
                  text-[#526174]
                  hover:bg-[#EEF5EF]
                  hover:text-[#1E2A22]
                  transition
                "
              >

                <FiMessageSquare size={17} />

                <span>
                  Send Feedback
                </span>

              </button>


              {/* HELP */}

              <button
                onClick={() => handleMenuClick("/dashboard/help")}
                className="
                  w-full
                  flex
                  items-center
                  gap-3
                  px-4
                  py-3
                  text-sm
                  text-[#526174]
                  hover:bg-[#EEF5EF]
                  hover:text-[#1E2A22]
                  transition
                "
              >

                <FiHelpCircle size={17} />

                <span>
                  Help
                </span>

              </button>


              {/* DIVIDER */}

              <div
                className="
                  my-1
                  border-t
                  border-[#E6EEE8]
                "
              />


              {/* LOGOUT */}

              <button
                onClick={handleLogout}
                className="
                  w-full
                  flex
                  items-center
                  gap-3
                  px-4
                  py-3
                  text-sm
                  text-[#B45309]
                  hover:bg-[#FFF7ED]
                  transition
                "
              >

                <FiLogOut size={17} />

                <span>
                  Logout
                </span>

              </button>

            </div>

          )}

        </div>

      </div>

    </header>
  );
}
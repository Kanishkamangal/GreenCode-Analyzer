import { useState, useEffect, useRef } from "react";
import {
  Outlet,
  Link,
  useNavigate,
} from "react-router-dom";

import {
  FiUser,
  FiEdit3,
  FiMessageSquare,
  FiHelpCircle,
  FiLogOut,
  FiChevronDown,
} from "react-icons/fi";

import Sidebar from "./Sidebar";

export default function DashboardLayout() {

  const [collapsed, setCollapsed] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);

  const navigate = useNavigate();
  const profileRef = useRef(null);
  const storedUser = JSON.parse(
  localStorage.getItem("user") || "{}"
);

const userName =
  storedUser?.name ||
  storedUser?.user_name ||
  storedUser?.full_name ||
  storedUser?.username ||
  "User";

  /* =====================================================
     CLOSE PROFILE DROPDOWN WHEN CLICKING OUTSIDE
  ===================================================== */

  useEffect(() => {

    const handleClickOutside = (event) => {

      if (
        profileRef.current &&
        !profileRef.current.contains(event.target)
      ) {
        setProfileOpen(false);
      }

    };

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
    };

  }, []);


  /* =====================================================
     LOGOUT
  ===================================================== */

const handleLogout = () => {

    setProfileOpen(false);

    // Remove all authentication data
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    localStorage.removeItem("isLoggedIn");

    navigate("/", {
      replace: true,
    });

  };


  /* =====================================================
     PROFILE MENU
  ===================================================== */

  const handleEditProfile = () => {

    setProfileOpen(false);

    // Settings page can act as the profile page
    navigate("/dashboard/settings");

  };


  const handleFeedback = () => {

    setProfileOpen(false);

    // Change this later if you create a feedback page
    alert("Feedback feature coming soon.");

  };


  const handleHelp = () => {

    setProfileOpen(false);

    // Change this later if you create a help page
    alert("Help & support section coming soon.");

  };


  /* =====================================================
     UI
  ===================================================== */

  return (

    <div
      className="
        min-h-screen
        bg-[#F9FAFA]
        text-[#0F172A]
      "
    >

      {/* =================================================
          FIXED TOP NAVBAR
      ================================================= */}

      <header
        className="
          fixed
          top-0
          left-0
          right-0
          z-[100]
          h-20

          bg-[#B8D9BC]
border-b
border-[#A5CBAA]

          shadow-[0_2px_12px_rgba(15,23,42,0.05)]
        "
      >

        <div
          className="
            h-full
            px-6
            md:px-8

            flex
            items-center
            justify-between
          "
        >

          {/* =================================================
              LOGO
          ================================================= */}

          <button
            onClick={() => navigate("/dashboard")}
            className="
              flex
              items-center
              gap-3
              outline-none
              group
            "
          >

            {/* LOGO ICON */}

            <div
              className="
                w-10
                h-10
                rounded-xl

                bg-[#0B6B2B]

                text-white

                flex
                items-center
                justify-center

                font-bold
                text-lg

                shadow-[0_4px_12px_rgba(11,107,43,0.15)]

                group-hover:scale-105

                transition-transform
                duration-200
              "
            >
              G
            </div>


            {/* LOGO TEXT */}

            <div className="leading-tight text-left">

              <h1
                className="
                  text-lg
                  font-bold
                  text-[#0F172A]
                "
              >
                GreenCode
              </h1>

              <p
                className="
                  text-[10px]
                  uppercase
                  tracking-[0.18em]
                  text-[#526174]
                "
              >
                Analyzer
              </p>

            </div>

          </button>


          {/* =================================================
              PROFILE AREA
          ================================================= */}

          <div
            ref={profileRef}
            className="relative"
          >

            {/* PROFILE BUTTON */}

            <button
              onClick={() =>
                setProfileOpen(!profileOpen)
              }

              className="
                flex
                items-center
                gap-3

                px-3
                py-2

                rounded-xl

                hover:bg-[#D7EBD9]

                transition-all
                duration-200

                outline-none
              "
            >

              {/* PROFILE ICON */}

              <div
                className="
                  w-10
                  h-10
                  rounded-full

                  bg-white

                  border
                  border-[#C6DCC9]

                  flex
                  items-center
                  justify-center

                  text-[#0B6B2B]

                  shadow-sm
                "
              >
                <FiUser size={19} />
              </div>


              {/* USER DETAILS */}

              <div
                className="
                  hidden
                  sm:block
                  text-left
                "
              >

                <p
                  className="
                    text-sm
                    font-semibold
                    text-[#0F172A]
                  "
                >
                  {userName}
                </p>

                <p
                  className="
                    text-xs
                    text-[#6B7280]
                  "
                >
                  Profile
                </p>

              </div>


              {/* ARROW */}

              <FiChevronDown
                size={16}
                className={`
                  text-[#526174]

                  transition-transform
                  duration-200

                  ${
                    profileOpen
                      ? "rotate-180"
                      : ""
                  }
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

                  w-60

                  bg-white

                  rounded-2xl

                  border
                  border-[#DDE8DF]

                  shadow-[0_15px_40px_rgba(15,23,42,0.14)]

                  overflow-hidden

                  py-2
                "
              >

                {/* ================= USER HEADER ================= */}

                <div
                  className="
                    px-4
                    py-4

                    border-b
                    border-[#E8EEE9]
                  "
                >

                  <div className="flex items-center gap-3">

                    <div
                      className="
                        w-10
                        h-10
                        rounded-full

                        bg-[#E6F2E6]

                        text-[#0B6B2B]

                        flex
                        items-center
                        justify-center
                      "
                    >
                      <FiUser size={18} />
                    </div>

                    <div>

                      <p
                        className="
                          text-sm
                          font-semibold
                          text-[#0F172A]
                        "
                      >
                        {userName}
                      </p>

                      <p
                        className="
                          text-xs
                          text-[#6B7280]
                          mt-0.5
                        "
                      >
                        GreenCode Analyzer
                      </p>

                    </div>

                  </div>

                </div>


                {/* =================================================
                    EDIT PROFILE
                ================================================= */}

                <Link
  to="/dashboard/edit-profile"
  onClick={() => setProfileOpen(false)}
  className="
    w-full
    flex
    items-center
    gap-3
    px-4
    py-3
    text-sm
    text-[#526174]
    hover:bg-[#F3F8F4]
    hover:text-[#0B6B2B]
    transition
  "
>
  <FiEdit3 size={17} />

  <span>
    Edit Profile
  </span>
</Link>


                {/* =================================================
                    SEND FEEDBACK
                ================================================= */}

                <Link
  to="/dashboard/feedback"
  onClick={() => setProfileOpen(false)}
  className="
    w-full
    flex
    items-center
    gap-3
    px-4
    py-3
    text-sm
    text-[#526174]
    hover:bg-[#F3F8F4]
    hover:text-[#0B6B2B]
    transition
  "
>
  <FiMessageSquare size={17} />

  <span>
    Send Feedback
  </span>
</Link>


                {/* =================================================
                    HELP
                ================================================= */}

                <Link
  to="/dashboard/help"
  onClick={() => setProfileOpen(false)}
  className="
    w-full
    flex
    items-center
    gap-3
    px-4
    py-3
    text-sm
    text-[#526174]
    hover:bg-[#F3F8F4]
    hover:text-[#0B6B2B]
    transition
  "
>
  <FiHelpCircle size={17} />

  <span>
    Help
  </span>
</Link>


                {/* =================================================
                    DIVIDER
                ================================================= */}

                <div
                  className="
                    my-2
                    border-t
                    border-[#E8EEE9]
                  "
                />


                {/* =================================================
                    LOGOUT
                ================================================= */}

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
                    text-[#DC2626]

                    hover:bg-[#FEF2F2]

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


      {/* =====================================================
          SIDEBAR
      ===================================================== */}

      <Sidebar
        collapsed={collapsed}
        setCollapsed={setCollapsed}
      />


      {/* =====================================================
          MAIN CONTENT
      ===================================================== */}

      <main
        className={`
          pt-20

          min-h-screen

          transition-all
          duration-300

          ${
            collapsed
              ? "ml-[88px]"
              : "ml-[270px]"
          }
        `}
      >

        <div
          className="
            min-h-[calc(100vh-80px)]

            p-6
            md:p-8
          "
        >

          <Outlet />

        </div>

      </main>

    </div>
  );
}
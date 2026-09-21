import { FiUser } from "react-icons/fi";
import { Link } from "react-router-dom";
import Logo from "./Logo";

export default function Navbar({ onLogin }) {
  const token = localStorage.getItem("access_token");
  return (
    <header
      className="
        w-full
        bg-[#E6F2E6]
        border-b
        border-[#CFE2D2]
        shadow-[0_2px_12px_rgba(15,23,42,0.05)]
      "
    >

      <nav
        className="
          max-w-[1700px]
          mx-auto
          h-24
          px-10
          flex
          items-center
          justify-between
        "
      >

        {/* =================================================
            LOGO
        ================================================= */}

        <Link
          to="/"
          className="
            flex
            items-center
            shrink-0
          "
        >
          <Logo />
        </Link>


        {/* =================================================
            NAVIGATION
        ================================================= */}

        <ul
          className="
            flex
            items-center
            gap-16
            text-[20px]
          "
        >

          {/* ================= HOME ================= */}

          <li>
            <Link
              to="/"
              className="
                relative
                inline-flex
                items-center
                text-[#0B6B2B]
                font-semibold
                cursor-pointer
                transition-colors
                duration-300
              "
            >
              Home

              <span
                className="
                  absolute
                  left-0
                  -bottom-3
                  w-full
                  h-[3px]
                  rounded-full
                  bg-[#16A34A]
                "
              />
            </Link>
          </li>


          {/* ================= ABOUT US ================= */}

          <li>
            <a
              href="/#about"
              className="
                text-[#526174]
                hover:text-[#0B6B2B]
                transition-colors
                duration-300
                cursor-pointer
              "
            >
              About Us
            </a>
          </li>


          {/* ================= FAQS ================= */}

          <li>
            <a
              href="/#faqs"
              className="
                text-[#526174]
                hover:text-[#0B6B2B]
                transition-colors
                duration-300
                cursor-pointer
              "
            >
              FAQs
            </a>
          </li>


          {/* ================= HOW IT WORKS ================= */}

          <li>
            <a
              href="/#how-it-works"
              className="
                text-[#526174]
                hover:text-[#0B6B2B]
                transition-colors
                duration-300
                cursor-pointer
              "
            >
              How It Works
            </a>
          </li>

        </ul>


        {/* =================================================
            LOGIN BUTTON
        ================================================= */}

        {token ? (

  <Link
    to="/dashboard"
    className="
      flex
      items-center
      gap-3
      px-8
      py-3
      rounded-xl

      border
      border-[#0B6B2B]

      bg-[#0B6B2B]
      text-white

      hover:bg-[#095823]

      transition-all
      duration-300

      shadow-sm
      hover:shadow-[0_6px_18px_rgba(11,107,43,0.15)]
    "
  >
    <FiUser size={22} />

    <span className="text-xl font-medium">
      Dashboard
    </span>
  </Link>

) : (

  <button
    onClick={onLogin}
    className="
      flex
      items-center
      gap-3
      px-8
      py-3
      rounded-xl

      border
      border-[#0B6B2B]

      bg-white
      text-[#0B6B2B]

      hover:bg-[#0B6B2B]
      hover:text-white

      transition-all
      duration-300

      shadow-sm
      hover:shadow-[0_6px_18px_rgba(11,107,43,0.15)]
    "
  >
    <FiUser size={22} />

    <span className="text-xl font-medium">
      Login
    </span>
  </button>

)}

      </nav>

    </header>
  );
}
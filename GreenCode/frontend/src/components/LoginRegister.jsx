import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FiMail,
  FiLock,
  FiPhone,
  FiUser,
  FiEye,
  FiEyeOff,
  FiArrowLeft,
  FiArrowRight,
  FiX,
  FiCheckCircle,
  FiRefreshCw,
} from "react-icons/fi";
import { GoogleLogin } from "@react-oauth/google";

export default function LoginRegister({
  onClose,
  onLogin,


}) {
  const navigate = useNavigate();
  /* =====================================================
     MAIN AUTH SCREEN
  ===================================================== */

  const [activePanel, setActivePanel] = useState("login");

  /*
    login
    register
    forgot
  */


  /* =====================================================
     LOGIN MODE
  ===================================================== */

  const [loginMode, setLoginMode] = useState("email");

  /*
    email
    phone
  */


  /* =====================================================
     PHONE OTP
  ===================================================== */

  const [otpSent, setOtpSent] = useState(false);

  const [otp, setOtp] = useState("");

  const [otpError, setOtpError] = useState("");

  const [resendTimer, setResendTimer] = useState(0);


  /* =====================================================
     PASSWORD VISIBILITY
  ===================================================== */

  const [showLoginPassword, setShowLoginPassword] =
    useState(false);

  const [showRegisterPassword, setShowRegisterPassword] =
    useState(false);

  const [showRegisterConfirm, setShowRegisterConfirm] =
    useState(false);

  const [showForgotPassword, setShowForgotPassword] =
    useState(false);

  const [showForgotConfirm, setShowForgotConfirm] =
    useState(false);


  /* =====================================================
     LOGIN FORM
  ===================================================== */

  const [loginEmail, setLoginEmail] = useState("");

  const [loginPassword, setLoginPassword] =
    useState("");

  const [loginPhone, setLoginPhone] =
    useState("");


  /* =====================================================
     REGISTER FORM
  ===================================================== */

  const [registerName, setRegisterName] =
    useState("");

  const [registerEmail, setRegisterEmail] =
    useState("");

  const [registerPhone, setRegisterPhone] =
    useState("");
  const [registerPhoneError, setRegisterPhoneError] =
    useState("");

  const [registerPassword, setRegisterPassword] =
    useState("");

  const [registerConfirm, setRegisterConfirm] =
    useState("");

  const [registerOtpSent, setRegisterOtpSent] = useState(false);
  const [registerOtp, setRegisterOtp] = useState("");
  const [registerOtpError, setRegisterOtpError] = useState("");


  /* =====================================================
     FORGOT PASSWORD
  ===================================================== */

  const [forgotMode, setForgotMode] =
    useState("email");

  const [forgotEmail, setForgotEmail] =
    useState("");

  const [forgotPhone, setForgotPhone] =
    useState("");

  const [forgotOtpSent, setForgotOtpSent] =
    useState(false);

  const [forgotOtp, setForgotOtp] =
    useState("");

  const [forgotNewPassword, setForgotNewPassword] =
    useState("");

  const [forgotConfirmPassword, setForgotConfirmPassword] =
    useState("");

  const [forgotSuccess, setForgotSuccess] =
    useState(false);


  /* =====================================================
     NAVIGATION
  ===================================================== */

  const goToLogin = () => {
    setActivePanel("login");

    setLoginMode("email");

    setOtpSent(false);
    setOtp("");
    setOtpError("");

    setForgotOtpSent(false);
    setForgotOtp("");

    setForgotSuccess(false);
  };


  const goToRegister = () => {
    setActivePanel("register");
  };


  const goToForgot = () => {
    setActivePanel("forgot");

    setForgotMode("email");

    setForgotOtpSent(false);
    setForgotOtp("");

    setForgotSuccess(false);
  };


  /* =====================================================
     LOGIN — EMAIL
  ===================================================== */
  const handleEmailLogin = async (e) => {
    e.preventDefault();

    if (!loginEmail || !loginPassword) {
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/users/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email_or_phone: loginEmail.trim(),
            password: loginPassword,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Login failed.");
        return;
      }

      localStorage.setItem(
        "access_token",
        data.access_token
      );

      localStorage.setItem(
        "user",
        JSON.stringify(data.user)
      );

      if (onLogin) {
        onLogin();
      }

      navigate("/dashboard", {
        replace: true,
      });

    } catch (error) {
      console.error("Login error:", error);
      alert("Unable to connect to backend.");
    }
  };


  /* =====================================================
     LOGIN — GOOGLE
  ===================================================== */
  const handleGoogleLogin = async (credentialResponse) => {
    try {
      if (!credentialResponse?.credential) {
        alert("Google authentication failed. Please try again.");
        return;
      }

      const response = await fetch(
        "http://127.0.0.1:8000/users/google",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            credential: credentialResponse.credential,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(
          data.detail ||
          "Google authentication failed."
        );
        return;
      }

      localStorage.setItem(
        "access_token",
        data.access_token
      );

      localStorage.setItem(
        "user",
        JSON.stringify(data.user)
      );

      if (onLogin) {
        onLogin();
      }

      navigate("/dashboard", {
        replace: true,
      });

    } catch (error) {
      console.error(
        "Google authentication error:",
        error
      );

      alert(
        "Unable to connect to backend for Google login."
      );
    }
  };


  /* =====================================================
     LOGIN — PHONE OTP
  ===================================================== */

  const handleSendLoginOtp = (e) => {
    e.preventDefault();

    if (!loginPhone) {
      return;
    }

    setOtpSent(true);
    setOtp("");
    setOtpError("");
    setResendTimer(30);

    /*
      Connect:
      POST /auth/send-otp
      here later.
    */

    startResendTimer();
  };


  const handleVerifyLoginOtp = (e) => {
    e.preventDefault();

    if (otp.length !== 6) {
      setOtpError(
        "Please enter the 6-digit OTP."
      );

      return;
    }

    /*
      Connect:
      POST /auth/verify-otp
      here later.
    */

    if (onLogin) {
      onLogin();
    }
  };


  /* =====================================================
     RESEND TIMER
  ===================================================== */

  const startResendTimer = () => {
    let seconds = 30;

    const timer = setInterval(() => {
      seconds -= 1;

      setResendTimer(seconds);

      if (seconds <= 0) {
        clearInterval(timer);
      }
    }, 1000);
  };


  const resendLoginOtp = () => {
    if (resendTimer > 0) {
      return;
    }

    setOtp("");
    setOtpError("");

    setResendTimer(30);

    startResendTimer();

    /*
      Connect OTP API here.
    */
  };


  /* =====================================================
     REGISTER
  ===================================================== */

  // const handleRegister = async (e) => {
  //   e.preventDefault();

  //   if (
  //     !registerName ||
  //     !registerEmail ||
  //     !registerPhone ||
  //     !registerPassword ||
  //     !registerConfirm
  //   ) {
  //     alert("Please fill all fields.");
  //     return;
  //   }

  //   if (registerPassword !== registerConfirm) {
  //     alert("Passwords do not match.");
  //     return;
  //   }

  //   try {
  //     const response = await fetch(
  //       "http://127.0.0.1:8000/users/register",
  //       {
  //         method: "POST",
  //         headers: {
  //           "Content-Type": "application/json",
  //         },
  //         body: JSON.stringify({
  //           name: registerName,
  //           email: registerEmail,
  //           phone: registerPhone,
  //           password: registerPassword,
  //         }),
  //       }
  //     );

  //     const data = await response.json();

  //     if (!response.ok) {
  //       alert(data.detail || "Registration failed.");
  //       return;
  //     }

  //     alert("Registration successful! Please login.");

  //     // Clear registration fields
  //     setRegisterName("");
  //     setRegisterEmail("");
  //     setRegisterPhone("");
  //     setRegisterPassword("");
  //     setRegisterConfirm("");

  //     // Open Login panel
  //     goToLogin();

  //   } catch (error) {
  //     console.error("Registration error:", error);
  //     alert("Unable to connect to backend.");
  //   }
  // };

  const handleRegister = async (e) => {
    e.preventDefault();

    if (
  !registerName ||
  !registerEmail ||
  !registerPassword ||
  !registerConfirm
) {
  alert("Please fill all fields.");
  return;
}

// Phone number required
if (!registerPhone.trim()) {
  setRegisterPhoneError(
    "Phone number is required."
  );
  return;
}

// Phone must contain exactly 10 digits
if (!/^\d{10}$/.test(registerPhone.trim())) {
  setRegisterPhoneError(
    "Please enter a valid 10-digit phone number."
  );
  return;
}

setRegisterPhoneError("");

if (registerPassword !== registerConfirm) {
  alert("Passwords do not match.");
  return;
}

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/otp/send-email",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: registerName.trim(),
            email: registerEmail.trim(),
            phone: registerPhone.trim(),
            password: registerPassword,
          }),
        }
      );

      const data = await response.json();

      // OTP was NOT sent
      if (!response.ok) {
        alert(data.detail || "Unable to send OTP.");
        return;
      }

      // OTP successfully sent
      setRegisterOtpSent(true);
      setRegisterOtp("");
      setRegisterOtpError("");

    } catch (error) {
      console.error("OTP send error:", error);
      alert("Unable to connect to backend.");
    }
  };

  const handleRegisterOtpVerification = async (e) => {
    e.preventDefault();

    if (registerOtp.length !== 6) {
      setRegisterOtpError(
        "Please enter the 6-digit OTP."
      );
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/otp/verify-email",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: registerEmail,
            otp: registerOtp,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setRegisterOtpError(
          data.detail || "Invalid or expired OTP."
        );
        return;
      }

      // Registration completed successfully

      // Save JWT token
      localStorage.setItem(
        "access_token",
        data.access_token
      );

      // Save user information
      localStorage.setItem(
        "user",
        JSON.stringify(data.user)
      );

      // Clear registration data
      setRegisterName("");
      setRegisterEmail("");
      setRegisterPhone("");
      setRegisterPassword("");
      setRegisterConfirm("");
      setRegisterOtp("");
      setRegisterOtpSent(false);
      setRegisterOtpError("");

      // Close authentication modal
      if (onClose) {
        onClose();
      }

      // Go directly to dashboard
      navigate("/dashboard", {
        replace: true,
      });

    } catch (error) {
      console.error(
        "OTP verification error:",
        error
      );

      setRegisterOtpError(
        "Unable to connect to backend."
      );
    }
  };

  /* =====================================================
     FORGOT — SEND OTP
  ===================================================== */

  const handleForgotSendOtp = (e) => {
    e.preventDefault();

    if (!forgotPhone) {
      return;
    }

    setForgotOtpSent(true);
    setForgotOtp("");
  };

  // resend OTP for registration
      const handleResendRegisterOtp = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/otp/resend-email",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: registerEmail,
            }),
          }
        );

        const data = await response.json();

        if (!response.ok) {
          setRegisterOtpError(
            data.detail || "Unable to resend OTP."
          );
          return;
        }

        setRegisterOtp("");
        setRegisterOtpError("");

        alert("New OTP has been sent to your email.");

      } catch (error) {
        console.error("Resend OTP error:", error);

        setRegisterOtpError(
          "Unable to connect to backend."
        );
      }
    };

  /* =====================================================
     FORGOT — RESET
  ===================================================== */

  const handlePasswordReset = (e) => {
    e.preventDefault();

    if (
      forgotOtp.length !== 6 ||
      !forgotNewPassword ||
      !forgotConfirmPassword
    ) {
      return;
    }

    if (
      forgotNewPassword !==
      forgotConfirmPassword
    ) {
      return;
    }

    /*
      Connect password reset API here.
    */

    setForgotSuccess(true);
  };


  /* =====================================================
     SHARED INPUT STYLE
  ===================================================== */

  const inputWrapper = `
    relative
    flex
    items-center
    w-full
    h-[56px]
    rounded-xl
    border
    border-[#D5E6D8]
    bg-[#FFFFFF]
    transition-all
    duration-300
    focus-within:border-[#16A34A]
    focus-within:ring-4
    focus-within:ring-[#EAF6EC]
  `;


  const inputStyle = `
    w-full
    h-full
    bg-transparent
    outline-none
    text-[#0F172A]
    placeholder:text-[#9CA3AF]
    text-[15px]
  `;


  const primaryButton = `
    w-full
    h-[56px]
    rounded-xl
    bg-[#0B6B2B]
    text-white
    font-semibold
    text-[16px]
    transition-all
    duration-300
    hover:bg-[#16A34A]
    hover:shadow-[0_8px_20px_rgba(11,107,43,0.18)]
    active:scale-[0.98]
  `;


  /* =====================================================
     RETURN
  ===================================================== */

  return (
    <div
      className="
        fixed
        inset-0
        z-[100]
        flex
        items-center
        justify-center
        bg-[#0F172A]/60
        backdrop-blur-md
        p-6
      "
    >

      {/* =================================================
          MAIN AUTH CONTAINER
      ================================================= */}

      <div
        className="
          relative
          w-full
          max-w-[1100px]
          h-[700px]
          overflow-hidden
          rounded-[28px]
          bg-[#FFFFFF]
          shadow-[0_30px_90px_rgba(15,23,42,0.25)]
          border
          border-[#D5E6D8]
          flex
        "
      >

        {/* =================================================
            CLOSE BUTTON
        ================================================= */}

        <button
          onClick={onClose}
          className="
            absolute
            z-50
            top-5
            right-5
            w-10
            h-10
            rounded-full
            bg-[#F9FAFA]
            border
            border-[#D5E6D8]
            flex
            items-center
            justify-center
            text-[#526174]
            hover:bg-[#DFF0E1]
            hover:text-[#0B6B2B]
            transition-all
            duration-300
          "
        >
          <FiX size={20} />
        </button>


        {/* =================================================
            LEFT BRAND PANEL
        ================================================= */}

        <div
          className="
            hidden
            lg:flex
            w-[46%]
            shrink-0
            relative
            overflow-hidden
            items-center
            justify-center
            bg-[#0B6B2B]
            text-white
          "
        >

          {/* Soft Background Glow */}

          <div
            className="
              absolute
              w-[500px]
              h-[500px]
              rounded-full
              bg-[#16A34A]/30
              blur-3xl
            "
          />


          <div
            className="
              relative
              z-10
              flex
              flex-col
              items-center
              text-center
              px-12
            "
          >

            {/* Brand Icon */}

            <div
              className="
                w-28
                h-28
                rounded-full
                flex
                items-center
                justify-center
                bg-white/10
                border
                border-white/20
                mb-8
                shadow-[0_10px_40px_rgba(0,0,0,0.12)]
              "
            >
              <span
                className="
                  text-[52px]
                "
              >
                🌿
              </span>
            </div>


            {/* Brand */}

            <h1
              className="
                text-[48px]
                font-black
                tracking-[-0.03em]
              "
            >
              GreenCode
            </h1>


            <p
              className="
                text-[26px]
                font-semibold
                mt-1
                text-[#DFF0E1]
              "
            >
              Analyzer
            </p>


            {/* Description */}

            <p
              className="
                mt-8
                max-w-[390px]
                text-[16px]
                leading-7
                text-white/80
              "
            >
              Benchmark programming languages,
              compare execution efficiency,
              analyze energy consumption,
              and discover greener code.
            </p>


            {/* Decorative Line */}

            <div
              className="
                mt-10
                w-20
                h-1
                rounded-full
                bg-[#84CC16]
              "
            />

          </div>

        </div>


        {/* =================================================
            RIGHT AUTH VIEWPORT
        ================================================= */}

        <div
          className="
            relative
            flex-1
            overflow-hidden
            bg-[#FFFFFF]
          "
        >

          {/* =================================================
              SLIDING PANELS
          ================================================= */}

          <div
            className={`
              absolute
              top-0
              left-0
              flex
              h-full
              w-[300%]
              transition-transform
              duration-700
              ease-[cubic-bezier(0.77,0,0.175,1)]
              ${activePanel === "login"
                ? "translate-x-0"
                : activePanel === "register"
                  ? "-translate-x-1/3"
                  : "-translate-x-2/3"
              }
            `}
          >

            {/* =================================================
                LOGIN PANEL
            ================================================= */}

            <div
              className="
                w-1/3
                h-full
                shrink-0
                overflow-y-auto
                px-12
                py-16
              "
            >

              <div className="max-w-[470px] mx-auto">

                <div className="text-center">

                  <h2
                    className="
                      text-[36px]
                      font-extrabold
                      text-[#0F172A]
                    "
                  >
                    Login to Continue
                  </h2>

                  <div
                    className="
                      mx-auto
                      mt-5
                      w-16
                      h-[3px]
                      rounded-full
                      bg-[#16A34A]
                    "
                  />

                </div>


                {/* =================================================
                    EMAIL LOGIN
                ================================================= */}

                {loginMode === "email" && (
                  <form
                    onSubmit={handleEmailLogin}
                    className="mt-12"
                  >

                  {/* Email / Phone */}

                    <label
                      className="
                        block
                        text-[15px]
                        font-semibold
                        text-[#0F172A]
                        mb-2
                      "
                    >
                      Email Address / Phone Number
                    </label>

                    <div className={inputWrapper}>

                      <FiUser
                        className="
                          ml-4
                          mr-3
                          text-[#0B6B2B]
                          shrink-0
                        "
                        size={20}
                      />

                      <input
                        type="text"
                        value={loginEmail}
                        onChange={(e) =>
                          setLoginEmail(e.target.value)
                        }
                        placeholder="Enter email or phone number"
                        className={inputStyle}
                      />

                    </div>


                    {/* Password */}

                    <label
                      className="
                        block
                        text-[15px]
                        font-semibold
                        text-[#0F172A]
                        mb-2
                        mt-6
                      "
                    >
                      Password
                    </label>

                    <div className={inputWrapper}>

                      <FiLock
                        className="
                          ml-4
                          mr-3
                          text-[#0B6B2B]
                          shrink-0
                        "
                        size={20}
                      />

                      <input
                        type={
                          showLoginPassword
                            ? "text"
                            : "password"
                        }
                        value={loginPassword}
                        onChange={(e) =>
                          setLoginPassword(
                            e.target.value
                          )
                        }
                        placeholder="Enter your password"
                        className={inputStyle}
                      />

                      <button
                        type="button"
                        onClick={() =>
                          setShowLoginPassword(
                            !showLoginPassword
                          )
                        }
                        className="
                          mr-4
                          text-[#6B7280]
                          hover:text-[#0B6B2B]
                        "
                      >
                        {showLoginPassword ? (
                          <FiEyeOff size={20} />
                        ) : (
                          <FiEye size={20} />
                        )}
                      </button>

                    </div>


                    {/* Forgot */}

                    <div className="flex justify-end mt-3">

                      <button
                        type="button"
                        onClick={goToForgot}
                        className="
                          text-[14px]
                          font-medium
                          text-[#0B6B2B]
                          hover:text-[#16A34A]
                        "
                      >
                        Forgot Password?
                      </button>

                    </div>


                    {/* Login */}

                    <button
                      type="submit"
                      className={`${primaryButton} mt-7`}
                    >
                      Login
                    </button>


                    {/* Divider */}

                    <div className="flex items-center gap-4 my-6">

                      <div className="flex-1 h-px bg-[#D5E6D8]" />

                      <span
                        className="
                          text-[13px]
                          text-[#6B7280]
                        "
                      >
                        OR
                      </span>

                      <div className="flex-1 h-px bg-[#D5E6D8]" />

                    </div>
                    {/* =====================================================
    GOOGLE LOGIN
===================================================== */}
<div className="mt-4 flex justify-center">
  <GoogleLogin
    onSuccess={handleGoogleLogin}
    onError={() => {
      alert("Google login failed. Please try again.");
    }}
    useOneTap={false}
  />
</div>

                    {/* Phone Login

                    <button
                      type="button"
                      onClick={() =>
                        setLoginMode("phone")
                      }
                      className="
                        w-full
                        h-[54px]
                        rounded-xl
                        border
                        border-[#0B6B2B]
                        bg-[#FFFFFF]
                        text-[#0B6B2B]
                        font-semibold
                        flex
                        items-center
                        justify-center
                        gap-3
                        hover:bg-[#EAF6EC]
                        transition-all
                        duration-300
                      "
                    >
                      <FiPhone size={19} />
                      Login with Phone Number
                    </button> */}


                    {/* Register */}

                    <p
                      className="
                        text-center
                        mt-8
                        text-[14px]
                        text-[#6B7280]
                      "
                    >
                      Don't have an account?

                      <button
                        type="button"
                        onClick={goToRegister}
                        className="
                          ml-2
                          font-semibold
                          text-[#0B6B2B]
                          hover:text-[#16A34A]
                        "
                      >
                        Register
                      </button>

                    </p>

                  </form>
                )}


                {/* =================================================
                    PHONE LOGIN
                ================================================= */}

                {loginMode === "phone" && (
                  <div className="mt-12">

                    {!otpSent ? (
                      <form
                        onSubmit={
                          handleSendLoginOtp
                        }
                      >

                        <label
                          className="
                            block
                            text-[15px]
                            font-semibold
                            text-[#0F172A]
                            mb-2
                          "
                        >
                          Phone Number
                        </label>

                        <div className={inputWrapper}>

                          <FiPhone
                            className="
                              ml-4
                              mr-3
                              text-[#0B6B2B]
                            "
                            size={20}
                          />

                          <span
                            className="
                              text-[#526174]
                              text-[14px]
                              pr-2
                              border-r
                              border-[#D5E6D8]
                            "
                          >
                            +91
                          </span>

                          <input
                            type="tel"
                            value={loginPhone}
                            onChange={(e) =>
                              setLoginPhone(
                                e.target.value
                              )
                            }
                            placeholder="Enter phone number"
                            className={`${inputStyle} pl-3`}
                            maxLength={10}
                          />

                        </div>


                        <button
                          type="submit"
                          className={`${primaryButton} mt-7`}
                        >
                          Send OTP
                        </button>


                        <button
                          type="button"
                          onClick={() =>
                            setLoginMode("email")
                          }
                          className="
                            flex
                            items-center
                            justify-center
                            gap-2
                            mx-auto
                            mt-6
                            text-[14px]
                            font-semibold
                            text-[#0B6B2B]
                          "
                        >
                          <FiArrowLeft />
                          Back to Email Login
                        </button>

                      </form>
                    ) : (
                      <form
                        onSubmit={
                          handleVerifyLoginOtp
                        }
                      >

                        <div
                          className="
                            flex
                            flex-col
                            items-center
                            text-center
                          "
                        >

                          <div
                            className="
                              w-14
                              h-14
                              rounded-full
                              bg-[#EAF6EC]
                              text-[#0B6B2B]
                              flex
                              items-center
                              justify-center
                            "
                          >
                            <FiPhone size={24} />
                          </div>

                          <h3
                            className="
                              mt-5
                              text-[22px]
                              font-bold
                              text-[#0F172A]
                            "
                          >
                            Verify your phone
                          </h3>

                          <p
                            className="
                              mt-2
                              text-[14px]
                              text-[#6B7280]
                            "
                          >
                            Enter the 6-digit OTP
                            sent to
                          </p>

                          <p
                            className="
                              mt-1
                              font-semibold
                              text-[#0B6B2B]
                            "
                          >
                            +91 {loginPhone}
                          </p>

                        </div>


                        <input
                          type="text"
                          inputMode="numeric"
                          value={otp}
                          onChange={(e) =>
                            setOtp(
                              e.target.value
                                .replace(
                                  /\D/g,
                                  ""
                                )
                                .slice(0, 6)
                            )
                          }
                          placeholder="Enter OTP"
                          className="
                            mt-8
                            w-full
                            h-14
                            rounded-xl
                            border
                            border-[#D5E6D8]
                            text-center
                            tracking-[12px]
                            text-[22px]
                            font-bold
                            text-[#0F172A]
                            outline-none
                            focus:border-[#16A34A]
                            focus:ring-4
                            focus:ring-[#EAF6EC]
                          "
                        />

                        {otpError && (
                          <p
                            className="
                              text-center
                              text-sm
                              text-red-500
                              mt-3
                            "
                          >
                            {otpError}
                          </p>
                        )}


                        <button
                          type="submit"
                          className={`${primaryButton} mt-6`}
                        >
                          Verify & Login
                        </button>


                        <button
                          type="button"
                          onClick={resendLoginOtp}
                          disabled={resendTimer > 0}
                          className={`
                            flex
                            items-center
                            justify-center
                            gap-2
                            mx-auto
                            mt-5
                            text-[14px]
                            font-semibold
                            ${resendTimer > 0
                              ? "text-[#9CA3AF]"
                              : "text-[#0B6B2B]"
                            }
                          `}
                        >
                          <FiRefreshCw />

                          {resendTimer > 0
                            ? `Resend OTP in ${resendTimer}s`
                            : "Resend OTP"}
                        </button>

                      </form>
                    )}

                  </div>
                )}

              </div>

            </div>


            {/* =================================================
                REGISTER PANEL
            ================================================= */}

            <div
              className="
                w-1/3
                h-full
                shrink-0
                overflow-y-auto
                px-12
                py-12
              "
            >

              <div className="max-w-[470px] mx-auto">

                <div className="text-center">

                  <h2
                    className="
                      text-[36px]
                      font-extrabold
                      text-[#0F172A]
                    "
                  >
                    Create Account
                  </h2>

                  <div
                    className="
                      mx-auto
                      mt-5
                      w-16
                      h-[3px]
                      rounded-full
                      bg-[#16A34A]
                    "
                  />

                </div>


                {!registerOtpSent ? (

                  /* ================= REGISTER FORM ================= */

                  <form
                    onSubmit={handleRegister}
                    className="mt-8"
                  >

                    {/* Name */}

                    <label
                      className="
                  block
                  text-[14px]
                  font-semibold
                  text-[#0F172A]
                  mb-2
                "
                    >
                      Full Name
                    </label>

                    <div className={inputWrapper}>

                      <FiUser
                        className="
                    ml-4
                    mr-3
                    text-[#0B6B2B]
                  "
                        size={20}
                      />

                      <input
                        type="text"
                        value={registerName}
                        onChange={(e) =>
                          setRegisterName(e.target.value)
                        }
                        placeholder="Enter your full name"
                        className={inputStyle}
                      />

                    </div>


                    {/* Email */}

                    <label
                      className="
                  block
                  text-[14px]
                  font-semibold
                  text-[#0F172A]
                  mb-2
                  mt-4
                "
                    >
                      Email Address
                    </label>

                    <div className={inputWrapper}>

                      <FiMail
                        className="
                    ml-4
                    mr-3
                    text-[#0B6B2B]
                  "
                        size={20}
                      />

                      <input
                        type="email"
                        value={registerEmail}
                        onChange={(e) =>
                          setRegisterEmail(e.target.value)
                        }
                        placeholder="Enter your email"
                        className={inputStyle}
                      />

                    </div>
                    {/* Phone Number */}

                    <label
                      className="
                        block
                        text-[14px]
                        font-semibold
                        text-[#0F172A]
                        mb-2
                        mt-4
                      "
                    >
                      Phone Number
                    </label>

                    <div className={inputWrapper}>

                      <FiPhone
                        className="
                          ml-4
                          mr-3
                          text-[#0B6B2B]
                          shrink-0
                        "
                        size={20}
                      />

                      <span
                        className="
                          text-[#526174]
                          text-[14px]
                          pr-2
                          border-r
                          border-[#D5E6D8]
                        "
                      >
                        +91
                      </span>

                      <input
                        type="tel"
                        inputMode="numeric"
                        value={registerPhone}
                        onChange={(e) => {
                          const value = e.target.value
                            .replace(/\D/g, "")
                            .slice(0, 10);

                          setRegisterPhone(value);

                          if (registerPhoneError) {
                            setRegisterPhoneError("");
                          }
                        }}
                        placeholder="Enter 10-digit phone number"
                        className={`${inputStyle} pl-3`}
                        maxLength={10}
                      />

                      </div>

                      {registerPhoneError && (
                        <p className="mt-1.5 text-[13px] text-red-500">
                          {registerPhoneError}
                        </p>
                      )}
                    {/* Password */}

                    <label
                      className="
                  block
                  text-[14px]
                  font-semibold
                  text-[#0F172A]
                  mb-2
                  mt-4
                "
                    >
                      Password
                    </label>

                    <div className={inputWrapper}>
                      <FiLock
                        className="
                    ml-4
                    mr-3
                    text-[#0B6B2B]
                  "
                        size={20}
                      />

                      <input
                        type={
                          showRegisterPassword
                            ? "text"
                            : "password"
                        }
                        value={registerPassword}
                        onChange={(e) =>
                          setRegisterPassword(e.target.value)
                        }
                        placeholder="Create a password"
                        className={inputStyle}
                      />

                      <button
                        type="button"
                        onClick={() =>
                          setShowRegisterPassword(
                            !showRegisterPassword
                          )
                        }
                        className="
                    mr-4
                    text-[#6B7280]
                    hover:text-[#0B6B2B]
                  "
                      >
                        {showRegisterPassword ? (
                          <FiEyeOff size={20} />
                        ) : (
                          <FiEye size={20} />
                        )}
                      </button>

                    </div>


                    {/* Confirm Password */}

                    <label
                      className="
                  block
                  text-[14px]
                  font-semibold
                  text-[#0F172A]
                  mb-2
                  mt-4
                "
                    >
                      Confirm Password
                    </label>

                    <div className={inputWrapper}>

                      <FiLock
                        className="
                    ml-4
                    mr-3
                    text-[#0B6B2B]
                  "
                        size={20}
                      />

                      <input
                        type={
                          showRegisterConfirm
                            ? "text"
                            : "password"
                        }
                        value={registerConfirm}
                        onChange={(e) =>
                          setRegisterConfirm(e.target.value)
                        }
                        placeholder="Confirm your password"
                        className={inputStyle}
                      />

                      <button
                        type="button"
                        onClick={() =>
                          setShowRegisterConfirm(
                            !showRegisterConfirm
                          )
                        }
                        className="
                    mr-4
                    text-[#6B7280]
                    hover:text-[#0B6B2B]
                  "
                      >
                        {showRegisterConfirm ? (
                          <FiEyeOff size={20} />
                        ) : (
                          <FiEye size={20} />
                        )}
                      </button>

                    </div>


                    {/* Register */}

<button
  type="submit"
  className={`${primaryButton} mt-6`}
>
  Register
</button>

{/* =====================================================
    REGISTER — GOOGLE
===================================================== */}
<div className="my-5 flex items-center">
  <div className="flex-1 border-t border-gray-300"></div>

  <span className="px-3 text-sm text-gray-500">
    OR
  </span>

  <div className="flex-1 border-t border-gray-300"></div>
</div>

<div className="flex justify-center">
  <GoogleLogin
    onSuccess={handleGoogleLogin}
    onError={() => {
      alert("Google registration failed. Please try again.");
    }}
    useOneTap={false}
  />
</div>

                    <p
                      className="
                  text-center
                  mt-6
                  text-[14px]
                  text-[#6B7280]
                "
                    >
                      Already have an account?

                      <button
                        type="button"
                        onClick={goToLogin}
                        className="
                    ml-2
                    font-semibold
                    text-[#0B6B2B]
                    hover:text-[#16A34A]
                  "
                      >
                        Login
                      </button>

                    </p>

                  </form>

                ) : (

                  /* ================= VERIFY EMAIL ================= */

                  <form
                    onSubmit={handleRegisterOtpVerification}
                    className="mt-12"
                  >

                    <div
                      className="
                  flex
                  flex-col
                  items-center
                  text-center
                "
                    >

                      <div
                        className="
                    w-16
                    h-16
                    rounded-full
                    bg-[#EAF6EC]
                    text-[#0B6B2B]
                    flex
                    items-center
                    justify-center
                  "
                      >
                        <FiMail size={28} />
                      </div>

                      <h3
                        className="
                    mt-6
                    text-[26px]
                    font-bold
                    text-[#0F172A]
                  "
                      >
                        Verify Your Email
                      </h3>

                      <p
                        className="
                    mt-3
                    text-[14px]
                    leading-6
                    text-[#6B7280]
                  "
                      >
                        We sent a 6-digit verification code
                        to
                      </p>

                      <p
                        className="
                    mt-1
                    font-semibold
                    text-[#0B6B2B]
                    break-all
                  "
                      >
                        {registerEmail}
                      </p>

                    </div>


                    {/* OTP */}

                    <input
                      type="text"
                      inputMode="numeric"
                      value={registerOtp}
                      onChange={(e) =>
                        setRegisterOtp(
                          e.target.value
                            .replace(/\D/g, "")
                            .slice(0, 6)
                        )
                      }
                      placeholder="Enter OTP"
                      className="
                  mt-8
                  w-full
                  h-14
                  rounded-xl
                  border
                  border-[#D5E6D8]
                  text-center
                  tracking-[12px]
                  text-[22px]
                  font-bold
                  text-[#0F172A]
                  outline-none
                  focus:border-[#16A34A]
                  focus:ring-4
                  focus:ring-[#EAF6EC]
                "
                    />


                    {registerOtpError && (
                      <p
                        className="
                    text-center
                    text-sm
                    text-red-500
                    mt-3
                  "
                      >
                        {registerOtpError}
                      </p>
                    )}


                    {/* Verify */}

                    <button
                      type="submit"
                      className={`${primaryButton} mt-6`}
                    >
                      Verify Email
                    </button>

                    {/* RESEND OTP */}
                    <button
                      type="button"
                      onClick={handleResendRegisterOtp}
                      className="
                        flex
                        items-center
                        justify-center
                        gap-2
                        mx-auto
                        mt-5
                        text-[14px]
                        font-semibold
                        text-[#0B6B2B]
                        hover:text-[#16A34A]
                      "
                    >
                      <FiRefreshCw />
                      Resend OTP
                    </button>


                    {/* Back */}

                    <button
                      type="button"
                      onClick={() => {
                        setRegisterOtpSent(false);
                        setRegisterOtp("");
                        setRegisterOtpError("");
                      }}
                      className="
                  flex
                  items-center
                  justify-center
                  gap-2
                  mx-auto
                  mt-6
                  text-[14px]
                  font-semibold
                  text-[#526174]
                  hover:text-[#0B6B2B]
                "
                    >
                      <FiArrowLeft />
                      Back to Registration
                    </button>

                  </form>

                )}

              </div>

            </div>


            {/* =================================================
                FORGOT PASSWORD PANEL
            ================================================= */}

            <div
              className="
                w-1/3
                h-full
                shrink-0
                overflow-y-auto
                px-12
                py-16
              "
            >

              <div className="max-w-[470px] mx-auto">

                <div className="text-center">

                  <div
                    className="
                      mx-auto
                      w-14
                      h-14
                      rounded-full
                      bg-[#EAF6EC]
                      text-[#0B6B2B]
                      flex
                      items-center
                      justify-center
                    "
                  >
                    <FiLock size={24} />
                  </div>


                  <h2
                    className="
                      text-[32px]
                      font-extrabold
                      text-[#0F172A]
                      mt-5
                    "
                  >
                    Reset Password
                  </h2>

                  <div
                    className="
                      mx-auto
                      mt-4
                      w-16
                      h-[3px]
                      rounded-full
                      bg-[#16A34A]
                    "
                  />

                </div>


                {/* =================================================
                    SUCCESS
                ================================================= */}

                {forgotSuccess ? (
                  <div
                    className="
                      flex
                      flex-col
                      items-center
                      text-center
                      mt-16
                    "
                  >

                    <FiCheckCircle
                      size={56}
                      className="
                        text-[#16A34A]
                      "
                    />

                    <h3
                      className="
                        text-[24px]
                        font-bold
                        text-[#0F172A]
                        mt-5
                      "
                    >
                      Password Updated
                    </h3>

                    <p
                      className="
                        text-[#6B7280]
                        mt-3
                      "
                    >
                      Your password has been
                      successfully reset.
                    </p>

                    <button
                      type="button"
                      onClick={goToLogin}
                      className={`${primaryButton} mt-8`}
                    >
                      Back to Login
                    </button>

                  </div>
                ) : (
                  <>
                    {/* =================================================
                        EMAIL RESET
                    ================================================= */}

                    {forgotMode === "email" && (
                      <div className="mt-10">

                        <p
                          className="
                            text-center
                            text-[14px]
                            text-[#526174]
                            leading-6
                            mb-7
                          "
                        >
                          Enter your email address and
                          we'll help you reset your password.
                        </p>


                        <label
                          className="
                            block
                            text-[15px]
                            font-semibold
                            text-[#0F172A]
                            mb-2
                          "
                        >
                          Email Address
                        </label>

                        <div className={inputWrapper}>

                          <FiMail
                            className="
                              ml-4
                              mr-3
                              text-[#0B6B2B]
                            "
                            size={20}
                          />

                          <input
                            type="email"
                            value={forgotEmail}
                            onChange={(e) =>
                              setForgotEmail(
                                e.target.value
                              )
                            }
                            placeholder="Enter your email"
                            className={inputStyle}
                          />

                        </div>


                        <button
                          type="button"
                          onClick={() =>
                            setForgotMode("phone")
                          }
                          className="
                            w-full
                            h-[54px]
                            rounded-xl
                            mt-6
                            border
                            border-[#0B6B2B]
                            text-[#0B6B2B]
                            font-semibold
                            hover:bg-[#EAF6EC]
                            transition-all
                          "
                        >
                          <FiPhone
                            className="inline mr-2"
                          />

                          Reset using Phone Number
                        </button>


                        <button
                          type="button"
                          className={`${primaryButton} mt-4`}
                        >
                          Send Reset Link
                        </button>

                      </div>
                    )}


                    {/* =================================================
                        PHONE RESET
                    ================================================= */}

                    {forgotMode === "phone" && (
                      <div className="mt-10">

                        {!forgotOtpSent ? (
                          <>
                            <label
                              className="
                                block
                                text-[15px]
                                font-semibold
                                text-[#0F172A]
                                mb-2
                              "
                            >
                              Phone Number
                            </label>

                            <div className={inputWrapper}>

                              <FiPhone
                                className="
                                  ml-4
                                  mr-3
                                  text-[#0B6B2B]
                                "
                                size={20}
                              />

                              <span
                                className="
                                  text-[#526174]
                                  pr-2
                                  border-r
                                  border-[#D5E6D8]
                                "
                              >
                                +91
                              </span>

                              <input
                                type="tel"
                                value={forgotPhone}
                                onChange={(e) =>
                                  setForgotPhone(
                                    e.target.value
                                  )
                                }
                                placeholder="Enter phone number"
                                className={`${inputStyle} pl-3`}
                                maxLength={10}
                              />

                            </div>


                            <button
                              type="button"
                              onClick={
                                handleForgotSendOtp
                              }
                              className={`${primaryButton} mt-6`}
                            >
                              Send OTP
                            </button>


                            <button
                              type="button"
                              onClick={() =>
                                setForgotMode("email")
                              }
                              className="
                                flex
                                items-center
                                justify-center
                                gap-2
                                mx-auto
                                mt-6
                                text-[14px]
                                font-semibold
                                text-[#0B6B2B]
                              "
                            >
                              <FiArrowLeft />
                              Back to Email Reset
                            </button>

                          </>
                        ) : (
                          <form
                            onSubmit={
                              handlePasswordReset
                            }
                          >

                            <p
                              className="
                                text-center
                                text-[14px]
                                text-[#526174]
                                mb-7
                              "
                            >
                              Enter the OTP sent to
                              <span
                                className="
                                  block
                                  mt-1
                                  font-semibold
                                  text-[#0B6B2B]
                                "
                              >
                                +91 {forgotPhone}
                              </span>
                            </p>


                            <input
                              type="text"
                              inputMode="numeric"
                              value={forgotOtp}
                              onChange={(e) =>
                                setForgotOtp(
                                  e.target.value
                                    .replace(
                                      /\D/g,
                                      ""
                                    )
                                    .slice(0, 6)
                                )
                              }
                              placeholder="Enter OTP"
                              className="
                                w-full
                                h-14
                                rounded-xl
                                border
                                border-[#D5E6D8]
                                text-center
                                tracking-[12px]
                                text-[22px]
                                font-bold
                                outline-none
                                focus:border-[#16A34A]
                                focus:ring-4
                                focus:ring-[#EAF6EC]
                              "
                            />


                            {/* New Password */}

                            <div className={inputWrapper + " mt-5"}>

                              <FiLock
                                className="
                                  ml-4
                                  mr-3
                                  text-[#0B6B2B]
                                "
                                size={20}
                              />

                              <input
                                type={
                                  showForgotPassword
                                    ? "text"
                                    : "password"
                                }
                                value={
                                  forgotNewPassword
                                }
                                onChange={(e) =>
                                  setForgotNewPassword(
                                    e.target.value
                                  )
                                }
                                placeholder="New password"
                                className={inputStyle}
                              />

                              <button
                                type="button"
                                onClick={() =>
                                  setShowForgotPassword(
                                    !showForgotPassword
                                  )
                                }
                                className="
                                  mr-4
                                  text-[#6B7280]
                                "
                              >
                                {showForgotPassword ? (
                                  <FiEyeOff />
                                ) : (
                                  <FiEye />
                                )}
                              </button>

                            </div>


                            {/* Confirm */}

                            <div className={inputWrapper + " mt-4"}>

                              <FiLock
                                className="
                                  ml-4
                                  mr-3
                                  text-[#0B6B2B]
                                "
                                size={20}
                              />

                              <input
                                type={
                                  showForgotConfirm
                                    ? "text"
                                    : "password"
                                }
                                value={
                                  forgotConfirmPassword
                                }
                                onChange={(e) =>
                                  setForgotConfirmPassword(
                                    e.target.value
                                  )
                                }
                                placeholder="Confirm new password"
                                className={inputStyle}
                              />

                              <button
                                type="button"
                                onClick={() =>
                                  setShowForgotConfirm(
                                    !showForgotConfirm
                                  )
                                }
                                className="
                                  mr-4
                                  text-[#6B7280]
                                "
                              >
                                {showForgotConfirm ? (
                                  <FiEyeOff />
                                ) : (
                                  <FiEye />
                                )}
                              </button>

                            </div>


                            <button
                              type="submit"
                              className={`${primaryButton} mt-6`}
                            >
                              Reset Password
                            </button>

                          </form>
                        )}

                      </div>
                    )}


                    {/* Back to Login */}

                    <button
                      type="button"
                      onClick={goToLogin}
                      className="
                        flex
                        items-center
                        justify-center
                        gap-2
                        mx-auto
                        mt-8
                        text-[14px]
                        font-semibold
                        text-[#526174]
                        hover:text-[#0B6B2B]
                        transition-colors
                      "
                    >
                      <FiArrowLeft />
                      Back to Login
                    </button>

                  </>
                )}

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

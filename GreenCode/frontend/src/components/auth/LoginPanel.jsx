import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";
import {
  FiMail,
  FiLock,
  FiEye,
  FiEyeOff,
  FiX,
} from "react-icons/fi";

export default function LoginPanel({
  isOpen,
  closeLogin,
}) {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [emailOrPhone, setEmailOrPhone] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const handleLogin = async () => {
  setError("");

  if (!emailOrPhone || !password) {
    setError("Please enter email/phone and password.");
    return;
  }

  try {
    setLoading(true);

    const response = await api.post("/users/login", {
      email_or_phone: emailOrPhone,
      password: password,
    });

    const { access_token, user } = response.data;

    localStorage.setItem("access_token", access_token);
    localStorage.setItem("user", JSON.stringify(user));

    console.log("Login successful:", user);

    closeLogin();
    navigate("/dashboard");
  } catch (err) {
    console.error(err);

    setError(
      err.response?.data?.detail ||
      "Login failed. Please check your credentials."
    );
  } finally {
    setLoading(false);
  }
};
  return (
    <>
      

      {/* Login Card */}
      <div
  className={`
    fixed
    top-0
    right-0
    h-screen
    w-[520px]
    bg-[#0B0B0B]
    border-l
    border-lime-400/20
    shadow-[-10px_0_40px_rgba(145,255,0,.15)]
    z-50
    flex
    flex-col
    transition-transform
    duration-500
    ease-in-out
    ${
      isOpen
        ? "translate-x-0"
        : "translate-x-full"
    }
  `}
>

        {/* Close Button */}
        <button
          onClick={closeLogin}
          className="absolute top-6 right-6 text-zinc-400 hover:text-lime-400 transition"
        >
          <FiX size={28} />
        </button>

        <div className="px-12 pt-20">

          <h2 className="text-4xl font-bold text-center">
            Login
          </h2>

          <div className="w-20 h-1 bg-lime-400 rounded-full mx-auto mt-5 mb-14" />

          {/* Email */}

          <label className="block text-lg mb-3">
            Email Address
          </label>

          <div className="flex items-center border border-zinc-700 rounded-xl px-5 py-4 mb-8">

            <FiMail className="text-lime-400 mr-4" size={22} />

            <input
              type="text"
              placeholder="Enter your email or phone"
              value={emailOrPhone}
              onChange={(e) => setEmailOrPhone(e.target.value)}
              className="bg-transparent outline-none w-full text-lg"
            />

          </div>

          {/* Password */}

          <label className="block text-lg mb-3">
            Password
          </label>

          <div className="flex items-center border border-zinc-700 rounded-xl px-5 py-4">

            <FiLock className="text-lime-400 mr-4" size={22} />

            <input
              type={showPassword ? "text" : "password"}
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-transparent outline-none w-full text-lg"
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <FiEyeOff size={22} />
              ) : (
                <FiEye size={22} />
              )}
            </button>

          </div>

          <div className="text-right mt-3">

          <button
            type="button"
            className="text-lime-400 hover:underline"
          >
            Forgot Password?
          </button>

          </div>
          {error && (
            <p className="text-red-400 text-center mt-5">
              {error}
            </p>
          )}
          {/* Login Button */}

          <button
            onClick={handleLogin}
            disabled={loading}
            className="
              mt-10
              w-full
              bg-lime-400
              text-black
              font-bold
              text-2xl
              py-4
              rounded-xl
              hover:scale-[1.02]
              transition
              disabled:opacity-50
            "
          >
            {loading ? "Logging in..." : "Login"}
          </button>

          {/* Divider */}

          <div className="flex items-center my-10">

            <div className="flex-1 h-px bg-zinc-700" />

            <span className="mx-4 text-zinc-400">
              OR
            </span>

            <div className="flex-1 h-px bg-zinc-700" />

          </div>

          {/* Register */}

          <p className="text-center text-lg">

            Don't have an account?{" "}

            <span className="text-lime-400 cursor-pointer hover:underline">
              Register
            </span>

          </p>

        </div>
      </div>
    </>
  );
}
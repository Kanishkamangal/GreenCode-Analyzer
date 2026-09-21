import { useState } from "react";
import {
  FiUser,
  FiMail,
  FiLock,
  FiSave,
  FiEye,
  FiEyeOff,
} from "react-icons/fi";
import api from "../../services/api";
export default function EditProfile() {
  const storedUser = JSON.parse(
    localStorage.getItem("user") || "{}"
  );

  const [name, setName] = useState(
    storedUser?.name || ""
  );

  const [email] = useState(
    storedUser?.email || ""
  );

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const handleSave = async (e) => {
  e.preventDefault();

  if (!name.trim()) {
    setMessage("Full name cannot be empty.");
    return;
  }

  if (/([a-zA-Z])\1\1/i.test(name.trim())) {
    setMessage(
      "Name cannot contain three consecutive identical characters."
    );
    return;
  }

  if (!/^[A-Za-z ]+$/.test(name.trim())) {
    setMessage(
      "Name cannot contain numbers or special characters."
    );
    return;
  }

  if (password || confirmPassword) {

    if (!password || !confirmPassword) {
      setMessage(
        "Please enter both new password and confirm password."
      );
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Passwords do not match.");
      return;
    }
  }

  try {

    setSaving(true);
    setMessage("");

    const payload = {
      name: name.trim(),
    };

    if (password) {
      payload.password = password;
    }

    const response = await api.put(
      `/users/${storedUser.user_id}`,
      payload
    );

    const updatedUser = {
      ...storedUser,
      name: response.data.name,
    };

    localStorage.setItem(
      "user",
      JSON.stringify(updatedUser)
    );

    setName(response.data.name);

    setPassword("");
    setConfirmPassword("");

    setMessage(
      "Profile Updated successfully!"
    );

    setTimeout(() => {
      setMessage("");
    }, 3000);

  } catch (error) {

    console.error(
      "Profile update error:",
      error
    );

    const detail =
      error.response?.data?.detail;

    if (Array.isArray(detail)) {

      setMessage(
        detail[0]?.msg?.replace(
          "Value error, ",
          ""
        ) ||
        "Unable to update profile."
      );

    } else {

      setMessage(
        detail ||
        "Unable to update profile."
      );

    }

  } finally {

    setSaving(false);

  }
};


  return (
    <div className="max-w-4xl mx-auto">

      {/* HEADER */}

      <div className="mb-8">
        <p className="text-[#0B6B2B] text-xs uppercase tracking-[0.25em] font-semibold">
          Account
        </p>

        <h1 className="mt-3 text-3xl md:text-4xl font-semibold text-[#0F172A]">
          Edit Profile
        </h1>

        <p className="mt-2 text-[#6B7280]">
          Update your GreenCode Analyzer account information.
        </p>
      </div>


      {/* PROFILE CARD */}

      <div
        className="
          bg-white
          rounded-2xl
          border
          border-[#DDE8DF]
          shadow-[0_8px_30px_rgba(15,23,42,0.04)]
          overflow-hidden
        "
      >

        {/* PROFILE HEADER */}

        <div
          className="
            px-6
            py-6
            md:px-8
            bg-[#F3F8F4]
            border-b
            border-[#E2ECE4]
            flex
            items-center
            gap-5
          "
        >

          <div
            className="
              w-16
              h-16
              rounded-full
              bg-[#E6F2E6]
              border
              border-[#C6DCC9]
              flex
              items-center
              justify-center
              text-[#0B6B2B]
            "
          >
            <FiUser size={28} />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-[#0F172A]">
              Profile Information
            </h2>

            <p className="text-sm text-[#6B7280] mt-1">
              Manage your personal account details.
            </p>
          </div>

        </div>


        {/* FORM */}

        <form onSubmit={handleSave} className="p-6 md:p-8">

          <div className="grid md:grid-cols-2 gap-6">

            {/* NAME */}

            <div>
              <label className="block text-sm font-medium text-[#334155] mb-2">
                Full Name
              </label>

              <div className="relative">

                <FiUser
                  className="
                    absolute
                    left-4
                    top-1/2
                    -translate-y-1/2
                    text-[#6B7280]
                  "
                  size={18}
                />

                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="
                    w-full
                    pl-11
                    pr-4
                    py-3
                    rounded-xl
                    border
                    border-[#DDE8DF]
                    bg-white
                    text-[#0F172A]
                    outline-none
                    transition
                    focus:border-[#0B6B2B]
                    focus:ring-2
                    focus:ring-[#0B6B2B]/10
                  "
                />

              </div>
            </div>


            {/* EMAIL */}

            <div>
              <label className="block text-sm font-medium text-[#334155] mb-2">
                Email Address
              </label>

              <div className="relative">

                <FiMail
                  className="
                    absolute
                    left-4
                    top-1/2
                    -translate-y-1/2
                    text-[#6B7280]
                  "
                  size={18}
                />

                <input 
                  type="email" 
                  value={email}
                  readOnly
                  className="
                    w-full
                    pl-11
                    pr-4
                    py-3
                    rounded-xl
                    border
                    border-[#DDE8DF]
                    bg-[#F8FAFC]
                    cursor-not-allowed
                    text-[#0F172A]
                    outline-none
                    transition
                    focus:border-[#0B6B2B]
                    focus:ring-2
                    focus:ring-[#0B6B2B]/10
                  "
                />

              </div>
              <p className="mt-2 text-xs text-[#94A3B8]">
                Email address cannot be changed from profile settings.
              </p>
            </div>

            {/* PASSWORD */}

            <div>
              <label className="block text-sm font-medium text-[#334155] mb-2">
                New Password
              </label>

            <div className="relative">

  <FiLock
    className="
      absolute
      left-4
      top-1/2
      -translate-y-1/2
      text-[#6B7280]
    "
    size={18}
  />

  <input
    type={showPassword ? "text" : "password"}
    value={password}
    onChange={(e) => setPassword(e.target.value)}
    placeholder="Leave blank to keep current"
    className="
      w-full
      pl-11
      pr-12
      py-3
      rounded-xl
      border
      border-[#DDE8DF]
      bg-white
      text-[#0F172A]
      placeholder:text-[#9CA3AF]
      outline-none
      transition
      focus:border-[#0B6B2B]
      focus:ring-2
      focus:ring-[#0B6B2B]/10
    "
  />

  <button
    type="button"
    onClick={() => setShowPassword(!showPassword)}
    className="
      absolute
      right-4
      top-1/2
      -translate-y-1/2
      text-[#6B7280]
      hover:text-[#0B6B2B]
    "
  >
    {showPassword ? (
      <FiEyeOff size={18} />
    ) : (
      <FiEye size={18} />
    )}
  </button>

</div>
            </div>


            {/* CONFIRM PASSWORD */}

            <div>
              <label className="block text-sm font-medium text-[#334155] mb-2">
                Confirm Password
              </label>

              <div className="relative">

  <FiLock
    className="
      absolute
      left-4
      top-1/2
      -translate-y-1/2
      text-[#6B7280]
    "
    size={18}
  />

  <input
    type={showConfirmPassword ? "text" : "password"}
    value={confirmPassword}
    onChange={(e) => setConfirmPassword(e.target.value)}
    placeholder="Confirm new password"
    className="
      w-full
      pl-11
      pr-12
      py-3
      rounded-xl
      border
      border-[#DDE8DF]
      bg-white
      text-[#0F172A]
      placeholder:text-[#9CA3AF]
      outline-none
      transition
      focus:border-[#0B6B2B]
      focus:ring-2
      focus:ring-[#0B6B2B]/10
    "
  />

  <button
    type="button"
    onClick={() =>
      setShowConfirmPassword(!showConfirmPassword)
    }
    className="
      absolute
      right-4
      top-1/2
      -translate-y-1/2
      text-[#6B7280]
      hover:text-[#0B6B2B]
    "
  >
    {showConfirmPassword ? (
      <FiEyeOff size={18} />
    ) : (
      <FiEye size={18} />
    )}
  </button>

</div>
            </div>

          </div>


          {/* MESSAGE */}

          {message && (
            <div
              className={`
                mt-6
                px-4
                py-3
                rounded-xl
                text-sm
                ${
                  message.includes("successfully")
                    ? "bg-[#EAF6EC] text-[#0B6B2B] border border-[#CFE2D2]"
                    : "bg-red-50 text-red-600 border border-red-100"
                }
              `}
            >
              {message}
            </div>
          )}


          {/* SAVE */}

          <div className="mt-8 flex justify-end">

              <button
                type="submit"
                disabled={saving}
              className="
                inline-flex
                items-center
                gap-2
                px-6
                py-3
                rounded-xl
                bg-[#0B6B2B]
                text-white
                font-semibold
                hover:bg-[#095A24]
                hover:-translate-y-0.5
                transition-all
                shadow-[0_6px_18px_rgba(11,107,43,0.15)]
                disabled:opacity-50
                disabled:cursor-not-allowed
              "
            >
              <FiSave size={17} />
              Save Changes
            </button>

          </div>

        </form>

      </div>

    </div>
  );
}
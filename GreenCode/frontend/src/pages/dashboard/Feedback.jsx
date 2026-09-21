import { useState } from "react";
import {
  FiMessageSquare,
  FiSend,
  FiStar,
} from "react-icons/fi";
import api from "../../services/api";
export default function Feedback() {
  const [rating, setRating] = useState(0);
  const [category, setCategory] = useState("General");
  const [message, setMessage] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const canSubmit =
  rating > 0 ||
  message.trim().length > 0;
  const handleSubmit = async (e) => {
  e.preventDefault();

  if (!canSubmit) {
    return;
  }

  const storedUser = JSON.parse(
    localStorage.getItem("user") || "{}"
  );

  if (!storedUser?.user_id) {
    setSubmitError(
      "User information not found. Please login again."
    );
    return;
  }

  try {
    setSubmitting(true);
    setSubmitError("");
    setSubmitted(false);

    await api.post("/feedback/", {
      user_id: storedUser.user_id,

      rating:
        rating > 0
          ? rating
          : null,

      category: category,

      feedback_text:
        message.trim()
          ? message.trim()
          : null,
    });

    setSubmitted(true);

    setRating(0);
    setCategory("General");
    setMessage("");

    setTimeout(() => {
      setSubmitted(false);
    }, 4000);

  } catch (error) {
    console.error(
      "Feedback submission error:",
      error
    );

    setSubmitError(
      error.response?.data?.detail ||
      "Unable to submit feedback. Please try again."
    );

  } finally {
    setSubmitting(false);
  }
};

  return (
    <div className="max-w-4xl mx-auto">

      {/* HEADER */}

      <div className="mb-8">

        <p className="text-[#0B6B2B] text-xs uppercase tracking-[0.25em] font-semibold">
          Feedback
        </p>

        <h1 className="mt-3 text-3xl md:text-4xl font-semibold text-[#0F172A]">
          Send Feedback
        </h1>

        <p className="mt-2 text-[#6B7280]">
          Help us improve GreenCode Analyzer by sharing your experience.
        </p>

      </div>


      {/* CARD */}

      <div
        className="
          bg-white
          rounded-2xl
          border
          border-[#DDE8DF]
          shadow-[0_8px_30px_rgba(15,23,42,0.04)]
          p-6
          md:p-8
        "
      >

        <div className="flex items-center gap-4 mb-8">

          <div
            className="
              w-12
              h-12
              rounded-xl
              bg-[#EAF6EC]
              text-[#0B6B2B]
              flex
              items-center
              justify-center
            "
          >
            <FiMessageSquare size={22} />
          </div>

          <div>

            <h2 className="text-lg font-semibold text-[#0F172A]">
              We'd love to hear from you
            </h2>

            <p className="text-sm text-[#6B7280] mt-1">
              Your feedback helps us make the analyzer better.
            </p>

          </div>

        </div>


        <form onSubmit={handleSubmit}>

          {/* RATING */}

          <div className="mb-7">

            <label className="block text-sm font-medium text-[#334155] mb-3">
              How would you rate your experience?
            </label>

            <div className="flex gap-2">

              {[1, 2, 3, 4, 5].map((star) => (

                <button
                  key={star}
                  type="button"
                  onClick={() => setRating(star)}
                  className={`
                    w-10
                    h-10
                    rounded-lg
                    border
                    flex
                    items-center
                    justify-center
                    transition
                    ${
                      rating >= star
                        ? "bg-[#EAF6EC] border-[#A5CBAA] text-[#0B6B2B]"
                        : "bg-white border-[#DDE8DF] text-[#9CA3AF] hover:border-[#A5CBAA]"
                    }
                  `}
                >
                  <FiStar
                    size={18}
                    className={rating >= star ? "fill-current" : ""}
                  />
                </button>

              ))}

            </div>

          </div>


          {/* CATEGORY */}

          <div className="mb-7">

            <label className="block text-sm font-medium text-[#334155] mb-2">
              Feedback Category
            </label>

            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="
                w-full
                px-4
                py-3
                rounded-xl
                border
                border-[#DDE8DF]
                bg-white
                text-[#0F172A]
                outline-none
                focus:border-[#0B6B2B]
                focus:ring-2
                focus:ring-[#0B6B2B]/10
              "
            >
              <option value="General">
                General
              </option>

              <option value="Bug Report">
                Bug Report
              </option>

              <option value="Performance Issue">
                Performance Issue
              </option>

              <option value="UI/UX Feedback">
                UI/UX Feedback
              </option>

              <option value="Feature Request">
                Feature Request
              </option>

              <option value="Benchmark Accuracy">
                Benchmark Accuracy
              </option>

              <option value="Other">
                Other
              </option>
            </select>

          </div>


          {/* MESSAGE */}

          <div className="mb-7">

            <label className="block text-sm font-medium text-[#334155] mb-2">
              Your Feedback
            </label>

            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={6}
              placeholder="Tell us what you think..."
              className="
                w-full
                px-4
                py-3
                rounded-xl
                border
                border-[#DDE8DF]
                bg-white
                text-[#0F172A]
                placeholder:text-[#9CA3AF]
                resize-none
                outline-none
                focus:border-[#0B6B2B]
                focus:ring-2
                focus:ring-[#0B6B2B]/10
              "
            />

          </div>


          {/* SUCCESS */}

          {submitted && (
            <div
              className="
                mb-6
                px-4
                py-3
                rounded-xl
                bg-[#EAF6EC]
                border
                border-[#CFE2D2]
                text-[#0B6B2B]
                text-sm
              "
            >
              Thank you! Your feedback has been submitted successfully.
            </div>
          )}
          {submitError && (
            <div
              className="
                mb-6
                px-4
                py-3
                rounded-xl
                bg-red-50
                border
                border-red-200
                text-red-700
                text-sm
              "
            >
              {submitError}
            </div>
          )}

          {/* SUBMIT */}

          <div className="flex justify-end">

            <button
              type="submit"
              disabled={!canSubmit || submitting}  
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
                disabled:opacity-40
                disabled:cursor-not-allowed
                transition
              "
            >
              <FiSend size={17} />
              {submitting
                ? "Submitting..."
                : "Submit Feedback"}
            </button>

          </div>

        </form>

      </div>

    </div>
  );
}
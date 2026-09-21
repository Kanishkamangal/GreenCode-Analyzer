import { useState } from "react";
import {
  FiHelpCircle,
  FiChevronDown,
  FiBookOpen,
  FiMail,
} from "react-icons/fi";

export default function Help() {
  const [openIndex, setOpenIndex] = useState(null);

  const faqs = [
    {
      question: "What is GreenCode Analyzer?",
      answer:
        "GreenCode Analyzer compares programs across programming languages using metrics such as execution time, CPU usage, memory usage, and estimated energy consumption.",
    },
    {
      question: "How do I run a benchmark?",
      answer:
        "Open Run Benchmark from the sidebar, select your benchmark task, choose the programming languages you want to compare, select the metrics, and start the benchmark.",
    },
    {
      question: "Where can I see previous benchmarks?",
      answer:
        "You can find your previous benchmark executions under Benchmark History in the dashboard sidebar.",
    },
    {
      question: "Where are generated reports stored?",
      answer:
        "Generated benchmark reports can be accessed from the Reports section of your dashboard.",
    },
    {
      question: "Can I change my account information?",
      answer:
        "Yes. Open your profile menu in the top-right corner and select Edit Profile to update your account information.",
    },
    {
      question: "How can I report a problem?",
      answer:
        "Use Send Feedback from your profile menu and select Bug Report as the feedback category. Describe the issue clearly so it can be investigated.",
    },
  ];

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="max-w-5xl mx-auto">

      {/* HEADER */}

      <div className="mb-8">

        <p className="text-[#0B6B2B] text-xs uppercase tracking-[0.25em] font-semibold">
          Support
        </p>

        <h1 className="mt-3 text-3xl md:text-4xl font-semibold text-[#0F172A]">
          Help Center
        </h1>

        <p className="mt-2 text-[#6B7280]">
          Find answers to common questions about GreenCode Analyzer.
        </p>

      </div>


      {/* QUICK HELP CARDS */}

      <div className="grid md:grid-cols-2 gap-5 mb-8">

        <div
          className="
            bg-white
            border
            border-[#DDE8DF]
            rounded-2xl
            p-6
            shadow-[0_8px_30px_rgba(15,23,42,0.04)]
          "
        >

          <div
            className="
              w-11
              h-11
              rounded-xl
              bg-[#EAF6EC]
              text-[#0B6B2B]
              flex
              items-center
              justify-center
              mb-4
            "
          >
            <FiBookOpen size={21} />
          </div>

          <h2 className="text-lg font-semibold text-[#0F172A]">
            Getting Started
          </h2>

          <p className="mt-2 text-sm text-[#6B7280] leading-6">
            Select a benchmark, choose the languages you want to compare,
            select your metrics, and start analyzing.
          </p>

        </div>


        <div
          className="
            bg-white
            border
            border-[#DDE8DF]
            rounded-2xl
            p-6
            shadow-[0_8px_30px_rgba(15,23,42,0.04)]
          "
        >

          <div
            className="
              w-11
              h-11
              rounded-xl
              bg-[#EAF6EC]
              text-[#0B6B2B]
              flex
              items-center
              justify-center
              mb-4
            "
          >
            <FiMail size={21} />
          </div>

          <h2 className="text-lg font-semibold text-[#0F172A]">
            Need More Help?
          </h2>

          <p className="mt-2 text-sm text-[#6B7280] leading-6">
            Can't find what you're looking for? Send us feedback and
            describe your question or problem.
          </p>

        </div>

      </div>


      {/* FAQ */}

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

        <div className="px-6 py-5 border-b border-[#E8EEE9]">

          <div className="flex items-center gap-3">

            <FiHelpCircle
              size={21}
              className="text-[#0B6B2B]"
            />

            <h2 className="text-lg font-semibold text-[#0F172A]">
              Frequently Asked Questions
            </h2>

          </div>

        </div>


        <div>

          {faqs.map((faq, index) => (

            <div
              key={index}
              className="border-b border-[#E8EEE9] last:border-b-0"
            >

              <button
                onClick={() => toggleFAQ(index)}
                className="
                  w-full
                  px-6
                  py-5
                  flex
                  items-center
                  justify-between
                  gap-5
                  text-left
                  hover:bg-[#F7FAF8]
                  transition
                "
              >

                <span className="text-sm md:text-base font-medium text-[#334155]">
                  {faq.question}
                </span>

                <FiChevronDown
                  size={18}
                  className={`
                    shrink-0
                    text-[#6B7280]
                    transition-transform
                    duration-200
                    ${
                      openIndex === index
                        ? "rotate-180 text-[#0B6B2B]"
                        : ""
                    }
                  `}
                />

              </button>


              {openIndex === index && (

                <div className="px-6 pb-5">

                  <p className="text-sm text-[#6B7280] leading-6 max-w-3xl">
                    {faq.answer}
                  </p>

                </div>

              )}

            </div>

          ))}

        </div>

      </div>

    </div>
  );
}
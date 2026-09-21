import { useState } from "react";
import { FiChevronDown } from "react-icons/fi";

export default function FAQs() {
  const [openIndex, setOpenIndex] = useState(null);

  const faqs = [
    {
      question: "What is GreenCode Analyzer?",
      answer:
        "GreenCode Analyzer is a benchmarking platform that compares programs across programming languages using metrics such as execution time, CPU utilization, memory usage and estimated energy consumption.",
    },
    {
      question: "What programming languages are supported?",
      answer:
        "The platform is designed to compare multiple languages including C, C++, Java, Python, JavaScript, Go, Rust, C#, Kotlin and PHP.",
    },
    {
      question: "What metrics does GreenCode Analyzer measure?",
      answer:
        "GreenCode Analyzer focuses on execution time, CPU utilization, memory usage and energy consumption. These measurements are combined to provide an overall efficiency score.",
    },
    {
      question: "Can I compare multiple languages at the same time?",
      answer:
        "Yes. You can select multiple programming languages and run the same benchmark across them, allowing you to compare their performance and resource usage.",
    },
    {
      question: "What benchmarks can I run?",
      answer:
        "You can run predefined benchmarks such as sorting, matrix multiplication, Fibonacci calculations and prime number calculations. A custom benchmark option can also be used for your own program.",
    },
    {
      question: "How is the Green Score calculated?",
      answer:
        "The Green Score provides an overall comparison of resource efficiency by considering benchmark performance and resource consumption. A higher score indicates better overall efficiency.",
    },
    {
      question: "Can I view previous benchmark results?",
      answer:
        "Yes. Completed benchmark runs can be stored in Benchmark History, allowing you to review previous executions and compare results.",
    },
    {
      question: "Can I generate reports?",
      answer:
        "Yes. GreenCode Analyzer can generate reports containing benchmark information and comparative results that can be reviewed or downloaded.",
    },
  ];

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section
      id="faqs"
      className="
        py-24
        px-6
        md:px-10
        bg-white
      "
    >

      {/* =================================================
          HEADER
      ================================================= */}

      <div className="max-w-3xl mx-auto text-center">

        <p
          className="
            text-[#16A34A]
            text-xs
            uppercase
            tracking-[0.25em]
            font-semibold
          "
        >
          FAQs
        </p>

        <h2
          className="
            mt-4
            text-3xl
            md:text-5xl
            font-bold
            text-[#0F172A]
          "
        >
          Frequently Asked
          <span className="text-[#0B6B2B]"> Questions</span>
        </h2>

        <p
          className="
            mt-5
            text-[#526174]
            text-base
            md:text-lg
            leading-8
          "
        >
          Everything you need to know about benchmarking, measurements and
          comparing programming languages.
        </p>

      </div>


      {/* =================================================
          FAQ LIST
      ================================================= */}

      <div className="max-w-4xl mx-auto mt-14 space-y-4">

        {faqs.map((faq, index) => {
          const isOpen = openIndex === index;

          return (
            <div
              key={index}
              className={`
                rounded-2xl
                border
                transition-all
                duration-300
                ${
                  isOpen
                    ? "border-[#B9D9BF] bg-[#F9FAFA] shadow-[0_8px_25px_rgba(11,107,43,0.05)]"
                    : "border-[#E1E9E2] bg-white hover:border-[#CFE2D2]"
                }
              `}
            >

              {/* QUESTION */}

              <button
                onClick={() => toggleFAQ(index)}
                className="
                  w-full
                  flex
                  items-center
                  justify-between
                  gap-6
                  text-left
                  px-6
                  py-5
                "
              >

                <span
                  className={`
                    text-base
                    md:text-lg
                    font-semibold
                    transition-colors
                    ${
                      isOpen
                        ? "text-[#0B6B2B]"
                        : "text-[#0F172A]"
                    }
                  `}
                >
                  {faq.question}
                </span>

                <span
                  className={`
                    shrink-0
                    w-9
                    h-9
                    rounded-full
                    flex
                    items-center
                    justify-center
                    transition-all
                    duration-300
                    ${
                      isOpen
                        ? "bg-[#0B6B2B] text-white rotate-180"
                        : "bg-[#E6F2E6] text-[#0B6B2B]"
                    }
                  `}
                >
                  <FiChevronDown size={18} />
                </span>

              </button>


              {/* ANSWER */}

              <div
                className={`
                  grid
                  transition-all
                  duration-300
                  ${
                    isOpen
                      ? "grid-rows-[1fr] opacity-100"
                      : "grid-rows-[0fr] opacity-0"
                  }
                `}
              >

                <div className="overflow-hidden">

                  <p
                    className="
                      px-6
                      pb-6
                      pr-16
                      text-sm
                      md:text-base
                      leading-7
                      text-[#526174]
                    "
                  >
                    {faq.answer}
                  </p>

                </div>

              </div>

            </div>
          );
        })}

      </div>


      {/* =================================================
          BOTTOM CARD
      ================================================= */}

      <div
        className="
          max-w-4xl
          mx-auto
          mt-14
          rounded-2xl
          bg-[#E6F2E6]
          border
          border-[#CFE2D2]
          px-6
          py-7
          text-center
        "
      >

        <h3
          className="
            text-lg
            font-semibold
            text-[#0F172A]
          "
        >
          Still have questions?
        </h3>

        <p
          className="
            mt-2
            text-sm
            text-[#526174]
          "
        >
          You can explore the dashboard or run your first benchmark to see
          GreenCode Analyzer in action.
        </p>

      </div>

    </section>
  );
}
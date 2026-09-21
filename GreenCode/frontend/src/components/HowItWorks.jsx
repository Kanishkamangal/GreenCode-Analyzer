import {
  FiCode,
  FiGlobe,
  FiPlayCircle,
  FiBarChart2,
  FiZap,
  FiAward,
} from "react-icons/fi";

export default function HowItWorks() {
  const steps = [
    {
      number: "01",
      icon: FiCode,
      title: "Select Your Program",
      description:
        "Choose a benchmark such as sorting, matrix multiplication, Fibonacci, or create your own benchmark.",
    },
    {
      number: "02",
      icon: FiGlobe,
      title: "Choose Languages",
      description:
        "Select the programming languages you want to compare, including C, C++, Java, Python, Go, Rust and more.",
    },
    {
      number: "03",
      icon: FiPlayCircle,
      title: "Run Benchmark",
      description:
        "GreenCode Analyzer executes the same benchmark across the selected programming languages.",
    },
    {
      number: "04",
      icon: FiBarChart2,
      title: "Measure Resources",
      description:
        "The system evaluates execution time, CPU utilization, memory usage and estimated energy consumption.",
    },
    {
      number: "05",
      icon: FiZap,
      title: "Compare Results",
      description:
        "View clear performance and energy comparisons through tables, scores and visual insights.",
    },
    {
      number: "06",
      icon: FiAward,
      title: "Find the Efficient Option",
      description:
        "Identify which language provides the best balance between performance and resource efficiency.",
    },
  ];

  return (
    <section
      id="how-it-works"
      className="
        relative
        py-24
        px-6
        md:px-10
        bg-[#F9FAFA]
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
          How It Works
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
          From Code to
          <span className="text-[#0B6B2B]"> Insights</span>
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
          GreenCode Analyzer makes it simple to understand how your code
          performs and how efficiently it uses computing resources.
        </p>

      </div>


      {/* =================================================
          STEPS
      ================================================= */}

      <div
        className="
          max-w-6xl
          mx-auto
          mt-16
          grid
          md:grid-cols-2
          xl:grid-cols-3
          gap-6
        "
      >

        {steps.map((step) => {
          const Icon = step.icon;

          return (
            <div
              key={step.number}
              className="
                group
                relative
                bg-white
                border
                border-[#DDE8DF]
                rounded-2xl
                p-7
                shadow-[0_8px_30px_rgba(15,23,42,0.04)]
                hover:-translate-y-1
                hover:border-[#B9D9BF]
                hover:shadow-[0_14px_35px_rgba(11,107,43,0.08)]
                transition-all
                duration-300
              "
            >

              {/* NUMBER */}

              <div className="flex items-center justify-between">

                <div
                  className="
                    w-12
                    h-12
                    rounded-xl
                    bg-[#E6F2E6]
                    text-[#0B6B2B]
                    flex
                    items-center
                    justify-center
                    group-hover:bg-[#0B6B2B]
                    group-hover:text-white
                    transition-all
                    duration-300
                  "
                >
                  <Icon size={22} />
                </div>

                <span
                  className="
                    text-3xl
                    font-bold
                    text-[#E3EEE5]
                  "
                >
                  {step.number}
                </span>

              </div>


              {/* CONTENT */}

              <h3
                className="
                  mt-6
                  text-lg
                  font-semibold
                  text-[#0F172A]
                "
              >
                {step.title}
              </h3>

              <p
                className="
                  mt-3
                  text-sm
                  leading-6
                  text-[#526174]
                "
              >
                {step.description}
              </p>

            </div>
          );
        })}

      </div>


      {/* =================================================
          BOTTOM MESSAGE
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

        <p
          className="
            text-[#0B6B2B]
            font-semibold
            text-lg
          "
        >
          Measure. Compare. Optimize.
        </p>

        <p
          className="
            mt-2
            text-sm
            text-[#526174]
          "
        >
          Make informed decisions about the performance and energy efficiency
          of your code.
        </p>

      </div>

    </section>
  );
}
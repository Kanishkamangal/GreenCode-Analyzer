import { useEffect, useRef } from "react";
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import AboutUs from "../components/AboutUs";
import HowItWorks from "../components/HowItWorks";
import FAQs from "../components/FAQs";

export default function Home({ onLogin }) {
  const homeRef = useRef(null);

  useEffect(() => {
    const root = homeRef.current;
    if (!root) return;

    const reducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    // Keep the first viewport immediately usable. Motion is applied to
    // the landing-page sections below/around the hero, not to navigation.
    const sections = Array.from(root.querySelectorAll("main > section:not(#home)"));

    sections.forEach((section, index) => {
      section.dataset.gcHomeSection = "true";
      section.style.setProperty(
        "--gc-section-delay",
        `${Math.min(index * 70, 280)}ms`
      );

      // Give sections a direction so the page does not feel like one
      // repeated fade animation.
      if (index % 3 === 1) section.dataset.gcMotion = "left";
      else if (index % 3 === 2) section.dataset.gcMotion = "right";
      else section.dataset.gcMotion = "up";
    });

    if (reducedMotion) {
      sections.forEach((section) => {
        section.classList.add("gc-home-visible");
      });
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("gc-home-visible");
          } else {
            // Re-trigger the entrance when the user scrolls back.
            entry.target.classList.remove("gc-home-visible");
          }
        });
      },
      {
        threshold: 0.12,
        rootMargin: "-7% 0px -10% 0px",
      }
    );

    sections.forEach((section) => observer.observe(section));

    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={homeRef}
      className="
        gc-home-page
        min-h-screen
        overflow-x-hidden
        bg-[#F9FAFA]
        text-[#0F172A]
      "
    >
      <Navbar onLogin={onLogin} />

      <main>
        <Hero />
        <AboutUs />
        <HowItWorks />
        <FAQs />
      </main>

      <style>{`
        /* =========================================================
           GREENCODE LANDING-PAGE SCROLL CHOREOGRAPHY
           The page moves as a continuous story:
           HERO -> MEASURE -> COMPARE -> OPTIMIZE -> HOW IT WORKS -> FAQ
        ========================================================= */

        .gc-home-page main > section[data-gc-home-section] {
          position: relative;
          opacity: 0;
          filter: blur(9px);
          transform:
            translate3d(0, 72px, 0)
            scale(.975);
          transition:
            opacity .82s cubic-bezier(.22, 1, .36, 1),
            transform .95s cubic-bezier(.22, 1, .36, 1),
            filter .82s cubic-bezier(.22, 1, .36, 1);
          transition-delay: var(--gc-section-delay);
          will-change: opacity, transform, filter;
        }

        .gc-home-page main > section[data-gc-home-section][data-gc-motion="left"] {
          transform:
            translate3d(-68px, 35px, 0)
            scale(.975);
        }

        .gc-home-page main > section[data-gc-home-section][data-gc-motion="right"] {
          transform:
            translate3d(68px, 35px, 0)
            scale(.975);
        }

        .gc-home-page main > section[data-gc-home-section].gc-home-visible {
          opacity: 1;
          filter: blur(0);
          transform: translate3d(0, 0, 0) scale(1);
        }

        /* Sub-elements inside each landing section reveal in sequence.
           Existing semantic elements remain untouched. */
        .gc-home-page main > section.gc-home-visible h1,
        .gc-home-page main > section.gc-home-visible h2,
        .gc-home-page main > section.gc-home-visible h3 {
          animation: gcHomeTextIn .72s cubic-bezier(.22, 1, .36, 1) both;
        }

        .gc-home-page main > section.gc-home-visible p {
          animation: gcHomeTextIn .72s .08s cubic-bezier(.22, 1, .36, 1) both;
        }

        .gc-home-page main > section.gc-home-visible a,
        .gc-home-page main > section.gc-home-visible button {
          animation: gcHomeControlIn .7s .16s cubic-bezier(.22, 1, .36, 1) both;
        }

        .gc-home-page main > section.gc-home-visible > div {
          animation: gcHomeContentIn .78s .04s cubic-bezier(.22, 1, .36, 1) both;
        }

        @keyframes gcHomeTextIn {
          from {
            opacity: 0;
            transform: translate3d(0, 22px, 0);
            filter: blur(5px);
          }
          to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
            filter: blur(0);
          }
        }

        @keyframes gcHomeContentIn {
          from {
            opacity: .25;
            transform: translate3d(0, 28px, 0);
          }
          to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
          }
        }

        @keyframes gcHomeControlIn {
          from {
            opacity: 0;
            transform: translate3d(0, 18px, 0) scale(.97);
          }
          to {
            opacity: 1;
            transform: translate3d(0, 0, 0) scale(1);
          }
        }

        /* A subtle technical scan line follows the section as it enters. */
        .gc-home-page main > section[data-gc-home-section]::after {
          content: "";
          pointer-events: none;
          position: absolute;
          left: 8%;
          right: 8%;
          top: 0;
          height: 1px;
          opacity: 0;
          transform: scaleX(0);
          transform-origin: left;
          background: linear-gradient(
            90deg,
            transparent,
            rgba(22, 163, 74, .35),
            transparent
          );
        }

        .gc-home-page main > section[data-gc-home-section].gc-home-visible::after {
          opacity: 1;
          transform: scaleX(1);
          transition:
            opacity .4s ease .2s,
            transform 1s cubic-bezier(.22, 1, .36, 1) .2s;
        }

        @media (max-width: 1024px) {
          .gc-home-page main > section[data-gc-home-section] {
            transform: translate3d(0, 48px, 0) scale(.985);
          }

          .gc-home-page main > section[data-gc-home-section][data-gc-motion="left"],
          .gc-home-page main > section[data-gc-home-section][data-gc-motion="right"] {
            transform: translate3d(0, 48px, 0) scale(.985);
          }
        }

        @media (prefers-reduced-motion: reduce) {
          .gc-home-page main > section[data-gc-home-section],
          .gc-home-page main > section[data-gc-home-section][data-gc-motion="left"],
          .gc-home-page main > section[data-gc-home-section][data-gc-motion="right"],
          .gc-home-page main > section.gc-home-visible h1,
          .gc-home-page main > section.gc-home-visible h2,
          .gc-home-page main > section.gc-home-visible h3,
          .gc-home-page main > section.gc-home-visible p,
          .gc-home-page main > section.gc-home-visible a,
          .gc-home-page main > section.gc-home-visible button,
          .gc-home-page main > section.gc-home-visible > div {
            opacity: 1 !important;
            filter: none !important;
            transform: none !important;
            animation: none !important;
            transition: none !important;
          }
        }
      `}</style>
    </div>
  );
}
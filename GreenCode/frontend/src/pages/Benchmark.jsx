import React, { useEffect, useMemo, useRef, useState } from "react";
import api from "../services/api";
import Editor from "@monaco-editor/react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
/* =========================================================
   LANGUAGE DATA
========================================================= */

const LANGUAGES = [
  {
    name: "C",
    extension: "c",
    code: `#include <stdio.h>

int main() {
    printf("Hello World");
    return 0;
}`,
  },

  {
    name: "C++",
    extension: "cpp",
    code: `#include <iostream>

int main() {
    std::cout << "Hello World";
    return 0;
}`,
  },

  {
    name: "Java",
    extension: "java",
    code: `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}`,
  },

  {
    name: "Python",
    extension: "py",
    code: `print("Hello World")`,
  },

  {
    name: "JavaScript",
    extension: "js",
    code: `console.log("Hello World");`,
  },

  {
    name: "Go",
    extension: "go",
    code: `package main

import "fmt"

func main() {
    fmt.Println("Hello World")
}`,
  },

  {
    name: "Rust",
    extension: "rs",
    code: `fn main() {
    println!("Hello World");
}`,
  },

  {
    name: "C#",
    extension: "cs",
    code: `using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello World");
    }
}`,
  },

  {
    name: "Kotlin",
    extension: "kt",
    code: `fun main() {
    println("Hello World")
}`,
  },

  {
    name: "PHP",
    extension: "php",
    code: `<?php
echo "Hello World";
?>`,
  },
];
const MONACO_LANGUAGE_MAP = {
  C: "c",
  "C++": "cpp",
  Java: "java",
  Python: "python",
  JavaScript: "javascript",
  Go: "go",
  Rust: "rust",
  "C#": "csharp",
  Kotlin: "kotlin",
  PHP: "php",
};

const LANGUAGE_LOGOS = {
  C: { label: "C", className: "bg-[#5B7DB1] text-white" },
  "C++": { label: "C++", className: "bg-[#2F68A5] text-white" },
  Java: { label: "☕", className: "bg-[#B8322C] text-white" },
  Python: { label: "Py", className: "bg-[#3776AB] text-white" },
  JavaScript: { label: "JS", className: "bg-[#D6B400] text-[#111827]" },
  Go: { label: "Go", className: "bg-[#2AA7C7] text-white" },
  Rust: { label: "R", className: "bg-[#CE422B] text-white" },
  "C#": { label: "C#", className: "bg-[#68217A] text-white" },
  Kotlin: { label: "K", className: "bg-[#7F52FF] text-white" },
  PHP: { label: "php", className: "bg-[#777BB4] text-white" },
};
const METRICS = [
  "Execution Time",
  "CPU Usage",
  "Memory Usage",
  "Energy Consumption",
];



/* =========================================================
   MAIN COMPONENT
========================================================= */

export default function Benchmark() {
  const [benchmarks, setBenchmarks] = useState([]);
  const [languages, setLanguages] = useState([]);
  const [loadingData, setLoadingData] = useState(true);
  const [dataError, setDataError] = useState("");
  /* =========================================================
     BENCHMARK MODE
  ========================================================= */

  const [benchmarkType, setBenchmarkType] =
    useState("predefined");
  /* =========================================================
     PREDEFINED SETTINGS
  ========================================================= */

  const [benchmark, setBenchmark] =
    useState("");

  const [benchmarkSize, setBenchmarkSize] =
    useState("medium");

  /* =========================================================
     LANGUAGE SELECTION
  ========================================================= */

  const [selectedLanguages, setSelectedLanguages] =
    useState([]);
  /* =========================================================
     CUSTOM BENCHMARK
  ========================================================= */
  const [benchmarkCategory, setBenchmarkCategory] =
    useState("");

  const [customInputSize, setCustomInputSize] =
    useState("");

  const [customName, setCustomName] =
    useState("");

  const [customDescription, setCustomDescription] =
    useState("");

  const [workloadMode, setWorkloadMode] =
    useState("automatic");

  const [customInput, setCustomInput] =
    useState("");

  const [referenceLanguageId, setReferenceLanguageId] =
    useState("");

  const [referenceCode, setReferenceCode] =
    useState("");

  const [uploadedFileName, setUploadedFileName] =
    useState("");

  const [isEditorExpanded, setIsEditorExpanded] =
    useState(false);

  const fileInputRef = useRef(null);

  const [isAnalyzingReference, setIsAnalyzingReference] =
  useState(false);

  const [referenceAnalysisComplete, setReferenceAnalysisComplete] =
    useState(false);

  const [referenceAnalysisError, setReferenceAnalysisError] =
    useState("");

  const [detectedLanguage, setDetectedLanguage] =
    useState(null);

  const [syntaxValidation, setSyntaxValidation] =
    useState(null);

  const [inputContract, setInputContract] =
    useState(null);

  const [workloadResolution, setWorkloadResolution] =
    useState(null);

  const [benchmarkMetadata, setBenchmarkMetadata] = useState(null);

  const [referenceAnalysisSteps, setReferenceAnalysisSteps] =
    useState([]);
  
  

  useEffect(() => {
  const loadBenchmarkData = async () => {
    try {
      setLoadingData(true);
      setDataError("");

      const [
        benchmarkResponse,
        languageResponse,
      ] = await Promise.all([
        api.get("/benchmarks/"),
        api.get("/languages/"),
      ]);

      console.log(
        "BENCHMARK API:",
        benchmarkResponse.data
      );

      console.log(
        "LANGUAGE API:",
        languageResponse.data
      );

      const benchmarkData =
        Array.isArray(benchmarkResponse.data)
          ? benchmarkResponse.data
          : [];

      const languageData =
        Array.isArray(languageResponse.data)
          ? languageResponse.data
          : [];

      setBenchmarks(benchmarkData);
      setLanguages(languageData);

      if (benchmarkData.length > 0) {
        setBenchmark(
          String(
            benchmarkData[0].bench_id
          )
        );
      }

    } catch (error) {

      console.error(
        "Benchmark data loading failed:",
        error
      );

      console.error(
        "Response:",
        error.response?.data
      );

      setDataError(
        "Unable to load benchmarks or programming languages."
      );

    } finally {
      setLoadingData(false);
    }
  };

  loadBenchmarkData();
}, []);

  /* =========================================================
     METRICS
  ========================================================= */

  const [selectedMetrics, setSelectedMetrics] =
    useState([
      "Execution Time",
      "CPU Usage",
      "Memory Usage",
      "Energy Consumption",
    ]);

  /* =========================================================
     EXECUTION
  ========================================================= */

  const [isRunning, setIsRunning] =
    useState(false);


  const [showResults, setShowResults] =
    useState(false);
  const [analysisResults, setAnalysisResults] =
    useState([]);

  const [runError, setRunError] =
    useState("");

  const [processingSteps, setProcessingSteps] =
    useState([]);

  const [currentProcessingStep, setCurrentProcessingStep] =
    useState(null);

  const buildProcessingSteps = () => {

    if (benchmarkType === "predefined") {
  const predefinedSteps = [
    {
      id: "workload",
      label: "Generating deterministic benchmark workload",
      status: "pending",
    },
  ];

  selectedLanguages.forEach((languageId) => {
    const language = languages.find(
      (item) =>
        Number(item.lang_id) === Number(languageId)
    );

    if (!language) return;

    predefinedSteps.push(
      {
        id: `${languageId}-prepare`,
        label: `Preparing ${language.lang_name} implementation`,
        status: "pending",
      },
      {
        id: `${languageId}-compile`,
        label: `Compiling ${language.lang_name}`,
        status: "pending",
      },
      {
        id: `${languageId}-execute`,
        label: `Executing ${language.lang_name} and measuring metrics`,
        status: "pending",
      },
      {
        id: `${languageId}-verify`,
        label: `Verifying ${language.lang_name} benchmark output`,
        status: "pending",
      }
    );
  });

  predefinedSteps.push(
    {
      id: "green-score",
      label: "Calculating Green Scores",
      status: "pending",
    },
    {
      id: "save",
      label: "Saving analysis results",
      status: "pending",
    }
  );

  return predefinedSteps;
}

    const makeStepId = (languageName) =>
      languageName
        .toLowerCase()
        .replaceAll("+", "plus")
        .replaceAll("#", "sharp")
        .replaceAll(" ", "-");

    const targetSteps = [];

    selectedLanguages.forEach(
      (languageId) => {

        const language = languages.find(
          (item) =>
            Number(item.lang_id) ===
            Number(languageId)
        );

        if (!language) return;

        const stepName =
          makeStepId(language.lang_name);

        targetSteps.push(
          {
            id: `generate-${stepName}`,
            label:
              `Generating ${language.lang_name} implementation`,
            status: "pending",
          },
          {
            id: `execute-${stepName}`,
            label:
              `Executing and validating ${language.lang_name} implementation`,
            status: "pending",
          }
        );
      }
    );

    return [
      {
        id: "validate",
        label: "Benchmark request validated",
        status: "pending",
      },

      {
        id: "input",
        label: "Preparing input workload",
        status: "pending",
      },

      {
        id: "reference",
        label:
          `Executing reference ${referenceLanguage?.lang_name || ""
          } implementation`,
        status: "pending",
      },

      ...targetSteps,

      {
        id: "green-score",
        label: "Calculating Green Scores",
        status: "pending",
      },

      {
        id: "save",
        label: "Saving analysis results",
        status: "pending",
      },
    ];
  };

  /* =========================================================
     SELECTED LANGUAGE OBJECTS
  ========================================================= */

  const referenceLanguage = useMemo(() => {

    return languages.find(
      (language) =>
        String(language.lang_id) ===
        String(referenceLanguageId)
    );

  }, [referenceLanguageId, languages]);

  const referenceMonacoLanguage =
    referenceLanguage
      ? (
        MONACO_LANGUAGE_MAP[
        referenceLanguage.lang_name
        ] || "plaintext"
      )
      : "plaintext";


  /* =========================================================
     LANGUAGE TOGGLE
  ========================================================= */

  const toggleLanguage = (languageId) => {
    if (
      benchmarkType === "custom" &&
      Number(referenceLanguageId) ===
      Number(languageId)
    ) {
      return;
    }
    setSelectedLanguages((current) => {

      if (current.includes(languageId)) {

        if (current.length === 1) {
          return current;
        }

        return current.filter(
          (languageIdItem) => languageIdItem !== languageId
        );

      }

      return [
        ...current,
        languageId
      ];

    });


    setShowResults(false);

  };




  /* =========================================================
     METRIC TOGGLE
  ========================================================= */

  const toggleMetric = (metric) => {

    setSelectedMetrics((current) => {


      if (current.includes(metric)) {


        if (current.length === 1) {
          return current;
        }


        return current.filter(
          (item) => item !== metric
        );


      }


      return [
        ...current,
        metric
      ];


    });


    setShowResults(false);

  };



  /* =========================================================
     RESET
  ========================================================= */

  const handleReset = () => {


    setBenchmark(
      benchmarks.length > 0
        ? String(benchmarks[0].bench_id)
        : ""
    );

    setBenchmarkSize("medium");

    setSelectedLanguages([]);

    setBenchmarkCategory("");
    setCustomInputSize("");
    setCustomName("");
    setCustomDescription("");
    setWorkloadMode("automatic");
    setCustomInput("");
    
    setReferenceLanguageId("");
    setReferenceCode("");
    setUploadedFileName("");
    setIsEditorExpanded(false);

    setIsAnalyzingReference(false);
    setReferenceAnalysisComplete(false);
    setReferenceAnalysisError("");

    setDetectedLanguage(null);
    setSyntaxValidation(null);
    setInputContract(null);
    setWorkloadResolution(null);
    setBenchmarkMetadata(null);
    setReferenceAnalysisSteps([]);

    setSelectedMetrics([
      "Execution Time",
      "CPU Usage",
      "Memory Usage",
      "Energy Consumption",
    ]);

    setIsRunning(false);

    setShowResults(false);
    setAnalysisResults([]);
    setRunError("");
    setProcessingSteps([]);
    setCurrentProcessingStep(null);
  };

/* =========================================================
   REFERENCE CODE ANALYSIS - CUSTOM ONLY
========================================================= */

const handleReferenceFileUpload = async (event) => {
  const file = event.target.files?.[0];

  if (!file) return;

  try {
    const text = await file.text();

    setReferenceCode(text);
    setUploadedFileName(file.name);
    setReferenceAnalysisError("");
  } catch (error) {
    console.error("Reference file upload failed:", error);
    setReferenceAnalysisError(
      "Unable to read the selected reference file."
    );
  } finally {
    event.target.value = "";
  }
};

const toggleEditorExpanded = () => {
  setIsEditorExpanded((current) => !current);
};

useEffect(() => {
  if (!isEditorExpanded) return;

  const handleEscape = (event) => {
    if (event.key === "Escape") {
      setIsEditorExpanded(false);
    }
  };

  document.addEventListener("keydown", handleEscape);
  document.body.style.overflow = "hidden";

  return () => {
    document.removeEventListener("keydown", handleEscape);
    document.body.style.overflow = "";
  };
}, [isEditorExpanded]);

const handleAnalyzeReference = async () => {

  if (
    benchmarkType !== "custom" ||
    !referenceCode.trim()
  ) {
    return;
  }

  try {

    setIsAnalyzingReference(true);
    setReferenceAnalysisComplete(false);
    setReferenceAnalysisError("");

    setDetectedLanguage(null);
    setSyntaxValidation(null);
    setInputContract(null);
    setWorkloadResolution(null);
    setBenchmarkMetadata(null);
    setReferenceAnalysisSteps([
      {
        id: "language",
        label: "Detecting programming language",
        status: "processing",
      },
      {
        id: "syntax",
        label: "Validating syntax",
        status: "pending",
      },
      {
        id: "input-contract",
        label: "Detecting input contract",
        status: "pending",
      },
    ]);


    /* =========================================
       STEP 1: START REFERENCE ANALYSIS JOB
    ========================================= */

    const startResponse = await api.post(
      "/analysis/custom-comparison/reference-analysis/start",
      {
        reference_code: referenceCode,
      }
    );


    const jobId =
      startResponse.data.job_id;


    if (!jobId) {
      throw new Error(
        "Backend did not return a reference analysis job ID."
      );
    }


    /* =========================================
       STEP 2: POLL JOB STATUS
    ========================================= */

    while (true) {

      const statusResponse =
        await api.get(
          `/analysis/custom-comparison/reference-analysis/status/${jobId}`
        );


      const job =
        statusResponse.data;


      const backendSteps =
        job.steps || {};


      /* =========================================
         UPDATE PROCESSING STEPS
      ========================================= */

      setReferenceAnalysisSteps(
        (currentSteps) =>
          currentSteps.map(
            (step) => {

              const backendStep =
                backendSteps[
                  step.id
                ];


              if (!backendStep) {
                return step;
              }


              return {
                ...step,

                status:
                  backendStep.status,

                label:
                  backendStep.message ||
                  step.label,
              };

            }
          )
      );


      /* =========================================
         COMPLETED
      ========================================= */

      if (
        job.status === "completed"
      ) {

        const result =
          job.result;


        if (!result) {
          throw new Error(
            "Reference analysis completed without a result."
          );
        }


        setDetectedLanguage(
          result.detected_language ||
          null
        );


        setSyntaxValidation(
          result.syntax_validation ||
          null
        );


        if (result.input_contract) {

          setInputContract({
            ...result.input_contract,

            description:
              result.input_contract.description ??
              result.input_contract.reason ??
              "",
          });

        } else {

          setInputContract(null);

        }


        setWorkloadResolution(
          result.workload_resolution ||
          null
        );
        setBenchmarkMetadata(
          result.benchmark_metadata || null
        );
        const metadata = result.benchmark_metadata;

        if (metadata) {
          setBenchmarkCategory(metadata.category || "");
          setCustomName(metadata.name || "");
          setCustomDescription(metadata.description || "");
        }

        /* -----------------------------------------
           MATCH DETECTED LANGUAGE TO DATABASE ID
        ----------------------------------------- */

        const detectedName =
          result.detected_language?.name;


        if (detectedName) {

          const matchedLanguage =
            languages.find(
              (language) =>
                language.lang_name ===
                detectedName
            );


          if (matchedLanguage) {

            setReferenceLanguageId(
              String(
                matchedLanguage.lang_id
              )
            );

          } else {

            setReferenceLanguageId("");

          }

        }


        setReferenceAnalysisComplete(
          true
        );


        break;
      }


      /* =========================================
         FAILED
      ========================================= */

      if (
        job.status === "failed"
      ) {

        throw new Error(
          job.error ||
          "Reference code analysis failed."
        );

      }


      /* =========================================
         WAIT BEFORE NEXT STATUS REQUEST
      ========================================= */

      await new Promise(
        (resolve) =>
          setTimeout(
            resolve,
            800
          )
      );

    }


  } catch (error) {

    console.error(
      "Reference analysis error:",
      error
    );


    setReferenceAnalysisError(
      error.response?.data?.detail ||
      error.message ||
      "Reference code analysis failed."
    );


    setReferenceAnalysisComplete(
      false
    );


  } finally {

    setIsAnalyzingReference(false);

  }

};

useEffect(() => {

  if (
    benchmarkType !== "custom" ||
    !referenceCode.trim()
  ) {
    return;
  }

  const timer = setTimeout(() => {

    handleAnalyzeReference();

  }, 800);

  return () => {
    clearTimeout(timer);
  };

}, [
  benchmarkType,
  referenceCode,
]);

  /* =========================================================
     RUN ANALYSIS
  ========================================================= */

  const handleRun = async () => {

    if (benchmarkType === "predefined") {

      if (
        selectedLanguages.length === 0 ||
        !benchmark
      ) {
        return;
      }
    }

    if (benchmarkType === "custom") {

      const automaticInputInvalid =
      workloadMode === "automatic" &&
      (
        !customInputSize ||
        Number(customInputSize) <= 0
      );

      const customInputInvalid =
        workloadMode === "custom" &&
        !customInput.trim();

      if (
        !referenceCode.trim() ||
        !referenceAnalysisComplete ||
        !referenceLanguageId ||
        !syntaxValidation?.valid ||
        !inputContract ||
        !workloadResolution ||
        !benchmarkCategory ||
        !customName.trim() ||
        !customDescription.trim() ||
        selectedLanguages.length === 0 ||
        automaticInputInvalid ||
        customInputInvalid
      ){
        setRunError(
          !referenceAnalysisComplete
            ? "Please wait for the reference code analysis to complete."
            : workloadMode === "custom"
              ? "Please complete the benchmark fields and provide custom input."
              : "Please complete the benchmark fields and provide a valid input size."
        );


        return;
      }
    }
    const storedUser = JSON.parse(
      localStorage.getItem("user")
    );

    if (!storedUser?.user_id) {
      setRunError(
        "User information not found. Please login again."
      );
      return;
    }

    setIsRunning(true);
    setShowResults(false);
    setRunError("");
    setAnalysisResults([]);

    try {

      /* =========================================
         PREDEFINED
      ========================================= */

      if (benchmarkType === "predefined") {

  const initialSteps =
    buildProcessingSteps();

  setProcessingSteps(
    initialSteps
  );

  setCurrentProcessingStep(null);

  /* STEP 1: START PREDEFINED JOB */

  const startResponse = await api.post(
    "/analysis/comparison/start",
    {
      user_id: storedUser.user_id,
      bench_id: Number(benchmark),
      lang_ids: selectedLanguages,
      bench_size: benchmarkSize,
    }
  );

  const jobId =
    startResponse.data.job_id;

  if (!jobId) {
    throw new Error(
      "Backend did not return a job ID."
    );
  }

  /* STEP 2: POLL REAL BACKEND STATUS */

  while (true) {

    const statusResponse =
      await api.get(
        `/analysis/comparison/status/${jobId}`
      );

    const job =
      statusResponse.data;

    const backendSteps =
      job.steps || {};

    setProcessingSteps(
      (currentSteps) =>
        currentSteps.map(
          (step) => {

            const backendStep =
              backendSteps[step.id];

            if (!backendStep) {
              return step;
            }

            return {
              ...step,

              status:
                backendStep.status,

              label:
                backendStep.message ||
                step.label,
            };
          }
        )
    );

    setCurrentProcessingStep(
      job.current_step || null
    );

    if (
      job.status === "completed"
    ) {

      setAnalysisResults(
        job.results || []
      );

      setShowResults(true);
      setIsRunning(false);

      break;
    }

    if (
      job.status === "failed"
    ) {
      throw new Error(
        job.error ||
        "Predefined benchmark analysis failed."
      );
    }

    await new Promise(
      (resolve) =>
        setTimeout(
          resolve,
          800
        )
    );
  }

  return;
}


      /* =========================================
         CUSTOM
      ========================================= */

      const initialSteps =
        buildProcessingSteps();

      setProcessingSteps(
        initialSteps
      );

      setCurrentProcessingStep(null);


      /* STEP 1: START JOB */

      const startResponse = await api.post(
        "/analysis/custom-comparison/start",
        {
          user_id: storedUser.user_id,

          custom_category:
            benchmarkCategory,

          custom_benchmark_name:
            customName.trim(),

          custom_description:
            customDescription.trim(),

          input_size:
            workloadMode === "automatic"
              ? Number(customInputSize)
              : null,

          workload_type:
            null,

          custom_input:
            workloadMode === "custom"
              ? customInput
              : null,

          reference_lang_id:
            Number(referenceLanguageId),

          reference_code:
            referenceCode,

          target_lang_ids:
            selectedLanguages,
        }
      );


      const jobId =
        startResponse.data.job_id;

      if (!jobId) {
        throw new Error(
          "Backend did not return a job ID."
        );
      }


      /* STEP 2: POLL STATUS */

      while (true) {

        const statusResponse =
          await api.get(
            `/analysis/custom-comparison/status/${jobId}`
          );

        const job =
          statusResponse.data;

        const backendSteps =
          job.steps || {};


        /* Update processing UI */

        setProcessingSteps(
          (currentSteps) =>
            currentSteps.map(
              (step) => {

                const backendStep =
                  backendSteps[
                  step.id
                  ];

                if (!backendStep) {
                  return step;
                }

                return {
                  ...step,

                  status:
                    backendStep.status,

                  label:
                    backendStep.message ||
                    step.label,
                };
              }
            )
        );


        setCurrentProcessingStep(
          job.current_step || null
        );


        /* COMPLETED */

        if (
            job.status ===
            "completed"
          ) {

            setAnalysisResults(
              job.results || []
            );

            if (job.benchmark_metadata) {
              setBenchmarkMetadata(
                job.benchmark_metadata
              );
            }

            setShowResults(true);
            setIsRunning(false);

            break;
          }


        /* FAILED */

        if (
          job.status ===
          "failed"
        ) {

          throw new Error(
            job.error ||
            "Custom benchmark analysis failed."
          );
        }


        /* Wait before next status request */

        await new Promise(
          (resolve) =>
            setTimeout(
              resolve,
              800
            )
        );
      }

    } catch (error) {

      console.error(
        "Analysis error:",
        error
      );

      setRunError(
        error.response?.data?.detail ||
        error.message ||
        "Analysis failed."
      );

      setIsRunning(false);
    }
  };


      const isRunDisabled =
      isRunning ||
      isAnalyzingReference ||
      (
        benchmarkType === "predefined"
          ? (
              !benchmark ||
              selectedLanguages.length === 0
            )
          : (
              !referenceCode.trim() ||
              !referenceAnalysisComplete ||
              !referenceLanguageId ||
              !syntaxValidation?.valid ||
              !inputContract ||
              !workloadResolution ||
              !benchmarkCategory ||
              !customName.trim() ||
              !customDescription.trim() ||
              selectedLanguages.length === 0 ||
              (
                workloadMode === "automatic" &&
                (
                  !customInputSize ||
                  Number(customInputSize) <= 0
                )
              ) ||
              (
                workloadMode === "custom" &&
                !customInput.trim()
              )
            )
      );

  /* =======================================================
     PAGE
  ======================================================= */
  return (

    <main
      className="
          min-h-screen
          bg-[#F8FAFC]
          text-[#111827]
          px-6
          py-10
          md:px-10
          md:py-14
          "
    >

      <div
        className="
              fixed
              top-[-200px]
              left-1/2
              -translate-x-1/2
              w-[600px]
              h-[400px]
              bg-[#22C55E]/10
              blur-[140px]
              rounded-full
              pointer-events-none
              "
      />


      <div className="relative max-w-7xl mx-auto">


        {/* ===================================================
            HEADER
        =================================================== */}

        <div className="mb-10">


          <div
            className="
                  inline-flex
                  items-center
                  gap-3
                  px-4
                  py-2
                  rounded-full
                  border
                  border-[#E5E7EB]
                  bg-white
                  text-xs
                  uppercase
                  tracking-[0.2em]
                  text-[#6B7280]
                  "
          >

            <span
              className="
                w-2
                h-2
                rounded-full
                bg-[#22C55E]
                "
            />

            Benchmark Workspace

          </div>



          <h1
            className="
mt-6
text-4xl
md:text-5xl
font-semibold
tracking-tight
"
          >

            Run your

            <span
              className="
text-[#166534]
"
            >
              benchmark.
            </span>

          </h1>



          <p
            className="
mt-5
max-w-2xl
text-[#6B7280]
text-base
md:text-lg
"
          >

            Compare programming languages by measuring
            execution performance, system resources
            and energy consumption.

          </p>


        </div>




        {/* ===================================================
            BENCHMARK TYPE
        =================================================== */}

        <section
          className="
                rounded-2xl
                border
                border-[#E5E7EB]
                bg-white
                shadow-sm
                overflow-hidden
                "
        >


          <div
            className="
                  p-6
                  md:p-8
                  border-b
                  border-[#E5E7EB]
                  "
          >


            <div
              className="
                  flex
                  flex-col
                  md:flex-row
                  justify-between
                  gap-5
"
            >


              <div>

                <p className="text-xs uppercase tracking-[0.2em] text-[#6B7280]">
                  Step 01
                </p>

                <h2 className="mt-2 text-xl font-medium">
                  Choose benchmark type
                </h2>

              </div>



              <div
                className="
                      flex
                      p-1
                      rounded-xl
                      border
                      border-[#E5E7EB]
                      bg-[#F8FAFC]
                      "
              >


                <button
                  type="button"
                  onClick={() => {

                    setBenchmarkType("predefined");
                    setShowResults(false);

                  }}

                  className={`

                      px-5
                      py-3
                      rounded-lg
                      text-sm
                      transition
                      ${benchmarkType === "predefined"
                      ?
                      "bg-[#166534] text-white"
                      :
                      "text-[#6B7280] hover:text-[#111827]"
                    }
                `}
                >
                  Predefined
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setBenchmarkType("custom");
                    setShowResults(false);
                  }}
                  className={`
                        px-5
                        py-3
                        rounded-lg
                        text-sm
                        transition
                        ${benchmarkType === "custom"
                      ?
                      "bg-[#166534] text-white"
                      :
                      "text-[#6B7280] hover:text-[#111827]"
                    }
                  `}
                >
                  Custom
                </button>

              </div>
            </div>
          </div>
          {/* =================================================
              PREDEFINED
          ================================================= */}


          {
            benchmarkType === "predefined" && (


              <div className="p-6 md:p-8">


                <div className="grid lg:grid-cols-2 gap-6">


                  <Field label="Benchmark">

                    <select
                      value={benchmark}
                      onChange={(e) => {
                        setBenchmark(e.target.value);
                        setShowResults(false);
                      }}
                      className="
                        w-full
                        rounded-xl
                        border
                        border-[#E5E7EB]
                        bg-white
                        px-4
                        py-3
                        text-[#111827]
                        outline-none
                        transition
                        focus:border-[#166534]
                        focus:ring-2
                        focus:ring-[#166534]/20
                      "
                    >

                      {benchmarks.map((item) => (

                        <option
                          key={item.bench_id}
                          value={String(item.bench_id)}
                        >
                          {item.bench_name}
                        </option>

                      ))}
                    </select>
                  </Field>
                  <Field label="Benchmark Size">
                    <select
                      value={benchmarkSize}
                      onChange={(e) => {
                        setBenchmarkSize(e.target.value);
                        setShowResults(false);
                      }}
                      className="
                                    w-full
                                    rounded-xl
                                    border
                                    border-[#E5E7EB]
                                    bg-white
                                    px-4
                                    py-3
                                    text-[#111827]
                                    outline-none
                                    transition
                                    focus:border-[#166534]
                                    focus:ring-2
                                    focus:ring-[#166534]/20
                                  "
                    >
                      <option value="small">
                        Small
                      </option>

                      <option value="medium">
                        Medium
                      </option>

                      <option value="large">
                        Large
                      </option>
                    </select>
                  </Field>
                </div>
                <div className="mt-8">
                  <SectionLabel>
                    Programming Languages
                  </SectionLabel>
                  <p className="mt-2 text-sm text-[#6B7280]">
                    Select one or more languages to compare.
                  </p>
                  <div
                    className="
                          mt-5
                          grid
                          grid-cols-2
                          sm:grid-cols-3
                          lg:grid-cols-5
                          gap-3
                          "
                  >

                    {languages.map((language) => (

                      <LanguageButton
                        key={language.lang_id}
                        language={language.lang_name}
                        selected={
                          selectedLanguages.includes(language.lang_id)
                        }
                        onClick={() =>
                          toggleLanguage(language.lang_id)
                        }
                      />

                    ))}

                  </div>
                </div>
              </div>
            )
          }
          {/* =================================================
    CUSTOM
================================================= */}
          {
            benchmarkType === "custom" && (


              <div className="p-6 md:p-8">

                {/* CREATE YOUR OWN BENCHMARK */}

                <div className="mb-8">

                  <SectionLabel>
                    Create Your Own Benchmark
                  </SectionLabel>

                  <p className="mt-2 text-sm text-[#6B7280]">
                    Provide your reference implementation. GreenCode Analyzer will
                    detect the language, validate the code, determine its input
                    contract and generate benchmark metadata.
                  </p>

                </div>

                {/* =================================================
                    REFERENCE IMPLEMENTATION
                ================================================= */}

                <div className="mt-8">

                  <SectionLabel>
                    Reference Implementation
                  </SectionLabel>

                  <p className="mt-2 text-sm text-[#6B7280]">
                    Provide the original implementation that will
                    be used as the reference for equivalent language
                    implementations.
                  </p>

                  {isEditorExpanded && (
                    <div
                      className="fixed inset-0 z-40 bg-black/60 backdrop-blur-[2px]"
                      aria-hidden="true"
                    />
                  )}

                  <div
                    className={
                      isEditorExpanded
                        ? "fixed inset-4 z-50 flex flex-col overflow-hidden rounded-2xl border border-[#1F2937] bg-[#0B0F14] shadow-2xl"
                        : "mt-5 overflow-hidden rounded-2xl border border-[#1F2937] bg-[#0B0F14] shadow-sm"
                    }
                  >

                    {/* EDITOR HEADER */}

                    <div
                      className="
                        flex
                        min-h-14
                        items-center
                        justify-between
                        gap-4
                        border-b
                        border-[#1F2937]
                        bg-[#111820]
                        px-5
                        py-2
                      "
                    >

                      <div className="flex min-w-0 items-center gap-3">

                        <div className="flex shrink-0 gap-2">
                          <span className="h-3 w-3 rounded-full bg-red-400/80" />
                          <span className="h-3 w-3 rounded-full bg-yellow-400/80" />
                          <span className="h-3 w-3 rounded-full bg-green-400/80" />
                        </div>

                        <span className="truncate text-xs font-mono text-[#CBD5E1]">
                          {uploadedFileName ||
                            (referenceLanguage
                              ? `main.${LANGUAGES.find(
                                  (item) =>
                                    item.name === referenceLanguage.lang_name
                                )?.extension || "txt"}`
                              : "reference-code")}
                        </span>

                      </div>

                      <div className="flex shrink-0 items-center gap-2">

                        <span className="hidden text-xs font-medium text-[#86EFAC] sm:inline">
                          {referenceLanguage?.lang_name ||
                            "Language will be detected"}
                        </span>

                        <input
                          ref={fileInputRef}
                          type="file"
                          className="hidden"
                          accept=".c,.h,.cpp,.cc,.cxx,.java,.py,.js,.mjs,.go,.rs,.cs,.kt,.kts,.php,.txt"
                          onChange={handleReferenceFileUpload}
                        />

                        <button
                          type="button"
                          onClick={() => fileInputRef.current?.click()}
                          className="inline-flex items-center gap-2 rounded-lg border border-[#334155] bg-[#18202A] px-3 py-2 text-xs font-medium text-[#E2E8F0] transition hover:border-[#4B5563] hover:bg-[#202A36]"
                          title="Upload reference file"
                        >
                          <svg
                            viewBox="0 0 24 24"
                            className="h-4 w-4"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.8"
                            aria-hidden="true"
                          >
                            <path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5" />
                            <path d="M5 15.5v3A1.5 1.5 0 0 0 6.5 20h11a1.5 1.5 0 0 0 1.5-1.5v-3" />
                          </svg>
                          Upload
                        </button>

                        <button
                          type="button"
                          onClick={toggleEditorExpanded}
                          className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-[#334155] bg-[#18202A] text-[#CBD5E1] transition hover:border-[#4B5563] hover:bg-[#202A36]"
                          title={
                            isEditorExpanded
                              ? "Exit expanded editor"
                              : "Expand editor"
                          }
                          aria-label={
                            isEditorExpanded
                              ? "Exit expanded editor"
                              : "Expand editor"
                          }
                        >
                          {isEditorExpanded ? (
                            <svg
                              viewBox="0 0 24 24"
                              className="h-4 w-4"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="1.8"
                              aria-hidden="true"
                            >
                              <path d="M8 8H5v3M16 8h3v3M8 16H5v-3M16 16h3v-3" />
                            </svg>
                          ) : (
                            <svg
                              viewBox="0 0 24 24"
                              className="h-4 w-4"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="1.8"
                              aria-hidden="true"
                            >
                              <path d="M8 3H5a2 2 0 0 0-2 2v3M16 3h3a2 2 0 0 1 2 2v3M8 21H5a2 2 0 0 1-2-2v-3M16 21h3a2 2 0 0 1 2-2v-3" />
                            </svg>
                          )}
                        </button>

                      </div>

                    </div>

                    {/* MONACO */}

                    <div
                      className={
                        isEditorExpanded
                          ? "min-h-0 flex-1"
                          : ""
                      }
                    >
                      <Editor
                        height={isEditorExpanded ? "100%" : "360px"}
                        language={referenceMonacoLanguage}
                        value={referenceCode}
                        onChange={(value) => {
                          setReferenceCode(value || "");

                          setReferenceAnalysisComplete(false);
                          setReferenceAnalysisError("");

                          setDetectedLanguage(null);
                          setSyntaxValidation(null);
                          setInputContract(null);
                          setWorkloadResolution(null);
                          setBenchmarkMetadata(null);

                          setBenchmarkCategory("");
                          setCustomName("");
                          setCustomDescription("");

                          setReferenceLanguageId("");
                          setSelectedLanguages([]);

                          setShowResults(false);
                        }}
                        theme="vs-dark"
                        options={{
                          minimap: {
                            enabled: false,
                          },

                          fontSize: 14,

                          lineNumbers: "on",

                          automaticLayout: true,

                          scrollBeyondLastLine: false,

                          wordWrap: "on",

                          tabSize: 4,

                          insertSpaces: true,

                          folding: true,

                          bracketPairColorization: {
                            enabled: true,
                          },

                          padding: {
                            top: 16,
                          },
                        }}
                      />
                    </div>

                  </div>

                </div>

{isAnalyzingReference && (

  <div
    className="
      mt-6
      rounded-2xl
      border
      border-[#22C55E]/30
      bg-[#F8FAFC]
      p-6
    "
  >

    <p className="font-semibold text-[#166534]">
      Analyzing reference implementation...
    </p>

    <div className="mt-5 space-y-4">

      {referenceAnalysisSteps.map((step) => (

        <div
          key={step.id}
          className="flex items-center gap-3"
        >

          <span>
            {step.status === "completed"
              ? "✓"
              : step.status === "processing"
                ? "●"
                : "○"
            }
          </span>

          <span className="text-sm">
            {step.label}
          </span>

        </div>

      ))}

    </div>

  </div>

)}

{referenceAnalysisError && (

  <div
    className="
      mt-5
      rounded-xl
      border
      border-red-200
      bg-red-50
      p-4
      text-sm
      text-red-700
    "
  >
    {referenceAnalysisError}
  </div>

)}

{referenceAnalysisComplete && (

  <div className="mt-8">

    <SectionLabel>
      Generated Metadata
    </SectionLabel>

    <p className="mt-2 text-sm text-[#6B7280]">
      Review the metadata generated from the reference implementation.
      You can edit these values before running the benchmark.
    </p>


    {/* LANGUAGE + SYNTAX */}

    <div className="mt-5 grid md:grid-cols-2 gap-4">

      <div
        className="
          rounded-xl
          border
          border-[#E5E7EB]
          bg-[#F8FAFC]
          p-5
        "
      >

        <p className="
          text-xs
          uppercase
          tracking-[0.15em]
          text-[#6B7280]
        ">
          Detected Language
        </p>

        <p className="mt-2 font-semibold text-[#111827]">
          {detectedLanguage?.name || "Unknown"}
        </p>

      </div>


      <div
        className={`
          rounded-xl
          border
          p-5
          ${
            syntaxValidation?.valid
              ? "border-[#CFE3D2] bg-[#F3F8F4]"
              : "border-red-200 bg-red-50"
          }
        `}
      >

        <p className="
          text-xs
          uppercase
          tracking-[0.15em]
          text-[#6B7280]
        ">
          Syntax Validation
        </p>

        <p
          className={`
            mt-2
            font-semibold
            ${
              syntaxValidation?.valid
                ? "text-[#166534]"
                : "text-red-700"
            }
          `}
        >
          {syntaxValidation?.valid
            ? "✓ Valid syntax"
            : "Invalid syntax"
          }
        </p>

      </div>

    </div>


    {/* CATEGORY + NAME */}

    <div className="mt-6 grid lg:grid-cols-2 gap-6">

      <Field label="Benchmark Category">

        <select
          value={benchmarkCategory}
          onChange={(e) => {
            setBenchmarkCategory(e.target.value);
            setShowResults(false);
          }}
          className="
            w-full
            rounded-xl
            border
            border-[#E5E7EB]
            bg-white
            px-4
            py-3
            text-[#111827]
            outline-none
            transition
            focus:border-[#166534]
            focus:ring-2
            focus:ring-[#166534]/20
          "
        >

          <option value="">
            Select category
          </option>

          {Object.entries(CATEGORY_LABELS).map(
            ([value, label]) => (

              <option
                key={value}
                value={value}
              >
                {label}
              </option>

            )
          )}

        </select>

      </Field>


      <Field label="Benchmark Name">

        <input
          type="text"
          value={customName}
          onChange={(e) => {
            setCustomName(e.target.value);
            setShowResults(false);
          }}
          placeholder="e.g. Two Sum Array Search"
          className="
            w-full
            rounded-xl
            border
            border-[#E5E7EB]
            bg-white
            px-4
            py-3
            text-[#111827]
            outline-none
            transition
            focus:border-[#166534]
            focus:ring-2
            focus:ring-[#166534]/20
          "
        />

      </Field>

    </div>


    {/* DESCRIPTION */}

    <div className="mt-6">

      <Field label="Description">

        <textarea
          value={customDescription}
          onChange={(e) => {
            setCustomDescription(e.target.value);
            setShowResults(false);
          }}
          placeholder="Describe what this benchmark measures."
          rows={4}
          className="
            w-full
            rounded-xl
            border
            border-[#E5E7EB]
            bg-white
            px-4
            py-3
            text-[#111827]
            outline-none
            transition
            resize-y
            focus:border-[#166534]
            focus:ring-2
            focus:ring-[#166534]/20
          "
        />

      </Field>

    </div>

  </div>

)}

{referenceAnalysisComplete && inputContract && (

  <div className="mt-8">

    <SectionLabel>
      Input Contract
    </SectionLabel>

    <p className="mt-2 text-sm text-[#6B7280]">
      Exact input structure detected from the reference implementation.
    </p>

    <div
      className="
        mt-4
        rounded-xl
        border
        border-[#E5E7EB]
        bg-[#F8FAFC]
        p-5
      "
    >

      <pre
        className="
          whitespace-pre-wrap
          break-words
          font-mono
          text-sm
          leading-6
          text-[#111827]
        "
      >
        {inputContract.description}
      </pre>

    </div>

  </div>

)}


{/* =================================================
                    INPUT / WORKLOAD
                ================================================= */}

                <div className="mb-8">

                  <SectionLabel>
                    Input / Workload
                  </SectionLabel>

                  <p className="mt-2 text-sm text-[#6B7280]">
                    Generate a deterministic workload automatically,
                    or provide the exact input you want every language
                    implementation to receive.
                  </p>

                  <div className="mt-5 grid md:grid-cols-2 gap-4">

                    {/* AUTOMATIC */}

                    <button
                      type="button"
                      onClick={() => {
                        setWorkloadMode("automatic");
                        setCustomInput("");
                        setShowResults(false);
                      }}
                      className={`
                        rounded-2xl
                        border
                        p-5
                        text-left
                        transition
                        ${
                          workloadMode === "automatic"
                            ? "border-[#22C55E] bg-[#F3F8F4]"
                            : "border-[#E5E7EB] bg-white hover:border-[#22C55E]/50"
                        }
                      `}
                    >

                      <div className="flex items-start gap-3">

                        <span
                          className={`
                            mt-0.5
                            flex
                            h-5
                            w-5
                            items-center
                            justify-center
                            rounded-full
                            border
                            ${
                              workloadMode === "automatic"
                                ? "border-[#166534] bg-[#166534]"
                                : "border-[#D1D5DB] bg-white"
                            }
                          `}
                        >
                          {workloadMode === "automatic" && (
                            <span className="h-2 w-2 rounded-full bg-white" />
                          )}
                        </span>

                        <div>

                          <p className="font-semibold text-[#111827]">
                            Generate automatically
                          </p>

                          <p className="mt-1 text-sm leading-5 text-[#6B7280]">
                            The system generates deterministic input according to the detected input contract and requested input size.
                          </p>

                        </div>

                      </div>

                    </button>


                    {/* CUSTOM INPUT */}

                    <button
                      type="button"
                      onClick={() => {
                        setWorkloadMode("custom");
                        setShowResults(false);
                      }}
                      className={`
                        rounded-2xl
                        border
                        p-5
                        text-left
                        transition
                        ${
                          workloadMode === "custom"
                            ? "border-[#22C55E] bg-[#F3F8F4]"
                            : "border-[#E5E7EB] bg-white hover:border-[#22C55E]/50"
                        }
                      `}
                    >

                      <div className="flex items-start gap-3">

                        <span
                          className={`
                            mt-0.5
                            flex
                            h-5
                            w-5
                            items-center
                            justify-center
                            rounded-full
                            border
                            ${
                              workloadMode === "custom"
                                ? "border-[#166534] bg-[#166534]"
                                : "border-[#D1D5DB] bg-white"
                            }
                          `}
                        >
                          {workloadMode === "custom" && (
                            <span className="h-2 w-2 rounded-full bg-white" />
                          )}
                        </span>

                        <div>

                          <p className="font-semibold text-[#111827]">
                            Use custom input
                          </p>

                          <p className="mt-1 text-sm leading-5 text-[#6B7280]">
                            Provide the exact stdin workload manually.
                            Any valid input format can be supplied.
                          </p>

                        </div>

                      </div>

                    </button>

                  </div>

                </div>

                {/* =================================================
                    AUTOMATIC INPUT SIZE
                  ================================================= */}

                {workloadMode === "automatic" && (

                  <div className="mb-8">

                    <Field label="Input Size">

                      <input
                        type="number"
                        min="1"
                        value={customInputSize}
                        onChange={(e) => {
                          setCustomInputSize(e.target.value);
                          setShowResults(false);
                        }}
                        placeholder="e.g. 1000"
                        className="
                          w-full
                          rounded-xl
                          border
                          border-[#E5E7EB]
                          bg-white
                          px-4
                          py-3
                          text-[#111827]
                          outline-none
                          transition
                          focus:border-[#166534]
                          focus:ring-2
                          focus:ring-[#166534]/20
                        "
                      />

                      <p className="mt-2 text-xs text-[#6B7280]">
                        The system uses this as the workload scale.
                        The actual input structure has already been determined
                        from the reference code.
                      </p>

                    </Field>

                  </div>

                )}

                {/* =================================================
                    USER PROVIDED INPUT
                ================================================= */}

                {workloadMode === "custom" && (

                  <div className="mb-8">

                    <Field label="Custom Input">

                      <textarea
                        value={customInput}
                        onChange={(e) => {
                          setCustomInput(e.target.value);
                          setShowResults(false);
                        }}
                        placeholder={`Enter the exact input your reference program expects.

                Examples:
                5
                2 7 11 15 3
                9

                or JSON / CSV / text / characters / any custom format.`}
                        rows={12}
                        className="
                          w-full
                          rounded-2xl
                          border
                          border-[#E5E7EB]
                          bg-white
                          px-4
                          py-4
                          font-mono
                          text-sm
                          text-[#111827]
                          outline-none
                          transition
                          resize-y
                          focus:border-[#166534]
                          focus:ring-2
                          focus:ring-[#166534]/20
                        "
                      />

                      <p className="mt-2 text-xs text-[#6B7280]">
                        This exact input will be supplied to the reference
                        implementation and every generated target implementation.
                      </p>

                    </Field>

                  </div>
                )}

                {/* =================================================
                  LANGUAGES TO COMPARE
              ================================================= */}

                <div className="mt-8">

                  <SectionLabel>
                    Languages to Compare
                  </SectionLabel>

                  <p className="mt-2 text-sm text-[#6B7280]">
                    Select the target languages for which equivalent
                    implementations will be generated and benchmarked.
                  </p>

                  <div
                    className="
                        mt-5
                        grid
                        grid-cols-2
                        sm:grid-cols-3
                        lg:grid-cols-5
                        gap-3
                      "
                  >

                    {languages.map(
                      (language) => {

                        const isReference =
                          Number(language.lang_id) ===
                          Number(referenceLanguageId);

                        return (

                          <LanguageButton
                            key={language.lang_id}
                            language={language.lang_name}
                            selected={
                              selectedLanguages.includes(
                                language.lang_id
                              )
                            }
                            disabled={isReference}
                            reference={isReference}
                            onClick={() =>
                              toggleLanguage(
                                language.lang_id
                              )
                            }
                          />

                        );

                      }
                    )}

                  </div>

                </div>
              </div>
            )
          }
        </section>

        {/* =========================================================
          ANALYSIS SETTINGS
      ========================================================= */}

        <section
          className="
          rounded-2xl
          border
          border-[#E5E7EB]
          bg-white
          p-7
          shadow-sm
        "
        >

          <p className="text-xs font-medium tracking-[0.2em] text-[#6B7280]">
            STEP 02
          </p>

          <h2 className="mt-2 text-xl font-semibold text-[#111827]">
            Analysis Settings
          </h2>



          {/* METRICS */}

          <div className="mt-8">


            <SectionLabel>
              Metrics to Measure
            </SectionLabel>


            <div
              className="
                  mt-4
                  grid
                  grid-cols-1
                  sm:grid-cols-2
                  lg:grid-cols-4
                  gap-3
                  "
            >


              {
                METRICS.map((metric) => (


                  <MetricToggle

                    key={metric}

                    title={metric}

                    selected={
                      selectedMetrics.includes(metric)
                    }

                    onClick={() =>
                      toggleMetric(metric)
                    }
                  />
                ))
              }
            </div>
          </div>
        </section>

        {/* ===================================================
    SUMMARY
=================================================== */}
        <section
          className="
mt-6
rounded-2xl
border
border-[#E5E7EB]
bg-white
shadow-sm
p-6
"
        >
          <p className="
text-xs
uppercase
tracking-[0.2em]
text-[#6B7280]
">
            Analysis Summary
          </p>
          <div className="mt-4 flex flex-wrap gap-2">


            <SummaryTag>

              {
                benchmarkType === "custom"
                  ? customName || "Custom Benchmark"
                  : (
                    benchmarks.find(
                      (item) =>
                        String(item.bench_id) === benchmark
                    )?.bench_name || "Benchmark"
                  )
              }

            </SummaryTag>

            {benchmarkType === "custom" &&
              benchmarkCategory && (

                <SummaryTag>
                  {CATEGORY_LABELS[benchmarkCategory]}
                </SummaryTag>

              )}

            <SummaryTag>

              {benchmarkType === "custom"
                ? `${selectedLanguages.length} target languages`
                : `${selectedLanguages.length} languages`
              }

            </SummaryTag>

            <SummaryTag>

              {selectedMetrics.length} metrics

            </SummaryTag>

            {benchmarkType === "custom" && (

              <SummaryTag>
                {workloadMode === "automatic"
                  ? `Automatic workload · size ${customInputSize}`
                  : "Custom input provided"
                }
              </SummaryTag>

            )}

            {benchmarkType === "custom" &&
              referenceLanguage && (

                <SummaryTag>
                  Reference: {referenceLanguage.lang_name}
                </SummaryTag>

              )}

            {benchmarkType === "custom" &&
              referenceLanguage && (

                <SummaryTag>
                  {selectedLanguages.length + 1} implementations
                </SummaryTag>

              )}

            {
              benchmarkType === "predefined" && (

                <SummaryTag>
                  {benchmarkSize} size
                </SummaryTag>

              )}

          </div>


        </section>

        {/* ===================================================
    ACTIONS
=================================================== */}


        <div
          className="
mt-6
flex
flex-col-reverse
sm:flex-row
justify-end
gap-3
"
        >


          <button

            type="button"

            onClick={handleReset}

            className="
px-7
py-3.5
rounded-xl
border
border-[#E5E7EB]
text-[#6B7280]
hover:text-[#111827]
transition
"
          >
            Reset
          </button>
            <button
  type="button"
  onClick={handleRun}
  disabled={isRunDisabled}
  className="
    px-8
    py-3.5
    rounded-xl
    bg-[#166534]
    text-white
    font-semibold
    transition
    hover:bg-[#22C55E]
    disabled:opacity-40
    disabled:cursor-not-allowed
    disabled:hover:bg-[#166534]
  "
>
  {isRunning
    ? "Running Analysis..."
    : "Run Analysis →"}
</button>
        </div>

        {/* ===================================================
    RUNNING
=================================================== */}

        {isRunning && (

          <div
            className="
      mt-8
      rounded-2xl
      border
      border-[#22C55E]/30
      bg-white
      p-6
      shadow-sm
    "
          >

            <div className="flex items-center gap-3">

              <div
                className="
          h-5
          w-5
          animate-spin
          rounded-full
          border-2
          border-[#DDE8DF]
          border-t-[#166534]
        "
              />

              <div>

                <p className="font-semibold text-[#166534]">
                  {benchmarkType === "custom"
                    ? "Preparing custom benchmark..."
                    : "Running benchmark..."
                  }
                </p>

                <p className="mt-1 text-sm text-[#6B7280]">
                  Please wait while GreenCode Analyzer processes
                  your benchmark.
                </p>

              </div>

            </div>


            <div
              className="
        mt-6
        border-t
        border-[#E5E7EB]
        pt-5
        space-y-4
      "
            >

              {processingSteps.map((step) => (

                <div
                  key={step.id}
                  className="flex items-center gap-3"
                >

                  {/* STATUS ICON */}

                  {step.status === "completed" ? (

                    <div
                      className="
                flex
                h-6
                w-6
                items-center
                justify-center
                rounded-full
                bg-[#166534]
                text-xs
                font-bold
                text-white
              "
                    >
                      ✓
                    </div>

                  ) : step.status === "processing" ? (

                    <div
                      className="
                h-5
                w-5
                animate-spin
                rounded-full
                border-2
                border-[#DDE8DF]
                border-t-[#166534]
              "
                    />

                  ) : (

                    <div
                      className="
                flex
                h-6
                w-6
                items-center
                justify-center
                rounded-full
                border
                border-[#D1D5DB]
                text-xs
                text-[#9CA3AF]
              "
                    >
                      ○
                    </div>

                  )}


                  {/* LABEL */}

                  <span
                    className={`text-sm ${step.status === "completed"
                        ? "font-medium text-[#166534]"
                        : step.status === "processing"
                          ? "font-medium text-[#111827]"
                          : "text-[#9CA3AF]"
                      }`}
                  >
                    {step.label}
                  </span>

                </div>

              ))}

            </div>

          </div>

        )}

        {runError && (

          <div
            className="
      mt-6
      rounded-xl
      border
      border-red-200
      bg-red-50
      p-4
      text-sm
      text-red-700
    "
          >
            {runError}
          </div>

        )}

        {/* ===================================================
    RESULTS
=================================================== */}
        {
          showResults && (
            <ResultsSection
              results={analysisResults}
              languages={languages}
              benchmark={
                benchmarkType === "custom"
                  ? customName || "Custom Benchmark"
                  : (
                    benchmarks.find(
                      (item) =>
                        String(item.bench_id) === benchmark
                    )?.bench_name || "Benchmark"
                  )
              }
              selectedMetrics={selectedMetrics}
              benchmarkType={benchmarkType}
              referenceLanguageId={referenceLanguageId}
              benchmarkMetadata={benchmarkMetadata}
            />
          )
        }
      </div>
    </main>
  );
}
/* =========================================================
   RESULTS SECTION
========================================================= */
function ResultsSection({
  results,
  languages,
  benchmark,
  selectedMetrics,
  benchmarkType,
  referenceLanguageId,
  benchmarkMetadata,
}) {
  /* =========================================================
     CREATE RESULTS
  ========================================================= */
  const formattedResults = results.map(
    (result) => {

      const language = languages.find(
        (item) =>
          item.lang_id === result.lang_id
      );

      return {
        language:
          language?.lang_name ||
          `Language ${result.lang_id}`,

        isReference:
          benchmarkType === "custom" &&
          Number(result.lang_id) ===
          Number(referenceLanguageId),
        time:
          result.execution_time != null
            ? Number(result.execution_time)
            : null,

        cpu:
          result.cpu_usage != null
            ? Number(result.cpu_usage)
            : null,

        memory:
          result.memory_usage != null
            ? Number(result.memory_usage)
            : null,

        energy:
          result.energy_consumption != null
            ? Number(result.energy_consumption)
            : null,

        greenScore:
          result.green_score != null
            ? Number(result.green_score)
            : null,

        greenLabel:
          result.green_score_label || null,

        outputVerified:
          result.output_verified,
      };

    }
  );

  // =========================================================
  //  CHART DATA
  // ========================================================= */

  const chartData = formattedResults.map(
    (result) => ({
      language: result.isReference
        ? `${result.language} (Reference)`
        : result.language,

      executionTime: result.time,
      cpuUsage: result.cpu,
      memoryUsage: result.memory,
      energyConsumption: result.energy,
      greenScore: result.greenScore,
    })
  );
  /* =========================================================
     SORT RESULTS
     Lowest execution time = best performance
  ========================================================= */

  const sortedResults =
    [...formattedResults].sort(
      (a, b) => {

        if (a.greenScore == null) return 1;
        if (b.greenScore == null) return -1;

        return (
          b.greenScore -
          a.greenScore
        );

      }
    );

  /* =========================================================
   BEST RESULT FOR EACH METRIC
========================================================= */

  const bestPerformance =
    [...formattedResults]
      .filter((result) => result.time != null)
      .sort((a, b) => a.time - b.time)[0];


  const bestCPU =
    [...formattedResults]
      .filter((result) => result.cpu != null)
      .sort((a, b) => a.cpu - b.cpu)[0];


  const bestMemory =
    [...formattedResults]
      .filter((result) => result.memory != null)
      .sort((a, b) => a.memory - b.memory)[0];


  const bestEnergy =
    [...formattedResults]
      .filter((result) => result.energy != null)
      .sort((a, b) => a.energy - b.energy)[0];


  const bestGreen =
    [...formattedResults]
      .filter(
        (result) =>
          result.greenScore != null
      )
      .sort(
        (a, b) =>
          b.greenScore - a.greenScore
      )[0];


  return (

    <section
      className="
        w-full
        mt-10
        mb-12
        px-6
      "
    >

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="mb-6">

        <h2
          className="
            text-2xl
            font-bold
            text-[#111827]
          "
        >
          Benchmark Results
        </h2>

        <p
          className="
            mt-1
            text-sm
            text-[#6B7280]
          "
        >
          {benchmark || "Benchmark"} comparison across
          selected programming languages.
        </p>
        <div
          className="
    mt-4
    rounded-xl
    border
    border-[#DDE8DF]
    bg-[#F3F8F4]
    px-4
    py-3
  "
        >
          <p
            className="
      text-xs
      font-semibold
      uppercase
      tracking-[0.15em]
      text-[#166534]
    "
          >
            Green Score
          </p>

          <p
            className="
      mt-1
      text-sm
      text-[#6B7280]
    "
          >
            Overall sustainability score calculated from
            normalized execution time, CPU usage, memory
            usage and measured energy consumption.
          </p>
        </div>

      </div>


      {/* =====================================================
          RESULTS TABLE
      ===================================================== */}

      <div
        className="
          w-full
          overflow-x-auto
          rounded-2xl
          border
          border-[#E5E7EB]
          bg-white
          shadow-sm
        "
      >

        <table className="w-full min-w-[800px]">

          {/* ================= HEADER ================= */}

          <thead>

            <tr
              className="
                border-b
                border-[#E5E7EB]
                bg-[#F8FAFC]
              "
            >

              <th
                className="
                  px-5
                  py-4
                  text-left
                  text-xs
                  font-semibold
                  uppercase
                  tracking-wide
                  text-[#6B7280]
                "
              >
                Language
              </th>


              {selectedMetrics.includes("Execution Time") && (

                <th
                  className="
                    px-5
                    py-4
                    text-left
                    text-xs
                    font-semibold
                    uppercase
                    tracking-wide
                    text-[#6B7280]
                  "
                >
                  Execution Time
                </th>

              )}


              {selectedMetrics.includes("CPU Usage") && (

                <th
                  className="
                    px-5
                    py-4
                    text-left
                    text-xs
                    font-semibold
                    uppercase
                    tracking-wide
                    text-[#6B7280]
                  "
                >
                  CPU Usage
                </th>

              )}


              {selectedMetrics.includes("Memory Usage") && (

                <th
                  className="
                    px-5
                    py-4
                    text-left
                    text-xs
                    font-semibold
                    uppercase
                    tracking-wide
                    text-[#6B7280]
                  "
                >
                  Memory Usage
                </th>

              )}


              {selectedMetrics.includes("Energy Consumption") && (

                <th
                  className="
                    px-5
                    py-4
                    text-left
                    text-xs
                    font-semibold
                    uppercase
                    tracking-wide
                    text-[#6B7280]
                  "
                >
                  Energy
                </th>

              )}
              <th
                className="
                  px-5
                  py-4
                  text-left
                  text-xs
                  font-semibold
                  uppercase
                  tracking-wide
                  text-[#6B7280]
                "
              >
                Green Score
              </th>

            </tr>

          </thead>


          {/* ================= BODY ================= */}

          <tbody>

            {sortedResults.map((result) => (
              <tr
                key={result.language}
                className="
                  border-b
                  border-[#E5E7EB]
                  last:border-b-0
                  hover:bg-[#F8FAFC]
                  transition
                "
              >

                {/* LANGUAGE */}

                <td
                  className="
                    px-5
                    py-4
                    text-sm
                    font-semibold
                    text-[#111827]
                  "
                >

                  <div className="flex items-center gap-3">

                    <span>
                      {result.language}
                    </span>
                    {result.isReference && (
                      <span
                        className="
                          rounded-md
                          border
                          border-[#166534]/20
                          bg-[#166534]/10
                          px-2
                          py-1
                          text-xs
                          font-semibold
                          text-[#166534]
                        "
                      >
                        Reference
                      </span>
                    )}
                    {(
                      bestGreen &&
                      result.language === bestGreen.language
                    ) && (

                        <span
                          className="
                          rounded-md
                          bg-[#84CC16]/20
                          px-2
                          py-1
                          text-xs
                          font-semibold
                          text-[#166534]
                        "
                        >
                          🌿 Greenest
                        </span>

                      )}

                  </div>

                </td>


                {/* EXECUTION TIME */}

                {selectedMetrics.includes("Execution Time") && (

                  <td
                    className="
                      px-5
                      py-4
                      text-sm
                      text-[#526174]
                    "
                  >
                    {result.time != null
                      ? `${result.time.toFixed(3)} ms`
                      : "—"}
                  </td>

                )}


                {/* CPU */}

                {selectedMetrics.includes("CPU Usage") && (

                  <td
                    className="
                      px-5
                      py-4
                      text-sm
                      text-[#526174]
                    "
                  >
                    {result.cpu != null
                      ? `${result.cpu.toFixed(2)}%`
                      : "—"}
                  </td>

                )}


                {/* MEMORY */}

                {selectedMetrics.includes("Memory Usage") && (

                  <td
                    className="
                      px-5
                      py-4
                      text-sm
                      text-[#526174]
                    "
                  >
                    {result.memory != null
                      ? `${result.memory.toFixed(2)} MB`
                      : "—"}
                  </td>

                )}


                {/* ENERGY */}

                {selectedMetrics.includes("Energy Consumption") && (

                  <td
                    className="
                      px-5
                      py-4
                      text-sm
                      text-[#526174]
                    "
                  >
                    {result.energy != null
                      ? `${result.energy.toFixed(4)} J`
                      : "Not measured"}
                  </td>

                )}

                <td
                  className="
    px-5
    py-4
    min-w-[170px]
  "
                >
                  {result.greenScore != null ? (

                    <div>

                      <div className="flex items-center gap-2">

                        <span
                          className="
            text-sm
            font-bold
            text-[#166534]
          "
                        >
                          {result.greenScore.toFixed(1)}
                          /100
                        </span>

                        <span
                          className="
            text-xs
            text-[#6B7280]
          "
                        >
                          {result.greenLabel}
                        </span>

                      </div>

                      <div
                        className="
          mt-2
          h-2
          w-full
          rounded-full
          bg-[#E5E7EB]
          overflow-hidden
        "
                      >
                        <div
                          className="
            h-full
            rounded-full
            bg-[#22C55E]
          "
                          style={{
                            width:
                              `${result.greenScore}%`
                          }}
                        />
                      </div>

                    </div>

                  ) : (

                    <span className="text-sm text-[#6B7280]">
                      N/A
                    </span>

                  )}
                </td>
              </tr>
            ))}

          </tbody>

        </table>

      </div>

      {/* =====================================================
    CUSTOM BENCHMARK VISUALIZATIONS
===================================================== */}

      { (

        <div className="mt-10">

          <div className="mb-6">

            <p
              className="
          text-xs
          font-semibold
          uppercase
          tracking-[0.2em]
          text-[#166534]
        "
            >
              Performance Visualizations
            </p>

            <h3
              className="
          mt-2
          text-xl
          font-bold
          text-[#111827]
        "
            >
              Benchmark Comparison
            </h3>

            <p
              className="
          mt-2
          max-w-3xl
          text-sm
          leading-6
          text-[#6B7280]
        "
            >
              Visual comparison of the measured performance
              and sustainability metrics for the reference
              and generated implementations.
            </p>

          </div>


          {/* EXECUTION + CPU */}

          <div
            className="
        grid
        grid-cols-1
        gap-6
        xl:grid-cols-2
      "
          >

            {selectedMetrics.includes(
              "Execution Time"
            ) && (

                <MetricComparisonChart
                  title="Execution Time"
                  description="Lower execution time indicates better performance."
                  data={chartData}
                  dataKey="executionTime"
                  unit="ms"
                />

              )}


            {selectedMetrics.includes(
              "CPU Usage"
            ) && (

                <MetricComparisonChart
                  title="CPU Usage"
                  description="Lower CPU utilization indicates lower processor demand."
                  data={chartData}
                  dataKey="cpuUsage"
                  unit="%"
                />

              )}

          </div>


          {/* MEMORY + ENERGY */}

          <div
            className="
        mt-6
        grid
        grid-cols-1
        gap-6
        xl:grid-cols-2
      "
          >

            {selectedMetrics.includes(
              "Memory Usage"
            ) && (

                <MetricComparisonChart
                  title="Memory Usage"
                  description="Lower memory usage indicates a smaller runtime memory footprint."
                  data={chartData}
                  dataKey="memoryUsage"
                  unit="MB"
                />

              )}


            {selectedMetrics.includes(
              "Energy Consumption"
            ) && (

                <MetricComparisonChart
                  title="Energy Consumption"
                  description="Lower measured energy consumption indicates better energy efficiency."
                  data={chartData}
                  dataKey="energyConsumption"
                  unit="J"
                  decimals={4}
                />

              )}

          </div>


          {/* GREEN SCORE */}

          <div className="mt-6">

            <MetricComparisonChart
              title="Green Score"
              description="Higher Green Score indicates a better overall sustainability balance."
              data={chartData}
              dataKey="greenScore"
              unit="/100"
              higherIsBetter
            />

          </div>

        </div>

      )}

      {/* =====================================================
    HIGHLIGHTS
===================================================== */}

      <div className="mt-8">

        <h3
          className="
      mb-4
      text-lg
      font-bold
      text-[#111827]
    "
        >
          Highlights
        </h3>

        <div
          className="
      grid
      grid-cols-1
      gap-4
      sm:grid-cols-2
      lg:grid-cols-5
    "
        >

          {selectedMetrics.includes("Execution Time") && (

            <ResultHighlight
              label="Best Performance"
              value={bestPerformance?.language || "—"}
              description={
                bestPerformance
                  ? `Lowest execution time: ${bestPerformance.time.toFixed(3)} ms`
                  : "Execution time is unavailable."
              }
            />

          )}


          {selectedMetrics.includes("CPU Usage") && (

            <ResultHighlight
              label="Lowest CPU Usage"
              value={bestCPU?.language || "—"}
              description={
                bestCPU
                  ? `Lowest CPU usage: ${bestCPU.cpu.toFixed(2)}%`
                  : "CPU usage is unavailable."
              }
            />

          )}


          {selectedMetrics.includes("Memory Usage") && (

            <ResultHighlight
              label="Lowest Memory Usage"
              value={bestMemory?.language || "—"}
              description={
                bestMemory
                  ? `Lowest memory usage: ${bestMemory.memory.toFixed(2)} MB`
                  : "Memory usage is unavailable."
              }
            />

          )}


          {selectedMetrics.includes("Energy Consumption") && (

            <ResultHighlight
              label="Best Energy Efficiency"
              value={bestEnergy?.language || "—"}
              description={
                bestEnergy
                  ? `Lowest energy consumption: ${bestEnergy.energy.toFixed(4)} J`
                  : "Energy measurement is currently unavailable."
              }
            />

          )}

          <ResultHighlight
            label="🌿 Greenest Language"
            value={bestGreen?.language || "—"}
            description={
              bestGreen
                ? `Green Score: ${bestGreen.greenScore.toFixed(1)} / 100`
                : "Green Score is unavailable."
            }
          />


        </div>

      </div>
      {/* =====================================================
    SUSTAINABILITY SUMMARY
===================================================== */}

      {bestGreen && (

        <div
          className="
      mt-8
      rounded-2xl
      border
      border-[#CFE3D2]
      bg-[#F3F8F4]
      p-6
    "
        >
          <p
            className="
        text-xs
        uppercase
        tracking-[0.2em]
        font-semibold
        text-[#166534]
      "
          >
            🌿 Sustainability Summary
          </p>

          <p
            className="
        mt-3
        text-sm
        leading-6
        text-[#526174]
      "
          >
            <span className="font-semibold text-[#111827]">
              {bestGreen.language}
            </span>

            {" "}achieved the highest Green Score of{" "}

            <span className="font-semibold text-[#166534]">
              {bestGreen.greenScore.toFixed(1)}/100
            </span>

            {" "}for this benchmark, providing the best
            overall balance of execution performance,
            resource usage and measured energy consumption.
          </p>

        </div>

      )}


    </section>
    /* =========================================================
       CODE EDITOR
    ========================================================= */

  );
}

/* =========================================================
   METRIC COMPARISON CHART
========================================================= */

function MetricComparisonChart({
  title,
  description,
  data,
  dataKey,
  unit,
  higherIsBetter = false,
  decimals = 2,
}) {

  const validData = data.filter(
    (item) =>
      item[dataKey] != null
  );

  if (validData.length === 0) {
    return null;
  }

  return (

    <div
      className="
        rounded-2xl
        border
        border-[#E5E7EB]
        bg-white
        p-6
        shadow-sm
      "
    >

      {/* HEADER */}

      <div
        className="
          flex
          flex-col
          gap-2
          sm:flex-row
          sm:items-start
          sm:justify-between
        "
      >

        <div>

          <h4
            className="
              text-base
              font-bold
              text-[#111827]
            "
          >
            {title}
          </h4>

          <p
            className="
              mt-1
              text-xs
              leading-5
              text-[#6B7280]
            "
          >
            {description}
          </p>

        </div>


        <span
          className="
            whitespace-nowrap
            rounded-lg
            bg-[#F3F8F4]
            px-3
            py-1.5
            text-xs
            font-medium
            text-[#166534]
          "
        >
          {higherIsBetter
            ? "Higher is better"
            : "Lower is better"}
        </span>

      </div>


      {/* CHART */}

      <div
        className="
          mt-5
          h-[210px]
          w-full
        "
      >

        <ResponsiveContainer
          width="100%"
          height="100%"
        >

          <BarChart
            data={validData}
            margin={{
              top: 10,
              right: 20,
              left: 5,
              bottom: 25,
            }}
          >

            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="#E5E7EB"
            />


            <XAxis
              dataKey="language"
              tick={{
                fontSize: 12,
                fill: "#6B7280",
              }}
              axisLine={{
                stroke: "#E5E7EB",
              }}
              tickLine={false}
              interval={0}
              angle={
                validData.length > 5
                  ? -20
                  : 0
              }
              textAnchor={
                validData.length > 5
                  ? "end"
                  : "middle"
              }
            />


            <YAxis
              tick={{
                fontSize: 12,
                fill: "#6B7280",
              }}
              axisLine={false}
              tickLine={false}
              width={65}
            />


            <Tooltip
              cursor={{
                fill:
                  "rgba(22, 101, 52, 0.05)",
              }}
              formatter={(value) => {

                const numericValue =
                  Number(value);

                const formattedValue =
                  Number.isFinite(
                    numericValue
                  )
                    ? numericValue.toFixed(
                      decimals
                    )
                    : value;

                return [
                  `${formattedValue} ${unit}`,
                  title,
                ];
              }}
            />


            <Bar
              dataKey={dataKey}
              fill="#166534"
              radius={[
                8,
                8,
                0,
                0,
              ]}
              maxBarSize={70}
            />

          </BarChart>

        </ResponsiveContainer>

      </div>

    </div>

  );
}

/* =========================================================
   LANGUAGE LOGO
========================================================= */
function LanguageLogo({ language }) {
  const logo =
    LANGUAGE_LOGOS[language] || {
      label: language?.slice(0, 2) || "?",
      className: "bg-[#475569] text-white",
    };

  return (
    <span
      className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-[10px] font-bold tracking-tight shadow-sm ${logo.className}`}
      aria-hidden="true"
    >
      {logo.label}
    </span>
  );
}

/* =========================================================
   LANGUAGE BUTTON
========================================================= */

function LanguageButton({
  language,
  selected,
  onClick,
  disabled = false,
  reference = false,
}) {

  return (

    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`

        p-4
        rounded-xl
        border
        text-left
        transition

        ${reference
          ?
          "border-[#166534] bg-[#F3F8F4] cursor-not-allowed"
          :
          selected
            ?
            "border-[#22C55E] bg-[#22C55E]/10"
            :
            "border-[#E5E7EB] bg-white hover:border-[#22C55E]/50"
        }

      `}
    >

      <div className="flex items-center justify-between gap-3">

        <div className="flex min-w-0 items-center gap-3">

          <LanguageLogo language={language} />

          <div className="min-w-0">
            <span
              className={`text-sm ${reference || selected
                ? "text-[#166534]"
                : "text-[#6B7280]"
              }`}
            >
              {language}
            </span>

            {reference && (
              <p className="mt-1 text-[11px] font-medium text-[#166534]">
                Reference
              </p>
            )}
          </div>

        </div>

        <span
          className={`
            flex
            h-5
            w-5
            shrink-0
            items-center
            justify-center
            rounded-md
            border
            text-xs
            ${reference
              ? "border-[#166534] bg-[#166534] text-white"
              : selected
                ? "border-[#166534] bg-[#166534] text-white"
                : "border-[#E5E7EB] text-transparent"
            }
          `}
        >
          {reference ? "R" : "✓"}
        </span>

      </div>

    </button>

  );

}

/* =========================================================
   METRIC TOGGLE
========================================================= */

function MetricToggle({
  title,
  selected,
  onClick,
}) {

  return (

    <button
      type="button"
      onClick={onClick}
      className={`

        p-4
        rounded-xl
        border
        text-left
        transition

        ${selected
          ?
          "border-[#22C55E] bg-[#22C55E]/10"
          :
          "border-[#E5E7EB] bg-white"
        }

      `}
    >

      <div className="
        flex
        items-center
        gap-3
      ">

        <span
          className={`

            w-5
            h-5
            rounded-md
            border
            flex
            items-center
            justify-center

            ${selected
              ?
              "bg-[#166534] border-[#166534] text-white"
              :
              "border-[#E5E7EB]"
            }

          `}
        >
          ✓
        </span>

        <span className="
          text-sm
          text-[#111827]
        ">
          {title}
        </span>

      </div>

    </button>

  );

}

const CUSTOM_INPUT_CONFIG = {

  "algorithms-data-structures": {
    label: "Input Elements",
    placeholder: "e.g. 10000",
    description:
      "Enter the number of input elements for this benchmark.",
  },

  "web-development": {
    label: "Requests",
    placeholder: "e.g. 1000",
    description:
      "Enter the number of requests for this benchmark.",
  },

  "desktop-applications": {
    label: "Operations",
    placeholder: "e.g. 10000",
    description:
      "Enter the number of operations for this benchmark.",
  },

  "backend-api": {
    label: "Requests",
    placeholder: "e.g. 1000",
    description:
      "Enter the number of API requests for this benchmark.",
  },

  "ai-machine-learning": {
    label: "Samples",
    placeholder: "e.g. 10000",
    description:
      "Enter the number of samples for this benchmark.",
  },

  "data-science": {
    label: "Records",
    placeholder: "e.g. 50000",
    description:
      "Enter the number of records for this benchmark.",
  },

  "database-data-processing": {
    label: "Rows",
    placeholder: "e.g. 100000",
    description:
      "Enter the number of rows to process.",
  },

  "system-programming": {
    label: "Operations",
    placeholder: "e.g. 10000",
    description:
      "Enter the number of system operations.",
  },

  "networking": {
    label: "Packets",
    placeholder: "e.g. 10000",
    description:
      "Enter the number of packets to process.",
  },

  "cybersecurity": {
    label: "Requests",
    placeholder: "e.g. 5000",
    description:
      "Enter the number of requests or security operations.",
  },

  "game-development": {
    label: "Iterations",
    placeholder: "e.g. 10000",
    description:
      "Enter the number of simulation or processing iterations.",
  },

  "mobile-development": {
    label: "Operations",
    placeholder: "e.g. 10000",
    description:
      "Enter the number of application operations.",
  },

};

const CATEGORY_LABELS = {
  "algorithms-data-structures":
    "Algorithms & Data Structures",

  "web-development":
    "Web Development",

  "desktop-applications":
    "Desktop Applications",

  "backend-api":
    "Backend / API",

  "ai-machine-learning":
    "AI & Machine Learning",

  "data-science":
    "Data Science",

  "database-data-processing":
    "Database & Data Processing",

  "system-programming":
    "Systems Programming",

  "networking":
    "Networking",

  "cybersecurity":
    "Cybersecurity",

  "game-development":
    "Game Development",

  "mobile-development":
    "Mobile Development",
};

/* =========================================================
   RESULT HIGHLIGHT
========================================================= */

function ResultHighlight({
  label,
  value,
  description,
}) {


  return (

    <div
      className="
rounded-2xl
border
border-[#E5E7EB]
bg-white
p-6
"
    >


      <p className="
text-xs
uppercase
tracking-[0.2em]
text-[#6B7280]
">

        {label}

      </p>



      <p className="
mt-4
text-2xl
font-semibold
text-[#166534]
">

        {value}

      </p>



      <p className="
mt-2
text-xs
text-[#6B7280]
">

        {description}

      </p>


    </div>

  );

}






/* =========================================================
   FIELD
========================================================= */

function Field({
  label,
  children,
}) {


  return (

    <div>


      <label
        className="
block
mb-3
text-xs
uppercase
tracking-[0.2em]
text-[#6B7280]
"
      >

        {label}

      </label>


      {children}


    </div>

  );

}





/* =========================================================
   SECTION LABEL
========================================================= */

function SectionLabel({ children }) {


  return (

    <p
      className="
text-xs
uppercase
tracking-[0.2em]
text-[#6B7280]
"
    >

      {children}

    </p>

  );

}





/* =========================================================
   SUMMARY TAG
========================================================= */

function SummaryTag({ children }) {


  return (

    <span
      className="
inline-flex
items-center
px-3
py-2
rounded-lg
border
border-[#E5E7EB]
bg-[#F8FAFC]
text-xs
text-[#6B7280]
"
    >

      {children}

    </span>

  );
}
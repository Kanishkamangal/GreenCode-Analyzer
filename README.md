# 🌱 GreenCode Analyzer

> **Benchmark code. Compare performance. Build greener software.**

GreenCode Analyzer is a web-based platform that helps developers **compare programs across different programming languages** based on performance and resource usage.

Instead of looking only at execution time, GreenCode analyzes:

* ⏱️ Execution Time
* 🖥️ CPU Usage
* 🧠 Memory Usage
* ⚡ Energy Consumption

It then combines these measurements into a **Green Score** to make comparisons easier.

---

## 🎥 Demo

<!-- Add your demo GIF/video here -->

![GreenCode Demo](docs/demo/greencode-demo.gif)

---

## ✨ What Can GreenCode Do?
_
### 🔍 Analyze Code

Submit code and let GreenCode identify its programming language, input requirements, algorithm characteristics, and benchmark information.

### 🧪 Run Benchmarks

Run predefined or custom benchmarks under controlled workloads.

### 🌍 Compare Languages

Compare equivalent implementations written in languages such as:

**C · C++ · Java · Python · JavaScript · Go · Rust · C# · Kotlin · PHP**

### 📊 Measure Resources

See how different implementations perform in terms of:

**Time · CPU · Memory · Energy**

### 🌱 Green Score

Get a comparative score based on the resource usage of the implementations.

### 📄 Generate Reports

Export benchmark results as:

**PDF · Excel · CSV**

---

## 🧠 How It Works

```text
        Source Code
             ↓
       Code Analysis
             ↓
      Workload Selection
             ↓
        Benchmark
             ↓
   ┌─────────┼─────────┐
   ↓         ↓         ↓
 Time       CPU     Memory/Energy
   └─────────┼─────────┘
             ↓
       Green Score
             ↓
     Comparison & Report
```

---

## 🖥️ Screenshots

### Dashboard

<!-- Add screenshot -->

![GreenCode Dashboard](docs/images/dashboard.png)

### Benchmark Results

<!-- Add screenshot -->

![Benchmark Results](docs/images/results.png)

---

## 🛠️ Tech Stack

**Frontend**

* React
* Vite
* JavaScript

**Backend**

* Python
* FastAPI

**Database**

* PostgreSQL

**Analysis & Benchmarking**

* Pandas
* NumPy
* psutil
* Matplotlib
* Intel RAPL / Windows energy measurement

**Reports**

* ReportLab
* Excel
* CSV

---

## 📁 Project Structure

```text
GreenCode/
├── backend/
│   ├── app/
│   ├── benchmarks/
│   ├── generator/
│   └── requirements.txt
│
├── GreenCode/
│   └── frontend/
│
└── README.md
```

---

## 🚀 Getting Started

### Clone

```bash
git clone https://github.com/Kanishkamangal/GreenCode-Analyzer.git
cd GreenCode
```

### Backend

```bash
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
```

Run the backend:

```bash
uvicorn backend.app.main:app --reload
```

### Frontend

```bash
cd GreenCode/frontend
npm install
npm run dev
```

---

## 🌱 Why GreenCode?

GreenCode makes it easier to understand that **software efficiency is more than just speed**.

By looking at performance, resource consumption, and energy together, developers can make more informed decisions when choosing between different implementations.

---

## 👩‍💻 Author

**Kanishka Mangal**
B.Tech Computer Science Engineering

---

⭐ If you find GreenCode interesting, consider giving the repository a star!

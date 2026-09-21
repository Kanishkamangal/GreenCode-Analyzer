import { useState } from "react";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Home from "./pages/Home";
import Benchmark from "./pages/Benchmark";
import LoginRegister from "./components/LoginRegister";

import DashboardLayout from "./components/dashboard/DashboardLayout";

import DashboardHome from "./pages/dashboard/DashboardHome";
import History from "./pages/dashboard/History";
import Reports from "./pages/dashboard/Reports";
import Settings from "./pages/dashboard/Settings";

import EditProfile from "./pages/dashboard/EditProfile";
import Feedback from "./pages/dashboard/Feedback";
import Help from "./pages/dashboard/Help";

function App() {

  const [showAuth, setShowAuth] = useState(false);
  return (

    <BrowserRouter>

      <div className="min-h-screen bg-[#F9FAFA]">

        <Routes>

          {/* =================================================
              HOME
          ================================================= */}

          <Route
            path="/"
            element={
              <Home
                onLogin={() => setShowAuth(true)}
              />
            }
          />


          {/* =================================================
              DASHBOARD WORKSPACE
          ================================================= */}

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >

            {/* ================= DASHBOARD ================= */}

            <Route
              index
              element={<DashboardHome />}
            />


            {/* ================= BENCHMARK ================= */}

            <Route
              path="benchmark"
              element={<Benchmark />}
            />


            {/* ================= HISTORY ================= */}

            <Route
              path="history"
              element={<History />}
            />


            {/* ================= REPORTS ================= */}

            <Route
              path="reports"
              element={<Reports />}
            />


            {/* ================= SETTINGS ================= */}

            <Route
              path="settings"
              element={<Settings />}
            />

            {/* =================================================
                EDIT PROFILE
            ================================================= */}

            <Route
              path="edit-profile"
              element={<EditProfile />}
            />

            {/* =================================================
                SEND FEEDBACK
            ================================================= */}

            <Route
              path="feedback"
              element={<Feedback />}
            />


            {/* =================================================
                HELP
            ================================================= */}

            <Route
              path="help"
              element={<Help />}
            />

          </Route>


          {/* =================================================
              OLD BENCHMARK URL
          ================================================= */}

          <Route
            path="/benchmark"
            element={
              <Navigate
                to="/dashboard/benchmark"
                replace
              />
            }
          />


          {/* =================================================
              UNKNOWN ROUTES
          ================================================= */}

          <Route
            path="*"
            element={
              <Navigate
                to="/"
                replace
              />
            }
          />
        </Routes>
        {/* =================================================
            AUTHENTICATION MODAL
        ================================================= */}

        {showAuth && (
          <LoginRegister

            onClose={() => {
              setShowAuth(false);
            }}
            onLogin={() => {
              setShowAuth(false);
              // navigate("/dashboard");
            }}
          />
        )}
      </div>
    </BrowserRouter>
  );
}

export default App;
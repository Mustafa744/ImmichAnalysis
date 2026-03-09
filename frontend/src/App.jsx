import { BrowserRouter, Routes, Route } from "react-router-dom";
import { FilterProvider } from "./context/FilterContext";
import AppShell from "./components/layout/AppShell";
import DashboardPage from "./pages/DashboardPage";
import TimelinePage from "./pages/TimelinePage";
import PhotoFrequencyPage from "./pages/PhotoFrequencyPage";

export default function App() {
  return (
    <BrowserRouter>
      <FilterProvider>
        <AppShell>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/timeline" element={<TimelinePage />} />
            <Route path="/frequency" element={<PhotoFrequencyPage />} />
          </Routes>
        </AppShell>
      </FilterProvider>
    </BrowserRouter>
  );
}

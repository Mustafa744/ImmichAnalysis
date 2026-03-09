import { FilterProvider } from "./context/FilterContext";
import AppShell from "./components/layout/AppShell";
import DashboardPage from "./pages/DashboardPage";

export default function App() {
  return (
    <FilterProvider>
      <AppShell>
        <DashboardPage />
      </AppShell>
    </FilterProvider>
  );
}

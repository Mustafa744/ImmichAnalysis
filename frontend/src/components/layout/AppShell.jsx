import { NavLink } from "react-router-dom";
import { Aperture, Map, TrendingUp, Clock, X } from "lucide-react";
import { useFilters } from "../../context/FilterContext";
import DateRangePicker from "../ui/DateRangePicker";

export default function AppShell({ children }) {
  const { dateFrom, dateTo, setDateRange, clearFilters, hasActiveFilters } =
    useFilters();

  const navItems = [
    { to: "/", icon: Map, label: "Country Overview" },
    { to: "/timeline", icon: TrendingUp, label: "Timeline" },
    { to: "/frequency", icon: Clock, label: "Photo Frequency" },
  ];

  return (
    <div className="flex h-screen overflow-hidden">
      {/* ── Sidebar ─────────────────────────────────────── */}
      <aside className="w-72 shrink-0 border-r border-border bg-bg-secondary flex flex-col">
        {/* Brand */}
        <div className="flex items-center gap-3 px-5 py-5 border-b border-border">
          <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-accent/15">
            <Aperture size={20} className="text-accent" />
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight">Immich</h1>
            <p className="text-[10px] text-text-muted uppercase tracking-widest">
              Photo Analytics
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 ${
                  isActive
                    ? "bg-accent/10 text-accent font-medium"
                    : "text-text-secondary hover:bg-bg-card hover:text-text-primary"
                }`
              }
            >
              <item.icon size={18} />
              <span className="text-sm">{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* ── Main Area ───────────────────────────────────── */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="flex items-center justify-end px-6 py-4 border-b border-border bg-bg-secondary/50 backdrop-blur-md">
          <div className="flex items-center gap-4">
            <DateRangePicker
              dateFrom={dateFrom}
              dateTo={dateTo}
              onChange={setDateRange}
            />

            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-lg bg-danger/10 text-danger hover:bg-danger/20 transition-colors cursor-pointer"
              >
                <X size={12} />
                Clear
              </button>
            )}
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}

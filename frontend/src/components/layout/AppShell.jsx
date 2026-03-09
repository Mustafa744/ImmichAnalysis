import { useCallback, useMemo } from "react";
import { Aperture, X, Search } from "lucide-react";
import { useFilters } from "../../context/FilterContext";
import { useApi } from "../../hooks/useApi";
import { fetchCountries, fetchCities } from "../../services/api";
import CountryCard from "../ui/CountryCard";
import DateRangePicker from "../ui/DateRangePicker";
import Loader from "../ui/Loader";

export default function AppShell({ children }) {
  const {
    selectedCountry,
    selectedCity,
    dateFrom,
    dateTo,
    setCountry,
    setCity,
    setDateRange,
    clearFilters,
    hasActiveFilters,
  } = useFilters();

  const countriesFetch = useCallback(() => fetchCountries(), []);
  const { data: countries, loading: countriesLoading } = useApi(
    countriesFetch,
    [],
  );

  const citiesFetch = useCallback(
    () =>
      selectedCountry ? fetchCities(selectedCountry) : Promise.resolve([]),
    [selectedCountry],
  );
  const { data: cities } = useApi(citiesFetch, [selectedCountry], {
    enabled: !!selectedCountry,
  });

  const sortedCountries = useMemo(() => {
    if (!countries) return [];
    return [...countries].sort((a, b) => b.count - a.count);
  }, [countries]);

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

        {/* Country list */}
        <div className="flex-1 overflow-y-auto px-3 py-3 space-y-1">
          {countriesLoading ? (
            <Loader rows={6} className="px-2" />
          ) : (
            sortedCountries.map((c) => (
              <CountryCard
                key={c.country}
                country={c.country}
                count={c.count}
                isActive={selectedCountry === c.country}
                onClick={() =>
                  setCountry(selectedCountry === c.country ? null : c.country)
                }
              />
            ))
          )}
        </div>

        {/* Sidebar footer */}
        <div className="px-4 py-3 border-t border-border">
          <p className="text-[10px] text-text-muted text-center">
            {countries?.length ?? 0} countries ·{" "}
            {countries?.reduce((s, c) => s + c.count, 0)?.toLocaleString() ?? 0}{" "}
            photos
          </p>
        </div>
      </aside>

      {/* ── Main Area ───────────────────────────────────── */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="flex items-center justify-between px-6 py-4 border-b border-border bg-bg-secondary/50 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <h2 className="text-lg font-semibold">
              {selectedCountry ? (
                <span className="flex items-center gap-2">
                  {selectedCountry}
                  {selectedCity && (
                    <span className="text-text-muted font-normal text-sm">
                      / {selectedCity}
                    </span>
                  )}
                </span>
              ) : (
                <span className="text-text-muted">
                  Select a country to explore
                </span>
              )}
            </h2>
          </div>

          <div className="flex items-center gap-4">
            {/* City picker */}
            {cities?.length > 0 && (
              <select
                value={selectedCity || ""}
                onChange={(e) => setCity(e.target.value || null)}
                className="bg-bg-card border border-border rounded-lg px-3 py-1.5 text-xs text-text-primary focus:outline-none focus:border-accent/50 transition-colors cursor-pointer"
              >
                <option value="">All Cities</option>
                {cities.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </select>
            )}

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

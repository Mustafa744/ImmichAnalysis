import React from "react";
import { useFilters } from "../context/FilterContext";
import StatsCards from "../components/charts/StatsCards";
import DailyTimeline from "../components/charts/DailyTimeline";
import HourlyDistribution from "../components/charts/HourlyDistribution";
import ColorHistogram from "../components/charts/ColorHistogram";
import IrqMetrics from "../components/charts/IrqMetrics";
import MomentsBreakdown from "../components/charts/MomentsBreakdown";
import ShotTypesChart from "../components/charts/ShotTypesChart";
import TopLocations from "../components/charts/TopLocations";
import Loader from "../components/ui/Loader";
import ErrorState from "../components/ui/ErrorState";
import { Sparkles } from "lucide-react";
import CountrySelector from "../components/ui/CountrySelector";
import DateRangePicker from "../components/ui/DateRangePicker";
import { useDashboardData } from "../hooks/useDashboardData";

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-full min-h-[60vh] gap-3 animate-fade-in-up">
      <div className="relative">
        <div className="absolute inset-0 bg-accent/20 blur-3xl rounded-full" />
        <div className="relative flex items-center justify-center w-24 h-24 rounded-3xl bg-bg-card border border-border">
          <Sparkles size={40} className="text-accent" />
        </div>
      </div>
      <h2 className="text-xl font-semibold text-text-primary">
        Your Photo Memories
      </h2>
      <p className="text-sm text-text-muted max-w-md text-center leading-relaxed">
        Select a country from the sidebar to explore your photo analytics —
        timelines, color profiles, shooting patterns, and more.
      </p>
    </div>
  );
}

export default function DashboardPage() {
  const {
    selectedCountry,
    selectedCity,
    setCountry,
    setCity,
    dateFrom,
    dateTo,
    setDateRange,
  } = useFilters();
  const {
    countries,
    cities,
    sortedCountries,
    overview,
    daily,
    hourly,
    histograms,
    moments,
    shotTypes,
    topLoc,
    anyLoading,
    firstError,
    hasCountry,
  } = useDashboardData();

  if (firstError) {
    return <ErrorState message={firstError} onRetry={overview.refetch} />;
  }

  return (
    <div className="gap-3 animate-fade-in-up pb-8 flex flex-col h-full">
      {/* Top Bar: Country & City Picker */}
      <div className="flex flex-col gap-3">
        <h2 className="text-xl font-semibold">
          {selectedCountry
            ? `Overview: ${selectedCountry}`
            : "Select a location"}
        </h2>

        <div className="flex flex-col md:flex-row items-center gap-3">
          <div className="flex-1 w-full md:w-auto">
            <CountrySelector
              countries={sortedCountries}
              selected={selectedCountry}
              onChange={setCountry}
              multi={false}
              loading={countries.loading}
              placeholder="Select a country..."
            />
          </div>

          {cities.data?.length > 0 && (
            <select
              value={selectedCity || ""}
              onChange={(e) => setCity(e.target.value || null)}
              className="bg-bg-card border border-border rounded-xl px-4 py-2.5 text-sm font-medium text-text-primary focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent/50 transition-all cursor-pointer min-w-[160px] h-[46px]"
            >
              <option value="">All Cities</option>
              {cities.data.map((city) => (
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
        </div>
      </div>

      {!hasCountry ? (
        <EmptyState />
      ) : anyLoading && !overview.data ? (
        <div className="flex flex-col gap-3 animate-fade-in-up">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            {[1, 2, 3, 4].map((i) => (
              <Loader key={i} rows={3} className="glass-card p-5" />
            ))}
          </div>
          <Loader rows={8} className="glass-card p-5" />
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {/* Row 1: Stats */}
          <StatsCards data={overview.data} />

          {/* Row 2: Timeline + Hourly */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
            {daily.loading ? (
              <Loader rows={6} className="glass-card p-5" />
            ) : (
              <DailyTimeline data={daily.data} />
            )}
            {hourly.loading ? (
              <Loader rows={6} className="glass-card p-5" />
            ) : (
              <HourlyDistribution data={hourly.data} />
            )}
          </div>

          {/* Row 3: Colors + Metrics */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
            {histograms.loading ? (
              <Loader rows={6} className="glass-card p-5" />
            ) : (
              <ColorHistogram data={histograms.data} />
            )}
            {histograms.loading ? (
              <Loader rows={6} className="glass-card p-5" />
            ) : (
              <IrqMetrics data={histograms.data} />
            )}
          </div>

          {/* Row 4: Insights */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
            {moments.loading ? (
              <Loader rows={6} className="glass-card p-5" />
            ) : (
              <MomentsBreakdown data={moments.data} />
            )}
            {shotTypes.loading ? (
              <Loader rows={6} className="glass-card p-5" />
            ) : (
              <ShotTypesChart data={shotTypes.data} />
            )}
            {topLoc.loading ? (
              <Loader rows={6} className="glass-card p-5" />
            ) : (
              <TopLocations data={topLoc.data} />
            )}
          </div>
        </div>
      )}
    </div>
  );
}

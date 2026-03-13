import React from "react";
import { Sparkles } from "lucide-react";
import { useFilters } from "../context/FilterContext";
import { useDashboardData } from "../hooks/useDashboardData";

// Charts & UI
import StatsCards from "../components/charts/StatsCards";
import DailyTimeline from "../components/charts/DailyTimeline";
import HourlyDistribution from "../components/charts/HourlyDistribution";
import ColorHistogram from "../components/charts/ColorHistogram";
import IrqMetrics from "../components/charts/IrqMetrics";
import MomentsBreakdown from "../components/charts/MomentsBreakdown";
import ShotTypesChart from "../components/charts/ShotTypesChart";
import TopLocations from "../components/charts/TopLocations";
import LocationPalette from "../components/charts/LocationPalette";
import Loader from "../components/ui/Loader";
import ErrorState from "../components/ui/ErrorState";
import CountrySelector from "../components/ui/CountrySelector";
import DateRangePicker from "../components/ui/DateRangePicker";

// ---------------------------------------------------------------------------
// 1. Extracted Pure UI Components (Keeps the main file clean)
// ---------------------------------------------------------------------------

const EmptyState = () => (
  <div className="flex flex-col items-center justify-center h-full min-h-[60vh] gap-3 animate-fade-in-up">
    <div className="relative">
      <div className="absolute inset-0 bg-accent/20 blur-3xl rounded-full" />
      <div className="relative flex items-center justify-center w-24 h-24 rounded-3xl bg-bg-card border border-border shadow-sm">
        <Sparkles size={40} className="text-accent" />
      </div>
    </div>
    <h2 className="text-xl font-semibold text-text-primary mt-4">Your Photo Memories</h2>
    <p className="text-sm text-text-muted max-w-md text-center leading-relaxed">
      Select a location from the controls above to explore your photo analytics —
      timelines, color profiles, shooting patterns, and more.
    </p>
  </div>
);

const InitialLoadingView = () => (
  <div className="flex flex-col gap-4 animate-fade-in-up">
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {[1, 2, 3, 4].map((i) => <Loader key={i} rows={3} className="glass-card p-5 h-32" />)}
    </div>
    <Loader rows={8} className="glass-card p-5 h-96" />
  </div>
);

// This single wrapper completely eliminates all `loading ? <Loader> : <Chart>` logic from your layout
const Widget = ({ loading = false, className = "", children }) => {
  if (loading) return <Loader rows={6} className={`glass-card p-5 w-full flex-shrink-0 ${className}`} />;
  
  return (
    <div className={`w-full flex flex-col ${className} [&>div]:h-full [&>div]:w-full [&>div]:min-h-0`}>
      {children}
    </div>
  );
};

// ---------------------------------------------------------------------------
// 2. Extracted Header Component
// ---------------------------------------------------------------------------

const DashboardControls = ({ filters, data }) => {
  const { selectedCountry, selectedCity, setCountry, setCity, dateFrom, dateTo, setDateRange } = filters;
  const { countries, cities, sortedCountries } = data;

  return (
    <div className="flex flex-col gap-4 bg-bg-card p-4 rounded-2xl border border-border shadow-sm shrink-0">
      <h2 className="text-lg font-semibold text-text-primary">
        {selectedCountry ? `Overview: ${selectedCountry}` : "Select a location"}
      </h2>
      <div className="flex flex-col md:flex-row items-center gap-3 w-full">
        <div className="flex-1 w-full md:w-auto">
          <CountrySelector
            countries={sortedCountries} selected={selectedCountry} onChange={setCountry}
            multi={false} loading={countries?.loading} placeholder="Select a country..."
          />
        </div>
        {cities?.data?.length > 0 && (
          <select
            value={selectedCity || ""} onChange={(e) => setCity(e.target.value || null)}
            className="bg-bg-card border border-border rounded-xl px-4 py-2.5 text-sm font-medium text-text-primary focus:outline-none focus:ring-2 focus:ring-accent/50 transition-all cursor-pointer min-w-[160px] h-[42px] w-full md:w-auto"
          >
            <option value="">All Cities</option>
            {cities.data.map((city) => <option key={city} value={city}>{city}</option>)}
          </select>
        )}
        <div className="w-full md:w-auto">
          <DateRangePicker dateFrom={dateFrom} dateTo={dateTo} onChange={setDateRange} />
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// 3. Main Dashboard Layout (Now purely semantic and easy to read)
// ---------------------------------------------------------------------------

export default function DashboardPage() {
  const filters = useFilters();
  const dashboardData = useDashboardData();
  
  const { overview, daily, hourly, histograms, moments, shotTypes, topLoc, palettes, anyLoading, firstError, hasCountry } = dashboardData;

  // Global States
  if (firstError) return <ErrorState message={firstError} onRetry={overview?.refetch} />;

  return (
    <div className="flex flex-col h-full gap-5 pb-8 animate-fade-in-up">
      
      <DashboardControls filters={filters} data={dashboardData} />

      {!hasCountry ? (
        <EmptyState />
      ) : anyLoading && !overview?.data ? (
        <InitialLoadingView />
      ) : (
        <div className="flex flex-col gap-4">
          
          <Widget loading={overview?.loading} className="shrink-0">
            <StatsCards data={overview?.data} />
          </Widget>

          {/* Dual Column Layout */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 min-h-[550px]">
            {/* Left Column */}
            <div className="flex flex-col gap-4 h-full">
              <Widget loading={daily?.loading} className="shrink-0 h-[350px]">
                <DailyTimeline data={daily?.data} />
              </Widget>
              <Widget loading={histograms?.loading} className="flex-1 min-h-0">
                <ColorHistogram data={histograms?.data} />
              </Widget>
            </div>

            {/* Right Column */}
            <div className="flex flex-col gap-4 h-full">
              <Widget loading={palettes?.loading} className="shrink-0">
                <LocationPalette data={palettes?.data} loading={palettes?.loading} />
              </Widget>
              <Widget loading={hourly?.loading} className="flex-1 min-h-0">
                <HourlyDistribution data={hourly?.data} />
              </Widget>
            </div>
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 h-auto xl:h-[350px]">
            <Widget loading={histograms?.loading}>
              <IrqMetrics data={histograms?.data} />
            </Widget>
            <div className="hidden xl:block"></div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-auto lg:h-[350px]">
            <Widget loading={moments?.loading}>
              <MomentsBreakdown data={moments?.data} />
            </Widget>
            <Widget loading={shotTypes?.loading}>
              <ShotTypesChart data={shotTypes?.data} />
            </Widget>
            <Widget loading={topLoc?.loading}>
              <TopLocations data={topLoc?.data} />
            </Widget>
          </div>

        </div>
      )}
    </div>
  );
}
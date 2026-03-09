import { useCallback } from "react";
import { useFilters } from "../context/FilterContext";
import { useApi } from "../hooks/useApi";
import * as api from "../services/api";

import StatsCards from "../components/charts/StatsCards";
import DailyTimeline from "../components/charts/DailyTimeline";
import HourlyDistribution from "../components/charts/HourlyDistribution";
import ColorHistogram from "../components/charts/ColorHistogram";
import IrqMetrics from "../components/charts/IrqMetrics";
import MomentsBreakdown from "../components/charts/MomentsBreakdown";
import ShotTypesChart from "../components/charts/ShotTypesChart";
import TopLocations from "../components/charts/TopLocations";
import TripsList from "../components/charts/TripsList";
import Loader from "../components/ui/Loader";
import ErrorState from "../components/ui/ErrorState";
import { BarChart3, Sparkles } from "lucide-react";

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-full min-h-[60vh] gap-4 animate-fade-in-up">
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
  const { filterParams, selectedCountry } = useFilters();
  const hasCountry = !!selectedCountry;

  // ── Data fetching ──────────────────────────────────
  const overviewFn = useCallback(
    () => api.fetchOverview(filterParams),
    [filterParams],
  );
  const dailyFn = useCallback(
    () => api.fetchDailyTimeline(filterParams),
    [filterParams],
  );
  const hourlyFn = useCallback(
    () => api.fetchHourlyTimeline(filterParams),
    [filterParams],
  );
  const histogramsFn = useCallback(
    () => api.fetchHistograms(filterParams),
    [filterParams],
  );
  const momentsFn = useCallback(
    () => api.fetchMoments(filterParams),
    [filterParams],
  );
  const shotTypesFn = useCallback(
    () => api.fetchShotTypes(filterParams),
    [filterParams],
  );
  const topLocFn = useCallback(
    () => api.fetchTopLocations(filterParams),
    [filterParams],
  );
  const tripsFn = useCallback(
    () => api.fetchTrips(filterParams),
    [filterParams],
  );

  const overview = useApi(overviewFn, [filterParams], { enabled: hasCountry });
  const daily = useApi(dailyFn, [filterParams], { enabled: hasCountry });
  const hourly = useApi(hourlyFn, [filterParams], { enabled: hasCountry });
  const histograms = useApi(histogramsFn, [filterParams], {
    enabled: hasCountry,
  });
  const moments = useApi(momentsFn, [filterParams], { enabled: hasCountry });
  const shotTypes = useApi(shotTypesFn, [filterParams], {
    enabled: hasCountry,
  });
  const topLoc = useApi(topLocFn, [filterParams], { enabled: hasCountry });
  const trips = useApi(tripsFn, [filterParams], { enabled: hasCountry });

  if (!hasCountry) return <EmptyState />;

  const anyLoading =
    overview.loading || daily.loading || hourly.loading || histograms.loading;
  const firstError = overview.error || daily.error;

  if (anyLoading && !overview.data) {
    return (
      <div className="space-y-6 animate-fade-in-up">
        <Loader rows={2} />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <Loader key={i} rows={3} className="glass-card p-5" />
          ))}
        </div>
        <Loader rows={8} className="glass-card p-5" />
      </div>
    );
  }

  if (firstError) {
    return <ErrorState message={firstError} onRetry={overview.refetch} />;
  }

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Row 1: Stats */}
      <StatsCards data={overview.data} />

      {/* Row 2: Timeline + Hourly */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
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
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
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
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
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

      {/* Row 5: Trips */}
      {trips.loading ? (
        <Loader rows={4} className="glass-card p-5" />
      ) : (
        <TripsList data={trips.data} />
      )}
    </div>
  );
}

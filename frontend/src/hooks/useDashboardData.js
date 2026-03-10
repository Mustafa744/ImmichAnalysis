import { useCallback, useMemo } from 'react';
import { useApi } from './useApi';
import * as api from '../services/api';
import { useFilters } from '../context/FilterContext';

export function useDashboardData() {
  const { filterParams, selectedCountry } = useFilters();
  const hasCountry = !!selectedCountry;

  // ── Country/City Fetching ──────────────────────────
  const countriesFetch = useCallback(() => api.fetchCountries(), []);
  const countries = useApi(countriesFetch, []);

  const citiesFetch = useCallback(
    () => (selectedCountry ? api.fetchCities(selectedCountry) : Promise.resolve([])),
    [selectedCountry]
  );
  const cities = useApi(citiesFetch, [selectedCountry], {
    enabled: !!selectedCountry,
  });

  const sortedCountries = useMemo(() => {
    if (!countries.data) return [];
    return [...countries.data].sort((a, b) => b.count - a.count);
  }, [countries.data]);

  // ── Data fetching ──────────────────────────────────
  const overviewFn = useCallback(() => api.fetchOverview(filterParams), [filterParams]);
  const dailyFn = useCallback(() => api.fetchDailyTimeline(filterParams), [filterParams]);
  const hourlyFn = useCallback(() => api.fetchHourlyTimeline(filterParams), [filterParams]);
  const histogramsFn = useCallback(() => api.fetchHistograms(filterParams), [filterParams]);
  const momentsFn = useCallback(() => api.fetchMoments(filterParams), [filterParams]);
  const shotTypesFn = useCallback(() => api.fetchShotTypes(filterParams), [filterParams]);
  const topLocFn = useCallback(() => api.fetchTopLocations(filterParams), [filterParams]);
  const tripsFn = useCallback(() => api.fetchTrips(filterParams), [filterParams]);

  const overview = useApi(overviewFn, [filterParams], { enabled: hasCountry });
  const daily = useApi(dailyFn, [filterParams], { enabled: hasCountry });
  const hourly = useApi(hourlyFn, [filterParams], { enabled: hasCountry });
  const histograms = useApi(histogramsFn, [filterParams], { enabled: hasCountry });
  const moments = useApi(momentsFn, [filterParams], { enabled: hasCountry });
  const shotTypes = useApi(shotTypesFn, [filterParams], { enabled: hasCountry });
  const topLoc = useApi(topLocFn, [filterParams], { enabled: hasCountry });
  const trips = useApi(tripsFn, [filterParams], { enabled: hasCountry });

  const anyLoading =
    hasCountry &&
    (overview.loading || daily.loading || hourly.loading || histograms.loading);
  const firstError = hasCountry && (overview.error || daily.error);

  return {
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
    trips,
    anyLoading,
    firstError,
    hasCountry,
  };
}

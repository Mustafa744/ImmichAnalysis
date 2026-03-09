import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
});

// ── Helpers ─────────────────────────────────────────────────
function buildFilterParams(filters = {}) {
  const params = new URLSearchParams();
  if (filters.country) params.append('country', filters.country);
  if (filters.city) params.append('city', filters.city);
  if (filters.dateFrom) params.append('from', filters.dateFrom);
  if (filters.dateTo) params.append('to', filters.dateTo);
  return params;
}

async function get(url, filters) {
  const params = buildFilterParams(filters);
  const { data } = await api.get(url, { params });
  return data;
}

// ── Stats ───────────────────────────────────────────────────
export const fetchOverview = (filters) => get('/stats/overview', filters);

// ── Countries ───────────────────────────────────────────────
export const fetchCountries = () => get('/countries');
export const fetchCities = (country) => get(`/countries/${encodeURIComponent(country)}/cities`);
export const fetchHeatmap = (country, filters) =>
  get(`/countries/${encodeURIComponent(country)}/heatmap`, filters);

// ── Timeline ────────────────────────────────────────────────
export const fetchDailyTimeline = (filters) => get('/timeline/daily', filters);
export const fetchHourlyTimeline = (filters) => get('/timeline/hourly', filters);
export const fetchTrips = (filters) => get('/timeline/trips', filters);
export const fetchTripDetails = (tripId, filters) => get(`/timeline/trips/${tripId}`, filters);

// ── Colors ──────────────────────────────────────────────────
export const fetchHistograms = (filters) => get('/colors/histograms', filters);
export const fetchPalette = (filters) => get('/colors/palette', filters);

// ── Insights ────────────────────────────────────────────────
export const fetchMoments = (filters) => get('/insights/moments', filters);
export const fetchShotTypes = (filters) => get('/insights/shot-types', filters);
export const fetchBurstClusters = (filters) => get('/insights/burst-clusters', filters);
export const fetchTopLocations = (filters) => get('/insights/top-locations', filters);

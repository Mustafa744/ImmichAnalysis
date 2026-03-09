import React, { useState, useCallback, useMemo } from "react";
import { useFilters } from "../context/FilterContext";
import { useApi } from "../hooks/useApi";
import * as api from "../services/api";
import MultiDailyTimeline from "../components/charts/MultiDailyTimeline";
import Loader from "../components/ui/Loader";
import { Check, TrendingUp } from "lucide-react";

export default function TimelinePage() {
  const { filterParams } = useFilters();
  const [selectedCountries, setSelectedCountries] = useState([]);

  const countriesFetch = useCallback(() => api.fetchCountries(), []);
  const { data: countries, loading: countriesLoading } = useApi(
    countriesFetch,
    [],
  );

  const sortedCountries = useMemo(() => {
    if (!countries) return [];
    return [...countries].sort((a, b) => b.count - a.count);
  }, [countries]);

  const toggleCountry = (country) => {
    setSelectedCountries((prev) =>
      prev.includes(country)
        ? prev.filter((c) => c !== country)
        : [...prev, country],
    );
  };

  const fetchAllTimelines = useCallback(async () => {
    if (selectedCountries.length === 0) return [];
    const promises = selectedCountries.map(async (country) => {
      const data = await api.fetchDailyTimeline({ ...filterParams, country });
      return { country, data };
    });
    return Promise.all(promises);
  }, [selectedCountries, filterParams]);

  const {
    data: timelinesData,
    loading: timelinesLoading,
    error: timelinesError,
  } = useApi(fetchAllTimelines, [selectedCountries, filterParams]);

  const mergedData = useMemo(() => {
    if (!timelinesData || timelinesData.length === 0) return [];

    const dateSet = new Set();
    timelinesData.forEach((item) => {
      if (item.data && Array.isArray(item.data)) {
        item.data.forEach((d) => dateSet.add(d.date));
      }
    });

    const dates = Array.from(dateSet).sort((a, b) => new Date(a) - new Date(b));

    return dates.map((date) => {
      const point = { date };
      timelinesData.forEach(({ country, data }) => {
        if (data && Array.isArray(data)) {
          const match = data.find((d) => d.date === date);
          point[country] = match ? match.count : null;
        } else {
          point[country] = null;
        }
      });
      return point;
    });
  }, [timelinesData]);

  return (
    <div className="space-y-6 animate-fade-in-up pb-8 flex flex-col h-full">
      <div className="flex flex-col gap-3">
        <div className="flex items-center gap-2 mb-2">
          <TrendingUp className="text-accent" />
          <h2 className="text-xl font-semibold">Timeline Comparison</h2>
        </div>

        <div className="flex items-center gap-3 overflow-x-auto pb-2 custom-scrollbar">
          {countriesLoading ? (
            <Loader rows={1} className="w-full h-12" />
          ) : (
            sortedCountries.map((c) => {
              const isActive = selectedCountries.includes(c.country);
              return (
                <button
                  key={c.country}
                  onClick={() => toggleCountry(c.country)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl border whitespace-nowrap transition-all duration-200 ${
                    isActive
                      ? "bg-accent/15 border-accent text-accent"
                      : "bg-bg-card border-border text-text-secondary hover:border-accent/50 hover:text-text-primary"
                  }`}
                >
                  {isActive && <Check size={14} />}
                  <span className="font-medium text-sm">{c.country}</span>
                  <span className="text-xs opacity-60">({c.count})</span>
                </button>
              );
            })
          )}
        </div>
      </div>

      {selectedCountries.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-text-muted">
          Select one or more countries above to compare timelines.
        </div>
      ) : timelinesLoading ? (
        <Loader rows={8} className="glass-card p-5 w-full" />
      ) : timelinesError ? (
        <div className="glass-card p-5 text-danger">{timelinesError}</div>
      ) : (
        <div className="w-full">
          <MultiDailyTimeline data={mergedData} countries={selectedCountries} />
        </div>
      )}
    </div>
  );
}

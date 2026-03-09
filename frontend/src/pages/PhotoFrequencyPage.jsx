import React, { useState, useCallback, useMemo } from "react";
import { useFilters } from "../context/FilterContext";
import { useApi } from "../hooks/useApi";
import * as api from "../services/api";
import MultiHourlyDistribution from "../components/charts/MultiHourlyDistribution";
import Loader from "../components/ui/Loader";
import { Check, Clock } from "lucide-react";

export default function PhotoFrequencyPage() {
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

  const fetchAllFrequencies = useCallback(async () => {
    if (selectedCountries.length === 0) return [];
    const promises = selectedCountries.map(async (country) => {
      const data = await api.fetchHourlyTimeline({ ...filterParams, country });
      return { country, data };
    });
    return Promise.all(promises);
  }, [selectedCountries, filterParams]);

  const {
    data: frequencyData,
    loading: frequencyLoading,
    error: frequencyError,
  } = useApi(fetchAllFrequencies, [selectedCountries, filterParams]);

  const mergedData = useMemo(() => {
    if (!frequencyData || frequencyData.length === 0) return [];

    const hourSet = new Set();
    frequencyData.forEach((item) => {
      if (item.data && Array.isArray(item.data)) {
        item.data.forEach((d) => hourSet.add(d.hour));
      }
    });

    const hours = Array.from(hourSet).sort((a, b) => a - b);

    return hours.map((hour) => {
      const point = { hour };
      frequencyData.forEach(({ country, data }) => {
        if (data && Array.isArray(data)) {
          const match = data.find((d) => d.hour === hour);
          point[country] = match ? match.count : 0;
        } else {
          point[country] = 0;
        }
      });
      return point;
    });
  }, [frequencyData]);

  return (
    <div className="space-y-6 animate-fade-in-up pb-8 flex flex-col h-full">
      <div className="flex flex-col gap-3">
        <div className="flex items-center gap-2 mb-2">
          <Clock className="text-accent" />
          <h2 className="text-xl font-semibold">Photo Frequency Comparison</h2>
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
          Select one or more countries above to compare photo frequencies.
        </div>
      ) : frequencyLoading ? (
        <Loader rows={8} className="glass-card p-5 w-full" />
      ) : frequencyError ? (
        <div className="glass-card p-5 text-danger">{frequencyError}</div>
      ) : (
        <div className="w-full">
          <MultiHourlyDistribution
            data={mergedData}
            countries={selectedCountries}
          />
        </div>
      )}
    </div>
  );
}

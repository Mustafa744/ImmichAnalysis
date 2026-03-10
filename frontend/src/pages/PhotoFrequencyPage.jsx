import React from "react";
import MultiHourlyDistribution from "../components/charts/MultiHourlyDistribution";
import Loader from "../components/ui/Loader";
import { Clock } from "lucide-react";
import DateRangePicker from "../components/ui/DateRangePicker";
import { useComparisonData } from "../hooks/useComparisonData";
import { useFilters } from "../context/FilterContext";

export default function PhotoFrequencyPage() {
  const {
    countries,
    sortedCountries,
    selectedCountries,
    setSelectedCountries,
    comparison,
    mergedData,
  } = useComparisonData("hourly");

  const { dateFrom, dateTo, setDateRange } = useFilters();

  return (
    <div className="flex flex-col items-center gap-8 animate-fade-in-up pb-8 max-w-6xl mx-auto px-4 md:px-8">
      <header className="flex flex-col items-center gap-4">
        <div className="flex items-center gap-2">
          <Clock className="text-accent" size={20} />
          <h1 className="text-xl font-bold tracking-tight">Photo Frequency</h1>
        </div>

        <div className="flex flex-col md:flex-row items-center gap-3 w-full justify-center">
          <CountrySelector
            countries={sortedCountries}
            selected={selectedCountries}
            onChange={setSelectedCountries}
            multi={true}
            loading={countries.loading}
            placeholder="Select countries to compare..."
          />
          <DateRangePicker
            dateFrom={dateFrom}
            dateTo={dateTo}
            onChange={setDateRange}
          />
        </div>
      </header>

      {selectedCountries.length === 0 ? (
        <div className="flex flex-col items-center justify-center flex-1 min-h-[50vh] gap-6 text-center">
          <div className="relative">
            <div className="absolute inset-0 bg-accent/20 blur-3xl rounded-full" />
            <div className="relative flex items-center justify-center w-20 h-20 rounded-3xl bg-bg-card border border-border">
              <Clock size={32} className="text-accent" />
            </div>
          </div>
          <div className="max-w-xs space-y-1">
            <h2 className="text-lg font-semibold text-text-primary">
              Frequency Analysis
            </h2>
            <p className="text-sm text-text-muted leading-relaxed">
              Select two or more countries above to compare their hourly photo
              distribution patterns.
            </p>
          </div>
        </div>
      ) : comparison.loading ? (
        <Loader rows={8} className="glass-card p-5 w-full" />
      ) : comparison.error ? (
        <div className="glass-card p-5 text-danger w-full">
          {comparison.error}
        </div>
      ) : (
        <MultiHourlyDistribution
          data={mergedData}
          countries={selectedCountries}
        />
      )}
    </div>
  );
}

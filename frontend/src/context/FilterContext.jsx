import {
  createContext,
  useContext,
  useState,
  useMemo,
  useCallback,
} from "react";

const FilterContext = createContext(null);

export function FilterProvider({ children }) {
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedCity, setSelectedCity] = useState(null);
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  const setCountry = useCallback((country) => {
    setSelectedCountry(country);
    setSelectedCity(null); // Reset city when country changes
  }, []);

  const setCity = useCallback((city) => {
    setSelectedCity(city);
  }, []);

  const setDateRange = useCallback((from, to) => {
    setDateFrom(from || "");
    setDateTo(to || "");
  }, []);

  const clearFilters = useCallback(() => {
    setSelectedCountry(null);
    setSelectedCity(null);
    setDateFrom("");
    setDateTo("");
  }, []);

  const filterParams = useMemo(() => {
    const params = {};
    if (selectedCountry) params.country = selectedCountry;
    if (selectedCity) params.city = selectedCity;
    if (dateFrom) params.dateFrom = dateFrom;
    if (dateTo) params.dateTo = dateTo;
    return params;
  }, [selectedCountry, selectedCity, dateFrom, dateTo]);

  const hasActiveFilters = useMemo(
    () => !!(selectedCountry || selectedCity || dateFrom || dateTo),
    [selectedCountry, selectedCity, dateFrom, dateTo],
  );

  const value = useMemo(
    () => ({
      selectedCountry,
      selectedCity,
      dateFrom,
      dateTo,
      filterParams,
      hasActiveFilters,
      setCountry,
      setCity,
      setDateRange,
      clearFilters,
    }),
    [
      selectedCountry,
      selectedCity,
      dateFrom,
      dateTo,
      filterParams,
      hasActiveFilters,
      setCountry,
      setCity,
      setDateRange,
      clearFilters,
    ],
  );

  return (
    <FilterContext.Provider value={value}>{children}</FilterContext.Provider>
  );
}

export function useFilters() {
  const ctx = useContext(FilterContext);
  if (!ctx) throw new Error("useFilters must be used within FilterProvider");
  return ctx;
}

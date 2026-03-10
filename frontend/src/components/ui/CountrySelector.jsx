import React, { useState, useRef, useEffect, useMemo } from "react";
import { Search, ChevronDown, Check, MapPin, X } from "lucide-react";
import { CHART_COLORS } from "../../utils/colors";

export default function CountrySelector({
  countries = [],
  selected = [], // array if multi, single string if not multi
  onChange,
  multi = false,
  loading = false,
  placeholder = "Select a country...",
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const dropdownRef = useRef(null);

  // Handle clicking outside to close
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Filter countries based on search query
  const filteredCountries = useMemo(() => {
    if (!searchQuery) return countries;
    const lowerQuery = searchQuery.toLowerCase();
    return countries.filter((c) =>
      c.country.toLowerCase().includes(lowerQuery),
    );
  }, [countries, searchQuery]);

  // Derived state for selections
  const selectedArray = multi ? selected : selected ? [selected] : [];

  const handleSelect = (countryName) => {
    if (multi) {
      const newSelected = selectedArray.includes(countryName)
        ? selectedArray.filter((c) => c !== countryName)
        : [...selectedArray, countryName];
      onChange(newSelected);
    } else {
      onChange(selected === countryName ? null : countryName);
      setIsOpen(false);
    }
    setSearchQuery(""); // Optionally clear search on select
  };

  const handleClear = (e) => {
    e.stopPropagation();
    onChange(multi ? [] : null);
  };

  const getButtonLabel = () => {
    if (loading) return "Loading countries...";
    if (selectedArray.length === 0) return placeholder;
    if (!multi) return selectedArray[0];
    if (selectedArray.length === 1) return selectedArray[0];
    return `${selectedArray.length} countries selected`;
  };

  return (
    <div className="relative w-full md:w-80" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={loading}
        className={`w-full flex items-center justify-between gap-3 px-4 py-2.5 bg-bg-card border rounded-xl transition-all duration-200 focus:outline-none ${
          isOpen
            ? "border-accent shadow-[0_0_10px_rgba(139,92,246,0.15)]"
            : "border-border hover:border-accent/50"
        } ${loading ? "opacity-60 cursor-not-allowed" : "cursor-pointer"}`}
      >
        <div className="flex items-center gap-2 overflow-hidden">
          <MapPin
            size={16}
            className={
              selectedArray.length > 0 ? "text-accent" : "text-text-muted"
            }
          />
          <span
            className={`text-sm font-medium truncate ${
              selectedArray.length > 0 ? "text-text-primary" : "text-text-muted"
            }`}
          >
            {getButtonLabel()}
          </span>
        </div>
        <div className="flex items-center gap-1 shrink-0">
          {selectedArray.length > 0 && (
            <div
              className="p-1 hover:bg-bg-secondary rounded-md text-text-muted hover:text-danger transition-colors"
              onClick={handleClear}
            >
              <X size={14} />
            </div>
          )}
          <ChevronDown
            size={16}
            className={`text-text-muted transition-transform duration-200 ${
              isOpen ? "rotate-180" : ""
            }`}
          />
        </div>
      </button>

      {/* Dropdown Popover */}
      {isOpen && (
        <div className="absolute top-full mt-2 bg-bg-card border border-border rounded-xl shadow-xl z-50 flex flex-col max-h-80 overflow-hidden animate-fade-in-up md:w-[320px] w-full right-0 md:right-auto">
          {/* Search Input */}
          <div className="p-3 border-b border-border bg-bg-secondary/50 backdrop-blur-sm sticky top-0 z-10">
            <div className="relative">
              <Search
                size={14}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted"
              />
              <input
                type="text"
                placeholder="Search countries..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-bg-card/80 border border-border rounded-lg pl-9 pr-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent/50 transition-colors"
                autoFocus
              />
            </div>
          </div>

          {/* List */}
          <div className="flex-1 overflow-y-auto custom-scrollbar p-1">
            {filteredCountries.length === 0 ? (
              <div className="p-4 text-center text-sm text-text-muted">
                No countries found.
              </div>
            ) : (
              filteredCountries.map((c) => {
                const isSelected = selectedArray.includes(c.country);
                const colorIndex = multi
                  ? selectedArray.indexOf(c.country)
                  : -1;
                const dotColor =
                  multi && colorIndex !== -1
                    ? CHART_COLORS[colorIndex % CHART_COLORS.length]
                    : null;

                return (
                  <button
                    key={c.country}
                    onClick={() => handleSelect(c.country)}
                    className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-left transition-colors ${
                      isSelected ? "bg-accent/10" : "hover:bg-bg-secondary"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      {multi && (
                        <div
                          className={`w-3 h-3 rounded-md border ${
                            isSelected
                              ? "bg-accent border-accent flex items-center justify-center"
                              : "border-border"
                          }`}
                          style={
                            isSelected && dotColor
                              ? {
                                  backgroundColor: dotColor,
                                  borderColor: dotColor,
                                }
                              : {}
                          }
                        >
                          {isSelected && (
                            <Check size={10} className="text-white" />
                          )}
                        </div>
                      )}
                      {!multi && isSelected && (
                        <Check size={14} className="text-accent" />
                      )}
                      {!multi && !isSelected && <div className="w-3.5" />}
                      <span
                        className={`text-sm ${
                          isSelected
                            ? "font-medium text-text-primary"
                            : "text-text-secondary"
                        }`}
                      >
                        {c.country}
                      </span>
                    </div>
                    <span className="text-xs text-text-muted bg-bg-secondary px-1.5 py-0.5 rounded-md">
                      {c.count}
                    </span>
                  </button>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
}

import { useState, useCallback, useMemo } from 'react';
import { useApi } from './useApi';
import * as api from '../services/api';
import { useFilters } from '../context/FilterContext';

export function useComparisonData(fetchType) {
  const { filterParams } = useFilters();
  const [selectedCountries, setSelectedCountries] = useState([]);

  const countriesFetch = useCallback(() => api.fetchCountries(), []);
  const countries = useApi(countriesFetch, []);

  const sortedCountries = useMemo(() => {
    if (!countries.data) return [];
    return [...countries.data].sort((a, b) => b.count - a.count);
  }, [countries.data]);

  const fetchAllData = useCallback(async () => {
    if (selectedCountries.length === 0) return [];
    const promises = selectedCountries.map(async (country) => {
      let data;
      if (fetchType === 'hourly') {
        data = await api.fetchHourlyTimeline({ ...filterParams, country });
      } else {
        data = await api.fetchDailyTimeline({ ...filterParams, country });
      }
      return { country, data };
    });
    return Promise.all(promises);
  }, [selectedCountries, filterParams, fetchType]);

  const comparison = useApi(fetchAllData, [selectedCountries, filterParams]);

  const mergedData = useMemo(() => {
    if (!comparison.data || comparison.data.length === 0) return [];

    const keySet = new Set();
    const keyAttr = fetchType === 'hourly' ? 'hour' : 'date';

    comparison.data.forEach((item) => {
      if (item.data && Array.isArray(item.data)) {
        item.data.forEach((d) => keySet.add(d[keyAttr]));
      }
    });

    const sortedKeys = Array.from(keySet).sort((a, b) => {
      if (fetchType === 'hourly') return a - b;
      return new Date(a) - new Date(b);
    });

    return sortedKeys.map((key) => {
      const point = { [keyAttr]: key };
      comparison.data.forEach(({ country, data }) => {
        if (data && Array.isArray(data)) {
          const match = data.find((d) => d[keyAttr] === key);
          point[country] = match ? match.count : (fetchType === 'hourly' ? 0 : null);
        } else {
          point[country] = fetchType === 'hourly' ? 0 : null;
        }
      });
      return point;
    });
  }, [comparison.data, fetchType]);

  return {
    countries,
    sortedCountries,
    selectedCountries,
    setSelectedCountries,
    comparison,
    mergedData,
  };
}

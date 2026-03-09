from fastapi import Query, HTTPException, Depends
from typing import List, Optional
from datetime import date


class LocationFilter:
    def __init__(
        self,
        countries: Optional[List[str]] = Query(
            None, alias="country", description="One or more country names"
        ),
        cities: Optional[List[str]] = Query(
            None, alias="city", description="One or more city names"
        ),
        date_from: Optional[date] = Query(
            None, alias="from", description="Start date filter (ISO YYYY-MM-DD)"
        ),
        date_to: Optional[date] = Query(
            None, alias="to", description="End date filter (ISO YYYY-MM-DD)"
        ),
    ):
        self.countries = countries or []
        self.cities = cities or []
        self.date_from = date_from
        self.date_to = date_to

        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise HTTPException(status_code=400, detail="from must be before to")


async def location_filter(filters: LocationFilter = Depends()) -> LocationFilter:
    return filters

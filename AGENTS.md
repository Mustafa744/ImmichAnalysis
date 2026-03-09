# AGENTS.md — Immich Analysis API Design

- Analysis pillars: **location, color, moments, attractions**
- Prefers metadata + classical CV and later will add some embedding based analysis

---

## Shared Filter System

### Dependency: `LocationFilter` (`src/api/deps.py`)
All analysis endpoints accept the same filter set via query params.

| Param       | Alias     | Type         | Description                          |
|-------------|-----------|--------------|--------------------------------------|
| `countries` | `country` | `list[str]`  | One or more country names            |
| `cities`    | `city`    | `list[str]`  | One or more city names               |
| `date_from` | `from`    | `date\|None` | Start date filter (ISO `YYYY-MM-DD`) |
| `date_to`   | `to`      | `date\|None` | End date filter (ISO `YYYY-MM-DD`)   |

### Rules
- Empty lists + no dates = **global** (no filter)
- **Cities take priority** over countries if both are provided
- `date_from > date_to` → raises `HTTP 400`
- City must belong to selected country (validate on frontend picker)

### Usage Pattern
```python
@router.get("/some-endpoint")
async def handler(loc: LocationFilter = Depends(location_filter)):
    return await analysis.module.get_data(loc)
DB Helper (src/db_client.py)
```

### Endpoints & API Contract

The backend now returns rich datasets rather than simple aggregations. Top-level categories typically include a `count` alongside a `photos` array (containing `{id, date, coords, city, country}`) to allow the frontend to instantly render drill-down grids when an aggregated slice is clicked.

```markdown
#### Stats
| Method | Endpoint | Description & Payload Shape |
|--------|----------|-----------------------------|
| `GET`  | `/api/v1/stats/overview` | Returns `{total_photos, countries, date_range, most_active_country, most_active_month}` |

#### Countries (Location)
| Method | Endpoint | Description & Payload Shape |
|--------|----------|-----------------------------|
| `GET`  | `/api/v1/countries` | `[{country, count, coords: {lat, lng}}]` (Global overview for picker) |
| `GET`  | `/api/v1/countries/{country}/cities` | `["CityA", "CityB"]` (Feeds city picker constraint) |
| `GET`  | `/api/v1/countries/{country}/heatmap` | `[{lat, lng}]` (Raw GPS points for overlay) |

#### Timeline (Time-Series Plotting)
| Method | Endpoint | Description & Payload Shape |
|--------|----------|-----------------------------|
| `GET`  | `/api/v1/timeline/daily` | `[{date: "YYYY-MM-DD", count, photos: [...]}]` (Zero-filled contiguous daily array) |
| `GET`  | `/api/v1/timeline/hourly` | `[{hour: 0-23, count, photos: [...]}]` (24-hour distribution array) |
| `GET`  | `/api/v1/timeline/trips` | `[{id, start, end, photos_count, city, country}]` |
| `GET`  | `/api/v1/timeline/trips/{id}` | `{id, count, photos: [...]}` |

#### Colors (Image Quality Plotting)
| Method | Endpoint | Description & Payload Shape |
|--------|----------|-----------------------------|
| `GET`  | `/api/v1/colors/histograms` | `{count, r_hist: [32 bins], g_hist: [...], b_hist: [...], brightness, colorfulness, warmth, sky_score}` |
| `GET`  | `/api/v1/colors/palette` | (TBD) Dynamic Hex distribution |
| `GET`  | `/api/v1/colors/trending` | (TBD) Mood shifts over time |

#### Insights (Categorical Breakdowns)
| Method | Endpoint | Description & Payload Shape |
|--------|----------|-----------------------------|
| `GET`  | `/api/v1/insights/moments` | `{"golden_hour": {count, photos: []}, "night": {...}, ...}` |
| `GET`  | `/api/v1/insights/shot-types` | `{"landscape": {count, photos: []}, "portrait": {...}, ...}` |
| `GET`  | `/api/v1/insights/burst-clusters` | `{"total_bursts": X, "burst_clusters": [{id, count, start, end}]}` |
| `GET`  | `/api/v1/insights/top-locations` | `[{country, city, count, photos: []}]` (Top 10 photo spots) |
```

---

## Overall Backend Description

The **Immich Analysis API** is a localized Python FastAPI service designed to ingest, process, and serve highly analytical subsets of a user's Immich photo library. 

1. **Analytical Engine**: Utilizing `numpy` and `PIL`, the backend downloads cache thumbnails from Immich and performs high-speed matrix extractions. It natively generates 32-bin RGB histograms alongside specialized Image Recognition Quality (IRQ) metrics like Brightness, Colorfulness, Warmth, and a synthetic Sky Score.
2. **Caching Layer (`ThumbnailCache`)**: Since pixel matrix mathematics can be expensive, analytical properties for each uniquely hashed photo are permanently stored to disk (via JSON mapping) ensuring real-time responsiveness when endpoints query aggregations.
3. **Data Service (`pandas`)**: The core database records (SQL Exif/Timeline data) are loaded into Memory as a contiguous `DataFrame`. The `LocationFilter` dependency operates instantly across this DataFrame, rapidly filtering vectors by Country, City, and Datetime bounds.

By tightly binding the vectorized Pandas queries with the cached thumbnail RGB arrays, the API endpoints successfully serve highly granular dynamic visualizations (like daily contiguous timeline arrays and real-time histogram curve generation bounded entirely by the user's active geographic filter inputs) formatted securely for React Recharts plotting integrations.



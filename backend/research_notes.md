# Location Palette Generation Logic

The **Location Palette** is a representative 5-color set that summarizes the visual "vibe" of a specific country or city. It isn't just a simple average of colors, which would often result in muddy browns or grays. Instead, it uses a weighted clustering approach to highlight significant and vibrant tones.

## 1. Data Aggregation
The process begins with the **Location Filter** (defined in `src/api/deps.py`).
- The system queries the Pandas DataFrame for all photos matching the selected `countries`, `cities`, and `date_range`.
- For every matching photo, the backend retrieves its pre-computed **Dominant Colors** from the `ThumbnailCache`. Each photo typically has 5–10 dominant colors with their respective proportions.

## 2. Saturation Boosting
To ensure that the pallet captures the characteristic "pops" of color (like the blue of a Santorini sky or the green of an Irish field), the system applies a **Saturation Boost**:
- Every color sample is converted to HSV.
- The weight of the color is multiplied by a factor based on its Saturation ($S$):
  - $Factor = 1 + Boost \times (S / 255)$
- With the current $Boost = 5.0$, a highly saturated color ($S=255$) gets a **6x higher weight** than a neutral gray ($S=0$). This prevents vivid colors from being "drowned out" by neutral background tones.

## 3. Perceptual Clustering (CIELAB)
Clustering in standard RGB space doesn't match human perception (e.g., humans are more sensitive to changes in green than blue).
- All collected colors are converted from **RGB** to **CIELAB** space.
- **MiniBatchKMeans** is used to group these thousands of color points into $k=5$ clusters.
- The algorithm uses the **saturation-boosted weights** to define the cluster centers. This means the clusters naturally gravitate towards the most prominent and vibrant color groups in the location.

## 4. Final Output
- The cluster centroids (centers) are converted back to RGB and Hex.
- The relative proportions are calculated based on the total weighted volume of each cluster.
- The result is a sorted list of colors representing the location's visual identity.

---

### Implementation Reference
- **Aggregation Handler**: [src/app/api/endpoints/palettes.py](file:///c:/Users/Aya/Desktop/Immich/backend/src/app/api/endpoints/palettes.py)
- **Clustering Engine**: [src/core/analysis/palette_analyzer.py](file:///c:/Users/Aya/Desktop/Immich/backend/src/core/analysis/palette_analyzer.py)
- **Cache Provider**: `src/infrastructure/persistence/cache.py`

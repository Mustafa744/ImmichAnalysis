from typing import Any, Dict, List, Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


METRICS = ["brightness", "colorfulness", "sky_score", "warmth"]

BINS = 32
BIN_EDGES = np.linspace(0, 256, BINS + 1)
BIN_CENTERS = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2


# --- HELPER FUNCTIONS ---


def _get_metric_values(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    filter_col: str,
    filter_val: str,
    metric: str,
    id_col: str = "id",
) -> List[float]:
    """Helper to extract metric values for a specific region."""
    ids = travel[travel[filter_col] == filter_val][id_col].tolist()
    return [results[i][metric] for i in ids if i in results]


def _plot_histograms(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    filter_col: str,
    filter_val: str,
    title_prefix: str,
    id_col: str = "id",
) -> None:
    """Core logic for the 4-panel histogram (Scalar Metrics) report."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"{title_prefix} Visual Distribution — {filter_val}", fontsize=14)

    for ax, metric in zip(axes.flat, METRICS):
        values = _get_metric_values(
            travel, results, filter_col, filter_val, metric, id_col
        )
        if not values:
            continue

        # We use seaborn to plot the exact distribution (KDE + Histogram) instead of averages
        sns.histplot(
            values, bins=30, kde=True, color="steelblue", ax=ax, edgecolor="white"
        )

        # Plot Median and Mean lines to show skewness
        median_val = np.median(values)
        ax.axvline(
            median_val,
            color="tomato",
            linestyle="--",
            linewidth=2,
            label=f"Median ({median_val:.1f})",
        )
        ax.set_title(metric.capitalize())
        ax.set_xlabel(metric)
        ax.set_ylabel("Density / Count")
        ax.legend(fontsize=9)

    plt.tight_layout()
    plt.show()


def _plot_color_profile(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    filter_col: str,
    filter_val: str,
    title_prefix: str,
    id_col: str = "id",
) -> None:
    """Core logic for the RGB Color Profile report with Median & IQR ribbons."""
    ids = travel[travel[filter_col] == filter_val][id_col].tolist()
    entries = [results[i] for i in ids if i in results]

    if not entries:
        print(f"  [SKIP] No cached data for {filter_val}")
        return

    # Extract 2D arrays (N photos x 32 bins) for each channel
    r_hists = np.array([e["r_hist"] for e in entries])
    g_hists = np.array([e["g_hist"] for e in entries])
    b_hists = np.array([e["b_hist"] for e in entries])

    # Calculate percentiles (25th, Median, 75th) instead of arithmetic mean
    r_med, r_25, r_75 = np.percentile(r_hists, [50, 25, 75], axis=0)
    g_med, g_25, g_75 = np.percentile(g_hists, [50, 25, 75], axis=0)
    b_med, b_25, b_75 = np.percentile(b_hists, [50, 25, 75], axis=0)

    plt.figure(figsize=(10, 5))
    plt.title(
        f"{title_prefix} Color Profile (Median + IQR) — {filter_val} ({len(entries)} photos)"
    )

    # Plot Median curves
    plt.plot(BIN_CENTERS, r_med, color="red", label="Red Median", linewidth=2)
    plt.plot(BIN_CENTERS, g_med, color="green", label="Green Median", linewidth=2)
    plt.plot(BIN_CENTERS, b_med, color="blue", label="Blue Median", linewidth=2)

    # Plot Interquartile Ranges (IQR) as shaded ribbons
    plt.fill_between(BIN_CENTERS, r_25, r_75, alpha=0.15, color="red", label="Red IQR")
    plt.fill_between(
        BIN_CENTERS, g_25, g_75, alpha=0.15, color="green", label="Green IQR"
    )
    plt.fill_between(
        BIN_CENTERS, b_25, b_75, alpha=0.15, color="blue", label="Blue IQR"
    )

    plt.xlabel("Pixel value (0–255)")
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    plt.show()


def _plot_timestamp_report(
    travel: pd.DataFrame,
    filter_col: str,
    filter_vals: Union[str, List[str]],
    title_prefix: str,
    date_col: str = "localDateTime",
) -> None:
    """Core logic to plot hourly histogram and daily timeline."""
    if isinstance(filter_vals, str):
        filter_vals = [filter_vals]

    # Filter the dataframe for any of the given values
    df = travel[travel[filter_col].isin(filter_vals)].copy()
    if df.empty:
        print(f"  [SKIP] No photo data for {filter_vals}")
        return

    df["dt"] = pd.to_datetime(df[date_col])
    df["hour"] = df["dt"].dt.hour
    df["date"] = pd.to_datetime(df["dt"].dt.date)

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    title_suffix = (
        ", ".join(filter_vals)
        if len(filter_vals) <= 3
        else f"{len(filter_vals)} {title_prefix}s"
    )
    fig.suptitle(
        f"{title_prefix} Hourly & Daily Timeline — {title_suffix} ({len(df)} photos)",
        fontsize=13,
    )

    # ── Left: hourly distribution ──────────────────────────────────────
    sns.histplot(
        data=df,
        x="hour",
        hue=filter_col,
        multiple="stack" if len(filter_vals) > 1 else "layer",
        discrete=True,
        ax=axes[0],
        palette="tab10",
    )
    axes[0].set_title("Photos by hour of day")
    axes[0].set_xlabel("Hour (0–23)")
    axes[0].set_ylabel("Photo count")
    axes[0].set_xticks(range(0, 24, 2))

    # Shade night hours context
    axes[0].axvspan(0, 6, alpha=0.08, color="black", label="Night")
    axes[0].axvspan(20, 24, alpha=0.08, color="black")

    # Optional: Fix legend if multiple overlapping
    if len(filter_vals) == 1 and axes[0].get_legend() is not None:
        axes[0].get_legend().remove()
        axes[0].legend(["Night"], fontsize=8)
    elif axes[0].get_legend() is not None:
        sns.move_legend(axes[0], "upper left", bbox_to_anchor=(1, 1))

    # ── Right: daily timeline ──────────────────────────────────────────
    # For a daily timeline of multiple countries over potentially non-overlapping dates,
    # a stacked histogram or staggered bar chart with seaborn works well.
    sns.histplot(
        data=df,
        x="date",
        hue=filter_col,
        multiple="stack",
        ax=axes[1],
        palette="tab10",
        bins=max(10, min(50, df["date"].nunique())),  # Heuristic for bin count
    )

    axes[1].set_title("Photos per day")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Photo count")

    # Rotate x labels for dates
    axes[1].tick_params(axis="x", rotation=45)

    if axes[1].get_legend() is not None:
        sns.move_legend(axes[1], "upper left", bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.show()


# --- PUBLIC API ---


def plot_country_histogram_report(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    country: str,
) -> None:
    """Plots the true density distribution (KDE+IQR) of visuals for a country."""
    _plot_color_profile(travel, results, "country", country, "Country")
    _plot_histograms(travel, results, "country", country, "Country")


def plot_city_histogram_report(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    city: str,
) -> None:
    """Plots the true density distribution (KDE+IQR) of visuals for a specific city."""
    _plot_color_profile(travel, results, "city", city, "City")
    _plot_histograms(travel, results, "city", city, "City")


def plot_country_timestamp_report(
    travel: pd.DataFrame,
    country: Union[str, List[str]],
    date_col: str = "localDateTime",
) -> None:
    """Plots the hourly and daily timeline distribution for one or more countries."""
    _plot_timestamp_report(travel, "country", country, "Country", date_col)


def plot_city_timestamp_report(
    travel: pd.DataFrame,
    city: Union[str, List[str]],
    date_col: str = "localDateTime",
) -> None:
    """Plots the hourly and daily timeline distribution for one or more cities."""
    _plot_timestamp_report(travel, "city", city, "City", date_col)

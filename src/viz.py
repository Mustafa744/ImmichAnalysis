import os
from datetime import datetime
from typing import Any, Dict, List, Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


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
    save_path: str = None,
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
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
        plt.close(fig)
    else:
        plt.show()


def _plot_color_profile(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    filter_col: str,
    filter_val: str,
    title_prefix: str,
    id_col: str = "id",
    save_path: str = None,
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

    fig = plt.figure(figsize=(10, 5))
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
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
        plt.close(fig)
    else:
        plt.show()


def _plot_timestamp_report(
    travel: pd.DataFrame,
    filter_col: str,
    filter_vals: Union[str, List[str]],
    title_prefix: str,
    date_col: str = "localDateTime",
    save_path: str = None,
) -> None:
    if isinstance(filter_vals, str):
        filter_vals = [filter_vals]

    df = travel[travel[filter_col].isin(filter_vals)].copy()
    if df.empty:
        print(f"  [SKIP] No photo data for {filter_vals}")
        return

    df["dt"] = pd.to_datetime(df[date_col])
    df["hour"] = df["dt"].dt.hour
    df["date"] = pd.to_datetime(df["dt"].dt.date)

    min_date = df["date"].min()
    max_date = df["date"].max()
    date_range_days = (max_date - min_date).days + 1
    n_groups = len(filter_vals)

    # Shared palette — consistent across both sub-plots
    palette = sns.color_palette("crest", n_colors=max(n_groups, 2))

    sns.set_theme(style="whitegrid", font_scale=1.02)
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(14, 9),
        gridspec_kw={"height_ratios": [1, 1.4]},
    )

    title_suffix = (
        ", ".join(filter_vals) if n_groups <= 3 else f"{n_groups} {title_prefix}s"
    )
    fig.suptitle(
        f"{title_prefix} Hourly & Daily Timeline — {title_suffix}  ({len(df)} photos)",
        fontsize=15,
        fontweight="bold",
        y=1.01,
    )

    # ── TOP: Hourly distribution ──────────────────────────────────────────
    ax0 = axes[0]

    # Time-of-day context zones drawn BEHIND bars (zorder=0)
    TIME_ZONES = [
        (0, 6, "#1a1a2e", 0.07, "Night"),
        (6, 12, "#f6d365", 0.08, "Morning"),
        (12, 18, "#fda085", 0.07, "Afternoon"),
        (18, 24, "#667eea", 0.08, "Evening"),
    ]
    for start, end, color, alpha, label in TIME_ZONES:
        ax0.axvspan(start - 0.5, end - 0.5, alpha=alpha, color=color, zorder=0)
        ax0.text(
            (start + end) / 2 - 0.5,
            1.0,
            label,
            ha="center",
            va="bottom",
            fontsize=8,
            color="grey",
            style="italic",
            transform=ax0.get_xaxis_transform(),
            zorder=1,
        )

    sns.histplot(
        data=df,
        x="hour",
        hue=filter_col if n_groups > 1 else None,
        multiple="stack" if n_groups > 1 else "layer",
        discrete=True,
        ax=ax0,
        palette="crest" if n_groups > 1 else None,
        color=palette[0] if n_groups == 1 else None,
        edgecolor="white",
        linewidth=1.2,
        alpha=0.88,
        zorder=2,
    )

    # Peak-hour annotation with arrow
    peak_hour = df["hour"].value_counts().idxmax()
    peak_count = df["hour"].value_counts().max()
    offset_dir = -3 if peak_hour > 18 else 3
    ax0.annotate(
        f"Peak\n{peak_hour:02d}:00",
        xy=(peak_hour, peak_count),
        xytext=(peak_hour + offset_dir, peak_count * 0.85),
        arrowprops=dict(arrowstyle="->", color="dimgray", lw=1.2),
        fontsize=9,
        color="dimgray",
        ha="center",
        zorder=3,
    )

    ax0.set_title("Photos by Hour of Day", fontsize=12, fontweight="semibold", pad=6)
    ax0.set_xlabel("Hour", fontsize=11)
    ax0.set_ylabel("Photo Count", fontsize=11)
    ax0.set_xticks(range(0, 24))
    ax0.set_xticklabels([f"{h:02d}" for h in range(24)], fontsize=8.5)
    ax0.set_xlim(-0.5, 23.5)
    ax0.grid(axis="y", linestyle="--", alpha=0.6, zorder=1)

    if n_groups == 1 and ax0.get_legend() is not None:
        ax0.get_legend().remove()
    elif ax0.get_legend() is not None:
        sns.move_legend(
            ax0,
            "upper left",
            bbox_to_anchor=(1.01, 1),
            title=filter_col.capitalize(),
            fontsize=9,
        )

    # ── BOTTOM: Daily timeline ────────────────────────────────────────────
    ax1 = axes[1]
    all_dates = pd.date_range(min_date, max_date, freq="D")

    if n_groups == 1:
        # Aggregate to daily counts and zero-fill gaps
        daily = (
            df.groupby("date")
            .size()
            .reindex(all_dates, fill_value=0)
            .rename_axis("date")
            .reset_index(name="count")
        )
        ax1.bar(
            daily["date"],
            daily["count"],
            width=0.75,
            color=palette[0],
            edgecolor="white",
            linewidth=0.6,
            alpha=0.9,
            label=filter_vals[0],
            zorder=2,
        )
        # Cumulative overlay on secondary y-axis
        ax1_r = ax1.twinx()
        ax1_r.plot(
            daily["date"],
            daily["count"].cumsum(),
            color="dimgray",
            linewidth=1.8,
            linestyle="--",
            alpha=0.65,
            label="Cumulative",
            zorder=3,
        )
        ax1_r.set_ylabel("Cumulative Photos", fontsize=10, color="dimgray")
        ax1_r.tick_params(axis="y", labelcolor="dimgray")
        ax1_r.spines["right"].set_visible(True)
        # Unified legend
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax1_r.get_legend_handles_labels()
        ax1.legend(h1 + h2, l1 + l2, fontsize=9, loc="upper left")

    else:
        # Manual stacked bars — no sns.histplot date hacks
        bottoms = np.zeros(len(all_dates))
        for idx, val in enumerate(filter_vals):
            sub_counts = (
                df[df[filter_col] == val]
                .groupby("date")
                .size()
                .reindex(all_dates, fill_value=0)
                .values
            )
            ax1.bar(
                all_dates,
                sub_counts,
                bottom=bottoms,
                width=0.75,
                color=palette[idx % len(palette)],
                edgecolor="white",
                linewidth=0.5,
                alpha=0.9,
                label=val,
                zorder=2,
            )
            bottoms += sub_counts

        ax1.legend(
            fontsize=9,
            bbox_to_anchor=(1.01, 1),
            loc="upper left",
            title=filter_col.capitalize(),
        )

    # Symmetric padding that scales with trip length
    x_pad = pd.Timedelta(days=max(1, date_range_days // 20))
    ax1.set_xlim(min_date - x_pad, max_date + x_pad)

    ax1.set_title(
        "Photos Chronological Timeline", fontsize=12, fontweight="semibold", pad=6
    )
    ax1.set_xlabel("Date", fontsize=11)
    ax1.set_ylabel("Photo Count", fontsize=11)
    ax1.grid(axis="y", linestyle="--", alpha=0.6, zorder=1)

    # Smart tick interval + two-line label removes all rotation
    interval = max(1, date_range_days // 14)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%Y"))
    ax1.tick_params(axis="x", rotation=0, labelsize=9)

    plt.tight_layout(pad=2.5)
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
        plt.close(fig)
    else:
        plt.show()

    sns.reset_orig()


def _compute_country_stats(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    country: str,
    date_col: str = "localDateTime",
    id_col: str = "id",
) -> Dict[str, Any]:
    """
    Aggregates per-country and per-city stats needed by the markdown generator.
    Returns a single flat dict so the generator stays purely presentational.
    """
    df = travel[travel["country"] == country].copy()
    df["dt"] = pd.to_datetime(df[date_col])
    df["date"] = pd.to_datetime(df["dt"].dt.date)
    df["hour"] = df["dt"].dt.hour

    day_counts = df.groupby("date").size()
    busiest_day = day_counts.idxmax()

    country_metrics = {
        m: np.median(v)
        if (v := _get_metric_values(travel, results, "country", country, m, id_col))
        else None
        for m in METRICS
    }

    cities = df["city"].dropna().unique().tolist()
    city_stats: Dict[str, Any] = {}
    for city in cities:
        cdf = df[df["city"] == city]
        city_ids = cdf[id_col].tolist()
        city_stats[city] = {
            "count": len(cdf),
            "first": cdf["dt"].min(),
            "last": cdf["dt"].max(),
            "peak_hour": int(cdf["hour"].value_counts().idxmax()),
            "metrics": {
                m: np.median([results[i][m] for i in city_ids if i in results])
                for m in METRICS
            },
        }

    return {
        "country": country,
        "total_photos": len(df),
        "first_date": df["dt"].min(),
        "last_date": df["dt"].max(),
        "duration_days": (df["dt"].max().date() - df["dt"].min().date()).days + 1,
        "peak_hour": int(df["hour"].value_counts().idxmax()),
        "busiest_day": busiest_day,
        "busiest_day_count": int(day_counts.max()),
        "cities": cities,
        "country_metrics": country_metrics,
        "city_stats": city_stats,
    }


# --- PUBLIC API ---


def plot_country_histogram_report(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    country: str,
    save_dir: str = None,
) -> None:
    """Plots the true density distribution (KDE+IQR) of visuals for a country."""
    if save_dir:
        color_dir = os.path.join(save_dir, "color_profiles")
        hist_dir = os.path.join(save_dir, "histograms")
        os.makedirs(color_dir, exist_ok=True)
        os.makedirs(hist_dir, exist_ok=True)
        color_path = os.path.join(color_dir, f"{country}.png")
        hist_path = os.path.join(hist_dir, f"{country}.png")
    else:
        color_path = None
        hist_path = None

    _plot_color_profile(
        travel, results, "country", country, "Country", save_path=color_path
    )
    _plot_histograms(
        travel, results, "country", country, "Country", save_path=hist_path
    )


def plot_city_histogram_report(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    city: str,
    save_dir: str = None,
) -> None:
    """Plots the true density distribution (KDE+IQR) of visuals for a specific city."""
    safe_city = city.replace("/", "_").replace("\\", "_")
    if save_dir:
        color_dir = os.path.join(save_dir, "color_profiles")
        hist_dir = os.path.join(save_dir, "histograms")
        os.makedirs(color_dir, exist_ok=True)
        os.makedirs(hist_dir, exist_ok=True)
        color_path = os.path.join(color_dir, f"{safe_city}.png")
        hist_path = os.path.join(hist_dir, f"{safe_city}.png")
    else:
        color_path = None
        hist_path = None

    _plot_color_profile(travel, results, "city", city, "City", save_path=color_path)
    _plot_histograms(travel, results, "city", city, "City", save_path=hist_path)


def plot_country_timestamp_report(
    travel: pd.DataFrame,
    country: Union[str, List[str]],
    date_col: str = "localDateTime",
    save_dir: str = None,
) -> None:
    """Plots the hourly and daily timeline distribution for one or more countries."""
    c_name = country if isinstance(country, str) else "_".join(country)
    if save_dir:
        time_dir = os.path.join(save_dir, "timelines")
        os.makedirs(time_dir, exist_ok=True)
        save_path = os.path.join(time_dir, f"{c_name}.png")
    else:
        save_path = None

    _plot_timestamp_report(
        travel, "country", country, "Country", date_col, save_path=save_path
    )


def plot_city_timestamp_report(
    travel: pd.DataFrame,
    city: Union[str, List[str]],
    date_col: str = "localDateTime",
    save_dir: str = None,
) -> None:
    """Plots the hourly and daily timeline distribution for one or more cities."""
    c_name = city if isinstance(city, str) else "_".join(city)
    safe_city = c_name.replace("/", "_").replace("\\", "_")
    if save_dir:
        time_dir = os.path.join(save_dir, "timelines")
        os.makedirs(time_dir, exist_ok=True)
        save_path = os.path.join(time_dir, f"{safe_city}.png")
    else:
        save_path = None

    _plot_timestamp_report(travel, "city", city, "City", date_col, save_path=save_path)


def generate_full_country_report(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    country: str,
    base_save_dir: str = "reports",
) -> None:
    """
    Generates all reports (color, histogram, timestamp) for a specific country
    and all its cities, then saves them into a designated directory.
    """
    # Create the country-specific subdirectory
    save_dir = os.path.join(base_save_dir, country)
    os.makedirs(save_dir, exist_ok=True)

    print(f"Generating full report for {country} in '{save_dir}'...")

    # 1. Generate Country-level reports
    plot_country_histogram_report(travel, results, country, save_dir=save_dir)
    plot_country_timestamp_report(travel, country, save_dir=save_dir)

    # 2. Generate City-level reports
    cities = travel[travel["country"] == country]["city"].dropna().unique()
    for city in cities:
        print(f"  -> Generating reports for city: {city}")
        plot_city_histogram_report(travel, results, city, save_dir=save_dir)
        plot_city_timestamp_report(travel, city, save_dir=save_dir)

    print(f"Done! All reports saved in {save_dir}/")


def generate_country_markdown_report(
    travel: pd.DataFrame,
    results: Dict[str, Dict[str, Any]],
    country: str,
    base_save_dir: str = "reports",
    generate_plots: bool = True,
    date_col: str = "localDateTime",
) -> str:
    """
    Builds a single structured Markdown report for a country and all its cities.
    Embeds the saved plot images (color profiles, histograms, timelines) using
    relative paths so the file is portable within the report directory.

    Parameters
    ----------
    travel         : The travel DataFrame.
    results        : Dict of per-photo metric results keyed by photo id.
    country        : Country name matching the 'country' column.
    base_save_dir  : Root reports directory (same as generate_full_country_report).
    generate_plots : If True, regenerates all PNG plots before writing the report.
    date_col       : Datetime column name in travel.

    Returns
    -------
    str  Markdown content (also saved as {base_save_dir}/{country}/report.md).
    """
    save_dir = os.path.join(base_save_dir, country)
    os.makedirs(save_dir, exist_ok=True)

    if generate_plots:
        generate_full_country_report(travel, results, country, base_save_dir)

    stats = _compute_country_stats(travel, results, country, date_col)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    safe = lambda name: name.replace("/", "_").replace("\\", "_")

    METRIC_FMT = {
        "brightness": ".1f",
        "colorfulness": ".1f",
        "sky_score": ".3f",
        "warmth": ".3f",
    }
    METRIC_ICON = {
        "brightness": "☀️",
        "colorfulness": "🎨",
        "sky_score": "🌤️",
        "warmth": "🌡️",
    }

    def fmt_metric(metric: str, val) -> str:
        return f"{val:{METRIC_FMT[metric]}}" if val is not None else "—"

    lines: List[str] = []

    # ── Title ─────────────────────────────────────────────────────────────────
    lines += [
        f"# 🗺️ Travel Report — {country}",
        "",
        f"> **Generated:** {generated_at}",
        "",
    ]

    # ── Overview table ────────────────────────────────────────────────────────
    lines += [
        "## Overview",
        "",
        "| | |",
        "|:---|:---|",
        f"| 📷 **Total Photos** | {stats['total_photos']} |",
        f"| 📅 **Date Range** | {stats['first_date'].strftime('%b %d, %Y')} → {stats['last_date'].strftime('%b %d, %Y')} |",
        f"| ⏱️ **Trip Duration** | {stats['duration_days']} days |",
        f"| 🏙️ **Cities Visited** | {len(stats['cities'])} — {', '.join(stats['cities'])} |",
        f"| 🕐 **Peak Shooting Hour** | {stats['peak_hour']:02d}:00 |",
        f"| 📆 **Busiest Day** | {stats['busiest_day'].strftime('%b %d, %Y')} ({stats['busiest_day_count']} photos) |",
        "",
    ]

    # ── City breakdown table ──────────────────────────────────────────────────
    lines += [
        "## City Breakdown",
        "",
        "| City | Photos | First Photo | Last Photo | Duration | Peak Hour |",
        "|:-----|-------:|:-----------:|:----------:|---------:|:---------:|",
    ]
    for city, cs in stats["city_stats"].items():
        dur = (cs["last"].date() - cs["first"].date()).days + 1
        lines.append(
            f"| {city} | {cs['count']} "
            f"| {cs['first'].strftime('%b %d, %Y')} "
            f"| {cs['last'].strftime('%b %d, %Y')} "
            f"| {dur}d "
            f"| {cs['peak_hour']:02d}:00 |"
        )
    lines.append("")

    # ── Metrics summary table ─────────────────────────────────────────────────
    city_list = list(stats["city_stats"].keys())
    lines += [
        "## Visual Metrics Summary",
        "",
        "> Median values across all photos. Higher brightness = more outdoor light. "
        "Sky score ∈ [0, 1]. Warmth ∈ [0, 1].",
        "",
        "| Metric | "
        + f"**{country}** | "
        + " | ".join(f"**{c}**" for c in city_list)
        + " |",
        "|:-------|" + ":----------:|" * (len(city_list) + 1),
    ]
    for metric in METRICS:
        country_str = fmt_metric(metric, stats["country_metrics"][metric])
        city_strs = [
            fmt_metric(metric, stats["city_stats"][c]["metrics"][metric])
            for c in city_list
        ]
        lines.append(
            f"| {METRIC_ICON[metric]} {metric.capitalize()} "
            f"| {country_str} | " + " | ".join(city_strs) + " |"
        )
    lines.append("")

    # ── Country-level plots ───────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "## Country-level Analysis",
        "",
        "### 🎨 Color Profile",
        "",
        f"![{country} Color Profile](color_profiles/{country}.png)",
        "",
        "### 📊 Metric Distributions",
        "",
        f"![{country} Histograms](histograms/{country}.png)",
        "",
        "### 📅 Timeline",
        "",
        f"![{country} Timeline](timelines/{country}.png)",
        "",
        "---",
        "",
        "## City Reports",
        "",
    ]

    # ── Per-city sections ─────────────────────────────────────────────────────
    for idx, city in enumerate(stats["cities"], 1):
        cs = stats["city_stats"][city]
        safe_city = safe(city)
        dur_city = (cs["last"].date() - cs["first"].date()).days + 1

        badges = "  ·  ".join(
            f"{METRIC_ICON[m]} **{m.capitalize()}** `{fmt_metric(m, cs['metrics'][m])}`"
            for m in METRICS
        )

        lines += [
            f"### {idx}. 🏙️ {city}",
            "",
            f"**{cs['count']} photos · "
            f"{cs['first'].strftime('%b %d')} – {cs['last'].strftime('%b %d, %Y')} · "
            f"{dur_city} days · "
            f"Peak: {cs['peak_hour']:02d}:00**",
            "",
            badges,
            "",
            "#### Color Profile",
            "",
            f"![{city} Color Profile](color_profiles/{safe_city}.png)",
            "",
            "#### Metric Distributions",
            "",
            f"![{city} Histograms](histograms/{safe_city}.png)",
            "",
            "#### Timeline",
            "",
            f"![{city} Timeline](timelines/{safe_city}.png)",
            "",
        ]
        if idx < len(stats["cities"]):
            lines += ["---", ""]

    md_content = "\n".join(lines)

    md_path = os.path.join(save_dir, "report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ Markdown report saved → {md_path}")
    return md_content

import os
from datetime import datetime
from typing import Any, Dict, List, Union, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


METRICS = ["brightness", "colorfulness", "sky_score", "warmth"]

BINS = 32
BIN_EDGES = np.linspace(0, 256, BINS + 1)
BIN_CENTERS = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2


class TravelVisualizer:
    """
    Object-oriented handler for analyzing and visually reporting travel photo data.
    """

    def __init__(
        self,
        travel: pd.DataFrame,
        results: Dict[str, Dict[str, Any]],
        date_col: str = "localDateTime",
        id_col: str = "id",
        min_images_thresh: int = 1,
    ):
        self.travel = travel
        self.results = results
        self.date_col = date_col
        self.id_col = id_col
        self.min_images_thresh = min_images_thresh

    # --- HELPER FUNCTIONS ---

    def _get_metric_values(
        self, filter_col: str, filter_val: str, metric: str
    ) -> List[float]:
        """Helper to extract metric values for a specific region."""
        ids = self.travel.loc[
            self.travel[filter_col] == filter_val, self.id_col
        ].tolist()
        return [self.results[i][metric] for i in ids if i in self.results]

    @staticmethod
    def _setup_save_paths(
        save_dir: str, subdirs: List[str], filename: str
    ) -> List[Optional[str]]:
        """Helper to create subdirectories and return file paths."""
        if not save_dir:
            return [None] * len(subdirs)
        paths = []
        for subdir in subdirs:
            d = os.path.join(save_dir, subdir)
            os.makedirs(d, exist_ok=True)
            paths.append(os.path.join(d, f"{filename}.png"))
        return paths

    def _plot_histograms(
        self,
        filter_col: str,
        filter_val: str,
        title_prefix: str,
        save_path: str = None,
    ) -> None:
        """Core logic for the 4-panel histogram (Scalar Metrics) report."""
        ids = self.travel[self.travel[filter_col] == filter_val][self.id_col].tolist()
        valid_ids = [i for i in ids if i in self.results]
        if len(valid_ids) < self.min_images_thresh:
            print(
                f"  [SKIP] Not enough data for {filter_val} histograms (needs {self.min_images_thresh})"
            )
            return

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f"{title_prefix} Visual Distribution — {filter_val}", fontsize=14)

        for ax, metric in zip(axes.flat, METRICS):
            values = self._get_metric_values(filter_col, filter_val, metric)
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
        self,
        filter_col: str,
        filter_val: str,
        title_prefix: str,
        save_path: str = None,
    ) -> None:
        """Core logic for the RGB Color Profile report with Median & IQR ribbons."""
        ids = self.travel[self.travel[filter_col] == filter_val][self.id_col].tolist()
        entries = [self.results[i] for i in ids if i in self.results]

        if len(entries) < self.min_images_thresh:
            print(
                f"  [SKIP] Not enough cached data for {filter_val} color profile (needs {self.min_images_thresh})"
            )
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
        plt.fill_between(
            BIN_CENTERS, r_25, r_75, alpha=0.15, color="red", label="Red IQR"
        )
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
        self,
        filter_col: str,
        filter_vals: Union[str, List[str]],
        title_prefix: str,
        save_path: str = None,
    ) -> None:
        if isinstance(filter_vals, str):
            filter_vals = [filter_vals]

        df = self.travel[self.travel[filter_col].isin(filter_vals)].copy()
        if len(df) < self.min_images_thresh:
            print(
                f"  [SKIP] Not enough photo data for {filter_vals} timestamp report (needs {self.min_images_thresh})"
            )
            return

        df["dt"] = pd.to_datetime(df[self.date_col])
        df["hour"] = df["dt"].dt.hour
        df["date"] = pd.to_datetime(df["dt"].dt.date)

        min_date = df["date"].min()
        max_date = df["date"].max()
        date_range_days = (max_date - min_date).days + 1
        n_groups = len(filter_vals)

        # Shared palette — consistent across both sub-plots
        if n_groups == 1:
            palette = sns.color_palette("crest", n_colors=2)
        else:
            palette = sns.color_palette("husl", n_colors=n_groups)

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
            palette=palette if n_groups > 1 else None,
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

        ax0.set_title(
            "Photos by Hour of Day", fontsize=12, fontweight="semibold", pad=6
        )
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

    def _compute_country_stats(self, country: str) -> Dict[str, Any]:
        """
        Aggregates per-country and per-city stats needed by the markdown generator.
        Returns a single flat dict so the generator stays purely presentational.
        """
        df = self.travel[self.travel["country"] == country].copy()
        if df.empty:
            return {}

        df["dt"] = pd.to_datetime(df[self.date_col])
        df["date"] = pd.to_datetime(df["dt"].dt.date)
        df["hour"] = df["dt"].dt.hour

        day_counts = df.groupby("date").size()
        busiest_day = day_counts.idxmax() if not day_counts.empty else None

        country_metrics = {
            m: np.median(v)
            if (v := self._get_metric_values("country", country, m))
            else None
            for m in METRICS
        }

        cities = (
            self.travel.loc[self.travel["country"] == country, "city"]
            .dropna()
            .unique()
            .tolist()
        )
        city_stats: Dict[str, Any] = {}
        for city in cities:
            cdf = df[df["city"] == city]
            if len(cdf) < self.min_images_thresh:
                continue

            city_ids = cdf[self.id_col].tolist()
            city_stats[city] = {
                "count": len(cdf),
                "first": cdf["dt"].min(),
                "last": cdf["dt"].max(),
                "peak_hour": int(cdf["hour"].value_counts().idxmax())
                if not cdf.empty
                else 0,
                "metrics": {
                    m: np.median(v)
                    if (
                        v := [self.results[i][m] for i in city_ids if i in self.results]
                    )
                    else None
                    for m in METRICS
                },
            }

        return {
            "country": country,
            "total_photos": len(df),
            "first_date": df["dt"].min(),
            "last_date": df["dt"].max(),
            "duration_days": (df["dt"].max().date() - df["dt"].min().date()).days + 1,
            "peak_hour": int(df["hour"].value_counts().idxmax()) if not df.empty else 0,
            "busiest_day": busiest_day,
            "busiest_day_count": int(day_counts.max()) if not day_counts.empty else 0,
            "cities": list(city_stats.keys()),
            "country_metrics": country_metrics,
            "city_stats": city_stats,
        }

    # --- WRAPPERS FOR PLOTTING API ---

    def _plot_histogram_report(
        self,
        filter_col: str,
        filter_val: str,
        title_prefix: str,
        save_dir: str = None,
    ) -> None:
        """Generic histogram & color profile generator."""
        safe_name = filter_val.replace("/", "_").replace("\\", "_")
        color_path, hist_path = self._setup_save_paths(
            save_dir, ["color_profiles", "histograms"], safe_name
        )
        self._plot_color_profile(
            filter_col, filter_val, title_prefix, save_path=color_path
        )
        self._plot_histograms(filter_col, filter_val, title_prefix, save_path=hist_path)

    def _plot_timeline_report(
        self,
        filter_col: str,
        filter_vals: Union[str, List[str]],
        title_prefix: str,
        save_dir: str = None,
    ) -> None:
        """Generic timeline generator."""
        c_name = filter_vals if isinstance(filter_vals, str) else "_".join(filter_vals)
        safe_name = c_name.replace("/", "_").replace("\\", "_")
        time_path = self._setup_save_paths(save_dir, ["timelines"], safe_name)[0]
        self._plot_timestamp_report(
            filter_col, filter_vals, title_prefix, save_path=time_path
        )

    # --- PUBLIC API ---

    def plot_country_histogram_report(self, country: str, save_dir: str = None) -> None:
        """Plots the true density distribution (KDE+IQR) of visuals for a country."""
        self._plot_histogram_report("country", country, "Country", save_dir)

    def plot_city_histogram_report(self, city: str, save_dir: str = None) -> None:
        """Plots the true density distribution (KDE+IQR) of visuals for a specific city."""
        self._plot_histogram_report("city", city, "City", save_dir)

    def plot_country_timestamp_report(
        self, country: Union[str, List[str]], save_dir: str = None
    ) -> None:
        """Plots the hourly and daily timeline distribution for one or more countries."""
        self._plot_timeline_report("country", country, "Country", save_dir)

    def plot_city_timestamp_report(
        self, city: Union[str, List[str]], save_dir: str = None
    ) -> None:
        """Plots the hourly and daily timeline distribution for one or more cities."""
        self._plot_timeline_report("city", city, "City", save_dir)

    def generate_full_country_report(
        self, country: str, base_save_dir: str = "reports"
    ) -> None:
        """
        Generates all reports (color, histogram, timestamp) for a specific country
        and all its cities, then saves them into a designated directory.
        """
        save_dir = os.path.join(base_save_dir, country)
        os.makedirs(save_dir, exist_ok=True)

        print(f"Generating full report for {country} in '{save_dir}'...")

        self.plot_country_histogram_report(country, save_dir=save_dir)
        self.plot_country_timestamp_report(country, save_dir=save_dir)

        cities = (
            self.travel[self.travel["country"] == country]["city"].dropna().unique()
        )
        for city in cities:
            cdf = self.travel[self.travel["city"] == city]
            if len(cdf) < self.min_images_thresh:
                continue
            print(f"  -> Generating reports for city: {city}")
            self.plot_city_histogram_report(city, save_dir=save_dir)
            self.plot_city_timestamp_report(city, save_dir=save_dir)

        print(f"Done! All reports saved in {save_dir}/")

    def generate_country_markdown_report(
        self, country: str, base_save_dir: str = "reports", generate_plots: bool = True
    ) -> str:
        """
        Builds a single structured Markdown report for a country and all its cities.
        Embeds the saved plot images (color profiles, histograms, timelines) using
        relative paths so the file is portable within the report directory.
        """
        save_dir = os.path.join(base_save_dir, country)
        os.makedirs(save_dir, exist_ok=True)

        df_country = self.travel[self.travel["country"] == country]
        if len(df_country) < self.min_images_thresh:
            print(
                f"Skipping markdown report for {country} (needs {self.min_images_thresh} photos)."
            )
            return ""

        if generate_plots:
            self.generate_full_country_report(country, base_save_dir)

        stats = self._compute_country_stats(country)
        if not stats:
            return ""

        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        def safe(name: str) -> str:
            return name.replace("/", "_").replace("\\", "_")

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

        lines: List[str] = [
            f"# 🗺️ Travel Report — {country}",
            "",
            f"> **Generated:** {generated_at}",
            "",
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
                f"| {METRIC_ICON[metric]} {metric.capitalize()} | {country_str} | "
                + " | ".join(city_strs)
                + " |"
            )
        lines.append("")

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
                f"**{cs['count']} photos · {cs['first'].strftime('%b %d')} – {cs['last'].strftime('%b %d, %Y')} · {dur_city} days · Peak: {cs['peak_hour']:02d}:00**",
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

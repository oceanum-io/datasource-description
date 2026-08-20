#!/usr/bin/env python3
"""
Generate Figure 1 for the Bass Strait Wave Forecast document.

The Bass Strait forecast nests have no gridstats datasource, so the figure is
built from a single forecast cycle instead: mean significant wave height over
the 7-day forecast, following the approach used by
/config/forecast/prax/swan/check_swan_output.py.

Three panels are produced, one per nest, each with depth contours, spectra
output sites and the bounding box of the nest it contains.

Usage:
    python scripts/generate_bass_forecast_figure1.py [CYCLE]

CYCLE defaults to the most recent cycle available on GCS (format YYYYMMDDTHH).
"""

import sys

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import gcsfs
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

BUCKET = "oceanum-prod-flush-1w/swan/gfs_aus"
OUTPUT = "figures/bass_forecast_figure1_hs_mean.png"

# nest id, model id, label, contour levels, extent pad (deg), coastline res
NESTS = [
    ("bass", "bass5km", "(a) Bass Strait 5 km", [50, 100, 200, 500, 1000], 0.1, "50m"),
    ("king", "king1km", "(b) King Island 1 km", [20, 50, 100], 0.02, "10m"),
    ("grassy", "grassy100m", "(c) Grassy 100 m", [10, 20, 30], 0.003, None),
]
# child nest drawn as a box on its parent panel
CHILD_BOX = {"bass": ("king", "King Island"), "king": ("grassy", "Grassy")}


def latest_cycle(fs: gcsfs.GCSFileSystem) -> str:
    """Most recent cycle string present for the parent domain."""
    paths = fs.ls(f"{BUCKET}/bass5km/post/grid")
    cycles = sorted(p.split("bass-grid-")[-1].replace(".zarr", "") for p in paths)
    if not cycles:
        raise SystemExit("No bass5km grid output found on GCS")
    return cycles[-1]


def load(nest: str, model_id: str, cycle: str) -> tuple[xr.Dataset, xr.Dataset]:
    grid = xr.open_zarr(f"gs://{BUCKET}/{model_id}/post/grid/{nest}-grid-{cycle}.zarr")
    spec = xr.open_zarr(f"gs://{BUCKET}/{model_id}/post/site/{nest}-spec-{cycle}.zarr")
    return grid, spec


def main(cycle: str | None = None) -> None:
    fs = gcsfs.GCSFileSystem()
    cycle = cycle or latest_cycle(fs)
    print(f"Using cycle {cycle}")

    data = {}
    for nest, model_id, *_ in NESTS:
        print(f"Loading {nest}...")
        grid, spec = load(nest, model_id, cycle)
        data[nest] = {
            "hs": grid.hs.mean(dim="time").load(),
            "depth": grid.depth.isel(time=0).load(),
            "lon": grid.longitude.values,
            "lat": grid.latitude.values,
            "site_lon": spec.lon.values.ravel(),
            "site_lat": spec.lat.values.ravel(),
            "bounds": (
                float(grid.longitude[0]),
                float(grid.longitude[-1]),
                float(grid.latitude[0]),
                float(grid.latitude[-1]),
            ),
        }
        print(f"  {len(data[nest]['site_lon'])} spectra sites")

    # Parent is wide and short, the two children are small: parent spans the top
    # row, children share the bottom row.
    fig = plt.figure(figsize=(12, 10))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.2], hspace=0.15, wspace=0.12)
    axes = [
        fig.add_subplot(gs[0, :], projection=ccrs.PlateCarree()),
        fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree()),
        fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree()),
    ]

    for ax, (nest, _, label, contours, pad, coast) in zip(axes, NESTS):
        d = data[nest]
        x0, x1, y0, y1 = d["bounds"]
        ax.set_extent([x0 - pad, x1 + pad, y0 - pad, y1 + pad], crs=ccrs.PlateCarree())
        # Dry cells are NaN in the model output; showing them as the axes
        # background renders the model's own land mask, which is the honest
        # coastline at these resolutions (a 100 m nest outruns any coastline
        # dataset cartopy ships).
        ax.set_facecolor("lightgray")

        mesh = ax.pcolormesh(
            d["lon"], d["lat"], d["hs"].values,
            transform=ccrs.PlateCarree(), cmap="turbo", shading="auto",
        )
        cbar = fig.colorbar(mesh, ax=ax, orientation="vertical", shrink=0.85, pad=0.02)
        cbar.set_label("Mean $H_s$ (m)", fontsize=9)
        cbar.ax.tick_params(labelsize=8)

        cs = ax.contour(
            d["lon"], d["lat"], d["depth"].values, levels=contours,
            colors="black", linewidths=0.4, alpha=0.5,
            transform=ccrs.PlateCarree(),
        )
        ax.clabel(cs, inline=True, fontsize=6, fmt="%d")

        ax.scatter(
            d["site_lon"], d["site_lat"], s=2.0, c="black", marker="o",
            transform=ccrs.PlateCarree(), zorder=12,
        )

        if nest in CHILD_BOX:
            child, child_label = CHILD_BOX[nest]
            cx0, cx1, cy0, cy1 = data[child]["bounds"]
            ax.add_patch(mpatches.Rectangle(
                (cx0, cy0), cx1 - cx0, cy1 - cy0,
                linewidth=1.5, edgecolor="white", facecolor="none",
                transform=ccrs.PlateCarree(), zorder=13,
            ))
            ax.text(
                (cx0 + cx1) / 2, cy1, child_label, transform=ccrs.PlateCarree(),
                fontsize=8, ha="center", va="bottom", color="white", zorder=14,
                bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="none", alpha=0.6),
            )

        if coast:
            ax.add_feature(
                cfeature.NaturalEarthFeature(
                    "physical", "land", coast, edgecolor="black", facecolor="none"
                ),
                linewidth=0.4, zorder=11,
            )
        gl = ax.gridlines(draw_labels=True, linewidth=0.3, alpha=0.4)
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {"size": 8}
        gl.ylabel_style = {"size": 8}
        ax.set_title(label, fontsize=11)

    cycle_label = f"{cycle[:4]}-{cycle[4:6]}-{cycle[6:8]} {cycle[9:11]}:00 UTC"
    fig.suptitle(
        f"Bass Strait wave forecast — 7-day mean $H_s$, GFS cycle {cycle_label}",
        fontsize=13, y=0.95,
    )
    fig.savefig(OUTPUT, dpi=150, bbox_inches="tight")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)

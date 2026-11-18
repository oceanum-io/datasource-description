#!/usr/bin/env python3
"""
Generate Figure 1 for the Northwest Cape Wave Forecast document.

Domain map in the style of the Southwest Western Australia forecast figure:
the Northwest Cape 5 km parent extent with the Gascoyne 500 m and Cape Cuvier
50 m nest boxes, depth contours from the parent grid, and spectra output sites
read from a forecast cycle on GCS.

Usage:
    python scripts/generate_nwcape_figure1.py [CYCLE]

CYCLE defaults to the most recent cycle available on GCS (format YYYYMMDDTHH).
"""

import sys

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import gcsfs
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import xarray as xr

BUCKET = "oceanum-prod-flush-1w/swan/gfs_aus"
OUTPUT = "figures/nwcape_figure1_domain.png"
CONTOURS = [200, 1000, 2000, 4000]

# label, x0, y0, x1, y1
NESTS = [
    ("Gascoyne 500 m", 113.0, -25.3, 113.9, -24.0),
    ("Cape Cuvier 50 m", 113.36, -24.25, 113.435, -24.2),
]
# nest id, model id, legend label
SITES = [
    ("nwcape", "nwcape5km", "Northwest Cape (5 km parent)"),
    ("cuvier", "cuvier50m", "Cape Cuvier 50 m"),
]


def latest_cycle(fs: gcsfs.GCSFileSystem) -> str:
    """Most recent cycle string with spectra output for the parent domain."""
    paths = fs.ls(f"{BUCKET}/nwcape5km/post/site")
    cycles = sorted(p.split("nwcape-spec-")[-1].replace(".zarr", "") for p in paths)
    if not cycles:
        raise SystemExit("No nwcape5km spectra output found on GCS")
    return cycles[-1]


def main(cycle: str | None = None) -> None:
    fs = gcsfs.GCSFileSystem()
    cycle = cycle or latest_cycle(fs)
    print(f"Using cycle {cycle}")

    grid = xr.open_zarr(f"gs://{BUCKET}/nwcape5km/post/grid/nwcape-grid-{cycle}.zarr")
    depth = grid.depth.isel(time=0).load()
    x0, x1 = float(grid.longitude[0]), float(grid.longitude[-1])
    y0, y1 = float(grid.latitude[0]), float(grid.latitude[-1])

    fig = plt.figure(figsize=(9, 11))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([x0, x1, y0, y1], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.OCEAN.with_scale("10m"), facecolor="#d1e7f4", zorder=0)
    ax.add_feature(
        cfeature.LAND.with_scale("10m"), facecolor="lightgray",
        edgecolor="black", linewidth=0.6, zorder=2,
    )

    cs = ax.contour(
        grid.longitude, grid.latitude, depth.values, levels=CONTOURS,
        colors="dimgray", linewidths=0.6, transform=ccrs.PlateCarree(), zorder=1,
    )
    ax.clabel(cs, inline=True, fontsize=8, fmt="%d m")

    for label, nx0, ny0, nx1, ny1 in NESTS:
        ax.add_patch(mpatches.Rectangle(
            (nx0, ny0), nx1 - nx0, ny1 - ny0, linewidth=1.5, edgecolor="black",
            facecolor="none", transform=ccrs.PlateCarree(), zorder=4,
        ))
    ax.text(
        113.0, -25.35, "Gascoyne 500 m", transform=ccrs.PlateCarree(),
        fontsize=9, ha="left", va="top", zorder=5,
    )

    for nest, model_id, label in SITES:
        spec = xr.open_zarr(f"gs://{BUCKET}/{model_id}/post/site/{nest}-spec-{cycle}.zarr")
        lon, lat = spec.lon.values.ravel(), spec.lat.values.ravel()
        print(f"  {nest}: {lon.size} spectra sites")
        if nest == "cuvier":
            ax.scatter(
                lon, lat, s=80, c="red", marker="*", edgecolor="black", linewidth=0.5,
                transform=ccrs.PlateCarree(), zorder=6, label=f"{label} (n={lon.size})",
            )
        else:
            ax.scatter(
                lon, lat, s=3, c="black", marker="o",
                transform=ccrs.PlateCarree(), zorder=5, label=f"{label} (n={lon.size})",
            )

    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)

    fig.savefig(OUTPUT, dpi=200, bbox_inches="tight")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)

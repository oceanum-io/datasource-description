#!/usr/bin/env python3
"""
Generate Figure 1 for the Peru (Lima / Chancay) Wave Forecast document.

Left panel: mean significant wave height from the Lima ERA5 hindcast gridstats
(same grid as the forecast parent domain) with depth contours, the Chancay
400 m nest box and the spectra output sites of both forecast domains.

Right panel: the Chancay 400 m nest only, showing the model bathymetry, the
nest spectra output sites and the location of the validation ADCP.

Usage:
    python scripts/generate_peru_forecast_figure1.py
"""

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from oceanum.datamesh import Connector

OUTPUT = "figures/peru_forecast_figure1_hs_mean.png"
GRIDSTATS = "oceanum_wave_lima_era5_gridstats"
CHANCAY_GRID = "oceanum_wave_gfs_chancay400m_grid_nowcast"
DEPTH_TIME = "2026-11-17T12:00:00"  # any single time step, depth is static
LIMA_SPEC = "oceanum_wave_gfs_lima5km_spec"
CHANCAY_SPEC = "oceanum_wave_gfs_chancay400m_spec"
EXTENT = [-79.0, -76.0, -13.0, -10.0]
CHANCAY = [-77.8, -77.1, -11.9, -11.2]
ADCP = (-77.2989976, -11.5976509)
CONTOURS = [50, 100, 200, 500, 1000, 2000]
CHANCAY_CONTOURS = [10, 20, 50, 100, 150, 200]
PC = ccrs.PlateCarree()


def site_coords(conn: Connector, datasource: str) -> tuple[np.ndarray, np.ndarray]:
    sites = conn.query(datasource=datasource, variables=["lon", "lat"])
    lon, lat = sites.lon.values.ravel(), sites.lat.values.ravel()
    print(f"{datasource}: {lon.size} sites")
    return lon, lat


def add_gridlines(ax) -> None:
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False


def main() -> None:
    conn = Connector()
    stats = conn.query(datasource=GRIDSTATS, variables=["hs_mean", "depth_mean"])
    nest = conn.query(
        datasource=CHANCAY_GRID, variables=["depth"],
        timefilter={"times": [DEPTH_TIME, DEPTH_TIME]},
    )
    depth = nest.depth.isel(time=0)
    lima_lon, lima_lat = site_coords(conn, LIMA_SPEC)
    chan_lon, chan_lat = site_coords(conn, CHANCAY_SPEC)
    x0, x1, y0, y1 = CHANCAY
    cbar_kwargs = {"orientation": "horizontal", "pad": 0.05, "shrink": 0.8}

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(16, 10), subplot_kw={"projection": PC},
        gridspec_kw={"wspace": 0.12},
    )

    # Left panel: Lima 5 km parent domain
    stats.hs_mean.plot(
        ax=ax1, transform=PC, cmap="turbo",
        cbar_kwargs={"label": "Mean Significant Wave Height (m)", **cbar_kwargs},
    )
    lon2d, lat2d = np.meshgrid(stats.longitude.values, stats.latitude.values)
    cs = ax1.contour(
        lon2d, lat2d, stats.depth_mean.values, levels=CONTOURS,
        colors="0.4", linewidths=0.5, transform=PC,
    )
    ax1.clabel(cs, inline=True, fontsize=8, fmt="%d m")
    ax1.scatter(
        lima_lon, lima_lat, s=20, c="black", marker=".", linewidths=0,
        transform=PC, zorder=5, label=f"Lima 5 km (n={lima_lon.size})",
    )
    ax1.scatter(
        chan_lon, chan_lat, s=12, c="blue", marker=".", linewidths=0,
        transform=PC, zorder=5, label=f"Chancay 400 m (n={chan_lon.size})",
    )
    ax1.plot(
        [x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], color="blue", linewidth=2,
        transform=PC, zorder=4,
    )
    ax1.add_feature(
        cfeature.LAND.with_scale("10m"), facecolor="lightgray",
        edgecolor="black", linewidth=0.5,
    )
    ax1.set_extent(EXTENT, crs=PC)
    ax1.set_title("(a) Lima 5 km", fontsize=12)
    add_gridlines(ax1)
    ax1.legend(loc="lower left", fontsize=8, title="Spectra output sites", title_fontsize=8)

    # Right panel: Chancay 400 m nest (land is where the model depth is masked)
    ax2.set_facecolor("lightgray")
    depth.plot(
        ax=ax2, transform=PC, cmap="Blues", vmin=0,
        cbar_kwargs={"label": "Model depth (m)", **cbar_kwargs},
    )
    cs = ax2.contour(
        depth.longitude, depth.latitude, depth.values, levels=CHANCAY_CONTOURS,
        colors="0.3", linewidths=0.5, transform=PC,
    )
    ax2.clabel(cs, inline=True, fontsize=8, fmt="%d m")
    ax2.scatter(
        chan_lon, chan_lat, s=40, c="blue", marker=".", linewidths=0,
        transform=PC, zorder=5, label=f"Spectra output sites (n={chan_lon.size})",
    )
    ax2.scatter(
        *ADCP, s=220, c="red", marker="*", edgecolor="black", linewidth=0.6,
        transform=PC, zorder=6, label="ADCP",
    )
    ax2.set_extent(CHANCAY, crs=PC)
    for spine in ax2.spines.values():
        spine.set_edgecolor("blue")
        spine.set_linewidth(2)
    ax2.set_title("(b) Chancay 400 m", fontsize=12)
    add_gridlines(ax2)
    ax2.legend(loc="lower left", fontsize=8)

    fig.savefig(OUTPUT, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()

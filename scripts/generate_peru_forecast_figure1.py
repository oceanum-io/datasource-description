#!/usr/bin/env python3
"""
Generate Figure 1 for the Lima / Chancay Wave Forecast document.

Mean significant wave height from the Lima ERA5 hindcast gridstats (same grid
as the forecast parent domain) with depth contours, the Chancay 400 m nest box
and the spectra output sites of both forecast domains.

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
EXTENT = [-79.0, -76.0, -13.0, -10.0]
CHANCAY = [-77.8, -77.1, -11.9, -11.2]
CONTOURS = [50, 100, 200, 500, 1000, 2000]
# datasource id, legend label, colour, marker size
SITES = [
    ("oceanum_wave_gfs_lima5km_spec", "Lima 5 km", "black", 20),
    ("oceanum_wave_gfs_chancay400m_spec", "Chancay 400 m", "blue", 12),
]


def main() -> None:
    conn = Connector()
    dset = conn.query(datasource=GRIDSTATS, variables=["hs_mean", "depth_mean"])

    fig, ax = plt.subplots(figsize=(8, 10), subplot_kw={"projection": ccrs.PlateCarree()})
    dset.hs_mean.plot(
        ax=ax, transform=ccrs.PlateCarree(), cmap="turbo",
        cbar_kwargs={
            "label": "Mean Significant Wave Height (m)",
            "orientation": "horizontal", "pad": 0.05, "shrink": 0.8,
        },
    )

    lon2d, lat2d = np.meshgrid(dset.longitude.values, dset.latitude.values)
    cs = ax.contour(
        lon2d, lat2d, dset.depth_mean.values, levels=CONTOURS,
        colors="0.4", linewidths=0.5, transform=ccrs.PlateCarree(),
    )
    ax.clabel(cs, inline=True, fontsize=8, fmt="%d m")

    for datasource, label, color, size in SITES:
        sites = conn.query(datasource=datasource, variables=["lon", "lat"])
        lon, lat = sites.lon.values.ravel(), sites.lat.values.ravel()
        print(f"{datasource}: {lon.size} sites")
        ax.scatter(
            lon, lat, s=size, c=color, marker=".", linewidths=0,
            transform=ccrs.PlateCarree(), zorder=5, label=f"{label} (n={lon.size})",
        )

    x0, x1, y0, y1 = CHANCAY
    ax.plot(
        [x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], color="blue", linewidth=2,
        transform=ccrs.PlateCarree(), zorder=4,
    )

    ax.add_feature(
        cfeature.LAND.with_scale("10m"), facecolor="lightgray",
        edgecolor="black", linewidth=0.5,
    )
    ax.set_extent(EXTENT, crs=ccrs.PlateCarree())
    ax.set_title("")
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False
    ax.legend(loc="lower left", fontsize=8, title="Spectra output sites", title_fontsize=8)

    fig.savefig(OUTPUT, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()

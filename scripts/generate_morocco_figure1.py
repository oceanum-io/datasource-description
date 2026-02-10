#!/usr/bin/env python3
"""
Generate Figure 1 for the Morocco Wave Hindcast document.
Shows mean significant wave height with depth contours and spectra site locations.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from oceanum.datamesh import Connector

# Initialize Datamesh connector
conn = Connector()

# Query gridstats for mean wave parameters
print("Querying gridstats data...")
dset = conn.query(
    datasource="oceanum_wave_morocco_5km_era5_gridstats",
    variables=["hs_mean", "depth_mean"]
)

# Query sites for spectra locations
print("Querying spectra sites...")
sites = conn.query(
    datasource="oceanum_wave_morocco_5km_era5_spec",
    variables=["lon", "lat"]
)

# Set up the figure with Cartopy projection
fig, ax = plt.subplots(
    figsize=(10, 12),
    subplot_kw={"projection": ccrs.PlateCarree()}
)

# Plot mean significant wave height
print("Plotting mean Hs...")
hs_plot = dset.hs_mean.plot(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap="turbo",
    cbar_kwargs={
        "label": "Mean Significant Wave Height (m)",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.8
    }
)

# Add depth contours
print("Adding depth contours...")
depth = dset.depth_mean.values
lon = dset.longitude.values if "longitude" in dset.coords else dset.lon.values
lat = dset.latitude.values if "latitude" in dset.coords else dset.lat.values

# Create meshgrid for contour plotting
lon2d, lat2d = np.meshgrid(lon, lat)

# Plot depth contours at 50m, 200m, 1000m, 3000m
contour_levels = [50, 200, 1000, 3000]
cs = ax.contour(
    lon2d, lat2d, depth,
    levels=contour_levels,
    colors="0.4",
    linewidths=0.5,
    transform=ccrs.PlateCarree()
)
ax.clabel(cs, inline=True, fontsize=8, fmt="%d m")

# Plot spectra site locations
print("Plotting spectra sites...")
site_lons = sites.lon.values
site_lats = sites.lat.values
ax.scatter(
    site_lons, site_lats,
    s=3,
    c="black",
    marker=".",
    transform=ccrs.PlateCarree(),
    label=f"Spectra sites (n={len(site_lons)})",
    zorder=5
)

# Add land features
ax.add_feature(cfeature.LAND, facecolor="lightgray", edgecolor="black", linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

# Set extent to match domain
ax.set_extent([-19, -6, 22, 38], crs=ccrs.PlateCarree())

# Add gridlines
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
gl.top_labels = False
gl.right_labels = False

# Add legend (no title)
ax.legend(loc="lower left", fontsize=9)

# Save figure
output_path = "/source/datasource-description/figures/morocco_figure1_hs_mean.png"
print(f"Saving figure to {output_path}...")
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

print("Done!")

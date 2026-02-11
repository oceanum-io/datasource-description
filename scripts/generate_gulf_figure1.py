#!/usr/bin/env python3
"""
Generate Figure 1 for the Arabian Gulf Wave Hindcast document.
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
print("Querying Gulf gridstats data...")
dset = conn.query(
    datasource="oceanum_wave_gulf_5km_era5_gridstats",
    variables=["hs_mean", "depth_mean"]
)

# Query sites for spectra locations
print("Querying Gulf spectra sites...")
sites = conn.query(datasource="oceanum_wave_gulf_5km_era5_spec", variables=["lon", "lat"])

# Get domain geometry
print("Getting domain geometry...")
ds = conn.get_datasource("oceanum_wave_gulf_5km_era5_grid")

# Set up the figure with Cartopy projection
fig, ax = plt.subplots(
    figsize=(14, 8),
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
        "shrink": 0.6
    }
)

# Add depth contours
print("Adding depth contours...")
depth = dset.depth_mean.values
lon = dset.longitude.values if "longitude" in dset.coords else dset.lon.values
lat = dset.latitude.values if "latitude" in dset.coords else dset.lat.values

# Create meshgrid for contour plotting
lon2d, lat2d = np.meshgrid(lon, lat)

# Plot depth contours
contour_levels = [20, 50, 100]
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
ax.scatter(
    sites.lon.values, sites.lat.values,
    s=3, c="black", marker=".",
    transform=ccrs.PlateCarree(),
    label=f"Spectra sites (n={len(sites.lon)})",
    zorder=5
)

# Plot domain bounding box
print("Plotting domain bbox...")
x, y = ds.geom.exterior.xy
ax.plot(x, y, color="black", linewidth=2, transform=ccrs.PlateCarree())

# Add land features
ax.add_feature(cfeature.LAND, facecolor="lightgray", edgecolor="black", linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

# Set extent to match Gulf domain
ax.set_extent([47.5, 60.5, 22.5, 31.0], crs=ccrs.PlateCarree())

# Add gridlines
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
gl.top_labels = False
gl.right_labels = False

# Add legend
ax.legend(loc="lower left", fontsize=8)

# Save figure
output_path = "/source/datasource-description/figures/gulf_figure1_hs_mean.png"
print(f"Saving figure to {output_path}...")
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

print("Done!")

#!/usr/bin/env python3
"""
Generate Figure 1 for the King Island Wave Hindcast document.
Shows mean significant wave height (from parent Bass Strait gridstats) with depth contours,
spectra site locations for King Island and Grassy, and the Grassy nest bounding box.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from oceanum.datamesh import Connector

# Initialize Datamesh connector
conn = Connector()

# Query gridstats for mean wave parameters (King Island native resolution)
print("Querying King Island gridstats data...")
dset = conn.query(
    datasource="oceanum_wave_king_1km_era5_gridstats",
    variables=["hs_mean", "depth_mean"]
)

# Query sites for spectra locations
print("Querying King Island spectra sites...")
sites_king = conn.query(datasource="oceanum_wave_king_1km_era5_spec", variables=["lon", "lat"])

print("Querying Grassy spectra sites...")
sites_grassy = conn.query(datasource="oceanum_wave_grassy_100m_era5_spec", variables=["lon", "lat"])

# Get nest geometries
print("Getting nest geometries...")
ds_king = conn.get_datasource("oceanum_wave_king_1km_era5_grid")
ds_grassy = conn.get_datasource("oceanum_wave_grassy_100m_era5_grid")

# Set up the figure with Cartopy projection
fig, ax = plt.subplots(
    figsize=(8, 10),
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

# Plot depth contours
contour_levels = [20, 50, 100, 200]
cs = ax.contour(
    lon2d, lat2d, depth,
    levels=contour_levels,
    colors="0.4",
    linewidths=0.5,
    transform=ccrs.PlateCarree()
)
ax.clabel(cs, inline=True, fontsize=8, fmt="%d m")

# Plot King Island spectra site locations
print("Plotting spectra sites...")
ax.scatter(
    sites_king.lon.values, sites_king.lat.values,
    s=5, c="black", marker=".",
    transform=ccrs.PlateCarree(),
    label=f"King Island 1km (n={len(sites_king.lon)})",
    zorder=5
)

# Plot Grassy spectra site locations
ax.scatter(
    sites_grassy.lon.values, sites_grassy.lat.values,
    s=5, c="blue", marker=".",
    transform=ccrs.PlateCarree(),
    label=f"Grassy 100m (n={len(sites_grassy.lon)})",
    zorder=5
)

# Plot nest bounding boxes
print("Plotting nest bboxes...")
# King Island bbox
king_x, king_y = ds_king.geom.exterior.xy
ax.plot(king_x, king_y, color="black", linewidth=2, transform=ccrs.PlateCarree(), label="King Island 1km domain")

# Grassy bbox
grassy_x, grassy_y = ds_grassy.geom.exterior.xy
ax.plot(grassy_x, grassy_y, color="blue", linewidth=2, transform=ccrs.PlateCarree(), label="Grassy 100m nest")

# Add land features
ax.add_feature(cfeature.LAND, facecolor="lightgray", edgecolor="black", linewidth=0.5)

# Set extent to match King Island domain with some buffer
ax.set_extent([143.4, 144.6, -40.6, -39.2], crs=ccrs.PlateCarree())

# Add gridlines
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
gl.top_labels = False
gl.right_labels = False

# Add legend
ax.legend(loc="lower left", fontsize=8)

# Save figure
output_path = "/source/datasource-description/figures/kingisland_figure1_hs_mean.png"
print(f"Saving figure to {output_path}...")
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

print("Done!")

#!/usr/bin/env python3
"""
Generate Figure 1 for the Peru Wave Hindcast document.
Shows mean significant wave height with depth contours,
spectra site locations for Chancay, and the Chancay nest bounding box.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from oceanum.datamesh import Connector

# Initialize Datamesh connector
conn = Connector()

# Query gridstats for mean wave parameters (Lima parent domain)
print("Querying Lima gridstats data...")
dset = conn.query(
    datasource="oceanum_wave_lima_era5_gridstats",
    variables=["hs_mean", "depth_mean"]
)

# Query sites for spectra locations (only Chancay has spectra)
print("Querying Chancay spectra sites...")
sites_chancay = conn.query(datasource="oceanum_wave_chancay_era5_spec", variables=["lon", "lat"])

# Get nest geometries
print("Getting nest geometries...")
ds_lima = conn.get_datasource("oceanum_wave_lima_era5_grid")
ds_chancay = conn.get_datasource("oceanum_wave_chancay_era5_grid")

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
contour_levels = [50, 100, 200, 500, 1000, 2000]
cs = ax.contour(
    lon2d, lat2d, depth,
    levels=contour_levels,
    colors="0.4",
    linewidths=0.5,
    transform=ccrs.PlateCarree()
)
ax.clabel(cs, inline=True, fontsize=8, fmt="%d m")

# Plot Chancay spectra site locations
print("Plotting spectra sites...")
ax.scatter(
    sites_chancay.lon.values, sites_chancay.lat.values,
    s=8, c="blue", marker=".",
    transform=ccrs.PlateCarree(),
    label=f"Chancay 400m (n={len(sites_chancay.lon)})",
    zorder=5
)

# Plot nest bounding boxes
print("Plotting nest bboxes...")
# Lima parent bbox (black)
lima_x, lima_y = ds_lima.geom.exterior.xy
ax.plot(lima_x, lima_y, color="black", linewidth=2, transform=ccrs.PlateCarree(), label="Lima 5km domain")

# Chancay child bbox (blue)
chancay_x, chancay_y = ds_chancay.geom.exterior.xy
ax.plot(chancay_x, chancay_y, color="blue", linewidth=2, transform=ccrs.PlateCarree(), label="Chancay 400m nest")

# Add land features
ax.add_feature(cfeature.LAND, facecolor="lightgray", edgecolor="black", linewidth=0.5)

# Set extent to match Lima domain
ax.set_extent([-79.0, -76.0, -13.0, -10.0], crs=ccrs.PlateCarree())

# Add gridlines
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
gl.top_labels = False
gl.right_labels = False

# Add legend
ax.legend(loc="lower left", fontsize=8)

# Save figure
output_path = "/source/datasource-description/figures/peru_figure1_hs_mean.png"
print(f"Saving figure to {output_path}...")
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

print("Done!")

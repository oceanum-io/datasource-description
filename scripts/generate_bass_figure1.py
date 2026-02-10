#!/usr/bin/env python3
"""
Generate Figure 1 for the Bass Strait Wave Hindcast document.
Shows mean significant wave height with depth contours, spectra site locations,
and child nest bounding boxes (Eastern Bass Strait, Portland, Grassy).
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from oceanum.datamesh import Connector

# Initialize Datamesh connector
conn = Connector()

# Query gridstats for mean wave parameters (Bass Strait parent)
print("Querying Bass Strait gridstats data...")
dset = conn.query(
    datasource="oceanum_wave_bass_5km_era5_gridstats",
    variables=["hs_mean", "depth_mean"]
)

# Query sites for spectra locations
print("Querying Bass Strait spectra sites...")
sites_bass = conn.query(datasource="oceanum_wave_bass_5km_era5_spec", variables=["lon", "lat"])

print("Querying Eastern Bass Strait spectra sites...")
sites_ebass = conn.query(datasource="oceanum_wave_ebass_1km_era5_spec", variables=["lon", "lat"])

print("Querying Portland spectra sites...")
sites_ptlan = conn.query(datasource="oceanum_wave_ptlan_1km_era5_spec", variables=["lon", "lat"])

print("Querying Grassy spectra sites...")
sites_grassy = conn.query(datasource="oceanum_wave_grassy_100m_era5_spec", variables=["lon", "lat"])

print("Querying King Island spectra sites...")
sites_king = conn.query(datasource="oceanum_wave_king_1km_era5_spec", variables=["lon", "lat"])

# Get nest geometries
print("Getting nest geometries...")
ds_ebass = conn.get_datasource("oceanum_wave_ebass_1km_era5_grid")
ds_ptlan = conn.get_datasource("oceanum_wave_ptlan_1km_era5_grid")
ds_king = conn.get_datasource("oceanum_wave_king_1km_era5_grid")
ds_grassy = conn.get_datasource("oceanum_wave_grassy_100m_era5_grid")

# Set up the figure with Cartopy projection
fig, ax = plt.subplots(
    figsize=(12, 8),
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
contour_levels = [50, 100, 200, 500]
cs = ax.contour(
    lon2d, lat2d, depth,
    levels=contour_levels,
    colors="0.4",
    linewidths=0.5,
    transform=ccrs.PlateCarree()
)
ax.clabel(cs, inline=True, fontsize=8, fmt="%d m")

# Plot Bass Strait spectra site locations
print("Plotting spectra sites...")
ax.scatter(
    sites_bass.lon.values, sites_bass.lat.values,
    s=3, c="black", marker=".",
    transform=ccrs.PlateCarree(),
    label=f"Bass Strait 5km (n={len(sites_bass.lon)})",
    zorder=5
)

# Plot Eastern Bass Strait spectra site locations
ax.scatter(
    sites_ebass.lon.values, sites_ebass.lat.values,
    s=2, c="blue", marker=".",
    transform=ccrs.PlateCarree(),
    label=f"Eastern Bass Strait 1km (n={len(sites_ebass.lon)})",
    zorder=5
)

# Plot Portland spectra site locations
ax.scatter(
    sites_ptlan.lon.values, sites_ptlan.lat.values,
    s=2, c="green", marker=".",
    transform=ccrs.PlateCarree(),
    label=f"Portland 1km (n={len(sites_ptlan.lon)})",
    zorder=5
)

# Plot King Island spectra site locations
ax.scatter(
    sites_king.lon.values, sites_king.lat.values,
    s=2, c="orange", marker=".",
    transform=ccrs.PlateCarree(),
    label=f"King Island 1km (n={len(sites_king.lon)})",
    zorder=5
)

# Plot Grassy spectra site locations
ax.scatter(
    sites_grassy.lon.values, sites_grassy.lat.values,
    s=2, c="magenta", marker=".",
    transform=ccrs.PlateCarree(),
    label=f"Grassy 100m (n={len(sites_grassy.lon)})",
    zorder=5
)

# Plot nest bounding boxes
print("Plotting nest bboxes...")
for geom, label, color in [
    (ds_ebass.geom, "Eastern Bass Strait 1km", "blue"),
    (ds_ptlan.geom, "Portland 1km", "green"),
    (ds_king.geom, "King Island 1km", "orange"),
    (ds_grassy.geom, "Grassy 100m", "magenta"),
]:
    x, y = geom.exterior.xy
    ax.plot(x, y, color=color, linewidth=1.5, transform=ccrs.PlateCarree())

# Add land features
ax.add_feature(cfeature.LAND, facecolor="lightgray", edgecolor="black", linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

# Set extent to match Bass Strait domain
ax.set_extent([140.0, 151.0, -42.0, -37.0], crs=ccrs.PlateCarree())

# Add gridlines
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
gl.top_labels = False
gl.right_labels = False

# Add legend
ax.legend(loc="lower left", fontsize=8)

# Save figure
output_path = "/source/datasource-description/figures/bass_figure1_hs_mean.png"
print(f"Saving figure to {output_path}...")
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

print("Done!")

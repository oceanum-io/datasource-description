#!/usr/bin/env python3
"""
Generate Figure 1 for the New Zealand Wave Hindcast document.
Shows mean significant wave height with depth contours and spectra site locations.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import box
import numpy as np
import geopandas
from oceanum.datamesh import Connector

# Initialize Datamesh connector
conn = Connector()

# Query gridstats for mean wave parameters
print("Querying NZ gridstats data...")
dset = conn.query(
    datasource="oceanum_wave_nz_era5_v1_gridstats",
    variables=["hs_mean", "depth_mean"]
)

# Map coordinates
lon = dset.longitude.values
lat = dset.latitude.values
lon2d, lat2d = np.meshgrid(lon, lat)

x0, x1 = lon[[0, -1]]
y0, y1 = lat[[0, -1]]

central_longitude = float((x0 + x1) / 2)
central_latitude = float((y0 + y1) / 2)

# Query sites for spectra locations
print("Querying NZ spectra sites...")
sites = conn.query(datasource="oceanum_wave_nz_era5_v1_spec", variables=["lon", "lat"])

# Get domain geometry
print("Getting domain geometry...")
ds = conn.get_datasource("oceanum_wave_nz_era5_v1_grid")

# Set up the figure with Cartopy projection (TransverseMercator centered on NZ)
projection = ccrs.PlateCarree()
transform = ccrs.PlateCarree()

fig, ax = plt.subplots(
    figsize=(8, 10),
    subplot_kw={"projection": projection}
)

# Plot mean significant wave height
print("Plotting mean Hs...")
hs_plot = dset.hs_mean.plot(
    ax=ax,
    transform=transform,
    cmap="turbo",
    cbar_kwargs={
        "label": "Mean Significant Wave Height (m)",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.7
    }
)

# Add depth contours
print("Adding depth contours...")
depth = dset.depth_mean.values

# Plot depth contours
contour_levels = [100, 500, 1000, 2000]
cs = ax.contour(
    lon2d, lat2d, depth,
    levels=contour_levels,
    colors="0.4",
    linewidths=0.5,
    transform=transform
)
ax.clabel(cs, inline=True, fontsize=7, fmt="%d m")

# Plot spectra site locations
print("Plotting spectra sites...")
ax.scatter(
    sites.lon.values, sites.lat.values,
    s=0.5, c="black", marker=".",
    transform=transform,
    label=f"Spectra sites (n={len(sites.lon)})",
    zorder=5
)

# Plot domain bounding box
print("Plotting domain bbox...")
gdf = geopandas.GeoSeries(box(x0, y0, x1, y1), crs="EPSG:4326")
gdf.plot(ax=ax, transform=transform, facecolor="none", edgecolor="black", linewidth=2)

# Add land features
ax.add_feature(cfeature.LAND, facecolor="lightgray", edgecolor="black", linewidth=0.5)

# Set extent to match NZ domain
ax.set_extent([x0, x1, y0, y1], crs=ccrs.PlateCarree())

# Add gridlines
from matplotlib.ticker import FixedLocator
gl = ax.gridlines(draw_labels=["left", "bottom"], linewidth=0.5, color="gray", alpha=0.5, linestyle="--")

# Add legend
ax.legend(loc="lower left", fontsize=8)

# Save figure
output_path = "/source/datasource-description/figures/nz_figure1_hs_mean.png"
print(f"Saving figure to {output_path}...")
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

print("Done!")

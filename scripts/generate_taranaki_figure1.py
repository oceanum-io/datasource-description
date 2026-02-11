#!/usr/bin/env python3
"""
Generate Figure 1 for Taranaki wave hindcast document.
This script computes mean Hs from the grid data since no gridstats datasource exists.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from oceanum.datamesh import Connector
import geopandas as gpd
from shapely.geometry import box

# Configuration
OUTPUT_PATH = "/source/datasource-description/figures/taranaki_figure1_hs_mean.png"
GRID_ID = "oceanum_wave_trki_era5_v1_grid"
SPEC_ID = "oceanum_wave_trki_era5_v1_spec"
DEPTH_CONTOURS = [50, 100, 200, 500, 1000]
FIGSIZE = (8, 8)

def main():
    conn = Connector()
    
    # Query spectra sites
    print("Querying Taranaki spectra sites...")
    sites = conn.query(datasource=SPEC_ID, variables=["lon", "lat"])
    
    # Get domain geometry
    print("Getting domain geometry...")
    ds = conn.get_datasource(GRID_ID)
    
    # Query depth data
    print("Querying depth data...")
    depth_data = conn.query(datasource=GRID_ID, variables=["depth"])
    
    # Compute mean Hs - query in yearly chunks to avoid memory issues
    print("Computing mean Hs (this may take a while)...")
    years = range(2015, 2021)  # Use 5 years for statistics
    hs_sum = None
    count = 0
    
    for year in years:
        print(f"  Processing {year}...")
        try:
            data = conn.query(
                datasource=GRID_ID,
                variables=["hs"],
                time=slice(f"{year}-01-01", f"{year}-12-31")
            )
            if hs_sum is None:
                hs_sum = data.hs.mean(dim="time").values
                count = 1
            else:
                hs_sum = hs_sum + data.hs.mean(dim="time").values
                count += 1
        except Exception as e:
            print(f"  Error processing {year}: {e}")
    
    hs_mean = hs_sum / count
    lon = depth_data.longitude.values
    lat = depth_data.latitude.values
    depth = depth_data.depth.values
    
    # Get domain extent
    x0, x1 = lon.min(), lon.max()
    y0, y1 = lat.min(), lat.max()
    
    # Create figure
    print("Creating figure...")
    projection = ccrs.PlateCarree()
    transform = ccrs.PlateCarree()
    
    fig, ax = plt.subplots(
        figsize=FIGSIZE,
        subplot_kw={"projection": projection}
    )
    
    # Plot mean Hs
    print("Plotting mean Hs...")
    mesh = ax.pcolormesh(
        lon, lat, hs_mean,
        transform=transform,
        cmap="turbo",
        vmin=0, vmax=2.5,
        shading="auto"
    )
    
    # Add depth contours
    print("Adding depth contours...")
    ax.contour(
        lon, lat, depth,
        levels=DEPTH_CONTOURS,
        colors="gray",
        linewidths=0.5,
        linestyles="solid",
        transform=transform
    )
    ax.clabel(
        ax.contour(
            lon, lat, depth,
            levels=DEPTH_CONTOURS,
            colors="gray",
            linewidths=0.5,
            transform=transform
        ),
        inline=True,
        fontsize=8,
        fmt="%d m"
    )
    
    # Plot spectra sites
    print("Plotting spectra sites...")
    ax.scatter(
        sites.lon.values, sites.lat.values,
        s=1.0, c="black", marker=".",
        transform=transform,
        label=f"Taranaki (n={len(sites.lon)})",
        zorder=5
    )
    
    # Plot domain bbox
    print("Plotting domain bbox...")
    gpd.GeoSeries(box(x0, y0, x1, y1), crs="EPSG:4326").plot(
        ax=ax,
        facecolor="none",
        edgecolor="black",
        linewidth=1.5,
        transform=transform,
        zorder=10
    )
    
    # Add features
    ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=1)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=2)
    
    # Set extent with small buffer
    buffer = 0.1
    ax.set_extent([x0 - buffer, x1 + buffer, y0 - buffer, y1 + buffer], crs=transform)
    
    # Add gridlines
    gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    
    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation="horizontal", shrink=0.8, pad=0.08)
    cbar.set_label("Mean Significant Wave Height (m)")
    
    # Add legend
    ax.legend(loc="lower left", fontsize=8)
    
    # Save figure
    print(f"Saving figure to {OUTPUT_PATH}...")
    plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    plt.close()
    print("Done!")

if __name__ == "__main__":
    main()

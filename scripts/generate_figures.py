#!/usr/bin/env python3
"""
Generalized figure generation for wave hindcast documentation.
Produces Figure 1 plots showing mean significant wave height with depth contours,
spectra site locations, and domain bounding boxes.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import box
import numpy as np
import geopandas
from oceanum.datamesh import Connector
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class NestConfig:
    """Configuration for a nested domain."""
    name: str
    spec_id: str
    grid_id: str
    color: str = "blue"
    site_size: float = 3.0


@dataclass
class FigureConfig:
    """Configuration for generating a hindcast figure."""
    output_name: str
    gridstats_id: str
    grid_id: str
    domain_name: str
    spec_id: Optional[str] = None  # Optional - some domains only have spectra in nests
    depth_contours: List[int] = field(default_factory=lambda: [100, 500, 1000, 2000])
    figsize: tuple = (10, 10)
    cbar_shrink: float = 0.7
    extent: Optional[List[float]] = None  # [x0, x1, y0, y1] or None for auto
    show_borders: bool = False
    site_size: float = 1.0
    site_color: str = "black"
    nests: List[NestConfig] = field(default_factory=list)


def generate_figure(config: FigureConfig):
    """
    Generate a Figure 1 plot for a wave hindcast document.
    
    Parameters
    ----------
    config : FigureConfig
        Configuration object specifying domains, output path, and plot options.
    """
    conn = Connector()
    
    # Query gridstats for mean wave parameters
    print(f"Querying {config.domain_name} gridstats data...")
    dset = conn.query(
        datasource=config.gridstats_id,
        variables=["hs_mean", "depth_mean"]
    )
    
    # Map coordinates
    lon = dset.longitude.values if "longitude" in dset.coords else dset.lon.values
    lat = dset.latitude.values if "latitude" in dset.coords else dset.lat.values
    lon2d, lat2d = np.meshgrid(lon, lat)
    
    x0, x1 = float(lon[0]), float(lon[-1])
    y0, y1 = float(lat[0]), float(lat[-1])
    
    # Query sites for spectra locations (if available for main domain)
    sites = None
    if config.spec_id:
        print(f"Querying {config.domain_name} spectra sites...")
        sites = conn.query(datasource=config.spec_id, variables=["lon", "lat"])
    
    # Get domain geometry
    print("Getting domain geometry...")
    ds = conn.get_datasource(config.grid_id)
    
    # Set up projection
    projection = ccrs.PlateCarree()
    transform = ccrs.PlateCarree()
    
    # Set up the figure
    fig, ax = plt.subplots(
        figsize=config.figsize,
        subplot_kw={"projection": projection}
    )
    
    # Plot mean significant wave height
    print("Plotting mean Hs...")
    dset.hs_mean.plot(
        ax=ax,
        transform=transform,
        cmap="turbo",
        cbar_kwargs={
            "label": "Mean Significant Wave Height (m)",
            "orientation": "horizontal",
            "pad": 0.05,
            "shrink": config.cbar_shrink
        }
    )
    
    # Add depth contours
    print("Adding depth contours...")
    depth = dset.depth_mean.values
    cs = ax.contour(
        lon2d, lat2d, depth,
        levels=config.depth_contours,
        colors="0.4",
        linewidths=0.5,
        transform=transform
    )
    ax.clabel(cs, inline=True, fontsize=7, fmt="%d m")
    
    # Plot spectra site locations for main domain (if available)
    if sites is not None:
        print("Plotting spectra sites...")
        ax.scatter(
            sites.lon.values, sites.lat.values,
            s=config.site_size, c=config.site_color, marker=".",
            transform=transform,
            label=f"{config.domain_name} (n={len(sites.lon)})",
            zorder=5
        )
    
    # Plot main domain bounding box
    print("Plotting domain bbox...")
    gdf = geopandas.GeoSeries(box(x0, y0, x1, y1), crs="EPSG:4326")
    gdf.plot(ax=ax, transform=transform, facecolor="none", edgecolor="black", linewidth=2)
    
    # Plot nested domains if any
    for nest in config.nests:
        print(f"Querying {nest.name} spectra sites...")
        nest_sites = conn.query(datasource=nest.spec_id, variables=["lon", "lat"])
        
        ax.scatter(
            nest_sites.lon.values, nest_sites.lat.values,
            s=nest.site_size, c=nest.color, marker=".",
            transform=transform,
            label=f"{nest.name} (n={len(nest_sites.lon)})",
            zorder=5
        )
        
        print(f"Plotting {nest.name} bbox...")
        nest_ds = conn.get_datasource(nest.grid_id)
        nest_x, nest_y = nest_ds.geom.exterior.xy
        ax.plot(nest_x, nest_y, color=nest.color, linewidth=2, transform=transform)
    
    # Add land features
    ax.add_feature(cfeature.LAND, facecolor="lightgray", edgecolor="black", linewidth=0.5)
    if config.show_borders:
        ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
    
    # Set extent
    if config.extent:
        ax.set_extent(config.extent, crs=ccrs.PlateCarree())
    else:
        ax.set_extent([x0, x1, y0, y1], crs=ccrs.PlateCarree())
    
    # Add gridlines
    gl = ax.gridlines(draw_labels=["left", "bottom"], linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
    
    # Add legend
    ax.legend(loc="lower left", fontsize=8)
    
    # Save figure
    output_path = f"/source/datasource-description/figures/{config.output_name}"
    print(f"Saving figure to {output_path}...")
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    
    print("Done!")


# ============================================================================
# Figure configurations for each hindcast document
# ============================================================================

NZ_CONFIG = FigureConfig(
    output_name="nz_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_nz_era5_v1_gridstats",
    spec_id="oceanum_wave_nz_era5_v1_spec",
    grid_id="oceanum_wave_nz_era5_v1_grid",
    domain_name="New Zealand",
    depth_contours=[100, 500, 1000, 2000],
    figsize=(8, 10),
    cbar_shrink=0.7,
    site_size=0.5,
)

MEDITERRANEAN_CONFIG = FigureConfig(
    output_name="mediterranean_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_mediterranean_era5_v1_gridstats",
    spec_id="oceanum_wave_mediterranean_era5_v1_spec",
    grid_id="oceanum_wave_mediterranean_era5_v1_grid",
    domain_name="Mediterranean",
    depth_contours=[100, 500, 1000, 2000],
    figsize=(14, 6),
    cbar_shrink=0.5,
    show_borders=True,
    site_size=1.0,
)

GULF_CONFIG = FigureConfig(
    output_name="gulf_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_gulf_5km_era5_gridstats",
    spec_id="oceanum_wave_gulf_5km_era5_spec",
    grid_id="oceanum_wave_gulf_5km_era5_grid",
    domain_name="Arabian Gulf",
    depth_contours=[20, 50, 100],
    figsize=(14, 8),
    cbar_shrink=0.6,
    show_borders=True,
    site_size=3.0,
)

PERU_CONFIG = FigureConfig(
    output_name="peru_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_lima_era5_gridstats",
    grid_id="oceanum_wave_lima_era5_grid",
    domain_name="Lima 5km",
    depth_contours=[50, 100, 200, 500, 1000, 2000],
    figsize=(8, 10),
    cbar_shrink=0.8,
    site_size=3.0,
    extent=[-79.0, -76.0, -13.0, -10.0],
    nests=[
        NestConfig(
            name="Chancay 400m",
            spec_id="oceanum_wave_chancay_era5_spec",
            grid_id="oceanum_wave_chancay_era5_grid",
            color="blue",
            site_size=8.0,
        )
    ],
)

KING_ISLAND_CONFIG = FigureConfig(
    output_name="kingisland_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_king_1km_era5_gridstats",
    spec_id="oceanum_wave_king_1km_era5_spec",
    grid_id="oceanum_wave_king_1km_era5_grid",
    domain_name="King Island 1km",
    depth_contours=[20, 50, 100, 200],
    figsize=(8, 10),
    cbar_shrink=0.8,
    site_size=5.0,
    extent=[143.6, 144.4, -40.4, -39.4],
    nests=[
        NestConfig(
            name="Grassy 100m",
            spec_id="oceanum_wave_grassy_100m_era5_spec",
            grid_id="oceanum_wave_grassy_100m_era5_grid",
            color="blue",
            site_size=5.0,
        )
    ],
)

WEST_AFRICA_CONFIG = FigureConfig(
    output_name="wafr_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_wafr_era5_gridstats",
    spec_id="oceanum_wave_wafr_era5_spec",
    grid_id="oceanum_wave_wafr_era5_grid",
    domain_name="West Africa",
    depth_contours=[50, 200, 1000, 3000],
    figsize=(10, 12),
    cbar_shrink=0.8,
    show_borders=True,
    site_size=3.0,
    extent=[2.5, 10.0, -2.0, 6.5],
    nests=[
        NestConfig(
            name="Nigeria 1km",
            spec_id="oceanum_wave_nga_era5_spec",
            grid_id="oceanum_wave_nga_era5_grid",
            color="blue",
            site_size=3.0,
        )
    ],
)

MOROCCO_CONFIG = FigureConfig(
    output_name="morocco_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_morocco_era5_gridstats",
    spec_id="oceanum_wave_morocco_era5_spec",
    grid_id="oceanum_wave_morocco_era5_grid",
    domain_name="Morocco",
    depth_contours=[50, 100, 500, 1000, 2000],
    figsize=(10, 10),
    cbar_shrink=0.7,
    site_size=2.0,
)

MALAY_CONFIG = FigureConfig(
    output_name="malay_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_malay_era5_gridstats",
    spec_id="oceanum_wave_malay_era5_spec",
    grid_id="oceanum_wave_malay_era5_grid",
    domain_name="Malay Peninsula",
    depth_contours=[20, 50, 100, 200],
    figsize=(10, 12),
    cbar_shrink=0.7,
    site_size=2.0,
)

BASS_STRAIT_CONFIG = FigureConfig(
    output_name="bass_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_bass_era5_gridstats",
    spec_id="oceanum_wave_bass_era5_spec",
    grid_id="oceanum_wave_bass_era5_grid",
    domain_name="Bass Strait",
    depth_contours=[50, 100, 200, 500],
    figsize=(12, 8),
    cbar_shrink=0.7,
    site_size=2.0,
)

RED_SEA_CONFIG = FigureConfig(
    output_name="redsea_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_redsea_era5_gridstats",
    spec_id="oceanum_wave_redsea_era5_spec",
    grid_id="oceanum_wave_redsea_era5_grid",
    domain_name="Red Sea",
    depth_contours=[50, 200, 500, 1000, 2000],
    figsize=(8, 12),
    cbar_shrink=0.7,
    show_borders=True,
    site_size=3.0,
)

TARANAKI_CONFIG = FigureConfig(
    output_name="taranaki_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_nz_era5_v1_gridstats",  # Use NZ gridstats
    spec_id="oceanum_wave_trki_era5_v1_spec",
    grid_id="oceanum_wave_trki_era5_v1_grid",
    domain_name="Taranaki",
    depth_contours=[50, 100, 200, 500, 1000],
    figsize=(8, 8),
    cbar_shrink=0.7,
    extent=[173.0, 175.2, -40.0, -37.8],  # Taranaki domain extent
    site_size=1.0,
)

US_EAST_CONFIG = FigureConfig(
    output_name="useast_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_useast_era5_gridstats",
    spec_id="oceanum_wave_useast_era5_spec",
    grid_id="oceanum_wave_useast_era5_grid",
    domain_name="US East Coast",
    depth_contours=[50, 100, 200, 500, 1000, 2000, 4000],
    figsize=(8, 12),
    cbar_shrink=0.7,
    show_borders=True,
    site_size=2.0,
)

WESTERN_EUROPE_CONFIG = FigureConfig(
    output_name="weuro_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_weuro_era5_v1_gridstats",
    spec_id="oceanum_wave_weuro_era5_v1_spec",
    grid_id="oceanum_wave_weuro_era5_v1_grid",
    domain_name="Western Europe",
    depth_contours=[50, 100, 200, 500, 1000, 2000],
    figsize=(12, 8),
    cbar_shrink=0.7,
    show_borders=True,
    site_size=1.0,
    nests=[
        NestConfig(
            name="Dutch Coast",
            spec_id="oceanum_wave_dutch_era5_v1_spec",
            grid_id="oceanum_wave_dutch_era5_v1_grid",
            color="blue",
            site_size=2.0,
        ),
    ],
)

WESTERN_EUROPE_NORA3_CONFIG = FigureConfig(
    output_name="weuro_nora3_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_weuro_nora3_v1_gridstats",
    spec_id="oceanum_wave_weuro_nora3_v1_spec",
    grid_id="oceanum_wave_weuro_nora3_v1_grid",
    domain_name="Western Europe NORA3",
    depth_contours=[50, 100, 200, 500, 1000, 2000],
    figsize=(12, 8),
    cbar_shrink=0.7,
    show_borders=True,
    site_size=1.0,
)

TAIWAN_CONFIG = FigureConfig(
    output_name="taiwan_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_twan5km_era5_gridstats",
    spec_id="oceanum_wave_twan5km_era5_spec",
    grid_id="oceanum_wave_twan5km_era5_grid",
    domain_name="Taiwan 5km",
    depth_contours=[50, 100, 500, 1000, 2000, 4000],
    figsize=(8, 10),
    cbar_shrink=0.7,
    show_borders=True,
    site_size=2.0,
    nests=[
        NestConfig(
            name="Taiwan 1km",
            spec_id="oceanum_wave_twan1km_era5_spec",
            grid_id="oceanum_wave_twan1km_era5_grid",
            color="blue",
            site_size=3.0,
        ),
        NestConfig(
            name="Taiwan 500m",
            spec_id="oceanum_wave_twan500m_era5_spec",
            grid_id="oceanum_wave_twan500m_era5_grid",
            color="green",
            site_size=5.0,
        ),
    ],
)


if __name__ == "__main__":
    import sys
    
    configs = {
        "nz": NZ_CONFIG,
        "mediterranean": MEDITERRANEAN_CONFIG,
        "gulf": GULF_CONFIG,
        "peru": PERU_CONFIG,
        "kingisland": KING_ISLAND_CONFIG,
        "wafr": WEST_AFRICA_CONFIG,
        "morocco": MOROCCO_CONFIG,
        "malay": MALAY_CONFIG,
        "bass": BASS_STRAIT_CONFIG,
        "redsea": RED_SEA_CONFIG,
        "taranaki": TARANAKI_CONFIG,
        "useast": US_EAST_CONFIG,
        "weuro": WESTERN_EUROPE_CONFIG,
        "weuro_nora3": WESTERN_EUROPE_NORA3_CONFIG,
        "taiwan": TAIWAN_CONFIG,
    }
    
    if len(sys.argv) < 2:
        print("Usage: python generate_figures.py <config_name> [config_name2 ...]")
        print(f"Available configs: {', '.join(configs.keys())}")
        print("Use 'all' to generate all figures.")
        sys.exit(1)
    
    if sys.argv[1] == "all":
        for name, config in configs.items():
            print(f"\n{'='*60}")
            print(f"Generating {name} figure...")
            print('='*60)
            generate_figure(config)
    else:
        for name in sys.argv[1:]:
            if name not in configs:
                print(f"Unknown config: {name}")
                print(f"Available configs: {', '.join(configs.keys())}")
                continue
            print(f"\n{'='*60}")
            print(f"Generating {name} figure...")
            print('='*60)
            generate_figure(configs[name])

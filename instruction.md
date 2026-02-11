# Oceanum Wave Hindcast Documentation Generation Guide

This document provides comprehensive instructions for generating wave hindcast specification documents for Oceanum datasources. It is designed to enable AI assistants to create consistent, accurate documentation without prior context.

---

## Overview

Oceanum produces wave hindcast datasets using spectral wave models (primarily SWAN and WW3). Each hindcast requires a specification document that describes the model configuration, forcing data, output parameters, and data access information. Documents are written in Markdown with HTML styling for proper rendering.

---

## 1. Information Sources

### 1.1 Model Configuration Files

The primary source of technical information is the model configuration YAML files located in:
- **SWAN hindcasts**: `/config/hindcast/ontask/tasks/swan/prod/` (production) or `/config/hindcast/ontask/tasks/swan/project/` (specialised projects)
- **WW3 hindcasts**: `/config/hindcast/ontask/tasks/ww3/`

Key parameters to extract from config files:

| Parameter | Config Location | Description |
|-----------|-----------------|-------------|
| `global_start` | `env.CONFIG.kwds` | Hindcast start date |
| `global_end` | `env.CONFIG.kwds` | Hindcast end date (if fixed) or check if updating |
| `grid.x0, x1, y0, y1` | `nests[].grid.kwds` | Domain bounding box |
| `grid.dx, dy` | `nests[].grid.kwds` | Spatial resolution in degrees |
| `spectrum.f0` | `nests[].spectrum.kwds` | Starting frequency (Hz) |
| `spectrum.nfcell` | `nests[].spectrum.kwds` | Number of frequency bins |
| `spectrum.df` | `nests[].spectrum.kwds` | Frequency increment ratio (e.g., 1.1 = 10%) |
| `spectrum.dd` | `nests[].spectrum.kwds` | Directional resolution (degrees) |
| `physics` | `nests[].physics` | Source term parameterisation (usually ST6) |
| `forcing.wind` | `nests[].forcing.wind` | Wind forcing source |
| `boundary` | `nests[].boundary` | Spectral boundary conditions |
| `sites` | `env.CONFIG.kwds.sites` | Path to spectra output sites file |

### 1.2 Intake Catalogs

Additional metadata is available in intake catalogs:
- **Gridded parameters**: `/config/catalog/intake/hindcast/hindcast.yml`
- **Wave spectra**: `/config/catalog/intake/wavespectra/wavespectra.yml`

Search for the datasource ID (e.g., `oceanum_wave_morocco_5km_era5_grid`) to find:
- `description`: Detailed dataset description
- `metadata.name`: Human-readable name
- `metadata.details`: URL to documentation (update this after creating document)
- `metadata.tags`: Keywords for the dataset

### 1.3 Datamesh API

Query live data for accurate temporal coverage and site counts:

```python
from oceanum.datamesh import Connector

conn = Connector()

# Get datasource metadata and variables
datasource = conn.get_datasource("oceanum_wave_morocco_5km_era5_grid")
variables = datasource.variables  # Full variable schema

# Get temporal coverage
times = conn.query(datasource="oceanum_wave_morocco_5km_era5_grid", variables=["time"])
start_time = times.time.values[0]
end_time = times.time.values[-1]

# Get number of spectra output sites
sites = conn.query(datasource="oceanum_wave_morocco_5km_era5_spec", variables=["lon", "lat"])
num_sites = len(sites.lon)
```

---

## 2. Document Structure

### 2.1 Required Sections

Every hindcast document must include these sections in order:

1. **HTML Style Block** - Centred tables and figures
2. **Title** - Format: "Oceanum [Region] [Forcing] Wave Hindcast Specification"
3. **Date** - Month and year of document creation
4. **Summary Table** - Key specifications at a glance
5. **Dataset Description** - Detailed narrative description
6. **Figure 1** - Mean significant wave height map with spectra sites
7. **Validation** - Link to satellite validation app
8. **Data Description (Table 1)** - Metadata summary
9. **Linked Datamesh Datasources** - Links to grid and spectra datasets
10. **Gridded Output Parameters (Table 2)** - Variable descriptions
11. **Footer** - www.oceanum.science

### 2.2 Template Structure

```markdown
<style>
p { text-align: justify; }
img { display: block; margin-left: auto; margin-right: auto; }
table { margin-left: auto; margin-right: auto; }
</style>

# Oceanum [Region] [Forcing] Wave Hindcast Specification

**[Month] [Year]**

| | |
|---|---|
| **Model** | SWAN 41.31 |
| **Period** | [Start] - [End or "Updating"] |
| **Spatial resolution** | [dx] degree (~[km] km) |
| **Temporal resolution** | 1 hourly |
| **Region** | [x0]E - [x1]E, [y0]N - [y1]N |
| **Forcings** | [Wind source] winds and Oceanum spectra |

---

## Dataset description

[3-4 paragraphs describing the dataset, model setup, and applications]

<img src="./figures/[region]_figure1_hs_mean.png" alt="Figure 1" width="600">

**Figure 1.** Mean significant wave height from the [Region] hindcast domain...

---

## Validation

The wave hindcast can be validated against satellite altimeter observations using the <a href="https://hindcast-satellite-validation-main-prod.apps.oceanum.io/" target="_blank">Oceanum Hindcast Satellite Validation App</a>...

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum [Region] [Forcing] wave hindcast |
| ... | ... |

### Linked Datamesh datasources

- <a href="https://ui.datamesh.oceanum.io/datasource/[grid_id]" target="_blank">[Grid description]</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/[spec_id]" target="_blank">[Spectra description]</a>

---

## Gridded output parameters

**Table 2.** Gridded output parameters.

| Variable | Long Name | Units |
|---|---|---|
| ... | ... | ... |

---

www.oceanum.science
```

---

## 3. Content Guidelines

### 3.1 Temporal Coverage

**Determining if a hindcast is "Updating":**
- Check `global_end` in the config file
- If `global_end` is in the past or has a fixed date → use that date (e.g., "Jan 1979 - Oct 2024")
- If `global_end` is `null`, very far in the future, or the config shows continuous operation → use "Updating" (e.g., "Jan 1979 - Updating")

**Important**: Always verify against actual data using Datamesh query for accurate end dates.

### 3.2 Spatial Resolution

Convert degrees to approximate kilometres:
- At equator: 1° ≈ 111 km
- General formula: km ≈ degrees × 111 × cos(latitude)
- Common conversions:
  - 0.05° ≈ 5 km
  - 0.01° ≈ 1 km
  - 0.005° ≈ 500 m
  - 0.001° ≈ 100 m
  - 0.0005° ≈ 50 m

### 3.3 Frequency Discretisation

Calculate the maximum frequency from spectrum parameters:
- `f_max = f0 × df^(nfcell-1)`
- Example: f0=0.0418, df=1.1, nfcell=36 → f_max ≈ 1.18 Hz

Standard format: "[nfcell] frequencies between [f0] - [f_max] Hz at [df×100-100]% logarithmic increments"

### 3.4 Partition Types

Identify partition types from output variables:
- **Sea/Swell split**: Variables like `hs_sea`, `hs_sw` (8-second period split)
- **Watershed partitions**: Variables like `phs0`, `phs1`, `phs2`, `phs3`
  - `phs0` = wind-forced partition
  - `phs1`, `phs2`, `phs3` = swell partitions (up to 3)

Count the number of `phs*` variables to determine partition count.

### 3.5 Wind Forcing Types

Common forcing sources and their descriptions:

| Forcing | Description | Link |
|---------|-------------|------|
| ERA5 | ECMWF ERA5 reanalysis | https://cds.climate.copernicus.eu/ |
| NORA3 | Norwegian Reanalysis 3km | https://thredds.met.no/thredds/catalog/nora3/catalog.html |
| CFSR | NCEP Climate Forecast System Reanalysis | https://cfs.ncep.noaa.gov/ |
| CCAM | Conformal Cubic Atmospheric Model (Oceanum) | Internal |
| CLIFLO | NIWA weather station observations | https://cliflo.niwa.co.nz/ |

### 3.6 Dataset Description Paragraphs

Structure the description as follows:

**Paragraph 1**: Domain overview, geographic coverage, temporal span, model type, and purpose.

**Paragraph 2**: Forcing data sources (winds, currents, water levels, boundaries), calibration reference (Ribal and Young 2019 satellite altimeter dataset), and bathymetry source.

**Paragraph 3**: Model physics (ST6 source terms), spectral discretisation, grid resolution.

**Paragraph 4**: Output summary (hourly estimates, parameter types, partitions), storage format, and applications.

**Key phrase to include**: "The hindcast is calibrated against the satellite altimeter dataset of <a href=\"https://www.nature.com/articles/s41597-019-0083-9\" target=\"_blank\">Ribal and Young (2019)</a>."

---

## 4. Figure Generation

### 4.1 Standard Hindcast Figures (with gridstats)

Use the figure generation script for hindcasts with gridstats available:

```bash
cd /source/datasource-description
python scripts/generate_figures.py [config_name]
```

The script requires a `FigureConfig` entry in `scripts/generate_figures.py`:

```python
REGION_CONFIG = FigureConfig(
    output_name="region_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_region_era5_v1_gridstats",
    spec_id="oceanum_wave_region_era5_v1_spec",
    grid_id="oceanum_wave_region_era5_v1_grid",
    domain_name="Region Name",
    depth_contours=[50, 100, 200, 500, 1000, 2000],
    figsize=(12, 8),
    cbar_shrink=0.7,
    show_borders=True,
    site_size=2.0,
)
```

### 4.2 Specialised Coastal Figures (without gridstats)

For ultra-high resolution domains without gridstats, create simple domain extent figures using OSM land polygons:

```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import box
from shapely.ops import unary_union
import geopandas as gpd
from oceanum.datamesh import Connector

conn = Connector()

# Domain bounds from config
x0, y0, x1, y1 = 174.75, -41.4, 174.915, -41.224

# Query high-resolution OSM land polygons
land = conn.query(
    datasource='osm-land-polygons',
    geofilter={'type': 'bbox', 'geom': [x0, y0, x1, y1]},
)

# Create ocean as inverse of land
plot_extent = box(x0-0.03, y0-0.02, x1+0.03, y1+0.02)
land_union = unary_union(land.geometry)
ocean = plot_extent.difference(land_union)

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([x0-0.03, x1+0.03, y0-0.02, y1+0.02], crs=ccrs.PlateCarree())

gpd.GeoSeries([ocean]).plot(ax=ax, facecolor='lightblue', edgecolor='none', transform=ccrs.PlateCarree())
land.plot(ax=ax, facecolor='lightgray', edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())
ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)

# Domain box
domain = box(x0, y0, x1, y1)
gpd.GeoSeries([domain]).boundary.plot(ax=ax, color='red', linewidth=2, transform=ccrs.PlateCarree())

ax.set_title('Region Wave Hindcast Domain', fontsize=12)
plt.savefig('figures/region_figure1_domain.png', dpi=150, bbox_inches='tight')
```

---

## 5. Post-Creation Tasks

### 5.1 Update README

Add the new document to `/source/datasource-description/README.md` under the appropriate section:

- **Global**: Global hindcasts
- **ERA5 Forced Regional Hindcasts**: Regional SWAN/WW3 with ERA5 winds
- **CFSR Forced Regional Hindcasts**: Regional with CFSR winds
- **NORA3 Forced Regional Hindcasts**: Regional with NORA3 winds
- **Specialised Coastal Hindcasts**: Ultra-high resolution harbour/coastal models

### 5.2 Update Intake Catalogs

Update the `details` field in both hindcast and wavespectra catalogs:

```yaml
details: https://datasets.oceanum.io/oceanum_[region]_wave_hindcast.html
```

**Note**: Use `.html` extension (documents are rendered to HTML for web hosting).

### 5.3 Naming Conventions

- **Document filename**: `oceanum_[region]_wave_hindcast.md`
- **Figure filename**: `figures/[region]_figure1_hs_mean.png` or `figures/[region]_figure1_domain.png`
- **HTML URL**: `https://datasets.oceanum.io/oceanum_[region]_wave_hindcast.html`

---

## 6. Reference Documents

Use these existing documents as templates:

| Document | Type | Notable Features |
|----------|------|------------------|
| `oceanum_morocco_wave_hindcast.md` | ERA5 regional | Standard structure |
| `oceanum_western_europe_wave_hindcast.md` | ERA5 regional | Large domain, multiple countries |
| `oceanum_western_europe_nora3_wave_hindcast.md` | NORA3 regional | Alternative forcing |
| `oceanum_black_sea_wave_hindcast.md` | CFSR regional | Dual forcing periods (CFSv1/CFSv2) |
| `oceanum_wellington_wave_hindcast.md` | Specialised coastal | Ultra-high resolution, observational winds |
| `oceanum_bluff_wave_hindcast.md` | Specialised coastal | CCAM downscaled winds |

---

## 7. Common Datasource ID Patterns

Datasource IDs follow predictable patterns:

| Type | Pattern | Example |
|------|---------|---------|
| Grid parameters | `oceanum_wave_[region]_[forcing]_v[N]_grid` | `oceanum_wave_morocco_5km_era5_grid` |
| Wave spectra | `oceanum_wave_[region]_[forcing]_v[N]_spec` | `oceanum_wave_morocco_5km_era5_spec` |
| Grid statistics | `oceanum_wave_[region]_[forcing]_v[N]_gridstats` | `oceanum_wave_morocco_5km_era5_gridstats` |

Search the intake catalogs to confirm exact IDs before using them.

---

## 8. Quality Checklist

Before finalising a document, verify:

- [ ] All dates are accurate (check Datamesh for actual temporal coverage)
- [ ] Spatial resolution matches config (dx/dy values)
- [ ] Frequency range calculated correctly from spectrum parameters
- [ ] Number of spectra sites verified via Datamesh query
- [ ] Partition types correctly identified from output variables
- [ ] All links are valid (Datamesh, external references)
- [ ] Figure generated and displays correctly
- [ ] README updated with new document link
- [ ] Intake catalog `details` field updated with HTML URL
- [ ] Document renders correctly in Markdown preview

---

## Appendix: Config File to Document Mapping

| Document | Config Files |
|----------|--------------|
| oceanum_sw_northamerica_wave_hindcast.pdf | `/config/hindcast/ontask/tasks/swan/prod/era5_northamerica/swan_era5_baja_*.yml` |
| oceanum_bass_strait_wave_hindcast.pdf | `/config/hindcast/ontask/tasks/swan/prod/era5_aus/swan_era5_bass*.yml` |
| oceanum_baltic_sea_wave_hindcast.pdf | `/config/hindcast/ontask/tasks/swan/prod/nora3_europe/swan_nora3_baltic.yml` |
| oceanum_global_wave_hindcast.pdf | `/config/hindcast/ontask/tasks/ww3/glob05_prod/ww3_era5_glob05*.yaml` |
| oceanum_black_sea_wave_hindcast.md | `/config/hindcast/ontask/tasks/swan/prod/cfsr_blacksea/swan_blacksea_cfs*.yml` |
| oceanum_wellington_wave_hindcast.md | `/config/hindcast/ontask/tasks/swan/project/welt/swan_era5_welt_cliflo.yml` |
| oceanum_bluff_wave_hindcast.md | `/config/hindcast/ontask/tasks/swan/project/bluff/swan_ccam_bluff.yml` |

---

www.oceanum.science
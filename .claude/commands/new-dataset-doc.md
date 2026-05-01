# New Dataset Description Document

Create a new Oceanum dataset description document for: **$ARGUMENTS**

You are creating documentation for an Oceanum Datamesh datasource. Work through the steps below in order, gathering real information at each stage before writing anything. Do not invent values — every number must be verified from a config file or Datamesh query.

---

## Step 1 — Identify the document type

Determine which type of document is needed from the arguments:

- **Wave hindcast** — historical wave model run (SWAN or WW3), forced by ERA5 / CFSR / NORA3 / CCAM / CLIFLO
- **Wave forecast** — operational wave model (SWAN), forced by GFS and/or ECMWF, with a rolling archive
- **CCAM atmospheric hindcast** — historical atmospheric downscaling using CCAM

If the type is ambiguous, ask the user before proceeding.

---

## Step 2 — Gather information from config files

### For wave hindcasts

Two config formats exist. Identify which applies before reading.

#### Ontask format (legacy)

Standalone YAML files in:
- SWAN production: `/config/hindcast/ontask/tasks/swan/prod/`
- SWAN special projects: `/config/hindcast/ontask/tasks/swan/project/`
- WW3: `/config/hindcast/ontask/tasks/ww3/`

Config keys use the prefix `env.CONFIG.kwds.*`.

#### Prax format (current)

Single YAML file per deployment in `/config/hindcast/prax/swan/[name]/[name].yml`.

The onswan config is embedded inside Kubernetes configmaps under `resources.configmaps`:

- **First configmap** (`onswan-[parent]-config`): the parent nest model config. Its `nests:` list defines the full hierarchy (parent + all children with `id`, `parentid`, `grid`, `boundary`), but only the parent entry has `blocks` (output variables) and `spectrum`. Extract from here: start/end dates, spectrum parameters, wind/current forcing, boundary, and the complete nest ID list with bounds.
- **Second configmap** (`onswan-nests-config`): one sub-config per child nest, each with full `blocks`, `spectrum`, `grid`, and `sites`. Use this to confirm child bounds, resolution, and output variables. Spectrum parameters should be consistent across all nests — verify this.

For a multi-nest deployment, build a summary table as you read:

| Nest | id | parentid | x0 / x1 / y0 / y1 | dx | Sites file |
|---|---|---|---|---|---|
| Parent | nzpar | — | … | 0.05 | … |
| Child | hbay | nzpar | … | 0.01 | … |

#### Fields to extract (both formats)

| Field | Config key |
|---|---|
| Start date | `kwds.global_start` |
| End date | `kwds.global_end` (null or far-future → "Updating") |
| Domain bounds | `nests[].grid.kwds`: `x0`, `x1`, `y0`, `y1` |
| Resolution | `nests[].grid.kwds`: `dx`, `dy` |
| Starting frequency | `nests[].spectrum.kwds.f0` |
| Frequency bins | `nests[].spectrum.kwds.nfcell` |
| Frequency ratio | `nests[].spectrum.kwds.df` (e.g. 1.1 = 10% increments) |
| Directional resolution | `nests[].spectrum.kwds.dd` |
| Wind forcing | `nests[].forcing.wind.kwds.dataset_id` |
| Current forcing | `nests[].forcing.current.kwds.dataset_id` (if present) |
| Boundary conditions | `nests[].boundary` |
| Physics | `nests[].physics` (usually ST6) |
| Spectra sites file | `kwds.sites` |

### For wave forecasts

Read config from `/config/forecast/ontask/tasks/swan/` under `gfs/` or `ec/`.

Additional fields:
- `run_length` → forecast horizon
- Check `/config/catalog/intake/forecast/forecast.yml` for `cycle_period`, `parchive`, `pforecast`
- Check `/config/catalog/intake/nowcast/nowcast.yml` for nowcast datasources

### For CCAM atmospheric hindcasts

Read config from the relevant CCAM project directory. Extract domain bounds, resolution, start/end dates, ERA5 forcing version, and vertical output levels.

---

## Step 3 — Look up the intake catalog entry

Search the relevant catalog for the datasource:

```bash
# Hindcast grid and spectra IDs
grep -A 20 "oceanum_wave_[region]" /config/catalog/intake/hindcast/hindcast.yml
grep -A 20 "oceanum_wave_[region]" /config/catalog/intake/wavespectra/wavespectra.yml

# Gridstats IDs (separate catalog — always check here, not hindcast.yml)
grep -A 20 "[region]" /config/catalog/intake/stats/stats.yml

# Forecasts
grep -A 20 "[region]" /config/catalog/intake/forecast/forecast.yml

# Atmospheric hindcasts
grep -A 20 "[region]" /config/catalog/intake/[relevant catalog]
```

For a multi-nest deployment, grep for each nest ID individually. Extract for each datasource: `description`, `metadata.name`, `metadata.tags`, and existing `details` URL (you will update this after creating the document).

If a gridstats entry is not found in `stats.yml`, note this and use the fallback figure approach described in Step 6.

---

## Step 4 — Query Datamesh to verify live data

```python
from oceanum.datamesh import Connector
conn = Connector()

# Verify temporal coverage
ds = conn.get_datasource("DATASOURCE_ID_GRID")
times = conn.query(datasource="DATASOURCE_ID_GRID", variables=["time"])
start = times.time.values[0]
end = times.time.values[-1]

# Count spectra output sites
sites = conn.query(datasource="DATASOURCE_ID_SPEC", variables=["lon", "lat"])
n_sites = len(sites.lon)

# Get output variables
print(ds.variables)

# For forecasts — verify frequency discretisation
spec = conn.query(datasource="DATASOURCE_ID_SPEC", variables=["freq"])
print("Frequencies:", spec.freq.values)
```

Use the Datamesh-reported dates as the authoritative temporal coverage. Cross-check the variable list against Table 2 in the template.

---

## Step 5 — Calculate derived values

**Maximum frequency:**

The formula depends on how `nfcell` is interpreted by the model wrapper:
- **onswan** (`nfcell` = number of frequency *increments*): `f_max = f0 × df^nfcell`
- **ontask/legacy** (`nfcell` = number of frequency *bins*): `f_max = f0 × df^(nfcell - 1)`

**Always verify by querying the actual `freq` coordinate from the spectra datasource — do not rely on the formula alone:**
```python
ds = conn.query(datasource="DATASOURCE_ID_SPEC", variables=["freq"])
print("n freqs:", len(ds.freq.values), "f0:", ds.freq.values[0], "fmax:", ds.freq.values[-1])
```

**Spatial resolution in km** (approximate):
- 0.05° ≈ 5 km, 0.01° ≈ 1 km, 0.005° ≈ 500 m, 0.001° ≈ 100 m
- General: km ≈ degrees × 111 × cos(centre_latitude)

**Directional resolution:** dd degrees (e.g. dd=10 → 36 directional bins; dd=360/ndirs)

**Partition types** — inspect the variable list:
- `hs_sea` / `hs_sw` present → sea/swell split at 8-second period
- `phs0`, `phs1`, `phs2`, `phs3` present → watershed partitions (phs0 = wind-forced, phs1-3 = swell)

---

## Step 6 — Generate the figure

### Standard hindcast (gridstats available)

Add a `FigureConfig` entry to `scripts/generate_figures.py`:

```python
REGION_CONFIG = FigureConfig(
    output_name="[region]_figure1_hs_mean.png",
    gridstats_id="oceanum_wave_[region]_[forcing]_v[N]_gridstats",
    spec_id="oceanum_wave_[region]_[forcing]_v[N]_spec",
    grid_id="oceanum_wave_[region]_[forcing]_v[N]_grid",
    domain_name="[Region Name]",
    depth_contours=[50, 200, 1000, 3000],   # adjust to domain depth range
    figsize=(12, 8),
    cbar_shrink=0.7,
    show_borders=True,
    site_size=2.0,
)
```

Then run:
```bash
python scripts/generate_figures.py [config_name]
```

### Multi-nest hindcast with parent gridstats

When a deployment has one parent domain and multiple child nests, produce a single overview figure: mean Hs from the parent gridstats as the background, with each child nest's bounding box overlaid as a labelled rectangle.

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from oceanum.datamesh import Connector

conn = Connector()

# Load parent gridstats mean Hs
stats = conn.query(datasource="[parent_gridstats_id]", variables=["hs_mean"])

fig, ax = plt.subplots(figsize=(12, 10), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([x0_parent, x1_parent, y0_parent, y1_parent], crs=ccrs.PlateCarree())

# Plot mean Hs
stats.hs_mean.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='turbo', add_colorbar=True)

# Coastlines and borders
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.3)
ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)

# Overlay child nest bounding boxes
nests = [
    ("hbay", "Hawke Bay",        176.85, 178.60, -39.80, -38.50),
    ("trki", "Taranaki",         173.35, 175.25, -40.30, -38.55),
    # ... one entry per child nest
]
for nest_id, label, nx0, nx1, ny0, ny1 in nests:
    rect = mpatches.Rectangle(
        (nx0, ny0), nx1 - nx0, ny1 - ny0,
        linewidth=1.5, edgecolor='black', facecolor='none',
        transform=ccrs.PlateCarree(),
    )
    ax.add_patch(rect)
    ax.text(nx0 + (nx1 - nx0) / 2, ny1, label,
            transform=ccrs.PlateCarree(), fontsize=7,
            ha='center', va='bottom')

ax.set_title('[Region] Multiscale Wave Hindcast', fontsize=13)
plt.savefig('figures/[region]_figure1_hs_mean.png', dpi=150, bbox_inches='tight')
```

For depth contours, **always use a dedicated static bathymetry datasource** (e.g. `gebco_2025` with variable `elevation`, `depth_negate=True`) rather than querying the model grid datasource. Model grids are large time-series datasets; querying them for depth pulls the full archive via dask and is extremely slow. The `depth_id` / `depth_variable` / `depth_negate` fields on `FigureConfig` exist for this purpose.

If the parent gridstats datasource does not yet exist in `stats.yml`, use the fallback approach below instead and update the figure later once gridstats are available.

### Coastal / ultra-high-res (no gridstats)

Use OSM land polygons to draw the domain extent:

```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import box
from shapely.ops import unary_union
import geopandas as gpd
from oceanum.datamesh import Connector

conn = Connector()
x0, y0, x1, y1 = [domain bounds from config]
pad_x, pad_y = 0.03, 0.02

land = conn.query(
    datasource='osm-land-polygons',
    geofilter={'type': 'bbox', 'geom': [x0, y0, x1, y1]},
)
plot_extent = box(x0 - pad_x, y0 - pad_y, x1 + pad_x, y1 + pad_y)
ocean = plot_extent.difference(unary_union(land.geometry))

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([x0 - pad_x, x1 + pad_x, y0 - pad_y, y1 + pad_y], crs=ccrs.PlateCarree())
gpd.GeoSeries([ocean]).plot(ax=ax, facecolor='lightblue', edgecolor='none', transform=ccrs.PlateCarree())
land.plot(ax=ax, facecolor='lightgray', edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())
ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)
gpd.GeoSeries([box(x0, y0, x1, y1)]).boundary.plot(ax=ax, color='red', linewidth=2, transform=ccrs.PlateCarree())
ax.set_title('[Region] Wave Hindcast Domain', fontsize=12)
plt.savefig('figures/[region]_figure1_domain.png', dpi=150, bbox_inches='tight')
```

### Forecast (same domain as existing hindcast)

Reuse the hindcast figure. No new figure needed.

---

## Step 7 — Write the document

Create the file `oceanum_[region]_wave_hindcast.md` (or `_forecast.md`, `_ccam_hindcast.md`). Use the exact template for the document type below.

### Wave hindcast template

```markdown
---
title: Oceanum [Region] [Forcing] Wave Hindcast
---

<style>
p { text-align: justify; }
img { display: block; margin-left: auto; margin-right: auto; }
table { margin-left: auto; margin-right: auto; }
</style>

<img src="./assets/oceanum-secondary-logo-marine-rgb-900px-w-72ppi.png" alt="Oceanum Logo" width="300">

<br><br>

# Oceanum [Region] [Forcing] Wave Hindcast

**[Month Year]**

| | |
|---|---|
| **Model** | SWAN 41.31 |
| **Period** | [Mon YYYY - Mon YYYY or "Updating"] |
| **Spatial resolution** | [dx] degree (~[km] km) |
| **Temporal resolution** | 1 hourly |
| **Region** | [x0]W/E - [x1]W/E, [y0]N/S - [y1]N/S |
| **Forcings** | [Wind source] winds[, currents,] and Oceanum spectra |

---

## Dataset description

[Paragraph 1: Domain overview — region name, geographic features covered, wave model type (SWAN third-generation spectral), period, broad purpose.]

[Paragraph 2: Forcing data — winds (with link), ocean currents, bathymetry source (GEBCO with year and link). Mention boundary spectra from Oceanum Global WW3. Include: "The hindcast is calibrated against the satellite altimeter dataset of <a href="https://www.nature.com/articles/s41597-019-0083-9" target="_blank">Ribal and Young (2019)</a>."]

[Paragraph 3: Model physics — ST6 source terms (with link), spectral discretisation: "[ndirs] directional bins and [nfcell] frequency bins, covering a frequency range from [f0] to [f_max] Hz with [increment]% logarithmic increments", grid resolution.]

[Paragraph 4: Output summary — hourly estimates, parameter types, partition types, spectra site count, storage format, applications.]

<img src="./figures/[region]_figure1_hs_mean.png" alt="Figure 1" width="600">

**Figure 1.** Mean significant wave height from the [Region] hindcast domain. The locations of 2D spectra hourly output are shown by the black dots. Depth contours are shown at [list contours]m.

---

## Validation

The wave hindcast can be validated against satellite altimeter observations using the <a href="https://hindcast-satellite-validation-main-prod.apps.oceanum.io/" target="_blank">Oceanum Hindcast Satellite Validation App</a>. This interactive tool allows users to compare modelled significant wave height against satellite altimeter measurements at any location within the model domain, providing density scatter plots, quantile comparisons, and statistical metrics.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum [Region] [forcing] wave hindcast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://swanmodel.sourceforge.io/" target="_blank">SWAN 41.31A</a> |
| **Source terms** | <a href="https://journals.ametsoc.org/view/journals/atot/29/9/jtech-d-11-00092_1.xml" target="_blank">ST6</a> |
| **Temporal coverage** | [YYYY-MM-DD] to [present (updating) or YYYY-MM-DD] |
| **Temporal resolution** | Hourly |
| **Spatial coverage** | [[x0]W/E, [y0]N/S, [x1]W/E, [y1]N/S] at [dx] degree |
| **Spectra output sites** | [n_sites] |
| **Frequency discretisation** | [nfcell] frequencies between [f0] - [f_max] Hz at [increment]% logarithmic increments |
| **Direction resolution** | [dd] deg |
| **Bathymetry** | <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/" target="_blank">GEBCO [year] Grid</a> |
| **Winds** | [Wind source with link] |
| **Currents** | [Currents source or omit row if none] |
| **Boundary** | <a href="https://ui.datamesh.oceanum.io/datasource/[boundary_id]" target="_blank">[Boundary description]</a> |

### Linked Datamesh datasources

- <a href="https://ui.datamesh.oceanum.io/datasource/[grid_id]" target="_blank">Oceanum [Region] [resolution] hourly wave parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/[spec_id]" target="_blank">Oceanum [Region] [resolution] hourly wave spectra</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/[gridstats_id]" target="_blank">Oceanum [Region] [resolution] gridded wave statistics</a>

---

## Integrated parameters gridded output

Integrated wave parameters are stored hourly over the domain at the native model resolution. Table 2 describes long names and units of all [N] gridded output parameters.

**Table 2.** Gridded output parameters.

| Variable | Long Name | Units |
|---|---|---|
[one row per variable from ds.variables — use exact names from Datamesh, match long names and units to those in existing documents for common variables]

---

www.oceanum.science
```

### Wave forecast template

```markdown
---
title: Oceanum [Region] Wave Forecast
---

<style>
p { text-align: justify; }
img { display: block; margin-left: auto; margin-right: auto; }
table { margin-left: auto; margin-right: auto; }
</style>

<img src="./assets/oceanum-secondary-logo-marine-rgb-900px-w-72ppi.png" alt="Oceanum Logo" width="300">

<br><br>

# Oceanum [Region] Wave Forecast

**[Month Year]**

| | |
|---|---|
| **Model** | SWAN 41.31 |
| **Forecast horizon** | [X] days |
| **Spatial resolution** | [dx] degree (~[km] km) |
| **Temporal resolution** | 1 hourly |
| **Region** | [x0]W/E - [x1]W/E, [y0]N/S - [y1]N/S |
| **Forcings** | GFS/ECMWF winds[, currents,] and Oceanum spectra |
| **Update frequency** | 6-hourly (GFS) / 12-hourly (ECMWF) |

---

## Dataset description

[Paragraph 1: Domain overview, geographic coverage, model type, forecast horizon, update frequency.]

[Paragraph 2: Forcing configurations — GFS (6-hourly, 00/06/12/18 UTC) and ECMWF (12-hourly, 00/12 UTC) in one flowing description. Boundary spectra from Oceanum Global WW3 forced with respective wind source. Currents (if any). Bathymetry.]

[Paragraph 3: Model physics — ST6, spectral discretisation, grid resolution.]

[Paragraph 4: Output summary — hourly forecasts, partition types, archive period (X days), spectra site count. If nowcasts available: "Nowcast datasets are also available, constructed by retaining the most recent data from each forecast cycle to provide a continuous near-real-time historical record."]

<img src="./figures/[region]_figure1_hs_mean.png" alt="Figure 1" width="600">

**Figure 1.** [Caption — can reference hindcast figure if same domain.]

---

## Validation

The wave model physics and calibration have been validated against satellite altimeter observations for the corresponding hindcast domain. Validation results are available through the <a href="https://hindcast-satellite-validation-main-prod.apps.oceanum.io/" target="_blank">Oceanum Hindcast Satellite Validation App</a>, which provides density scatter plots, quantile comparisons, and statistical metrics for the [Region] region.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum [Region] wave forecast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://swanmodel.sourceforge.io/" target="_blank">SWAN 41.31A</a> |
| **Source terms** | <a href="https://journals.ametsoc.org/view/journals/atot/29/9/jtech-d-11-00092_1.xml" target="_blank">ST6</a> |
| **Forecast horizon** | [X] days |
| **Update frequency** | 6-hourly (GFS) / 12-hourly (ECMWF) |
| **Archive period** | [X] days |
| **Temporal resolution** | 1 hourly |
| **Spatial coverage** | [[x0], [y0], [x1], [y1]] at [dx] degree |
| **Spectra output sites** | [n_sites] |
| **Frequency discretisation** | [nfcell] frequencies between [f0] - [f_max] Hz at [increment]% logarithmic increments |
| **Direction resolution** | [dd] deg |
| **Bathymetry** | <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/" target="_blank">GEBCO [year] Grid</a> |
| **Winds** | <a href="https://www.ncep.noaa.gov/products/gfs/" target="_blank">NOAA GFS</a> or <a href="https://www.ecmwf.int/en/forecasts/datasets/open-data" target="_blank">ECMWF IFS</a> |
| **Currents** | [Currents description or omit] |
| **Boundary** | Oceanum Global WW3 wave forecast (GFS or ECMWF forced) |

### Linked Datamesh datasources

**GFS-forced (6-hourly updates):**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_[region]_grid" target="_blank">Oceanum [Region] GFS wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_[region]_spec" target="_blank">Oceanum [Region] GFS wave forecast spectra</a>

**ECMWF-forced (12-hourly updates):**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_[region]_grid" target="_blank">Oceanum [Region] ECMWF wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_[region]_spec" target="_blank">Oceanum [Region] ECMWF wave forecast spectra</a>

**Nowcasts (continuous near-real-time archive):**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_[region]_grid_nowcast" target="_blank">Oceanum [Region] GFS wave nowcast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_[region]_spec_nowcast" target="_blank">Oceanum [Region] GFS wave nowcast spectra</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_[region]_grid_nowcast" target="_blank">Oceanum [Region] ECMWF wave nowcast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_[region]_spec_nowcast" target="_blank">Oceanum [Region] ECMWF wave nowcast spectra</a>

---

## Gridded output parameters

Integrated wave parameters are stored hourly over the domain at the native model resolution. Table 2 describes the gridded output parameters.

**Table 2.** Gridded output parameters.

| Variable | Long Name | Units |
|---|---|---|
[one row per variable]

---

www.oceanum.science
```

### CCAM atmospheric hindcast template

```markdown
---
title: Oceanum [Region] CCAM Atmospheric Hindcast
---

<style>
p { text-align: justify; }
img { display: block; margin-left: auto; margin-right: auto; }
table { margin-left: auto; margin-right: auto; }
</style>

<img src="./assets/oceanum-secondary-logo-marine-rgb-900px-w-72ppi.png" alt="Oceanum Logo" width="300">

<br><br>

# Oceanum [Region] CCAM Atmospheric Hindcast

**[Month Year]**

| | |
|---|---|
| **Model** | CCAM |
| **Period** | [Mon YYYY - Mon YYYY] |
| **Spatial resolution** | [dx] degree (~[km] km) |
| **Temporal resolution** | 1 hourly |
| **Region** | [x0]E - [x1]E, [y0]N/S - [y1]N/S |
| **Forcing** | ERA5 reanalysis |

---

## Dataset description

[Paragraph 1: Domain overview — region, geographic features, weather characteristics specific to the area.]

[Paragraph 2: Model description — CCAM (Conformal Cubic Atmospheric Model) developed by CSIRO with link, dynamical downscaling approach, ERA5 forcing with link.]

[Paragraph 3: Resolution benefits — what the resolution enables, terrain features captured, key atmospheric processes represented, vertical output levels.]

[Paragraph 4: Output summary — hourly atmospheric variables, intended applications (wind resource, wave model forcing, etc.).]

<img src="./figures/[region]_ccam_figure1_domain.png" alt="Figure 1" width="600">

**Figure 1.** [Region] CCAM atmospheric hindcast domain extent. The model covers [description] at [resolution] resolution.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum [Region] CCAM atmospheric hindcast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://www.ccrc.unsw.edu.au/ccam" target="_blank">CCAM (Conformal Cubic Atmospheric Model)</a> |
| **Temporal coverage** | [YYYY-MM-DD] to [YYYY-MM-DD] |
| **Temporal resolution** | 1 hourly |
| **Spatial coverage** | [[x0]E, [y0]N/S, [x1]E, [y1]N/S] at [dx] degree (~[km] km) |
| **Vertical levels** | [e.g. 10m, 150m] |
| **Forcing** | <a href="https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5" target="_blank">ERA5 reanalysis</a> |

### Linked Datamesh datasources

- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_meteo_[region]_ccam_v[N]" target="_blank">Oceanum [Region] CCAM meteo hindcast</a>

---

## Output parameters

Atmospheric variables are stored hourly over the domain at the native model resolution. Table 2 describes the key output parameters.

**Table 2.** Output parameters.

| Variable | Long Name | Units |
|---|---|---|
[one row per variable from ds.variables]

---

www.oceanum.science
```

---

## Step 8 — Post-creation tasks

### 8.1 Add to README.md

Insert a link under the correct section of `README.md`:

| Document type | README section |
|---|---|
| Global hindcast | `## Wave Hindcast > ### Global` |
| ERA5 regional hindcast | `## Wave Hindcast > ### ERA5 Forced Regional Hindcasts` |
| CFSR regional hindcast | `## Wave Hindcast > ### CFSR Forced Regional Hindcasts` |
| NORA3 regional hindcast | `## Wave Hindcast > ### NORA3 Forced Regional Hindcasts` |
| Coastal/specialised hindcast | `## Wave Hindcast > ### Specialised Coastal Hindcasts` |
| GFS+ECMWF forecast | `## Wave Forecast > ### GFS/ECMWF Forced Regional Forecasts` |
| GFS-only forecast | `## Wave Forecast > ### GFS Forced Regional Forecasts` |
| ECMWF-only forecast | `## Wave Forecast > ### ECMWF Forced Regional Forecasts` |
| CCAM atmospheric hindcast | `## Atmospheric Hindcast > ### CCAM Regional Hindcasts` |

Link format: `- [Oceanum [Region] [Type]](./oceanum_[region]_wave_hindcast.md)`

### 8.2 Update intake catalog

Set the `details` field in the catalog entry to the published URL. Use `.html` extension (Jekyll renders `.md` to `.html`):

```yaml
details: https://datasets.oceanum.io/oceanum_[region]_wave_hindcast.html
```

Update both the hindcast grid catalog and the wavespectra catalog. For forecasts, update the forecast catalog (and nowcast catalog if applicable).

---

## Quality checklist

Before finishing, verify each item:

- [ ] All dates confirmed from Datamesh (not just config)
- [ ] Frequency range calculated correctly: f_max = f0 × df^(nfcell−1)
- [ ] Number of spectra sites verified via Datamesh query
- [ ] Partition types correctly identified from actual variable names
- [ ] Figure generated and saved to `figures/`
- [ ] All Datamesh datasource IDs confirmed against intake catalog (don't guess)
- [ ] README.md updated
- [ ] Intake catalog `details` field updated with `.html` URL

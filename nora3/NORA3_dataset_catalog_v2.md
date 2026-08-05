# NORA3 Thredds Catalog — Dataset Overview for Wind Turbine Applications

> **Purpose:** Identify the best NORA3 atmospheric dataset for wind turbine calculations requiring multi-level wind, temperature, and density up to ~300 m height.
> **Source:** MET Norway Thredds server — `thredds.met.no`
> **Crawled:** May 2026 (all height values and time coverage verified directly from OPeNDAP DAS/DDS/ASCII endpoints)

---

## Summary Recommendation

| Priority | Dataset | Reason |
|---|---|---|
| ⭐ Best overall | `atm_3hourly` | Wind, temperature, density, TKE at 50–300 m; 1959–present |
| 2nd (wind only, hourly) | `wind_hourly_v2` | Hourly wind speed/direction at 7 heights (10–750 m); 1959–present |
| 3rd (surface/BL only) | `atm_hourly_v2` | Hourly, but all variables at single scalar heights only (0, 2, 10, 20 m); no multi-level wind |
| Raw archive | `nora3/` raw cycles | 6-hourly forecast cycles; wind components at 6 heights (height2); complex to use |

---

## NORA3_Subsets — Pre-processed Datasets

These are **concatenated "nowcast" files**, built by extracting hours +4 to +9 from each 6-hourly forecast cycle and stitching them into a continuous time series. Available as monthly NetCDF files on Thredds.

---

### 1. `atm_3hourly` — Atmospheric 3-Hourly ⭐ RECOMMENDED

**Path:** `nora3_subset_atmos/atm_3hourly/arome3km_3hr_YYYYMM.nc`

| Property | Value |
|---|---|
| Time resolution | 3-hourly |
| Time coverage start | 1959-01-01 (verified from `arome3km_3hr_195901.nc` DAS) |
| Time coverage end | Present |
| File size | ~8 GB/month |
| Data structure | Nowcast (concatenated from forecast hours +4 to +9) |
| Grid | AROME 3 km Lambert conformal; 1489×889 grid points |

**Height dimension:** Single `height` coordinate with **5 levels** (m AGL):

| height[0] | height[1] | height[2] | height[3] | height[4] |
|---|---|---|---|---|
| 50 m | 100 m | 150 m | 200 m | 300 m |

**Variables — all available at all 5 height levels above:**

| Variable name | Long name | Units | Standard name |
|---|---|---|---|
| `wind_speed` | Wind speed in fixed heights above surface | m/s | `wind_speed` |
| `wind_direction` | Wind direction in fixed heights above surface | degrees clockwise from N | `wind_from_direction` |
| `air_temperature` | Air temperature in fixed heights above surface | K | `air_temperature` |
| `relative_humidity` | Relative humidity in fixed heights above surface | percent | `relative_humidity` |
| `density` | Density of air in fixed heights above surface | kg m⁻³ | `air_density` |
| `tke` | Turbulence kinetic energy | m² s⁻² | — |

**Additional 2D (surface) variables:**

| Variable name | Long name | Units |
|---|---|---|
| `sea_surface_temperature` | Sea surface temperature (SST) | K |

---

### 2. `wind_hourly_v2` — Wind-Only Hourly

**Path:** `nora3_subset_atmos/wind_hourly_v2/arome3kmwind_1hr_YYYYMM.nc`

| Property | Value |
|---|---|
| Time resolution | 1-hourly |
| Time coverage start | 1959-01-01 (verified from `arome3kmwind_1hr_195901.nc` DAS) |
| Time coverage end | Present |
| File size | ~13 GB/month (full); ~2 GB/month (_150m variant) |
| Data structure | Nowcast (concatenated from forecast hours +4 to +9) |
| Grid | AROME 3 km Lambert conformal; 1489×889 grid points |

**Height dimension:** Single `height` coordinate with **7 levels** (m AGL) — confirmed from chunk sizes `[30, 7, 20, 20]`:

| height[0] | height[1] | height[2] | height[3] | height[4] | height[5] | height[6] |
|---|---|---|---|---|---|---|
| 10 m | 20 m | 50 m | 100 m | 250 m | 500 m | 750 m |

**Variables — both available at all 7 height levels:**

| Variable name | Long name | Units | Standard name |
|---|---|---|---|
| `wind_speed` | Wind speed in fixed heights above surface | m/s | `wind_speed` |
| `wind_direction` | Wind direction in fixed heights above surface | degrees clockwise from N | `wind_from_direction` |

**150 m variant** (`arome3kmwind_1hr_YYYYMM_150m.nc`):
- Same 2 variables; single height: **150 m only**
- File size ~2 GB/month

> ⚠️ Wind speed and direction only — no temperature, humidity, density, or TKE. Use `atm_3hourly` if those are needed.

---

### 3. `atm_hourly_v2` — Surface/Boundary Layer Hourly

**Path:** `nora3_subset_atmos/atm_hourly_v2/arome3km_1hr_YYYYMM.nc`

| Property | Value |
|---|---|
| Time resolution | 1-hourly |
| Time coverage start | 1959-01-01 (verified from `arome3km_1hr_195901.nc` DAS) |
| Time coverage end | Present |
| Data structure | Nowcast (concatenated from forecast hours +4 to +9) |
| Grid | AROME 3 km Lambert conformal; 1489×889 grid points |

> ⚠️ **This dataset has NO multi-level wind data.** All variables are at single scalar height dimensions only. The height dimensions are:

| Dimension name | Value | Variables using it |
|---|---|---|
| `height0` | 0 m | `high_type_cloud_area_fraction`, `medium_type_cloud_area_fraction`, `low_type_cloud_area_fraction`, `lifting_condensation_level`, `convective_cloud_area_fraction`, `surface_net_longwave_radiation`, `surface_net_shortwave_radiation`, `precipitation_amount_hourly`, `air_pressure_at_sea_level` (via height_above_msl) |
| `height1` | 2 m | `air_temperature_2m`, `relative_humidity_2m` |
| `height4` | 10 m | `wind_speed`, `wind_direction` |
| `height3` | 20 m | `fog` |
| `height_above_msl` | 0 m | `air_pressure_at_sea_level` |

**Full variable list:**

| Variable name | Long name | Height | Units |
|---|---|---|---|
| `air_pressure_at_sea_level` | Mean Sea Level Pressure (MSLP) | height_above_msl (0 m) | Pa |
| `air_temperature_2m` | Screen level temperature (T2M) | height1 (2 m) | K |
| `relative_humidity_2m` | Screen level relative humidity (RH2M) | height1 (2 m) | 1 |
| `wind_speed` | Wind speed in 10 metre | height4 (10 m) | m/s |
| `wind_direction` | Wind direction in 10 metre | height4 (10 m) | degree |
| `low_type_cloud_area_fraction` | Cloud cover of low clouds (LCC) | height0 (0 m) | 1 |
| `medium_type_cloud_area_fraction` | Cloud cover of medium height clouds (MCC) | height0 (0 m) | 1 |
| `high_type_cloud_area_fraction` | Cloud cover of high clouds (HCC) | height0 (0 m) | 1 |
| `lifting_condensation_level` | Atmosphere lifting condensation level wrt surface (LCL) | height0 (0 m) | m |
| `surface_net_longwave_radiation` | Surface net downward longwave flux in air | height0 (0 m) | W/m² |
| `surface_net_shortwave_radiation` | Surface net downward shortwave flux in air | height0 (0 m) | W/m² |
| `precipitation_amount_hourly` | Hourly precipitation amount | height0 (0 m) | kg/m² |
| `fog` | Fog area fraction | height3 (20 m) | 0–1 |

> ℹ️ Despite what the keyword metadata suggests, this dataset does **not** contain multi-level wind. It is a surface/near-surface boundary layer dataset.

---

## NORA3 Raw Archive — Forecast Cycles

Raw 6-hourly forecast cycles from the AROME-Arctic model. Organised as:

`nora3/{YYYY}/{MM}/{DD}/{HH}/fc{YYYYMMDD}{HH}_{LT}_{type}.nc`

Where `{HH}` ∈ {00, 06, 12, 18} and `{LT}` is the forecast lead time (e.g., 006 = +6 h).

**Time coverage:** August 1958 – present (earliest folder: `nora3/1958/08/`)

Three file types exist per cycle:

---

### A. `_fp.nc` — Fixed Pressure + Height Levels

**Path:** `nora3/YYYY/MM/DD/HH/fc{init}_{lt}_fp.nc`

| Property | Value |
|---|---|
| Time dimension | 1 timestep per file (the lead time hour) |
| Data structure | Forecast (6-hourly init, up to +9 h lead time) |
| Grid | 1489×889 |

**Height dimensions and their values (all verified from `.ascii` query):**

| Dimension | Size | Values (m AGL) | Used by |
|---|---|---|---|
| `height0` | 1 | 0 m | Surface/integral variables (radiation fluxes, precip, etc.) |
| `height1` | 1 | 2 m | `air_temperature_2m`, `relative_humidity_2m`, `specific_humidity_2m`, T min/max |
| `height2` | 6 | **20, 50, 100, 250, 500, 750 m** | `x_wind_z`, `y_wind_z` (wind components at multiple heights) |
| `height3` | 13 | 0, 20, 50, 100, 150, 250, 500, 750, 1000, 1250, 1500, 2000, 2500 m | `cloud_area_fraction` |
| `height4` | 1 | 10 m | `x_wind_10m`, `y_wind_10m`, `wind_speed`, `wind_direction`, wind gusts |
| `height_above_msl` | 1 | 0 m | `air_pressure_at_sea_level` |
| `pressure0` | 16 | 50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000 hPa | All `_pl` variables |

**Key multi-level wind variables (height2: 20–750 m):**

| Variable | Description | Units |
|---|---|---|
| `x_wind_z` | Eastward wind component at height2 levels | m/s |
| `y_wind_z` | Northward wind component at height2 levels | m/s |

**Pressure-level variables (all on pressure0: 16 levels):**

| Variable | Description |
|---|---|
| `x_wind_pl`, `y_wind_pl` | Wind components on pressure levels |
| `air_temperature_pl` | Air temperature on pressure levels |
| `relative_humidity_pl` | Relative humidity on pressure levels |
| `geopotential_pl` | Geopotential on pressure levels |
| `cloud_area_fraction_pl` | Cloud fraction on pressure levels |
| `upward_air_velocity_pl` | Vertical velocity on pressure levels |

**Surface/single-level variables (height0, height1, height4):**
`wind_speed` (10m), `wind_direction` (10m), `x_wind_10m`/`y_wind_10m` (10m), `x_wind_gust_10m`/`y_wind_gust_10m` (10m), `air_temperature_2m`, `relative_humidity_2m`, `specific_humidity_2m`, `air_pressure_at_sea_level`, `surface_air_pressure`, `atmosphere_boundary_layer_thickness`, precipitation, radiation fluxes, cloud fractions, convective diagnostics.

---

### B. `.nc` (no suffix) — Model Levels (65 hybrid sigma-pressure levels)

**Path:** `nora3/YYYY/MM/DD/HH/fc{init}_{lt}.nc`

| Property | Value |
|---|---|
| Vertical levels | 65 hybrid sigma-pressure model levels |
| Data structure | Forecast (6-hourly init) |

> ⚠️ Requires vertical coordinate transformation (hybrid levels to height AGL) before use. Not directly comparable to the subset datasets.

**Variables on 65 model levels:**

| Variable | Description |
|---|---|
| `x_wind_ml`, `y_wind_ml` | Wind components |
| `air_temperature_ml` | Air temperature |
| `turbulent_kinetic_energy_ml` | TKE |
| `specific_humidity_ml` | Specific humidity |
| `cloud_area_fraction_ml` | Cloud fraction |
| `air_pressure_ml` | Full pressure field |

---

### C. `_sfx.nc` — SURFEX Surface Fields

**Path:** `nora3/YYYY/MM/DD/HH/fc{init}_{lt}_sfx.nc`

| Property | Value |
|---|---|
| Vertical levels | Surface only |
| Data structure | Forecast (6-hourly init) |

**Variables:**

| Variable | Description |
|---|---|
| `SST` | Sea surface temperature |
| `TS` | Surface temperature |
| `T2M` | 2m temperature |
| `ZON10M`, `MER10M` | 10m zonal and meridional wind |
| `H` | Sensible heat flux |
| `LE` | Latent heat flux |
| `GFLUX` | Ground heat flux |
| `SIC` | Sea ice concentration |

---

## Summary Comparison Table

| Dataset | Temporal res. | Time coverage | Multi-level wind heights (m) | Temp | Density | TKE | Notes |
|---|---|---|---|---|---|---|---|
| `atm_3hourly` ⭐ | 3-hourly | 1959–present | **50, 100, 150, 200, 300** | ✅ (same heights) | ✅ (same heights) | ✅ (same heights) | Best for wind turbine work |
| `wind_hourly_v2` | 1-hourly | 1959–present | **10, 20, 50, 100, 250, 500, 750** | ❌ | ❌ | ❌ | Wind only; good height range |
| `wind_hourly_v2_150m` | 1-hourly | 1959–present | **150 only** | ❌ | ❌ | ❌ | Compact single-height variant |
| `atm_hourly_v2` | 1-hourly | 1959–present | ❌ (10m only, scalar) | 2m only | ❌ | ❌ | Surface/BL variables only |
| NORA3 raw `_fp.nc` | Per cycle (hourly LT) | Aug 1958–present | **20, 50, 100, 250, 500, 750** (x/y components) | 2m & pressure levels | ❌ | ❌ | One file per forecast lead time; complex |
| NORA3 raw `.nc` | Per cycle | Aug 1958–present | 65 hybrid model levels | ✅ | ❌ | ✅ | Needs level transformation |
| NORA3 raw `_sfx.nc` | Per cycle | Aug 1958–present | 10m only | Surface/2m | ❌ | ❌ | Surface fields only |

---

## Notes on Data Structure

- **NORA3_Subsets**: All files are **nowcast composites**, built by concatenating forecast hours +4 to +9 from each 6-hourly AROME-Arctic cycle (00, 06, 12, 18 UTC). This minimises spin-up issues and produces a seamless time series. Files are stored as monthly NetCDF.
- **NORA3 raw**: Individual forecast cycles stored under `YYYY/MM/DD/HH/` folders. Each cycle provides multiple lead times (+0 to +9 h), one file per lead time. To reconstruct a continuous time series, the +4 to +9 extraction strategy used by the subsets must be applied manually.
- **Grid domain:** All datasets cover roughly 44°N–83°N, 30°W–85°E (Lambert conformal conic centred at 66.3°N, −42°E).

---

*Generated from OPeNDAP DAS/DDS/ASCII metadata queries on thredds.met.no — May 2026*
*All height level values and time coverage start dates verified directly from server responses.*

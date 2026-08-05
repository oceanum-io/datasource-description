# NORA3 Thredds Catalog — Dataset Overview for Wind Turbine Applications

> **Purpose:** Identify the best NORA3 atmospheric dataset for wind turbine calculations requiring multi-level wind, temperature, and density up to ~300 m height.
> **Source:** MET Norway Thredds server — `thredds.met.no`
> **Crawled:** May 2026

---

## Summary Recommendation

| Priority | Dataset | Reason |
|---|---|---|
| ⭐ Best overall | `atm_3hourly` | Wind, temperature, density, TKE at 50–300 m; 1959–present |
| 2nd (wind only) | `wind_hourly_v2` | Hourly wind speed/direction at 10–750 m; 1959–present |
| 3rd (rich variables) | `atm_hourly_v2` | Hourly, many variables, but no density; 1959–present |
| Raw archive | `nora3/` raw cycles | 6-hourly forecast cycles; all model levels; complex to use |

---

## NORA3_Subsets — Pre-processed Datasets

These are **concatenated "nowcast" files**, built by extracting hours +4 to +9 from each 6-hourly forecast cycle, stitching them into a continuous time series. Available as monthly NetCDF files.

### 1. `atm_3hourly` — Atmospheric 3-Hourly ⭐ RECOMMENDED

| Property | Value |
|---|---|
| Path | `nora3_subset_atmos/atm_3hourly/arome3km_3hr_YYYYMM.nc` |
| Time resolution | 3-hourly |
| Time coverage | January 1959 – present |
| File size | ~8 GB/month |
| Data structure | Nowcast (concatenated from forecast hours +4 to +9) |
| Grid | AROME 3 km |

**Height levels (m AGL):** 50, 100, 150, 200, 300

**Variables at multiple heights:**

| Variable | Standard name / Description | Heights available |
|---|---|---|
| `wind_speed` | Wind speed | 50, 100, 150, 200, 300 m |
| `wind_direction` | Wind direction | 50, 100, 150, 200, 300 m |
| `air_temperature_ml` | Air temperature | 50, 100, 150, 200, 300 m |
| `air_density_0` | Air density | 50, 100, 150, 200, 300 m |
| `turbulent_kinetic_energy` | TKE | 50, 100, 150, 200, 300 m |

**Additional surface/2D variables:**
- `air_temperature_2m`, `relative_humidity_2m`
- `sea_surface_temperature`
- `surface_air_pressure`, `precipitation_amount`
- `integral_of_surface_downwelling_shortwave_flux_in_air_wrt_time`

---

### 2. `wind_hourly_v2` — Wind-Only Hourly

| Property | Value |
|---|---|
| Path | `nora3_subset_atmos/wind_hourly_v2/arome3kmwind_1hr_YYYYMM.nc` |
| Time resolution | 1-hourly |
| Time coverage | January 1959 – present |
| File size | ~13 GB/month (full); ~2 GB/month (_150m variant) |
| Data structure | Nowcast (concatenated from forecast hours +4 to +9) |
| Grid | AROME 3 km |

**Height levels (m AGL):** 10, 20, 50, 100, 250, 500, 750

**Variables at multiple heights:**

| Variable | Description | Heights available |
|---|---|---|
| `wind_speed` | Wind speed | 10, 20, 50, 100, 250, 500, 750 m |
| `wind_direction` | Wind direction | 10, 20, 50, 100, 250, 500, 750 m |

**150 m variant** (`arome3kmwind_1hr_YYYYMM_150m.nc`):
- Same 2 variables, single height: 150 m only
- File size ~2 GB/month

> ⚠️ Wind-only dataset — no temperature or density. Use `atm_3hourly` if those are needed.

---

### 3. `atm_hourly_v2` — Full Atmospheric Hourly

| Property | Value |
|---|---|
| Path | `nora3_subset_atmos/atm_hourly_v2/arome3km_1hr_YYYYMM.nc` |
| Time resolution | 1-hourly |
| Time coverage | January 1959 – present |
| File size | Large (multi-level, full variable set) |
| Data structure | Nowcast (concatenated from forecast hours +4 to +9) |
| Grid | AROME 3 km |

**Height levels (m AGL):** 10, 20, 50, 100, 250, 500, 750 (inferred from DAS — same as wind_hourly_v2)

**Variables at multiple heights:**

| Variable | Description |
|---|---|
| `x_wind`, `y_wind` | Eastward and northward wind components |
| `air_temperature` | Air temperature |
| `relative_humidity` | Relative humidity |
| `cloud_area_fraction` | Cloud fraction |
| `atmosphere_boundary_layer_thickness` | PBLH |

**Additional surface variables:**
- `air_pressure_at_sea_level`, `surface_air_pressure`
- `precipitation_amount`, `snowfall_amount`
- Radiation fluxes (SW, LW downwelling/upwelling)

> ℹ️ Richer set of variables than wind_hourly_v2 but no air density. Summary attribute confirms: "concatenated from hour 4 to 9 of each forecast"

---

## NORA3 Raw Archive — Forecast Cycles

These are the **raw 6-hourly forecast cycles** as produced by the AROME-Arctic model. Data is organised as:

`nora3/{YYYY}/{MM}/{DD}/{HH}/fc{YYYYMMDD}{HH}_{LT}_{type}.nc`

Where `{HH}` ∈ {00, 06, 12, 18} and `{LT}` is the lead time (e.g., 006).

Three file types per cycle:

---

### A. `_fp.nc` — Fixed Pressure Levels + Height Levels

| Property | Value |
|---|---|
| Path | `nora3/YYYY/MM/DD/HH/fc{init}_{lt}_fp.nc` |
| Time resolution | 1-hourly (within each 6-hr cycle) |
| Time coverage | 1979 – present |
| Data structure | Forecast (6-hourly init, hours +0 to +9) |

**Height levels (m AGL):** 20, 50, 100, 250, 500, 750

**Pressure levels (hPa):** 50, 70, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 950, 1000

**Variables:**

| Variable | Description | Vertical coord |
|---|---|---|
| `x_wind_z`, `y_wind_z` | Wind components | Height levels |
| `x_wind_pl`, `y_wind_pl` | Wind components | Pressure levels |
| `air_temperature_pl` | Temperature | Pressure levels |
| `relative_humidity_pl` | Relative humidity | Pressure levels |
| `geopotential_pl` | Geopotential | Pressure levels |
| `wind_speed`, `wind_direction` | Derived wind | Height levels |
| `air_pressure_at_sea_level` | MSLP | Surface |
| `air_temperature_2m` | 2m temperature | Surface |
| `relative_humidity_2m` | 2m RH | Surface |

---

### B. `.nc` (no suffix) — Model Levels (Hybrid sigma-pressure)

| Property | Value |
|---|---|
| Path | `nora3/YYYY/MM/DD/HH/fc{init}_{lt}.nc` |
| Time resolution | 1-hourly (within each 6-hr cycle) |
| Vertical levels | 65 hybrid sigma-pressure model levels |
| Data structure | Forecast (6-hourly init) |

**Variables (all on 65 model levels):**

| Variable | Description |
|---|---|
| `x_wind_ml`, `y_wind_ml` | Wind components |
| `air_temperature_ml` | Air temperature |
| `turbulent_kinetic_energy_ml` | TKE |
| `specific_humidity_ml` | Specific humidity |
| `cloud_area_fraction_ml` | Cloud fraction |
| `air_pressure_ml` | Pressure |

> ⚠️ Requires vertical interpolation from hybrid levels to height AGL. Complex to use — prefer `atm_3hourly` subsets unless you need sub-50 m resolution.

---

### C. `_sfx.nc` — SURFEX Surface Fields

| Property | Value |
|---|---|
| Path | `nora3/YYYY/MM/DD/HH/fc{init}_{lt}_sfx.nc` |
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

## Comparison Table

| Dataset | Temporal res. | Time coverage | Heights (m) | Wind | Temp | Density | TKE | Notes |
|---|---|---|---|---|---|---|---|---|
| `atm_3hourly` ⭐ | 3-hourly | 1959–present | 50,100,150,200,300 | ✅ | ✅ | ✅ | ✅ | Best for wind turbine work |
| `wind_hourly_v2` | 1-hourly | 1959–present | 10,20,50,100,250,500,750 | ✅ | ❌ | ❌ | ❌ | Wind only; good height range |
| `wind_hourly_v2_150m` | 1-hourly | 1959–present | 150 | ✅ | ❌ | ❌ | ❌ | Compact; single height |
| `atm_hourly_v2` | 1-hourly | 1959–present | 10,20,50,100,250,500,750 | ✅ | ✅ | ❌ | ❌ | No density |
| NORA3 raw `_fp.nc` | 1-hr (in cycles) | 1979–present | 20,50,100,250,500,750 | ✅ | ✅ | ❌ | ❌ | Forecast cycles; complex |
| NORA3 raw `.nc` | 1-hr (in cycles) | 1979–present | 65 model levels | ✅ | ✅ | ❌ | ✅ | Needs level interpolation |
| NORA3 raw `_sfx.nc` | 1-hr (in cycles) | 1979–present | Surface only | 10m only | ✅ | ❌ | ❌ | Surface fields only |

---

## Notes on Data Structure

- **NORA3_Subsets**: All files are **nowcast composites**, built by concatenating forecast hours +4 to +9 from each 6-hourly AROME-Arctic cycle (00, 06, 12, 18 UTC). This minimises spin-up issues and produces a seamless time series. Files are stored as monthly NetCDF with aggregated versions also available.
- **NORA3 raw**: Individual forecast cycles stored under `YYYY/MM/DD/HH/` folders. Each cycle provides hours +0 to +9. To reconstruct a continuous time series, the same +4 to +9 extraction strategy used by the subsets must be applied manually.
- **Temporal note**: NORA3-WP paper states coverage up to 2019, but the actual files on Sigma2 archive show hourly data from **1996–2017** (72 files). The Thredds subsets extend coverage to **1959–present**.

---

*Generated from OPeNDAP DAS/DDS metadata queries on thredds.met.no — May 2026*

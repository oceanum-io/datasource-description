# NORA3 Datasets Overview

NORA3 is a high-resolution (3 km) regional atmospheric reanalysis based on the HARMONIE-AROME nonhydrostatic model, covering the Nordic/North Atlantic region (44°N–83°N, 30°W–85°E). This document summarises the atmospheric datasets available through the MET Norway Thredds catalog relevant for wind power calculations.

---

## NORA3_Subsets / Atmospheric Datasets

These are pre-processed subsets available at `https://thredds.met.no/thredds/catalog/nora3_subset_atmos/`

### 1. Wind Hourly v2

**Catalog:** `nora3_subset_atmos/wind_hourly_v2/`  
**Aggregated:** `nora3_subset_atmos/wind_hourly_v2_agg/nora3_wind_hourly.ncml`

| Property | Value |
|---|---|
| Time coverage | 1970-01-01 – 2025-01 (aggregated) |
| Temporal resolution | Hourly |
| Grid | 1489 (y) × 889 (x) |
| File organisation | Monthly files |

**Height levels:** 10, 20, 50, 100, 250, 500, 750 m (7 levels)

**Variables:**
- `wind_speed` (time, height, y, x)
- `wind_direction` (time, height, y, x)

---

### 2. Atmospheric Hourly v2

**Catalog:** `nora3_subset_atmos/atm_hourly_v2/`  
**Aggregated:** `nora3_subset_atmos/atm_hourly_v2_agg/nora3_atm_hourly.ncml`

| Property | Value |
|---|---|
| Time coverage | 1970-01-01 – present (aggregated) |
| Temporal resolution | Hourly |
| Grid | 1489 (y) × 889 (x) |
| File organisation | Monthly files |

**Height levels:** Single levels only — surface (0 m MSL), 2 m, 10 m, 20 m

**Variables (15 total, 12 shown):**
- `air_pressure_at_sea_level` (height_above_msl=0)
- `air_temperature_2m` (height=2 m)
- `wind_speed` (height=10 m)
- `wind_direction` (height=10 m)
- `fog` (height=20 m)
- `high_type_cloud_area_fraction` (height=0)
- `lifting_condensation_level` (height=0)
- `surface_net_longwave_radiation` (height=0)
- `surface_net_shortwave_radiation` (height=0)
- `precipitation_amount_hourly` (height=0)
- *(3 additional variables not shown in truncated output)*

> **Note:** Wind is only at 10 m in this dataset. For multi-level wind data, use Wind Hourly v2 above.

---

### 3. Atmospheric 3-Hourly

**Catalog:** `nora3_subset_atmos/atm_3hourly/`

| Property | Value |
|---|---|
| Temporal resolution | 3-hourly |
| Grid | 1489 (y) × 889 (x) |
| File organisation | Monthly files |

**Height levels:** 50, 100, 150, 200, 300 m (5 levels above ground)

**Variables:**
- `air_temperature` (time, height, y, x)
- `relative_humidity` (time, height, y, x)
- `wind_speed` (time, height, y, x)
- `wind_direction` (time, height, y, x)
- `density` (time, height, y, x)
- `tke` — turbulent kinetic energy (time, height, y, x)
- `sea_surface_temperature` (surface only)

> **Note for wind power:** This dataset has multi-level wind up to 300 m at 3-hourly resolution. Notably includes air density, useful for power calculations.

---

## NORA3 Full Archive

Raw model output files available at `https://thredds.met.no/thredds/catalog/nora3/` (individual files) and aggregated at `https://thredds.met.no/thredds/catalog/nora3agg/`.

| Property | Value |
|---|---|
| Time coverage | 1958-01-01 – present (ongoing) |
| Temporal resolution | 3-hourly (forecast runs at +003h to +009h) |
| Grid | 1489 (y) × 889 (x), 3 km resolution |
| Projection | Lambert Conformal Conic |
| File organisation | Year / Month / Day / Hour hierarchy |

Each timestamp produces several file types:

### 3a. Main Model-Level Files (`fc[YYYYMMDDHH]_[NNN].nc`)

**Vertical coordinates:** 65 hybrid sigma-pressure levels (surface to top of atmosphere)

Wind components are on model levels using hybrid coordinates: `p(n,k,j,i) = ap(k) + b(k) * ps(n,j,i)`

**Variables:**
- `air_temperature_ml` — temperature on model levels
- `x_wind_ml` / `y_wind_ml` — zonal/meridional wind components on model levels
- `specific_humidity_ml`
- `turbulent_kinetic_energy_ml`
- `cloud_area_fraction_ml`
- `pressure_departure`
- `surface_air_pressure`
- `air_pressure_at_sea_level`
- `surface_geopotential`
- `land_area_fraction`
- `precipitation_amount_acc`
- `atmosphere_boundary_layer_thickness`
- Radiation: `toa_net_downward_shortwave_flux`, `toa_outgoing_longwave_flux`, `surface_downwelling_shortwave_flux_in_air`, `surface_downwelling_longwave_flux_in_air`

### 3b. Forecast Product Files (`fc[YYYYMMDDHH]_[NNN]_fp.nc`)

**Vertical coordinates:**
- Standard pressure levels (16 levels, `_pl` suffix variables)
- Specific height levels above ground: 10 m, and additional levels via `x_wind_z` / `y_wind_z`

**Key variables for wind power:**
- `x_wind_10m` / `y_wind_10m` — wind components at 10 m
- `x_wind_gust_10m` / `y_wind_gust_10m` — gusts at 10 m
- `x_wind_z` / `y_wind_z` — wind on height levels: **20, 50, 100, 250, 500, 750 m** (6 levels)
- `x_wind_pl` / `y_wind_pl` — wind on pressure levels: **50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000 hPa** (16 levels)
- `wind_speed` / `wind_direction`

**Other variables (~50 total):**
- Temperature: `air_temperature_0m`, `air_temperature_2m`, `air_temperature_pl`, `air_temperature_max`, `air_temperature_min`
- Pressure/geopotential: `air_pressure_at_sea_level`, `surface_air_pressure`, `geopotential_pl`
- Humidity: `relative_humidity_2m`, `relative_humidity_pl`, `specific_humidity_2m`, `lwe_thickness_of_atmosphere_mass_content_of_water_vapor`
- Cloud: `cloud_area_fraction`, `high_type_cloud_area_fraction`, `medium_type_cloud_area_fraction`, `low_type_cloud_area_fraction`, `convective_cloud_area_fraction`, `cloud_area_fraction_pl`
- Precipitation: `rainfall_amount`, `snowfall_amount`, `precipitation_amount_acc`, `snowfall_amount_acc`
- Radiation (accumulated integrals): shortwave and longwave, upwelling and downwelling, surface and TOA
- Heat fluxes: sensible, latent heat (evaporation + sublimation)
- Stability: `atmosphere_boundary_layer_thickness`, `lifting_condensation_level`, `atmosphere_level_of_free_convection`, `atmosphere_level_of_neutral_buoyancy`
- Momentum: `downward_northward_momentum_flux_in_air`, `downward_eastward_momentum_flux_in_air`
- `upward_air_velocity_pl`
- `hail_diagnostic`

### 3c. Surface Flux Files (`_sfx.nc` / `_full_sfx.nc`)

SURFEX land-surface model output. Primarily land/sea surface properties:
- Sea: `SST`, `SIC`, `Z0SEA`, 2 m variables over sea, energy fluxes over sea
- Soil: 3-layer temperature (`TG1–3`), liquid water content (`WG1–3`), ice content (`WGI1–3`)
- Vegetation: `LAI`, `VEG`, albedos
- Stability: `RI`, `RI_SEA` (Richardson number)

---

## NORA3-WP (Wind Power Subset)

Derived product from NORA3, specifically designed for wind resource assessment. Available at `https://archive.sigma2.no/dataset/482CC467-9E4F-4377-9E05-CB9822938D07`.

| Property | Value |
|---|---|
| Time coverage | 1996–2019 (extension to 1979 planned) |
| Domain | Eastern Norwegian Sea, North Sea, Baltic Sea, part of Barents Sea (smaller than full NORA3) |

**Vertical levels:** 101 m, 119 m, 150 m a.s.l. (turbine hub heights); wind shear layers at 10–100 m, 50–100 m, 100–250 m

**Variables (~25 total):**
- Wind speed at hub heights (101, 119, 150 m)
- Wind power for 3 reference turbines (6 MW, 10 MW, 15 MW)
- Air density-corrected power estimates
- Storm control options (SC1, SC2)
- Pre-computed monthly statistics: means, percentiles, Weibull parameters

---

## Summary Comparison Table

| Dataset | Time Coverage | Temporal Res. | Wind Height Levels | Key Wind Variables |
|---|---|---|---|---|
| Wind Hourly v2 (subset) | ~1970–2025 | 1h | 10, 20, 50, 100, 250, 500, 750 m | speed, direction |
| Atmospheric Hourly v2 (subset) | ~1970–present | 1h | 10 m only | speed, direction + other atm vars |
| Atmospheric 3-Hourly (subset) | — | 3h | 50, 100, 150, 200, 300 m | speed, direction, density, TKE |
| NORA3 Full (fp files) | 1958–present | 3h | 10 m + 20/50/100/250/500/750 m + 16 pressure levels | u/v components, speed, direction, gusts |
| NORA3 Full (ml files) | 1958–present | 3h | 65 hybrid model levels | u/v components (model levels) |
| NORA3-WP | 1996–2019 | Monthly stats | 101, 119, 150 m (hub heights) | speed, power, Weibull params |

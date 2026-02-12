---
title: Oceanum New Zealand GFS Wave Forecast
---

<style>
p { text-align: justify; }
img { display: block; margin-left: auto; margin-right: auto; }
table { margin-left: auto; margin-right: auto; }
</style>

<img src="./assets/oceanum-secondary-logo-marine-rgb-900px-w-72ppi.png" alt="Oceanum Logo" width="300">

<br><br>

# Oceanum New Zealand GFS Wave Forecast

**February 2025**

| | |
|---|---|
| **Model** | SWAN 41.31 |
| **Forecast horizon** | 7 days |
| **Spatial resolution** | 0.05 - 0.00025 degree (~5 km - 25 m) |
| **Temporal resolution** | 1 hourly |
| **Region** | 165E - 180E, 48S - 34S |
| **Forcings** | GFS winds and Oceanum spectra |
| **Update frequency** | 6-hourly |

---

## Dataset description

The New Zealand wave forecast dataset provides operational wave predictions across New Zealand's coastal waters and the surrounding Southwest Pacific Ocean (Figure 1). The forecast system comprises a hierarchy of nested domains: a regional 5 km parent grid covering all of New Zealand, with higher-resolution child grids for Auckland (1 km), Eastern Auckland (200 m), Taranaki (1 km), and Port Taranaki (25 m). Wave forecasts are produced using the SWAN (Simulating WAves Nearshore) third-generation spectral wave model, with a 7-day forecast horizon updated every 6 hours (00, 06, 12, 18 UTC).

Wind forcing is provided by <a href="https://www.ncep.noaa.gov/products/gfs/" target="_blank">NOAA GFS</a> global atmospheric model. Spectral boundary conditions are supplied by the Oceanum Global WW3 wave model forced with GFS winds. Bathymetry is derived from the <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/" target="_blank">GEBCO 2021</a> global bathymetric grid.

The modelling setup employs the <a href="https://journals.ametsoc.org/view/journals/atot/29/9/jtech-d-11-00092_1.xml" target="_blank">ST6</a> source term parameterisations. Spectra are discretised into 36 directional bins and 32 frequency bins, covering a frequency range from 0.037 to 0.71 Hz with 10% logarithmic increments. The parent grid features a 5 km (0.05 degree) resolution spanning New Zealand's Exclusive Economic Zone, with progressively finer nested grids for coastal applications.

The dataset provides hourly forecast estimates for key ocean wave parameters (Table 2) including spectral quantities integrated over the full spectrum and for spectral partitions. Partitions are defined from an 8-second split (sea/swell) and from the Watershed method, which identifies one wind-forced partition and up to three swell partitions. Forecasts are archived for 30 days, and frequency-direction wave spectra are available at selected sites across all domains. Nowcast datasets are also available, constructed by retaining the most recent data from each forecast cycle to provide a continuous near-real-time historical record.

<img src="./figures/nz_figure1_hs_mean.png" alt="Figure 1" width="600">

**Figure 1.** Mean significant wave height from the New Zealand hindcast domain (used for forecast validation). The locations of 2D spectra hourly output are shown by the black dots.

---

## Validation

The wave model physics and calibration have been validated against satellite altimeter observations for the corresponding hindcast domain. Validation results are available through the <a href="https://hindcast-satellite-validation-main-prod.apps.oceanum.io/" target="_blank">Oceanum Hindcast Satellite Validation App</a>, which provides density scatter plots, quantile comparisons, and statistical metrics for the New Zealand region.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum New Zealand wave forecast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://swanmodel.sourceforge.io/" target="_blank">SWAN 41.31A</a> |
| **Source terms** | <a href="https://journals.ametsoc.org/view/journals/atot/29/9/jtech-d-11-00092_1.xml" target="_blank">ST6</a> |
| **Forecast horizon** | 7 days |
| **Update frequency** | 6-hourly (GFS) |
| **Archive period** | 30 days |
| **Temporal resolution** | 1 hourly |
| **Frequency discretisation** | 32 frequencies between 0.037 - 0.71 Hz at 10% logarithmic increments |
| **Direction resolution** | 10 deg |
| **Bathymetry** | <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/" target="_blank">GEBCO 2021 Grid</a> |
| **Winds** | <a href="https://www.ncep.noaa.gov/products/gfs/" target="_blank">NOAA GFS</a> |
| **Boundary** | Oceanum Global WW3 wave forecast (GFS forced) |

### Nested domains

| Domain | Resolution | Coverage | Spectra sites |
|--------|------------|----------|---------------|
| New Zealand | 0.05° (~5 km) | 165E-180E, 48S-34S | 2390 |
| Auckland | 0.01° (~1 km) | Auckland region | 552 |
| Eastern Auckland | 0.002° (~200 m) | Eastern Auckland coast | - |
| Taranaki | 0.01° (~1 km) | Taranaki Bight | 22 |
| Port Taranaki | 0.00025° (~25 m) | Port Taranaki | - |

### Linked Datamesh datasources

**New Zealand 5km:**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_nz_grid" target="_blank">Oceanum New Zealand GFS wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_nz_spec" target="_blank">Oceanum New Zealand GFS wave forecast spectra</a>

**Auckland 1km:**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_akl1km_grid" target="_blank">Oceanum Auckland 1km GFS wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_akl1km_spec" target="_blank">Oceanum Auckland 1km GFS wave forecast spectra</a>

**Eastern Auckland 200m:**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_eakl_grid" target="_blank">Oceanum Eastern Auckland 200m GFS wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_eakl_spec" target="_blank">Oceanum Eastern Auckland 200m GFS wave forecast spectra</a>

**Taranaki 1km:**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_trki_grid" target="_blank">Oceanum Taranaki GFS wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_trki_spec" target="_blank">Oceanum Taranaki GFS wave forecast spectra</a>

**Port Taranaki 25m:**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_trkiport_grid" target="_blank">Oceanum Port Taranaki GFS wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_trkiport_spec" target="_blank">Oceanum Port Taranaki GFS wave forecast spectra</a>

**Nowcasts (continuous near-real-time archive):**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_nz_grid_nowcast" target="_blank">Oceanum New Zealand GFS wave nowcast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_gfs_nz_spec_nowcast" target="_blank">Oceanum New Zealand GFS wave nowcast spectra</a>

---

## Gridded output parameters

Integrated wave parameters are stored hourly over the domain at the native model resolution. Table 2 describes the gridded output parameters.

**Table 2.** Gridded output parameters.

| Variable | Long Name | Units |
|---|---|---|
| depth | depth below sea surface | m |
| hs | significant height of wind and swell waves | m |
| hs_sea | significant height of wind waves | m |
| hs_sw | significant height of swell waves | m |
| tps | smooth relative peak wave period of wind and swell waves | s |
| tps_sea | smooth relative peak wave period of wind waves | s |
| tps_sw | smooth relative peak wave period of swell waves | s |
| dpm | mean direction at the spectral peak of wind and swell waves | degree |
| dpm_sea | mean direction at the spectral peak of wind waves | degree |
| dpm_sw | mean direction at the spectral peak of swell waves | degree |
| tm01 | mean wave period based on first moment | s |
| tm02 | mean wave period based on second moment | s |
| dspr | directional spreading | degree |
| fspr | frequency spreading | - |
| phs0 | significant wave height of partition 0 (wind-forced) | m |
| phs1 | significant wave height of partition 1 (swell) | m |
| phs2 | significant wave height of partition 2 (swell) | m |
| phs3 | significant wave height of partition 3 (swell) | m |
| ptp0 | peak period of partition 0 (wind-forced) | s |
| ptp1 | peak period of partition 1 (swell) | s |
| ptp2 | peak period of partition 2 (swell) | s |
| ptp3 | peak period of partition 3 (swell) | s |
| pdir0 | peak direction of partition 0 (wind-forced) | degree |
| pdir1 | peak direction of partition 1 (swell) | degree |
| pdir2 | peak direction of partition 2 (swell) | degree |
| pdir3 | peak direction of partition 3 (swell) | degree |
| xwnd | eastward component of wind velocity | m/s |
| ywnd | northward component of wind velocity | m/s |

---

www.oceanum.science

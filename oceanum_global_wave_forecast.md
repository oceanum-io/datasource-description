---
title: Oceanum Global Wave Forecast
---

<style>
p { text-align: justify; }
img { display: block; margin-left: auto; margin-right: auto; }
table { margin-left: auto; margin-right: auto; }
</style>

<img src="./assets/oceanum-secondary-logo-marine-rgb-900px-w-72ppi.png" alt="Oceanum Logo" width="300">

<br><br>

# Oceanum Global Wave Forecast

**February 2025**

| | |
|---|---|
| **Model** | WAVEWATCH III 6.07 |
| **Forecast horizon** | 10 days |
| **Spatial resolution** | 0.5 degree (~50 km) |
| **Temporal resolution** | 1 hourly (spectra), 3 hourly (grid) |
| **Region** | Global (0E - 359.5E, 77.5S - 77.5N) |
| **Forcings** | GFS (6-hourly) / ECMWF (12-hourly) winds |

---

## Dataset description

The Oceanum global wave forecast provides 10-day predictions of wave conditions across all ocean basins (Figure 1). Wave fields are produced using the WAVEWATCH III (WW3) third-generation spectral wave model at 0.5-degree resolution. The forecast is run operationally with both GFS (updated 6-hourly) and ECMWF (updated 12-hourly) atmospheric forcing.

Wind forcing is provided by <a href="https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast" target="_blank">NOAA GFS</a> at 0.25-degree resolution or <a href="https://www.ecmwf.int/en/forecasts/datasets/open-data" target="_blank">ECMWF IFS</a> at 0.25-degree resolution. Sea ice concentration is obtained from GFS for both model configurations. Bathymetry is derived from <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/" target="_blank">GEBCO 2020</a>.

The modelling setup employs the ST4 source term parameterisations with calibrated parameters for global wave climate representation. Spectra are discretised into 24 directional bins and 31 frequency bins, covering a frequency range from 0.037 to 0.71 Hz with 10% logarithmic increments.

The dataset provides hourly estimates for key ocean wave parameters (Table 2) including spectral quantities integrated over the full spectrum and for spectral partitions. Partitions are defined from an 8-second split (sea/swell) and from the Watershed method, which identifies one wind-sea partition and up to four swell partitions. Frequency-direction wave spectra are available at strategically selected sites worldwide (black dots in Figure 1). Nowcast datasources are also provided, constructed from the most recent data in each forecast cycle to form continuous time series.

The global forecast is well suited for deep water wave predictions anywhere on the planet. A key application is providing directional spectral boundary conditions for downscaling regional and coastal wave models. The spectra output network is designed with variable density, ranging from 2 degrees in deep water to 0.5 degrees near coastlines, ensuring appropriate resolution for boundary forcing across diverse modelling applications. The spectral data is optimised for very fast access (seconds to a few minutes), enabling efficient operational workflows.

<img src="./figures/glob05_figure1_hs_mean.png" alt="Figure 1" width="800">

**Figure 1.** Mean significant wave height (Hs) over the global domain from the Oceanum ERA5 wave hindcast (1979-2020). Black dots indicate spectra output locations.

---

## Validation

The global wave model configuration has been validated against satellite altimeter observations from multiple missions including Jason-2, Jason-3, Sentinel-3A, and Sentinel-3B. Validation statistics demonstrate excellent agreement with observed wave heights across all ocean basins. Detailed validation results are available in the <a href="https://datasets.oceanum.io/oceanum_global_wave_hindcast_specification.pdf" target="_blank">hindcast specification document</a>.

Interactive validation results are available through the <a href="https://validation.oceanum.io" target="_blank">Oceanum Validation App</a>.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum global wave forecast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://github.com/NOAA-EMC/WW3" target="_blank">WAVEWATCH III 6.07</a> |
| **Source terms** | ST4 |
| **Forecast horizon** | 10 days |
| **Temporal resolution** | 1 hourly (spectra), 3 hourly (grid) |
| **Spatial coverage** | Global (0E - 359.5E, 77.5S - 77.5N) at 0.5 degree |
| **Frequency discretisation** | 31 frequencies between 0.037 - 0.71 Hz at 10% logarithmic increments |
| **Direction resolution** | 15 deg |
| **Bathymetry** | <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/" target="_blank">GEBCO 2020</a> |
| **Winds (GFS)** | <a href="https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast" target="_blank">NOAA GFS</a> (6-hourly updates) |
| **Winds (ECMWF)** | <a href="https://www.ecmwf.int/en/forecasts/datasets/open-data" target="_blank">ECMWF IFS</a> (12-hourly updates) |
| **Sea ice** | GFS sea ice concentration |

### Linked Datamesh datasources

#### GFS Forced

- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_glob05_gfs_grid" target="_blank">Oceanum global GFS wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_glob05_gfs_spec" target="_blank">Oceanum global GFS wave forecast spectra</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_glob05_gfs_grid_nowcast" target="_blank">Oceanum global GFS wave nowcast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_glob05_gfs_spec_nowcast" target="_blank">Oceanum global GFS wave nowcast spectra</a>

#### ECMWF Forced

- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_glob05_ec_grid" target="_blank">Oceanum global ECMWF wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_glob05_ec_spec" target="_blank">Oceanum global ECMWF wave forecast spectra</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_glob05_grid_nowcast" target="_blank">Oceanum global ECMWF wave nowcast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_glob05_spec_nowcast" target="_blank">Oceanum global ECMWF wave nowcast spectra</a>

#### Related Hindcast

- <a href="https://datasets.oceanum.io/oceanum_global_wave_hindcast.html" target="_blank">Oceanum global ERA5 wave hindcast</a>

---

## Integrated parameters gridded output

Integrated wave parameters are stored 3-hourly over the domain at the native model resolution. Table 2 describes long names and units of key gridded output parameters.

**Table 2.** Gridded output parameters.

| Variable | Long Name | Units |
|---|---|---|
| dpt | depth below sea surface | m |
| hs | significant height of wind and swell waves | m |
| lm | mean wave length | m |
| t02 | mean wave period (Tm0,2) | s |
| fp | peak frequency | Hz |
| dir | mean wave direction | degree |
| spr | mean directional spread | degree |
| dp | peak wave direction | degree |
| phs0 | significant height of wind waves (partition 0) | m |
| phs1 | significant height of primary swell waves (partition 1) | m |
| phs2 | significant height of secondary swell waves (partition 2) | m |
| phs3 | significant height of tertiary swell waves (partition 3) | m |
| phs4 | significant height of quaternary swell waves (partition 4) | m |
| ptp0 | peak period of wind waves (partition 0) | s |
| ptp1 | peak period of primary swell waves (partition 1) | s |
| ptp2 | peak period of secondary swell waves (partition 2) | s |
| ptp3 | peak period of tertiary swell waves (partition 3) | s |
| ptp4 | peak period of quaternary swell waves (partition 4) | s |
| pt020 | mean period (Tm0,2) of wind waves (partition 0) | s |
| pt021 | mean period (Tm0,2) of primary swell waves (partition 1) | s |
| pt022 | mean period (Tm0,2) of secondary swell waves (partition 2) | s |
| pt023 | mean period (Tm0,2) of tertiary swell waves (partition 3) | s |
| pt024 | mean period (Tm0,2) of quaternary swell waves (partition 4) | s |
| pdir0 | mean direction of wind waves (partition 0) | degree |
| pdir1 | mean direction of primary swell waves (partition 1) | degree |
| pdir2 | mean direction of secondary swell waves (partition 2) | degree |
| pdir3 | mean direction of tertiary swell waves (partition 3) | degree |
| pdir4 | mean direction of quaternary swell waves (partition 4) | degree |
| pdp0 | peak direction of wind waves (partition 0) | degree |
| pdp1 | peak direction of primary swell waves (partition 1) | degree |
| pdp2 | peak direction of secondary swell waves (partition 2) | degree |
| pdp3 | peak direction of tertiary swell waves (partition 3) | degree |
| pdp4 | peak direction of quaternary swell waves (partition 4) | degree |
| pws0 | wind sea fraction of partition 0 | - |
| pws1 | wind sea fraction of partition 1 | - |
| pws2 | wind sea fraction of partition 2 | - |
| pws3 | wind sea fraction of partition 3 | - |
| pws4 | wind sea fraction of partition 4 | - |
| wnd | wind speed at 10m | m/s |
| ice | sea ice concentration | - |

---

www.oceanum.science

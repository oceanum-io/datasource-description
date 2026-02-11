<style>
p { text-align: justify; }
img { display: block; margin-left: auto; margin-right: auto; }
table { margin-left: auto; margin-right: auto; }
</style>

# Oceanum Baltic Sea Wave Forecast Specification

**February 2025**

| | |
|---|---|
| **Model** | SWAN 41.31 |
| **Forecast horizon** | 7 days |
| **Spatial resolution** | 0.05 degree (~5 km) |
| **Temporal resolution** | 1 hourly |
| **Region** | 9E - 30.3E, 53.8N - 66N |
| **Forcings** | ECMWF winds, sea ice, and Oceanum spectra |
| **Update frequency** | 12-hourly |

---

## Dataset description

The Baltic Sea wave forecast dataset provides operational wave predictions across the entire Baltic Sea basin, including the Gulf of Bothnia, Gulf of Finland, Gulf of Riga, and the Danish Straits (Figure 1). The domain encompasses the coastal waters of Sweden, Finland, Estonia, Latvia, Lithuania, Poland, Germany, and Denmark. Wave forecasts are produced using the SWAN (Simulating WAves Nearshore) third-generation spectral wave model, with a 7-day forecast horizon updated every 12 hours (00, 12 UTC).

Wind forcing is provided by <a href="https://www.ecmwf.int/en/forecasts/datasets/open-data" target="_blank">ECMWF IFS Open Data</a> global atmospheric model. Sea ice concentration is prescribed from GFS to account for wave attenuation in ice-covered regions during winter months. Spectral boundary conditions are supplied by the <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_weuro_grid" target="_blank">Oceanum Western Europe ECMWF wave forecast</a>. Bathymetry is derived from the <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/" target="_blank">GEBCO 2024</a> global bathymetric grid.

The modelling setup employs the <a href="https://journals.ametsoc.org/view/journals/atot/29/9/jtech-d-11-00092_1.xml" target="_blank">ST6</a> source term parameterisations. Spectra are discretised into 36 directional bins and 43 frequency bins, covering a frequency range from 0.037 to 1.98 Hz with 10% logarithmic increments, extending to higher frequencies to capture the short-period wind waves characteristic of the enclosed Baltic Sea. The model features a regular grid with a 5 km (0.05 degree) resolution.

The dataset provides hourly forecast estimates for key ocean wave parameters (Table 2) including spectral quantities integrated over the full spectrum and for spectral partitions. Partitions are defined from an 8-second split (sea/swell) and from the Watershed method, which identifies one wind-forced partition and up to two swell partitions. Forecasts are archived for 30 days, and frequency-direction wave spectra are available at 1610 sites distributed across the domain. Nowcast datasets are also available, constructed by retaining the most recent data from each forecast cycle to provide a continuous near-real-time historical record.

<img src="./figures/baltic_nora3_figure1_hs_mean.png" alt="Figure 1" width="600">

**Figure 1.** Mean significant wave height from the Baltic Sea hindcast domain (used for forecast validation). The locations of 2D spectra hourly output are shown by the black dots.

---

## Validation

The wave model physics and calibration have been validated against satellite altimeter observations for the corresponding hindcast domain. Validation results are available through the <a href="https://hindcast-satellite-validation-main-prod.apps.oceanum.io/" target="_blank">Oceanum Hindcast Satellite Validation App</a>, which provides density scatter plots, quantile comparisons, and statistical metrics for the Baltic Sea region.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum Baltic Sea wave forecast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://swanmodel.sourceforge.io/" target="_blank">SWAN 41.31A</a> |
| **Source terms** | <a href="https://journals.ametsoc.org/view/journals/atot/29/9/jtech-d-11-00092_1.xml" target="_blank">ST6</a> |
| **Forecast horizon** | 7 days |
| **Update frequency** | 12-hourly (ECMWF) |
| **Archive period** | 30 days |
| **Temporal resolution** | 1 hourly |
| **Spatial coverage** | [9E, 53.8N, 30.3E, 66N] at 0.05 degree |
| **Spectra output sites** | 1610 |
| **Frequency discretisation** | 43 frequencies between 0.037 - 1.98 Hz at 10% logarithmic increments |
| **Direction resolution** | 10 deg |
| **Bathymetry** | <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/" target="_blank">GEBCO 2024 Grid</a> |
| **Winds** | <a href="https://www.ecmwf.int/en/forecasts/datasets/open-data" target="_blank">ECMWF IFS</a> |
| **Sea ice** | <a href="https://www.ncep.noaa.gov/products/gfs/" target="_blank">NOAA GFS</a> |
| **Boundary** | <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_weuro_grid" target="_blank">Oceanum Western Europe ECMWF wave forecast</a> |

### Linked Datamesh datasources

**ECMWF-forced (12-hourly updates):**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_baltic_grid" target="_blank">Oceanum Baltic Sea ECMWF wave forecast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_baltic_spec" target="_blank">Oceanum Baltic Sea ECMWF wave forecast spectra</a>

**Nowcasts (continuous near-real-time archive):**
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_baltic_grid_nowcast" target="_blank">Oceanum Baltic Sea ECMWF wave nowcast parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_ec_baltic_spec_nowcast" target="_blank">Oceanum Baltic Sea ECMWF wave nowcast spectra</a>

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
| aice | sea ice concentration | - |
| phs0 | significant wave height of partition 0 (wind-forced) | m |
| phs1 | significant wave height of partition 1 (swell) | m |
| phs2 | significant wave height of partition 2 (swell) | m |
| ptp0 | peak period of partition 0 (wind-forced) | s |
| ptp1 | peak period of partition 1 (swell) | s |
| ptp2 | peak period of partition 2 (swell) | s |
| pdir0 | peak direction of partition 0 (wind-forced) | degree |
| pdir1 | peak direction of partition 1 (swell) | degree |
| pdir2 | peak direction of partition 2 (swell) | degree |
| xwnd | eastward component of wind velocity | m/s |
| ywnd | northward component of wind velocity | m/s |

---

www.oceanum.science

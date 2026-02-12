---
title: Oceanum Baltic Sea NORA3 Wave Hindcast
---

<style>
p { text-align: justify; }
img { display: block; margin-left: auto; margin-right: auto; }
table { margin-left: auto; margin-right: auto; }
</style>

<img src="./assets/oceanum-secondary-logo-marine-rgb-900px-w-72ppi.png" alt="Oceanum Logo" width="300">

<br><br>

# Oceanum Baltic Sea NORA3 Wave Hindcast

**February 2025**

| | |
|---|---|
| **Model** | SWAN 41.31 |
| **Period** | Feb 1979 - Updating |
| **Spatial resolution** | 5 km (0.05 degree) |
| **Temporal resolution** | 1 hourly |
| **Region** | 9E - 30.3E, 53.8N - 66N |
| **Forcings** | NORA3 winds, sea ice, and Oceanum spectra |

---

## Dataset description

The Baltic Sea NORA3 wave hindcast dataset provides a detailed account of ocean wave parameters across the Baltic Sea and its sub-basins (Figure 1). The domain encompasses the entire Baltic Sea including the Gulf of Bothnia, Gulf of Finland, Gulf of Riga, and the Danish Straits connecting to the North Sea. This semi-enclosed sea experiences a unique wave climate characterised by fetch-limited conditions, seasonal ice cover, and complex coastline geometry. Wave spectra are computed over a 45+ year period between 1979 and present using the SWAN (Simulating WAves Nearshore) third-generation spectral wave model.

This hindcast is distinguished by its use of the high-resolution <a href="https://thredds.met.no/thredds/catalog/nora3/catalog.html" target="_blank">NORA3 reanalysis winds</a> from the Norwegian Meteorological Institute, which provides superior representation of coastal wind patterns compared to global reanalyses. The model also includes sea ice concentration from <a href="https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5" target="_blank">ERA5 reanalysis</a> to account for wave attenuation in ice-covered areas during winter months. Spectral boundaries are provided by the <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_weuro_era5_v1_spec" target="_blank">Oceanum Western Europe Wave Model</a>. Bathymetry is derived from the <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/gebco_2024/" target="_blank">GEBCO 2024</a> global bathymetric grid.

The modelling setup employs the <a href="https://journals.ametsoc.org/view/journals/atot/29/9/jtech-d-11-00092_1.xml" target="_blank">ST6</a> source term parameterisations. Spectra are discretised into 36 directional bins and 43 frequency bins, covering a frequency range from 0.037 to 2.03 Hz with 10% logarithmic increments. The extended frequency range captures the short-period wind waves characteristic of fetch-limited seas. The model features a regular grid with a 5 km (0.05 degree) resolution, providing detailed wave information for the Baltic Sea region.

The dataset provides hourly estimates for an extensive array of ocean wave parameters (Table 2) including spectral quantities integrated over the full spectrum and for spectral partitions. Partitions are defined from an 8-second split (sea/swell) and from the Watershed method, which identifies one wind-forced partition and up to two swell partitions. These data are stored over the entire grid at native resolution. Additionally, frequency-direction wave spectra are available at 1610 sites distributed across the domain (see Figure 1).

<img src="./figures/baltic_nora3_figure1_hs_mean.png" alt="Figure 1" width="500">

**Figure 1.** Mean significant wave height from the Baltic Sea NORA3 hindcast domain. The locations of 2D spectra hourly output are shown by the black dots. Depth contours are shown at 20m, 50m, 100m, and 200m.

---

## Validation

The wave hindcast can be validated against satellite altimeter observations using the <a href="https://hindcast-satellite-validation-main-prod.apps.oceanum.io/" target="_blank">Oceanum Hindcast Satellite Validation App</a>. This interactive tool allows users to compare modelled significant wave height against satellite altimeter measurements at any location within the model domain, providing density scatter plots, quantile comparisons, and statistical metrics.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum Baltic Sea NORA3 wave hindcast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://swanmodel.sourceforge.io/" target="_blank">SWAN 41.31A</a> |
| **Source terms** | <a href="https://journals.ametsoc.org/view/journals/atot/29/9/jtech-d-11-00092_1.xml" target="_blank">ST6</a> |
| **Temporal coverage** | 1979-02-01 to present (updating) |
| **Temporal resolution** | 1 hourly |
| **Spatial coverage** | [9E, 53.8N, 30.3E, 66N] at 0.05 degree |
| **Spectra output sites** | 1610 |
| **Frequency discretisation** | 43 frequencies between 0.037 - 2.03 Hz at 10% logarithmic increments |
| **Direction resolution** | 10 deg |
| **Bathymetry** | <a href="https://www.gebco.net/data_and_products/gridded_bathymetry_data/gebco_2024/" target="_blank">GEBCO 2024 Grid</a> |
| **Winds** | <a href="https://thredds.met.no/thredds/catalog/nora3/catalog.html" target="_blank">NORA3 Reanalysis</a> |
| **Sea ice** | <a href="https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5" target="_blank">ERA5 Reanalysis</a> (sea ice concentration) |
| **Boundary** | <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_weuro_era5_v1_spec" target="_blank">Oceanum Western Europe ERA5 3-hourly wave spectra</a> |

### Linked Datamesh datasources

- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_baltic_nora3_grid" target="_blank">Oceanum Baltic Sea NORA3 5 km hourly wave parameters</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_baltic_nora3_spec" target="_blank">Oceanum Baltic Sea NORA3 5 km hourly wave spectra</a>
- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_wave_baltic_nora3_gridstats" target="_blank">Oceanum Baltic Sea NORA3 5 km gridded wave statistics</a>

---

## Integrated parameters gridded output

Integrated wave parameters are stored hourly over the domain at the native model resolution. Table 2 describes long names and units of the 35 gridded output parameters, including one wind-forced partition and two swell partitions from the Watershed method.

**Table 2.** Gridded output parameters.

| Variable | Long Name | Units |
|---|---|---|
| aice | sea ice area fraction | - |
| depth | depth below sea surface | m |
| dpm | mean direction at the spectral peak of wind and swell waves | degree |
| dpmsea | mean direction at the spectral peak of wind waves below 8 seconds period | degree |
| dpmswe | mean direction at the spectral peak of swell waves above 8 seconds period | degree |
| dspr | directional spreading of wind and swell waves | degree |
| fspr | normalised width of the frequency spectrum of wind and swell waves | - |
| hs | significant height of wind and swell waves | m |
| hsea | significant height of wind waves under 8 seconds period | m |
| hswe | significant height of swell waves above 8 seconds period | m |
| pdir0 | mean direction of wind waves (partition 0) | degree |
| pdir1 | mean direction of primary swell waves (partition 1) | degree |
| pdir2 | mean direction of secondary swell waves (partition 2) | degree |
| pdspr0 | directional spreading of wind waves (partition 0) | degree |
| pdspr1 | directional spreading of primary swell waves (partition 1) | degree |
| pdspr2 | directional spreading of secondary swell waves (partition 2) | degree |
| phs0 | significant height of wind waves (partition 0) | m |
| phs1 | significant height of primary swell waves (partition 1) | m |
| phs2 | significant height of secondary swell waves (partition 2) | m |
| ptp0 | peak period of wind waves (partition 0) | s |
| ptp1 | peak period of primary swell waves (partition 1) | s |
| ptp2 | peak period of secondary swell waves (partition 2) | s |
| pwlen0 | mean wavelength of wind waves (partition 0) | m |
| pwlen1 | mean wavelength of primary swell waves (partition 1) | m |
| pwlen2 | mean wavelength of secondary swell waves (partition 2) | m |
| tm01 | mean absolute wave period of wind and swell waves from the first frequency moment | s |
| tm02 | mean absolute wave period of wind and swell waves from the second frequency moment | s |
| tps | smooth relative peak wave period of wind and swell waves | s |
| tpssea | smooth relative peak wave period of wind waves below 8 seconds period | s |
| tpsswe | smooth relative peak wave period of swell waves above 8 seconds period | s |
| ucur | eastward component of current velocity | m/s |
| vcur | northward component of current velocity | m/s |
| xwnd | eastward component of wind velocity | m/s |
| ywnd | northward component of wind velocity | m/s |

---

www.oceanum.science

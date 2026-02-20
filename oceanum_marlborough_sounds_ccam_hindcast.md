---
title: Oceanum Marlborough Sounds CCAM Atmospheric Hindcast
---

<style>
p { text-align: justify; }
img { display: block; margin-left: auto; margin-right: auto; }
table { margin-left: auto; margin-right: auto; }
</style>

<img src="./assets/oceanum-secondary-logo-marine-rgb-900px-w-72ppi.png" alt="Oceanum Logo" width="300">

<br><br>

# Oceanum Marlborough Sounds CCAM Atmospheric Hindcast

**February 2025**

| | |
|---|---|
| **Model** | CCAM |
| **Period** | Jan 2017 - Jun 2024 |
| **Spatial resolution** | 0.01 degree (~1 km) |
| **Temporal resolution** | 1 hourly |
| **Region** | 173.23E - 174.75E, 41.65S - 40.50S |
| **Forcing** | ERA5 reanalysis |

---

## Dataset description

The Marlborough Sounds CCAM atmospheric hindcast provides very high-resolution meteorological data over the Marlborough Sounds region at the northern tip of New Zealand's South Island (Figure 1). The domain encompasses the intricate network of drowned river valleys that form the Sounds, including Queen Charlotte Sound, Pelorus Sound, and Kenepuru Sound, as well as the adjacent Cook Strait waters. This region features some of New Zealand's most complex coastal topography, with steep-sided valleys and narrow waterways that strongly influence local wind patterns.

The dataset is produced using the <a href="https://www.ccrc.unsw.edu.au/ccam" target="_blank">Conformal Cubic Atmospheric Model (CCAM)</a>, a variable-resolution global atmospheric model developed by CSIRO. CCAM employs dynamical downscaling to simulate climate and weather at fine spatial resolutions while maintaining interaction with global circulation patterns. The model is forced by <a href="https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5" target="_blank">ERA5 reanalysis</a> from the European Centre for Medium-Range Weather Forecasts, providing consistent and accurate large-scale atmospheric forcing.

The very high 1 km resolution enables detailed representation of the complex fjord-like topography of Marlborough Sounds and its influence on local wind patterns. Key features captured include wind channelling through the sounds, katabatic (downslope) winds draining from surrounding hills, sea breeze circulations, and the interaction with Cook Strait wind acceleration. The model provides atmospheric variables at three height levels (10m, 80m, and 150m), enabling vertical profiling of the atmospheric boundary layer.

The dataset provides hourly estimates for a comprehensive suite of atmospheric variables (Table 2) including wind components at multiple heights, temperature, humidity, pressure fields, cloud properties, precipitation, and solar radiation (DNI). This dataset is suitable for applications including wind resource assessment, marine operations planning, air quality modelling, and as atmospheric forcing for regional ocean models such as the Oceanum Marlborough Sounds SCHISM ocean hindcast.

<img src="./figures/marlborough_sounds_ccam_figure1_domain.png" alt="Figure 1" width="600">

**Figure 1.** Marlborough Sounds CCAM atmospheric hindcast domain extent. The model covers the Marlborough Sounds and adjacent Cook Strait waters at 1km resolution.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum Marlborough Sounds CCAM atmospheric hindcast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://www.ccrc.unsw.edu.au/ccam" target="_blank">CCAM (Conformal Cubic Atmospheric Model)</a> |
| **Temporal coverage** | 2017-01-01 to 2024-06-01 |
| **Temporal resolution** | 1 hourly |
| **Spatial coverage** | [173.23E, 41.65S, 174.75E, 40.50S] at 0.01 degree (~1 km) |
| **Vertical levels** | 10m, 80m, 150m |
| **Forcing** | <a href="https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5" target="_blank">ERA5 reanalysis</a> |

### Linked Datamesh datasources

- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_meteo_ms_ccam_v1" target="_blank">Oceanum Marlborough Sounds meteo hindcast</a>

---

## Output parameters

Atmospheric variables are stored hourly over the domain at the native model resolution. Table 2 describes the key output parameters.

**Table 2.** Output parameters.

| Variable | Long Name | Units |
|---|---|---|
| cfrac | cloud fraction | - |
| clh | high cloud cover | % |
| cll | low cloud cover | % |
| clm | mid cloud cover | % |
| clt | total cloud cover | % |
| dni | direct normal irradiance | W/m² |
| hus | water vapour mixing ratio | kg/kg |
| huss | screen mixing ratio | kg/kg |
| orog | surface height | m |
| pr | precipitation | kg/m²/s |
| prc | convective precipitation | kg/m²/s |
| press | air pressure | hPa |
| prmax | maximum precipitation rate in a timestep | kg/m²/s |
| ps | surface pressure | Pa |
| psl | mean sea level pressure | Pa |
| rlds | LW downwelling at ground | W/m² |
| rnet | net radiation at surface | W/m² |
| rsds | SW downwelling at ground | W/m² |
| sgn_ave | SW net at ground | W/m² |
| ta | air temperature | K |
| td | dew point temperature | K |
| ts | surface temperature | K |
| tsea | sea surface temperature | K |
| u10max | x-component max 10m wind | m/s |
| ua | zonal wind | m/s |
| uas | x-component 10m wind | m/s |
| va | meridional wind | m/s |
| vas | y-component 10m wind | m/s |
| zg | geopotential height | m |
| zmla | PBL depth | m |
| zolnd | surface roughness | m |

---

www.oceanum.science

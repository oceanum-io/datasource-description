---
title: Oceanum Central New Zealand CCAM Atmospheric Hindcast
---

<img src="./assets/oceanum-secondary-logo-marine-rgb-900px-w-72ppi.png" alt="Oceanum Logo" width="300">

<br><br>

# Oceanum Central New Zealand CCAM Atmospheric Hindcast

**February 2025**

| | |
|---|---|
| **Model** | CCAM |
| **Period** | Jan 1999 - Jan 2020 |
| **Spatial resolution** | 0.04 degree (~4 km) |
| **Temporal resolution** | 1 hourly |
| **Region** | 172.08E - 175.92E, 42.22S - 38.38S |
| **Forcing** | ERA5 reanalysis |

---

## Dataset description

The Central New Zealand CCAM atmospheric hindcast provides high-resolution meteorological data over the central North Island and Cook Strait region of New Zealand (Figure 1). The domain encompasses the lower North Island including Wellington, the Wairarapa, Taranaki, and Manawatu-Whanganui regions, as well as the northern South Island including Marlborough and Nelson. This strategically important area includes Cook Strait, one of the most meteorologically complex regions in New Zealand due to the funnelling of winds between the two main islands.

The dataset is produced using the <a href="https://www.ccrc.unsw.edu.au/ccam" target="_blank">Conformal Cubic Atmospheric Model (CCAM)</a>, a variable-resolution global atmospheric model developed by CSIRO. CCAM employs dynamical downscaling to simulate climate and weather at fine spatial resolutions while maintaining interaction with global circulation patterns. The model is forced by <a href="https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5" target="_blank">ERA5 reanalysis</a> from the European Centre for Medium-Range Weather Forecasts, providing consistent and accurate large-scale atmospheric forcing.

The 4 km resolution enables accurate representation of New Zealand's complex topography and its influence on local atmospheric processes. Key features captured include orographic effects from the Tararua and Rimutaka ranges, sea breeze circulations, terrain-induced flow modifications, and the acceleration of winds through Cook Strait. The model provides multi-level atmospheric variables at six height levels (10m, 20m, 40m, 100m, 150m, 200m), enabling detailed vertical profiling of the atmospheric boundary layer.

The dataset provides hourly estimates for a comprehensive suite of atmospheric variables (Table 2) including wind components at multiple heights, temperature, humidity, pressure fields, cloud properties, and precipitation. Derived variables for wind speed are also available. This dataset is suitable for applications including wind resource assessment, renewable energy planning, air quality modelling, and as atmospheric forcing for regional ocean and wave models.

<img src="./figures/central_nz_ccam_figure1_domain.png" alt="Figure 1" width="600">

**Figure 1.** Central New Zealand CCAM atmospheric hindcast domain extent. The model covers the lower North Island, Cook Strait, and northern South Island at 4km resolution.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum Central New Zealand CCAM atmospheric hindcast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://www.ccrc.unsw.edu.au/ccam" target="_blank">CCAM (Conformal Cubic Atmospheric Model)</a> |
| **Temporal coverage** | 1999-01-01 to 2020-01-01 |
| **Temporal resolution** | 1 hourly |
| **Spatial coverage** | [172.08E, 42.22S, 175.92E, 38.38S] at 0.04 degree (~4 km) |
| **Vertical levels** | 10m, 20m, 40m, 100m, 150m, 200m |
| **Forcing** | <a href="https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5" target="_blank">ERA5 reanalysis</a> |

### Linked Datamesh datasources

- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_meteo_central_nz_ccam_v1" target="_blank">Oceanum Central NZ CCAM meteo hindcast</a>

---

## Output parameters

Atmospheric variables are stored hourly over the domain at the native model resolution. Table 2 describes the key output parameters.

**Table 2.** Output parameters.

*Variable names link to the corresponding <a href="https://vocab.nerc.ac.uk/standard_name/" target="_blank">NERC Vocabulary Server</a> standard name where available.*

| Variable | Long Name | Units |
|---|---|---|
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_base_altitude/" target="_blank">cbas_ave</a> | average cloud base | sigma |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction/" target="_blank">cfrac</a> | cloud fraction | - |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction_in_atmosphere_layer/" target="_blank">clh</a> | high cloud cover | % |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction_in_atmosphere_layer/" target="_blank">cll</a> | low cloud cover | % |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction_in_atmosphere_layer/" target="_blank">clm</a> | mid cloud cover | % |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction/" target="_blank">clt</a> | total cloud cover | % |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_top_altitude/" target="_blank">ctop_ave</a> | average cloud top | sigma |
| <a href="https://vocab.nerc.ac.uk/standard_name/specific_humidity/" target="_blank">hus</a> | water vapour mixing ratio | kg/kg |
| <a href="https://vocab.nerc.ac.uk/standard_name/humidity_mixing_ratio/" target="_blank">huss</a> | screen mixing ratio | kg/kg |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_altitude/" target="_blank">orog</a> | surface height | m |
| <a href="https://vocab.nerc.ac.uk/standard_name/precipitation_flux/" target="_blank">pr</a> | precipitation | kg/m²/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/convective_precipitation_flux/" target="_blank">prc</a> | convective precipitation | kg/m²/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/air_pressure/" target="_blank">press</a> | air pressure | hPa |
| <a href="https://vocab.nerc.ac.uk/standard_name/precipitation_flux/" target="_blank">prhmax</a> | maximum hourly precip rate | kg/m²/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/precipitation_flux/" target="_blank">prmax</a> | maximum precipitation rate in a timestep | kg/m²/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_air_pressure/" target="_blank">ps</a> | surface pressure | Pa |
| <a href="https://vocab.nerc.ac.uk/standard_name/air_pressure_at_mean_sea_level/" target="_blank">psl</a> | mean sea level pressure | Pa |
| <a href="https://vocab.nerc.ac.uk/standard_name/relative_humidity/" target="_blank">rh</a> | relative humidity | % |
| <a href="https://vocab.nerc.ac.uk/standard_name/air_temperature/" target="_blank">ta</a> | air temperature | K |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_downward_eastward_stress/" target="_blank">tauu</a> | zonal wind stress | N/m² |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_downward_northward_stress/" target="_blank">tauv</a> | meridional wind stress | N/m² |
| <a href="https://vocab.nerc.ac.uk/standard_name/dew_point_temperature/" target="_blank">td</a> | dew point temperature | K |
| <a href="https://vocab.nerc.ac.uk/standard_name/air_potential_temperature/" target="_blank">theta</a> | potential air temperature | K |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_temperature/" target="_blank">ts</a> | surface temperature | K |
| <a href="https://vocab.nerc.ac.uk/standard_name/sea_surface_temperature/" target="_blank">tsea</a> | sea surface temperature | K |
| <a href="https://vocab.nerc.ac.uk/standard_name/wind_speed_of_gust/" target="_blank">u10max</a> | x-component max 10m wind | m/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/eastward_wind/" target="_blank">ua</a> | zonal wind | m/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/eastward_wind/" target="_blank">uas</a> | x-component 10m wind | m/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/northward_wind/" target="_blank">va</a> | meridional wind | m/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/northward_wind/" target="_blank">vas</a> | y-component 10m wind | m/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/geopotential_height/" target="_blank">zg</a> | geopotential height | m |
| <a href="https://vocab.nerc.ac.uk/standard_name/atmosphere_boundary_layer_thickness/" target="_blank">zmla</a> | PBL depth | m |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_roughness_length/" target="_blank">zolnd</a> | surface roughness | m |

### Derived variables

| Variable | Long Name | Units |
|---|---|---|
| <a href="https://vocab.nerc.ac.uk/standard_name/wind_speed/" target="_blank">wspd</a> | wind speed (from ua, va) | m/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/wind_speed/" target="_blank">wspdsfc</a> | surface wind speed (from uas, vas) | m/s |

---

www.oceanum.science

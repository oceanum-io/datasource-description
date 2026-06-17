---
title: Oceanum Taranaki New Zealand CCAM Atmospheric Hindcast
---

<img src="./assets/oceanum-secondary-logo-marine-rgb-900px-w-72ppi.png" alt="Oceanum Logo" width="300">

<br><br>

# Oceanum Taranaki New Zealand CCAM Atmospheric Hindcast

**February 2025**

| | |
|---|---|
| **Model** | CCAM |
| **Period** | Jan 2010 - Jan 2020 |
| **Spatial resolution** | 0.01 degree (~1 km) |
| **Temporal resolution** | 1 hourly |
| **Region** | 172.99E - 175.23E, 40.15S - 38.43S |
| **Forcing** | ERA5 reanalysis |

---

## Dataset description

The Taranaki New Zealand CCAM atmospheric hindcast provides very high-resolution meteorological data over the Taranaki region of New Zealand's North Island (Figure 1). The domain encompasses the Taranaki peninsula including Mount Taranaki (Egmont), the surrounding coastal waters of the North and South Taranaki Bights, and extends inland to capture the complex terrain interactions. Mount Taranaki's isolated volcanic cone (2,518 m) creates distinctive local wind patterns that are well-resolved at this resolution.

The dataset is produced using the <a href="https://www.ccrc.unsw.edu.au/ccam" target="_blank">Conformal Cubic Atmospheric Model (CCAM)</a>, a variable-resolution global atmospheric model developed by CSIRO. CCAM employs dynamical downscaling to simulate climate and weather at fine spatial resolutions while maintaining interaction with global circulation patterns. The model is forced by <a href="https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5" target="_blank">ERA5 reanalysis</a> from the European Centre for Medium-Range Weather Forecasts, providing consistent and accurate large-scale atmospheric forcing.

The very high 1 km resolution enables detailed representation of Mount Taranaki's volcanic cone and its significant influence on local wind patterns. Key features captured include flow separation around the mountain, lee effects and wake turbulence, thermally-driven circulations (anabatic and katabatic winds), and orographic cloud formation. The model provides atmospheric variables at three height levels (10m, 80m, and 150m), enabling vertical profiling relevant for wind energy applications.

The dataset provides hourly estimates for a comprehensive suite of atmospheric variables (Table 2) including wind components at multiple heights, temperature, humidity, pressure fields, cloud properties, precipitation, and solar radiation (DNI). This dataset is particularly suitable for wind and solar resource assessment, renewable energy planning, and as atmospheric forcing for regional ocean and wave models.

<img src="./figures/taranaki_nz_ccam_figure1_domain.png" alt="Figure 1" width="600">

**Figure 1.** Taranaki New Zealand CCAM atmospheric hindcast domain extent. The model covers the Taranaki peninsula and surrounding waters at 1km resolution.

---

## Data description

**Table 1.** Data description.

| Field | Value |
|---|---|
| **Title** | Oceanum Taranaki New Zealand CCAM atmospheric hindcast |
| **Institution** | <a href="https://oceanum.io" target="_blank">Oceanum</a> |
| **Access** | <a href="https://ui.datamesh.oceanum.io/" target="_blank">Oceanum Datamesh</a> |
| **Source** | <a href="https://www.ccrc.unsw.edu.au/ccam" target="_blank">CCAM (Conformal Cubic Atmospheric Model)</a> |
| **Temporal coverage** | 2010-01-01 to 2020-01-01 |
| **Temporal resolution** | 1 hourly |
| **Spatial coverage** | [172.99E, 40.15S, 175.23E, 38.43S] at 0.01 degree (~1 km) |
| **Vertical levels** | 10m, 80m, 150m |
| **Forcing** | <a href="https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5" target="_blank">ERA5 reanalysis</a> |

### Linked Datamesh datasources

- <a href="https://ui.datamesh.oceanum.io/datasource/oceanum_meteo_taranaki_nz_ccam_v1" target="_blank">Oceanum Taranaki NZ CCAM meteo hindcast</a>

---

## Output parameters

Atmospheric variables are stored hourly over the domain at the native model resolution. Table 2 describes the key output parameters.

**Table 2.** Output parameters.

*Variable names link to the corresponding <a href="https://vocab.nerc.ac.uk/standard_name/" target="_blank">NERC Vocabulary Server</a> standard name where available.*

| Variable | Long Name | Units |
|---|---|---|
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction/" target="_blank">cfrac</a> | cloud fraction | - |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction_in_atmosphere_layer/" target="_blank">clh</a> | high cloud cover | % |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction_in_atmosphere_layer/" target="_blank">cll</a> | low cloud cover | % |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction_in_atmosphere_layer/" target="_blank">clm</a> | mid cloud cover | % |
| <a href="https://vocab.nerc.ac.uk/standard_name/cloud_area_fraction/" target="_blank">clt</a> | total cloud cover | % |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_direct_downwelling_shortwave_flux_in_air/" target="_blank">dni</a> | direct normal irradiance | W/m² |
| <a href="https://vocab.nerc.ac.uk/standard_name/specific_humidity/" target="_blank">hus</a> | water vapour mixing ratio | kg/kg |
| <a href="https://vocab.nerc.ac.uk/standard_name/humidity_mixing_ratio/" target="_blank">huss</a> | screen mixing ratio | kg/kg |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_altitude/" target="_blank">orog</a> | surface height | m |
| <a href="https://vocab.nerc.ac.uk/standard_name/precipitation_flux/" target="_blank">pr</a> | precipitation | kg/m²/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/convective_precipitation_flux/" target="_blank">prc</a> | convective precipitation | kg/m²/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/air_pressure/" target="_blank">press</a> | air pressure | hPa |
| <a href="https://vocab.nerc.ac.uk/standard_name/precipitation_flux/" target="_blank">prmax</a> | maximum precipitation rate in a timestep | kg/m²/s |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_air_pressure/" target="_blank">ps</a> | surface pressure | Pa |
| <a href="https://vocab.nerc.ac.uk/standard_name/air_pressure_at_mean_sea_level/" target="_blank">psl</a> | mean sea level pressure | Pa |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_downwelling_longwave_flux_in_air/" target="_blank">rlds</a> | LW downwelling at ground | W/m² |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_net_downward_radiative_flux/" target="_blank">rnet</a> | net radiation at surface | W/m² |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_downwelling_shortwave_flux_in_air/" target="_blank">rsds</a> | SW downwelling at ground | W/m² |
| <a href="https://vocab.nerc.ac.uk/standard_name/surface_net_downward_shortwave_flux/" target="_blank">sgn_ave</a> | SW net at ground | W/m² |
| <a href="https://vocab.nerc.ac.uk/standard_name/air_temperature/" target="_blank">ta</a> | air temperature | K |
| <a href="https://vocab.nerc.ac.uk/standard_name/dew_point_temperature/" target="_blank">td</a> | dew point temperature | K |
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

---

www.oceanum.science

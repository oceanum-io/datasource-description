NORA3 Thredds Catalog: Dataset Inventory
Source: https://thredds.met.no/thredds/projects/nora3.html
Model: HARMONIE-AROME Cy40h1.2, 3 km horizontal grid, 65 hybrid sigma-pressure vertical levels
Domain: 44°N–83°N, 30°W–85°E (Lambert conformal conic projection)
Production method (all datasets): Four 9-hour forecast cycles per day (00, 06, 12, 18 UTC). Each cycle is initialised from the previous cycle's assimilated state, corrected against surface observations (SYNOP, METAR, ships, buoys). ERA5 provides lateral boundary forcing. Subsets concatenate lead times +4 to +9 h to form a seamless hindcast time series.
License: CC-BY-4.0 / NLOD 2.0

1. NORA3 — Raw Forecast Archive
Thredds path: https://thredds.met.no/thredds/catalog/nora3/catalog.html
Overview
PropertyValueTime coverage~2007 – present (ongoing updates, ~3-month lag)Time structureIndividual files per lead time, per 6-hourly cycle, in daily foldersFile namingfc<YYYYMMDDHH>_<LT>_fp.nc, fc<YYYYMMDDHH>_<LT>.nc, fc<YYYYMMDDHH>_<LT>_sfx.nc, fc<YYYYMMDDHH>_<LT>_full_sfx.ncFile size~770 MB (model levels), ~980 MB (surface/fp), ~28 MB (sfx)Grid1489 × 889 pointsSuitable for wind turbine usePartially — requires manual assembly of lead times
1a. fc*_fp.nc — Surface and near-surface parameters (hourly)
These are the "flat-packed" surface output files, one per lead time (LT+03 to LT+09), containing near-surface variables plus wind at fixed height levels and pressure levels.
VariableDescriptionHeight / LevelUnitswind_speedWind speed10 mm/swind_directionWind direction10 mdegreesx_wind_10m, y_wind_10mWind components10 mm/sx_wind_z, y_wind_zWind components at height levels20, 50, 100, 250, 500, 750 mm/sx_wind_pl, y_wind_plWind components at pressure levels50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000 hPam/sair_temperature_plAir temperature at pressure levelsSame 16 pressure levelsKrelative_humidity_plRelative humidity at pressure levelsSame 16 pressure levels1geopotential_plGeopotential at pressure levelsSame 16 pressure levelsm²/s²upward_air_velocity_plVertical wind at pressure levelsSame 16 pressure levelsm/scloud_area_fraction_plCloud cover at pressure levelsSame 16 pressure levels1air_temperature_2mScreen-level temperature2 mKrelative_humidity_2m, specific_humidity_2mHumidity2 m–x_wind_gust_10m, y_wind_gust_10mWind gust components10 mm/sair_pressure_at_sea_levelMSLPMSLPasurface_air_pressureSurface pressure0 mPacloud_area_fractionTotal/high/mid/low cloudVarious1atmosphere_boundary_layer_thicknessPBL height–mlifting_condensation_level, atmosphere_level_of_free_convection, atmosphere_level_of_neutral_buoyancyConvective indices–mprecipitation_amount_accAccumulated precipitation (from cycle start)–kg/m²snowfall_amount_acc, rainfall_amount, snowfall_amount, graupelfall_amountPrecipitation types–kg/m²integral_of_surface_net_downward_shortwave_flux_wrt_timeAccumulated SW radiation–W·s/m²integral_of_surface_net_downward_longwave_flux_wrt_timeAccumulated LW radiation–W·s/m²downward_eastward_momentum_flux_in_air, downward_northward_momentum_flux_in_airSurface momentum flux (wind stress)–N/m²

Note for wind turbine use: x_wind_z/y_wind_z provides wind components at 20, 50, 100, 250, 500, 750 m — directly relevant. Pressure-level wind also available at 16 levels but these require geopotential-to-height conversion for use at specific AGL heights.

1b. fc*.nc — Model-level parameters (3-hourly: LT+03, LT+06, LT+09)
Full atmospheric state on all 65 hybrid sigma-pressure model levels.
VariableDescriptionLevelsUnitsx_wind_ml, y_wind_mlWind components65 hybrid model levelsm/sair_temperature_mlAir temperature65 hybrid levelsKspecific_humidity_mlSpecific humidity65 hybrid levelskg/kgturbulent_kinetic_energy_mlTKE65 hybrid levelsm²/s²cloud_area_fraction_mlCloud cover65 hybrid levels1pressure_departureNon-hydrostatic pressure departure65 hybrid levelsPasurface_air_pressureSurface pressure (needed to compute AGL heights from hybrid coords)–Pasurface_geopotentialTerrain elevation–m²/s²atmosphere_boundary_layer_thicknessPBL height–mair_pressure_at_sea_levelMSLP–Paprecipitation_amount_accAccumulated precipitation–kg/m²land_area_fractionLand/sea mask–1

Note: Hybrid levels are terrain-following near the surface and become pure pressure levels aloft. Height above ground must be computed from ap, b coefficients and surface_air_pressure. The lowest model levels are approximately 10–20 m above ground, with ~10–30 m spacing in the boundary layer.

1c. fc*_sfx.nc — SURFEX land-surface output (3-hourly)
VariableDescriptionUnitsSSTSea surface temperatureKTSSurface temperatureKT2M, Q2M, HU2M2 m temperature, specific humidity, relative humidityK / kg/kg / 1ZON10M, MER10M10 m zonal and meridional windm/sHSensible heat fluxW/m²LELatent heat fluxW/m²GFLUXGround heat fluxW/m²SICSea ice fraction1

2. NORA3_Subsets — Processed Hindcast Datasets
Thredds path: https://thredds.met.no/thredds/catalog/nora3_subset_atmos/catalog.html
All subsets are assembled by concatenating lead times +4 to +9 from each 6-hourly forecast cycle, stored as monthly netCDF4 files, with aggregated versions also available. All share the same domain, grid, and projection as the raw archive.

2a. atm_hourly_v2 — Hourly surface/boundary layer parameters
Path: nora3_subset_atmos/atm_hourly_v2/arome3km_1hr_YYYYMM.nc
PropertyValueTime coverageJanuary 1984 – present (ongoing, ~3-month lag)Time resolution1 hourFile size~20 GB/monthMulti-height windNo — wind only at 10 m
VariableDescriptionHeightUnitswind_speedWind speed10 mm/swind_directionWind direction10 mdegreesair_temperature_2mAir temperature2 mKrelative_humidity_2mRelative humidity2 m1air_pressure_at_sea_levelMSLPMSLPalow/medium/high_type_cloud_area_fractionCloud cover by level–1lifting_condensation_levelLCL height–mprecipitation_amount_hourlyHourly precipitation–kg/m²surface_net_shortwave_radiationNet surface SW flux–W/m²surface_net_longwave_radiationNet surface LW flux–W/m²fogFog fraction–0–1

For wind turbine use: Limited — wind only at 10 m. Good as a companion for surface conditions.


2b. wind_hourly_v2 — Hourly wind at multiple heights ⭐
Path: nora3_subset_atmos/wind_hourly_v2/arome3kmwind_1hr_YYYYMM.nc (full) and arome3kmwind_1hr_YYYYMM_150m.nc (150 m only)
PropertyValueTime coverageJanuary 1984 – present (ongoing, ~3-month lag)Time resolution1 hourFile size (full)~13 GB/monthFile size (150m only)~2 GB/monthMulti-height windYes — 7 levels
VariableDescriptionHeightsUnitswind_speedWind speed magnitude10, 20, 50, 100, 250, 500, 750 mm/swind_directionWind direction (met. convention)10, 20, 50, 100, 250, 500, 750 mdegrees

For wind turbine use: Excellent for hourly wind profiles. Covers all typical hub heights (100–250 m). No temperature or density — must be combined with another dataset for those. The _150m.nc variant is a compact single-height subset.


2c. atm_3hourly — 3-hourly multi-variable profiles at wind turbine heights ⭐⭐ [Recommended for wind turbine applications]
Path: nora3_subset_atmos/atm_3hourly/arome3km_3hr_YYYYMM.nc
PropertyValueTime coverageJanuary 1984 – present (ongoing, ~3-month lag)Time resolution3 hoursFile size~8 GB/monthMulti-height variablesYes — 5 levels: 50, 100, 150, 200, 300 m
VariableDescriptionHeightsUnitswind_speedWind speed50, 100, 150, 200, 300 mm/swind_directionWind direction50, 100, 150, 200, 300 mdegreesair_temperatureAir temperature50, 100, 150, 200, 300 mKrelative_humidityRelative humidity50, 100, 150, 200, 300 m%densityAir density50, 100, 150, 200, 300 mkg/m³tkeTurbulent Kinetic Energy50, 100, 150, 200, 300 mm²/s²sea_surface_temperatureSSTsurfaceK

For wind turbine use: This is the most directly applicable dataset. It provides wind speed, direction, temperature, density, and TKE all pre-interpolated to fixed heights spanning the full rotor-swept area of modern large offshore turbines (50–300 m). Air density is critical for power curve corrections. TKE is a proxy for turbulence intensity. The only trade-off is 3-hourly resolution instead of hourly.


3. Summary Comparison Table
DatasetTime CoverageΔtWind HeightsTemperatureDensityTKEPrecip/RadiationFile Size/monthNotesNORA3 raw _fp.nc~2007–present1 h (LT+4–9)10 m + 20/50/100/250/500/750 m + 16 pressure levels2 m + pressure levels✗✗✓ (accumulated)~980 MB/fileRequires assembly; full domainNORA3 raw _fp.nc (pressure levels)~2007–present1 h16 pressure levels (50–1000 hPa)✓ pressure levels✗✗✗~980 MB/fileNeeds geopotential→height conversionNORA3 raw .nc~2007–present3 h (LT+3,6,9)65 hybrid model levels✓✗ (derivable)✓✓ (accumulated)~770 MB/fileFull vertical resolution; complex coordinateatm_hourly_v21984–present1 h10 m only2 m only✗✗✓~20 GBSurface onlywind_hourly_v21984–present1 h10/20/50/100/250/500/750 m✗✗✗~13 GBBest for hourly wind profiles onlywind_hourly_v2 150m1984–present1 h150 m only✗✗✗~2 GBCompact single-height fileatm_3hourly ⭐1984–present3 h50/100/150/200/300 m✓ at all 5 heights✓ at all 5 heights✓ at all 5 heights✗~8 GBBest all-in-one for wind turbine analysis

4. Recommendation
For wind turbine rotor-layer calculations up to ~300 m, the atm_3hourly dataset (nora3_subset_atmos/atm_3hourly) is the best single-dataset choice. It is the only subset that provides wind, temperature, air density, and TKE together at multiple heights spanning exactly the range relevant for modern large offshore turbines. The 3-hour time resolution is adequate for resource assessment and most load analysis workflows.
If hourly resolution is required (e.g., for wake modelling or transient load analysis), combine wind_hourly_v2 (wind at 7 heights) with atm_hourly_v2 (surface conditions). For air density at hourly resolution, the raw _fp.nc files provide temperature and pressure at pressure levels from which density can be derived, but this requires additional processing.
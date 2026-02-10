This repository has a few documents with descriptions of our wave hindcast datasources. I would like you to analyse these documents to get context, and then create new documents for other wave hindcast datasources that need descriptions for. The datasources are specified using numerical model wrapper configs which define how the model is set up and what forcing it uses. I will provide you with a list of corresponding config files for each existing description document so you can use them as templates to understand how to create new documents.

# oceanum_sw_northamerica_wave_hindcast.pdf (https://docs.google.com/document/d/e/2PACX-1vRYzduOqxcnkvSCIfq7t2prgvahl40GQjaaLzXmTcw-GD92VnIdOUSj2IcdenG8UOZI37SMhgaGv2UE/pub)
- /config/hindcast/ontask/tasks/swan/prod/era5_northamerica/swan_era5_baja_cali.yml
- /config/hindcast/ontask/tasks/swan/prod/era5_northamerica/swan_era5_baja_ense.yml
- /config/hindcast/ontask/tasks/swan/prod/era5_northamerica/swan_era5_baja_swna.yml

# oceanum_bass_strait_wave_hindcast.pdf (https://docs.google.com/document/d/e/2PACX-1vRRA_HPnShQbK1yXG-L9OUYw-512tEoUB915lL9hFSdgO9o6BTYIGtZelMIiGD9XUgR0j7XqWwAn_2E/pub)
- /config/hindcast/ontask/tasks/swan/prod/era5_aus/swan_era5_bass.yml
- /config/hindcast/ontask/tasks/swan/prod/era5_aus/swan_era5_ebass.yml
- /config/hindcast/ontask/tasks/swan/prod/era5_aus/swan_era5_ptlan.yml

# oceanum_baltic_sea_wave_hindcast.pdf (https://docs.google.com/document/d/e/2PACX-1vS8R4kKtpzqy3U42e9FLH55HIENw5kxPltOvz5rweK_5Mrw_DDqzvPVnKG-HwPaeBgdb7n-Y0at_Dqz/pub)
- /config/hindcast/ontask/tasks/swan/prod/nora3_europe/swan_nora3_baltic.yml

# oceanum_global_wave_hindcast.pdf (https://docs.google.com/document/d/e/2PACX-1vTvOeme9NxvuZskPz5vPDUgXyD37YavvErqqgRVlxjOSJMTptO8YhXL2SewZinNewUsoUyG-by4A_GD/pub)
- /config/hindcast/ontask/tasks/ww3/glob05_prod/ww3_era5_glob05_group.yaml
- /config/hindcast/ontask/tasks/ww3/glob05_prod/ww3_era5_glob05.yaml

# oceanum_auckland_wave_forecast_specification.pdf (https://docs.google.com/document/d/e/2PACX-1vSfNvdD7hpVCcjwfVa3Wle3YMqTtRw2H3vLloeyeVM821XGGuXRcx0TkVzMpSqQsTz-nok-IFkrMss2/pub)
- /config/forecast/ontask/tasks/swan/gfs/nz/swan_gfs_akl1km.yml
- /config/forecast/ontask/tasks/swan/gfs/nz/swan_gfs_eakl.yml
- /config/forecast/ontask/tasks/swan/gfs/nz/swan_gfs_nz.yml

The WW3 configs and document are quite different from the SWAN ones, don't worry too much about them for now, most new documents will be for SWAN datasources.

Let's start with the Morocco wave hindcast. These below are the config files to get context from (there is one single nest, but two different configs because the wind forcing changes resolution after some specific year, perhaps 2003 or so). Now, the validation will be a trickier problem to solve. For now, we could make some reference to the hindcast validation app, which includes this datasource, and lets the user validate the model against satellite altimeter anywhere within the model domain. The app is here: https://hindcast-satellite-validation-main-prod.apps.oceanum.io/

- /config/hindcast/ontask/tasks/swan/prod/era5_afr/swan_era5_morocco_cmems0p25.yml
- /config/hindcast/ontask/tasks/swan/prod/era5_afr/swan_era5_morocco_cmems0p125.yml

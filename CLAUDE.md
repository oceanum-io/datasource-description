# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a Jekyll-based static site hosted at **datasets.oceanum.io** containing specification documents for Oceanum wave hindcast, wave forecast, and atmospheric hindcast datasets produced using spectral wave models (SWAN, WW3) and the CCAM atmospheric model.

## Figure Generation

To generate mean significant wave height figures for a hindcast:

```bash
cd /source/datasource-description
python scripts/generate_figures.py [config_name]
```

The script reads `FigureConfig` entries defined at the top of [scripts/generate_figures.py](scripts/generate_figures.py). Add a new config entry there before running. For ultra-high-resolution coastal domains without gridstats, use the OSM land polygon approach described in [instruction.md](instruction.md) (Section 4.2).

## Document Creation

`instruction.md` is the authoritative guide for creating new datasource documents. Key sources for document content:

- **Model configs**: `/config/hindcast/ontask/tasks/swan/prod/` (SWAN) or `/config/hindcast/ontask/tasks/ww3/` (WW3)
- **Forecast configs**: `/config/forecast/ontask/tasks/swan/`
- **Intake catalogs**: `/config/catalog/intake/hindcast/hindcast.yml`, `wavespectra/wavespectra.yml`, `forecast/forecast.yml`
- **Live data verification**: Use `oceanum.datamesh.Connector` to confirm temporal coverage and site counts

### Datasource ID patterns

- Hindcast grid: `oceanum_wave_[region]_[forcing]_v[N]_grid`
- Hindcast spectra: `oceanum_wave_[region]_[forcing]_v[N]_spec`
- Hindcast gridstats: `oceanum_wave_[region]_[forcing]_v[N]_gridstats`
- Forecast: `oceanum_wave_gfs_[region]_grid`, `oceanum_wave_ec_[region]_spec`, etc.

### After creating a document

1. Add entry to [README.md](README.md) under the appropriate section
2. Update `details` field in the relevant intake catalog(s) to `https://datasets.oceanum.io/oceanum_[region]_wave_hindcast.html` (note: `.html` extension, not `.md`)

## Document Structure

Every document follows a consistent markdown template with inline HTML styling. Use these as canonical references:

| Template | Type |
|---|---|
| [oceanum_morocco_wave_hindcast.md](oceanum_morocco_wave_hindcast.md) | ERA5 hindcast |
| [oceanum_western_europe_wave_hindcast.md](oceanum_western_europe_wave_hindcast.md) | Large domain hindcast |
| [oceanum_black_sea_wave_hindcast.md](oceanum_black_sea_wave_hindcast.md) | CFSR hindcast (dual forcing periods) |
| [oceanum_wellington_wave_hindcast.md](oceanum_wellington_wave_hindcast.md) | Specialised coastal hindcast |
| [oceanum_western_europe_wave_forecast.md](oceanum_western_europe_wave_forecast.md) | GFS/ECMWF forecast with nowcasts |

## Naming Conventions

- **Hindcast filename**: `oceanum_[region]_wave_hindcast.md`
- **Forecast filename**: `oceanum_[region]_wave_forecast.md`
- **Atmospheric hindcast filename**: `oceanum_[region]_ccam_hindcast.md`
- **Figures**: `figures/[region]_figure1_hs_mean.png` (standard) or `figures/[region]_figure1_domain.png` (coastal)
- **Datamesh UI links**: `https://ui.datamesh.oceanum.io/datasource/[datasource_id]`

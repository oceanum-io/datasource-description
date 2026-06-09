#!/usr/bin/env python3
"""
Generate interactive index maps for the README sections using Folium/Leaflet.
Produces one self-contained HTML file per section with clickable domain boxes.
"""

import json
import folium
from branca.element import MacroElement
from jinja2 import Template


BASE_URL = "https://datasets.oceanum.io"

# ── Domain definitions ────────────────────────────────────────────────────────
# Each entry: (label, x0, y0, x1, y1, document_slug)

HINDCAST_DOMAINS = [
    # Global
    ("Global ERA5",              -180.0, -77.5,  180.0,  77.5,  "oceanum_global_wave_hindcast"),
    # ERA5 Regional
    ("Arabian/Persian Gulf ERA5",  47.5,  22.5,   60.5,  31.0,  "oceanum_arabian_persian_gulf_wave_hindcast"),
    ("Bass Strait ERA5",          143.0, -40.5,  152.0, -36.0,  "oceanum_bass_strait_wave_hindcast"),
    ("King Island ERA5",          143.6, -40.4,  144.4, -39.4,  "oceanum_king_island_wave_hindcast"),
    ("Malay Peninsula ERA5",       99.0,   4.0,  104.5,   8.5,  "oceanum_malay_peninsula_wave_hindcast"),
    ("Mediterranean ERA5",         -5.5,  30.3,   36.2,  45.9,  "oceanum_mediterranean_wave_hindcast"),
    ("Morocco ERA5",              -19.0,  22.0,   -6.0,  38.0,  "oceanum_morocco_wave_hindcast"),
    ("New Zealand ERA5",          165.0, -48.0,  180.0, -34.0,  "oceanum_new_zealand_era5_wave_hindcast"),
    ("Peru ERA5",                 -79.0, -13.0,  -76.0, -10.0,  "oceanum_peru_wave_hindcast"),
    ("Red Sea ERA5",               32.5,  10.0,   56.0,  30.0,  "oceanum_red_sea_wave_hindcast"),
    ("SW North America ERA5",    -130.0,  25.0, -117.0,  40.0,  "oceanum_sw_northamerica_wave_hindcast"),
    ("Taiwan ERA5",               116.5,  21.0,  123.0,  26.5,  "oceanum_taiwan_wave_hindcast"),
    ("US East Coast ERA5",        -77.5,  35.5,  -63.0,  46.0,  "oceanum_us_east_coast_wave_hindcast"),
    ("West Africa ERA5",            2.5,  -2.0,   10.0,   6.5,  "oceanum_west_africa_wave_hindcast"),
    ("Western Europe ERA5",       -11.0,  48.5,   13.0,  61.0,  "oceanum_western_europe_wave_hindcast"),
    # CFSR
    ("Black Sea CFSR",             27.3,  40.8,   41.9,  46.7,  "oceanum_black_sea_wave_hindcast"),
    # NORA3
    ("Baltic Sea NORA3",            8.0,  53.0,   30.0,  66.0,  "oceanum_baltic_sea_wave_hindcast"),
    ("Waddenzee NORA3",             4.5,  52.85,   6.4,  53.6,  "oceanum_waddenzee_nora3_wave_hindcast"),
    ("Western Europe NORA3",      -11.0,  48.5,   13.0,  61.0,  "oceanum_western_europe_nora3_wave_hindcast"),
    # Specialised Coastal
    ("Bluff Harbour",             168.29, -46.67, 168.53, -46.53, "oceanum_bluff_wave_hindcast"),
    ("Wellington",                174.75, -41.40, 174.92, -41.22, "oceanum_wellington_wave_hindcast"),
]

FORECAST_DOMAINS = [
    # Global
    ("Global Forecast",          -180.0, -77.5,  180.0,  77.5,  "oceanum_global_wave_forecast"),
    # GFS + ECMWF
    ("NW Cape",                   112.0, -27.0,  117.5, -20.0,  "oceanum_northwest_cape_wave_forecast"),
    ("SW Western Australia",      112.0, -34.0,  116.5, -27.0,  "oceanum_sw_western_australia_wave_forecast"),
    ("Western Europe",            -11.0,  48.5,   13.0,  61.0,  "oceanum_western_europe_wave_forecast"),
    # GFS
    ("New Zealand",               165.0, -48.0,  180.0, -34.0,  "oceanum_new_zealand_wave_forecast"),
    ("Auckland",                  173.5, -37.5,  176.5, -35.5,  "oceanum_auckland_wave_forecast_specification"),
    # ECMWF
    ("Baltic Sea",                  9.0,  53.8,   30.3,  66.0,  "oceanum_baltic_sea_wave_forecast"),
    ("Dutch Coast",                 3.0,  51.4,    4.75, 53.05, "oceanum_dutch_wave_forecast"),
    ("Gabon",                       5.0,  -6.0,   12.5,   3.0,  "oceanum_gabon_wave_forecast"),
    ("Nigeria",                     2.5,  -2.0,   10.0,   6.5,  "oceanum_nigeria_wave_forecast"),
    ("US East Coast",             -77.5,  35.5,  -63.0,  46.0,  "oceanum_us_east_coast_wave_forecast"),
]

CCAM_DOMAINS = [
    ("Central NZ",                172.08, -42.22, 175.92, -38.38, "oceanum_central_nz_ccam_hindcast"),
    ("Marlborough Sounds",        172.99, -40.15, 175.23, -38.43, "oceanum_marlborough_sounds_ccam_hindcast"),
    ("Southland NZ",              166.00, -48.44, 170.23, -45.56, "oceanum_southland_nz_ccam_hindcast"),
    ("Taranaki NZ",               173.23, -41.65, 174.75, -40.50, "oceanum_taranaki_nz_ccam_hindcast"),
]

# tab20-inspired hex palette for regional domains
COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
]
GLOBAL_COLOR = "#999999"


# ── Leaflet GeoJSON layer injected via MacroElement ───────────────────────────

INSET_STEP = 0.4  # degrees to inset each successive domain with identical bounds


class DomainLayer(MacroElement):
    """
    Injects two Leaflet GeoJSON layers:
    - Global domains: decorative only, non-interactive (no event capture).
    - Regional domains: interactive hover + click-to-URL.
    Domains sharing the same bounding box are progressively inset so all
    borders remain visible and independently clickable.
    """

    _template = Template("""
    {% macro script(this, kwargs) %}
    (function() {
        var map = {{ this._parent.get_name() }};

        // ── Global domains: visual indicator only, no mouse events ──────────
        L.geoJSON({{ this.global_geojson }}, {
            interactive: false,
            style: function() {
                return {
                    fillColor: "#999", fillOpacity: 0.04,
                    color: "#999", weight: 1.0, dashArray: "6 4",
                };
            }
        }).addTo(map);

        // ── Regional domains: hover + click ──────────────────────────────────
        var regional = L.geoJSON({{ this.regional_geojson }}, {
            style: function(feature) {
                return {
                    fillColor:   feature.properties.color,
                    fillOpacity: 0.18,
                    color:       feature.properties.color,
                    weight:      2.0,
                };
            },
            onEachFeature: function(feature, lyr) {
                var p = feature.properties;
                lyr.bindTooltip(
                    '<div style="font-family:Poppins,sans-serif;font-size:13px;'
                    + 'font-weight:600;color:#0b2d40;line-height:1.4">'
                    + p.name
                    + '<div style="font-size:10px;font-weight:400;color:#666;'
                    + 'margin-top:2px">Click to open dataset ↗</div></div>',
                    {sticky: true, opacity: 1}
                );
                lyr.on({
                    mouseover: function() {
                        lyr.setStyle({fillOpacity: 0.38, weight: 3.5});
                    },
                    mouseout: function() { regional.resetStyle(lyr); },
                    click:    function() { window.open(p.url, "_blank"); },
                });
            }
        }).addTo(map);
    })();
    {% endmacro %}
    """)

    def __init__(self, domains):
        super().__init__()
        self._name = "DomainLayer"

        global_features = []
        regional_features = []

        # Sort regional domains largest-first so smaller ones are rendered last
        # (later in SVG = on top), making them permanently accessible.
        # Global domains are kept in original order for the background layer.
        def area(d):
            return (d[3] - d[1]) * abs(d[4] - d[2])

        sorted_domains = (
            [d for d in domains if (d[3] - d[1]) > 300] +          # globals first
            sorted([d for d in domains if (d[3] - d[1]) <= 300],    # regionals by area desc
                   key=area, reverse=True)
        )

        # Track how many domains share the same bounding box so we can inset
        seen_bounds = {}  # rounded-bounds key → inset count
        color_idx = 0

        # Preserve original color assignment order (by list position, not sort order)
        color_map = {
            name: COLORS[i % len(COLORS)]
            for i, (name, x0, y0, x1, y1, slug) in enumerate(
                d for d in domains if (d[3] - d[1]) <= 300
            )
        }

        for name, x0, y0, x1, y1, slug in sorted_domains:
            is_global = (x1 - x0) > 300
            url = f"{BASE_URL}/{slug}.html"

            if is_global:
                global_features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[x0,y0],[x1,y0],[x1,y1],[x0,y1],[x0,y0]]],
                    },
                    "properties": {"name": name},
                })
            else:
                color = color_map[name]

                # Inset overlapping domains so their borders stay distinct
                key = f"{round(x0,1)},{round(y0,1)},{round(x1,1)},{round(y1,1)}"
                n = seen_bounds.get(key, 0)
                seen_bounds[key] = n + 1
                d = n * INSET_STEP
                ix0, iy0, ix1, iy1 = x0 + d, y0 + d, x1 - d, y1 - d

                regional_features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[ix0,iy0],[ix1,iy0],[ix1,iy1],[ix0,iy1],[ix0,iy0]]],
                    },
                    "properties": {"name": name, "url": url, "color": color},
                })

        self.global_geojson   = json.dumps({"type": "FeatureCollection", "features": global_features})
        self.regional_geojson = json.dumps({"type": "FeatureCollection", "features": regional_features})


# ── Map builder ───────────────────────────────────────────────────────────────

def make_map(domains, center, zoom, output_path):
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="CartoDB positron",
        prefer_canvas=True,
    )
    m.get_root().header.add_child(folium.Element(
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Poppins:wght@400;600&display=swap">'
    ))
    m.add_child(DomainLayer(domains))
    m.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    base = "/source/datasource-description/figures"

    make_map(
        HINDCAST_DOMAINS,
        center=[20, 10], zoom=2,
        output_path=f"{base}/index_wave_hindcast.html",
    )
    make_map(
        FORECAST_DOMAINS,
        center=[20, 10], zoom=2,
        output_path=f"{base}/index_wave_forecast.html",
    )
    make_map(
        CCAM_DOMAINS,
        center=[-43, 173], zoom=6,
        output_path=f"{base}/index_atmospheric_hindcast.html",
    )
